"""Unified commercial engines for HAMED AGI.

The engines are deterministic, testable planning components. External execution
must still pass through the permission layer and configured adapters.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    kind: str
    title: str
    target: str
    source: str = ""
    evidence: str = ""
    cost: float = 0.0
    expected_revenue: float = 0.0
    probability: float = 0.0
    risk_score: float = 0.0
    time_hours: float = 0.0
    next_action: str = "research"
    approval_required: bool = False

    @property
    def expected_profit(self) -> float:
        return self.expected_revenue - self.cost

    @property
    def margin_percent(self) -> float:
        return (self.expected_profit / self.expected_revenue * 100) if self.expected_revenue else 0.0

    @property
    def expected_value(self) -> float:
        return self.expected_profit * max(0.0, min(1.0, self.probability))

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.update(expected_profit=self.expected_profit, margin_percent=self.margin_percent, expected_value=self.expected_value)
        return data


def score_opportunity(o: Opportunity) -> float:
    """Risk/time-adjusted score; higher means more attractive for investigation."""
    return o.expected_value * (1.0 - max(0.0, min(1.0, o.risk_score))) / max(1.0, o.time_hours)


def rank_opportunities(items: list[Opportunity]) -> list[Opportunity]:
    return sorted(items, key=score_opportunity, reverse=True)


def build_service_offer(service: str, problem: str, target: str, price: float, value_points: list[str]) -> dict[str, Any]:
    return {"type": "service_offer", "service": service, "problem": problem, "target": target, "price": price, "value_points": value_points, "ai_disclosure": True}


def build_affiliate_test(product: str, audience: str, commission: float, content_angles: list[str]) -> dict[str, Any]:
    return {"type": "affiliate_test", "product": product, "audience": audience, "commission": commission, "content_angles": content_angles, "metrics": ["clicks", "conversion", "revenue", "refund_rate"]}


def build_b2b_match(buyer_need: str, buyer: str, supplier: str, terms: dict[str, Any]) -> dict[str, Any]:
    return {"type": "b2b_match", "buyer_need": buyer_need, "buyer": buyer, "supplier": supplier, "terms": terms, "commission_model": "configured"}


def build_site_audit(target: str, findings: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "site_audit", "target": target, "findings": findings, "offer_next": True}
