"""
Cross-encoder reranker (E2).
Loaded once per process and reused across queries.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

_instance: Optional["Reranker"] = None


class Reranker:
    """
    Wraps sentence-transformers CrossEncoder for (query, passage) re-scoring.
    Higher score = more relevant.
    """

    def __init__(self, model_name: str):
        from sentence_transformers import CrossEncoder
        logger.info("Loading cross-encoder: %s", model_name)
        self._model = CrossEncoder(model_name)
        self.model_name = model_name

    def rerank(self, query: str, results: list) -> list:
        """
        Re-score and re-sort results in-place.
        `results` is a list of SearchResult (or any object with .text and .score).
        Returns the same list sorted by cross-encoder score descending.
        """
        if not results:
            return results

        pairs = [(query, r.text) for r in results]
        scores = self._model.predict(pairs)

        for result, score in zip(results, scores):
            result.score = float(score)

        results.sort(key=lambda r: r.score, reverse=True)
        return results


def get_reranker(model_name: str) -> "Reranker":
    """Return a cached Reranker instance (singleton per process)."""
    global _instance
    if _instance is None or _instance.model_name != model_name:
        _instance = Reranker(model_name)
    return _instance
