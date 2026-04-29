"""
SQLite cache and history manager (E1 semantic cache, E5 history).

Schema:
    cache   — question embeddings + answers for semantic deduplication (E1)
    history — all Q&A pairs for the History tab
"""

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS cache (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    use_case    TEXT    NOT NULL,
    question    TEXT    NOT NULL,
    embedding   BLOB    NOT NULL,   -- float32 numpy array, serialised
    answer      TEXT    NOT NULL,
    sources     TEXT    NOT NULL,   -- JSON
    tier        INTEGER NOT NULL,
    created_at  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    use_case    TEXT    NOT NULL,
    question    TEXT    NOT NULL,
    answer      TEXT    NOT NULL,
    sources     TEXT    NOT NULL,   -- JSON
    tier        INTEGER NOT NULL,
    from_cache  INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL
);
"""

_CLEANUP_SQL = """
DELETE FROM cache   WHERE created_at < datetime('now', '-{days} days');
DELETE FROM history WHERE created_at < datetime('now', '-{days} days');
"""


class DBManager:

    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._path = str(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    # ------------------------------------------------------------------
    # Cache (E1 — semantic)
    # ------------------------------------------------------------------

    def find_cached(
        self,
        embedding: np.ndarray,
        use_case: str,
        similarity_threshold: float = 0.92,
    ) -> Optional[dict]:
        """
        Return a cached answer if a semantically similar question exists.
        Cosine similarity >= similarity_threshold → cache hit.
        """
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM cache WHERE use_case = ?", (use_case,)
            ).fetchall()

        if not rows:
            return None

        query_norm = embedding / (np.linalg.norm(embedding) + 1e-9)

        best_score = -1.0
        best_row = None
        for row in rows:
            stored = np.frombuffer(row["embedding"], dtype=np.float32)
            stored_norm = stored / (np.linalg.norm(stored) + 1e-9)
            score = float(np.dot(query_norm, stored_norm))
            if score > best_score:
                best_score = score
                best_row = row

        if best_score >= similarity_threshold:
            logger.info(
                "Cache hit (similarity=%.4f): '%s'", best_score, best_row["question"]
            )
            return {
                "question": best_row["question"],
                "answer": best_row["answer"],
                "sources": json.loads(best_row["sources"]),
                "tier": best_row["tier"],
                "from_cache": True,
            }

        return None

    def save_cache(
        self,
        question: str,
        embedding: np.ndarray,
        answer: str,
        sources: list,
        use_case: str,
        tier: int,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO cache (use_case, question, embedding, answer, sources, tier, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    use_case,
                    question,
                    embedding.astype(np.float32).tobytes(),
                    answer,
                    json.dumps(sources, ensure_ascii=False),
                    tier,
                    now,
                ),
            )

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def save_history(
        self,
        question: str,
        answer: str,
        sources: list,
        use_case: str,
        tier: int,
        from_cache: bool = False,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO history (use_case, question, answer, sources, tier, from_cache, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    use_case,
                    question,
                    answer,
                    json.dumps(sources, ensure_ascii=False),
                    tier,
                    int(from_cache),
                    now,
                ),
            )

    def get_history(
        self,
        use_case: Optional[str] = None,
        tier: Optional[int] = None,
        limit: int = 100,
    ) -> list[dict]:
        query = "SELECT * FROM history"
        params: list = []
        conditions = []
        if use_case:
            conditions.append("use_case = ?")
            params.append(use_case)
        if tier is not None:
            conditions.append("tier = ?")
            params.append(tier)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            {
                "id": r["id"],
                "use_case": r["use_case"],
                "question": r["question"],
                "answer": r["answer"],
                "sources": json.loads(r["sources"]),
                "tier": r["tier"],
                "from_cache": bool(r["from_cache"]),
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear_cache(self) -> int:
        with self._connect() as conn:
            n = conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
            conn.execute("DELETE FROM cache")
        logger.info("Cache cleared (%d entries removed)", n)
        return n

    def clear_history(self) -> int:
        with self._connect() as conn:
            n = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
            conn.execute("DELETE FROM history")
        logger.info("History cleared (%d entries removed)", n)
        return n

    def cleanup_old(self, days: int) -> None:
        with self._connect() as conn:
            conn.executescript(_CLEANUP_SQL.format(days=days))
        logger.info("Cleaned up entries older than %d days", days)

    def stats(self) -> dict:
        with self._connect() as conn:
            cache_count = conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
            history_count = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
        return {"cache_entries": cache_count, "history_entries": history_count}
