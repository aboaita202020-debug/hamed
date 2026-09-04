"""Universal commercial rules for Hamed AI.

Rules are deterministic guardrails. They do not claim a market price exists; prices
must come from verified research or user-supplied evidence.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class CommercialRule:
    category: str
    min_margin_percent: float
    max_margin_percent: float
    strategy: str

class UniversalCommercialEngine:
    """Classify opportunities and calculate a bounded target selling price."""

    RULES = {
        "food": CommercialRule("food", 1.0, 2.0, "high-volume/competitive"),
        "clothing": CommercialRule("clothing", 8.0, 20.0, "brand-and-demand"),
        "electronics": CommercialRule("electronics", 3.0, 10.0, "competitive"),
        "home": CommercialRule("home", 8.0, 20.0, "value-and-market"),
        "beauty": CommercialRule("beauty", 10.0, 30.0, "brand-and-value"),
        "industrial": CommercialRule("industrial", 5.0, 15.0, "volume-and-contract"),
        "services": CommercialRule("services", 20.0, 60.0, "time-and-value"),
        "digital": CommercialRule("digital", 20.0, 70.0, "value-and-delivery"),
        "general": CommercialRule("general", 5.0, 20.0, "market-based"),
    }

    ALIASES = {
        "غذاء":"food", "غذائية":"food", "مواد غذائية":"food", "food":"food",
        "ملابس":"clothing", "ملابس رجالي":"clothing", "ملابس حريمي":"clothing", "clothing":"clothing",
        "الكترونيات":"electronics", "إلكترونيات":"electronics", "electronics":"electronics",
        "منزل":"home", "أثاث":"home", "home":"home",
        "تجميل":"beauty", "مستحضرات":"beauty", "beauty":"beauty",
        "صناعي":"industrial", "صناعية":"industrial", "industrial":"industrial",
        "خدمات":"services", "service":"services", "services":"services",
        "رقمية":"digital", "برمجيات":"digital", "digital":"digital",
    }

    def classify(self, product: str, category: str | None = None) -> str:
        raw = (category or product or "").strip().lower()
        for alias, normalized in self.ALIASES.items():
            if alias.lower() in raw:
                return normalized
        return "general"

    def rule_for(self, product: str, category: str | None = None) -> CommercialRule:
        return self.RULES[self.classify(product, category)]

    def target_price(self, cost: float, *, product: str, category: str | None = None,
                     margin_percent: float | None = None, expenses_per_unit: float = 0.0) -> dict[str, Any]:
        if cost < 0 or expenses_per_unit < 0:
            raise ValueError("cost and expenses must be non-negative")
        rule = self.rule_for(product, category)
        margin = rule.min_margin_percent if margin_percent is None else float(margin_percent)
        if not rule.min_margin_percent <= margin <= rule.max_margin_percent:
            raise ValueError(f"margin must be between {rule.min_margin_percent}% and {rule.max_margin_percent}% for {rule.category}")
        landed = cost + expenses_per_unit
        price = landed * (1 + margin / 100.0)
        return {"category": rule.category, "margin_percent": margin, "cost_per_unit": cost,
                "expenses_per_unit": expenses_per_unit, "landed_cost_per_unit": landed,
                "target_price_per_unit": round(price, 2), "strategy": rule.strategy}

    def opportunity_plan(self, request: dict[str, Any]) -> dict[str, Any]:
        product = str(request.get("product") or request.get("item") or "")
        category = request.get("category")
        rule = self.rule_for(product, category)
        return {"product": product, "category": rule.category,
                "margin_range_percent": [rule.min_margin_percent, rule.max_margin_percent],
                "strategy": rule.strategy,
                "research_required": True,
                "research_targets": ["suppliers", "market_prices", "availability", "delivery_costs", "customer_demand", "competitors"],
                "outreach_allowed_only_with_authorized_channel": True,
                "high_impact_actions_require_approval": True}
