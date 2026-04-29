"""
run_pipeline.py
Orchestrate the full RAG pipeline end-to-end, or query an existing index.

Usage:
  # Build index from scratch (steps 1 → 4):
  python run_pipeline.py --build

  # Build for a specific use-case:
  python run_pipeline.py --build --use-case editorial

  # Dry-run: show what would be executed without running anything:
  python run_pipeline.py --build --dry-run
  # Query an already-built index:
  python run_pipeline.py --query "What did we publish about climate?"

  # Build + query in one call:
  python run_pipeline.py --build --query "What did we publish about climate?"

  # Force a specific LLM tier:
  python run_pipeline.py --query "..." --tier 1
  python run_pipeline.py --query "..." --tier 2
  python run_pipeline.py --query "..." --tier 3
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("run_pipeline")

SCRIPTS = PROJECT_ROOT / "scripts"
PYTHON = sys.executable


def _run_step(script: str, extra_args: list[str] | None = None) -> None:
    """Run a pipeline step script as a subprocess and propagate errors."""
    cmd = [PYTHON, str(SCRIPTS / script)] + (extra_args or [])
    logger.info("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        logger.error("Step failed: %s (exit code %d)", script, result.returncode)
        sys.exit(result.returncode)


def _dry_run_build(use_case: str | None) -> None:
    from src.utils.config import load_config, get_corpus_dir, get_checkpoint_dir, get_index_dir

    cfg = load_config()
    uc = use_case or cfg["active_use_case"]
    corpus_dir = get_corpus_dir(uc)
    checkpoint_dir = get_checkpoint_dir(uc)
    index_dir = get_index_dir(uc)

    print("\n=== DRY-RUN — build index ===")
    print(f"  use_case       : {uc}")
    print(f"  corpus_dir     : {corpus_dir}")
    print(f"  checkpoint_dir : {checkpoint_dir}")
    print(f"  index_dir      : {index_dir}")
    print(f"  embeddings     : {cfg['embeddings']['provider']} / {cfg['embeddings']['model']}")
    print()
    steps = [
        ("Step 1 — Ingest",  "scan corpus → step_1_documents.json"),
        ("Step 2 — Parse",   "spaCy + business rules → step_2_chunks.json"),
        ("Step 3 — Embed",   f"embed chunks → step_3_embeddings.npy  [{cfg['embeddings']['provider']}]"),
        ("Step 4 — Index",   "build FAISS index → index.faiss + chunks.json"),
    ]
    for name, desc in steps:
        print(f"  [{name}] {desc}")
    print("\n  (nothing executed — remove --dry-run to run)")


def _dry_run_query(query: str, use_case: str | None, tier: int | None) -> None:
    from src.utils.config import load_config, get_index_dir

    cfg = load_config()
    uc = use_case or cfg["active_use_case"]
    index_dir = get_index_dir(uc)
    tier_label = {1: "Tier 1 (template)", 2: "Tier 2 (Ollama)", 3: "Tier 3 (Azure)"}.get(
        tier or 0, f"auto ({cfg['llm']['provider']} / {cfg['llm']['model']})"
    )
    print("\n=== DRY-RUN — query ===")
    print(f"  query      : {query}")
    print(f"  use_case   : {uc}")
    print(f"  index_dir  : {index_dir}")
    print(f"  LLM tier   : {tier_label}")
    print("\n  (nothing executed — remove --dry-run to run)")


def build_index(use_case: str | None = None) -> None:
    """Run steps 1 → 4 to build the FAISS index."""
    extra = (["--use-case", use_case] if use_case else [])

    logger.info("=== Step 1 — Ingest ===")
    _run_step("step_1_001_ingest.py", extra)

    logger.info("=== Step 2 — Parse ===")
    _run_step("step_2_001_parse.py", extra)

    logger.info("=== Step 3 — Embed ===")
    _run_step("step_3_001_embed.py", extra)

    logger.info("=== Step 4 — Index ===")
    _run_step("step_4_001_index.py", extra)

    logger.info("Index build complete.")


def query_index(query: str, use_case: str | None = None, tier: int | None = None) -> None:
    """Run step 6 (synthesize) which internally calls step 5 (query)."""
    extra: list[str] = ["--query", query]
    if use_case:
        extra += ["--use-case", use_case]
    if tier:
        extra += ["--tier", str(tier)]
    _run_step("step_6_001_synthesize.py", extra)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RAG pipeline — build index and/or query corpus"
    )
    parser.add_argument("--build", action="store_true",
                        help="Build the FAISS index (steps 1–4)")
    parser.add_argument("--use-case", type=str, default=None,
                        help="Override active_use_case from config.yaml")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be executed without running anything")
    parser.add_argument("--query", type=str, default=None,
                        help="Question to send to the RAG pipeline (uses step 6)")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3], default=None,
                        help="Force LLM tier (1=template, 2=Ollama, 3=Azure)")
    args = parser.parse_args()

    if not args.build and args.query is None:
        parser.print_help()
        sys.exit(0)

    if args.build:
        if args.dry_run:
            _dry_run_build(args.use_case)
        else:
            build_index(use_case=args.use_case)

    if args.query:
        if args.dry_run:
            _dry_run_query(args.query, args.use_case, args.tier)
        else:
            query_index(args.query, use_case=args.use_case, tier=args.tier)


if __name__ == "__main__":
    main()
