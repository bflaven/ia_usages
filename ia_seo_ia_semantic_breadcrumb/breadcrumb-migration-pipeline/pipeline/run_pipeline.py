#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Pipeline orchestrator — Python replacement for run_pipeline.sh.

Runs steps 1-4 in sequence via subprocess.
Stops immediately on any step failure.
Reports timing and progress per step.

Conda env : tags_treatment

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[usage]
python source/pipeline/run_pipeline.py                             # dry-run, limit=10, all
python source/pipeline/run_pipeline.py --limit 10 --taxonomy post_tag
python source/pipeline/run_pipeline.py --limit 0 --taxonomy all --no-dry-run
python source/pipeline/run_pipeline.py --steps 1 2 --limit 5      # run only steps 1 and 2
python source/pipeline/run_pipeline.py --from-step 3              # resume from step 3
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_DIR = PROJECT_ROOT / "source" / "pipeline"

STEPS = {
    1: PIPELINE_DIR / "001_step_1_list_tags_categories_wp.py",
    2: PIPELINE_DIR / "002_step_2_spacy_ner.py",
    3: PIPELINE_DIR / "003_step_3_wikidata_enrich.py",
    4: PIPELINE_DIR / "004_step_4_breadcrumb_proposal.py",
}

STEP_LABELS = {
    1: "Inventory         (fetch WP terms)",
    2: "spaCy NER         (entity detection)",
    3: "Wikidata enrich   (id / label / description)",
    4: "Breadcrumb + DB   (proposals → MySQL)",
}


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run breadcrumb migration pipeline steps 1-4."
    )
    parser.add_argument("--limit", type=int, default=10,
                        help="Max terms per step (0=all, default: 10)")
    parser.add_argument("--taxonomy", default="all",
                        choices=["category", "post_tag", "all"])
    parser.add_argument("--dry-run", dest="dry_run",
                        action="store_true", default=True)
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false")
    parser.add_argument("--steps", type=int, nargs="+",
                        choices=[1, 2, 3, 4],
                        help="Run only these step numbers (e.g. --steps 1 2)")
    parser.add_argument("--from-step", type=int, choices=[1, 2, 3, 4],
                        dest="from_step",
                        help="Resume from this step number")
    return parser.parse_args()


# ── Runner ─────────────────────────────────────────────────────────────────────

def build_cmd(step: int, args: argparse.Namespace) -> list[str]:
    cmd = [sys.executable, str(STEPS[step])]

    if step == 1:
        cmd += ["--limit", str(args.limit), "--taxonomy", args.taxonomy]
        if not args.dry_run:
            cmd.append("--no-dry-run")
    else:
        cmd += ["--auto-input", "--limit", str(args.limit),
                "--taxonomy", args.taxonomy]
        if not args.dry_run:
            cmd.append("--no-dry-run")

    return cmd


def run_step(step: int, args: argparse.Namespace) -> bool:
    label = STEP_LABELS[step]
    cmd   = build_cmd(step, args)

    print(f"\n{'='*60}")
    print(f"  STEP {step} — {label}")
    print(f"  cmd: {' '.join(cmd)}")
    print(f"{'='*60}")

    t0     = time.time()
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    elapsed = time.time() - t0

    status = "OK" if result.returncode == 0 else "FAILED"
    print(f"\n  → Step {step} {status}  ({elapsed:.1f}s)")
    return result.returncode == 0


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    # Determine which steps to run
    if args.steps:
        steps_to_run = sorted(args.steps)
    elif args.from_step:
        steps_to_run = list(range(args.from_step, 5))
    else:
        steps_to_run = [1, 2, 3, 4]

    mode = "DRY-RUN" if args.dry_run else "PRODUCTION"
    print(f"\n{'#'*60}")
    print(f"  Breadcrumb Migration Pipeline")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  mode={mode}  limit={args.limit}  taxonomy={args.taxonomy}")
    print(f"  steps={steps_to_run}")
    print(f"{'#'*60}")

    pipeline_start = time.time()
    failed_step    = None

    for step in steps_to_run:
        ok = run_step(step, args)
        if not ok:
            failed_step = step
            break

    total = time.time() - pipeline_start

    print(f"\n{'#'*60}")
    if failed_step:
        print(f"  PIPELINE FAILED at step {failed_step}  ({total:.1f}s total)")
        print(f"  Fix the error above, then resume with:")
        print(f"  python source/pipeline/run_pipeline.py --from-step {failed_step} ...")
        print(f"{'#'*60}")
        return 1

    print(f"  PIPELINE COMPLETE  ({total:.1f}s total)")
    print(f"  Exports → {PROJECT_ROOT / 'source' / 'pipeline' / 'exports'}")
    print(f"{'#'*60}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
