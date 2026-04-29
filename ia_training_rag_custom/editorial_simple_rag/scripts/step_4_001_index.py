"""
Step 4 — Index
--------------
Reads the Step 2 (chunks) and Step 3 (embeddings) checkpoints, builds a
FAISS IndexFlatIP, and writes it to the index directory.

Output:
    data/indexes/<use_case>/<corpus_id>/index.faiss
    data/indexes/<use_case>/<corpus_id>/chunks.json

Run standalone:
    python scripts/step_4_001_index.py
    python scripts/step_4_001_index.py --use-case editorial
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.vector_store.faiss_store import FAISSStore
from src.utils.config import load_config, get_checkpoint_dir, get_index_dir, get_logs_dir


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
            logging.FileHandler(logs_dir / "step_4_index.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step4")


# ---------------------------------------------------------------------------
# Checkpoint loaders
# ---------------------------------------------------------------------------

def load_step2_chunks(checkpoint_dir: Path) -> list[dict]:
    path = checkpoint_dir / "step_2_chunks.json"
    if not path.exists():
        raise FileNotFoundError(f"Step 2 checkpoint not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_step3_embeddings(checkpoint_dir: Path) -> tuple[np.ndarray, list[str]]:
    npy_path = checkpoint_dir / "step_3_embeddings.npy"
    ids_path = checkpoint_dir / "step_3_chunk_ids.json"

    if not npy_path.exists():
        raise FileNotFoundError(f"Step 3 embeddings not found: {npy_path}")
    if not ids_path.exists():
        raise FileNotFoundError(f"Step 3 chunk IDs not found: {ids_path}")

    embeddings = np.load(str(npy_path))
    with open(ids_path, encoding="utf-8") as f:
        chunk_ids = json.load(f)

    return embeddings, chunk_ids


# ---------------------------------------------------------------------------
# Alignment helper
# ---------------------------------------------------------------------------

def align_chunks_to_embeddings(
    chunks: list[dict],
    chunk_ids: list[str],
) -> list[dict]:
    """
    Return chunks reordered to match the embedding row order from step 3.
    Raises if any chunk_id from step 3 is missing in step 2.
    """
    chunk_map = {c["chunk_id"]: c for c in chunks}
    aligned = []
    missing = []
    for cid in chunk_ids:
        if cid not in chunk_map:
            missing.append(cid)
        else:
            aligned.append(chunk_map[cid])
    if missing:
        raise ValueError(f"{len(missing)} chunk_id(s) from step 3 not found in step 2: {missing[:5]}")
    return aligned


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 4 — Build FAISS index")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    args = parser.parse_args()

    logs_dir = get_logs_dir()
    _setup_logging(logs_dir)

    config = load_config()
    checkpoint_dir = get_checkpoint_dir(args.use_case)
    index_dir = get_index_dir(args.use_case)
    use_case = args.use_case or config["active_use_case"]

    logger.info("=== Step 4 — Index ===")
    logger.info("Use case    : %s", use_case)
    logger.info("Checkpoint  : %s", checkpoint_dir)
    logger.info("Index dir   : %s", index_dir)

    # Load inputs
    try:
        chunks = load_step2_chunks(checkpoint_dir)
        embeddings, chunk_ids = load_step3_embeddings(checkpoint_dir)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Chunks: %d  |  Embeddings: %s", len(chunks), embeddings.shape)

    # Align chunk metadata to embedding row order
    try:
        aligned_chunks = align_chunks_to_embeddings(chunks, chunk_ids)
    except ValueError as exc:
        logger.error("Alignment error: %s", exc)
        sys.exit(1)

    # Build and save
    store = FAISSStore.build(embeddings, aligned_chunks)
    store.save(index_dir)

    logger.info(
        "Index ready — %d vectors, dim=%d, saved to %s",
        store.size, store.dim, index_dir,
    )
    logger.info("Step 4 done.")


if __name__ == "__main__":
    main()
