"""
LLMClient — wraps Ollama (Tier 2) and Azure OpenAI (Tier 3).
Tier 1 (static template) is handled directly in synthesize.py.

Provider and model are selected from config.yaml (llm.provider / llm.model).
"""

import logging
import os

logger = logging.getLogger(__name__)

_TIMEOUT = 120   # seconds


class LLMClient:
    """
    Unified LLM interface for Ollama and Azure OpenAI.

    Usage:
        client = LLMClient.from_config(config)
        answer = client.complete(prompt)
    """

    def __init__(self, provider: str, model: str, **kwargs):
        self.provider = provider
        self.model = model
        self._kwargs = kwargs
        self._client = None

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_config(cls, config: dict) -> "LLMClient":
        llm = config.get("llm", {})
        provider = llm.get("provider", "ollama")

        if provider == "ollama":
            ollama_cfg = config.get("ollama", {})
            return cls(
                provider="ollama",
                model=llm.get("model", "llama3.1"),
                host=ollama_cfg.get("host", "http://localhost:11434"),
            )

        if provider == "azure":
            azure_cfg = config.get("azure", {})
            api_key = os.environ.get(azure_cfg.get("api_key_env", "AZURE_OPENAI_API_KEY"), "")
            # Endpoint: prefer env var (endpoint_env), fall back to inline value
            endpoint = (
                os.environ.get(azure_cfg.get("endpoint_env", ""), "")
                or azure_cfg.get("endpoint", "")
            )
            return cls(
                provider="azure",
                model=llm.get("azure_deployment", "gpt-4.1"),
                endpoint=endpoint,
                api_key=api_key,
                api_version=azure_cfg.get("api_version", "2024-12-01-preview"),
            )

        raise ValueError(f"Unknown LLM provider: {provider!r}")

    # ------------------------------------------------------------------
    # Lazy client init
    # ------------------------------------------------------------------

    def _get_ollama_client(self):
        if self._client is None:
            import ollama
            self._client = ollama.Client(
                host=self._kwargs.get("host", "http://localhost:11434")
            )
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
    # Public API
    # ------------------------------------------------------------------

    def complete(self, prompt: str, system: str = "") -> str:
        """
        Send a prompt to the LLM and return the response text.

        Args:
            prompt: the user/question prompt
            system: optional system instruction
        """
        if self.provider == "ollama":
            return self._complete_ollama(prompt, system)
        if self.provider == "azure":
            return self._complete_azure(prompt, system)
        raise ValueError(f"Unknown provider: {self.provider}")

    # ------------------------------------------------------------------
    # Provider implementations
    # ------------------------------------------------------------------

    def _complete_ollama(self, prompt: str, system: str) -> str:
        client = self._get_ollama_client()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": 0.1},
        )
        return response["message"]["content"].strip()

    def _complete_azure(self, prompt: str, system: str) -> str:
        client = self._get_azure_client()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            timeout=_TIMEOUT,
        )
        return response.choices[0].message.content.strip()
