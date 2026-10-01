"""Revenue Compiler: choose a legitimate monetization model for a validated opportunity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class RevenueOption:
    model: str
    fit_score: float
    rationale: str
    pricing_basis: str
    approval_required: bool = False

class RevenueCompiler:
    MODELS = ("subscription", "success_fee", "pay_per_result", "project_fee", "referral_fee", "licensing", "usage_based")

    def compile(self, opportunity: dict[str, Any]) -> dict[str, Any]:
        evidence = list(opportunity.get("evidence") or [])
        if not evidence:
            return {"status": "needs_validation", "options": [], "reason": "revenue_model_requires_evidence"}
        recurring = bool(opportunity.get("recurring_value"))
        measurable = bool(opportunity.get("measurable_outcome"))
        partner = bool(opportunity.get("partner_referral"))
        scalable = bool(opportunity.get("scalable"))
        options: list[RevenueOption] = []
        if recurring:
            options.append(RevenueOption("subscription", 90, "Recurring customer value supports recurring pricing.", "verified_scope_and_service_level"))
        if measurable:
            options.append(RevenueOption("pay_per_result", 88, "A measurable outcome can support performance-based pricing.", "verified_result_definition"))
            options.append(RevenueOption("success_fee", 82, "A completed transaction or outcome can support a success fee.", "verified_transaction_value", True))
        if partner:
            options.append(RevenueOption("referral_fee", 76, "A disclosed partner relationship can support a referral fee.", "partner_agreement", True))
        if scalable:
            options.append(RevenueOption("licensing", 72, "A repeatable product can be licensed.", "license_scope_and_terms", True))
        options.append(RevenueOption("project_fee", 65, "A defined deliverable can be sold as a project.", "verified_deliverables"))
        options.append(RevenueOption("usage_based", 60, "Usage can be metered when the unit of consumption is measurable.", "verified_usage_unit"))
        options.sort(key=lambda x: x.fit_score, reverse=True)
        return {
            "status": "compiled",
            "recommended": options[0].model,
            "options": [o.__dict__ for o in options],
            "evidence": evidence,
            "no_guaranteed_revenue": True,
            "approval_boundary": "major_financial_commitments_require_authorization",
        }
