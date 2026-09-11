"""Provider-agnostic cognitive loop for Hamed.

The runtime is intentionally small and deterministic at its boundaries. An
LLM/council can propose plans and decisions, while this layer validates state,
tracks outcomes, records learning, and enforces execution gates.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Optional
import json
import uuid


@dataclass
class Goal:
    description: str
    success_criteria: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    priority: int = 5
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    status: str = "ACTIVE"


@dataclass
class PlanStep:
    title: str
    agent: str
    payload: dict[str, Any] = field(default_factory=dict)
    risk: str = "low"
    requires_approval: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    status: str = "PENDING"


@dataclass
class Decision:
    recommendation: str
    confidence: float
    reasons: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    requires_approval: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class LearningRecord:
    lesson: str
    evidence: str
    outcome: str
    confidence: float = 0.5
    source: str = "runtime"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CognitiveRuntime:
    """Run Hamed's goal -> plan -> deliberate -> gate -> execute -> learn loop."""

    def __init__(
        self,
        dispatcher: Optional[Callable[[str, dict[str, Any]], Any]] = None,
        approval_required_for: Optional[Iterable[str]] = None,
    ) -> None:
        self.dispatcher = dispatcher
        self.approval_required_for = set(approval_required_for or {"high", "critical"})
        self.learning: list[LearningRecord] = []
        self.history: list[dict[str, Any]] = []

    def create_goal(
        self,
        description: str,
        success_criteria: Optional[list[str]] = None,
        constraints: Optional[list[str]] = None,
        priority: int = 5,
    ) -> Goal:
        return Goal(description, success_criteria or [], constraints or [], priority)

    def build_plan(self, goal: Goal, steps: Iterable[PlanStep]) -> list[PlanStep]:
        plan = list(steps)
        if not plan:
            raise ValueError("goal_requires_at_least_one_plan_step")
        return plan

    def deliberate(
        self,
        goal: Goal,
        plan: list[PlanStep],
        confidence: float,
        reasons: Optional[list[str]] = None,
        risks: Optional[list[str]] = None,
    ) -> Decision:
        confidence = max(0.0, min(1.0, float(confidence)))
        high_risk = any(step.risk in self.approval_required_for for step in plan)
        decision = Decision(
            recommendation=f"execute_plan:{goal.id}",
            confidence=confidence,
            reasons=reasons or [],
            risks=risks or [],
            requires_approval=high_risk,
        )
        self.history.append({"type": "decision", "goal": goal.id, "decision": self._json(decision)})
        return decision

    def critique(self, goal: Goal, plan: list[PlanStep], decision: Decision) -> dict[str, Any]:
        issues: list[str] = []
        if decision.confidence < 0.60:
            issues.append("low_confidence")
        if not goal.success_criteria:
            issues.append("missing_success_criteria")
        if any(not step.agent for step in plan):
            issues.append("plan_step_missing_agent")
        if any(step.risk in self.approval_required_for for step in plan) and not decision.requires_approval:
            issues.append("approval_gate_bypassed")
        return {"passed": not issues, "issues": issues}

    def execute(
        self,
        goal: Goal,
        plan: list[PlanStep],
        decision: Decision,
        approved: bool = False,
    ) -> list[dict[str, Any]]:
        critique = self.critique(goal, plan, decision)
        if not critique["passed"]:
            raise RuntimeError(json.dumps({"execution_blocked": critique}, ensure_ascii=False))
        if decision.requires_approval and not approved:
            return [{"status": "WAITING_APPROVAL", "goal_id": goal.id}]
        if self.dispatcher is None:
            return [{"status": "PLANNED", "step": step.title, "agent": step.agent} for step in plan]

        results: list[dict[str, Any]] = []
        for step in plan:
            step.status = "RUNNING"
            try:
                raw = self.dispatcher(step.agent, step.payload)
                result = {"status": "DONE", "step": step.title, "agent": step.agent, "result": self._json(raw)}
                step.status = "DONE"
            except Exception as exc:
                step.status = "FAILED"
                result = {"status": "FAILED", "step": step.title, "agent": step.agent, "error": str(exc)}
            results.append(result)
            self.history.append({"type": "execution", "goal": goal.id, "result": result})
            if result["status"] == "FAILED":
                break
        return results

    def learn(self, lesson: str, evidence: str, outcome: str, confidence: float = 0.5, source: str = "runtime") -> LearningRecord:
        record = LearningRecord(lesson, evidence, outcome, max(0.0, min(1.0, confidence)), source)
        self.learning.append(record)
        self.history.append({"type": "learning", "record": self._json(record)})
        return record

    @staticmethod
    def _json(value: Any) -> Any:
        if hasattr(value, "__dataclass_fields__"):
            return {k: CognitiveRuntime._json(getattr(value, k)) for k in value.__dataclass_fields__}
        if isinstance(value, dict):
            return {str(k): CognitiveRuntime._json(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [CognitiveRuntime._json(v) for v in value]
        return value
