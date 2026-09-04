"""CEO-level revenue decision engine for Hamed AI."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class RevenueDecision:
    mode: str
    reason: str
    next_action: str
    score: float

class RevenueCEO:
    """Portfolio decision layer above the commercial revenue engines."""
    DEFAULT_MODES = (
        "deal_sniper", "price_arbitrage", "buyer_intent", "quote_auction",
        "smart_commission", "revenue_calendar", "customer_wallet",
        "lost_deal_recovery", "competitor_watcher", "margin_guardian",
        "cashflow_brain", "customer_lifetime_value", "subscription_converter",
        "product_service_converter", "service_product_converter", "deal_factory",
        "b2b_account_hunter", "reorder_radar", "referral_marketplace",
        "revenue_kill_switch",
    )

    def rank(self, opportunities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ranked = []
        for raw in opportunities:
            item = dict(raw)
            evidence = min(1.0, max(0.0, float(item.get("evidence", item.get("evidence_count", 0))) / 5.0))
            fit = min(1.0, max(0.0, float(item.get("fit", item.get("customer_fit", 0.0)))))
            value = min(1.0, max(0.0, float(item.get("value", item.get("estimated_value", 0.0))) / 100000.0))
            speed = min(1.0, max(0.0, float(item.get("speed", 0.5))))
            effort = max(1.0, float(item.get("effort", 1.0)))
            risk = min(1.0, max(0.0, float(item.get("risk", 0.0))))
            item["ceo_score"] = round(100.0 * (0.30 * evidence + 0.25 * fit + 0.20 * value + 0.15 * speed + 0.10 * (1.0 - risk)) / effort, 2)
            item["guaranteed_revenue"] = False
            ranked.append(item)
        return sorted(ranked, key=lambda x: x["ceo_score"], reverse=True)

    def decide(self, opportunities: list[dict[str, Any]], *, daily_target: float = 0.0) -> dict[str, Any]:
        if daily_target < 0:
            raise ValueError("daily_target must be non-negative")
        ranked = self.rank(opportunities)
        focus = ranked[0] if ranked else None
        return {"daily_target": daily_target, "focus": focus, "portfolio": ranked[:10],
                "next_action": focus.get("next_action", "collect_evidence") if focus else "collect_evidence",
                "decision": "focus_highest_scored_observed_opportunity" if focus else "build_evidence_base",
                "guaranteed_revenue": False}

    def guardrails(self) -> dict[str, Any]:
        return {"no_spam": True, "no_deception": True, "no_fabricated_market_data": True,
                "no_unauthorized_payments": True, "no_unauthorized_contracts": True,
                "no_irreversible_actions": True}
