"""
reset_corpus.py
Reset a corpus: delete all pipeline artefacts (checkpoints and index)
without touching logs/ or the source documents in data/corpora/.

Run:
  python reset_corpus.py                            # resets active use_case
  python reset_corpus.py --use-case editorial       # resets a specific use_case
  python reset_corpus.py --yes                      # skip confirmation prompt
  python reset_corpus.py --dry-run                  # show what would be deleted
"""

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.config import load_config, get_checkpoint_dir, get_index_dir


def _delete(path: Path, dry_run: bool = False) -> None:
    if not path.exists():
        print(f"  (skip, not found) {path}")
        return
    if dry_run:
        print(f"  [dry-run] would delete: {path}")
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    print(f"  deleted: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reset pipeline artefacts for a corpus (keeps source docs and logs)"
    )
    parser.add_argument(
        "--use-case",
        type=str,
        default=None,
        help="Override active_use_case from config.yaml",
    )
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without deleting",
    )
    args = parser.parse_args()

    cfg = load_config()
    uc = args.use_case or cfg["active_use_case"]

    checkpoint_dir = get_checkpoint_dir(uc)
    index_dir = get_index_dir(uc)

    print(f"\nReset corpus artefacts — use_case: {uc}")
    print(f"  Checkpoint dir : {checkpoint_dir}")
    print(f"  Index dir      : {index_dir}")
    print()

    # All artefacts produced by steps 1–4
    targets = [
        checkpoint_dir / "step_1_documents.json",
        checkpoint_dir / "step_2_chunks.json",
        checkpoint_dir / "step_3_embeddings.npy",
        checkpoint_dir / "step_3_chunk_ids.json",
        index_dir / "index.faiss",
        index_dir / "chunks.json",
    ]

    existing = [t for t in targets if t.exists()]
    if not existing:
        print("Nothing to reset — artefacts not found.")
        return

    print("The following will be deleted:")
    for t in existing:
        kind = "dir" if t.is_dir() else "file"
        print(f"  [{kind}] {t}")
    print()

    if not args.yes and not args.dry_run:
        answer = input("Confirm reset? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            return

    for target in targets:
        _delete(target, dry_run=args.dry_run)

    if not args.dry_run:
        print("\nReset complete. Source documents and logs preserved.")
        print("Rebuild with:")
        print("  python scripts/step_1_001_ingest.py")
        print("  python scripts/step_2_001_parse.py")
        print("  python scripts/step_3_001_embed.py")
        print("  python scripts/step_4_001_index.py")
    else:
        print("\n[dry-run] Nothing was deleted.")


if __name__ == "__main__":
    main()
