# editorial_simple_rag

**Modular RAG system — query a document corpus in natural language**
Use case: Editorial / CMS JSON export

---

## Changelog

### v1.5 — 2026-04-10 · Azure config + retrieval fix + multilingual editorial

**Azure OpenAI — `.env` auto-loading**
- `src/utils/config.py` — `_load_dotenv()` added; called from `load_config()` on every startup. Reads `.env` from the project root into `os.environ`. Uses `python-dotenv` if installed, falls back to a built-in line parser so it works without any extra dependency.
- `config.yaml` — Azure block rewritten: `endpoint_env: "ENDPOINT"` and `api_key_env: "API_KEY"` now name the `.env` keys explicitly. The `endpoint:` inline fallback is kept but can remain empty.
- `src/llm/llm_client.py` and `src/llm/embeddings.py` — both now read the Azure endpoint from the env var named by `endpoint_env` (with inline `endpoint:` as fallback), consistent with the API-key pattern.
- `.env` format expected: `ENDPOINT=https://...` and `API_KEY=...` (no quotes required).

**Retrieval rules — `rfp_pricing` doc_type filter removed**
- `config/retrieval_rules.yaml` — removed `filters: {doc_type: ["rfp_public_tender"]}` from the `rfp_pricing` rule. Readers tag every chunk with the file's extension (`"pdf"`, `"tsv"`, `"xlsx"`), not with the chunking-rule ID. The filter was silently wiping all results for every price-related query.
- French keyword synonyms added to `rfp_pricing`: `coût`, `prix`, `montant`, `tarif`, `devis` — the rule now fires on French queries too.
- Root cause documented: `filters.doc_type` must match the `doc_type` value set by the reader (`"pdf"`, `"tsv"`, `"xlsx"`, `"editorial_article"`), not the chunking rule ID.

**Multilingual editorial corpus — `langdetect` support**
- `spacy.default_language: ""` (empty) is the correct setting for mixed-language corpora (e.g. ~500 French posts + ~75 English posts). When empty, `langdetect` detects the language per document and the appropriate spaCy model is loaded automatically.
- `spacy.default_language: "fr"` (or `"en"`) forces a single language for the whole corpus — use this for monolingual corpora to avoid running langdetect and to load exactly one spaCy model.
- Prerequisite: `pip install langdetect` (see Prerequisites section below).

**Full clean-slate reset**
- `reset_corpus.py --yes` deletes only pipeline artefacts (checkpoints + index) for the active use case.
- To wipe **all** generated data and start from scratch:
  ```bash
  rm -rf data/checkpoints data/indexes data/evaluations logs data/rag_cache.db
  ```
  Source corpus files in `data/corpora/` and `.env` are preserved.

### v1.6 — 2026-04-13 · Journalist use case + large-corpus robustness

**Journalist use case**
- `config/workflow_paths.yaml` — `journalist` entry added with correct `corpus_dir`, `index_dir`, and `checkpoint_dir` paths (previously all three pointed to the corpus dir, which would have landed index and checkpoint files in the wrong place).
- `active_use_case: "journalist"` is now a first-class supported value in `config.yaml`.

**CSV corpus reader (`filename,text` format)**
- `src/ingestion/readers.py` — new `read_csv_corpus()` reads flat CSV dumps where each row is one document (columns: `filename`, `text`). Used for the journalist corpus (`EPS_FILES_20K_NOV2025.txt` — a ~100 MB CSV file containing ~20 000 documents).
- `read_txt()` auto-detects the CSV format: if the first line is exactly `filename,text`, it dispatches to `read_csv_corpus()` transparently. All plain `.txt` files are unaffected.
- `csv.field_size_limit(sys.maxsize)` set before parsing — required when individual article fields exceed Python's default 128 KB CSV field limit.

**spaCy E088 — text exceeds 1 000 000 characters**
- `src/parsing/chunker.py` — new `_split_text_for_spacy()` pre-splits texts larger than 900 000 chars on paragraph boundaries before calling `nlp()`. spaCy's hard limit is 1 000 000 chars; passing a 100 MB document directly triggered `ValueError [E088]`. Documents under 900 K chars are unaffected.
- `split_sentences()` processes each segment sequentially and concatenates the resulting sentences.

**spaCy model — speed vs. accuracy**
- `config.yaml` — `spacy.models.en` switched from `en_core_web_trf` (transformer, accurate but very slow on large corpora) to `en_core_web_md` (medium, 10–20× faster). The transformer model can be restored for accuracy-critical use cases by swapping the value back.

**Progress logging in chunker**
- `src/parsing/chunker.py` — `chunk_all_documents()` now logs `[i/N] Chunking: <source> (X chars)` for every document so long runs show visible progress.
- `split_sentences()` logs `spaCy segment [i/N] — X chars` when a document is large enough to be pre-split.

**`check_status.py` — LLM model key**
- Fixed `KeyError: 'model'` when `llm.provider` is `azure`. The config uses `azure_deployment` instead of `model` for Azure; `check_status.py` now falls back to `azure_deployment` when `model` is absent.

### v1.5.1 — 2026-04-10 · bridge_export — `--source` and `--out` flags

- `bridge_export.py` — added `--source` and `--out` CLI flags. Previously the source JSON file and output path were hardcoded in `config/bridge_wp.yaml` with no way to override from the command line. Now you can point the exporter at any corpus file without touching the config:
  ```bash
  python bridge_export.py \
    --source data/corpora/editorial/CMS_EXPORT_2026_2/my_posts.json \
    --out data/bridge/rag_bridge.json
  ```
  Both flags are optional — when omitted the values from `bridge_wp.yaml` are used as before.

### v1.4 — 2026-04-10 · RFP use case + embedding stability

**RFP use case**
- `active_use_case: "rfp"` now fully operational — PDF, DOCX, TSV, XLSX corpora
- `config/chunking_rules.yaml` — `rfp_public_tender` rule now matches by **path** (`any_path_contains: ["rfp"]`) instead of filename keywords; previously no RFP files matched at all
- All chunk sizes lowered to **150 words** across all rules and the global default to stay within the nomic-embed-text 2048-token architecture limit

**Language detection**
- `spacy.default_language` added to `config.yaml` — when set, forces that language for all documents in the corpus and loads exactly one spaCy model; previously all non-CMS readers hardcoded `"en"`, blocking auto-detection and causing unnecessary model loads
- Non-CMS readers (`read_pdf`, `read_docx`, `read_txt`, `read_tsv`, `read_xlsx`) no longer set `"language": "en"` — language is now detected by `langdetect` or forced by `default_language`
- `step_1_001_ingest.py` reads `spacy.default_language` from config and forces it for all documents when set

**Embedding stability**
- `src/llm/embeddings.py` — switched from the old `/api/embeddings` endpoint to the new `/api/embed` endpoint (`client.embed`) with `truncate=True`; the old endpoint ignored `num_ctx` on already-loaded models, causing persistent HTTP 500 errors
- `options` dict removed from the new `/api/embed` call — it caused HTTP 400 on some Ollama builds
- Added `_safe_truncate()` capping input at **1500 chars** (~375 BPE tokens) before each Ollama call as a Python-side safety net
- Root cause confirmed: `nomic-embed-text` (nomic-bert architecture) has a hard **2048-token context window**; prior chunk sizes of 350–800 words could produce 1 000–2 000+ tokens of French legal text, reliably exceeding the limit

**Chunker robustness**
- `src/parsing/chunker.py` — `_hard_split_sentence()` added; any "sentence" returned by spaCy that exceeds `chunk_size` words (e.g. a full PDF table page with no punctuation) is now split word-by-word before grouping, preventing single-sentence chunks from blowing past the model limit

### v1.3 — 2026-04-09 · WordPress bridge + semantic search plugin

- **`bridge_export.py`** — new standalone script; reads `sample_posts.json` (WordPress REST API format), normalises 74 posts to the exchange format (HTML stripped, date truncated), writes `data/bridge/rag_bridge.json`. Controlled by `config/bridge_wp.yaml`. WP API fetch is stubbed behind `wordpress.enabled: false`.
- **`config/bridge_wp.yaml`** — updated: `wordpress.enabled` flag (false = local file, true = live API); `bridge.local_source` and `bridge.exchange_file` explicit path keys.
- **`data/bridge/rag_bridge_schema.json`** — exchange format spec v1.0: fields `id`, `title`, `url`, `date`, `slug`, `excerpt`, `text`. Tags and categories excluded (Option B — IDs only, no label resolution).
- **`data/bridge/rag_schema.sql`** — reference MySQL/MariaDB schema for `rag_posts` + `rag_results`; includes utility queries for TTL purge, empty, and drop.
- **`rag-semantic-search/`** — WordPress plugin (PHP). Activate → creates `wp_rag_posts` + `wp_rag_results`. Uninstall → drops both tables. Admin page: live row counts, JSON import (idempotent upsert), empty-tables button. Front-end: `[rag_search]` shortcode with Standard / Semantic mode toggle, scored result cards, MySQL FULLTEXT search with LIKE fallback.

### v1.2 — 2026-04-08 · Bug fixes + UX

- **Ollama context window fix** — `embeddings.ollama_num_ctx: 8192` added to `config.yaml`; passed as `options={"num_ctx": ...}` to every Ollama embedding call — fixes "input length exceeds context length" error with `nomic-embed-text`
- **Chunking** — `editorial_article` rule reduced from 800 → 400 words; safer subword token budget within the 8192 context window
- **Streamlit** — `NameError: st is not defined` fixed in `_render_sources()` (lazy import added)
- **Streamlit** — "🗑️ Clear" button added to the RAG tab header; clears visible chat and resets E7 conversational memory in one click
- **spaCy config** — model selection moved from hardcode to `config.yaml` (`spacy.models.en`, `spacy.models.fr`, `spacy.fallback`); swap models without touching code

### v1.1 — 2026-04-08 · WordPress JSON + utility scripts

- `src/ingestion/readers.py` — `read_json_cms()` now handles the WordPress REST API format natively: `title.rendered` and `content.rendered` are extracted, HTML is stripped via BeautifulSoup, HTML entities decoded, title prepended to content text
- `sample_posts.json` updated to WordPress REST API format (real HTML, encoded entities)
- 6 utility/orchestration scripts added or rewritten: `run_pipeline.py`, `reset_corpus.py`, `check_status.py`, `validate_pipeline.py`, `test_index.py`, `merge_indexes.py` — all use the current `load_config()` / `get_*_dir()` API

### v1.0 — 2026-04-08 · Initial build

- Full 8-step pipeline operational (ingest → parse → embed → index → query → synthesize → interface → evaluate)
- Editorial use case active — CMS JSON corpus (WordPress / Strapi / Contentful / custom API)
- spaCy sentence-boundary chunking: `en_core_web_trf` (English), `fr_dep_news_trf` (French)
- FAISS `IndexFlatIP` — cosine similarity, exact search
- Cross-encoder re-ranking (E2): `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Semantic cache (E1) — SQLite, cosine similarity threshold 0.92
- Conversational memory (E7) — follow-up detection + LLM rewrite
- LLM-as-a-judge evaluation (E6) — faithfulness, relevance, context precision
- Streamlit UI: 4 tabs (RAG, History, Debug, Definitions)
- All 5 levers controlled exclusively via YAML — no hard-coded parameters

---

## Overview

Sequential RAG (Retrieval-Augmented Generation) pipeline driven entirely by YAML.
No hard-coding: all parameters (embeddings, chunking, retrieval, LLM) live in `config/config.yaml`.

The LLM never reads full documents — it only sees the passages the system selected.
This makes the system fast, cost-effective, and auditable.

**Supported use cases:** `rfp` · `hr` · `editorial` · `journalist` · `screenwriting` · `support`
Switch by changing `active_use_case` in `config/config.yaml`. Each use case has its own corpus directory and chunking rules.

---

## Prerequisites

```bash
conda activate ia_achats          # Python 3.11

# Ollama (required for embeddings and Tier 2 LLM)
ollama serve                      # in a dedicated terminal
ollama pull nomic-embed-text      # embedding model (768 dim, 2048-token context)
ollama pull llama3.1              # local LLM (Tier 2)

# Verify the embedding model context window
ollama show nomic-embed-text
# Expected: context length 2048 (nomic-bert architecture hard limit)
# num_ctx may show 8192 in Parameters — this is Ollama's target, but the
# architecture caps at 2048. Chunk sizes in chunking_rules.yaml are set
# accordingly (150 words ≈ 300 BPE tokens, safely under the 2048 limit).
```

spaCy models (already installed in `ia_achats`):

```bash
# English
python -m spacy download en_core_web_md
python -m spacy download en_core_web_trf

# French
python -m spacy download fr_core_news_md
python -m spacy download fr_dep_news_trf
```

Azure credentials in `.env` at the project root (only if `llm.provider: azure`):

```
ENDPOINT=https://<your-resource>.openai.azure.com
API_KEY=<your-azure-api-key>
```

The file is loaded automatically by `load_config()` on startup — no `source .env` or shell export required.
The key names (`ENDPOINT`, `API_KEY`) are configured in `config.yaml` under `azure.endpoint_env` and `azure.api_key_env`.

Optional but recommended — install `python-dotenv` for robust `.env` parsing:

```bash
pip install python-dotenv langdetect
```

`langdetect` is required for mixed-language corpora (i.e. when `spacy.default_language` is empty).

---

## Quick start

```bash
# Navigate to project root
cd editorial_simple_rag

# Activate environment
conda activate ia_achats

# 1. Drop your CMS JSON files into the corpus directory
#    data/corpora/editorial/CMS_EXPORT_2026/

# 2a. Build the index — one-liner orchestrator (steps 1 → 4)
python run_pipeline.py --build
python run_pipeline.py --build --dry-run


# 2b. Or run each step individually
python scripts/step_1_001_ingest.py
python scripts/step_2_001_parse.py
python scripts/step_3_001_embed.py
python scripts/step_4_001_index.py

# 3. Verify everything is coherent
python check_status.py
python validate_pipeline.py

# 4a. Interactive CLI
python scripts/step_7_001_interface.py

# 4b. Streamlit web UI
streamlit run scripts/step_7_001_interface.py -- --streamlit
```

---

## Pipeline architecture

```
CMS JSON export (articles)
    │
    ▼
step_1_001_ingest.py     → data/checkpoints/.../step_1_documents.json
step_2_001_parse.py      → data/checkpoints/.../step_2_chunks.json       (spaCy + business rules)
step_3_001_embed.py      → data/checkpoints/.../step_3_embeddings.npy    (Ollama nomic-embed-text)
step_4_001_index.py      → data/indexes/.../index.faiss + chunks.json    (IndexFlatIP)
    │
    ▼ (on each query)
step_5_001_query.py      → embed query → FAISS search → filter → boost → rerank (E2)
step_6_001_synthesize.py → prompt builder → LLM (Tier 1/2/3) → Answer + sources
step_7_001_interface.py  → CLI REPL or Streamlit UI
step_8_001_evaluate.py   → LLM-as-a-judge: faithfulness / relevance / context precision
```

Each step is **runnable standalone**:

```bash
python scripts/step_1_001_ingest.py
python scripts/step_2_001_parse.py
python scripts/step_3_001_embed.py
python scripts/step_4_001_index.py
python scripts/step_5_001_query.py --query "What did we publish about climate?"
python scripts/step_6_001_synthesize.py --query "Which authors covered the elections?"
python scripts/step_7_001_interface.py
python scripts/step_8_001_evaluate.py --limit 10
```

---

## Project structure

```
editorial_simple_rag/
│
├── run_pipeline.py               ← orchestrate build (steps 1–4) and/or query
├── reset_corpus.py               ← delete checkpoints + index for a use-case
├── check_status.py               ← corpus / artefact / cache status report
├── validate_pipeline.py          ← artefact coherence checks (step 1 → 4)
├── test_index.py                 ← FAISS index integrity (null vectors, metadata)
├── merge_indexes.py              ← merge two FAISS indexes into one
├── bridge_export.py              ← export CMS posts → rag_bridge.json (WP bridge)
│
├── config/
│   ├── config.yaml               ← master configuration (single entry point)
│   ├── workflow_paths.yaml       ← corpus / index / checkpoint paths per use case
│   ├── chunking_rules.yaml       ← business rules for chunking (lever 2)
│   ├── retrieval_rules.yaml      ← business rules for retrieval (lever 3)
│   └── bridge_wp.yaml            ← WordPress bridge config (enabled flag, paths, DB)
│
├── data/
│   ├── corpora/
│   │   ├── editorial/CMS_EXPORT_2026/   ← CMS JSON export (WordPress REST API or flat format)
│   │   ├── journalist/EPSTEIN_FILES_20K_1/ ← CSV corpus (filename,text columns)
│   │   ├── rfp/AO_2025_003/             ← PDF, DOCX, TSV, XLSX tender documents
│   │   └── hr/04_JOB_OFFER_8779878/     ← CVs and job descriptions
│   ├── bridge/
│   │   ├── rag_bridge_schema.json        ← exchange format spec (field definitions)
│   │   ├── rag_schema.sql                ← reference MySQL schema for WP tables
│   │   └── rag_bridge.json               ← generated by bridge_export.py (gitignored)
│   ├── checkpoints/              ← JSON snapshots after each step
│   ├── indexes/                  ← FAISS index + chunk metadata
│   ├── evaluations/              ← evaluation results (step 8)
│   └── rag_cache.db              ← SQLite cache (created on first run)
│
├── logs/                         ← one log file per step
│
├── scripts/
│   ├── step_1_001_ingest.py      ← read corpus files → documents
│   ├── step_2_001_parse.py       ← spaCy sentence split → chunks
│   ├── step_3_001_embed.py       ← embed chunks via Ollama
│   ├── step_4_001_index.py       ← build FAISS index
│   ├── step_5_001_query.py       ← embed query → retrieve → rerank
│   ├── step_6_001_synthesize.py  ← prompt builder → LLM → Answer
│   ├── step_7_001_interface.py   ← CLI + Streamlit UI
│   └── step_8_001_evaluate.py    ← LLM-as-a-judge evaluation
│
└── src/
    ├── ingestion/readers.py          ← readers: JSON/CMS (WP REST API + flat), CSV corpus (filename,text), TXT, PDF, DOCX, TSV, XLSX
    ├── parsing/chunker.py            ← sentence splitter + chunk grouper + business rules
    ├── llm/
    │   ├── embeddings.py             ← EmbeddingClient (Ollama / Azure)
    │   ├── llm_client.py             ← LLMClient (Ollama / Azure)
    │   └── reranker.py               ← CrossEncoder wrapper (E2)
    ├── memory/conversation.py        ← turn history + follow-up rewrite (E7)
    ├── vector_store/faiss_store.py   ← FAISSStore: build / save / load / search
    └── utils/
        ├── config.py                 ← load_config(), get_corpus_dir(), etc.
        └── db_manager.py             ← SQLite semantic cache + history (E1)
```

---

## The 5 levers (all YAML-controlled)

| # | Lever | Key parameter | File |
|---|-------|--------------|------|
| L1 | **Embeddings** | `embeddings.provider` / `embeddings.model` | `config.yaml` |
| L2 | **Chunking** | `chunking.size` / `chunking.overlap` / `enable_business_rules` | `config.yaml` + `chunking_rules.yaml` |
| L3 | **Retrieval** | `retrieval.k` / `retrieval.score_threshold` / `enable_business_rules` | `config.yaml` + `retrieval_rules.yaml` |
| L4 | **LLM tier** | `llm.provider` / `llm.model` | `config.yaml` |
| L5 | **Cache** | `database.enabled` / `database.path` | `config.yaml` |

---

## CMS JSON corpus format

The ingestion reader handles two formats transparently. The primary format is the **WordPress REST API** export. The reader also accepts the legacy flat format for backward compatibility.

### WordPress REST API format (primary)

`title` and `content` are objects with a `rendered` key. HTML in rendered fields is automatically stripped via BeautifulSoup (or a regex fallback). HTML entities (e.g. `&#233;` → `é`) are decoded. The title is prepended to the content text so retrieval can match on article headings.

```json
[
  {
    "id": 13148,
    "date": "2026-02-06T11:34:55",
    "date_gmt": "2026-02-06T10:34:55",
    "guid": {"rendered": "https://example.com/?p=13148"},
    "modified": "2026-02-10T08:32:53",
    "slug": "my-article-slug",
    "status": "publish",
    "type": "post",
    "link": "https://example.com/2026/02/my-article-slug/",
    "title":   {"rendered": "Article title here"},
    "content": {"rendered": "<p>HTML content…</p>", "protected": false}
  }
]
```

Fields read by the reader:

| Field | Used as |
|-------|---------|
| `id` | `metadata.post_id` |
| `date` | `metadata.published_at` |
| `link` | `source` (URL) |
| `title.rendered` | `metadata.title` + prepended to text |
| `content.rendered` | main text (HTML stripped) |

### Flat format (legacy / backward-compatible)

```json
[
  {
    "id": "post-001",
    "title": "Article title here",
    "content": "Plain text content…",
    "author": "Marie Dupont",
    "published_at": "2026-03-15T10:30:00Z",
    "tags": ["climate", "environment"],
    "categories": ["World", "Science"],
    "url": "https://cms.example.com/articles/post-001",
    "language": "en"
  }
]
```

Place JSON files in `data/corpora/editorial/CMS_EXPORT_2026/` — multiple files are supported.

> **Dependency:** `beautifulsoup4` (already in `ia_achats`). HTML entities (e.g. `&#233;` → `é`) are decoded automatically.

---

## Chunking — spaCy + business rules

Two independent modes, combinable in `config.yaml`.

### Mode 1 — Business rules (`enable_business_rules: true`)

Adapts chunking parameters per document type detected from path and extension.
Rules are defined in `config/chunking_rules.yaml`.

| Rule ID | Match logic | Chunk size | Notes |
|---------|------------|-----------|-------|
| `rfp_public_tender` | path contains `rfp`, `ao_`, `marche`, or `dce` | 150 words | Dense legal/table PDFs; path-based match catches all files in the rfp corpus |
| `hr_cv` | path contains `hr`, `cv`, or `candidates` | 150 words | |
| `editorial_article` | `.json` extension + path contains `editorial` or `cms` | 150 words | |
| `journalist_article` | path contains `journalist` | 150 words | CSV corpus — one document per row; large files pre-split before spaCy |

> **Why 150 words?** `nomic-embed-text` uses the nomic-bert architecture with a hard **2048-token context limit**. 150 French words × ~2 WordPiece tokens/word ≈ 300 tokens — well within the limit even for dense legal text. The `_safe_truncate()` cap of 1 500 chars in `embeddings.py` is a secondary safety net.

Each rule can also define:
- `keep_together_patterns` — never split before these headings (regex)
- `drop_patterns` — discard matching lines (e.g. page numbers)

### Mode 2 — spaCy sentence boundaries

Uses spaCy to detect sentence boundaries before grouping into chunks.
Without spaCy: sliding word window (may split mid-sentence).
With spaCy: sentences stay intact, chunks are semantically coherent.

The model used per language is configured in `config.yaml` under the `spacy` key:

```yaml
spacy:
  models:
    en: "en_core_web_md"     # swap to "en_core_web_trf" for accuracy (much slower on large corpora)
    fr: "fr_dep_news_trf"    # swap to "fr_core_news_md" for speed
  fallback: "en_core_web_md" # used when document language is unknown
  default_language: ""       # "" = auto-detect per document (langdetect required)
                             # "fr" or "en" = force one language for the entire corpus
```

**`default_language`** — controls how language is determined for each document in step 1:

| Value | Behaviour | Use when |
|-------|-----------|----------|
| `""` (empty) | `langdetect` runs per document; the matching spaCy model is selected automatically | Mixed-language corpora (e.g. ~500 FR + ~75 EN editorial posts) |
| `"fr"` or `"en"` | All documents get that language; `langdetect` is skipped; exactly one spaCy model loads | Monolingual corpora (e.g. an all-French RFP corpus) |

> **Dependency:** `pip install langdetect` is required when `default_language` is empty.

All four models are installed in `ia_achats`:

| Model | Language | Type | Speed |
|-------|----------|------|-------|
| `en_core_web_trf` | English | Transformer | slower, most accurate |
| `en_core_web_md` | English | Medium | faster, good quality |
| `fr_dep_news_trf` | French | Transformer | slower, most accurate |
| `fr_core_news_md` | French | Medium | faster, good quality |

To swap models, edit `config.yaml` — no code change required.

Both modes are **cumulative** (recommended configuration):

```
spaCy → sentence boundaries
  ↓
chunking_rules.yaml → per-type size, keep/drop patterns
  ↓
Well-structured chunks → nomic-embed-text
```

> Any change to `spacy.models` or `chunking` requires rebuilding the index (re-run steps 2 → 4).

---

## LLM tiers — cost and privacy

| Tier | Provider | Cost | Data stays local? |
|------|----------|------|------------------|
| 1 | Static template | Free | Yes |
| 2 | Ollama `llama3.1` | ~Free | Yes |
| 3 | Azure OpenAI `gpt-4.1` | Per token | No — sent to cloud |

**Default:** Tier 2 (local). Tier 3 is opt-in only.
For sensitive corpora, Tier 2 is the recommended mode.

```bash
# Force a specific tier
python scripts/step_6_001_synthesize.py --query "..." --tier 1   # instant, no LLM
python scripts/step_6_001_synthesize.py --query "..." --tier 2   # Ollama (default)
python scripts/step_6_001_synthesize.py --query "..." --tier 3   # Azure GPT-4.1
```

### Enabling Tier 3 (Azure OpenAI)

1. Create `.env` in the project root:
   ```
   ENDPOINT=https://<your-resource>.openai.azure.com
   API_KEY=<your-azure-api-key>
   ```

2. Set in `config/config.yaml`:
   ```yaml
   llm:
     provider: "azure"
     azure_deployment: "gpt-4.1"

   azure:
     endpoint_env: "ENDPOINT"          # name of the env var holding the endpoint URL
     api_key_env: "API_KEY"            # name of the env var holding the API key
     api_version: "2024-12-01-preview"
   ```

3. The `.env` file is loaded automatically — no shell export or `source .env` needed.

> **Note:** `endpoint_env` and `api_key_env` are the key names in your `.env` file, not the values. Change them only if your `.env` uses different variable names.

---

## Step-by-step command reference

### Step 1 — Ingest

```bash
# Active use case from config.yaml
python scripts/step_1_001_ingest.py

# Override use case
python scripts/step_1_001_ingest.py --use-case editorial

# Override corpus directory
python scripts/step_1_001_ingest.py --corpus-dir /path/to/my/files
```

### Step 2 — Parse and chunk

```bash
python scripts/step_2_001_parse.py
python scripts/step_2_001_parse.py --use-case editorial
```

### Step 3 — Embed

```bash
python scripts/step_3_001_embed.py
python scripts/step_3_001_embed.py --use-case editorial
```

### Step 4 — Index

```bash
python scripts/step_4_001_index.py
python scripts/step_4_001_index.py --use-case editorial
```

### Step 5 — Query (standalone)

```bash
# Single question
python scripts/step_5_001_query.py --query "What did we publish about climate?"

# Interactive mode
python scripts/step_5_001_query.py

# Skip cross-encoder (faster)
python scripts/step_5_001_query.py --query "..." --no-rerank

# Override k and score threshold
python scripts/step_5_001_query.py --query "..." --k 10 --threshold 0.15
```

### Step 6 — Synthesize (standalone)

```bash
python scripts/step_6_001_synthesize.py --query "Which authors covered the elections in West Africa?"
python scripts/step_6_001_synthesize.py --query "..." --tier 1
python scripts/step_6_001_synthesize.py --query "..." --tier 2 --no-rerank
python scripts/step_6_001_synthesize.py --query "..." --k 5
```

### Step 7 — Interface

```bash
# CLI interactive mode
python scripts/step_7_001_interface.py

# CLI with use case override
python scripts/step_7_001_interface.py --use-case editorial

# Streamlit web UI
streamlit run scripts/step_7_001_interface.py -- --streamlit
```

CLI special commands:
- `clear` — reset conversational memory for the current session
- `exit` — quit

### Step 8 — Evaluate

```bash
# Evaluate last 5 history entries (default)
python scripts/step_8_001_evaluate.py

# Evaluate more entries
python scripts/step_8_001_evaluate.py --limit 20

# Filter by tier
python scripts/step_8_001_evaluate.py --limit 10 --tier 2

# Override use case
python scripts/step_8_001_evaluate.py --use-case editorial --limit 10
```

---

## 7 active enhancements (E1–E7)

| # | Name | What it does | Rebuild index? |
|---|------|-------------|---------------|
| E1 | Semantic cache | Recognises similar questions (cosine ≥ 0.92) — returns cached answers instantly | No |
| E2 | Cross-encoder re-ranking | Re-scores each (question, chunk) pair before the LLM — improves precision | No |
| E3 | spaCy chunking | Splits at sentence boundaries — prevents clauses from being cut mid-sentence | Yes |
| E4 | Named Entity Recognition | Extracts ORG, DATE, AMOUNT, LOC from each chunk — stored as metadata | Yes |
| E5 | Hierarchical summaries | Per-document summary indexed alongside chunks — used for comparative questions | Yes |
| E6 | Automatic evaluation | Scores each LLM answer: faithfulness, relevance, context precision | No |
| E7 | Conversational memory | Detects follow-up questions, rewrites as standalone queries before retrieval | No |

---

## Streamlit UI — 4 tabs

| Tab | Content |
|-----|---------|
| 💬 RAG | Chat interface — question + answer + sources + E7 rewrite notification + E1 cache badge + **🗑️ Clear** button |
| 📋 History | All queries filterable by use case and tier — full answer and source detail |
| 🔧 Debug | Checkpoint inspector (steps 1–3) + FAISS index stats |
| 📖 Definitions | Glossary: chunking, embeddings, FAISS, re-ranking, LLM tiers, E1/E2/E7 |

**To clear the visible chat:** click **🗑️ Clear** (top-right of the RAG tab). This wipes the chat display and resets E7 conversational memory.

**Sidebar controls:**
- LLM tier selector (Auto / Tier 1 / 2 / 3)
- Force re-generation toggle (bypasses cache)
- Cross-encoder re-rank toggle (E2)
- Conversational memory toggle + **Clear session memory** (clears chat + E7 memory)
- Database: clear cache / clear history

---

## SQLite cache

Queries and answers are cached in `data/rag_cache.db` when `database.enabled: true`.

```bash
# Inspect cache entries
sqlite3 data/rag_cache.db "SELECT question, tier, created_at FROM cache ORDER BY id DESC LIMIT 10;"

# Inspect query history
sqlite3 data/rag_cache.db "SELECT question, tier, from_cache, created_at FROM history ORDER BY id DESC LIMIT 10;"
```

Programmatic access:

```python
from src.utils.db_manager import DBManager
db = DBManager("data/rag_cache.db")

db.stats()          # {"cache_entries": N, "history_entries": M}
db.clear_cache()    # empty the cache table
db.clear_history()  # empty the history table
db.get_history(use_case="editorial", tier=2, limit=20)
```

---

## Conversational memory (E7)

Allows natural follow-up questions without repeating context.

**How it works:**
1. **Detection** — the system detects follow-ups by looking for short questions or pronouns (`it`, `they`, `this`, `that`, `same`, etc.).
2. **Rewrite** — the LLM rewrites the follow-up as a fully self-contained question before FAISS retrieval.
3. **Context injection** — the last N turns are prepended to the synthesis prompt.

**Example:**
```
Q1: What did we publish about AI regulation?
A1: The European Parliament approved landmark AI regulation…

Q2: And who wrote it?          ← detected as follow-up
      ↓ rewritten automatically to:
      "Who is the author of the article about AI regulation in Europe?"
A2: The article was written by Jean Martin.
```

**Configuration:**
```yaml
memory:
  enabled: true
  max_turns: 5
```

---

## Retrieval business rules

Defined in `config/retrieval_rules.yaml`. Active when `retrieval.enable_business_rules: true`.

The first matching rule overrides the default `k` and `score_threshold`, applies doc_type filters, and multiplies scores with boost factors.

```yaml
- id: "editorial_topic"
  when:
    query_contains_any: ["article", "published", "coverage", "wrote", "report"]
  filters:
    doc_type: ["editorial_article"]
  params:
    k: 10
    score_threshold: 0.15
  boost:
    metadata_field:
      recency: 1.3    # boost more recent articles
```

To add a rule: edit `config/retrieval_rules.yaml` — no code change required.

> **`filters.doc_type` must match reader-assigned values**, not chunking rule IDs.
> Readers set `doc_type` to the file extension: `"pdf"`, `"docx"`, `"tsv"`, `"xlsx"`, `"txt"`, or `"editorial_article"` (JSON CMS files only).
> A filter like `doc_type: ["rfp_public_tender"]` will silently return zero results because no reader ever assigns that value.
> Use `doc_type: ["pdf", "tsv", "xlsx"]` to restrict to RFP file types, or omit the filter entirely.

---

## Evaluation results

Step 8 saves JSON reports to `data/evaluations/<use_case>/eval_<timestamp>.json`:

```json
{
  "timestamp": "20260408T184743",
  "use_case": "editorial",
  "count": 5,
  "avg_faithfulness": 0.9,
  "avg_relevance": 1.0,
  "avg_context_precision": 0.9,
  "avg_overall": 0.933,
  "scores": [...]
}
```

**Metrics:**

| Metric | Meaning |
|--------|---------|
| **Faithfulness** | Every claim in the answer can be traced to the retrieved sources |
| **Relevance** | The answer directly addresses the question |
| **Context precision** | The retrieved passages contained what was needed to answer |

---

## Utility scripts

| Script | Purpose |
|--------|---------|
| `check_status.py` | Display corpus files, pipeline artefacts, index state, and cache stats |
| `validate_pipeline.py` | Check artefact coherence between each step (step 1 → 4) |
| `test_index.py` | FAISS index integrity: null vectors, count match, required metadata fields |
| `run_pipeline.py` | Orchestrate the full build (steps 1–4) and/or query from the command line |
| `reset_corpus.py` | Delete checkpoints and index for a use-case (keeps source docs and logs) |
| `merge_indexes.py` | Merge two FAISS indexes (same embedding model) into one |

### `check_status.py`

```bash
python check_status.py
python check_status.py --use-case editorial
```

Shows corpus files, chunk estimate, step 1–3 checkpoint sizes, FAISS index stats, embedding/LLM config, and SQLite cache counts.

### `validate_pipeline.py`

```bash
python validate_pipeline.py
python validate_pipeline.py --use-case editorial
```

Verifies end-to-end artefact coherence: corpus → step_1 → step_2 → step_3 → step_4. Exits with a non-zero code if any check fails.

### `test_index.py`

```bash
python test_index.py
python test_index.py --use-case editorial
```

Checks that `index.faiss` loads, vector count matches `chunks.json`, no null vectors in a random sample, and required metadata fields are present.

### `run_pipeline.py`

```bash
# Build index (steps 1 → 4)
python run_pipeline.py --build

# Build for a specific use-case
python run_pipeline.py --build --use-case editorial

# Dry-run (show what would run without executing)
python run_pipeline.py --build --dry-run

# Query an existing index
python run_pipeline.py --query "What did we publish about climate?"

# Force a specific LLM tier
python run_pipeline.py --query "..." --tier 2

# Build + query in one call
python run_pipeline.py --build --query "What did we publish about climate?"
```

### `reset_corpus.py`

```bash
# Reset active use_case (prompts for confirmation)
python reset_corpus.py

# Reset a specific use-case
python reset_corpus.py --use-case editorial

# Skip confirmation prompt
python reset_corpus.py --yes

# Show what would be deleted without deleting
python reset_corpus.py --dry-run
```

Deletes: `step_1_documents.json`, `step_2_chunks.json`, `step_3_embeddings.npy`, `step_3_chunk_ids.json`, `index.faiss`, `chunks.json`.
Preserves: source corpus files in `data/corpora/`, `logs/`, SQLite cache.

**Full clean-slate reset** (all use cases, all artefacts, all logs):

```bash
rm -rf data/checkpoints data/indexes data/evaluations logs data/rag_cache.db
```

This wipes every generated file. Source corpus files in `data/corpora/` and `.env` are preserved.
After this, re-run `python run_pipeline.py --build` to rebuild from scratch.

### `merge_indexes.py`

```bash
python merge_indexes.py \
    --a data/indexes/editorial/CMS_EXPORT_2026_Q1 \
    --b data/indexes/editorial/CMS_EXPORT_2026_Q2 \
    --out data/indexes/editorial/CMS_EXPORT_2026_merged
```

Both indexes must have the same embedding model (same vector dimension). The merged index is an `IndexFlatIP`. Update `workflow_paths.yaml` to point to the merged index after merging.

---

## WordPress bridge

Exports the processed CMS corpus into a WordPress installation via a custom plugin, enabling semantic search inside WP without any live API dependency during development.

### Data flow

```
data/corpora/editorial/CMS_EXPORT_2026/sample_posts.json   (74 posts, WP REST API format)
        │
        ▼  bridge_export.py
data/bridge/rag_bridge.json                                 (normalised: id, title, url, date, slug, excerpt, text)
        │
        ▼  WP plugin admin → Import
wp_rag_posts  (MySQL table in WordPress)
        │
        ▼  [rag_search] shortcode
Semantic search results page (Standard ↔ Semantic toggle)
```

### Step 1 — Generate the exchange file

```bash
conda activate ia_achats

# Default — reads the path set in config/bridge_wp.yaml (bridge.local_source)
python bridge_export.py

# Override source file without editing the config (e.g. a new corpus export)
python bridge_export.py \
  --source data/corpora/editorial/CMS_EXPORT_2026_2/flaven_posts_full_20260410_150759.json

# Override both source and output path
python bridge_export.py \
  --source data/corpora/editorial/CMS_EXPORT_2026_2/flaven_posts_full_20260410_150759.json \
  --out data/bridge/rag_bridge.json
```

| Flag | Default | Purpose |
|------|---------|---------|
| `--source` | `bridge.local_source` from `bridge_wp.yaml` | Path to the input JSON file (WP REST API format) |
| `--out` | `bridge.exchange_file` from `bridge_wp.yaml` | Path for the output `rag_bridge.json` |
| `--config` | `config/bridge_wp.yaml` | Path to the bridge config file |

`wordpress.enabled: false` in `config/bridge_wp.yaml` — reads from local file only.
To fetch live from the WP REST API: set `enabled: true` and fill in `api_url`.

**Tip:** if you always use a new corpus directory, update `bridge.local_source` in `config/bridge_wp.yaml` once so `python bridge_export.py` works with no flags.

### Step 2 — Install the plugin

```
cp -r rag-semantic-search/  /path/to/wordpress/wp-content/plugins/
```

Or zip the `rag-semantic-search/` folder and upload via WP Admin → Plugins → Add New → Upload Plugin.

Activate the plugin. Two tables are created automatically:

| Table | Purpose |
|---|---|
| `wp_rag_posts` | One row per imported article |
| `wp_rag_results` | One row per (query, ranked result) pair — TTL-managed |

### Step 3 — Import posts

WP Admin → **RAG Search** → upload `data/bridge/rag_bridge.json` → click **Import posts**.

- 74 posts inserted on first import.
- Re-importing the same file is safe — existing rows are updated (`ON DUPLICATE KEY UPDATE`).
- Use **Empty tables** (Danger zone) to wipe and re-import from scratch.

### Step 4 — Add the search page

Create a WordPress page (e.g. "Semantic Search"), add the shortcode to its content:

```
[rag_search]
[rag_search limit="5"]
[rag_search query="climate policy"]
```

The page renders a search form with two modes:

| Mode | Behaviour |
|---|---|
| **Standard search** | Redirects to `/?s=query` (native WP search) |
| **Semantic search** | Queries `wp_rag_posts` via MySQL FULLTEXT, renders scored result cards |

### Plugin file layout

```
rag-semantic-search/
├── rag-semantic-search.php         ← plugin header, hooks, shortcode, redirect
├── uninstall.php                   ← drops both tables on plugin delete
├── includes/
│   ├── class-db.php                ← create / drop / empty / counts / TTL purge
│   ├── class-importer.php          ← JSON parse + upsert into wp_rag_posts
│   └── class-search.php            ← FULLTEXT search + LIKE fallback + snippet
├── admin/
│   ├── admin-page.php              ← import form, empty-tables button, row counts
│   └── admin.css
├── templates/
│   └── semantic-search-results.php ← shortcode output: form + toggle + result cards
└── public/
    └── search.css                  ← front-end card styles, score bar, responsive
```

### Exchange format (Option B — no tags/categories)

| Field | Source | Type | Notes |
|---|---|---|---|
| `id` | `id` | integer | WP post ID, primary key |
| `title` | `title.rendered` | string | HTML stripped |
| `url` | `link` | string | Canonical post URL |
| `date` | `date` | string | `YYYY-MM-DD` |
| `slug` | `slug` | string | Plain string |
| `excerpt` | `excerpt.rendered` | string | HTML stripped, may be empty |
| `text` | `content.rendered` | string | Full body, HTML stripped |

Full spec: `data/bridge/rag_bridge_schema.json`. SQL schema: `data/bridge/rag_schema.sql`.

---

## Absolute rules

1. Do not change the public interface of any step script without updating all dependent steps.
2. Every step must be runnable standalone.
3. Default embeddings: **local Ollama**. Azure embeddings only if explicitly set in `config.yaml`.
4. LLM switching (Ollama ↔ Azure) is controlled by `config.yaml` only — never by code.
5. Single path entry point: `config/workflow_paths.yaml`.
6. Single config entry point: `config/config.yaml`.
7. All 5 levers are controlled **only via YAML** — no hard-coding.
8. Business rules for chunking and retrieval are **opt-in** (`enable_business_rules: true/false`).
