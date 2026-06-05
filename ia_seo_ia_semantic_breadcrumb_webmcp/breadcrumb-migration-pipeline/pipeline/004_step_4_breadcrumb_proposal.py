#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Step 4: Generate breadcrumb proposals and export to JSON + CSV.

Reads Step 3 Wikidata-enriched JSON, builds breadcrumb path per term,
and writes two export files for manual import into the WordPress plugin.

No direct database writes — use the plugin "Import & Export" tab to load the
*_step_4_proposals.json file into WordPress.

Conda env : tags_treatment

Breadcrumb logic:
  category with parent → ["Home", "Parent Name", "Term Name"]
  category root        → ["Home", "Term Name"]
  post_tag             → ["Home", "Tags", "Term Name"]

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[preview]
python source/pipeline/004_step_4_breadcrumb_proposal.py --auto-input --limit 10

[export JSON + CSV]
python source/pipeline/004_step_4_breadcrumb_proposal.py --auto-input --no-dry-run
python source/pipeline/004_step_4_breadcrumb_proposal.py --auto-input --no-dry-run --limit 0
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# ── PATHS ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent.parent
EXPORT_DIR = BASE_DIR / "source" / "pipeline" / "exports"
TIMEZONE   = ZoneInfo("Europe/Paris")


# ── BREADCRUMB BUILDER ─────────────────────────────────────────────────────────

def build_id_map(data: list) -> dict:
    """WP term_id (int) → row dict — used for parent chain resolution."""
    return {int(r["id"]): r for r in data}


def build_breadcrumb(row: dict, id_map: dict, max_depth: int = 6) -> list:
    if row.get("taxonomy") == "post_tag":
        return ["Home", "Tags", row["name"]]

    parts = []
    current = row
    seen: set[int] = set()

    while current and len(parts) < max_depth:
        wp_id = int(current["id"])
        if wp_id in seen:
            break
        seen.add(wp_id)
        parts.append(current["name"])
        parent_id = int(current.get("parent_id") or 0)
        current = id_map.get(parent_id) if parent_id else None

    parts.reverse()
    return ["Home"] + parts


# ── HELPERS ────────────────────────────────────────────────────────────────────

def latest_export(suffix: str) -> Path | None:
    files = sorted(EXPORT_DIR.glob(f"*_{suffix}.json"), reverse=True)
    return files[0] if files else None


def ts_now() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M")


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Step 4: Generate breadcrumb proposals → JSON + CSV export."
    )
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--input", type=Path,
                     help="Path to Step 3 Wikidata JSON.")
    grp.add_argument("--auto-input", action="store_true",
                     help="Auto-detect latest *_wikidata.json in exports/.")
    parser.add_argument("--limit", type=int, default=10,
                        help="Max terms (0=all, default: 10)")
    parser.add_argument("--taxonomy", default="all",
                        choices=["category", "post_tag", "all"])
    parser.add_argument("--dry-run", dest="dry_run",
                        action="store_true", default=True)
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false")
    parser.add_argument("--output-dir", type=Path, default=EXPORT_DIR)
    return parser.parse_args()


# ── MAIN ───────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    # Resolve input
    if args.auto_input or args.input is None:
        input_file = latest_export("wikidata")
        if not input_file:
            print("[ERROR] No *_wikidata.json in exports/. Run Step 3 first.",
                  file=sys.stderr)
            return 1
        print(f"[AUTO]   Input: {input_file.name}")
    else:
        input_file = args.input

    if not input_file.exists():
        print(f"[ERROR] File not found: {input_file}", file=sys.stderr)
        return 1

    with open(input_file, encoding="utf-8") as f:
        payload = json.load(f)

    all_data = payload.get("data", [])
    id_map   = build_id_map(all_data)

    data = all_data
    if args.taxonomy != "all":
        data = [r for r in data if r.get("taxonomy") == args.taxonomy]
    if args.limit > 0:
        data = data[:args.limit]

    print(f"[CONFIG] terms={len(data)}  limit={args.limit}  "
          f"taxonomy={args.taxonomy}  dry_run={args.dry_run}")

    # Build proposals
    proposals = []
    for row in data:
        breadcrumb = build_breadcrumb(row, id_map)
        proposals.append({**row, "proposed_breadcrumb": breadcrumb})

    # ── DRY-RUN — preview only ────────────────────────────────────────────────
    if args.dry_run:
        print("[DRY-RUN] Preview (first 10):")
        for p in proposals[:10]:
            print(
                f"  {p['taxonomy']:10} | {str(p['name'])[:28]:28} | "
                f"entity={str(p.get('spacy_entity') or '—'):8} | "
                f"wiki={str(p.get('wikidata_id') or '—'):12} | "
                f"crumb: {' > '.join(p['proposed_breadcrumb'])}"
            )
        print(f"\n[DRY-RUN] {len(proposals)} proposals ready. "
              "Use --no-dry-run to write JSON + CSV exports.")
        return 0

    # ── EXPORT JSON ───────────────────────────────────────────────────────────
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ts = ts_now()

    json_path = args.output_dir / f"{args.taxonomy}_{ts}_step_4_proposals.json"
    json_payload = {
        "timestamp":       datetime.now(tz=TIMEZONE).isoformat(),
        "pipeline_step":   "breadcrumb_proposals",
        "taxonomy":        args.taxonomy,
        "source_file":     input_file.name,
        "total_processed": len(proposals),
        "config": {
            "limit":    args.limit,
            "dry_run":  args.dry_run,
            "taxonomy": args.taxonomy,
        },
        "data": proposals,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, ensure_ascii=False, indent=2, default=str)
    print(f"[EXPORT] JSON → {json_path}")

    # ── EXPORT CSV ────────────────────────────────────────────────────────────
    csv_path = args.output_dir / f"{args.taxonomy}_{ts}_step_4_proposals.csv"
    fieldnames = [
        "taxonomy", "id", "name", "slug", "post_count", "parent_id",
        "spacy_entity", "wikidata_id", "wikidata_label", "wikidata_description",
        "proposed_breadcrumb",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for p in proposals:
            row = {**p, "proposed_breadcrumb": " > ".join(p["proposed_breadcrumb"])}
            writer.writerow(row)
    print(f"[EXPORT] CSV  → {csv_path}")

    print(f"\n[DONE] {len(proposals)} proposals exported.")
    print(f"       Import the JSON file via the WordPress plugin:")
    print(f"       Admin → Breadcrumb Migration → Import & Export → Import Pipeline Data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
