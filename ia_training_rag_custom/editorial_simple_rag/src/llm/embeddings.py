"""
EmbeddingClient — wraps Ollama and Azure OpenAI embedding providers.
Provider is selected from config.yaml (embeddings.provider).
"""

import logging
import time
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

_BATCH_SIZE = 32          # chunks per Ollama call
_RETRY_ATTEMPTS = 3
_RETRY_DELAY = 2.0        # seconds between retries
# Python-side safety cap before sending text to Ollama.
# The primary guard is truncate=True on the /api/embed endpoint.
# This cap is the last-resort pre-filter: if something unexpectedly large
# reaches here, clip it before it hits the network.
# 1500 chars ≈ 375 BPE tokens — safe for any realistic Ollama context window.
_MAX_EMBED_CHARS = 1500


def _safe_truncate(text: str) -> str:
    if len(text) > _MAX_EMBED_CHARS:
        logger.warning(
            "Chunk truncated %d → %d chars to fit embedding context window",
            len(text), _MAX_EMBED_CHARS,
        )
        return text[:_MAX_EMBED_CHARS]
    return text


class EmbeddingClient:
    """
    Unified embedding interface for Ollama and Azure OpenAI.

    Usage:
        client = EmbeddingClient.from_config(config)
        vectors = client.embed(["text one", "text two"])   # np.ndarray (n, dim)
    """

    def __init__(self, provider: str, model: str, **kwargs):
        self.provider = provider
        self.model = model
        self._kwargs = kwargs
        self._client = None
        self._dim: Optional[int] = None

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_config(cls, config: dict) -> "EmbeddingClient":
        emb = config.get("embeddings", {})
        provider = emb.get("provider", "ollama")

        if provider == "ollama":
            ollama_cfg = config.get("ollama", {})
            return cls(
                provider="ollama",
                model=emb.get("model", "nomic-embed-text"),
                host=ollama_cfg.get("host", "http://localhost:11434"),
                # Pass num_ctx so Ollama uses the model's full context window.
                # nomic-embed-text supports 8192 tokens; Ollama defaults to 2048.
                num_ctx=emb.get("ollama_num_ctx", 8192),
            )

        if provider == "azure":
            import os
            azure_cfg = config.get("azure", {})
            api_key = os.environ.get(azure_cfg.get("api_key_env", "AZURE_OPENAI_API_KEY"), "")
            endpoint = (
                os.environ.get(azure_cfg.get("endpoint_env", ""), "")
                or azure_cfg.get("endpoint", "")
            )
            return cls(
                provider="azure",
                model=emb.get("azure_deployment", "text-embedding-3-large"),
                endpoint=endpoint,
                api_key=api_key,
                api_version=azure_cfg.get("api_version", "2024-12-01-preview"),
            )

        raise ValueError(f"Unknown embedding provider: {provider!r}")

    # ------------------------------------------------------------------
    # Lazy client init
    # ------------------------------------------------------------------

    def _get_ollama_client(self):
        if self._client is None:
            import ollama
            self._client = ollama.Client(host=self._kwargs.get("host", "http://localhost:11434"))
        return self._client

    def _get_azure_client(self):
        if self._client is None:
            from openai import AzureOpenAI
            self._client = AzureOpenAI(
                azure_endpoint=self._kwargs["endpoint"],
                api_key=self._kwargs["api_key"],
                api_version=self._kwargs["api_version"],
            )
        return self._client

    # ------------------------------------------------------------------
    # Core embed methods
    # ------------------------------------------------------------------

    def _embed_ollama_one(self, client, text: str, num_ctx: int) -> list[float]:
        """
        Embed a single text via Ollama.

        Uses the new /api/embed endpoint (Ollama ≥ 0.1.34) with truncate=True.
        No `options` are sent — options caused HTTP 400 on the new endpoint in
        some Ollama builds.  truncate=True is the server-side safety valve;
        _safe_truncate() is the Python-side pre-filter.

        Falls back to the legacy /api/embeddings endpoint if client.embed()
        is not available (older Ollama Python library).
        """
        # ── New API: POST /api/embed ───────────────────────────────────────
        if hasattr(client, "embed"):
            resp = client.embed(
                model=self.model,
                input=text,
                truncate=True,   # silently clips overlong input; no options dict
            )
            embeddings = (
                resp.get("embeddings")
                if isinstance(resp, dict)
                else getattr(resp, "embeddings", None)
            )
            if embeddings:
                return embeddings[0]

        # ── Legacy API: POST /api/embeddings ──────────────────────────────
        resp = client.embeddings(
            model=self.model,
            prompt=text,
            options={"num_ctx": num_ctx},
        )
        return resp.get("embedding") if isinstance(resp, dict) else resp["embedding"]

    def _embed_ollama_batch(self, texts: list[str]) -> np.ndarray:
        client = self._get_ollama_client()
        num_ctx = self._kwargs.get("num_ctx", 8192)
        vectors = []
        for text in texts:
            text = _safe_truncate(text)
            for attempt in range(1, _RETRY_ATTEMPTS + 1):
                try:
                    vectors.append(self._embed_ollama_one(client, text, num_ctx))
                    break
                except Exception as exc:
                    if attempt == _RETRY_ATTEMPTS:
                        raise RuntimeError(
                            f"Ollama embedding failed after {_RETRY_ATTEMPTS} attempts: {exc}"
                        ) from exc
                    logger.warning("Ollama retry %d/%d: %s", attempt, _RETRY_ATTEMPTS, exc)
                    time.sleep(_RETRY_DELAY)
        return np.array(vectors, dtype=np.float32)

    def _embed_azure_batch(self, texts: list[str]) -> np.ndarray:
        client = self._get_azure_client()
        for attempt in range(1, _RETRY_ATTEMPTS + 1):
            try:
                resp = client.embeddings.create(input=texts, model=self.model)
                vectors = [item.embedding for item in sorted(resp.data, key=lambda x: x.index)]
                return np.array(vectors, dtype=np.float32)
            except Exception as exc:
                if attempt == _RETRY_ATTEMPTS:
                    raise RuntimeError(
                        f"Azure embedding failed after {_RETRY_ATTEMPTS} attempts: {exc}"
                    ) from exc
                logger.warning("Azure retry %d/%d: %s", attempt, _RETRY_ATTEMPTS, exc)
                time.sleep(_RETRY_DELAY)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def embed(self, texts: list[str]) -> np.ndarray:
        """
        Embed a list of texts. Returns np.ndarray of shape (len(texts), dim).
        Processes in batches to avoid memory/timeout issues.
        """
        if not texts:
            return np.empty((0, self.dim), dtype=np.float32)

        all_vectors = []
        for i in range(0, len(texts), _BATCH_SIZE):
            batch = texts[i : i + _BATCH_SIZE]
            logger.info(
                "Embedding batch %d–%d / %d",
                i + 1, min(i + _BATCH_SIZE, len(texts)), len(texts),
            )
            if self.provider == "ollama":
                vecs = self._embed_ollama_batch(batch)
            elif self.provider == "azure":
                vecs = self._embed_azure_batch(batch)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            all_vectors.append(vecs)

        return np.vstack(all_vectors)

    def embed_one(self, text: str) -> np.ndarray:
        """Embed a single text. Returns 1-D np.ndarray of shape (dim,)."""
        return self.embed([text])[0]

    @property
    def dim(self) -> int:
        """Return embedding dimension (lazily detected on first call)."""
        if self._dim is None:
            probe = self.embed(["probe"])
            self._dim = probe.shape[1]
        return self._dim
