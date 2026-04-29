"""
validate_pipeline.py
Validate the coherence of pipeline artefacts between each step.

Checks:
  ✓ Corpus directory exists and contains supported files
  ✓ step_1_documents.json exists and has documents
  ✓ step_2_chunks.json exists and chunk count > 0
  ✓ step_3_embeddings.npy + step_3_chunk_ids.json exist and sizes match step 2
  ✓ index.faiss + chunks.json exist and sizes match each other

Run:
  python validate_pipeline.py
  python validate_pipeline.py --use-case editorial
"""

import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.WARNING)

from src.utils.config import load_config, get_corpus_dir, get_checkpoint_dir, get_index_dir
from src.ingestion.readers import READERS

PASS = "✓"
FAIL = "✗"


def check(label: str, ok: bool, detail: str = "") -> bool:
    mark = PASS if ok else FAIL
    msg = f"  {mark} {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return ok


def main(use_case: str | None = None) -> int:
    cfg = load_config()
    uc = use_case or cfg["active_use_case"]

    corpus_dir = get_corpus_dir(uc)
    checkpoint_dir = get_checkpoint_dir(uc)
    index_dir = get_index_dir(uc)

    errors = 0

    print(f"\n=== validate_pipeline — use_case: {uc} ===\n")

    # ------------------------------------------------------------------
    # Step 1 — Corpus
    # ------------------------------------------------------------------
    print("Step 1 — Corpus")
    corpus_ok = check("corpus_dir exists", corpus_dir.exists(), str(corpus_dir))
    if not corpus_ok:
        errors += 1
    else:
        supported = set(READERS.keys())
        files = [f for f in corpus_dir.rglob("*")
                 if f.is_file() and f.suffix.lower() in supported]
        ok = check("corpus contains supported files", len(files) > 0,
                   f"{len(files)} file(s)")
        if not ok:
            errors += 1

    # ------------------------------------------------------------------
    # Step 1 → checkpoint
    # ------------------------------------------------------------------
    print("\nStep 1 — Checkpoint (step_1_documents.json)")
    step1_path = checkpoint_dir / "step_1_documents.json"
    step1_ok = check("step_1_documents.json exists", step1_path.exists(),
                     str(step1_path))
    n_documents = 0
    if not step1_ok:
        errors += 1
        print("  (run: python scripts/step_1_001_ingest.py)")
    else:
        docs = json.loads(step1_path.read_text(encoding="utf-8"))
        n_documents = len(docs)
        ok = check("documents count > 0", n_documents > 0,
                   f"{n_documents} document(s)")
        if not ok:
            errors += 1

    # ------------------------------------------------------------------
    # Step 2 — Chunks
    # ------------------------------------------------------------------
    print("\nStep 2 — Checkpoint (step_2_chunks.json)")
    step2_path = checkpoint_dir / "step_2_chunks.json"
    step2_ok = check("step_2_chunks.json exists", step2_path.exists(),
                     str(step2_path))
    n_chunks = 0
    if not step2_ok:
        errors += 1
        print("  (run: python scripts/step_2_001_parse.py)")
    else:
        chunks = json.loads(step2_path.read_text(encoding="utf-8"))
        n_chunks = len(chunks)
        ok = check("chunks count > 0", n_chunks > 0, f"{n_chunks} chunk(s)")
        if not ok:
            errors += 1

    # ------------------------------------------------------------------
    # Step 3 — Embeddings
    # ------------------------------------------------------------------
    print("\nStep 3 — Checkpoint (step_3_embeddings.npy + step_3_chunk_ids.json)")
    npy_path = checkpoint_dir / "step_3_embeddings.npy"
    ids_path = checkpoint_dir / "step_3_chunk_ids.json"

    npy_ok = check("step_3_embeddings.npy exists", npy_path.exists())
    ids_ok = check("step_3_chunk_ids.json exists", ids_path.exists())
    n_embeddings = 0

    if not npy_ok or not ids_ok:
        errors += 1
        print("  (run: python scripts/step_3_001_embed.py)")
    else:
        try:
            import numpy as np
            arr = np.load(str(npy_path))
            n_embeddings = arr.shape[0]
            dim = arr.shape[1]
            check("embeddings loaded", True, f"shape={arr.shape}")

            chunk_ids = json.loads(ids_path.read_text(encoding="utf-8"))
            n_ids = len(chunk_ids)

            ok = check(
                "embedding rows match chunk_ids",
                n_embeddings == n_ids,
                f"{n_embeddings} embeddings / {n_ids} chunk_ids",
            )
            if not ok:
                errors += 1

            if n_chunks > 0:
                ok = check(
                    "embedding rows match step-2 chunks",
                    n_embeddings == n_chunks,
                    f"{n_embeddings} embeddings / {n_chunks} chunks",
                )
                if not ok:
                    errors += 1

        except Exception as e:
            check("embeddings readable", False, str(e))
            errors += 1

    # ------------------------------------------------------------------
    # Step 4 — FAISS index
    # ------------------------------------------------------------------
    print("\nStep 4 — Index (index.faiss + chunks.json)")
    faiss_path = index_dir / "index.faiss"
    chunks_json = index_dir / "chunks.json"

    faiss_ok = check("index.faiss exists", faiss_path.exists())
    meta_ok = check("chunks.json exists", chunks_json.exists())

    if not faiss_ok or not meta_ok:
        errors += 1
        print("  (run: python scripts/step_4_001_index.py)")
    else:
        try:
            import faiss
            index = faiss.read_index(str(faiss_path))
            idx_chunks = json.loads(chunks_json.read_text(encoding="utf-8"))

            n_idx = index.ntotal
            n_meta = len(idx_chunks)

            check("index loaded", True, f"{n_idx} vectors  dim={index.d}")

            ok = check(
                "index size matches chunks.json",
                n_idx == n_meta,
                f"{n_idx} index / {n_meta} metadata",
            )
            if not ok:
                errors += 1

            if n_embeddings > 0:
                ok = check(
                    "index size matches step-3 embeddings",
                    n_idx == n_embeddings,
                    f"{n_idx} index / {n_embeddings} embeddings",
                )
                if not ok:
                    errors += 1

        except Exception as e:
            check("FAISS index readable", False, str(e))
            errors += 1

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    if errors == 0:
        print(f"=== {PASS} All checks passed — pipeline is coherent ===\n")
    else:
        print(f"=== {FAIL} {errors} check(s) failed — see details above ===\n")

    return errors


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate pipeline artefact coherence")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    args = parser.parse_args()
    sys.exit(main(args.use_case))
