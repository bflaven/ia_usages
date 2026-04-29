"""
Conversational memory (E7).

Keeps the last N turns and detects follow-up questions.
When a follow-up is detected, rewrites the question as a standalone query
using the LLM so the retrieval step has full context.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# Pronouns and demonstratives that suggest a follow-up
_FOLLOWUP_PATTERNS = re.compile(
    r"\b(it|its|they|them|their|this|that|these|those|he|she|him|her|"
    r"the same|the article|the author|the report|same topic)\b",
    re.IGNORECASE,
)

_REWRITE_PROMPT = (
    "Given the conversation history below, rewrite the follow-up question "
    "as a fully self-contained question that can be understood without the history.\n\n"
    "History:\n{history}\n\n"
    "Follow-up question: {question}\n\n"
    "Rewritten question (output ONLY the rewritten question, nothing else):"
)


@dataclass
class Turn:
    question: str
    answer: str
    rewritten: Optional[str] = None   # filled if question was rewritten


class ConversationMemory:
    """
    Stores the last `max_turns` Q&A pairs and rewrites follow-up questions.
    """

    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self._turns: list[Turn] = []

    # ------------------------------------------------------------------
    # Turn management
    # ------------------------------------------------------------------

    def add(self, question: str, answer: str, rewritten: Optional[str] = None) -> None:
        self._turns.append(Turn(question=question, answer=answer, rewritten=rewritten))
        if len(self._turns) > self.max_turns:
            self._turns.pop(0)

    def clear(self) -> None:
        self._turns.clear()

    @property
    def turns(self) -> list[Turn]:
        return list(self._turns)

    @property
    def is_empty(self) -> bool:
        return len(self._turns) == 0

    # ------------------------------------------------------------------
    # Follow-up detection
    # ------------------------------------------------------------------

    def is_followup(self, question: str) -> bool:
        """Heuristic: short question containing a pronoun/demonstrative."""
        if self.is_empty:
            return False
        words = question.split()
        # Very short questions are likely follow-ups ("And the author?")
        if len(words) <= 5:
            return True
        return bool(_FOLLOWUP_PATTERNS.search(question))

    # ------------------------------------------------------------------
    # Rewrite
    # ------------------------------------------------------------------

    def rewrite(self, question: str, llm_client) -> str:
        """
        Rewrite `question` as a standalone query using the LLM.
        Returns the original question unchanged on failure.
        """
        history_lines = []
        for t in self._turns[-3:]:   # last 3 turns for context
            q = t.rewritten or t.question
            history_lines.append(f"Q: {q}")
            history_lines.append(f"A: {t.answer[:300]}")

        prompt = _REWRITE_PROMPT.format(
            history="\n".join(history_lines),
            question=question,
        )
        try:
            rewritten = llm_client.complete(prompt).strip()
            logger.info("E7 rewrite: '%s' → '%s'", question, rewritten)
            return rewritten
        except Exception as exc:
            logger.warning("E7 rewrite failed: %s — using original question", exc)
            return question

    # ------------------------------------------------------------------
    # Context string for prompt injection
    # ------------------------------------------------------------------

    def as_context(self) -> str:
        """Return recent turns as a string for inclusion in the synthesis prompt."""
        if self.is_empty:
            return ""
        lines = ["Recent conversation:"]
        for t in self._turns[-3:]:
            lines.append(f"Q: {t.rewritten or t.question}")
            lines.append(f"A: {t.answer[:200]}")
        return "\n".join(lines)
