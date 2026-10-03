"""Twenty additional revenue engines and a unified Opportunity Graph."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class RevenueEngine:
    key: str
    name: str
    monetization: tuple[str, ...]

ENGINES = [
RevenueEngine("tender_hunter","Tender Hunter",("submission_fee","project_fee")),
RevenueEngine("rfp_factory","RFP Response Factory",("proposal_fee","project_fee")),
RevenueEngine("b2b_retainer_hunter","B2B Retainer Hunter",("subscription",)),
RevenueEngine("corporate_vendor_hunter","Corporate Vendor Hunter",("supplier_fee","project_fee")),
RevenueEngine("distributor_network_builder","Distributor Network Builder",("setup_fee","commission")),
RevenueEngine("partnership_hunter","Partnership Hunter",("referral_fee","success_fee")),
RevenueEngine("business_rescue","Business Rescue Engine",("audit_fee","project_fee","retainer")),
RevenueEngine("churn_prevention","Churn Prevention Engine",("subscription","retainer")),
RevenueEngine("customer_ltv","Customer Lifetime Value Engine",("subscription","success_fee")),
RevenueEngine("inventory_to_cash","Inventory-to-Cash Engine",("project_fee","commission")),
RevenueEngine("capacity_to_cash","Capacity-to-Cash Engine",("brokerage_fee","commission")),
RevenueEngine("cross_border_gap","Cross-Border Gap Hunter",("brokerage_fee","distribution_margin")),
RevenueEngine("product_licensing","Product Licensing Hunter",("licensing_fee","commission")),
RevenueEngine("knowledge_to_product","Knowledge-to-Product Engine",("product_sales","subscription","licensing")),
RevenueEngine("data_to_product","Data-to-Product Engine",("report_sales","subscription","licensing")),
RevenueEngine("local_monopoly_finder","Local Monopoly Finder",("market_report","project_fee")),
RevenueEngine("emergency_demand","Emergency Demand Engine",("brokerage_fee","success_fee")),
RevenueEngine("service_arbitrage","Service Arbitrage Engine",("project_margin","retainer")),
RevenueEngine("problem_to_business","Problem-to-Business Engine",("project_fee","subscription","licensing")),
RevenueEngine("opportunity_graph","Hamed Opportunity Graph",("subscription","brokerage_fee","licensing")),
]

class RevenueOpportunitySuite:
    def catalog(self) -> list[dict[str, Any]]:
        return [asdict(e) for e in ENGINES]

    def evaluate(self, opportunity: dict[str, Any]) -> dict[str, Any]:
        evidence = list(opportunity.get("evidence") or [])
        if not evidence:
            return {"status":"needs_validation","reason":"evidence_required","engines":self.catalog()}
        signal = str(opportunity.get("signal") or opportunity.get("problem") or "").strip()
        if not signal:
            return {"status":"needs_input","reason":"missing_opportunity_signal"}
        s = signal.lower()
        groups = {
          "tender_hunter":["tender","مناقصة","rfp"],"rfp_factory":["proposal","عرض فني","rfp"],
          "b2b_retainer_hunter":["monthly","retainer","اشتراك","شهري"],"corporate_vendor_hunter":["vendor","مورد","supplier"],
          "distributor_network_builder":["distributor","موزع","وكيل"],"partnership_hunter":["partner","شراكة"],
          "business_rescue":["sales problem","مبيعات ضعيفة","خسارة"],"churn_prevention":["churn","ترك العملاء","إلغاء"],
          "customer_ltv":["upsell","cross-sell","renewal","تجديد"],"inventory_to_cash":["inventory","مخزون راكد","تصريف"],
          "capacity_to_cash":["capacity","طاقة غير مستغلة","وقت فارغ"],"cross_border_gap":["export","import","تصدير","استيراد"],
          "product_licensing":["license","ترخيص","licensing"],"knowledge_to_product":["course","كورس","خبرة","كتاب"],
          "data_to_product":["data","بيانات","report","تقرير"],"local_monopoly_finder":["local","محلي","منطقة"],
          "emergency_demand":["urgent","عاجل","emergency","فوري"],"service_arbitrage":["service","خدمة","provider"],
          "problem_to_business":["problem","مشكلة","gap","فجوة"]}
        matches=[e for e in ENGINES if e.key != "opportunity_graph" and any(k in s for k in groups.get(e.key,[]))]
        return {"status":"evaluated","signal":signal,"matched_engines":[asdict(e) for e in (matches or [ENGINES[-1]])],"opportunity_graph":{"nodes":["customer","problem","product","supplier","distributor","service","partner","market","country","sales_channel","revenue_model"],"rule":"connect nodes only when supported by evidence"},"pipeline":["discover","verify","score","package","price","find_buyer","personalized_outreach","negotiate","approval_gate","deliver","verify_outcome","attribute_revenue","measure_profit","reinvest"],"approval_boundary":"contracts_payments_binding_commitments_regulated_activity_and_irreversible_high_impact_actions_require_authorization"}
