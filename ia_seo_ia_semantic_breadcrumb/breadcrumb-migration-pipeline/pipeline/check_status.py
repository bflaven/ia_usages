#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Pipeline status dashboard.

Shows:
  - Which export files exist per step (latest + file size + term count)
  - DB table row counts (wp_breadcrumb_terms, proposals, redirects)
  - Proposal breakdown by validation_state
  - What step is done vs pending

Conda env : tags_treatment

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[usage]
python source/pipeline/check_status.py
python source/pipeline/check_status.py --no-db    # skip DB check (no MySQL needed)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORT_DIR   = PROJECT_ROOT / "source" / "pipeline" / "exports"
ENV_FILE     = PROJECT_ROOT / ".env"

# step suffix → human label
STEP_SUFFIXES = {
    "inventory": "Step 1 — Inventory",
    "spacy":     "Step 2 — spaCy NER",
    "wikidata":  "Step 3 — Wikidata",
    "proposals": "Step 4 — DB proposals (CSV audit)",
}

REQUIRED_DATA_KEYS = {
    "inventory": {"id", "name", "slug", "taxonomy"},
    "spacy":     {"id", "name", "slug", "taxonomy", "spacy_entity"},
    "wikidata":  {"id", "name", "slug", "taxonomy", "wikidata_id", "wikidata_label", "wikidata_description"},
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def fmt_size(path: Path) -> str:
    b = path.stat().st_size
    return f"{b/1024:.1f} KB" if b < 1_048_576 else f"{b/1_048_576:.1f} MB"


def latest_by_suffix(suffix: str) -> list[Path]:
    return sorted(EXPORT_DIR.glob(f"*_{suffix}.json"), reverse=True)


def load_json_summary(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
        return {
            "timestamp":       obj.get("timestamp", "—"),
            "total_processed": obj.get("total_processed", "?"),
            "taxonomy":        obj.get("taxonomy", "?"),
            "step":            obj.get("pipeline_step", "?"),
            "extra":           obj,
        }
    except Exception as exc:
        return {"error": str(exc)}


def col(text: str, width: int) -> str:
    return str(text)[:width].ljust(width)


# ── Sections ───────────────────────────────────────────────────────────────────

def section_exports() -> None:
    print("\n── EXPORT FILES ──────────────────────────────────────────────")
    if not EXPORT_DIR.exists():
        print(f"  exports/ not found: {EXPORT_DIR}")
        return

    any_found = False
    for suffix, label in STEP_SUFFIXES.items():
        files = latest_by_suffix(suffix)
        if not files:
            print(f"  {label:38} — NO FILE")
            continue

        any_found = True
        latest = files[0]
        info   = load_json_summary(latest)
        size   = fmt_size(latest)

        if "error" in info:
            print(f"  {label:38} — ERROR: {info['error']}")
            continue

        extra = ""
        raw = info["extra"]
        if suffix == "spacy" and "entity_summary" in raw:
            es = raw["entity_summary"]
            total = info["total_processed"] or 1
            none_pct = int(100 * es.get("none", 0) / total)
            extra = f"  entities={dict((k,v) for k,v in es.items() if k != 'none')}  no_entity={none_pct}%"
        elif suffix == "wikidata" and "wikidata_summary" in raw:
            ws = raw["wikidata_summary"]
            total = info["total_processed"] or 1
            hit_pct = int(100 * ws.get("hits", 0) / total)
            extra = f"  hits={ws.get('hits')}  misses={ws.get('misses')}  ({hit_pct}% match)"

        print(
            f"  {label:38} "
            f"{col(latest.name, 45)} "
            f"{col(size, 9)} "
            f"terms={info['total_processed']}"
            f"{extra}"
        )

        if len(files) > 1:
            print(f"    + {len(files)-1} older file(s)")

    if not any_found:
        print("  No export files found. Run the pipeline first.")


def section_db(skip: bool) -> None:
    print("\n── DATABASE ──────────────────────────────────────────────────")
    if skip:
        print("  (skipped — use without --no-db to include DB check)")
        return

    try:
        load_dotenv(ENV_FILE if ENV_FILE.exists() else None)
        import mysql.connector
        conn = mysql.connector.connect(
            host=os.getenv("WP_DB_HOST", "127.0.0.1"),
            port=int(os.getenv("WP_DB_PORT", "3307")),
            database=os.getenv("WP_DB_NAME", "wordpress2"),
            user=os.getenv("WP_DB_USER", ""),
            password=os.getenv("WP_DB_PASSWORD", ""),
        )
    except Exception as exc:
        print(f"  Cannot connect to DB: {exc}")
        return

    cur = conn.cursor()

    # Check tables exist
    cur.execute("SHOW TABLES LIKE 'wp_breadcrumb%'")
    tables = [r[0] for r in cur.fetchall()]
    if not tables:
        print("  wp_breadcrumb_* tables NOT found.")
        print("  → Run sql/create_tables.sql in phpMyAdmin, or activate the WP plugin.")
        cur.close(); conn.close()
        return

    # Row counts
    for tbl in ["wp_breadcrumb_terms", "wp_breadcrumb_proposals", "wp_breadcrumb_redirects"]:
        cur.execute(f"SELECT COUNT(*) FROM `{tbl}`")  # noqa: S608 — table name is hardcoded
        count = cur.fetchone()[0]
        print(f"  {tbl:35} {count:>6} rows")

    # Proposals by validation_state
    cur.execute(
        "SELECT validation_state, COUNT(*) FROM wp_breadcrumb_proposals GROUP BY validation_state"
    )
    rows = cur.fetchall()
    if rows:
        print("\n  Proposals by state:")
        for state, cnt in rows:
            bar = "█" * min(cnt, 40)
            print(f"    {str(state):10} {cnt:5}  {bar}")

    # Terms by taxonomy
    cur.execute(
        "SELECT taxonomy, COUNT(*) FROM wp_breadcrumb_terms GROUP BY taxonomy"
    )
    rows = cur.fetchall()
    if rows:
        print("\n  Terms by taxonomy:")
        for taxonomy, cnt in rows:
            print(f"    {str(taxonomy):12} {cnt:5}")

    cur.close()
    conn.close()


def section_pipeline_state() -> None:
    print("\n── PIPELINE STATE ────────────────────────────────────────────")
    states = {
        1: bool(latest_by_suffix("inventory")),
        2: bool(latest_by_suffix("spacy")),
        3: bool(latest_by_suffix("wikidata")),
        4: bool(EXPORT_DIR.glob("*_proposals.csv")) if EXPORT_DIR.exists() else False,
    }
    labels = {
        1: "Step 1 Inventory exported",
        2: "Step 2 spaCy NER exported",
        3: "Step 3 Wikidata exported",
        4: "Step 4 Proposals CSV written",
    }
    for step, done in states.items():
        mark = "✓" if done else "○"
        print(f"  [{mark}] {labels[step]}")

    next_step = next((s for s, done in states.items() if not done), None)
    if next_step:
        cmds = {
            1: "python source/pipeline/001_step_1_list_tags_categories_wp.py --no-dry-run",
            2: "python source/pipeline/002_step_2_spacy_ner.py --auto-input --no-dry-run",
            3: "python source/pipeline/003_step_3_wikidata_enrich.py --auto-input --no-dry-run",
            4: "python source/pipeline/004_step_4_breadcrumb_proposal.py --auto-input --no-dry-run",
        }
        print(f"\n  Next: {cmds[next_step]}")
    else:
        print("\n  All steps complete. Go to WP admin to validate proposals.")


# ── CLI + main ─────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Breadcrumb pipeline status dashboard.")
    parser.add_argument("--no-db", action="store_true",
                        help="Skip database check.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(f"\n{'='*60}")
    print(f"  Breadcrumb Pipeline — Status")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  exports: {EXPORT_DIR}")
    print(f"{'='*60}")

    section_exports()
    section_pipeline_state()
    section_db(skip=args.no_db)

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
