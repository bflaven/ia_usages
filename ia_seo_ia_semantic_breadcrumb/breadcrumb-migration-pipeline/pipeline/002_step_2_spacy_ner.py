#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Step 2: spaCy NER enrichment of WordPress taxonomy terms.

Reads Step 1 inventory JSON, runs fr_core_news_md on each term name,
adds spacy_entity field, exports enriched JSON + CSV.

Conda env : tags_treatment
Model     : fr_core_news_md (fallback: fr_core_news_sm)
Entity map: PER→PERSON  ORG→ORG  LOC→LOC  MISC→MISC

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[test dry-run]
python source/pipeline/002_step_2_spacy_ner.py --auto-input --limit 10
python source/pipeline/002_step_2_spacy_ner.py --auto-input --taxonomy category --limit 5

[export]
python source/pipeline/002_step_2_spacy_ner.py --auto-input --limit 0 --no-dry-run
ls -lh source/pipeline/exports/
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import spacy

# ── PATHS ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent.parent
EXPORT_DIR = BASE_DIR / "source" / "pipeline" / "exports"
TIMEZONE   = ZoneInfo("Europe/Paris")

# ── CONFIG ─────────────────────────────────────────────────────────────────────
SPACY_MODEL    = "fr_core_news_md"
SPACY_FALLBACK = "fr_core_news_sm"

# French spaCy labels → our standard labels
ENTITY_MAP = {
    "PER":  "PERSON",
    "ORG":  "ORG",
    "LOC":  "LOC",
    "MISC": "MISC",
}


# ── HELPERS ────────────────────────────────────────────────────────────────────

def normalize_term(name: str) -> str:
    """Slug/hashtag/CamelCase → readable space-separated text."""
    text = name.lstrip('#')
    text = re.sub(r'[-_.]', ' ', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)        # camelCase
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)  # ACRONym
    return re.sub(r'\s+', ' ', text).strip()


def detect_entity(nlp, name: str) -> str | None:
    """Run NER on term name; try sentence context if direct pass yields nothing."""
    normalized = normalize_term(name)

    # Direct pass
    for ent in nlp(normalized).ents:
        if ent.label_ in ENTITY_MAP:
            return ENTITY_MAP[ent.label_]

    # Sentence context (helps short/ambiguous terms)
    for ent in nlp(f"Le sujet principal est {normalized}.").ents:
        if ent.label_ in ENTITY_MAP:
            return ENTITY_MAP[ent.label_]

    return None


def load_nlp():
    try:
        return spacy.load(SPACY_MODEL)
    except OSError:
        print(f"[WARN] {SPACY_MODEL} not found, falling back to {SPACY_FALLBACK}")
        return spacy.load(SPACY_FALLBACK)


def latest_export(suffix: str) -> Path | None:
    files = sorted(EXPORT_DIR.glob(f"*_{suffix}.json"), reverse=True)
    return files[0] if files else None


def ts_now() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M")


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Step 2: spaCy NER enrichment of WP taxonomy terms."
    )
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--input", type=Path,
                     help="Path to Step 1 inventory JSON.")
    grp.add_argument("--auto-input", action="store_true",
                     help="Auto-detect latest *_inventory.json in exports/.")
    parser.add_argument("--limit", type=int, default=10,
                        help="Max terms to process (0=all, default: 10)")
    parser.add_argument("--taxonomy", default="all",
                        choices=["category", "post_tag", "all"],
                        help="Filter by taxonomy after load. (default: all)")
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
        input_file = latest_export("inventory")
        if not input_file:
            print("[ERROR] No *_inventory.json in exports/. Run Step 1 first.",
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

    data = payload.get("data", [])

    if args.taxonomy != "all":
        data = [r for r in data if r.get("taxonomy") == args.taxonomy]
    if args.limit > 0:
        data = data[:args.limit]

    print(f"[CONFIG] terms={len(data)}  limit={args.limit}  "
          f"taxonomy={args.taxonomy}  dry_run={args.dry_run}")

    # Load model
    print(f"[MODEL]  Loading {SPACY_MODEL}...")
    nlp = load_nlp()
    print(f"[MODEL]  {nlp.meta['name']} v{nlp.meta['version']}")

    # Run NER
    enriched = []
    entity_counts: dict[str, int] = {}
    none_count = 0

    for i, row in enumerate(data, 1):
        normalized = normalize_term(row["name"])
        entity = detect_entity(nlp, row["name"])

        enriched.append({**row, "spacy_entity": entity,
                         "spacy_normalized": normalized})

        if entity:
            entity_counts[entity] = entity_counts.get(entity, 0) + 1
        else:
            none_count += 1

        if i <= 5 or (args.dry_run and i <= 10):
            tag = entity or "—"
            print(f"  [{i:3}] {row['taxonomy']:10} | "
                  f"{str(row['name'])[:32]:32} → "
                  f"{normalized[:32]:32} | {tag}")

    print(f"\n[NER]    {entity_counts}  none={none_count}  "
          f"total={len(enriched)}")

    if args.dry_run:
        print("[DRY-RUN] No files written. Use --no-dry-run to export.")
        return 0

    # Export
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ts = ts_now()
    stem = f"{args.taxonomy}_{ts}_step_2_spacy"

    json_path = args.output_dir / f"{stem}.json"
    out_payload = {
        "timestamp":       datetime.now(tz=TIMEZONE).isoformat(),
        "pipeline_step":   "spacy_ner",
        "taxonomy":        args.taxonomy,
        "source_file":     input_file.name,
        "total_processed": len(enriched),
        "entity_summary":  {**entity_counts, "none": none_count},
        "config": {
            "limit":    args.limit,
            "dry_run":  args.dry_run,
            "taxonomy": args.taxonomy,
            "model":    SPACY_MODEL,
        },
        "data": enriched,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, ensure_ascii=False, indent=2, default=str)

    csv_path = args.output_dir / f"{stem}.csv"
    fieldnames = ["taxonomy", "id", "name", "slug", "post_count", "parent_id",
                  "spacy_entity", "spacy_normalized"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched)

    print(f"[EXPORT] JSON → {json_path}")
    print(f"[EXPORT] CSV  → {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
