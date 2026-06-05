#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Pre-flight smoke tests — verify all pipeline dependencies before running.

Tests:
  T01  .env file exists and has required keys
  T02  MySQL connection (host, port, credentials)
  T03  DB tables exist (wp_breadcrumb_*)
  T04  spaCy model loads (fr_core_news_md, fallback fr_core_news_sm)
  T05  spaCy processes a sample term correctly
  T06  Wikidata API is reachable (live HTTP check)
  T07  exports/ directory exists (or can be created)
  T08  All 4 pipeline scripts exist in source/pipeline/

Conda env : tags_treatment

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[usage]
python source/pipeline/test_index.py
python source/pipeline/test_index.py --skip-network   # skip Wikidata live call
python source/pipeline/test_index.py --skip-spacy     # skip spaCy model load (slow)
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_DIR = PROJECT_ROOT / "source" / "pipeline"
EXPORT_DIR   = PIPELINE_DIR / "exports"
ENV_FILE     = PROJECT_ROOT / ".env"

PIPELINE_SCRIPTS = [
    "001_step_1_list_tags_categories_wp.py",
    "002_step_2_spacy_ner.py",
    "003_step_3_wikidata_enrich.py",
    "004_step_4_breadcrumb_proposal.py",
]

PASS  = "PASS"
FAIL  = "FAIL"
SKIP  = "SKIP"
WARN  = "WARN"

results: list[tuple[str, str, str]] = []  # (test_id, status, message)


# ── Test helpers ───────────────────────────────────────────────────────────────

def record(test_id: str, status: str, msg: str) -> None:
    results.append((test_id, status, msg))
    icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "–", "WARN": "!"}.get(status, "?")
    print(f"  [{icon}] {test_id:<6} {msg}")


# ── Tests ──────────────────────────────────────────────────────────────────────

def t01_env_file() -> None:
    if not ENV_FILE.exists():
        record("T01", FAIL, f".env not found at {ENV_FILE}")
        return
    load_dotenv(ENV_FILE)
    missing = [k for k in ("WP_DB_HOST", "WP_DB_PORT", "WP_DB_NAME", "WP_DB_USER", "WP_DB_PASSWORD")
               if not os.getenv(k)]
    if missing:
        record("T01", FAIL, f".env missing keys: {missing}")
    else:
        record("T01", PASS, f".env found, all keys present ({ENV_FILE.name})")


def t02_db_connection() -> None:
    load_dotenv(ENV_FILE if ENV_FILE.exists() else None)
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=os.getenv("WP_DB_HOST", "127.0.0.1"),
            port=int(os.getenv("WP_DB_PORT", "3307")),
            database=os.getenv("WP_DB_NAME", "wordpress2"),
            user=os.getenv("WP_DB_USER", ""),
            password=os.getenv("WP_DB_PASSWORD", ""),
        )
        conn.close()
        record("T02", PASS,
               f"MySQL connected ({os.getenv('WP_DB_HOST')}:{os.getenv('WP_DB_PORT')} / {os.getenv('WP_DB_NAME')})")
    except Exception as exc:
        record("T02", FAIL, f"MySQL connection failed: {exc}")


def t03_db_tables() -> None:
    load_dotenv(ENV_FILE if ENV_FILE.exists() else None)
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=os.getenv("WP_DB_HOST", "127.0.0.1"),
            port=int(os.getenv("WP_DB_PORT", "3307")),
            database=os.getenv("WP_DB_NAME", "wordpress2"),
            user=os.getenv("WP_DB_USER", ""),
            password=os.getenv("WP_DB_PASSWORD", ""),
        )
        cur = conn.cursor()
        cur.execute("SHOW TABLES LIKE 'wp_breadcrumb%'")
        found = [r[0] for r in cur.fetchall()]
        cur.close(); conn.close()

        expected = {"wp_breadcrumb_terms", "wp_breadcrumb_proposals", "wp_breadcrumb_redirects"}
        missing  = expected - set(found)
        if missing:
            record("T03", WARN,
                   f"Tables missing: {missing}. Run sql/create_tables.sql or activate WP plugin.")
        else:
            record("T03", PASS, f"All 3 breadcrumb tables exist: {found}")
    except Exception as exc:
        record("T03", FAIL, f"Cannot check tables: {exc}")


def t04_spacy_model(skip: bool) -> None:
    if skip:
        record("T04", SKIP, "spaCy model load skipped (--skip-spacy)")
        return
    try:
        t0 = time.time()
        import spacy
        model = "fr_core_news_md"
        try:
            nlp = spacy.load(model)
        except OSError:
            model = "fr_core_news_sm"
            nlp = spacy.load(model)
        elapsed = time.time() - t0
        record("T04", PASS,
               f"spaCy model '{model}' v{nlp.meta['version']} loaded ({elapsed:.1f}s)")
    except Exception as exc:
        record("T04", FAIL, f"spaCy model load failed: {exc}")


def t05_spacy_ner(skip: bool) -> None:
    if skip:
        record("T05", SKIP, "spaCy NER test skipped (--skip-spacy)")
        return
    try:
        import spacy
        try:
            nlp = spacy.load("fr_core_news_md")
        except OSError:
            nlp = spacy.load("fr_core_news_sm")

        samples = [
            ("Barack Obama",            "PER"),
            ("Intelligence Artificielle", None),   # MISC or None — flexible
            ("Paris",                   "LOC"),
        ]
        ok = 0
        for text, expected_label in samples:
            doc = nlp(text)
            labels = [e.label_ for e in doc.ents]
            if expected_label is None or expected_label in labels:
                ok += 1
        record("T05", PASS if ok >= 2 else WARN,
               f"NER sample check: {ok}/{len(samples)} expected entities found")
    except Exception as exc:
        record("T05", FAIL, f"spaCy NER test failed: {exc}")


def t06_wikidata_api(skip: bool) -> None:
    if skip:
        record("T06", SKIP, "Wikidata API check skipped (--skip-network)")
        return
    try:
        import requests
        t0  = time.time()
        resp = requests.get(
            "https://www.wikidata.org/w/api.php",
            params={"action": "wbsearchentities", "search": "Python",
                    "language": "fr", "type": "item", "limit": 1, "format": "json"},
            timeout=8,
            headers={"User-Agent": "breadcrumb-migration/test"},
        )
        resp.raise_for_status()
        hits    = resp.json().get("search", [])
        elapsed = time.time() - t0
        if hits:
            record("T06", PASS,
                   f"Wikidata API reachable ({elapsed:.1f}s) — test result: {hits[0].get('id')} '{hits[0].get('label')}'")
        else:
            record("T06", WARN, "Wikidata API responded but returned no results for test query 'Python'")
    except Exception as exc:
        record("T06", FAIL, f"Wikidata API unreachable: {exc}")


def t07_exports_dir() -> None:
    if EXPORT_DIR.exists():
        files = list(EXPORT_DIR.glob("*.json"))
        record("T07", PASS,
               f"exports/ exists — {len(files)} JSON file(s) present")
    else:
        try:
            EXPORT_DIR.mkdir(parents=True)
            record("T07", PASS, f"exports/ created at {EXPORT_DIR}")
        except Exception as exc:
            record("T07", FAIL, f"Cannot create exports/: {exc}")


def t08_pipeline_scripts() -> None:
    missing = [s for s in PIPELINE_SCRIPTS if not (PIPELINE_DIR / s).exists()]
    if missing:
        record("T08", FAIL, f"Missing pipeline scripts: {missing}")
    else:
        record("T08", PASS,
               f"All {len(PIPELINE_SCRIPTS)} pipeline scripts found in source/pipeline/")


# ── CLI + main ─────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pre-flight smoke tests for the pipeline.")
    parser.add_argument("--skip-network", action="store_true",
                        help="Skip live Wikidata API check.")
    parser.add_argument("--skip-spacy", action="store_true",
                        help="Skip spaCy model load tests (T04, T05).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print(f"\n{'='*60}")
    print("  Breadcrumb Pipeline — Pre-flight Smoke Tests")
    print(f"  project root: {PROJECT_ROOT}")
    print(f"{'='*60}\n")

    t01_env_file()
    t02_db_connection()
    t03_db_tables()
    t04_spacy_model(args.skip_spacy)
    t05_spacy_ner(args.skip_spacy)
    t06_wikidata_api(args.skip_network)
    t07_exports_dir()
    t08_pipeline_scripts()

    # ── Summary ───────────────────────────────────────────────────────────────
    counts = {s: sum(1 for _, st, _ in results if st == s)
              for s in (PASS, FAIL, WARN, SKIP)}

    print(f"\n{'='*60}")
    print(f"  Results: {counts[PASS]} PASS  {counts[FAIL]} FAIL  "
          f"{counts[WARN]} WARN  {counts[SKIP]} SKIP")
    print(f"{'='*60}")

    if counts[FAIL] > 0:
        print("\n  FAILED tests:")
        for tid, st, msg in results:
            if st == FAIL:
                print(f"    [{tid}] {msg}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
