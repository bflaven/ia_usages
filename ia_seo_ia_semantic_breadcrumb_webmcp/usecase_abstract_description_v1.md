# Use Case — Abstract Description

## Directory Descriptions

### `_prompt`
Collection of iterative prompts used to drive Claude (and other AI tools) throughout the project. Covers early exploration of the breadcrumb pipeline concept, requirements gathering, CLAUDE.md scaffolding, and the editorial category consolidation problem. Serves as the conversation log and specification source for everything built in the other directories.

### `breadcrumb-migration-pipeline`
Core Python pipeline (4 sequential steps) that automates semantic enrichment of WordPress taxonomy terms:
1. **Step 1** — Fetch all tags and categories from a live WordPress MySQL database.
2. **Step 2** — Run spaCy Named Entity Recognition (NER) to detect entity types (person, org, location, product…).
3. **Step 3** — Query Wikidata to attach canonical IDs, labels, and descriptions to each term.
4. **Step 4** — Generate structured breadcrumb proposals and write them to custom MySQL tables.

Orchestrated by `run_pipeline.py` (Python) or `run_pipeline.sh` (Bash). Supports dry-run mode, step-level resumption, and per-taxonomy filtering.

### `breadcrumb-migration-pipeline-sql`
SQL schema for the two custom MySQL tables (`wp_breadcrumb_terms`, `wp_breadcrumb_proposals`) that back the pipeline. Designed to sit alongside WordPress core tables without modifying them. Stores the original term snapshot, the spaCy/Wikidata-enriched proposals, validation state, and the final JSON breadcrumb array per term.

### `breadcrumb-migration-pipeline-wp_docker`
Docker Compose environment that spins up WordPress + MySQL + phpMyAdmin locally (ports 8080/8081). Used to test all pipeline steps and WordPress plugins in isolation before touching the production site. Enables importing production DB dumps, validating schema markup, and debugging plugin output in a safe sandbox.

### `breadcrumb-migration-pipeline-wp_plugins_breadcrumb`
Suite of four WordPress plugins built to support the migration workflow:
- **breadcrumb-migration** — Validates spaCy/Wikidata pipeline proposals and publishes enriched taxonomy terms back into WordPress.
- **breadcrumb-migration-category-migration** — Two-tab admin tool: drag-and-drop post re-categorisation (multi-select, non-destructive) + `.htaccess` 301-redirect generator for renamed categories.
- **breadcrumb-migration-primary-category** — Lets editors define and bulk-manage a primary category per post without altering existing category assignments.
- **breadcrumb-migration-taxonomy-exporter** — Exports `category` or `post_tag` taxonomies to JSON/CSV for Step 1 of the pipeline (inventory phase).

### `migrate-categories-by-claude`
Editorial mapping artifact: the old 103-item French category taxonomy collapsed into a smaller, English-only category set, produced with Claude assistance. Contains the old→new mapping file, post-count distribution per new category (~2,318 posts referenced), and a diff showing the consolidation changes. The decision record for the taxonomy redesign that feeds the plugin work.

### `migration-python-wp-handling-migration-redirects`
Python script and CSV dataset for generating and managing the HTTP 301 redirects required after renaming or merging WordPress categories. Takes category mapping CSVs as input, produces redirect rule files as output, and ensures no old category URL goes dead after the migration. Supports multiple mapping versions (v2–v6) reflecting iterative editorial decisions.

### `README.md`
Project index. Links the two main themes of the repository — (1) the Breadcrumb Migration Pipeline and its companion WordPress plugins, and (2) WebMCP (a proposed standard for exposing WordPress content as structured tools for AI agents). Entry point for navigating all sub-directories.

---

## Overall Abstract

This repository documents a full content-taxonomy migration for 
French-English WordPress tech blog flaven.fr (~600 posts) running on WordPress, using AI-assisted tooling at every stage.

The core problem: a legacy taxonomy of 103 French-language categories had become an SEO liability. The solution spans three concerns:

**1. Editorial redesign (AI-assisted):** Claude was used to consolidate the old taxonomy into a leaner, English-only category set. The `_prompt` and `migrate-categories-by-claude` directories record the prompts and mapping artifacts produced during this phase.

**2. Semantic enrichment pipeline:** A 4-step Python pipeline (`breadcrumb-migration-pipeline`) fetches WordPress terms, runs spaCy NER, queries Wikidata for canonical entity data, and writes structured breadcrumb proposals to custom MySQL tables (`breadcrumb-migration-pipeline-sql`). A Docker environment (`breadcrumb-migration-pipeline-wp_docker`) provides a safe local staging ground for the whole process.

**3. WordPress-side tooling:** Four companion plugins (`breadcrumb-migration-pipeline-wp_plugins_breadcrumb`) handle the WordPress end: exporting terms for the pipeline, importing validated proposals back, re-assigning posts to new categories without data loss, managing primary categories, and generating `.htaccess` 301 redirects. A standalone Python script (`migration-python-wp-handling-migration-redirects`) also produces redirect rule sets from the category mapping CSVs.

Together, the directories form an end-to-end, reproducible workflow for migrating a content site's taxonomy while preserving SEO equity — combining classical NLP (spaCy), knowledge-graph enrichment (Wikidata), AI-assisted editorial judgment (Claude), and WordPress plugin development.

---

## Short Abstract

AI-assisted taxonomy migration for a French-English WordPress tech blog flaven.fr (~600 posts). A 4-step Python pipeline fetches WordPress terms, enriches them with spaCy NER and Wikidata, then writes structured breadcrumb proposals to MySQL. Four companion WordPress plugins handle the site-side work: exporting terms, importing validated proposals, re-categorising posts, and generating 301 redirects. Claude drove the editorial consolidation of 103 French categories into a leaner English-only taxonomy. Docker provides a local staging environment throughout. The result is an end-to-end, reproducible workflow for taxonomy migration that preserves SEO equity.

---

## Keywords

AI, Claude, WordPress, SEO, taxonomy, breadcrumb, category migration, editorial, NLP, spaCy, NER, Wikidata, knowledge graph, semantic enrichment, Python, MySQL, Docker, WordPress plugin, 301 redirect, htaccess, URL migration, content taxonomy, tag management, primary category, schema markup, pipeline, automation, flaven.fr


---

## YouTube Series Proposals (IA Claude code propositions)

**Series title:** *AI-Powered WordPress Taxonomy Migration — From Chaos to Clean SEO*

**Total: 10 videos.** Episodes 3–9 are hands-on/demo; 1, 2, 10 are concept/strategy. Natural split: 3-episode mini-series on pipeline (4–6), 2-episode mini-series on plugins + redirects (8–9).

---

**#1 — The Problem: Why 103 French Categories Was an SEO Disaster**
Overview of the starting point: legacy French taxonomy, duplicate categories, broken URLs, SEO dilution. Sets the stakes and the roadmap for the whole series. No code, pure editorial thinking.

**#2 — Using Claude to Redesign Your Category Taxonomy**
Live walkthrough of the AI-assisted consolidation: prompts used, how Claude proposed the old→new mapping, how to validate the output editorially. Covers the `_prompt` and `migrate-categories-by-claude` directories.

**#3 — Spinning Up a Local WordPress Lab with Docker**
Practical episode: `docker-compose.yml` walkthrough, import a production DB dump, update site URLs, verify everything works at `localhost:8080`. Covers `breadcrumb-migration-pipeline-wp_docker`.

**#4 — Build a Taxonomy Inventory Pipeline with Python and WordPress**
Step 1 of the pipeline: connect Python to a WordPress MySQL DB, fetch all tags and categories with post counts, export to CSV. Covers `001_step_1_list_tags_categories_wp.py`.

**#5 — Named Entity Recognition on Your WordPress Tags with spaCy**
Step 2: run spaCy NER on taxonomy terms, detect entity types (ORG, PERSON, GPE, PRODUCT…), understand what your tags actually mean semantically. Covers `002_step_2_spacy_ner.py`.

**#6 — Enrich WordPress Terms with Wikidata**
Step 3: query Wikidata API to attach canonical IDs, labels, and descriptions to each term. Why knowledge graphs matter for SEO. Covers `003_step_3_wikidata_enrich.py`.

**#7 — Generate Breadcrumb Proposals and Store Them in MySQL**
Step 4 + SQL schema: write enriched proposals to custom tables, validate state machine (pending → approved → published), JSON breadcrumb array structure. Covers `004_step_4_breadcrumb_proposal.py` and `create_tables.sql`.

**#8 — Four WordPress Plugins That Wire the Pipeline to Your Site**
Plugin tour: taxonomy exporter, breadcrumb publisher, category migration drag-and-drop UI, primary category setter. Demo in the Docker environment. Covers `breadcrumb-migration-pipeline-wp_plugins_breadcrumb`.

**#9 — 301 Redirects at Scale: No Old URL Left Behind**
Generate `.htaccess` redirect rules from category mapping CSVs with Python. Why this step is non-negotiable for SEO. Covers `migration-python-wp-handling-migration-redirects`.

**#10 — WebMCP: Exposing Your WordPress Site as AI Agent Tools**
Bonus/forward-looking episode: what WebMCP is, why structured content exposure matters for AI agents, how this project connects to the broader agentic web trend.

  