"""Freelance Revenue Engine: discover, qualify and monetize freelance opportunities."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class FreelanceOpportunity:
    title: str
    category: str
    fit_score: int
    suggested_model: str
    next_actions: list[str]

class FreelanceRevenueEngine:
    CATEGORIES = ("websites", "ecommerce", "marketing", "content", "video", "seo", "lead_generation", "automation", "ai_agents", "research", "sales", "procurement", "data", "translation")

    def qualify(self, request: dict[str, Any]) -> dict[str, Any]:
        title = str(request.get("title") or request.get("request") or "freelance opportunity").strip()
        if not title:
            return {"status": "needs_input", "reason": "missing_project_description"}
        evidence = list(request.get("evidence") or [])
        if not evidence:
            return {"status": "needs_validation", "reason": "freelance_opportunity_requires_verifiable_project_evidence"}
        category = str(request.get("category") or "general").lower()
        fit = 50
        if category in self.CATEGORIES: fit += 25
        if request.get("budget_known"): fit += 10
        if request.get("deadline_known"): fit += 5
        if request.get("deliverables_clear"): fit += 10
        model = "project_fee" if request.get("deliverables_clear", True) else "milestone"
        opportunity = FreelanceOpportunity(title, category, min(fit, 100), model, ["verify_scope", "prepare_proposal", "price_with_margin", "outreach_or_submit", "deliver_and_verify", "measure_profit"])
        return {"status": "qualified", "opportunity": asdict(opportunity), "evidence": evidence, "approval_boundary": "binding_contracts_and_material_financial_commitments_require_authorization", "no_guaranteed_income": True}
