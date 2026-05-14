#!/bin/bash
# Breadcrumb migration pipeline orchestrator
# Conda env: tags_treatment
#
# Usage:
#   bash source/pipeline/run_pipeline.sh              → limit=10, dry-run, all
#   bash source/pipeline/run_pipeline.sh 0 false all  → full production
#   bash source/pipeline/run_pipeline.sh 50 false post_tag

set -euo pipefail

LIMIT="${1:-10}"
DRY_RUN="${2:-true}"
TAXONOMY="${3:-all}"

PIPELINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${PIPELINE_DIR}/../.." && pwd)"

DRY_FLAG=""
if [ "${DRY_RUN}" = "false" ]; then
    DRY_FLAG="--no-dry-run"
fi

echo "================================================="
echo " Breadcrumb Migration Pipeline"
echo " limit=${LIMIT}  dry_run=${DRY_RUN}  taxonomy=${TAXONOMY}"
echo "================================================="

cd "${PROJECT_ROOT}"

# ── Step 1 : Inventory ─────────────────────────────────────────────────────────
echo ""
echo "[STEP 1] Taxonomy inventory..."
python source/pipeline/001_step_1_list_tags_categories_wp.py \
    --limit "${LIMIT}" \
    --taxonomy "${TAXONOMY}" \
    ${DRY_FLAG}

# ── Step 2 : spaCy NER ────────────────────────────────────────────────────────
echo ""
echo "[STEP 2] spaCy NER enrichment..."
python source/pipeline/002_step_2_spacy_ner.py \
    --auto-input \
    --limit "${LIMIT}" \
    --taxonomy "${TAXONOMY}" \
    ${DRY_FLAG}

# ── Step 3 : Wikidata enrichment ──────────────────────────────────────────────
echo ""
echo "[STEP 3] Wikidata enrichment..."
python source/pipeline/003_step_3_wikidata_enrich.py \
    --auto-input \
    --limit "${LIMIT}" \
    --taxonomy "${TAXONOMY}" \
    ${DRY_FLAG}

# ── Step 4 : Breadcrumb proposals → DB ───────────────────────────────────────
echo ""
echo "[STEP 4] Breadcrumb proposals..."
python source/pipeline/004_step_4_breadcrumb_proposal.py \
    --auto-input \
    --limit "${LIMIT}" \
    --taxonomy "${TAXONOMY}" \
    ${DRY_FLAG}

echo ""
echo "================================================="
echo " Pipeline complete."
echo " Exports: ${PROJECT_ROOT}/source/pipeline/exports/"
echo "================================================="
ls -lh "${PROJECT_ROOT}/source/pipeline/exports/" 2>/dev/null || echo "(no exports — dry-run?)"
