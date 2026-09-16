"""Autonomous self-improvement layer for HAMED AGI.

This module turns verified learning and observed outcomes into explicit
improvement plans. It does not grant new permissions: execution authority
remains controlled by the existing permission/approval layer.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class SelfImprovementEngine:
    """Learn, reflect, identify gaps, and produce the next improvement plan."""

    def __init__(self, orchestrator: Any, state_path: Optional[str] = None) -> None:
        self.orchestrator = orchestrator
        self.state_path = Path(
            state_path or os.getenv("HAMED_SELF_IMPROVEMENT_STATE", "hamed_self_improvement.json")
        )
        self.state = self._load()

    def _load(self) -> Dict[str, Any]:
        try:
            value = json.loads(self.state_path.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                value.setdefault("cycles", 0)
                value.setdefault("plans", [])
                value.setdefault("skill_gaps", [])
                value.setdefault("goals", [])
                return value
        except Exception:
            pass
        return {"cycles": 0, "plans": [], "skill_gaps": [], "goals": []}

    def _save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def reflect(self, topic: str, evidence: str, outcome: str = "") -> Dict[str, Any]:
        prompt = (
            "You are Hamed AGI's self-improvement engine. Review the latest learning and outcome. "
            "Identify what Hamed learned, what remains uncertain, skill gaps, process weaknesses, "
            "and the smallest reversible next improvements. Create measurable goals. "
            "Do not invent facts. Do not grant new permissions. Do not propose bypassing safety, "
            "approval, platform, privacy, or legal controls. Separate evidence from hypotheses.\n\n"
            "TOPIC:\n" + topic + "\n\nEVIDENCE:\n" + evidence[:10000] +
            "\n\nOUTCOME:\n" + outcome[:6000]
        )
        try:
            reflection = self.orchestrator.provider.generate_response(
                [{"role": "user", "content": prompt}],
                system="Return a concise structured self-improvement plan for an autonomous business agent.",
            )
        except Exception as exc:
            reflection = "Self-improvement provider unavailable: " + type(exc).__name__

        now = datetime.now(timezone.utc).isoformat()
        plan = {"time": now, "topic": topic, "reflection": reflection[:8000]}
        self.state["cycles"] = int(self.state.get("cycles", 0)) + 1
        self.state.setdefault("plans", []).append(plan)
        self.state["plans"] = self.state["plans"][-100:]
        self._save()
        return plan

    def add_goal(self, goal: str, metric: str = "") -> Dict[str, str]:
        item = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "goal": goal,
            "metric": metric,
            "status": "active",
        }
        self.state.setdefault("goals", []).append(item)
        self.state["goals"] = self.state["goals"][-100:]
        self._save()
        return item
