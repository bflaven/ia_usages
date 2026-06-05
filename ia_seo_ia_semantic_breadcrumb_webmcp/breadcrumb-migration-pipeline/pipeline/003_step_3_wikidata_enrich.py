#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Step 3: Wikidata enrichment of spaCy-tagged WP taxonomy terms.

Reads Step 2 spaCy JSON, queries Wikidata API per term,
adds wikidata_id, wikidata_label, wikidata_description.
Supports checkpoint/resume for large datasets.

Conda env : tags_treatment
API       : https://www.wikidata.org/w/api.php  (wbsearchentities)

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[test dry-run — queries 3 live terms]
python source/pipeline/003_step_3_wikidata_enrich.py --auto-input --limit 10

[full export]
python source/pipeline/003_step_3_wikidata_enrich.py --auto-input --no-dry-run
python source/pipeline/003_step_3_wikidata_enrich.py --auto-input --no-dry-run --resume
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

# ── PATHS ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent.parent
EXPORT_DIR = BASE_DIR / "source" / "pipeline" / "exports"
TIMEZONE   = ZoneInfo("Europe/Paris")

# ── CONFIG ─────────────────────────────────────────────────────────────────────
WIKIDATA_API     = "https://www.wikidata.org/w/api.php"
WIKIDATA_LANG    = "fr"
BATCH_SIZE       = 50
REQUEST_DELAY    = 5.0           # seconds between API calls (rate limit)
CHECKPOINT_EVERY = 200           # save checkpoint every N terms
REQUEST_TIMEOUT  = 10            # seconds
MAX_RETRIES      = 4             # attempts on 429 before giving up
RETRY_BACKOFF    = 30.0          # initial wait on 429; multiplied by attempt number


# ── HELPERS ────────────────────────────────────────────────────────────────────

def normalize_term(name: str) -> str:
    """Slug/hashtag/CamelCase → readable space-separated text."""
    text = name.lstrip('#')
    text = re.sub(r'[-_.]', ' ', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)
    return re.sub(r'\s+', ' ', text).strip()


def wikidata_search(term_name: str, lang: str = WIKIDATA_LANG) -> dict:
    """
    Query Wikidata wbsearchentities.
    Returns {wikidata_id, wikidata_label, wikidata_description} or {}.
    Falls back to "en" if French yields no results.
    Retries up to MAX_RETRIES times on 429 with exponential backoff.
    """
    query_text = normalize_term(term_name)
    params = {
        "action":   "wbsearchentities",
        "search":   query_text,
        "language": lang,
        "type":     "item",
        "limit":    3,
        "format":   "json",
    }

    results = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(WIKIDATA_API, params=params,
                                timeout=REQUEST_TIMEOUT,
                                headers={"User-Agent": "breadcrumb-migration/1.0"})
            if resp.status_code == 429:
                wait = RETRY_BACKOFF * attempt
                print(f"  [429] Rate limited '{query_text}'. "
                      f"Waiting {wait:.0f}s (attempt {attempt}/{MAX_RETRIES})…")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            results = resp.json().get("search", [])
            break
        except requests.RequestException as exc:
            print(f"  [WARN] API error for '{query_text}': {exc}")
            return {}
    else:
        print(f"  [WARN] Gave up after {MAX_RETRIES} retries for '{query_text}'")
        return {}

    if not results:
        if lang == WIKIDATA_LANG and lang != "en":
            return wikidata_search(term_name, lang="en")
        return {}

    best = results[0]
    return {
        "wikidata_id":          best.get("id", ""),
        "wikidata_label":       best.get("label", ""),
        "wikidata_description": best.get("description", ""),
    }


def latest_export(suffix: str) -> Path | None:
    files = sorted(EXPORT_DIR.glob(f"*_{suffix}.json"), reverse=True)
    return files[0] if files else None


def ts_now() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M")


def save_checkpoint(path: Path, data: list, index: int) -> None:
    path.write_text(
        json.dumps({"checkpoint_index": index, "data": data},
                   ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def load_checkpoint(path: Path) -> tuple[list, int]:
    if not path.exists():
        return [], 0
    obj = json.loads(path.read_text(encoding="utf-8"))
    return obj.get("data", []), obj.get("checkpoint_index", 0)


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Step 3: Wikidata enrichment of WP taxonomy terms."
    )
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--input", type=Path,
                     help="Path to Step 2 spaCy JSON.")
    grp.add_argument("--auto-input", action="store_true",
                     help="Auto-detect latest *_spacy.json in exports/.")
    parser.add_argument("--limit", type=int, default=10,
                        help="Max terms to query (0=all, default: 10)")
    parser.add_argument("--taxonomy", default="all",
                        choices=["category", "post_tag", "all"])
    parser.add_argument("--dry-run", dest="dry_run",
                        action="store_true", default=True)
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from checkpoint file if it exists.")
    parser.add_argument("--output-dir", type=Path, default=EXPORT_DIR)
    return parser.parse_args()


# ── MAIN ───────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    # Resolve input
    if args.auto_input or args.input is None:
        input_file = latest_export("spacy")
        if not input_file:
            print("[ERROR] No *_spacy.json in exports/. Run Step 2 first.",
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

    # Output paths use taxonomy + fresh timestamp (avoid double-timestamp from input stem)
    ts = ts_now()
    checkpoint_path = args.output_dir / f"{args.taxonomy}_{ts}_step_3_wikidata_checkpoint.json"
    output_json     = args.output_dir / f"{args.taxonomy}_{ts}_step_3_wikidata.json"
    output_csv      = args.output_dir / f"{args.taxonomy}_{ts}_step_3_wikidata.csv"

    print(f"[CONFIG] terms={len(data)}  limit={args.limit}  "
          f"taxonomy={args.taxonomy}  dry_run={args.dry_run}")
    print(f"[CONFIG] LANG={WIKIDATA_LANG}  DELAY={REQUEST_DELAY}s  "
          f"CHECKPOINT_EVERY={CHECKPOINT_EVERY}  BATCH_SIZE={BATCH_SIZE}")

    # ── DRY-RUN ──────────────────────────────────────────────────────────────
    if args.dry_run:
        print("[DRY-RUN] Querying first 3 terms live (then stop):")
        for row in data[:3]:
            result = wikidata_search(row["name"])
            wid   = result.get("wikidata_id", "—")
            label = result.get("wikidata_label", "—")
            desc  = result.get("wikidata_description", "—")
            print(f"  {row['taxonomy']:10} | {str(row['name'])[:28]:28} → "
                  f"{wid:12} | {label[:28]:28} | {desc[:40]}")
            time.sleep(REQUEST_DELAY)
        print(f"[DRY-RUN] {len(data)} terms queued. "
              "Use --no-dry-run to run full enrichment.")
        return 0

    # ── FULL RUN ─────────────────────────────────────────────────────────────
    enriched: list[dict] = []
    start_index = 0

    if args.resume:
        enriched, start_index = load_checkpoint(checkpoint_path)
        if start_index > 0:
            print(f"[RESUME] From index {start_index} "
                  f"({len(enriched)} terms already done)")
            data = data[start_index:]

    hit_count = miss_count = 0

    for i, row in enumerate(data, start=start_index + 1):
        result = wikidata_search(row["name"])

        enriched_row = {
            **row,
            "wikidata_id":          result.get("wikidata_id", ""),
            "wikidata_label":       result.get("wikidata_label", ""),
            "wikidata_description": result.get("wikidata_description", ""),
        }
        enriched.append(enriched_row)

        if result.get("wikidata_id"):
            hit_count += 1
        else:
            miss_count += 1

        print(f"  [{i:4}] {row['taxonomy']:10} | "
              f"{str(row['name'])[:28]:28} → "
              f"{result.get('wikidata_id','—'):12} "
              f"{result.get('wikidata_label','—')[:25]}")

        if i % CHECKPOINT_EVERY == 0:
            args.output_dir.mkdir(parents=True, exist_ok=True)
            save_checkpoint(checkpoint_path, enriched, i)
            print(f"  [CHECKPOINT] Saved at index {i} → {checkpoint_path.name}")

        time.sleep(REQUEST_DELAY)

    # ── EXPORT ───────────────────────────────────────────────────────────────
    args.output_dir.mkdir(parents=True, exist_ok=True)

    out_payload = {
        "timestamp":        datetime.now(tz=TIMEZONE).isoformat(),
        "pipeline_step":    "wikidata_enrich",
        "taxonomy":         args.taxonomy,
        "source_file":      input_file.name,
        "total_processed":  len(enriched),
        "wikidata_summary": {"hits": hit_count, "misses": miss_count},
        "config": {
            "limit":            args.limit,
            "dry_run":          args.dry_run,
            "taxonomy":         args.taxonomy,
            "wikidata_lang":    WIKIDATA_LANG,
            "batch_size":       BATCH_SIZE,
            "request_delay":    REQUEST_DELAY,
            "checkpoint_every": CHECKPOINT_EVERY,
        },
        "data": enriched,
    }
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, ensure_ascii=False, indent=2, default=str)

    fieldnames = [
        "taxonomy", "id", "name", "slug", "post_count", "parent_id",
        "spacy_entity", "spacy_normalized",
        "wikidata_id", "wikidata_label", "wikidata_description",
    ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched)

    # Remove checkpoint on clean finish
    if checkpoint_path.exists():
        checkpoint_path.unlink()
        print(f"[CHECKPOINT] Removed: {checkpoint_path.name}")

    print(f"\n[EXPORT] JSON → {output_json}")
    print(f"[EXPORT] CSV  → {output_csv}")
    print(f"[SUMMARY] hits={hit_count}  misses={miss_count}  total={len(enriched)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
