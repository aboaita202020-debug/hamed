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
    # Revenue expansion engines: each is a decision path, not a promise of income.
    "cross_border", "demand_predictor", "supplier_negotiator", "bulk_buyer",
    "white_label_finder", "distributor_network", "commission_finder",
    "corporate_accounts", "recurring_revenue", "unused_capacity_hunter",
    "dead_stock_exchange", "bundle_optimizer", "churn_predictor",
    "referral_network", "revenue_experiments", "profit_leak_detector",
    "opportunity_portfolio", "daily_revenue_target", "revenue_brain",
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
        modes = ["lead_hunting", "universal_services", "opportunity_hunting", "sales_analytics", "revenue_radar", "revenue_brain"]
        if any(x in text for x in ("affiliate", "عمولة", "افلييت")):
            modes.extend(["affiliate", "commission_finder", "commission_marketplace"])
        if any(x in text for x in ("شركة", "توريد", "b2b", "wholesale", "جملة")):
            modes.extend(["b2b_deals", "procurement_service", "distributor_finder", "corporate_accounts"])
        if any(x in text for x in ("اشتراك", "subscription", "monthly", "شهري")):
            modes.extend(["subscriptions", "recurring_revenue", "churn_predictor"])
        if any(x in text for x in ("تصدير", "export", "خارج مصر", "دولي", "international")):
            modes.append("export_hunter")
            modes.append("cross_border")
        if any(x in text for x in ("مناقصة", "tender", "rfq", "طلب عرض")):
            modes.extend(["tender_hunter", "rfq_hunter"])
        if any(x in text for x in ("مخزون", "inventory", "تصفيات", "clearance", "راكد")):
            modes.extend(["inventory_optimizer", "clearance_hunter", "dead_stock_exchange"])
        if any(x in text for x in ("مصنع", "factory", "طاقة", "capacity")):
            modes.append("unused_capacity_hunter")
        if any(x in text for x in ("منتج", "product", "طلب", "demand")):
            modes.extend(["product_validation", "demand_predictor", "bulk_buyer", "white_label_finder"])
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
            "cross_border": ("Match verified cross-border demand and supply with trade constraints visible", "research_cross_border_trade"),
            "demand_predictor": ("Estimate demand signals from observed evidence before committing resources", "predict_demand"),
            "supplier_negotiator": ("Prepare evidence-based supplier negotiation targets and alternatives", "prepare_supplier_negotiation"),
            "bulk_buyer": ("Aggregate compatible demand to unlock legitimate volume economics", "build_bulk_buying_plan"),
            "white_label_finder": ("Find and validate private-label/white-label supply options", "research_white_label_supply"),
            "distributor_network": ("Build a verified distributor and agent network by market", "map_distributor_network"),
            "commission_finder": ("Find transparent commission/referral opportunities that fit Hamed's services", "research_commission_opportunities"),
            "corporate_accounts": ("Build recurring B2B account opportunities and procurement relationships", "target_corporate_accounts"),
            "recurring_revenue": ("Convert repeatable customer value into ethical recurring offers", "design_recurring_offer"),
            "unused_capacity_hunter": ("Find verified unused business capacity that can be matched to demand", "research_unused_capacity"),
            "dead_stock_exchange": ("Match verified surplus/dead stock with relevant buyers", "match_dead_stock"),
            "bundle_optimizer": ("Optimize complementary bundles for customer value and margin", "optimize_bundle"),
            "churn_predictor": ("Detect observable churn signals and prepare retention actions", "predict_churn"),
            "referral_network": ("Turn satisfied customers and partners into a disclosed referral network", "grow_referral_network"),
            "revenue_experiments": ("Run measurable low-risk offer, pricing and channel experiments", "run_revenue_experiment"),
            "profit_leak_detector": ("Find margin leakage in pricing, costs, discounts and operations", "detect_profit_leaks"),
            "opportunity_portfolio": ("Balance fast, recurring and high-value opportunities instead of chasing one bet", "build_opportunity_portfolio"),
            "daily_revenue_target": ("Translate a daily revenue target into measurable pipeline requirements", "plan_daily_revenue_target"),
            "revenue_brain": ("Choose the highest expected-return lawful revenue work from the whole opportunity portfolio", "decide_revenue_focus"),
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

    def revenue_brain(self, opportunities: list[dict[str, Any]], *, daily_target: float = 0.0) -> dict[str, Any]:
        """Select a focus from observed opportunities and convert a target into pipeline math.

        Missing values remain unknown. This is a prioritization engine, not a revenue guarantee.
        """
        if daily_target < 0:
            raise ValueError("daily_target must be non-negative")
        ranked = self.rank_opportunities(opportunities)
        focus = ranked[0] if ranked else None
        return {
            "daily_target": daily_target,
            "opportunity_count": len(ranked),
            "focus": focus,
            "portfolio": ranked[:10],
            "next_action": focus.get("next_action") if focus else "collect_evidence",
            "guaranteed_revenue": False,
        }

    def daily_revenue_plan(self, *, target: float, average_deal_value: float | None = None,
                           close_rate: float | None = None) -> dict[str, Any]:
        """Turn a target into required wins/leads when the required inputs are known."""
        if target < 0 or (average_deal_value is not None and average_deal_value <= 0):
            raise ValueError("invalid revenue target inputs")
        if close_rate is not None and not 0 < close_rate <= 1:
            raise ValueError("close_rate must be between 0 and 1")
        deals_needed = None if average_deal_value is None else int((target + average_deal_value - 1) // average_deal_value)
        leads_needed = None if deals_needed is None or close_rate is None else int((deals_needed + close_rate - 1) // close_rate)
        return {"target": target, "average_deal_value": average_deal_value, "close_rate": close_rate,
                "deals_needed": deals_needed, "leads_needed": leads_needed,
                "guaranteed_revenue": False}

    def client_growth_mode(self, *, goal: str, platforms: list[str] | None = None) -> dict[str, Any]:
        return {
            "goal": goal,
            "platforms": platforms or [],
            "steps": ["audit", "define_audience", "content_strategy", "distribution", "lead_generation", "conversion", "analytics", "iteration"],
            "sell_what_is_needed": True,
            "approval_required_for_external_actions": True,
        }
