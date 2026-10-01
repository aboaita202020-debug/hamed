from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class RevenueEngine:
    key: str
    name: str
    models: list[str]

ENGINES = [
 RevenueEngine("quote_sniper","Quote Sniper",["project_fee","success_fee"]),
 RevenueEngine("deal_rescue","Deal Rescue",["project_fee","success_fee"]),
 RevenueEngine("negotiation_optimizer","Negotiation Optimizer",["project_fee","subscription"]),
 RevenueEngine("margin_guardian","Margin Guardian",["subscription","usage_based"]),
 RevenueEngine("cashflow_forecaster","Cashflow Forecaster",["subscription","report_fee"]),
 RevenueEngine("renewal_hunter","Renewal Hunter",["subscription","success_fee"]),
 RevenueEngine("referral_engine","Referral Engine",["referral_fee","subscription"]),
 RevenueEngine("bundle_profit","Bundle Profit Engine",["project_fee","subscription"]),
 RevenueEngine("vendor_replacement","Vendor Replacement Hunter",["project_fee","success_fee"]),
 RevenueEngine("procurement_intelligence","Procurement Intelligence",["subscription","project_fee"]),
 RevenueEngine("private_buyer_network","Private Buyer Network",["subscription","membership_fee"]),
 RevenueEngine("strategic_account_hunter","Strategic Account Hunter",["project_fee","success_fee"]),
 RevenueEngine("contract_expansion","Contract Expansion Engine",["subscription","success_fee"]),
 RevenueEngine("supplier_risk_radar","Supplier Risk Radar",["subscription","report_fee"]),
 RevenueEngine("egypt_gulf_gap","Egypt-Gulf Gap Finder",["report_fee","brokerage_fee"]),
 RevenueEngine("arab_market_entry","Arab Market Entry Engine",["project_fee","retainer"]),
 RevenueEngine("distributor_deal_builder","Distributor Deal Builder",["project_fee","commission"]),
 RevenueEngine("export_compliance_precheck","Export Compliance Precheck",["audit_fee","project_fee"]),
 RevenueEngine("trade_route_optimizer","Trade Route Optimizer",["report_fee","subscription"]),
 RevenueEngine("private_label_hunter","Private Label Hunter",["brokerage_fee","project_fee"]),
 RevenueEngine("hamed_as_a_service","Hamed-as-a-Service",["subscription","usage_based"]),
 RevenueEngine("white_label_hamed","White-Label Hamed",["licensing","subscription"]),
 RevenueEngine("ai_department_builder","AI Department Builder",["setup_fee","subscription"]),
 RevenueEngine("ai_workforce_marketplace","AI Workforce Marketplace",["usage_based","subscription"]),
 RevenueEngine("agent_subscription_factory","Agent Subscription Factory",["subscription","usage_based"]),
 RevenueEngine("custom_brain_factory","Custom Brain Factory",["setup_fee","licensing"]),
 RevenueEngine("competitor_warning","Competitor Early-Warning",["subscription","report_fee"]),
 RevenueEngine("demand_forecast","Demand Forecast Engine",["subscription","report_fee"]),
 RevenueEngine("price_anomaly","Price Anomaly Hunter",["subscription","report_fee"]),
 RevenueEngine("market_whitespace","Market White-Space Radar",["subscription","report_fee"]),
 RevenueEngine("trend_to_money","Trend-to-Money Engine",["project_fee","subscription"]),
 RevenueEngine("portfolio_optimizer","Opportunity Portfolio Optimizer",["subscription","advisory_fee"]),
 RevenueEngine("revenue_kill_switch","Revenue Kill Switch",["subscription","usage_based"]),
 RevenueEngine("opportunity_factory","Hamed Opportunity Factory",["subscription","usage_based"]),
]

class RevenueExpansionSuite:
    def catalog(self) -> list[dict[str, Any]]:
        return [asdict(x) for x in ENGINES]

    def evaluate(self, opportunity: dict[str, Any]) -> dict[str, Any]:
        evidence = list(opportunity.get("evidence") or [])
        if not evidence:
            return {"status":"needs_validation","reason":"evidence_required","engines":self.catalog()}
        signal = str(opportunity.get("signal") or opportunity.get("problem") or "").strip()
        if not signal:
            return {"status":"needs_input","reason":"missing_opportunity_signal"}
        matches = self._match(signal)
        return {"status":"evaluated","signal":signal,"matched_engines":[asdict(x) for x in matches],"opportunity_factory_loop":["signal","verify","score","test","first_customer","measure","learn","scale_or_kill"],"kill_switch_rule":"stop_or_reduce a channel when verified economics fail configured thresholds; preserve evidence and learning","approval_boundary":"payments_contracts_binding_commitments_regulated_actions_and_irreversible_high_impact_actions_require_authorization","no_guaranteed_revenue":True}

    def _match(self, signal: str) -> list[RevenueEngine]:
        s = signal.lower()
        groups = {
            "quote_sniper":["quote","rfq","عرض سعر"],"deal_rescue":["stuck","متوقفة","صفقة"],"negotiation_optimizer":["negotiat","تفاوض"],"margin_guardian":["margin","هامش","ربح"],"cashflow_forecaster":["cashflow","سيولة","تدفق نقدي"],"renewal_hunter":["renewal","تجديد"],"referral_engine":["referral","إحالة"],"bundle_profit":["bundle","باقة"],"vendor_replacement":["vendor","مورد بديل"],"procurement_intelligence":["procurement","مشتريات"],"private_buyer_network":["buyer","مشتري"],"strategic_account_hunter":["enterprise","شركة كبيرة"],"contract_expansion":["contract","عقد"],"supplier_risk_radar":["supplier risk","مخاطر المورد"],"egypt_gulf_gap":["egypt gulf","مصر الخليج"],"arab_market_entry":["market entry","دخول السوق"],"distributor_deal_builder":["distributor","موزع"],"export_compliance_precheck":["export compliance","امتثال التصدير"],"trade_route_optimizer":["shipping route","مسار الشحن"],"private_label_hunter":["private label","علامة خاصة"],"hamed_as_a_service":["hamed as a service","حامد كخدمة"],"white_label_hamed":["white label"],"ai_department_builder":["ai department","قسم ذكاء اصطناعي"],"ai_workforce_marketplace":["ai workforce","موظفين ai"],"agent_subscription_factory":["agent subscription","اشتراك agent"],"custom_brain_factory":["custom brain","عقل متخصص"],"competitor_warning":["competitor","منافس"],"demand_forecast":["forecast","توقع الطلب"],"price_anomaly":["price anomaly","سعر شاذ"],"market_whitespace":["white-space","فجوة سوق"],"trend_to_money":["trend","ترند"],"portfolio_optimizer":["portfolio","محفظة الفرص"]}
        return [e for e in ENGINES if any(k in s for k in groups.get(e.key, []))] or [next(e for e in ENGINES if e.key == "opportunity_factory")]
