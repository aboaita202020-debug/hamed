"""Unified revenue planning for Hamed AI.

This module turns commercial ideas into structured, measurable revenue work:
lead hunting, B2B opportunities, affiliate research, digital products,
subscriptions, upsells, referrals, lead recovery, pricing and agency mode.
It plans and queues work; external actions still require authorized channels.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


REVENUE_MODES = (
    "lead_hunting", "universal_services", "affiliate", "b2b_deals",
    "digital_products", "subscriptions", "upsell", "referrals",
    "lead_recovery", "pricing", "opportunity_hunting", "sales_analytics",
    "agency_growth",
)


@dataclass(frozen=True)
class RevenueOpportunity:
    mode: str
    title: str
    next_action: str
    evidence_required: bool = True
    approval_required: bool = False


class RevenueHub:
    """Central commercial engine used to discover and grow legitimate revenue."""

    def discover_modes(self, customer_or_market: dict[str, Any] | None = None) -> list[str]:
        """Return revenue modes relevant to supplied context without inventing facts."""
        data = customer_or_market or {}
        text = " ".join(str(v) for v in data.values()).lower()
        modes = ["lead_hunting", "universal_services", "opportunity_hunting", "sales_analytics"]
        if any(x in text for x in ("affiliate", "عمولة", "افلييت")):
            modes.append("affiliate")
        if any(x in text for x in ("شركة", "توريد", "b2b", "wholesale", "جملة")):
            modes.append("b2b_deals")
        if any(x in text for x in ("اشتراك", "subscription", "monthly")):
            modes.append("subscriptions")
        return list(dict.fromkeys(modes))

    def build_pipeline(self, *, modes: list[str] | None = None) -> list[RevenueOpportunity]:
        selected = modes or list(REVENUE_MODES)
        invalid = [m for m in selected if m not in REVENUE_MODES]
        if invalid:
            raise ValueError(f"unsupported revenue mode: {invalid[0]}")
        actions = {
            "lead_hunting": ("Find qualified demand with evidence", "research_public_demand"),
            "universal_services": ("Sell the best lawful service for the customer's need", "qualify_and_offer"),
            "affiliate": ("Find relevant affiliate programs and track conversions", "research_affiliate_programs"),
            "b2b_deals": ("Find verified buyers and suppliers for a commercial deal", "research_b2b_demand"),
            "digital_products": ("Identify a useful repeatable digital product", "validate_digital_product"),
            "subscriptions": ("Turn repeatable value into a recurring service", "design_subscription"),
            "upsell": ("Find the next useful offer for an existing customer", "analyze_customer_history"),
            "referrals": ("Create a referral opportunity from satisfied customers", "prepare_referral_offer"),
            "lead_recovery": ("Re-engage qualified inactive leads without spam", "prepare_contextual_follow_up"),
            "pricing": ("Calculate cost, price, margin and risk from known inputs", "calculate_quote"),
            "opportunity_hunting": ("Continuously scan for evidence-backed opportunities", "run_opportunity_cycle"),
            "sales_analytics": ("Measure conversion, revenue and reasons for wins/losses", "analyze_sales_funnel"),
            "agency_growth": ("Diagnose a client's growth goal and sell the right package", "build_client_growth_plan"),
        }
        return [RevenueOpportunity(m, actions[m][0], actions[m][1]) for m in selected]

    def score_opportunity(self, *, evidence_count: int, customer_fit: float, estimated_value: float = 0.0) -> float:
        if evidence_count < 0 or estimated_value < 0 or not 0 <= customer_fit <= 1:
            raise ValueError("invalid opportunity inputs")
        evidence_score = min(1.0, evidence_count / 5.0)
        value_score = min(1.0, estimated_value / 100000.0)
        return round(100 * (0.45 * evidence_score + 0.4 * customer_fit + 0.15 * value_score), 2)

    def calculate_price(self, *, cost: float, expenses: float = 0.0, margin: float = 0.0) -> dict[str, float]:
        if cost < 0 or expenses < 0 or not 0 <= margin < 1:
            raise ValueError("invalid pricing inputs")
        base = cost + expenses
        price = base / (1 - margin) if margin else base
        return {"cost": cost, "expenses": expenses, "margin": margin, "price": round(price, 2), "gross_profit": round(price - base, 2)}

    def recommend_next_offer(self, customer: dict[str, Any]) -> dict[str, Any]:
        history = customer.get("purchase_history") or []
        interests = customer.get("interests") or []
        if not history and not interests:
            return {"recommended": False, "reason": "insufficient customer context"}
        return {"recommended": True, "basis": "existing customer context", "next_action": "prepare_relevant_upsell", "approval_required": False}

    def recover_lead(self, lead: dict[str, Any]) -> dict[str, Any]:
        if not lead.get("last_need") and not lead.get("last_interaction"):
            return {"ready": False, "reason": "missing context"}
        return {"ready": True, "strategy": "contextual_non_spam_follow_up", "approval_required": False}

    def client_growth_mode(self, *, goal: str, platforms: list[str] | None = None) -> dict[str, Any]:
        return {
            "goal": goal,
            "platforms": platforms or [],
            "steps": ["audit", "define_audience", "content_strategy", "distribution", "lead_generation", "conversion", "analytics", "iteration"],
            "sell_what_is_needed": True,
            "approval_required_for_external_actions": True,
        }
