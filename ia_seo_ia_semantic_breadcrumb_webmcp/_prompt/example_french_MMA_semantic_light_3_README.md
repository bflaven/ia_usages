# MMA_semantic_light_3

NLP pipeline for processing and enriching editorial tags (ThemaTag) from France Médias Monde media brands: France 24 FR, RFI FR, Monte Carlo Doualiya, etc.

Each brand/language combination is a **service** (e.g. `F24_FR`).

---

## Table of contents

- [MMA\_semantic\_light\_3](#mma_semantic_light_3)
  - [Table of contents](#table-of-contents)
  - [1. Environment setup](#1-environment-setup)
  - [2. Project structure](#2-project-structure)
  - [3. Configuration](#3-configuration)
    - [config/pipeline.yaml — global parameters](#configpipelineyaml--global-parameters)
    - [config/F24\_FR/paths.yaml — all I/O paths](#configf24_frpathsyaml--all-io-paths)
    - [config/F24\_FR/taxonomy.yaml — editorial taxonomy](#configf24_frtaxonomyyaml--editorial-taxonomy)
    - [config/F24\_FR/editorial\_rules.yaml — editorial rules](#configf24_freditorial_rulesyaml--editorial-rules)
  - [4. Pipeline overview](#4-pipeline-overview)
  - [5. Running individual steps](#5-running-individual-steps)
    - [COLLECT phase](#collect-phase)
    - [ORTHO phase](#ortho-phase)
    - [WIKIDATA phase](#wikidata-phase)
    - [CLASS phase](#class-phase)
    - [PICQ phase](#picq-phase)
  - [6. Running the full pipeline](#6-running-the-full-pipeline)
  - [7. Streamlit review interface](#7-streamlit-review-interface)
  - [8. Utility scripts](#8-utility-scripts)
  - [9. Adding a new service](#9-adding-a-new-service)
  - [Authorship](#authorship)

---

## 1. Environment setup

```bash
# Create and activate the Conda environment
conda create --name tags_treatment python=3.9.13
conda activate tags_treatment

# Install dependencies
pip install -r requirements.txt
```

Key dependencies: `pyyaml`, `requests`, `sentence-transformers`, `scikit-learn`, `spacy`, `rapidfuzz`, `streamlit`, `pandas`.

---

## 2. Project structure

```
MMA_semantic_light_3/
│
├── config/
│   ├── loader.py                    # Single config entry point
│   ├── pipeline.yaml                # Global pipeline parameters
│   ├── csv_schema.yaml              # CSV column contract
│   └── F24_FR/
│       ├── paths.yaml               # All I/O paths for the service
│       ├── taxonomy.yaml            # C1 stable, canonical_c1, arbo_primaire,
│       │                            # level2_taxonomy, level2_overrides,
│       │                            # country_to_category, category_anchors, …
│       ├── editorial_rules.yaml     # hors_arbo, format_vocab, program_vocab,
│       │                            # theme_keywords, tags_promouvoir, …
│       └── api.yaml                 # Mezzo endpoints, Wikidata, timeouts
│
├── source_csv/F24_FR/               # 5 editorial CSV source files (input)
│   ├── 001_sheet_1_vue_d_ensemble.csv
│   ├── 002_sheet_2_arbo_stable_recommandee.csv
│   ├── 003_sheet_3_sous_rubriques_candidates.csv
│   ├── 004_sheet_4_dossiers_candidates.csv
│   └── 005_sheet_5_mapping_exhaustif.csv
│
├── data/F24_FR/                     # Pipeline data (generated)
│   ├── step_01_collect/
│   │   ├── tags/                    # step_001 output
│   │   ├── stats/                   # step_003 output
│   │   ├── consolidated/            # step_004 output
│   │   └── consolidated_ortho/      # step_005 output
│   ├── step_02_wikidata/
│   │   ├── lookup/                  # step_006 output
│   │   └── enrichment/              # step_007 output
│   ├── step_03_classification/
│   │   ├── bucket_b/                # step_008 output
│   │   ├── embedding/               # step_009 output
│   │   └── clustering/              # step_010 output
│   └── step_04_picq/
│       ├── artefacts/               # step_011 output
│       ├── chunks/                  # step_012 output (chunks)
│       └── final/                   # step_012 output (final JSON + stats)
│
├── step_001_COLLECT_api_tags.py
├── step_002_COLLECT_prepare_stats_call.py
├── step_003_COLLECT_api_stats.py
├── step_004_COLLECT_consolidate_tags_stats.py
├── step_005_ORTHO_spell_check.py
├── step_006_WIKIDATA_lookup.py
├── step_007_WIKIDATA_enrichment.py
├── step_008_CLASS_bucket_b.py
├── step_009_CLASS_embedding.py
├── step_010_CLASS_clustering_breadcrumb.py
├── step_011_PICQ_ingest_csv.py
├── step_012_PICQ_breadcrumb_merge.py
├── step_013_PICQ_streamlit_review.py
│
├── check_pipeline.py                # Global pipeline state
├── lint_config.py                   # Detect hardcoded values in scripts
└── run_pipeline.py                  # Optional orchestrator
```

---

## 3. Configuration

All business values live in YAML files under `config/`. **No paths, endpoints, or editorial values are hardcoded in Python scripts.**

### config/pipeline.yaml — global parameters

```yaml
dry_run: false         # Override with --dry-run
cap_tags: null         # null = full run; N = test on first N tags
embedding_model: "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
threshold_high: 0.40
threshold_low: 0.25
k_clusters: 60
chunk_size: 100
```

### config/F24_FR/paths.yaml — all I/O paths

All input/output directories and CSV file paths for a service. Scripts read paths from here — never hardcode them.

### config/F24_FR/taxonomy.yaml — editorial taxonomy

- `c1_stable` — the 10 stable primary categories
- `canonical_c1` — variant → canonical form mapping
- `arbo_primaire` — C1 → sub-categories
- `level2_taxonomy` — controlled C2 nodes with slugs
- `level2_overrides` — manual breadcrumb overrides by tag label
- `country_to_category`, `instance_to_type`, `occupation_to_category` — Wikidata type mapping
- `category_anchors` — rich text anchors for embedding classification

### config/F24_FR/editorial_rules.yaml — editorial rules

- `hors_arbo` — tags outside the main hierarchy
- `a_transformer_en_dossier` — tags to promote to dossier (C3)
- `tags_promouvoir` — tags to promote to stable sub-category (C2)
- `format_vocab` / `program_vocab` — format and program definitions
- `theme_keywords` — keyword-based thematic classification

---

## 4. Pipeline overview

```
COLLECT          ORTHO          WIKIDATA           CLASS                   PICQ
─────────────────────────────────────────────────────────────────────────────────
step_001         step_005       step_006            step_008                step_011
API tags    →    spell     →    lookup (Wikidata)→  Bucket B rules  →       ingest CSV
                 check          Bucket A / B        step_009
step_002                        step_007            embedding class         step_012
prepare stats                   enrichment          step_010                breadcrumb
                                                    clustering +            merge
step_003                                            breadcrumb
API stats
                                                                            step_013
step_004                                                                    Streamlit
consolidate                                                                 review
```

Each step reads the latest output file from its input directory and writes to its output directory. Steps are independent and resumable.

---

## 5. Running individual steps

All steps share the same CLI interface:

```bash
python step_NNN_PHASE_name.py --service SERVICE [--dry-run] [--cap N] [--verbose]
```

### COLLECT phase

```bash
# Fetch tags from Mezzo API
python step_001_COLLECT_api_tags.py --service F24_FR

# Merge individual page files into a single thema_complete.json
python step_002_COLLECT_prepare_stats_call.py --service F24_FR

# Fetch publication stats for each tag (slow — 1 API call/tag)
python step_003_COLLECT_api_stats.py --service F24_FR

# Test on 50 tags, no file written
python step_003_COLLECT_api_stats.py --service F24_FR --dry-run --cap 50

# Merge tags + stats into a consolidated JSON
python step_004_COLLECT_consolidate_tags_stats.py --service F24_FR
```

### ORTHO phase

```bash
# Spell check, fuzzy duplicate detection, suspicious pattern detection
python step_005_ORTHO_spell_check.py --service F24_FR

# Verbose mode to inspect each tag decision
python step_005_ORTHO_spell_check.py --service F24_FR --verbose
```

### WIKIDATA phase

```bash
# Wikidata lookup — routes tags to Bucket A (hit) or Bucket B (miss)
# Checkpoint saved every N tags — safe to interrupt and resume
python step_006_WIKIDATA_lookup.py --service F24_FR

# Test on first 100 tags only
python step_006_WIKIDATA_lookup.py --service F24_FR --cap 100

# Dry-run: show what would be called without hitting the API
python step_006_WIKIDATA_lookup.py --service F24_FR --dry-run

# Batch enrichment for Bucket A tags (wbgetentities + optional Wikipedia summary)
python step_007_WIKIDATA_enrichment.py --service F24_FR
python step_007_WIKIDATA_enrichment.py --service F24_FR --cap 100
```

### CLASS phase

```bash
# Rule-based classification for Bucket B tags (PROGRAM > FORMAT > THEME > UNKNOWN)
python step_008_CLASS_bucket_b.py --service F24_FR

# Embedding-based classification (downloads ~120 MB model on first run, cached after)
python step_009_CLASS_embedding.py --service F24_FR
python step_009_CLASS_embedding.py --service F24_FR --dry-run  # no model loaded

# K-Means clustering + 5-branch breadcrumb builder
python step_010_CLASS_clustering_breadcrumb.py --service F24_FR
python step_010_CLASS_clustering_breadcrumb.py --service F24_FR --verbose  # debug per-tag branch
```

### PICQ phase

```bash
# Ingest and normalise 5 editorial CSV files → 6 artefact JSON files
python step_011_PICQ_ingest_csv.py --service F24_FR
python step_011_PICQ_ingest_csv.py --service F24_FR --dry-run  # stats only, no files written

# Merge semantic breadcrumb (step_010) with CSV editorial arborescense (step_011)
# Writes chunks to dir_chunks + final JSON + stats to dir_final
python step_012_PICQ_breadcrumb_merge.py --service F24_FR
python step_012_PICQ_breadcrumb_merge.py --service F24_FR --dry-run
```

---

## 6. Running the full pipeline

`run_pipeline.py` is an optional orchestrator that chains steps 001–012 as subprocesses.

```bash

# PATH
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/_cleaning_tags_taxonomy/MMA_semantic_light_3/

# COMMAND PERSO
python run_pipeline.py --service F24_FR --steps 001 002 003 004 005 006 007 008 009 010 --cap 3




python run_pipeline.py --service RFI_FR --steps 001 002 003 004 005 006 007 008 009 010 --cap 3
python run_pipeline.py --service RFI_FR --steps 011 012 --cap 3





# Full production run
python run_pipeline.py --service F24_FR
python run_pipeline.py --service RFI_FR


# Dry-run: all steps, no files written, no APIs called
python run_pipeline.py --service F24_FR --dry-run
python run_pipeline.py --service RFI_FR --dry-run


# Test run: first 50 tags end-to-end
python run_pipeline.py --service F24_FR --cap 50

# Run only specific steps
python run_pipeline.py --service F24_FR --steps 006 007

# Resume from step_006 to the end
python run_pipeline.py --service F24_FR --from-step 006

# Skip steps 001 002 003 (already done)
python run_pipeline.py --service F24_FR --skip 001 002 003

# Combine: resume from step_009 with verbose logging
python run_pipeline.py --service F24_FR --from-step 009 --verbose
```

Each step's output is an independent JSON file with a `_manifest.json` alongside it. If a step fails, the orchestrator stops and reports which step failed.

---

## 7. Streamlit review interface

step_013 provides an interactive 5-tab review interface. It has no `--service` argument — select the service from the sidebar dropdown.

```bash
# Launch the review interface
streamlit run step_013_PICQ_streamlit_review.py
```

The app reads from `dir_chunks` (fast, streamed) with `dir_final` as fallback.

**Tabs:**
- **Stats** — distribution by branch, layer, primary category, NER type
- **Explorer** — filterable dataframe + per-tag detail card
- **Revision** — queue of `needs_review=True` tags + CSV export + YAML override generator
- **Breadcrumb** — side-by-side comparison of step6 vs step7 breadcrumb for any tag
- **Lexique** — reference guide for all pipeline concepts

**Override workflow** — to fix a `S6_FALLBACK` or `CSV_C5_flat` tag:
1. Find the tag in the **Revision** tab
2. Copy the generated YAML snippet from the "Générer les overrides" expander
3. Add it to `config/{service}/taxonomy.yaml` under `level2_overrides`
4. Re-run step_010 then step_012

---

## 8. Utility scripts

```bash
# Show global pipeline state (reads all _manifest.json files)
python check_pipeline.py --service F24_FR

# Check all scripts for hardcoded business values (paths, labels, endpoints)
python lint_config.py
```

`check_pipeline.py` reads every `_manifest.json` across all steps and reports:
- Status (OK / MISSING)
- Last execution timestamp
- Input/output tag counts
- Duration

---

## 9. Adding a new service

1. Create `config/{NEW_SERVICE}/` with the four YAML files:
   ```
   config/{NEW_SERVICE}/paths.yaml
   config/{NEW_SERVICE}/taxonomy.yaml
   config/{NEW_SERVICE}/editorial_rules.yaml
   config/{NEW_SERVICE}/api.yaml
   ```
   Use `config/F24_FR/` as a template.

2. Create the CSV source files in `source_csv/{NEW_SERVICE}/`.

3. Validate the CSV column contract:
   ```bash
   python lint_config.py
   ```

4. Run the pipeline:
   ```bash
   python run_pipeline.py --service NEW_SERVICE --dry-run --cap 10
   python run_pipeline.py --service NEW_SERVICE --cap 50
   python run_pipeline.py --service NEW_SERVICE
   ```

The new service will appear automatically in the Streamlit sidebar.

---

## Authorship

Bruno Flaven — FMM / DEN
Version 3.0 — MMA_semantic_light_3
