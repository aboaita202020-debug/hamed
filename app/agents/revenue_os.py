"""Revenue OS: prioritize legitimate fast-cash opportunities for Hamed."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class RevenueChannel:
    name: str
    action: str
    speed: float
    margin: float
    capital_required: float
    risk: float


CHANNELS = (
    RevenueChannel("service_sales", "website_service", 0.90, 0.85, 0.05, 0.10),
    RevenueChannel("b2b_brokerage", "b2b_brokerage", 0.82, 0.90, 0.02, 0.12),
    RevenueChannel("qualified_leads", "qualified_lead_sale", 0.88, 0.80, 0.05, 0.10),
    RevenueChannel("affiliate", "affiliate_marketing", 0.55, 0.70, 0.00, 0.08),
    RevenueChannel("resale", "sale", 0.72, 0.65, 0.20, 0.18),
    RevenueChannel("reactivation", "lead_recovery", 0.95, 0.82, 0.00, 0.05),
    RevenueChannel("upsell", "upsell", 0.93, 0.86, 0.00, 0.05),
    RevenueChannel("cross_sell", "cross_sell", 0.88, 0.80, 0.00, 0.06),
    RevenueChannel("buyer_first", "buyer_first", 0.90, 0.92, 0.03, 0.10),
    RevenueChannel("wholesale", "sale", 0.68, 0.78, 0.25, 0.20),
    RevenueChannel("referrals", "referral", 0.80, 0.88, 0.00, 0.04),
    RevenueChannel("retainer", "website_service", 0.58, 0.90, 0.02, 0.08),
)


class RevenueOS:
    """Scores evidence-backed opportunities by profit, speed, probability and risk."""

    def __init__(self, channels: tuple[RevenueChannel, ...] = CHANNELS) -> None:
        self.channels = channels

    def score(self, opportunity: dict[str, Any], channel: RevenueChannel) -> float:
        profit = max(float(opportunity.get("expected_profit", 0.0)), 0.0)
        probability = min(max(float(opportunity.get("close_probability", 0.5)), 0.0), 1.0)
        evidence = min(max(float(opportunity.get("evidence_quality", 0.5)), 0.0), 1.0)
        urgency = min(max(float(opportunity.get("urgency", 0.5)), 0.0), 1.0)
        capital = min(max(float(opportunity.get("capital_required", 0.0)), 0.0), 1.0)
        profit_factor = min(profit / 1000.0, 2.0) / 2.0
        return round(100 * (
            0.28 * profit_factor +
            0.24 * probability +
            0.18 * evidence +
            0.16 * urgency +
            0.10 * channel.speed +
            0.06 * channel.margin -
            0.04 * channel.risk -
            0.04 * capital
        ), 2)

    def rank(self, opportunity: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
        if not opportunity.get("evidence") and not opportunity.get("summary"):
            return []
        ranked = []
        for channel in self.channels:
            ranked.append({"channel": channel.name, "action": channel.action, "score": self.score(opportunity, channel)})
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[:max(1, limit)]

    def daily_money_mission(self, opportunities: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
        ranked: list[dict[str, Any]] = []
        for opportunity in opportunities:
            for item in self.rank(opportunity, limit=1):
                row = dict(item)
                row["opportunity"] = opportunity
                ranked.append(row)
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[:max(1, limit)]

    def summary(self) -> dict[str, Any]:
        return {"channels": [asdict(channel) for channel in self.channels], "revenue_never_guaranteed": True}
