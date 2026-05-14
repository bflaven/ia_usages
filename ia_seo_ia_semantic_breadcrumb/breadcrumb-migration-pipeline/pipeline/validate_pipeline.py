#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Pipeline output validator — checks export files after each step.

For each JSON export found in exports/, validates:
  - File is valid JSON and non-empty
  - Envelope keys present (timestamp, pipeline_step, total_processed, data)
  - All required data fields present per step type
  - Data quality metrics (% entity detected, % wikidata hit, etc.)
  - CSV counterpart exists alongside each JSON

Conda env : tags_treatment

[path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/

[usage]
python source/pipeline/validate_pipeline.py                  # validate all exports
python source/pipeline/validate_pipeline.py --step inventory # one step only
python source/pipeline/validate_pipeline.py --latest         # only latest file per step
python source/pipeline/validate_pipeline.py --strict         # fail on WARN too
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORT_DIR   = PROJECT_ROOT / "source" / "pipeline" / "exports"

# ── Schema definitions per step ────────────────────────────────────────────────

ENVELOPE_KEYS = {"timestamp", "pipeline_step", "total_processed", "data"}

STEP_SCHEMAS: dict[str, dict] = {
    "inventory": {
        "required_fields": {"id", "name", "slug", "taxonomy", "post_count", "parent_id"},
        "optional_fields": set(),
        "quality_checks":  [],
    },
    "spacy_ner": {
        "required_fields": {"id", "name", "slug", "taxonomy", "spacy_entity", "spacy_normalized"},
        "optional_fields": set(),
        "quality_checks":  [
            ("spacy_entity", "% terms with entity detected",
             lambda rows: sum(1 for r in rows if r.get("spacy_entity")) / len(rows) * 100 if rows else 0,
             40.0),  # warn if < 40%
        ],
    },
    "wikidata_enrich": {
        "required_fields": {"id", "name", "slug", "taxonomy",
                            "wikidata_id", "wikidata_label", "wikidata_description"},
        "optional_fields": {"spacy_entity", "spacy_normalized"},
        "quality_checks":  [
            ("wikidata_id", "% terms with Wikidata match",
             lambda rows: sum(1 for r in rows if r.get("wikidata_id")) / len(rows) * 100 if rows else 0,
             30.0),  # warn if < 30%
        ],
    },
}

# suffix in filename → pipeline_step value in JSON
SUFFIX_TO_STEP = {
    "inventory": "inventory",
    "spacy":     "spacy_ner",
    "wikidata":  "wikidata_enrich",
}

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
INFO = "INFO"


# ── Helpers ────────────────────────────────────────────────────────────────────

class Report:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.findings: list[tuple[str, str]] = []  # (status, message)

    def add(self, status: str, msg: str) -> None:
        self.findings.append((status, msg))

    @property
    def has_fail(self) -> bool:
        return any(s == FAIL for s, _ in self.findings)

    @property
    def has_warn(self) -> bool:
        return any(s == WARN for s, _ in self.findings)

    def print(self) -> None:
        icon_map = {PASS: "✓", FAIL: "✗", WARN: "!", INFO: "·"}
        worst = FAIL if self.has_fail else (WARN if self.has_warn else PASS)
        header_icon = icon_map[worst]
        print(f"\n  [{header_icon}] {self.filename}")
        for status, msg in self.findings:
            print(f"        {icon_map[status]} {msg}")


def detect_suffix(path: Path) -> str | None:
    stem = path.stem
    for suffix in SUFFIX_TO_STEP:
        if f"_{suffix}" in stem:
            return suffix
    return None


# ── Validators ─────────────────────────────────────────────────────────────────

def validate_file(path: Path) -> Report:
    report = Report(path.name)

    # ── Load JSON ──────────────────────────────────────────────────────────────
    try:
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
    except json.JSONDecodeError as exc:
        report.add(FAIL, f"Invalid JSON: {exc}")
        return report
    except OSError as exc:
        report.add(FAIL, f"Cannot read file: {exc}")
        return report

    # ── Envelope ──────────────────────────────────────────────────────────────
    missing_env = ENVELOPE_KEYS - set(obj.keys())
    if missing_env:
        report.add(FAIL, f"Missing envelope keys: {missing_env}")
    else:
        report.add(PASS, f"Envelope keys present")

    data = obj.get("data", [])
    if not isinstance(data, list):
        report.add(FAIL, "'data' is not a list")
        return report
    if len(data) == 0:
        report.add(WARN, "'data' array is empty — did the pipeline fetch any terms?")
        return report
    report.add(INFO, f"total_processed={obj.get('total_processed')}  "
                     f"taxonomy={obj.get('taxonomy')}  "
                     f"timestamp={obj.get('timestamp','?')[:19]}")

    # ── Pipeline step matches filename ─────────────────────────────────────────
    file_suffix = detect_suffix(path)
    json_step   = obj.get("pipeline_step", "")
    if file_suffix and SUFFIX_TO_STEP.get(file_suffix) != json_step:
        report.add(WARN,
                   f"pipeline_step mismatch: filename says '{file_suffix}' but JSON says '{json_step}'")

    # ── Schema validation ──────────────────────────────────────────────────────
    schema = STEP_SCHEMAS.get(json_step)
    if not schema:
        report.add(INFO, f"No schema defined for step '{json_step}' — skipping field checks")
    else:
        # Check first row for required fields
        sample = data[0]
        actual = set(sample.keys())
        missing_fields = schema["required_fields"] - actual
        if missing_fields:
            report.add(FAIL, f"Required fields missing in data rows: {missing_fields}")
        else:
            report.add(PASS, f"All required fields present: {schema['required_fields']}")

        # Check for unexpected None-only columns (data quality)
        all_none = {k for k in schema["required_fields"]
                    if all(r.get(k) is None or r.get(k) == "" for r in data)}
        if all_none:
            report.add(WARN, f"Fields are all null/empty across all rows: {all_none}")

        # Quality checks
        for field, label, fn, threshold in schema["quality_checks"]:
            pct = fn(data)
            status = PASS if pct >= threshold else WARN
            report.add(status, f"{label}: {pct:.1f}%"
                                + (f"  (warn threshold: {threshold:.0f}%)" if status == WARN else ""))

    # ── CSV counterpart ────────────────────────────────────────────────────────
    csv_path = path.with_suffix(".csv")
    if csv_path.exists():
        try:
            with open(csv_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                csv_rows = list(reader)
            report.add(PASS, f"CSV counterpart exists: {csv_path.name} ({len(csv_rows)} rows)")
        except Exception as exc:
            report.add(WARN, f"CSV exists but cannot read: {exc}")
    else:
        report.add(WARN, f"CSV counterpart missing: {csv_path.name}")

    return report


# ── CLI + main ─────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate pipeline export files.")
    parser.add_argument("--step",
                        choices=["inventory", "spacy", "wikidata"],
                        help="Validate only this step's exports.")
    parser.add_argument("--latest", action="store_true",
                        help="Validate only the latest file per step (not all files).")
    parser.add_argument("--strict", action="store_true",
                        help="Exit code 1 on any WARN (not just FAIL).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print(f"\n{'='*60}")
    print("  Breadcrumb Pipeline — Output Validator")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  exports: {EXPORT_DIR}")
    print(f"{'='*60}")

    if not EXPORT_DIR.exists():
        print(f"\n  exports/ not found. Run the pipeline first.")
        return 1

    # Collect files to validate
    all_files: list[Path] = []
    suffixes = [args.step] if args.step else ["inventory", "spacy", "wikidata"]

    for suffix in suffixes:
        found = sorted(EXPORT_DIR.glob(f"*_{suffix}.json"), reverse=True)
        if args.latest and found:
            all_files.append(found[0])
        else:
            all_files.extend(found)

    if not all_files:
        print(f"\n  No export files found for step(s): {suffixes}")
        print("  Run the pipeline with --no-dry-run to generate exports.")
        return 1

    print(f"\n  Validating {len(all_files)} file(s)...\n")

    reports: list[Report] = []
    for path in sorted(all_files):
        report = validate_file(path)
        report.print()
        reports.append(report)

    # ── Summary ───────────────────────────────────────────────────────────────
    total_fail = sum(1 for r in reports if r.has_fail)
    total_warn = sum(1 for r in reports if r.has_warn)
    total_pass = len(reports) - total_fail - total_warn

    print(f"\n{'='*60}")
    print(f"  Files: {len(reports)}   "
          f"PASS: {total_pass}   FAIL: {total_fail}   WARN: {total_warn}")
    print(f"{'='*60}")

    if total_fail > 0:
        return 1
    if args.strict and total_warn > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
