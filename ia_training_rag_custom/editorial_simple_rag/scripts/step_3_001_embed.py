"""
Step 3 — Embed
--------------
Reads the Step 2 checkpoint (chunks), vectorizes every chunk text using
the EmbeddingClient configured in config.yaml, and saves:

  step_3_embeddings.npy   — float32 array of shape (n_chunks, dim)
  step_3_chunk_ids.json   — ordered list of chunk_ids matching the rows

Step 4 joins these two files with step_2_chunks.json to build the FAISS index.

Run standalone:
    python scripts/step_3_001_embed.py
    python scripts/step_3_001_embed.py --use-case editorial
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.llm.embeddings import EmbeddingClient
from src.utils.config import load_config, get_checkpoint_dir, get_logs_dir


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
            logging.FileHandler(logs_dir / "step_3_embed.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step3")


# ---------------------------------------------------------------------------
# Checkpoint I/O
# ---------------------------------------------------------------------------

def load_step2_checkpoint(checkpoint_dir: Path) -> list[dict]:
    path = checkpoint_dir / "step_2_chunks.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Step 2 checkpoint not found: {path}\nRun step_2_001_parse.py first."
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_checkpoint(
    embeddings: np.ndarray,
    chunk_ids: list[str],
    checkpoint_dir: Path,
) -> None:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    npy_path = checkpoint_dir / "step_3_embeddings.npy"
    np.save(str(npy_path), embeddings)
    logger.info("Embeddings saved → %s  shape=%s", npy_path, embeddings.shape)

    ids_path = checkpoint_dir / "step_3_chunk_ids.json"
    with open(ids_path, "w", encoding="utf-8") as f:
        json.dump(chunk_ids, f, ensure_ascii=False, indent=2)
    logger.info("Chunk IDs saved  → %s  (%d entries)", ids_path, len(chunk_ids))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 3 — Embed chunks")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    args = parser.parse_args()

    logs_dir = get_logs_dir()
    _setup_logging(logs_dir)

    config = load_config()
    checkpoint_dir = get_checkpoint_dir(args.use_case)
    use_case = args.use_case or config["active_use_case"]

    emb_cfg = config.get("embeddings", {})
    logger.info("=== Step 3 — Embed ===")
    logger.info("Use case  : %s", use_case)
    logger.info("Provider  : %s", emb_cfg.get("provider", "ollama"))
    logger.info("Model     : %s", emb_cfg.get("model") or emb_cfg.get("azure_deployment"))

    # Load step 2 output
    try:
        chunks = load_step2_checkpoint(checkpoint_dir)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Loaded %d chunk(s) from step 2", len(chunks))

    # Build client and embed
    try:
        client = EmbeddingClient.from_config(config)
    except Exception as exc:
        logger.error("Failed to initialise EmbeddingClient: %s", exc)
        sys.exit(1)

    texts = [c["text"] for c in chunks]
    chunk_ids = [c["chunk_id"] for c in chunks]

    try:
        embeddings = client.embed(texts)
    except RuntimeError as exc:
        logger.error("Embedding failed: %s", exc)
        logger.error(
            "Is Ollama running? Start it with: ollama serve"
            if emb_cfg.get("provider") == "ollama"
            else "Check your Azure credentials and endpoint."
        )
        sys.exit(1)

    logger.info(
        "Embedded %d chunk(s) — dim=%d  provider=%s  model=%s",
        len(chunks), embeddings.shape[1], client.provider, client.model,
    )

    save_checkpoint(embeddings, chunk_ids, checkpoint_dir)
    logger.info("Step 3 done.")


if __name__ == "__main__":
    main()
