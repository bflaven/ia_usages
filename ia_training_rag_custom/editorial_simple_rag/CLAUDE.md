# OpenWolf

@.wolf/OPENWOLF.md

This project uses OpenWolf for context management. Read and follow .wolf/OPENWOLF.md every session. Check .wolf/cerebrum.md before generating code. Check .wolf/anatomy.md before reading files.


# CLAUDE.md — Technical and Operational Specification for the RAG Project

**Last updated:** April 8, 2026
**Author:** Bruno Flaven

A modular RAG (Retrieval-Augmented Generation) system that lets users query a document corpus in natural language and get sourced answers in seconds.

Key capabilities:
- Strict cost control (3 LLM tiers)
- SQLite cache with semantic matching
- Configurable embedding and LLM providers (Ollama ↔ Azure)
- 5 tunable levers, all driven by YAML (no hard-coding)
- 7 active enhancements (E1–E7)
- Multiple use cases: RFP, HR, screenwriting, journalism, support, **editorial (CMS posts)**

---

## 1. What this system does

A user types a question in natural language. The system:

1. Searches all documents in the active corpus and identifies the most relevant passages.
2. Optionally re-ranks those passages with a cross-encoder model.
3. Passes the best passages to an LLM which writes a structured answer.
4. Returns the answer with exact source references (file, page, relevance score).

The LLM never reads the full documents — it only sees the passages the system selected. This makes the system fast, cost-effective, and auditable.

---

## 2. Use cases

The system is use-case agnostic. Switch the active corpus and the YAML business rules to move between domains.

| Use case | Example corpus | Example question |
|---|---|---|
| **RFP** | Tender submissions (PDF, DOCX, TSV) | "What is the total 4-year cost for each bidder?" |
| **HR** | Job applications, CVs, job descriptions | "Which candidates have more than 5 years of Python experience?" |
| **Screenwriting** | Scripts, treatments, series bibles | "In which episode does the protagonist first mention the artifact?" |
| **Journalism** | Archive articles, press releases | "What did we report on the ceasefire negotiations in March 2025?" |
| **Support** | Technical documentation, manuals, FAQs | "What is the recommended restart procedure for module B?" |
| **Editorial (CMS)** | JSON export of CMS posts | "What articles did we publish about climate policy in Q1 2026?" |

Each use case has its own corpus directory and can have its own chunking and retrieval rules (see section 5).

---

## 3. Project structure

```text
.
├── CLAUDE_v7.md
├── check_status.py
├── config/
│   ├── config.yaml              ← single config entry point
│   ├── workflow_paths.yaml      ← single path entry point
│   ├── chunking_rules.yaml      ← business rules for lever 2
│   ├── retrieval_rules.yaml     ← business rules for lever 3
│   └── vocabularies/
├── data/
│   ├── corpora/
│   │   ├── rfp/AO_2025_003/
│   │   ├── hr/BATCH_2026_01/
│   │   ├── editorial/CMS_EXPORT_2026/
│   │   └── ...
│   ├── indexes/
│   │   └── <use_case>/<corpus_id>/
│   └── rag_cache.db
├── logs/
├── scripts/
│   ├── step_1_001_ingest.py
│   ├── step_2_001_parse.py
│   ├── step_2b_001_summarize.py
│   ├── step_3_001_embed.py
│   ├── step_4_001_index.py
│   ├── step_5_001_query.py
│   ├── step_6_001_synthesize.py
│   ├── step_7_001_interface.py
│   └── step_8_001_evaluate.py
├── src/
│   ├── ingestion/readers.py
│   ├── llm/
│   │   ├── embeddings.py
│   │   ├── llm_client.py
│   │   ├── reranker.py
│   │   └── summarizer.py
│   ├── memory/conversation.py
│   ├── parsing/chunker.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── db_manager.py
│   │   └── checkpoint.py
│   └── vector_store/faiss_store.py
├── run_pipeline.py
├── validate_pipeline.py
├── reset_corpus.py
├── test_index.py
└── merge_indexes.py
```

Each corpus is isolated: its own `corpora/`, `indexes/`, and checkpoints.

---

## 4. Central config (`config/config.yaml`) — 5 levers

### 4.1. Full config example

```yaml
active_use_case: "rfp"   # rfp | hr | screenwriting | journalism | support | editorial

embeddings:
  provider: "ollama"               # "ollama" | "azure"
  model: "nomic-embed-text"        # local default, dim 768
  azure_deployment: null           # "text-embedding-3-large" if provider="azure"

chunking:
  size: 512
  overlap: 0.1
  min_tokens: 50
  strip_headers: true
  enable_business_rules: true      # uses chunking_rules.yaml if true

retrieval:
  k: 5
  score_threshold: 0.2
  rerank:
    enabled: true
    model: "cross-encoder/ms-marco-MiniLM-L-6-v2"
  enable_business_rules: true      # uses retrieval_rules.yaml if true

llm:
  provider: "ollama"               # "ollama" | "azure"
  model: "llama3.1"
  azure_deployment: "gpt-4.1"

memory:
  enabled: true
  max_turns: 5                     # how many prior turns to keep in context

azure:
  endpoint: "https://<endpoint>.openai.azure.com"
  api_key_env: "AZURE_OPENAI_API_KEY"
  api_version: "2024-02-15-preview"

ollama:
  host: "http://localhost:11434"

database:
  enabled: true
  path: "data/rag_cache.db"
  cleanup:
    enabled: true
    days: 30
```

### 4.2. The 5 levers

| # | Lever | Controlled by | Effect |
|---|---|---|---|
| L1 | Embedding model | `embeddings` in config.yaml | Quality of semantic search |
| L2 | Chunking (size, overlap, spaCy) | `chunking` + `chunking_rules.yaml` | What gets indexed |
| L3 | Retrieval rules and file-type boost | `retrieval` + `retrieval_rules.yaml` | Which passages surface |
| L4 | LLM tier (Tier 1 / 2 / 3) | `llm` in config.yaml | Cost vs. quality trade-off |
| L5 | SQLite cache strategy | `database` in config.yaml | Response time and cost |

All 5 levers are changed in YAML only — no code edits required.

---

## 5. Business rules (YAML) for levers 2 and 3

### 5.1. `config/chunking_rules.yaml`

Applies per-document chunking parameters based on filename, path, or extension.

```yaml
# config/chunking_rules.yaml

defaults:
  size: 512
  overlap: 0.1
  min_tokens: 50
  strip_headers: true

document_types:

  - id: "rfp_public_tender"
    match:
      any_filename_contains: ["AO_", "MARCHE", "DCE"]
      any_extension: ["pdf", "docx"]
    chunking:
      size: 600
      overlap: 0.15
    keep_together_patterns:
      - regex: "^Article\\s+[0-9IVX]+"
      - regex: "^Object of the contract"
    drop_patterns:
      - regex: "^Page \\d+ / \\d+"

  - id: "hr_cv"
    match:
      any_path_contains: ["hr", "cv", "candidates"]
    chunking:
      size: 300
      overlap: 0.1
    keep_together_patterns:
      - regex: "^Experience"
      - regex: "^Education"
    drop_patterns: []

  - id: "editorial_article"
    match:
      any_extension: ["json"]
      any_path_contains: ["editorial", "cms"]
    chunking:
      size: 800
      overlap: 0.05
    keep_together_patterns: []
    drop_patterns:
      - regex: "^\\s*$"   # skip empty lines
```

**Logic:**
- `enable_business_rules: false` → ignore this file, use only `config.yaml` chunking values.
- `enable_business_rules: true` → `step_2_001_parse.py` detects document type via `match`, applies its specific `chunking`, merges paragraphs via `keep_together_patterns`, drops lines via `drop_patterns`.

### 5.2. `config/retrieval_rules.yaml`

Adjusts search parameters and boosts based on what the user asked.

```yaml
# config/retrieval_rules.yaml

rules:

  - id: "rfp_pricing"
    when:
      query_contains_any: ["cost", "price", "budget", "BPU", "amount", "total"]
    filters:
      doc_type: ["rfp_public_tender"]
    params:
      k: 8
      score_threshold: 0.15
    boost:
      source_extension:
        tsv: 2.5    # divide L2 score by 2.5 → raises ranking
        xlsx: 2.0

  - id: "hr_screening"
    when:
      query_contains_any: ["experience", "skills", "candidate", "years of"]
    filters:
      doc_type: ["hr_cv"]
    params:
      k: 6
      score_threshold: 0.2

  - id: "editorial_topic"
    when:
      query_contains_any: ["article", "published", "coverage", "wrote about"]
    filters:
      doc_type: ["editorial_article"]
    params:
      k: 10
      score_threshold: 0.18
    boost:
      metadata_field:
        recency: 1.3   # boost more recent posts

defaults:
  k: 5
  score_threshold: 0.2
```

**Logic:**
- `enable_business_rules: false` → use only global `k` and `score_threshold` from `config.yaml`.
- `enable_business_rules: true` → `step_5_001_query.py` selects the first matching rule, applies its filters, params, and boosts.

---

## 6. Pipeline overview

### Step 1 — Ingest (`step_1_001_ingest.py`)

Reads all supported formats, runs basic cleaning, language detection, and optional anonymization.

**Supported formats:** PDF, DOCX, TXT, XLSX, TSV, JSON (including CMS exports — see section 9).

### Step 2 — Parse and chunk (`step_2_001_parse.py`)

1. Loads the spaCy model (`fr_dep_news_trf` for French, or multilingual `xx_sent_ud_sm`).
2. Splits the text into sentences using `doc.sents`.
3. Groups sentences into chunks up to `chunking.size` tokens.
4. If `enable_business_rules: true`, applies `chunking_rules.yaml` per document type.
5. Each chunk carries metadata: source file, page, language, doc type, tags.

spaCy guarantees clean sentence boundaries. The YAML rules control how sentences are grouped into business-relevant chunks.

### Step 2b — Summarize (`step_2b_001_summarize.py`)

For each document, generates a summary via the LLM. Summaries are indexed alongside fine-grained chunks. The system uses summaries for broad/comparative questions (E5) and chunks for precise questions.

### Step 3 — Embed (`step_3_001_embed.py`)

Vectorizes all chunks using the `EmbeddingClient` configured in `config.yaml`.

Default: `nomic-embed-text` via Ollama (768 dimensions, local, no data leaves the network).

### Step 4 — Index (`step_4_001_index.py`)

Builds a FAISS index per corpus. One index per corpus in `data/indexes/<use_case>/<corpus_id>/`.

### Step 5 — Query (`step_5_001_query.py`)

1. Embeds the user question.
2. If `memory.enabled: true` and a follow-up is detected, rewrites the question first (E7).
3. If `enable_business_rules: true`, selects the matching retrieval rule.
4. Queries the FAISS index, applies filters and boosts.
5. If `rerank.enabled: true`, passes results through the cross-encoder (E2).
6. Returns the top-k chunks with scores.

### Step 6 — Synthesize (`step_6_001_synthesize.py`)

Builds the prompt (question + retrieved chunks) and calls the LLM. Returns the answer text plus source references (file, page, score).

### Step 7 — Interface (`step_7_001_interface.py`)

CLI mode (default) or Streamlit web UI (`--streamlit` flag).

### Step 8 — Evaluate (`step_8_001_evaluate.py`)

Scores pending LLM responses on 3 metrics (E6):
- **Faithfulness** — is the answer grounded in the retrieved sources?
- **Relevance** — does it answer the question?
- **Context precision** — were the right passages retrieved?

---

## 7. The 7 enhancements (E1–E7)

All 7 are active in the current version. None require a code change — they are toggled in `config.yaml`.

| # | Name | What it does | Rebuild index? |
|---|---|---|---|
| E1 | Semantic cache | Recognizes similar questions (not just identical ones) — returns cached answers instantly | No |
| E2 | Cross-encoder re-ranking | Re-scores each (question, chunk) pair before passing to the LLM — improves precision | No |
| E3 | spaCy chunking | Splits documents at sentence boundaries — prevents clauses from being cut in half | Yes |
| E4 | Named Entity Recognition | Extracts organizations, dates, amounts, locations from each chunk — stored as metadata | Yes |
| E5 | Hierarchical summaries | Generates a per-document summary at indexing time — used for comparative questions | Yes |
| E6 | Automatic evaluation | Scores each LLM answer on faithfulness, relevance, context precision | No |
| E7 | Conversational memory | Detects follow-up questions, rewrites them as standalone queries before searching | No |

---

## 8. LLM tiers — cost and privacy

| Tier | Mode | Cost | Data stays local? |
|---|---|---|---|
| Tier 1 | Static template response | Free | Yes |
| Tier 2 | Local LLM via Ollama (`llama3.1`) | ~Free | Yes |
| Tier 3 | Azure OpenAI (`gpt-4.1`) | Per token | No — sent to cloud |

**Default:** Tier 2 (local). Tier 3 is opt-in only — set it explicitly in config or in the Streamlit sidebar.

For sensitive corpora (RFP, HR, contracts), Tier 2 is the recommended mode.

---

## 9. Editorial use case — CMS JSON corpus

### 9.1. What it is

The editorial use case lets journalists, editors, or content teams query their published article archive using natural language. The source is a JSON file exported from a CMS (WordPress, Strapi, Contentful, custom API).

Example questions:
- "What did we publish about climate policy in Q1 2026?"
- "Which authors covered the elections in West Africa?"
- "Summarize our editorial angle on AI regulation over the past year."
- "Find all articles tagged 'economy' published between January and March 2026."

### 9.2. Expected JSON format

The ingestion reader expects a JSON array of post objects. Minimum required fields:

```json
[
  {
    "id": "post-001",
    "title": "Climate Summit Ends Without Agreement",
    "content": "Full article text here...",
    "author": "Marie Dupont",
    "published_at": "2026-03-15T10:30:00Z",
    "tags": ["climate", "environment", "COP"],
    "categories": ["World", "Science"],
    "url": "https://cms.example.com/articles/post-001",
    "language": "en"
  }
]
```

Optional but useful fields: `summary`, `excerpt`, `status` (published/draft), `section`.

### 9.3. Ingestion (`step_1_001_ingest.py`)

The JSON reader (`src/ingestion/readers.py`) handles CMS exports:

```python
def read_json_cms(file_path: str) -> list[dict]:
    """
    Read a CMS JSON export (array of post objects).
    Each post becomes a document with its metadata preserved.
    Returns list of dicts: {text, source, metadata}.
    """
    with open(file_path) as f:
        posts = json.load(f)
    documents = []
    for post in posts:
        documents.append({
            "text": post.get("content", ""),
            "source": post.get("url", post["id"]),
            "metadata": {
                "doc_type": "editorial_article",
                "title": post.get("title", ""),
                "author": post.get("author", ""),
                "published_at": post.get("published_at", ""),
                "tags": post.get("tags", []),
                "categories": post.get("categories", []),
                "language": post.get("language", "en"),
            }
        })
    return documents
```

The title, author, date, tags, and categories travel as metadata through the full pipeline and appear in source references alongside every answer.

### 9.4. Chunking for articles

Articles are usually shorter and more self-contained than legal documents. Recommended settings in `chunking_rules.yaml`:

```yaml
- id: "editorial_article"
  match:
    any_extension: ["json"]
    any_path_contains: ["editorial", "cms"]
  chunking:
    size: 800          # keep more context per chunk
    overlap: 0.05      # minimal overlap — articles don't repeat themselves
  keep_together_patterns:
    - regex: "^##\\s"  # keep markdown section headings with their paragraph
  drop_patterns:
    - regex: "^\\s*$"
```

For very long investigative pieces, the system will produce multiple chunks. For short news items (under 300 tokens), the entire article becomes one chunk.

### 9.5. Retrieval rules for editorial queries

```yaml
- id: "editorial_topic"
  when:
    query_contains_any: ["article", "published", "coverage", "wrote", "report", "journalist"]
  filters:
    doc_type: ["editorial_article"]
  params:
    k: 10
    score_threshold: 0.15
  boost:
    metadata_field:
      recency: 1.3   # slightly boost more recent articles
```

The `tags` and `categories` metadata fields can be used to filter at query time when the user specifies them explicitly (e.g., "articles tagged 'economy'").

### 9.6. Placing the corpus

```
data/corpora/editorial/CMS_EXPORT_2026/
  posts_2026_q1.json
  posts_2026_q2.json
```

Set `active_use_case: "editorial"` in `config.yaml` and `workflow_paths.yaml` to point to this directory.

---

## 10. Absolute rules

1. Do not change the public interface of `run_pipeline.py` without updating all steps.
2. Every step must be runnable standalone.
3. Default embeddings: **local Ollama**. Azure embeddings only if enabled in `config.yaml`.
4. LLM switching (Ollama ↔ Azure) is controlled by tiers and `config.yaml` only.
5. Single path entry point: `workflow_paths.yaml`.
6. Single config entry point: `config/config.yaml`.
7. All 5 levers are controlled **only via YAML** — never hard-coded.
8. Business rules for chunking and retrieval are **opt-in** (`enable_business_rules: true/false`).

---

## 11. Key utility scripts

| Script | Purpose |
|---|---|
| `run_pipeline.py` | Run the pipeline step by step |
| `check_status.py` | Verify config (Azure API key, Ollama models, paths) |
| `validate_pipeline.py` | Check data consistency between steps |
| `reset_corpus.py` | Reset a corpus without deleting logs |
| `test_index.py` | Check index integrity (detect null vectors) |
| `merge_indexes.py` | Merge two indexes into one |

---

## 12. Streamlit interface — 5 tabs

| Tab | Purpose |
|---|---|
| **RAG** | Free-text questions, answers with sourced references, NER entities visible (E4), rewrite notification for follow-ups (E7) |
| **Evaluation** | Score pending LLM answers — faithfulness, relevance, context precision (E6) |
| **History** | All queries, filterable by use case, LLM tier, date. Purge cache or history. |
| **Debug** | Checkpoint summary per corpus. JSON inspection of each step. |
| **Definitions** | Glossary: chunking, embeddings, FAISS, re-ranking, LLM tiers, cache. |

**Sidebar controls:**
- LLM tier selector (Auto / Tier 1 / 2 / 3)
- Force re-generation (bypasses cache)
- Conversational memory toggle + session clear (E7)
- Database controls: clear cache / clear history / reset all

---

## 13. Quick start

```bash
# 1. Activate environment and start Ollama
conda activate ia_achats
ollama serve   # in a dedicated terminal

# 2. Check system state
python check_status.py

# 3. Build the index
python run_pipeline.py --build

# 4. Validate
python validate_pipeline.py
python test_index.py

# 5a. Launch CLI
python scripts/step_7_001_interface.py

# 5b. Launch Streamlit
streamlit run scripts/step_7_001_interface.py -- --streamlit
```

CLI commands: ask questions freely. Type `clear` to reset conversational memory, `exit` to quit.

---

## 14. Decisions to document in `DECISIONS.md`

- Using or not using business rules (`enable_business_rules`) and their impact on quality.
- FAISS vs. Chroma — choice and rationale.
- Embedding model selection (local vs. cloud, dimension, multilingual support).
- LLM model selection per use case.
- spaCy model selection (transformer vs. smaller models — speed/quality trade-off).
- Cross-encoder model selection for re-ranking (E2).
- When to use hierarchical summaries vs. fine-grained chunks (E5).

