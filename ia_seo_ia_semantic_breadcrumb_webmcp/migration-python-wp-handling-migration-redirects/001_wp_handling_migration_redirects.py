#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
[env]
# Conda Environment
conda create --name tags_treatment python=3.9.13
conda info --envs
source activate tags_treatment
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n tags_treatment

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

pip install dotenv
# [path]

cd /Users/brunoflaven/Documents/01_work/blog_articles/_ia_seo_ia_semantic_breadcrumb/wp_handling_migration_redirects/

python 001_wp_handling_migration_redirects.py


001_wp_handling_migration_redirects.py

Goal
-----

Take:
- A WordPress categories export CSV (wp_categories_export.csv)
- An editorial mapping CSV (mapping_editorial.csv)

Produce:
- migration_categories.csv
    old_name;new_category;old_name_slug;new_category_slug;status;redirect_type

- redirects_categories.csv
    source;target;redirect_type

Plus a summary printed in the console:
- how many categories mapped
- which categories are missing from the editorial mapping
- duplicates / potential issues

Design choices
--------------

- All editorial decisions are in mapping_editorial.csv.
- Python only joins, validates, slugifies, and generates the technical artifacts.
- Uses only the standard library (csv, pathlib, unicodedata, re).
"""

import csv
import unicodedata
import re
from pathlib import Path
from typing import Dict, Tuple, List, Optional

# =========================
# Configuration
# =========================

BASE_DIR = Path(__file__).resolve().parent

# Input files
WP_CATEGORIES_CSV = BASE_DIR / "input/wp_categories_export_v3.csv"
EDITORIAL_MAPPING_CSV = BASE_DIR / "input/mapping_editorial_v2.csv"


# Output files
MIGRATION_OUTPUT_CSV = BASE_DIR / "output/migration_categories_v5.csv"
REDIRECTS_OUTPUT_CSV = BASE_DIR / "output/redirects_categories_v5.csv"

# Category base path in URLs
CATEGORY_BASE = "/category"  # adjust if you use a different base


# =========================
# Helpers
# =========================

def slugify(value: str) -> str:
    """
    Convert a string into a WordPress-friendly slug:
    - lowercase
    - ASCII only
    - spaces and punctuation to hyphens
    - strip extra hyphens
    """
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "category"


def build_category_path(slug: str) -> str:
    """
    Build the URL path for a category slug.
    Example: slug 'ux-and-product-design' -> '/category/ux-and-product-design/'
    """
    slug = slug.strip("/")
    return f"{CATEGORY_BASE}/{slug}/"


# =========================
# Data loading
# =========================

def load_wp_categories(path: Path) -> Dict[str, Dict]:
    """
    Load the WordPress categories export.
    Key by 'name' (exact string match).

    Expected columns:
    taxonomy,id,name,slug,post_count,parent_id
    """
    categories: Dict[str, Dict] = {}
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if not name:
                continue
            # Keep first occurrence; warn if duplicates later
            if name in categories:
                # Could log duplicates here if needed
                pass
            categories[name] = {
                "taxonomy": row.get("taxonomy", ""),
                "id": row.get("id", ""),
                "name": name,
                "slug": row.get("slug", "").strip(),
                "post_count": row.get("post_count", ""),
                "parent_id": row.get("parent_id", ""),
            }
    return categories


def load_editorial_mapping(path: Path) -> Dict[str, Dict]:
    """
    Load the editorial mapping.

    Expected columns:
    old_name;new_category;status;redirect_type

    new_category can be empty for 'drop'.
    """
    mapping: Dict[str, Dict] = {}
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            old_name = (row.get("old_name") or "").strip()
            if not old_name:
                continue
            new_category = (row.get("new_category") or "").strip()
            status = (row.get("status") or "").strip().lower() or "migrate"
            redirect_type = (row.get("redirect_type") or "").strip().upper() or "301"

            mapping[old_name] = {
                "old_name": old_name,
                "new_category": new_category,
                "status": status,
                "redirect_type": redirect_type,
            }
    return mapping


# =========================
# Core logic
# =========================

def build_migration_and_redirects(
    wp_categories: Dict[str, Dict],
    editorial_mapping: Dict[str, Dict],
) -> Tuple[List[Dict], List[Dict], List[str]]:
    """
    Join WP categories with editorial mapping.

    Returns:
    - migration_rows: list of dict for migration_categories.csv
    - redirect_rows: list of dict for redirects_categories.csv
    - unmapped_names: list of category names present in WP but missing from mapping
    """
    migration_rows: List[Dict] = []
    redirect_rows: List[Dict] = []
    unmapped_names: List[str] = []

    for old_name, cat_data in wp_categories.items():
        map_row = editorial_mapping.get(old_name)

        old_slug = cat_data.get("slug", "").strip()
        if old_slug:
            old_path = build_category_path(old_slug)
        else:
            # If slug missing, derive from name
            old_path = build_category_path(slugify(old_name))

        if not map_row:
            # No editorial decision yet
            unmapped_names.append(old_name)
            # Still write a row with empty new values so you see them in migration CSV
            migration_rows.append({
                "old_name": old_name,
                "new_category": "",
                "old_name_slug": old_path,
                "new_category_slug": "",
                "status": "unmapped",
                "redirect_type": "",
            })
            continue

        new_category = map_row["new_category"]
        status = map_row["status"]
        redirect_type = map_row["redirect_type"]

        if new_category:
            new_slug = slugify(new_category)
            new_path = build_category_path(new_slug)
        else:
            new_slug = ""
            new_path = ""

        migration_rows.append({
            "old_name": old_name,
            "new_category": new_category,
            "old_name_slug": old_path,
            "new_category_slug": new_path,
            "status": status,
            "redirect_type": redirect_type,
        })

        # Build redirects
        # Only for migrate/merge with a new target
        if status in {"migrate", "merge"} and new_path and redirect_type:
            redirect_rows.append({
                "source": old_path,
                "target": new_path,
                "redirect_type": redirect_type,
            })
        # For 'drop', you may want 410 or redirect to a broader URL; this can be handled in mapping.
        elif status == "drop" and redirect_type:
            # If new_path empty and redirect_type is 410, we can use that.
            redirect_rows.append({
                "source": old_path,
                "target": "",
                "redirect_type": redirect_type,
            })

    return migration_rows, redirect_rows, unmapped_names


# =========================
# CSV writing
# =========================

def write_migration_csv(path: Path, rows: List[Dict]) -> None:
    fieldnames = [
        "old_name",
        "new_category",
        "old_name_slug",
        "new_category_slug",
        "status",
        "redirect_type",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_redirects_csv(path: Path, rows: List[Dict]) -> None:
    fieldnames = ["source", "target", "redirect_type"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# =========================
# Reporting
# =========================

def print_summary(
    wp_categories: Dict[str, Dict],
    editorial_mapping: Dict[str, Dict],
    migration_rows: List[Dict],
    redirect_rows: List[Dict],
    unmapped_names: List[str],
) -> None:
    total_wp = len(wp_categories)
    total_mapping = len(editorial_mapping)
    total_migration = len(migration_rows)
    total_redirects = len(redirect_rows)
    total_unmapped = len(unmapped_names)

    print("=" * 72)
    print("WP CATEGORY MIGRATION & REDIRECTS SUMMARY")
    print("=" * 72)
    print(f"Total WP categories      : {total_wp}")
    print(f"Total mapping entries    : {total_mapping}")
    print(f"Total migration rows     : {total_migration}")
    print(f"Total redirect rows      : {total_redirects}")
    print(f"Unmapped WP categories   : {total_unmapped}")
    print("-" * 72)

    if unmapped_names:
        print("Unmapped categories (present in WP but missing from mapping_editorial.csv):")
        for name in sorted(unmapped_names):
            print(f"  - {name}")
        print("-" * 72)
        print("→ Add these old_name values to mapping_editorial.csv (with new_category, status, redirect_type)")
        print("  then re-run this script.")
    else:
        print("All WP categories are covered by mapping_editorial.csv. ✅")

    print("=" * 72)


# =========================
# Main
# =========================

def main():
    if not WP_CATEGORIES_CSV.exists():
        print(f"ERROR: WP categories CSV not found: {WP_CATEGORIES_CSV}")
        return

    if not EDITORIAL_MAPPING_CSV.exists():
        print(f"ERROR: Editorial mapping CSV not found: {EDITORIAL_MAPPING_CSV}")
        return

    wp_categories = load_wp_categories(WP_CATEGORIES_CSV)
    editorial_mapping = load_editorial_mapping(EDITORIAL_MAPPING_CSV)

    migration_rows, redirect_rows, unmapped_names = build_migration_and_redirects(
        wp_categories,
        editorial_mapping,
    )

    write_migration_csv(MIGRATION_OUTPUT_CSV, migration_rows)
    write_redirects_csv(REDIRECTS_OUTPUT_CSV, redirect_rows)

    print_summary(
        wp_categories,
        editorial_mapping,
        migration_rows,
        redirect_rows,
        unmapped_names,
    )

    print(f"\nMigration CSV written to : {MIGRATION_OUTPUT_CSV}")
    print(f"Redirects CSV written to : {REDIRECTS_OUTPUT_CSV}\n")


if __name__ == "__main__":
    main()





