"""
Step 7 — Interface
------------------
CLI mode (default) or Streamlit web UI (--streamlit flag).

CLI:
    python scripts/step_7_001_interface.py
    python scripts/step_7_001_interface.py --use-case editorial

Streamlit:
    streamlit run scripts/step_7_001_interface.py -- --streamlit
"""

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.llm.embeddings import EmbeddingClient
from src.llm.llm_client import LLMClient
from src.memory.conversation import ConversationMemory
from src.utils.config import load_config, get_index_dir, get_logs_dir
from src.utils.db_manager import DBManager
from src.vector_store.faiss_store import FAISSStore

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_RETRIEVAL_RULES_PATH = _PROJECT_ROOT / "config" / "retrieval_rules.yaml"

sys.path.insert(0, str(_PROJECT_ROOT))
from scripts.step_5_001_query import run_query, _load_retrieval_rules
from scripts.step_6_001_synthesize import synthesize, Answer


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logging(logs_dir: Path) -> None:
    logs_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / "step_7_interface.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step7")


# ---------------------------------------------------------------------------
# Shared pipeline runner (used by both CLI and Streamlit)
# ---------------------------------------------------------------------------

def ask(
    question: str,
    config: dict,
    store: FAISSStore,
    embedding_client: EmbeddingClient,
    llm_client: LLMClient,
    db: DBManager,
    memory: ConversationMemory,
    retrieval_rules: dict | None,
    tier: int | None,
    force_regen: bool,
    rerank: bool,
    use_case: str,
) -> Answer:
    """Full pipeline: cache → E7 rewrite → retrieve → synthesize → cache save."""

    # --- E1: semantic cache lookup ---
    query_embedding = embedding_client.embed_one(question)
    if not force_regen and config.get("database", {}).get("enabled"):
        cached = db.find_cached(query_embedding, use_case)
        if cached:
            answer = Answer(
                question=question,
                text=cached["answer"],
                tier=cached["tier"],
                sources=cached["sources"],
                from_cache=True,
            )
            db.save_history(question, answer.text, answer.sources, use_case, answer.tier, from_cache=True)
            return answer

    # --- E7: follow-up rewrite ---
    rewritten = None
    effective_question = question
    if config.get("memory", {}).get("enabled") and memory.is_followup(question):
        effective_question = memory.rewrite(question, llm_client)
        if effective_question != question:
            rewritten = effective_question
            logger.info("E7: question rewritten → '%s'", effective_question)

    # --- Step 5: retrieve ---
    results = run_query(
        effective_question,
        config,
        store,
        embedding_client,
        retrieval_rules=retrieval_rules,
        rerank=rerank,
    )

    # --- Step 6: synthesize ---
    answer = synthesize(effective_question, results, config, tier=tier)
    answer.question = question   # show original question to user

    # --- Persist ---
    if config.get("database", {}).get("enabled"):
        db.save_cache(question, query_embedding, answer.text, answer.sources, use_case, answer.tier)
        db.save_history(question, answer.text, answer.sources, use_case, answer.tier)

    # --- E7: store turn ---
    if config.get("memory", {}).get("enabled"):
        memory.add(question, answer.text, rewritten=rewritten)

    return answer


# ===========================================================================
# CLI
# ===========================================================================

def run_cli(config: dict, use_case: str) -> None:
    index_dir = get_index_dir()
    try:
        store = FAISSStore.load(index_dir)
    except FileNotFoundError as exc:
        logger.error("%s\nRun step_4_001_index.py first.", exc)
        sys.exit(1)

    embedding_client = EmbeddingClient.from_config(config)
    llm_client = LLMClient.from_config(config)
    memory = ConversationMemory(max_turns=config.get("memory", {}).get("max_turns", 5))

    db_cfg = config.get("database", {})
    db_path = _PROJECT_ROOT / db_cfg.get("path", "data/rag_cache.db")
    db = DBManager(db_path)

    retrieval_rules = None
    if config.get("retrieval", {}).get("enable_business_rules") and _RETRIEVAL_RULES_PATH.exists():
        retrieval_rules = _load_retrieval_rules(_RETRIEVAL_RULES_PATH)

    print(f"\nRAG CLI — use case: {use_case}  |  {store.size} chunks indexed")
    print("Commands: 'clear' = reset memory  |  'exit' = quit\n")

    while True:
        try:
            question = input("Q> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            print("Bye.")
            break
        if question.lower() == "clear":
            memory.clear()
            print("  [memory cleared]\n")
            continue

        answer = ask(
            question, config, store, embedding_client, llm_client,
            db, memory, retrieval_rules,
            tier=None, force_regen=False, rerank=True, use_case=use_case,
        )
        answer.print()


# ===========================================================================
# Streamlit UI
# ===========================================================================

def run_streamlit(config: dict, use_case: str) -> None:
    import streamlit as st

    st.set_page_config(
        page_title="RAG — Editorial",
        page_icon="📰",
        layout="wide",
    )

    # --- Cached resources (loaded once) ---
    @st.cache_resource
    def load_store():
        return FAISSStore.load(get_index_dir())

    @st.cache_resource
    def load_embedding_client():
        return EmbeddingClient.from_config(config)

    @st.cache_resource
    def load_llm_client():
        return LLMClient.from_config(config)

    @st.cache_resource
    def load_db():
        db_cfg = config.get("database", {})
        db_path = _PROJECT_ROOT / db_cfg.get("path", "data/rag_cache.db")
        return DBManager(db_path)

    @st.cache_resource
    def load_rules():
        if config.get("retrieval", {}).get("enable_business_rules") and _RETRIEVAL_RULES_PATH.exists():
            return _load_retrieval_rules(_RETRIEVAL_RULES_PATH)
        return None

    try:
        store = load_store()
    except FileNotFoundError:
        st.error("Index not found. Run `python scripts/step_4_001_index.py` first.")
        st.stop()

    embedding_client = load_embedding_client()
    llm_client = load_llm_client()
    db = load_db()
    retrieval_rules = load_rules()

    # --- Session state ---
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory(
            max_turns=config.get("memory", {}).get("max_turns", 5)
        )
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # -----------------------------------------------------------------------
    # Sidebar
    # -----------------------------------------------------------------------
    with st.sidebar:
        st.title("⚙️ Controls")

        tier_map = {"Auto": None, "Tier 1 — Static": 1, "Tier 2 — Ollama": 2, "Tier 3 — Azure": 3}
        tier_label = st.selectbox("LLM Tier", list(tier_map.keys()), index=0)
        selected_tier = tier_map[tier_label]

        force_regen = st.toggle("Force re-generation", value=False,
                                help="Bypass the semantic cache")
        rerank = st.toggle("Cross-encoder re-rank", value=True,
                           help="E2: re-score results with a cross-encoder")
        memory_on = st.toggle("Conversational memory (E7)", value=True)

        if st.button("Clear session memory"):
            st.session_state.memory.clear()
            st.session_state.chat_history = []
            st.success("Memory cleared.")

        st.divider()
        st.subheader("🗄️ Database")
        stats = db.stats()
        st.caption(f"Cache: {stats['cache_entries']} entries  |  History: {stats['history_entries']} entries")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear cache"):
                n = db.clear_cache()
                st.success(f"Removed {n} cache entries.")
        with col2:
            if st.button("Clear history"):
                n = db.clear_history()
                st.success(f"Removed {n} history entries.")

        st.divider()
        st.caption(f"Use case: **{use_case}**  |  Index: **{store.size}** chunks")

    # -----------------------------------------------------------------------
    # Tabs
    # -----------------------------------------------------------------------
    tab_rag, tab_history, tab_debug, tab_defs = st.tabs(
        ["💬 RAG", "📋 History", "🔧 Debug", "📖 Definitions"]
    )

    # ===== TAB 1: RAG =======================================================
    with tab_rag:
        col_title, col_clear = st.columns([8, 1])
        with col_title:
            st.header("Ask a question")
        with col_clear:
            st.write("")  # vertical alignment nudge
            if st.button("🗑️ Clear", help="Clear the chat and reset conversational memory"):
                st.session_state.chat_history = []
                st.session_state.memory.clear()
                st.rerun()

        # Replay chat history
        for entry in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(entry["question"])
            with st.chat_message("assistant"):
                st.markdown(entry["answer"])
                if entry.get("rewritten"):
                    st.caption(f"🔄 E7 rewrite: _{entry['rewritten']}_")
                if entry.get("from_cache"):
                    st.caption("⚡ From semantic cache (E1)")
                _render_sources(entry["sources"])

        question = st.chat_input("Type your question…")
        if question:
            with st.chat_message("user"):
                st.markdown(question)

            effective_memory = st.session_state.memory if memory_on else ConversationMemory(0)

            with st.chat_message("assistant"):
                with st.spinner("Searching…"):
                    answer = ask(
                        question, config, store, embedding_client, llm_client,
                        db, effective_memory, retrieval_rules,
                        tier=selected_tier,
                        force_regen=force_regen,
                        rerank=rerank,
                        use_case=use_case,
                    )

                st.markdown(answer.text)

                rewritten_q = None
                if memory_on and effective_memory.turns:
                    last = effective_memory.turns[-1]
                    rewritten_q = last.rewritten
                    if rewritten_q:
                        st.caption(f"🔄 E7 rewrite: _{rewritten_q}_")

                if answer.from_cache:
                    st.caption("⚡ From semantic cache (E1)")

                tier_labels = {1: "Tier 1 (static)", 2: "Tier 2 (Ollama)", 3: "Tier 3 (Azure)"}
                st.caption(f"🤖 {tier_labels.get(answer.tier, answer.tier)}")

                _render_sources(answer.sources)

            st.session_state.chat_history.append({
                "question": question,
                "answer": answer.text,
                "sources": answer.sources,
                "from_cache": answer.from_cache,
                "rewritten": rewritten_q,
            })

    # ===== TAB 2: HISTORY ===================================================
    with tab_history:
        st.header("Query history")

        col1, col2 = st.columns(2)
        with col1:
            filter_uc = st.selectbox("Use case", ["All"] + [use_case], index=0)
        with col2:
            filter_tier = st.selectbox("Tier", ["All", "1", "2", "3"], index=0)

        rows = db.get_history(
            use_case=None if filter_uc == "All" else filter_uc,
            tier=None if filter_tier == "All" else int(filter_tier),
            limit=50,
        )

        if not rows:
            st.info("No history yet.")
        else:
            for row in rows:
                with st.expander(f"[{row['created_at'][:16]}] {row['question'][:80]}"):
                    st.markdown(f"**Tier {row['tier']}**"
                                + (" · from cache" if row["from_cache"] else ""))
                    st.markdown(row["answer"])
                    _render_sources(row["sources"])

    # ===== TAB 3: DEBUG =====================================================
    with tab_debug:
        st.header("Debug — checkpoints")

        from src.utils.config import get_checkpoint_dir
        cp_dir = get_checkpoint_dir()

        checkpoints = {
            "step_1_documents.json": "Step 1 — Ingested documents",
            "step_2_chunks.json": "Step 2 — Parsed chunks",
            "step_3_embeddings.npy": "Step 3 — Embeddings (binary)",
            "step_3_chunk_ids.json": "Step 3 — Chunk IDs",
        }

        for filename, label in checkpoints.items():
            path = cp_dir / filename
            exists = path.exists()
            status = "✅" if exists else "❌"
            with st.expander(f"{status} {label} ({filename})"):
                if not exists:
                    st.warning("File not found.")
                    continue
                if filename.endswith(".npy"):
                    import numpy as np
                    arr = np.load(str(path))
                    st.code(f"shape={arr.shape}  dtype={arr.dtype}")
                else:
                    with open(path, encoding="utf-8") as f:
                        data = json.load(f)
                    st.json(data[:3] if isinstance(data, list) else data)

        st.subheader("FAISS index")
        index_dir = get_index_dir()
        faiss_path = index_dir / "index.faiss"
        st.write(f"Path: `{faiss_path}`")
        st.write(f"Exists: {'✅' if faiss_path.exists() else '❌'}")
        st.write(f"Vectors in store: **{store.size}**  |  Dim: **{store.dim}**")

    # ===== TAB 4: DEFINITIONS ===============================================
    with tab_defs:
        st.header("Glossary")
        defs = {
            "Chunking": (
                "Splitting documents into overlapping text passages (chunks). "
                "Chunk size and overlap are set in `config.yaml` or `chunking_rules.yaml`."
            ),
            "Embeddings": (
                "Numerical vector representations of text. Similar texts have similar vectors. "
                "Default model: `nomic-embed-text` via Ollama (768 dimensions)."
            ),
            "FAISS": (
                "Facebook AI Similarity Search — a library for fast nearest-neighbour search "
                "over dense vectors. This system uses `IndexFlatIP` (cosine similarity)."
            ),
            "Re-ranking (E2)": (
                "A cross-encoder model (`ms-marco-MiniLM-L-6-v2`) re-scores each "
                "(question, chunk) pair for higher precision before the LLM sees the results."
            ),
            "Semantic cache (E1)": (
                "Similar questions (cosine similarity ≥ 0.92) reuse a cached answer "
                "instead of calling the LLM again."
            ),
            "Conversational memory (E7)": (
                "The last N turns are stored. Follow-up questions (short or containing "
                "pronouns) are rewritten as standalone queries before retrieval."
            ),
            "LLM Tiers": (
                "**Tier 1** — static template (free, local).  \n"
                "**Tier 2** — local Ollama `llama3.1` (~free, local).  \n"
                "**Tier 3** — Azure OpenAI `gpt-4.1` (per-token cost, cloud)."
            ),
        }
        for term, explanation in defs.items():
            with st.expander(term):
                st.markdown(explanation)


# ---------------------------------------------------------------------------
# Source rendering helper
# ---------------------------------------------------------------------------

def _render_sources(sources: list) -> None:
    import streamlit as st
    if not sources:
        return
    with st.expander(f"Sources ({len(sources)})"):
        for s in sources:
            score = s.get("score")
            score_str = f"`{score:.4f}`" if isinstance(score, float) else ""
            title = s.get("title") or s.get("source", "")
            author = f" · {s['author']}" if s.get("author") else ""
            date = f" · {s['date'][:10]}" if s.get("date") else ""
            tags = (
                "  " + " ".join(f"`{t}`" for t in s.get("tags", []))
                if s.get("tags") else ""
            )
            st.markdown(f"**{title}**{author}{date}  {score_str}{tags}")


# ===========================================================================
# Entry point
# ===========================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 7 — Interface")
    parser.add_argument("--streamlit", action="store_true", help="Launch Streamlit UI")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    args = parser.parse_args()

    config = load_config()
    use_case = args.use_case or config["active_use_case"]

    if args.streamlit:
        run_streamlit(config, use_case)
    else:
        logs_dir = get_logs_dir()
        _setup_logging(logs_dir)
        logger.info("=== Step 7 — CLI Interface ===")
        run_cli(config, use_case)


if __name__ == "__main__":
    main()
