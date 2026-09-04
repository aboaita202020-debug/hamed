"""Unified revenue planning for Hamed AI.

This module turns commercial ideas into structured, measurable revenue work:
lead hunting, B2B opportunities, affiliate research, digital products,
subscriptions, upsells, referrals, lead recovery, pricing, sourcing,
export, distribution, procurement and agency modes.
It plans and queues work; external actions still require authorized channels.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


REVENUE_MODES = (
    "lead_hunting", "universal_services", "affiliate", "b2b_deals",
    "digital_products", "subscriptions", "upsell", "referrals",
    "lead_recovery", "pricing", "opportunity_hunting", "sales_analytics",
    "agency_growth", "brokerage", "service_reseller", "rfq_hunter",
    "wholesale_arbitrage", "export_hunter", "import_substitute",
    "distributor_finder", "private_label", "bulk_deals", "clearance_hunter",
    "product_validation", "competitor_gap", "quote_comparison",
    "procurement_service", "sales_service", "customer_service",
    "ai_website_agent", "crm_service", "pricing_consulting",
    "inventory_optimizer", "repeat_order", "commission_marketplace",
    "tender_hunter", "market_intelligence", "seasonal_opportunities",
    "digital_services", "reorder_prediction", "deal_packaging",
    "revenue_radar",
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
        modes = ["lead_hunting", "universal_services", "opportunity_hunting", "sales_analytics", "revenue_radar"]
        if any(x in text for x in ("affiliate", "عمولة", "افلييت")):
            modes.append("affiliate")
        if any(x in text for x in ("شركة", "توريد", "b2b", "wholesale", "جملة")):
            modes.extend(["b2b_deals", "procurement_service", "distributor_finder"])
        if any(x in text for x in ("اشتراك", "subscription", "monthly")):
            modes.append("subscriptions")
        if any(x in text for x in ("تصدير", "export", "خارج مصر")):
            modes.append("export_hunter")
        if any(x in text for x in ("مناقصة", "tender", "rfq", "طلب عرض")):
            modes.extend(["tender_hunter", "rfq_hunter"])
        if any(x in text for x in ("مخزون", "inventory", "تصفيات", "clearance")):
            modes.extend(["inventory_optimizer", "clearance_hunter"])
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
            "brokerage": ("Connect verified buyers and sellers for disclosed commission", "match_buyer_seller"),
            "service_reseller": ("Resell verified digital services with transparent margin", "source_service_provider"),
            "rfq_hunter": ("Find public requests for quotation and prepare truthful responses", "research_public_rfq"),
            "wholesale_arbitrage": ("Compare lawful wholesale and resale prices for margin opportunities", "compare_market_prices"),
            "export_hunter": ("Find qualified overseas demand for suitable local products", "research_export_buyers"),
            "import_substitute": ("Find local alternatives to imported products", "research_local_alternatives"),
            "distributor_finder": ("Find suitable distributors and agents for a product", "research_distributors"),
            "private_label": ("Validate products suitable for a private-label offer", "validate_private_label"),
            "bulk_deals": ("Aggregate compatible demand to seek better wholesale terms", "aggregate_demand"),
            "clearance_hunter": ("Find lawful clearance or surplus inventory opportunities", "research_clearance_stock"),
            "product_validation": ("Validate demand before committing capital to inventory", "validate_product_demand"),
            "competitor_gap": ("Identify observable competitor gaps that can become better offers", "analyze_competitor_gaps"),
            "quote_comparison": ("Compare supplier quotations and total landed cost", "compare_supplier_quotes"),
            "procurement_service": ("Offer procurement research and supplier comparison to businesses", "build_procurement_plan"),
            "sales_service": ("Offer Hamed as a sales service for qualified businesses", "build_sales_service_plan"),
            "customer_service": ("Offer customer-support and follow-up automation to businesses", "build_support_service_plan"),
            "ai_website_agent": ("Offer a website AI sales agent to businesses", "build_ai_website_offer"),
            "crm_service": ("Offer CRM setup, organization and follow-up services", "build_crm_service_plan"),
            "pricing_consulting": ("Improve pricing using verified cost and market inputs", "audit_pricing"),
            "inventory_optimizer": ("Find slow-moving inventory and evidence-backed disposal or promotion paths", "analyze_inventory"),
            "repeat_order": ("Predict and support legitimate repeat orders from known customer history", "prepare_reorder"),
            "commission_marketplace": ("Match businesses with disclosed commission-based commercial partners", "match_commission_partners"),
            "tender_hunter": ("Monitor public tenders and identify relevant opportunities", "research_public_tenders"),
            "market_intelligence": ("Create evidence-backed market, competitor and pricing reports", "build_market_report"),
            "seasonal_opportunities": ("Find seasonal demand before the demand peak", "research_seasonal_demand"),
            "digital_services": ("Package lawful digital, marketing, automation and AI services", "build_digital_service_package"),
            "reorder_prediction": ("Estimate reorder timing from actual customer/order history", "predict_reorder_timing"),
            "deal_packaging": ("Bundle complementary products or services into useful packages", "build_value_bundle"),
            "revenue_radar": ("Rank all evidence-backed revenue opportunities by expected value and effort", "rank_revenue_opportunities"),
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

    def rank_opportunities(self, opportunities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Rank opportunities using evidence, customer fit, value and effort; never invent missing values."""
        ranked = []
        for item in opportunities:
            score = self.score_opportunity(
                evidence_count=int(item.get("evidence_count", 0)),
                customer_fit=float(item.get("customer_fit", 0.0)),
                estimated_value=float(item.get("estimated_value", 0.0)),
            )
            effort = max(1.0, float(item.get("effort", 1.0)))
            risk = max(0.0, min(1.0, float(item.get("risk", 0.0))))
            item = dict(item)
            item["score"] = round(score * (1.0 - 0.25 * risk) / effort * min(effort, 10.0), 2)
            ranked.append(item)
        return sorted(ranked, key=lambda x: x["score"], reverse=True)

    def client_growth_mode(self, *, goal: str, platforms: list[str] | None = None) -> dict[str, Any]:
        return {
            "goal": goal,
            "platforms": platforms or [],
            "steps": ["audit", "define_audience", "content_strategy", "distribution", "lead_generation", "conversion", "analytics", "iteration"],
            "sell_what_is_needed": True,
            "approval_required_for_external_actions": True,
        }
