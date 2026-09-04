"""Autonomous execution pipeline for evidence-backed commercial opportunities."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional
from .permissions import Risk, can_execute


@dataclass(frozen=True)
class ExecutionStep:
    name: str
    action: str
    status: str
    reason: str
    value: Optional[float] = None


class AutonomousExecutionEngine:
    """Turns an observed opportunity into bounded, reversible commercial work."""

    def __init__(self, executor: Optional[Callable[[str, dict[str, Any]], Any]] = None) -> None:
        self.executor = executor

    def plan(self, opportunity: dict[str, Any]) -> list[ExecutionStep]:
        evidence = opportunity.get("evidence") or opportunity.get("summary")
        if not evidence:
            return [ExecutionStep("verify", "market_research", "blocked", "missing evidence")]
        return [
            ExecutionStep("verify", "market_research", "ready", "evidence present"),
            ExecutionStep("prepare", "offer_build", "ready", "prepare a truthful offer"),
            ExecutionStep("contact", "customer_reply", "ready", "contact only an appropriate prospect/channel"),
            ExecutionStep("negotiate", "negotiate", "ready", "within configured limits"),
            ExecutionStep("followup", "followup", "ready", "schedule non-spam follow-up"),
        ]

    def execute(self, opportunity: dict[str, Any]) -> dict[str, Any]:
        steps = self.plan(opportunity)
        results = []
        for step in steps:
            allowed = can_execute(step.action, value=step.value, risk=Risk.LOW)
            if not allowed:
                results.append(asdict(ExecutionStep(step.name, step.action, "blocked", "server policy denied", step.value)))
                continue
            if self.executor:
                try:
                    output = self.executor(step.action, opportunity)
                    results.append(asdict(ExecutionStep(step.name, step.action, "executed", str(output)[:500], step.value)))
                except Exception as exc:
                    results.append(asdict(ExecutionStep(step.name, step.action, "error", type(exc).__name__, step.value)))
            else:
                results.append(asdict(ExecutionStep(step.name, step.action, "ready", "execution adapter not configured", step.value)))
        return {"autonomous": True, "guaranteed_revenue": False, "results": results}
