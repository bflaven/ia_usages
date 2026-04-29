"""
test_index.py
Verify FAISS index integrity:
  - index.faiss loads without errors
  - chunks.json count matches vector count
  - no null/zero vectors in a random sample
  - required metadata fields present in chunks

Run:
  python test_index.py
  python test_index.py --use-case editorial
"""

import json
import logging
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.WARNING)

import numpy as np

from src.utils.config import load_config, get_index_dir

PASS = "✓"
FAIL = "✗"
WARN = "⚠"


def check(label: str, ok: bool, detail: str = "", warn: bool = False) -> bool:
    if ok:
        mark = PASS
    elif warn:
        mark = WARN
    else:
        mark = FAIL
    msg = f"  {mark} {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return ok


def main(use_case: str | None = None) -> int:
    cfg = load_config()
    uc = use_case or cfg["active_use_case"]
    index_dir = get_index_dir(uc)

    faiss_path = index_dir / "index.faiss"
    chunks_path = index_dir / "chunks.json"

    errors = 0

    print(f"\n=== test_index — use_case: {uc} ===\n")

    # --- Load FAISS index ---
    if not faiss_path.exists():
        print(f"  {FAIL} index.faiss not found: {faiss_path}")
        print("  Run: python run_pipeline.py --build")
        return 1

    try:
        import faiss
        index = faiss.read_index(str(faiss_path))
    except Exception as e:
        print(f"  {FAIL} Failed to load index.faiss: {e}")
        return 1

    check("index.faiss loaded", True, faiss_path.name)

    n_vectors = index.ntotal
    ok = check("index is not empty", n_vectors > 0, f"{n_vectors} vectors")
    if not ok:
        errors += 1

    # --- Load chunks.json ---
    if not chunks_path.exists():
        print(f"  {FAIL} chunks.json not found: {chunks_path}")
        return 1

    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    n_chunks = len(chunks)

    ok = check(
        "chunks.json count matches index",
        n_chunks == n_vectors,
        f"{n_chunks} chunks / {n_vectors} vectors",
    )
    if not ok:
        errors += 1

    # --- Dimension info ---
    dim = index.d
    model = cfg.get("embeddings", {}).get("model", "unknown")
    print(f"\n  Dimension : {dim}  (model: {model})")

    # --- Null vector detection (via reconstruct) ---
    # IndexFlatIP supports reconstruct since it stores raw vectors.
    print("\nVector integrity:")
    if n_vectors > 0 and hasattr(index, "reconstruct"):
        sample_size = min(50, n_vectors)
        sample_indices = random.sample(range(n_vectors), sample_size)
        null_count = 0
        low_norm_count = 0

        for idx in sample_indices:
            vec = np.zeros(dim, dtype=np.float32)
            try:
                index.reconstruct(idx, vec)
            except Exception:
                # Some index types don't support reconstruct
                break
            norm = float(np.linalg.norm(vec))
            if norm == 0.0:
                null_count += 1
            elif norm < 0.01:
                low_norm_count += 1

        ok = check(
            "no null vectors in sample",
            null_count == 0,
            f"checked {sample_size} random vectors, {null_count} null",
            warn=null_count > 0,
        )
        if not ok:
            errors += 1

        check(
            "no suspiciously low-norm vectors",
            low_norm_count == 0,
            f"{low_norm_count} vectors with norm < 0.01",
            warn=True,
        )
    else:
        print("  (skipped — index type does not support reconstruct)")

    # --- Metadata field check ---
    print("\nChunk metadata fields (first 3 chunks):")
    required_fields = {"chunk_id", "text", "source", "metadata"}
    for i, chunk in enumerate(chunks[:3]):
        present = set(chunk.keys())
        missing = required_fields - present
        check(
            f"chunk[{i}] has required fields",
            len(missing) == 0,
            f"missing: {missing}" if missing else f"keys: {sorted(present)}",
        )

    # --- Summary ---
    print()
    if errors == 0:
        print(f"=== {PASS} Index integrity OK ({n_vectors} vectors, dim={dim}) ===\n")
    else:
        print(f"=== {FAIL} {errors} integrity issue(s) found ===\n")

    return errors


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test FAISS index integrity")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    args = parser.parse_args()
    sys.exit(main(args.use_case))
