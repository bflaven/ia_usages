"""
check_status.py
Display the status of the RAG project: corpus files, pipeline artefacts,
index state, and cache stats.

Run:
  python check_status.py
  python check_status.py --use-case editorial
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


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def main(use_case: str | None = None) -> None:
    cfg = load_config()
    uc = use_case or cfg["active_use_case"]

    corpus_dir = get_corpus_dir(uc)
    checkpoint_dir = get_checkpoint_dir(uc)
    index_dir = get_index_dir(uc)

    print("\n" + "=" * 60)
    print(f"  RAG Status — use_case: {uc}")
    print("=" * 60)

    # --- Corpus ---
    print(f"\nCorpus directory : {corpus_dir}")
    supported = set(READERS.keys())   # {'.json', '.txt', '.pdf', ...}
    if not corpus_dir.exists():
        print("  [!] Directory does not exist.")
    else:
        files = [f for f in corpus_dir.rglob("*")
                 if f.is_file() and f.suffix.lower() in supported]
        total_size = sum(f.stat().st_size for f in files)
        print(f"  Files found     : {len(files)}")
        print(f"  Total size      : {human_size(total_size)}")
        for f in sorted(files):
            print(f"    [{f.suffix.upper()[1:]}] {f.name}  ({human_size(f.stat().st_size)})")

        ch = cfg.get("chunking", {})
        chunk_size = ch.get("size", 512)
        overlap_frac = ch.get("overlap", 0.1)
        overlap_tokens = int(chunk_size * overlap_frac)
        stride = max(1, chunk_size - overlap_tokens)
        approx_words = total_size // 5
        est = max(1, approx_words // stride)
        print(f"\n  Chunk estimate  : ~{est} chunks")
        print(f"  Chunk size      : {chunk_size} tokens  overlap={overlap_frac:.0%}")

    # --- Step 1 checkpoint ---
    step1 = checkpoint_dir / "step_1_documents.json"
    print(f"\nStep 1 checkpoint: {step1}")
    if step1.exists():
        docs = json.loads(step1.read_text(encoding="utf-8"))
        print(f"  Documents       : {len(docs)}")
    else:
        print("  [missing] — run: python scripts/step_1_001_ingest.py")

    # --- Step 2 checkpoint ---
    step2 = checkpoint_dir / "step_2_chunks.json"
    print(f"\nStep 2 checkpoint: {step2}")
    if step2.exists():
        chunks = json.loads(step2.read_text(encoding="utf-8"))
        print(f"  Chunks          : {len(chunks)}")
    else:
        print("  [missing] — run: python scripts/step_2_001_parse.py")

    # --- Step 3 checkpoint ---
    step3_npy = checkpoint_dir / "step_3_embeddings.npy"
    step3_ids = checkpoint_dir / "step_3_chunk_ids.json"
    print(f"\nStep 3 checkpoint: {step3_npy}")
    if step3_npy.exists():
        print(f"  Size            : {human_size(step3_npy.stat().st_size)}")
        try:
            import numpy as np
            arr = np.load(str(step3_npy))
            print(f"  Shape           : {arr.shape}")
        except Exception:
            pass
    else:
        print("  [missing] — run: python scripts/step_3_001_embed.py")

    # --- FAISS index ---
    faiss_path = index_dir / "index.faiss"
    chunks_path = index_dir / "chunks.json"
    print(f"\nFAISS index      : {faiss_path}")
    if faiss_path.exists():
        print(f"  Size            : {human_size(faiss_path.stat().st_size)}")
        try:
            import faiss
            idx = faiss.read_index(str(faiss_path))
            print(f"  Vectors         : {idx.ntotal}  dim={idx.d}")
        except Exception:
            print("  (could not read index details)")
    else:
        print("  [missing] — run: python scripts/step_4_001_index.py")

    if chunks_path.exists():
        n = len(json.loads(chunks_path.read_text(encoding="utf-8")))
        print(f"  Chunks metadata : {n} entries ({chunks_path.name})")
    else:
        print(f"  Chunks metadata : [missing] ({chunks_path})")

    # --- Config summary ---
    print(f"\nEmbeddings       : {cfg['embeddings']['provider']} / {cfg['embeddings']['model']}")
    llm = cfg.get("llm", {})
    llm_model = llm.get("model") or llm.get("azure_deployment", "?")
    print(f"LLM              : {llm.get('provider', '?')} / {llm_model}")
    r = cfg.get("retrieval", {})
    print(f"Retrieval        : k={r.get('k', 5)}  threshold={r.get('score_threshold', 0.2)}  "
          f"rerank={r.get('rerank', {}).get('enabled', False)}")

    # --- Cache stats ---
    db_cfg = cfg.get("database", {})
    if db_cfg.get("enabled", False):
        db_path = PROJECT_ROOT / db_cfg.get("path", "data/rag_cache.db")
        if db_path.exists():
            from src.utils.db_manager import DBManager
            db = DBManager(db_path)
            stats = db.stats()
            print(f"\nCache (SQLite)   : {db_path}")
            print(f"  Cache entries   : {stats.get('cache_entries', '?')}")
            print(f"  History entries : {stats.get('history_entries', '?')}")
        else:
            print(f"\nCache            : not yet created ({db_path})")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check RAG pipeline status")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    args = parser.parse_args()
    main(args.use_case)
