"""
Step 1 — Ingest
---------------
Reads all supported files from the active corpus directory,
runs basic cleaning and language detection, and saves a
checkpoint JSON for the next step.

Run standalone:
    python scripts/step_1_001_ingest.py
    python scripts/step_1_001_ingest.py --use-case editorial
    python scripts/step_1_001_ingest.py --corpus-dir path/to/dir
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingestion.readers import read_file, READERS
from src.utils.config import load_config, get_corpus_dir, get_checkpoint_dir, get_logs_dir

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
            logging.FileHandler(logs_dir / "step_1_ingest.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step1")


# ---------------------------------------------------------------------------
# Cleaning helpers
# ---------------------------------------------------------------------------

_WHITESPACE_RE = re.compile(r"\s+")


def _clean_text(text: str) -> str:
    """Collapse multiple whitespace, strip leading/trailing."""
    return _WHITESPACE_RE.sub(" ", text).strip()


def _detect_language(text: str, hint: str = "en") -> str:
    """
    Lightweight language detection.
    Uses langdetect if available, otherwise returns the hint.
    """
    try:
        from langdetect import detect
        return detect(text[:500]) if text else hint
    except Exception:
        return hint


# ---------------------------------------------------------------------------
# Core ingest logic
# ---------------------------------------------------------------------------

def ingest_corpus(corpus_dir: Path, default_language: str = "en") -> list[dict]:
    """
    Walk corpus_dir recursively and ingest all supported files.
    Returns a list of document dicts: {text, source, metadata}.
    """
    supported_exts = set(READERS.keys())
    documents = []
    files_found = 0
    files_skipped = 0

    for file_path in sorted(corpus_dir.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in supported_exts:
            files_skipped += 1
            logger.debug("Skipping unsupported file: %s", file_path)
            continue

        files_found += 1
        logger.info("Ingesting: %s", file_path.relative_to(corpus_dir))

        try:
            docs = read_file(str(file_path))
        except Exception as exc:
            logger.error("Failed to read %s: %s", file_path, exc)
            continue

        for doc in docs:
            doc["text"] = _clean_text(doc["text"])
            if not doc["text"]:
                continue
            # Fill in language if not set by reader.
            # When default_language is set in config.yaml (spacy.default_language),
            # force it for all documents — avoids loading multiple spaCy models
            # for a corpus that is known to be in one language.
            if not doc["metadata"].get("language"):
                if default_language:
                    doc["metadata"]["language"] = default_language
                else:
                    doc["metadata"]["language"] = _detect_language(doc["text"])
            documents.append(doc)

    logger.info(
        "Ingestion complete — %d file(s) processed, %d skipped, %d document(s) produced",
        files_found, files_skipped, len(documents),
    )
    return documents


# ---------------------------------------------------------------------------
# Checkpoint I/O
# ---------------------------------------------------------------------------

def save_checkpoint(documents: list[dict], checkpoint_dir: Path) -> Path:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    out_path = checkpoint_dir / "step_1_documents.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)
    logger.info("Checkpoint saved → %s (%d documents)", out_path, len(documents))
    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 1 — Ingest corpus files")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    parser.add_argument("--corpus-dir", help="Override corpus directory path")
    args = parser.parse_args()

    logs_dir = get_logs_dir()
    _setup_logging(logs_dir)

    # Resolve corpus and checkpoint dirs
    if args.corpus_dir:
        corpus_dir = Path(args.corpus_dir).resolve()
        checkpoint_dir = corpus_dir.parent / "checkpoints"
    else:
        corpus_dir = get_corpus_dir(args.use_case)
        checkpoint_dir = get_checkpoint_dir(args.use_case)

    if not corpus_dir.exists():
        logger.error("Corpus directory not found: %s", corpus_dir)
        sys.exit(1)

    config = load_config()
    default_language = config.get("spacy", {}).get("default_language", "en")

    logger.info("=== Step 1 — Ingest ===")
    logger.info("Corpus dir      : %s", corpus_dir)
    logger.info("Checkpoint      : %s", checkpoint_dir)
    logger.info("Default language: %s", default_language)

    documents = ingest_corpus(corpus_dir, default_language=default_language)

    if not documents:
        logger.warning("No documents ingested — check corpus directory and file formats.")
        sys.exit(0)

    save_checkpoint(documents, checkpoint_dir)
    logger.info("Step 1 done.")


if __name__ == "__main__":
    main()
