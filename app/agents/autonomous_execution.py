"""Autonomous revenue execution pipeline for evidence-backed opportunities."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional
from .permissions import Risk, can_execute
from .revenue_os import RevenueOS


@dataclass(frozen=True)
class ExecutionStep:
    name: str
    action: str
    status: str
    reason: str
    value: Optional[float] = None


class AutonomousExecutionEngine:
    """Turns an observed opportunity into bounded, reversible commercial work."""

    def __init__(self, executor: Optional[Callable[[str, dict[str, Any]], Any]] = None,
                 revenue_os: Optional[RevenueOS] = None) -> None:
        self.executor = executor
        self.revenue_os = revenue_os or RevenueOS()

    def plan(self, opportunity: dict[str, Any]) -> list[ExecutionStep]:
        evidence = opportunity.get("evidence") or opportunity.get("summary")
        if not evidence:
            return [ExecutionStep("verify", "market_research", "blocked", "missing evidence")]
        ranked = self.revenue_os.rank(opportunity, limit=1)
        steps = [
            ExecutionStep("verify", "market_research", "ready", "evidence present"),
            ExecutionStep("hunt", "opportunity_hunt", "ready", "find the highest-value supported opportunity"),
            ExecutionStep("leads", "lead_generation", "ready", "identify appropriate prospects and channels"),
            ExecutionStep("prepare", "offer_build", "ready", "prepare a truthful offer"),
            ExecutionStep("price", "dynamic_pricing", "ready", "optimize price inside configured bounds"),
        ]
        if ranked:
            steps.append(ExecutionStep("money_route", ranked[0]["action"], "ready", f"top revenue channel: {ranked[0]['channel']} (score {ranked[0]['score']})"))
        steps.extend([
            ExecutionStep("contact", "customer_reply", "ready", "contact only an appropriate prospect/channel"),
            ExecutionStep("negotiate", "negotiate", "ready", "within configured limits"),
            ExecutionStep("recover", "lead_recovery", "ready", "recover eligible lost opportunities without spam"),
            ExecutionStep("followup", "followup", "ready", "schedule non-spam follow-up"),
            ExecutionStep("referral", "referral", "ready", "request eligible referrals transparently"),
            ExecutionStep("measure", "revenue_tracking", "ready", "record funnel and profit metrics"),
        ])
        if opportunity.get("voice_call"):
            steps.insert(7, ExecutionStep("call", "voice_call", "ready", "call only an explicitly eligible/allowlisted prospect"))
        return steps

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
