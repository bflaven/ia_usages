"""
Step 6 — Synthesize
--------------------
Takes a question and the retrieved chunks from step 5, builds a prompt,
calls the LLM (Tier 1 / 2 / 3), and returns a structured answer with
source references.

Can be run standalone or imported by the interface step.

Run standalone:
    python scripts/step_6_001_synthesize.py --query "What did we publish about climate?"
    python scripts/step_6_001_synthesize.py --tier 1 --query "..."
    python scripts/step_6_001_synthesize.py --use-case editorial --query "..."
"""

import argparse
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.llm.llm_client import LLMClient
from src.llm.embeddings import EmbeddingClient
from src.llm.reranker import get_reranker
from src.vector_store.faiss_store import FAISSStore, SearchResult
from src.utils.config import load_config, get_index_dir, get_logs_dir

# Step 5 is imported as a library function
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))
from scripts.step_5_001_query import run_query, _load_retrieval_rules

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
            logging.FileHandler(logs_dir / "step_6_synthesize.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step6")


# ---------------------------------------------------------------------------
# Answer dataclass
# ---------------------------------------------------------------------------

@dataclass
class Answer:
    question: str
    text: str
    tier: int
    sources: list[dict] = field(default_factory=list)
    from_cache: bool = False

    def print(self) -> None:
        tier_label = {1: "Tier 1 (static)", 2: "Tier 2 (Ollama)", 3: "Tier 3 (Azure)"}
        print(f"\n{'='*60}")
        print(f"Q: {self.question}")
        print(f"{'='*60}")
        print(f"\n{self.text}\n")
        print(f"{'—'*60}")
        print(f"Tier: {tier_label.get(self.tier, self.tier)}"
              + ("  [from cache]" if self.from_cache else ""))
        if self.sources:
            print(f"\nSources ({len(self.sources)}):")
            for s in self.sources:
                score = f"{s['score']:.4f}" if isinstance(s.get('score'), float) else s.get('score', '')
                title = s.get('title') or s.get('source', '')
                author = f"  by {s['author']}" if s.get('author') else ''
                date = f"  ({s['date'][:10]})" if s.get('date') else ''
                print(f"  • [{score}] {title}{author}{date}")
        print()


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer the question using ONLY the provided context. "
    "Be concise and factual. If the context does not contain enough information, say so. "
    "Always cite which source(s) you are drawing from."
)

_MAX_CONTEXT_TOKENS = 3000   # rough word-count cap for context block


def _build_prompt(question: str, results: list[SearchResult]) -> str:
    context_parts = []
    total_words = 0

    for i, r in enumerate(results, 1):
        meta = r.metadata
        header_parts = [f"[Source {i}]"]
        if meta.get("title"):
            header_parts.append(f"Title: {meta['title']}")
        if meta.get("author"):
            header_parts.append(f"Author: {meta['author']}")
        if meta.get("published_at"):
            header_parts.append(f"Date: {meta['published_at'][:10]}")

        block = "\n".join(header_parts) + f"\n{r.text}"
        words = len(block.split())

        if total_words + words > _MAX_CONTEXT_TOKENS:
            logger.debug("Context truncated at source %d (token budget reached)", i)
            break

        context_parts.append(block)
        total_words += words

    context = "\n\n---\n\n".join(context_parts)
    return (
        f"Context:\n\n{context}\n\n"
        f"---\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )


# ---------------------------------------------------------------------------
# Tier 1 — static template
# ---------------------------------------------------------------------------

def _tier1_answer(question: str, results: list[SearchResult]) -> str:
    if not results:
        return "No relevant documents found for your question."

    lines = [f"Based on {len(results)} retrieved passage(s):\n"]
    for i, r in enumerate(results, 1):
        meta = r.metadata
        title = meta.get("title", r.source)
        author = f" by {meta['author']}" if meta.get("author") else ""
        date = f" ({meta['published_at'][:10]})" if meta.get("published_at") else ""
        lines.append(f"  {i}. {title}{author}{date} [score: {r.score:.3f}]")
        lines.append(f"     {r.text[:200]}{'...' if len(r.text) > 200 else ''}\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core synthesize function (importable by step 7)
# ---------------------------------------------------------------------------

def synthesize(
    question: str,
    results: list[SearchResult],
    config: dict,
    tier: Optional[int] = None,
) -> Answer:
    """
    Generate an answer from retrieved results.

    Args:
        question: user question
        results:  ranked SearchResult list from step 5
        config:   loaded config.yaml
        tier:     force LLM tier (1/2/3); None = use config

    Returns:
        Answer dataclass
    """
    # Resolve tier
    if tier is None:
        llm_cfg = config.get("llm", {})
        provider = llm_cfg.get("provider", "ollama")
        tier = 2 if provider == "ollama" else 3

    # Source references
    sources = [
        {
            "chunk_id": r.chunk_id,
            "source": r.source,
            "title": r.metadata.get("title", ""),
            "author": r.metadata.get("author", ""),
            "date": r.metadata.get("published_at", ""),
            "score": r.score,
            "tags": r.metadata.get("tags", []),
        }
        for r in results
    ]

    # Tier 1 — no LLM call
    if tier == 1:
        return Answer(
            question=question,
            text=_tier1_answer(question, results),
            tier=1,
            sources=sources,
        )

    # Tier 2 / 3 — LLM call
    if not results:
        return Answer(
            question=question,
            text="No relevant documents found for your question.",
            tier=tier,
            sources=[],
        )

    prompt = _build_prompt(question, results)

    try:
        llm = LLMClient.from_config(config)
        text = llm.complete(prompt, system=_SYSTEM_PROMPT)
        logger.info("LLM response: %d words (tier %d, model=%s)", len(text.split()), tier, llm.model)
    except Exception as exc:
        logger.error("LLM call failed: %s", exc)
        # Graceful degradation to Tier 1
        logger.warning("Falling back to Tier 1 (static template)")
        return Answer(
            question=question,
            text=_tier1_answer(question, results),
            tier=1,
            sources=sources,
        )

    return Answer(question=question, text=text, tier=tier, sources=sources)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 6 — Synthesize an answer")
    parser.add_argument("--query", "-q", required=True, help="Question to answer")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3], help="Force LLM tier")
    parser.add_argument("--no-rerank", action="store_true", help="Skip cross-encoder re-ranking")
    parser.add_argument("--k", type=int, help="Override number of retrieved chunks")
    args = parser.parse_args()

    logs_dir = get_logs_dir()
    _setup_logging(logs_dir)

    config = load_config()
    index_dir = get_index_dir(args.use_case)
    use_case = args.use_case or config["active_use_case"]

    logger.info("=== Step 6 — Synthesize ===")
    logger.info("Use case : %s", use_case)
    logger.info("Query    : %s", args.query)
    logger.info("Tier     : %s", args.tier or "auto")

    # Load index
    try:
        store = FAISSStore.load(index_dir)
    except FileNotFoundError as exc:
        logger.error("%s\nRun step_4_001_index.py first.", exc)
        sys.exit(1)

    # Init clients
    embedding_client = EmbeddingClient.from_config(config)

    # Load retrieval rules
    retrieval_rules = None
    if config.get("retrieval", {}).get("enable_business_rules") and _RETRIEVAL_RULES_PATH.exists():
        retrieval_rules = _load_retrieval_rules(_RETRIEVAL_RULES_PATH)

    # Step 5 — retrieve
    results = run_query(
        args.query,
        config,
        store,
        embedding_client,
        retrieval_rules=retrieval_rules,
        force_k=args.k,
        rerank=not args.no_rerank,
    )
    logger.info("Retrieved %d chunk(s)", len(results))

    # Step 6 — synthesize
    answer = synthesize(args.query, results, config, tier=args.tier)
    answer.print()


if __name__ == "__main__":
    main()
