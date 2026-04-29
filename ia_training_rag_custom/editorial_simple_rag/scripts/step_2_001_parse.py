"""
Step 2 — Parse and Chunk
------------------------
Reads the Step 1 checkpoint, splits each document into overlapping chunks
using spaCy sentence boundaries (French) or regex fallback (other languages),
and applies chunking_rules.yaml if enable_business_rules is true.

Writes: data/checkpoints/<use_case>/<corpus_id>/step_2_chunks.json

Run standalone:
    python scripts/step_2_001_parse.py
    python scripts/step_2_001_parse.py --use-case editorial
"""

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.parsing.chunker import chunk_all_documents
from src.utils.config import (
    load_config,
    get_checkpoint_dir,
    get_logs_dir,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_RULES_PATH = _PROJECT_ROOT / "config" / "chunking_rules.yaml"


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
            logging.FileHandler(logs_dir / "step_2_parse.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step2")


# ---------------------------------------------------------------------------
# Checkpoint I/O
# ---------------------------------------------------------------------------

def load_step1_checkpoint(checkpoint_dir: Path) -> list[dict]:
    path = checkpoint_dir / "step_1_documents.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Step 1 checkpoint not found: {path}\nRun step_1_001_ingest.py first."
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_checkpoint(chunks: list[dict], checkpoint_dir: Path) -> Path:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    out_path = checkpoint_dir / "step_2_chunks.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    logger.info("Checkpoint saved → %s (%d chunks)", out_path, len(chunks))
    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 2 — Parse and chunk documents")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    args = parser.parse_args()

    logs_dir = get_logs_dir()
    _setup_logging(logs_dir)

    config = load_config()
    checkpoint_dir = get_checkpoint_dir(args.use_case)
    use_case = args.use_case or config["active_use_case"]

    logger.info("=== Step 2 — Parse and Chunk ===")
    logger.info("Use case      : %s", use_case)
    logger.info("Checkpoint dir: %s", checkpoint_dir)
    logger.info(
        "Chunk size=%d  overlap=%.0f%%  min_tokens=%d  business_rules=%s",
        config["chunking"]["size"],
        config["chunking"]["overlap"] * 100,
        config["chunking"]["min_tokens"],
        config["chunking"]["enable_business_rules"],
    )

    # Load step 1 output
    try:
        documents = load_step1_checkpoint(checkpoint_dir)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Loaded %d document(s) from step 1", len(documents))

    # Chunk
    chunks = chunk_all_documents(documents, config, rules_path=_RULES_PATH)

    if not chunks:
        logger.warning("No chunks produced — check documents and chunking config.")
        sys.exit(0)

    # Stats
    avg_tokens = sum(c["metadata"]["tokens"] for c in chunks) / len(chunks)
    logger.info(
        "Produced %d chunk(s) from %d document(s) — avg %.0f tokens/chunk",
        len(chunks), len(documents), avg_tokens,
    )

    save_checkpoint(chunks, checkpoint_dir)
    logger.info("Step 2 done.")


if __name__ == "__main__":
    main()
