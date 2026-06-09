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

---

## YouTube Video Descriptions — Actual Published Videos

> Blog post: https://wp.me/p3Vuhl-3rb
> GitHub: https://github.com/bflaven/
> YouTube channel: https://www.youtube.com/channel/UCnUBoVx9Yai3wirPBvNpNQw

---

### Video 1 of 3 — `001_a_ia_seo_ia_semantic_breadcrumb_webmcp.mov`

**Best YouTube Title:**
```
WordPress Taxonomy Pipeline Pt.1: Fetch Tags + spaCy NER in Python & Docker
```

**Best YouTube Description:**
```
Part 1 of 2 | AI-Powered WordPress Taxonomy Migration

In this video I walk through the first half of a 4-step Python pipeline
that semantically enriches WordPress tags using NLP and knowledge graphs —
all running locally in Docker.

What you will see:

Step 1 — Connect Python directly to a WordPress MySQL database and fetch
100 taxonomy terms (post_tag) with post counts. No plugin required — raw
SQL via Python.
Command used:
  python source/pipeline/001_step_1_list_tags_categories_wp.py \
    --limit 100 --taxonomy post_tag --no-dry-run

Step 2 — Run spaCy Named Entity Recognition (NER) on each tag to classify
them automatically: is "Amazon" a company (ORG), a location (GPE), or a
product (PRODUCT)? NER answers that without any manual labelling.
Command used:
  python source/pipeline/002_step_2_spacy_ner.py \
    --limit 100 --taxonomy post_tag --no-dry-run

Step 3 starts — Wikidata enrichment kicks off for 100 tags. Because the
Wikidata API queries take several minutes to complete, I leave Step 3
running and pick up the results in Part 2 (video 001_b).

Stack used:
- Python 3.9 managed via Anaconda (conda env: tags_treatment)
- Docker + WordPress + phpMyAdmin running locally on ports 8080 / 8081
- spaCy NER model: en_core_web_md
- MySQL connector for direct WordPress DB access

Why this matters for SEO:
Most WordPress sites accumulate taxonomy chaos — hundreds of tags with
zero semantic meaning attached. This pipeline is the first step toward
converting raw taxonomy strings into structured, AI-readable breadcrumb
proposals. That is the foundation for GEO (Generative Engine
Optimization): making your content legible to LLMs and AI agents, not
just to search-engine crawlers.

Full article: https://wp.me/p3Vuhl-3rb
GitHub: https://github.com/bflaven/

Continue in Part 2 (001_b): Wikidata results + breadcrumb JSON +
WordPress plugin demo.
```

**Best Keywords for YouTube:**
```
WordPress taxonomy migration, Python WordPress pipeline, spaCy NER WordPress,
Named Entity Recognition SEO, Docker WordPress local, WordPress tags cleanup,
Python MySQL WordPress, semantic SEO, breadcrumb pipeline, GEO generative
engine optimization, taxonomy enrichment, spaCy tutorial, WordPress SEO
automation, conda Python environment, Wikidata WordPress
```

**Best Hashtags for YouTube:**
```
#WordPress #SEO #Python #spaCy #NLP #NER #Docker #taxonomy #breadcrumb
#GEO #AI #WordPressDev #ContentStrategy #Wikidata #MachineLearning
#SemanticSEO #PythonTutorial #WordPressPlugin #MySQL #Anaconda
```

---

### Video 2 of 3 — `001_b_ia_seo_ia_semantic_breadcrumb_webmcp.mov`

**Best YouTube Title:**
```
WordPress Taxonomy Pipeline Pt.2: Wikidata + Breadcrumb JSON & WP Plugin Demo
```

**Best YouTube Description:**
```
Part 2 of 2 | AI-Powered WordPress Taxonomy Migration

Continuing from Part 1 — Step 3 (Wikidata enrichment) has finished
processing 100 WordPress tags. Now I complete the pipeline and wire the
output directly into WordPress.

What you will see:

Step 3 results — Each tag now carries a Wikidata canonical Q-number,
multilingual labels, and a human-readable description. "Airbnb" is no
longer just a string — it is a knowledge-graph entity with provenance,
description, and links to related concepts.

Step 4 — Write enriched proposals to two custom MySQL tables
(wp_breadcrumb_terms, wp_breadcrumb_proposals) that sit alongside
WordPress core tables without touching them. Each term gets a structured
JSON breadcrumb array, e.g.:
  [
    {"label": "Home",   "url": "/"},
    {"label": "Tech",   "url": "/category/tech"},
    {"label": "Airbnb", "url": "/tag/airbnb"}
  ]
Command used:
  python source/pipeline/004_step_4_breadcrumb_proposal.py \
    --limit 100 --taxonomy post_tag --no-dry-run

WordPress plugin demo — The breadcrumb-migration plugin imports the
validated JSON proposals back into WordPress. I show how the admin UI
displays the enriched proposals and how the structured breadcrumb data
appears on tag archive pages in the Docker environment.

Stack used:
- Python 3.9 + Wikidata REST API
- MySQL custom tables alongside WordPress core
- breadcrumb-migration WordPress plugin
- Docker local WordPress environment (localhost:8080 / localhost:8081)

Why this matters:
The JSON breadcrumb proposals are the bridge between raw taxonomy strings
and structured, machine-readable content. Schema-markup breadcrumbs signal
to search engines AND AI agents where each page sits in your site
hierarchy. That is critical for both classical SEO link equity and GEO —
making your content usable by LLMs that reason over structured knowledge,
not free-form HTML.

Full article: https://wp.me/p3Vuhl-3rb
GitHub: https://github.com/bflaven/

Missed Part 1? Watch the setup + Steps 1 and 2 first.
```

**Best Keywords for YouTube:**
```
Wikidata WordPress SEO, knowledge graph enrichment, WordPress breadcrumb
plugin, structured data WordPress, JSON breadcrumb schema, MySQL WordPress
custom tables, WordPress taxonomy enrichment, breadcrumb schema markup,
Python Wikidata API, WordPress plugin demo, GEO generative engine
optimization, semantic breadcrumb, content migration WordPress, category
migration WordPress, spaCy Wikidata pipeline
```

**Best Hashtags for YouTube:**
```
#WordPress #SEO #Wikidata #KnowledgeGraph #breadcrumb #Python #MySQL
#WordPressPlugin #taxonomy #schemaMarkup #GEO #AI #contentMigration
#structuredData #Docker #SemanticSEO #JSONSchema #WordPressDev
#NLP #TaxonomyMigration
```

---

### Video 3 of 3 — `002_ia_seo_ia_semantic_breadcrumb_webmcp.mov`

**Best YouTube Title:**
```
WebMCP Explained: Turn Your WordPress Site into Tools for AI Agents
```

**Best YouTube Description:**
```
WebMCP: The Next Layer of Your WordPress Strategy

This video introduces WebMCP — a concept and WordPress plugin that exposes
your site's structured content as callable tools that AI agents can query,
browse, and reason over. Think of it as MCP (Model Context Protocol) for
the open web, applied directly to a WordPress installation.

What you will see:

What WebMCP is — how it differs from a standard REST API or an RSS feed,
and why that distinction matters when the consumer is an AI agent rather
than a human browser.

Why "the end of clicks" is already happening — AI assistants don't browse;
they query structured data sources and synthesise answers. If your content
is not structured and semantically enriched, it is invisible to this layer.

WordPress plugin demo — how the WebMCP plugin exposes your posts,
categories, and taxonomy terms as agent-readable tool endpoints that an
LLM or AI agent can call programmatically.

How this connects to the full pipeline — the breadcrumb migration work from
Parts 1 and 2 (clean taxonomy + Wikidata enrichment + structured breadcrumbs)
feeds directly into what WebMCP exposes. Dirty taxonomy = poor WebMCP
signal. Clean, semantically enriched taxonomy = rich, trustworthy agent tools.

The big shift:
We have moved from SEO (ranking pages for humans via search engines) to
GEO (Generative Engine Optimization — making content legible to LLMs and
AI agents). WebMCP is one concrete infrastructure layer that makes this
shift real for any WordPress site.

Stack used:
- WordPress plugin (WebMCP)
- MCP — Model Context Protocol (Anthropic / open standard)
- Structured content, JSON-LD, schema markup
- Docker local WordPress environment

Full article: https://wp.me/p3Vuhl-3rb
GitHub: https://github.com/bflaven/

Watch Parts 1 and 2 for the Python pipeline that creates the structured
taxonomy data this layer exposes.
```

**Best Keywords for YouTube:**
```
WebMCP WordPress, Model Context Protocol WordPress, AI agents WordPress,
WordPress AI tools, GEO generative engine optimization, structured content
AI, WordPress plugin AI, MCP plugin WordPress, agentic web WordPress,
LLM content strategy, WordPress SEO 2025, WordPress schema markup,
AI discoverability, WordPress structured data, MCP tutorial
```

**Best Hashtags for YouTube:**
```
#WebMCP #MCP #WordPress #AI #GEO #AIAgents #SEO #structuredData
#schemaMarkup #WordPressPlugin #LLM #GenerativeAI #ContentStrategy
#ModelContextProtocol #AgenticWeb #WordPress2025 #SemanticWeb
#AISearch #WordPressDev #FutureOfSEO
```

---

## LinkedIn Posts — Actual Published Videos

> Context: the main blog post promo ("WebMCP, the End of Clicks, and the Semantic Upgrade Your WordPress Site Actually Needs") is already published on LinkedIn. These 3 posts promote the companion videos.
> Blog post: https://wp.me/p3Vuhl-3rb
> YouTube channel: https://www.youtube.com/channel/UCnUBoVx9Yai3wirPBvNpNQw
> GitHub: https://github.com/bflaven/

> LinkedIn format notes: hook in line 1 (visible before "see more"), short paragraphs, white space, 3–5 hashtags max, ~1,000–1,500 chars sweet spot.

---

### LinkedIn Post — Video 1 of 3 (`001_a_ia_seo_ia_semantic_breadcrumb_webmcp.mov`)

**Hook / Title line:**
```
I just ran a Python pipeline that semantically understands every WordPress tag on my site — before touching a single line of WordPress code.
```

**Full LinkedIn Post:**
```
I just ran a Python pipeline that semantically understands every WordPress
tag on my site — before touching a single line of WordPress code.

Here is what happened in 4 minutes of terminal output.

Step 1 — Python connects directly to the WordPress MySQL database (no
plugin, no REST API) and pulls 100 tags with post counts. You see exactly
what lives in your taxonomy.

Step 2 — spaCy Named Entity Recognition runs on every tag.
"Airbnb" → ORG. "Afghanistan" → GPE. "Amazon" stops being ambiguous.
Your tags have semantic identity now.

Step 3 starts — Wikidata enrichment kicks off: 100 API calls to the
world's largest open knowledge graph. Each tag will get a canonical
Q-number, multilingual labels, and a human-readable description.

(Step 3 takes a few minutes for 100 tags. I leave it running and pick
up the results in Part 2.)

Why does this matter for your site?

Classic SEO ranks pages for human readers.
GEO — Generative Engine Optimization — requires that AI agents can
*understand* your content taxonomy, not just crawl it.
Semantically enriched tags are the first layer of that signal.

Stack: Python 3.9 · Anaconda · Docker (WordPress + MySQL + phpMyAdmin)
· spaCy en_core_web_md

▶ Video (Part 1 of 2): [YouTube link]
📖 Full article: https://wp.me/p3Vuhl-3rb

#WordPress #SEO #Python #NLP #GEO
```

**Best LinkedIn Hashtags:**
```
#WordPress #SEO #Python #NLP #GEO
```

---

### LinkedIn Post — Video 2 of 3 (`001_b_ia_seo_ia_semantic_breadcrumb_webmcp.mov`)

**Hook / Title line:**
```
Wikidata just told me that "Adolph Zukor" — a tag on my WordPress site — is a person born in 1873, founder of Paramount Pictures. In 3 languages. Automatically.
```

**Full LinkedIn Post:**
```
Wikidata just told me that "Adolph Zukor" — a tag on my WordPress site —
is a person born in 1873, founder of Paramount Pictures. In 3 languages.
Automatically.

That is Step 3 of my taxonomy enrichment pipeline, finished.

Here is the full picture of Part 2.

Step 3 done — Every tag now carries a Wikidata Q-number (canonical ID),
labels, and descriptions from the world's largest open knowledge graph.
No manual research. No Wikipedia scraping. Pure structured data.

Step 4 — The pipeline writes structured breadcrumb proposals into custom
MySQL tables that sit alongside WordPress core without modifying it.
Each tag gets a JSON breadcrumb array:

[
  {"label": "Home",         "url": "/"},
  {"label": "Film History", "url": "/category/film-history"},
  {"label": "Adolph Zukor", "url": "/tag/adolph-zukor"}
]

WordPress plugin demo — The breadcrumb-migration plugin reads these
proposals from MySQL and publishes enriched breadcrumbs onto tag archive
pages. Zero manual entry.

This JSON structure is the bridge between raw taxonomy strings and
structured, machine-readable content that search engines AND AI agents
can reason over.

Schema breadcrumbs tell Google where a page sits in your site hierarchy.
They tell AI agents exactly the same thing — and that signal matters
more every month as AI-first search grows.

Stack: Python · Wikidata REST API · MySQL · breadcrumb-migration WP plugin
· Docker

▶ Video (Part 2 of 2): [YouTube link]
📖 Full article: https://wp.me/p3Vuhl-3rb

#WordPress #Wikidata #SEO #StructuredData #AI
```

**Best LinkedIn Hashtags:**
```
#WordPress #Wikidata #SEO #StructuredData #AI
```

---

### LinkedIn Post — Video 3 of 3 (`002_ia_seo_ia_semantic_breadcrumb_webmcp.mov`)

**Hook / Title line:**
```
Clicks are dying. AI agents don't browse your site — they query structured data sources and synthesise answers. If your WordPress content isn't machine-readable, it is already invisible to this layer.
```

**Full LinkedIn Post:**
```
Clicks are dying. AI agents don't browse your site — they query structured
data sources and synthesise answers.

If your WordPress content isn't machine-readable, it is already invisible
to this layer.

That is the problem WebMCP solves.

WebMCP is a concept (and a WordPress plugin) that exposes your site's
posts, categories, and taxonomy as callable tools — endpoints that AI
agents can query directly, the same way a developer calls an API.

Think of MCP (Model Context Protocol) applied to the open web, running
on a standard WordPress installation.

In this video I show:

→ What WebMCP is and how it differs from REST APIs or RSS feeds
→ Why "the end of clicks" is already happening in AI-first search
→ A live plugin demo running in a local Docker WordPress environment
→ How this connects to the taxonomy enrichment pipeline from Parts 1 & 2

The logic is straightforward:
Clean, Wikidata-enriched taxonomy + structured breadcrumbs
→ richer WebMCP signal
→ better AI agent discoverability

Dirty taxonomy = invisible to agents.
Clean taxonomy = trustworthy, queryable, AI-readable content.

We have moved from SEO to GEO (Generative Engine Optimization).
WebMCP is one concrete infrastructure step to get there on WordPress.

Stack: WordPress · WebMCP plugin · MCP (Model Context Protocol) · Docker

▶ Video: [YouTube link]
📖 Full article: https://wp.me/p3Vuhl-3rb

#WebMCP #AI #WordPress #GEO #MCP
```

**Best LinkedIn Hashtags:**
```
#WebMCP #AI #WordPress #GEO #MCP
```
