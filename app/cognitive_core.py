from __future__ import annotations

"""ORVIA Cognitive Core: evidence-first rapid learning and meta-learning.

This layer does not claim human-level or superhuman intelligence. It makes
learning measurable by turning observations and outcomes into reusable memory,
hypotheses, strategy updates, and benchmarks.
"""

import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from .memory_store import memory_store

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "cognitive_state.json"
EVENT_PATH = ROOT / "data" / "cognitive_activity.jsonl"
_lock = Lock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {
            "cycles": 0,
            "observations": 0,
            "hypotheses": 0,
            "experiments": 0,
            "lessons": 0,
            "verified_lessons": 0,
            "strategy_updates": 0,
            "errors_learned": 0,
            "last_cycle_at": None,
            "learning_rate": 0.0,
            "knowledge_retention": 0.0,
        }
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _log(event: str, data: dict[str, Any]) -> None:
    record = {"timestamp": _now(), "event": event, **data}
    with _lock:
        EVENT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with EVENT_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


class CognitiveCore:
    """Measurable cognitive improvement loop: observe -> test -> learn -> reuse."""

    def observe(self, topic: str, observation: str, source: str = "system",
                evidence: list[str] | None = None) -> dict[str, Any]:
        state = _load_state()
        state["observations"] = int(state.get("observations", 0)) + 1
        item = {
            "topic": topic.strip(),
            "observation": observation.strip(),
            "source": source,
            "evidence": evidence or [],
            "observed_at": _now(),
        }
        memory_store.record("cognitive_observation", item, source=source)
        _write_state(state)
        _log("observation", item)
        return item

    def hypothesize(self, problem: str, hypotheses: list[str]) -> dict[str, Any]:
        hypotheses = [str(x).strip() for x in hypotheses if str(x).strip()]
        state = _load_state()
        state["hypotheses"] = int(state.get("hypotheses", 0)) + len(hypotheses)
        item = {"problem": problem.strip(), "hypotheses": hypotheses, "created_at": _now()}
        memory_store.record("cognitive_hypotheses", item, source="cognitive_core")
        _write_state(state)
        _log("hypotheses", item)
        return item

    def record_experiment(self, hypothesis: str, result: str, success: bool,
                          metric: float | None = None, evidence: list[str] | None = None) -> dict[str, Any]:
        state = _load_state()
        state["experiments"] = int(state.get("experiments", 0)) + 1
        item = {
            "hypothesis": hypothesis,
            "result": result,
            "success": bool(success),
            "metric": metric,
            "evidence": evidence or [],
            "tested_at": _now(),
        }
        memory_store.record("cognitive_experiment", item, source="experiment_lab")
        _write_state(state)
        _log("experiment", item)
        return item

    def learn(self, lesson: str, topic: str, confidence: float = 0.5,
              verified: bool = False, source: str = "experience") -> dict[str, Any]:
        confidence = max(0.0, min(1.0, float(confidence)))
        state = _load_state()
        state["lessons"] = int(state.get("lessons", 0)) + 1
        if verified:
            state["verified_lessons"] = int(state.get("verified_lessons", 0)) + 1
        item = {
            "topic": topic,
            "lesson": lesson,
            "confidence": confidence,
            "verified": bool(verified),
            "source": source,
            "learned_at": _now(),
        }
        memory_store.record("cognitive_lesson", item, source=source)
        _write_state(state)
        _log("lesson", item)
        return item

    def learn_from_error(self, error: str, cause: str, prevention: str) -> dict[str, Any]:
        state = _load_state()
        state["errors_learned"] = int(state.get("errors_learned", 0)) + 1
        item = {"error": error, "cause": cause, "prevention": prevention, "learned_at": _now()}
        memory_store.record("failure_lesson", item, source="error_learning")
        _write_state(state)
        _log("error_learning", item)
        return item

    def update_strategy(self, strategy: str, evidence: str, outcome: str,
                        score_before: float | None = None, score_after: float | None = None) -> dict[str, Any]:
        state = _load_state()
        state["strategy_updates"] = int(state.get("strategy_updates", 0)) + 1
        item = {
            "strategy": strategy,
            "evidence": evidence,
            "outcome": outcome,
            "score_before": score_before,
            "score_after": score_after,
            "updated_at": _now(),
        }
        memory_store.record("strategy_update", item, source="meta_learning")
        _write_state(state)
        _log("strategy_update", item)
        return item

    def run_cycle(self, topic: str = "ORVIA continuous improvement") -> dict[str, Any]:
        state = _load_state()
        state["cycles"] = int(state.get("cycles", 0)) + 1
        state["last_cycle_at"] = _now()
        recent = memory_store.recent(200)
        kinds = Counter(x.get("kind") for x in recent)
        # A conservative, measurable proxy: verified lessons relative to all lessons.
        lessons = max(1, int(state.get("lessons", 0)))
        verified = int(state.get("verified_lessons", 0))
        state["learning_rate"] = round(verified / lessons, 4)
        state["knowledge_retention"] = round(
            min(1.0, sum(1 for x in recent if x.get("kind") == "cognitive_lesson") / 20.0), 4
        )
        _write_state(state)
        result = {
            "status": "completed",
            "topic": topic,
            "cycle": state["cycles"],
            "learning_rate": state["learning_rate"],
            "knowledge_retention": state["knowledge_retention"],
            "recent_memory_items": len(recent),
            "memory_mix": dict(kinds),
            "next_action": "prioritize the highest-impact unverified knowledge gap",
        }
        _log("cycle", result)
        return result

    def benchmark(self) -> dict[str, Any]:
        state = _load_state()
        return {
            "name": "ORVIA Intelligence Benchmark",
            "method": "measured task performance, learning progress, error reduction and verified outcomes",
            "dimensions": [
                "problem_solving", "reasoning_quality", "learning_rate",
                "knowledge_retention", "transfer", "planning",
                "execution_reliability", "error_reduction", "tool_use", "collaboration",
            ],
            "state": state,
            "warning": "This benchmark is not a claim of human-level or superhuman general intelligence.",
        }

    def status(self) -> dict[str, Any]:
        state = _load_state()
        return {
            "status": "ok",
            "engine": "ORVIA Cognitive Core",
            "mode": "rapid_learning_and_meta_learning",
            "state": state,
            "principles": [
                "evidence_first",
                "learn_from_success_and_failure",
                "hypothesis_before_confidence",
                "measure_before_claim",
                "reuse_verified_knowledge",
            ],
        }


cognitive_core = CognitiveCore()
