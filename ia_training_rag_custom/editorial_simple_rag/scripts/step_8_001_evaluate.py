"""
Step 8 — Evaluate (E6)
-----------------------
Scores LLM answers from the history on three metrics:

  Faithfulness     — is the answer grounded in the retrieved sources?
  Relevance        — does the answer address the question?
  Context precision — were the right chunks retrieved?

Each metric is scored 0.0–1.0 by asking the LLM to judge its own output
(LLM-as-a-judge pattern). Results are saved to:

    data/evaluations/<use_case>/eval_<timestamp>.json

Run standalone:
    python scripts/step_8_001_evaluate.py
    python scripts/step_8_001_evaluate.py --limit 10
    python scripts/step_8_001_evaluate.py --use-case editorial --tier 2
"""

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.llm.llm_client import LLMClient
from src.utils.config import load_config, get_logs_dir
from src.utils.db_manager import DBManager

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


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
            logging.FileHandler(logs_dir / "step_8_evaluate.log", encoding="utf-8"),
        ],
    )

logger = logging.getLogger("step8")


# ---------------------------------------------------------------------------
# Scoring prompts
# ---------------------------------------------------------------------------

_FAITHFULNESS_PROMPT = """\
You are an evaluator. Given a question, an answer, and the source passages \
that were retrieved to answer it, score the faithfulness of the answer.

Faithfulness means: every claim in the answer can be traced back to the sources.
Score 1.0 if fully faithful, 0.5 if partially faithful, 0.0 if not grounded.

Question: {question}

Sources:
{sources}

Answer: {answer}

Respond with ONLY a JSON object: {{"score": <0.0|0.5|1.0>, "reason": "<one sentence>"}}
"""

_RELEVANCE_PROMPT = """\
You are an evaluator. Score how well the answer addresses the question.

Relevance: does the answer directly respond to what was asked?
Score 1.0 if fully relevant, 0.5 if partially, 0.0 if off-topic.

Question: {question}
Answer: {answer}

Respond with ONLY a JSON object: {{"score": <0.0|0.5|1.0>, "reason": "<one sentence>"}}
"""

_CONTEXT_PRECISION_PROMPT = """\
You are an evaluator. Given a question and the retrieved source passages, \
score how well the retrieved context covers what is needed to answer the question.

Context precision: were the right passages retrieved?
Score 1.0 if the context clearly contains the answer, \
0.5 if partially useful, 0.0 if irrelevant.

Question: {question}

Retrieved passages:
{sources}

Respond with ONLY a JSON object: {{"score": <0.0|0.5|1.0>, "reason": "<one sentence>"}}
"""


# ---------------------------------------------------------------------------
# Score dataclass
# ---------------------------------------------------------------------------

@dataclass
class EvalScore:
    history_id: int
    question: str
    faithfulness: float = 0.0
    faithfulness_reason: str = ""
    relevance: float = 0.0
    relevance_reason: str = ""
    context_precision: float = 0.0
    context_precision_reason: str = ""
    overall: float = 0.0
    error: str = ""

    def compute_overall(self) -> None:
        self.overall = round(
            (self.faithfulness + self.relevance + self.context_precision) / 3, 4
        )

    def print(self) -> None:
        print(f"\n  Q: {self.question[:80]}")
        print(f"     Faithfulness     : {self.faithfulness:.2f}  — {self.faithfulness_reason}")
        print(f"     Relevance        : {self.relevance:.2f}  — {self.relevance_reason}")
        print(f"     Context precision: {self.context_precision:.2f}  — {self.context_precision_reason}")
        print(f"     Overall          : {self.overall:.2f}")


# ---------------------------------------------------------------------------
# LLM judge helper
# ---------------------------------------------------------------------------

_SCORE_RE = re.compile(r'"score"\s*:\s*([0-9.]+)')
_REASON_RE = re.compile(r'"reason"\s*:\s*"([^"]+)"')


def _ask_judge(llm: LLMClient, prompt: str) -> tuple[float, str]:
    """Call the LLM judge and parse the JSON response. Returns (score, reason)."""
    try:
        raw = llm.complete(prompt)
        # Try full JSON parse first
        try:
            data = json.loads(raw)
            return float(data.get("score", 0.0)), data.get("reason", "")
        except json.JSONDecodeError:
            pass
        # Fallback: regex extract
        score_m = _SCORE_RE.search(raw)
        reason_m = _REASON_RE.search(raw)
        score = float(score_m.group(1)) if score_m else 0.0
        reason = reason_m.group(1) if reason_m else raw[:100]
        return score, reason
    except Exception as exc:
        logger.warning("Judge call failed: %s", exc)
        return 0.0, f"error: {exc}"


# ---------------------------------------------------------------------------
# Core evaluate function (importable by step 7 Evaluation tab)
# ---------------------------------------------------------------------------

def evaluate_entry(entry: dict, llm: LLMClient) -> EvalScore:
    """
    Score a single history entry on all three metrics.

    Args:
        entry: row from db.get_history() — has question, answer, sources
        llm:   LLMClient to use as judge
    """
    score = EvalScore(
        history_id=entry.get("id", 0),
        question=entry["question"],
    )

    # Build sources block
    sources_text = "\n\n".join(
        f"[{i+1}] {s.get('title', s.get('source',''))} — {s.get('date','')[:10]}"
        for i, s in enumerate(entry.get("sources", []))
    )
    if not sources_text:
        sources_text = "(no sources)"

    try:
        # Faithfulness
        faith_score, faith_reason = _ask_judge(
            llm,
            _FAITHFULNESS_PROMPT.format(
                question=entry["question"],
                answer=entry["answer"],
                sources=sources_text,
            ),
        )
        score.faithfulness = faith_score
        score.faithfulness_reason = faith_reason

        # Relevance
        rel_score, rel_reason = _ask_judge(
            llm,
            _RELEVANCE_PROMPT.format(
                question=entry["question"],
                answer=entry["answer"],
            ),
        )
        score.relevance = rel_score
        score.relevance_reason = rel_reason

        # Context precision
        ctx_score, ctx_reason = _ask_judge(
            llm,
            _CONTEXT_PRECISION_PROMPT.format(
                question=entry["question"],
                sources=sources_text,
            ),
        )
        score.context_precision = ctx_score
        score.context_precision_reason = ctx_reason

    except Exception as exc:
        score.error = str(exc)
        logger.error("Evaluation failed for '%s': %s", entry["question"][:60], exc)

    score.compute_overall()
    return score


def evaluate_batch(entries: list[dict], llm: LLMClient) -> list[EvalScore]:
    scores = []
    for i, entry in enumerate(entries, 1):
        logger.info("Evaluating %d/%d: '%s'", i, len(entries), entry["question"][:60])
        score = evaluate_entry(entry, llm)
        score.print()
        scores.append(score)
    return scores


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_results(scores: list[EvalScore], use_case: str) -> Path:
    out_dir = _PROJECT_ROOT / "data" / "evaluations" / use_case
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = out_dir / f"eval_{ts}.json"

    data = {
        "timestamp": ts,
        "use_case": use_case,
        "count": len(scores),
        "avg_faithfulness": round(sum(s.faithfulness for s in scores) / len(scores), 4) if scores else 0,
        "avg_relevance": round(sum(s.relevance for s in scores) / len(scores), 4) if scores else 0,
        "avg_context_precision": round(sum(s.context_precision for s in scores) / len(scores), 4) if scores else 0,
        "avg_overall": round(sum(s.overall for s in scores) / len(scores), 4) if scores else 0,
        "scores": [asdict(s) for s in scores],
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return out_path


def _print_summary(scores: list[EvalScore]) -> None:
    if not scores:
        return
    print(f"\n{'='*60}")
    print(f"Evaluation summary — {len(scores)} answer(s)")
    print(f"{'='*60}")
    print(f"  Faithfulness     : {sum(s.faithfulness for s in scores)/len(scores):.2f}")
    print(f"  Relevance        : {sum(s.relevance for s in scores)/len(scores):.2f}")
    print(f"  Context precision: {sum(s.context_precision for s in scores)/len(scores):.2f}")
    print(f"  Overall          : {sum(s.overall for s in scores)/len(scores):.2f}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Step 8 — Evaluate RAG answers")
    parser.add_argument("--use-case", help="Override active_use_case from config.yaml")
    parser.add_argument("--limit", type=int, default=5,
                        help="Number of history entries to evaluate (default: 5)")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3],
                        help="Filter history by LLM tier")
    args = parser.parse_args()

    logs_dir = get_logs_dir()
    _setup_logging(logs_dir)

    config = load_config()
    use_case = args.use_case or config["active_use_case"]

    logger.info("=== Step 8 — Evaluate ===")
    logger.info("Use case : %s  |  limit: %d", use_case, args.limit)

    # Load history
    db_cfg = config.get("database", {})
    db_path = _PROJECT_ROOT / db_cfg.get("path", "data/rag_cache.db")
    db = DBManager(db_path)

    entries = db.get_history(use_case=use_case, tier=args.tier, limit=args.limit)
    if not entries:
        logger.warning("No history entries found. Run some queries first via step_7.")
        sys.exit(0)

    logger.info("Evaluating %d entr(ies) with LLM-as-a-judge…", len(entries))

    llm = LLMClient.from_config(config)
    scores = evaluate_batch(entries, llm)

    _print_summary(scores)

    out_path = save_results(scores, use_case)
    logger.info("Results saved → %s", out_path)
    logger.info("Step 8 done.")


if __name__ == "__main__":
    main()
