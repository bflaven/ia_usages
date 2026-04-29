"""
Step 5 — Query
--------------
Embeds a question, searches the FAISS index, applies retrieval business rules
and score boosts, then optionally re-ranks with a cross-encoder (E2).

Can be run standalone (interactive CLI) or imported by the interface step.

Run standalone:
    python scripts/step_5_001_query.py --query "What did we publish about climate?"
    python scripts/step_5_001_query.py           # interactive mode
    python scripts/step_5_001_query.py --use-case editorial --no-rerank
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.llm.embeddings import EmbeddingClient
from src.llm.reranker import get_reranker
from src.vector_store.faiss_store import FAISSStore, SearchResult
from src.utils.config import load_config, get_index_dir, get_logs_dir

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_RETRIEVAL_RULES_PATH = _PROJECT_ROOT / "config" / "retrieval_rules.yaml"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logging(logs_dir: Path) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / "step_5_query.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step5")


# ---------------------------------------------------------------------------
# Retrieval rules
# ---------------------------------------------------------------------------

def _load_retrieval_rules(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def _match_rule(query: str, rules: dict) -> Optional[dict]:
    """Return first rule whose query_contains_any matches the query."""
    query_lower = query.lower()
    for rule in rules.get("rules", []):
        keywords = rule.get("when", {}).get("query_contains_any", [])
        if any(k.lower() in query_lower for k in keywords):
            return rule
    return None


# ---------------------------------------------------------------------------
# Boost logic
# ---------------------------------------------------------------------------

def _recency_score(published_at: str) -> float:
    """
    Normalised recency score in [0, 1].
    Documents published in the last 30 days → 1.0, decays over 365 days.
    """
    if not published_at:
        return 0.5
    try:
        pub = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        days_old = max(0, (now - pub).days)
        return max(0.0, 1.0 - days_old / 365.0)
    except Exception:
        return 0.5


def _apply_boosts(results: list[SearchResult], boost_cfg: dict) -> list[SearchResult]:
    """Multiply cosine scores by configured boost factors, then re-sort."""
    if not boost_cfg:
        return results

    ext_boosts: dict = boost_cfg.get("source_extension", {})
    meta_boosts: dict = boost_cfg.get("metadata_field", {})

    for r in results:
        # Extension boost
        if ext_boosts:
            ext = Path(r.metadata.get("source_file", r.source)).suffix.lstrip(".").lower()
            factor = ext_boosts.get(ext, 1.0)
            r.score *= factor

        # Recency boost
        if "recency" in meta_boosts:
            rec = _recency_score(r.metadata.get("published_at", ""))
            r.score *= 1.0 + (meta_boosts["recency"] - 1.0) * rec

    results.sort(key=lambda r: r.score, reverse=True)
    return results


# ---------------------------------------------------------------------------
# Filter logic
# ---------------------------------------------------------------------------

def _apply_filters(results: list[SearchResult], filters: dict) -> list[SearchResult]:
    """Keep only results matching the doc_type filter (if specified)."""
    doc_types = filters.get("doc_type")
    if not doc_types:
        return results
    return [r for r in results if r.metadata.get("doc_type") in doc_types]


# ---------------------------------------------------------------------------
# Core query function (importable by step 7)
# ---------------------------------------------------------------------------

def run_query(
    question: str,
    config: dict,
    store: FAISSStore,
    embedding_client: EmbeddingClient,
    retrieval_rules: Optional[dict] = None,
    force_k: Optional[int] = None,
    force_threshold: Optional[float] = None,
    rerank: bool = True,
) -> list[SearchResult]:
    """
    Full query pipeline: embed → retrieve → filter → boost → rerank.

    Args:
        question:         user question string
        config:           loaded config.yaml
        store:            loaded FAISSStore
        embedding_client: initialised EmbeddingClient
        retrieval_rules:  loaded retrieval_rules.yaml (or None)
        force_k:          override k (ignores config and rules)
        force_threshold:  override score_threshold
        rerank:           whether to apply cross-encoder (E2)

    Returns:
        list of SearchResult, sorted by score descending
    """
    retrieval_cfg = config.get("retrieval", {})
    use_rules = retrieval_cfg.get("enable_business_rules", False) and retrieval_rules is not None
    rerank_cfg = retrieval_cfg.get("rerank", {})

    # Defaults
    k = force_k or retrieval_cfg.get("k", 5)
    threshold = force_threshold if force_threshold is not None else retrieval_cfg.get("score_threshold", 0.2)
    filters: dict = {}
    boost_cfg: dict = {}

    # Apply matching rule
    if use_rules:
        rule = _match_rule(question, retrieval_rules)
        if rule:
            logger.info("Retrieval rule matched: '%s'", rule["id"])
            params = rule.get("params", {})
            k = force_k or params.get("k", k)
            threshold = force_threshold if force_threshold is not None else params.get("score_threshold", threshold)
            filters = rule.get("filters", {})
            boost_cfg = rule.get("boost", {})

    # Embed query
    query_vector = embedding_client.embed_one(question)

    # Search (retrieve more than k to allow for filter/boost losses)
    fetch_k = max(k * 3, 20)
    results = store.search(query_vector, k=fetch_k, score_threshold=0.0)

    # Filter by doc_type
    if filters:
        results = _apply_filters(results, filters)

    # Score threshold after filter
    results = [r for r in results if r.score >= threshold]

    # Boosts
    if boost_cfg:
        results = _apply_boosts(results, boost_cfg)

    # Re-rank (E2)
    if rerank and rerank_cfg.get("enabled", False) and results:
        model_name = rerank_cfg.get("model", "cross-encoder/ms-marco-MiniLM-L-6-v2")
        reranker = get_reranker(model_name)
        results = reranker.rerank(question, results)

    return results[:k]


# ---------------------------------------------------------------------------
# CLI / interactive mode
# ---------------------------------------------------------------------------

def _print_results(results: list[SearchResult]) -> None:
    if not results:
        print("\n  No results above threshold.\n")
        return
    print(f"\n  {len(results)} result(s):\n")
    for i, r in enumerate(results, 1):
        meta = r.metadata
        print(f"  [{i}] score={r.score:.4f}  chunk={r.chunk_id}")
        if meta.get("title"):
            print(f"      title : {meta['title']}")
        if meta.get("author"):
            print(f"      author: {meta['author']}")
        if meta.get("published_at"):
            print(f"      date  : {meta['published_at'][:10]}")
        print(f"      text  : {r.text[:200]}{'...' if len(r.text) > 200 else ''}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Step 5 — Query the FAISS index")
    parser.add_argument("--query", "-q", help="Question to ask (omit for interactive mode)")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    parser.add_argument("--no-rerank", action="store_true", help="Skip cross-encoder re-ranking")
    parser.add_argument("--k", type=int, help="Override number of results")
    parser.add_argument("--threshold", type=float, help="Override score threshold")
    args = parser.parse_args()

    logs_dir = get_logs_dir()
    _setup_logging(logs_dir)

    config = load_config()
    index_dir = get_index_dir(args.use_case)
    use_case = args.use_case or config["active_use_case"]

    logger.info("=== Step 5 — Query ===")
    logger.info("Use case  : %s", use_case)
    logger.info("Index dir : %s", index_dir)

    # Load index
    try:
        store = FAISSStore.load(index_dir)
    except FileNotFoundError as exc:
        logger.error("%s\nRun step_4_001_index.py first.", exc)
        sys.exit(1)

    # Init embedding client
    embedding_client = EmbeddingClient.from_config(config)

    # Load retrieval rules
    retrieval_rules = None
    if config.get("retrieval", {}).get("enable_business_rules") and _RETRIEVAL_RULES_PATH.exists():
        retrieval_rules = _load_retrieval_rules(_RETRIEVAL_RULES_PATH)
        logger.info("Retrieval rules loaded from %s", _RETRIEVAL_RULES_PATH)

    rerank = not args.no_rerank

    # Single query mode
    if args.query:
        results = run_query(
            args.query, config, store, embedding_client,
            retrieval_rules=retrieval_rules,
            force_k=args.k,
            force_threshold=args.threshold,
            rerank=rerank,
        )
        _print_results(results)
        return

    # Interactive mode
    print(f"\nRAG query — use case: {use_case}  |  index: {store.size} chunks")
    print("Type your question and press Enter. Type 'exit' to quit.\n")
    while True:
        try:
            question = input("Question> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("Bye.")
            break
        results = run_query(
            question, config, store, embedding_client,
            retrieval_rules=retrieval_rules,
            force_k=args.k,
            force_threshold=args.threshold,
            rerank=rerank,
        )
        _print_results(results)


if __name__ == "__main__":
    main()
