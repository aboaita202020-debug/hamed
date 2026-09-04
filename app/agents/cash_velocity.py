"""Cash Velocity Engine: prioritize legitimate opportunities by time-to-cash.

The engine uses only opportunity data Hamed is allowed to access. It does not
infer or expose private balances, confidential budgets, or financial records.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .compliance_checkpoint import ExternalComplianceCheckpoint


@dataclass(frozen=True)
class CashAssessment:
    route: str
    score: float
    expected_profit: float
    time_to_cash_hours: float
    decision_speed: float
    payment_ready: float
    fulfillment_ready: float
    probability: float
    risk_penalty: float
    status: str
    reason: str
    compliance_status: str = "not_required"


class CashVelocityEngine:
    """Ranks opportunities for the fastest realistic, compliant collection."""

    ROUTES = (
        "warm_reactivation",
        "approved_public_opportunity",
        "ready_to_buy",
        "buyer_first",
        "arbitrage",
        "qualified_lead_sale",
    )

    def __init__(self, compliance: ExternalComplianceCheckpoint | None = None) -> None:
        self.compliance = compliance or ExternalComplianceCheckpoint()

    def assess(self, opportunity: dict[str, Any]) -> CashAssessment:
        route = str(opportunity.get("route") or opportunity.get("channel") or "ready_to_buy")
        if route not in self.ROUTES:
            route = "ready_to_buy"

        evidence = opportunity.get("evidence") or opportunity.get("summary")
        if not evidence:
            return CashAssessment(route, 0, 0, 9999, 0, 0, 0, 0, 100, "blocked", "missing evidence")

        compliance_review = self.compliance.evaluate(opportunity)
        if compliance_review.required and not opportunity.get("external_compliance_approved"):
            return CashAssessment(
                route, 0, 0, 9999, 0, 0, 0, 0, 100, "blocked",
                "external compliance review required before autonomous execution",
                compliance_review.status,
            )

        decision = self._bounded(opportunity.get("decision_speed", 0.5))
        payment = self._bounded(opportunity.get("payment_ready", 0.5))
        fulfillment = self._bounded(opportunity.get("fulfillment_ready", 0.5))
        probability = self._bounded(opportunity.get("close_probability", 0.5))
        risk = self._bounded(opportunity.get("risk", 0.0))
        approvals = max(0, int(opportunity.get("approval_count", 0) or 0))
        if approvals > 1 or opportunity.get("requires_escalation"):
            decision *= 0.35
        if not opportunity.get("payment_method") and payment >= 0.5:
            payment *= 0.6
        profit = max(0.0, float(opportunity.get("expected_profit", 0) or 0))
        hours = max(0.25, float(opportunity.get("time_to_cash_hours", 24) or 24))
        speed = max(0.0, min(100.0, (decision * 0.25 + payment * 0.25 + fulfillment * 0.2 + probability * 0.3) * 100))
        score = max(0.0, min(100.0, speed - risk * 25 + min(profit / 1000.0, 20) + (12 if route == "warm_reactivation" else 0)))
        status = "fast_track" if score >= 70 and approvals <= 1 and payment >= 0.6 else "slow_track"
        reason = "fast decision/payment/fulfillment path" if status == "fast_track" else "requires more evidence, approvals, payment readiness, or fulfillment readiness"
        return CashAssessment(route, round(score, 2), round(profit, 2), round(hours, 2), round(decision, 3), round(payment, 3), round(fulfillment, 3), round(probability, 3), round(risk, 3), status, reason, compliance_review.status)

    def rank(self, opportunities: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
        assessed = [self.assess(item) for item in opportunities]
        assessed.sort(key=lambda x: (x.status == "fast_track", x.score, x.expected_profit), reverse=True)
        return [asdict(item) for item in assessed[:limit]]

    @staticmethod
    def _bounded(value: Any) -> float:
        try:
            return max(0.0, min(1.0, float(value)))
        except (TypeError, ValueError):
            return 0.0
