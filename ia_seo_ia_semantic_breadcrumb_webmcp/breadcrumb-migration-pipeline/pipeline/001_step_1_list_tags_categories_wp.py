#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
WordPress taxonomy inventory — Step 1 of breadcrumb migration pipeline.

Conda env : tags_treatment
Usage:
    python 001_step_1_list_tags_categories_wp.py --limit 10 --taxonomy post_tag
    python 001_step_1_list_tags_categories_wp.py --limit 0 --taxonomy all --no-dry-run
    python 001_step_1_list_tags_categories_wp.py --limit 3 --taxonomy category

Purpose:
    Connect to WordPress MySQL, fetch categories and/or post_tag terms,
    export dual JSON + CSV with ISO8601 timestamp in filename.
    Dry-run (default) shows preview without writing files.

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[test]
python source/pipeline/001_step_1_list_tags_categories_wp.py --limit 3 --taxonomy post_tag
python source/pipeline/001_step_1_list_tags_categories_wp.py --limit 5 --no-dry-run
ls -la source/pipeline/exports/
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
import mysql.connector

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT       = Path(__file__).resolve().parent.parent.parent
ENV_FILE           = PROJECT_ROOT / ".env"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "source" / "pipeline" / "exports"
TABLE_PREFIX = "wp_"
TIMEZONE = ZoneInfo("Europe/Paris")


# ============================================================
# CLI
# ============================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch WordPress tags/categories → JSON + CSV export."
    )
    parser.add_argument(
        "--limit", type=int, default=10,
        help="Max terms to fetch. 0=all. (default: 10)"
    )
    parser.add_argument(
        "--taxonomy", default="all",
        choices=["category", "post_tag", "all"],
        help="Taxonomy filter. (default: all)"
    )
    parser.add_argument(
        "--dry-run", dest="dry_run", action="store_true", default=True,
        help="Preview only, skip file export. (default: true)"
    )
    parser.add_argument(
        "--no-dry-run", dest="dry_run", action="store_false",
        help="Write export files."
    )
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
        help=f"Export directory. (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--no-timestamp", dest="use_timestamp", action="store_false", default=True,
        help="Omit timestamp from filenames."
    )
    return parser.parse_args()


# ============================================================
# DB
# ============================================================

def load_db_config() -> dict:
    load_dotenv(ENV_FILE if ENV_FILE.exists() else None)
    return {
        "host":     os.getenv("WP_DB_HOST", "127.0.0.1"),
        "port":     int(os.getenv("WP_DB_PORT", "3307")),
        "database": os.getenv("WP_DB_NAME", "wordpress2"),
        "user":     os.getenv("WP_DB_USER", ""),
        "password": os.getenv("WP_DB_PASSWORD", ""),
    }


def build_query(taxonomy: str, limit: int) -> tuple:
    if taxonomy == "all":
        where = "WHERE tt.taxonomy IN (%s, %s)"
        params = ("category", "post_tag")
    else:
        where = "WHERE tt.taxonomy = %s"
        params = (taxonomy,)

    limit_clause = f"LIMIT {limit}" if limit > 0 else ""
    query = f"""
        SELECT
            t.term_id   AS id,
            t.name      AS name,
            t.slug      AS slug,
            tt.taxonomy AS taxonomy,
            tt.count    AS post_count,
            tt.parent   AS parent_id
        FROM {TABLE_PREFIX}terms t
        INNER JOIN {TABLE_PREFIX}term_taxonomy tt
            ON tt.term_id = t.term_id
        {where}
        ORDER BY tt.taxonomy, t.name
        {limit_clause};
    """
    return query, params


def fetch_terms(db_cfg: dict, taxonomy: str, limit: int) -> list:
    query, params = build_query(taxonomy, limit)
    conn = mysql.connector.connect(**db_cfg)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ============================================================
# EXPORT
# ============================================================

def ts_now() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M")


def save_exports(rows: list, args: argparse.Namespace) -> tuple:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ts = f"_{ts_now()}" if args.use_timestamp else ""
    stem = f"{args.taxonomy}{ts}_step_1_inventory"

    # CSV
    csv_path = args.output_dir / f"{stem}.csv"
    fieldnames = ["taxonomy", "id", "name", "slug", "post_count", "parent_id"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # JSON
    json_path = args.output_dir / f"{stem}.json"
    payload = {
        "timestamp":       datetime.now(tz=TIMEZONE).isoformat(),
        "pipeline_step":   "inventory",
        "taxonomy":        args.taxonomy,
        "total_processed": len(rows),
        "config": {
            "limit":    args.limit,
            "dry_run":  args.dry_run,
            "taxonomy": args.taxonomy,
        },
        "data": rows,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    return csv_path, json_path


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    args = parse_args()
    db_cfg = load_db_config()

    missing = [k for k in ("user", "password") if not db_cfg.get(k)]
    if missing:
        print(f"[ERROR] Missing DB credentials: {missing}", file=sys.stderr)
        return 1

    print(f"[CONFIG] {db_cfg['host']}:{db_cfg['port']} / {db_cfg['database']}")
    print(f"[CONFIG] taxonomy={args.taxonomy}  limit={args.limit}  dry_run={args.dry_run}")

    try:
        rows = fetch_terms(db_cfg, args.taxonomy, args.limit)
    except mysql.connector.Error as exc:
        print(f"[ERROR] MySQL: {exc}", file=sys.stderr)
        return 1

    print(f"[FETCH] {len(rows)} terms retrieved")

    if args.dry_run:
        print("[DRY-RUN] Preview (first 5):")
        for row in rows[:5]:
            print(
                f"  {row['taxonomy']:10} | {row['id']:5} | "
                f"{str(row['name'])[:40]:40} | posts={row['post_count']}"
            )
        if len(rows) > 5:
            print(f"  ... ({len(rows)} total)")
        print("[DRY-RUN] No files written. Use --no-dry-run to export.")
        return 0

    csv_path, json_path = save_exports(rows, args)
    print(f"[EXPORT] CSV  → {csv_path}")
    print(f"[EXPORT] JSON → {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
