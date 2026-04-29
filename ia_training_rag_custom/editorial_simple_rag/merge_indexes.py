"""
merge_indexes.py
Merge two FAISS indexes (+ their chunks.json) into one.

Use case: combine two corpus indexes, e.g.
  CMS_EXPORT_2026_Q1 + CMS_EXPORT_2026_Q2 → merged index.

Both indexes must use the same embedding model (same dimension).
The merged index is an IndexFlatIP (cosine similarity, L2-normalised vectors).

Run:
  python merge_indexes.py \
      --a data/indexes/editorial/CMS_EXPORT_2026_Q1 \
      --b data/indexes/editorial/CMS_EXPORT_2026_Q2 \
      --out data/indexes/editorial/CMS_EXPORT_2026_merged

The output directory is created if it does not exist.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np


def load_index(index_dir: Path):
    """Load index.faiss and chunks.json from an index directory."""
    import faiss

    faiss_path = index_dir / "index.faiss"
    chunks_path = index_dir / "chunks.json"

    if not faiss_path.exists():
        raise FileNotFoundError(f"index.faiss not found in {index_dir}")
    if not chunks_path.exists():
        raise FileNotFoundError(f"chunks.json not found in {index_dir}")

    index = faiss.read_index(str(faiss_path))
    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))

    return index, chunks


def extract_vectors(index, n: int, dim: int) -> np.ndarray:
    """Reconstruct all vectors from a FAISS IndexFlatIP."""
    vectors = np.zeros((n, dim), dtype=np.float32)
    for i in range(n):
        index.reconstruct(i, vectors[i])
    return vectors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge two FAISS indexes (IndexFlatIP) into one"
    )
    parser.add_argument("--a", required=True, type=Path,
                        help="Path to first index directory")
    parser.add_argument("--b", required=True, type=Path,
                        help="Path to second index directory")
    parser.add_argument("--out", required=True, type=Path,
                        help="Output directory for merged index")
    args = parser.parse_args()

    import faiss

    print(f"\n=== merge_indexes ===")
    print(f"  A   : {args.a}")
    print(f"  B   : {args.b}")
    print(f"  Out : {args.out}\n")

    # Load both indexes
    print("Loading index A...")
    index_a, chunks_a = load_index(args.a)
    print(f"  {index_a.ntotal} vectors, dim={index_a.d}")

    print("Loading index B...")
    index_b, chunks_b = load_index(args.b)
    print(f"  {index_b.ntotal} vectors, dim={index_b.d}")

    if index_a.d != index_b.d:
        print(f"\nERROR: dimension mismatch — A={index_a.d}, B={index_b.d}")
        print("Both indexes must have been built with the same embedding model.")
        sys.exit(1)

    dim = index_a.d
    n_a = index_a.ntotal
    n_b = index_b.ntotal

    if len(chunks_a) != n_a:
        print(f"ERROR: index A has {n_a} vectors but chunks_a has {len(chunks_a)} entries")
        sys.exit(1)
    if len(chunks_b) != n_b:
        print(f"ERROR: index B has {n_b} vectors but chunks_b has {len(chunks_b)} entries")
        sys.exit(1)

    # Reconstruct all vectors
    print(f"\nExtracting {n_a} vectors from A...")
    vecs_a = extract_vectors(index_a, n_a, dim)

    print(f"Extracting {n_b} vectors from B...")
    vecs_b = extract_vectors(index_b, n_b, dim)

    # Build merged IndexFlatIP
    # Vectors are already L2-normalised (they were normalised before being added
    # to the original indexes), so we can add them directly.
    total = n_a + n_b
    print(f"\nBuilding merged IndexFlatIP ({total} total vectors)...")
    merged = faiss.IndexFlatIP(dim)
    merged.add(vecs_a)
    merged.add(vecs_b)

    merged_chunks = list(chunks_a) + list(chunks_b)
    assert merged.ntotal == len(merged_chunks), "Vector/metadata count mismatch after merge"

    # Save
    args.out.mkdir(parents=True, exist_ok=True)
    out_index = args.out / "index.faiss"
    out_chunks = args.out / "chunks.json"

    faiss.write_index(merged, str(out_index))
    with open(out_chunks, "w", encoding="utf-8") as f:
        json.dump(merged_chunks, f, ensure_ascii=False, indent=2)

    print(f"\nMerged index saved:")
    print(f"  {out_index}  ({merged.ntotal} vectors, dim={dim})")
    print(f"  {out_chunks}  ({len(merged_chunks)} chunks)")
    print("\nTo query the merged index, update workflow_paths.yaml:")
    try:
        rel = args.out.resolve().relative_to(PROJECT_ROOT)
        print(f'  index_dir: "{rel}"')
    except ValueError:
        print(f'  index_dir: "{args.out}"')


if __name__ == "__main__":
    main()
