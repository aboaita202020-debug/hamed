"""Universal Human Opportunity Engine.

Treats every legitimate interaction as a potential business opportunity while
keeping evidence, consent, anti-spam, and approval boundaries explicit.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HumanOpportunity:
    subject_id: str
    signal: str
    role_candidates: list[str] = field(default_factory=list)
    intent: str = "unknown"
    need: str = ""
    evidence: list[str] = field(default_factory=list)
    fit_score: float = 0.0
    opportunity_score: float = 0.0
    recommended_agents: list[str] = field(default_factory=list)
    recommended_offers: list[str] = field(default_factory=list)
    allowed_channels: list[str] = field(default_factory=list)
    status: str = "discovery_only"
    approval_required: bool = False
    opt_out: bool = False


class UniversalHumanOpportunityEngine:
    ROLES = [
        "prospect", "buyer", "seller", "supplier", "partner", "referrer",
        "provider", "creator", "investor", "previous_customer", "inactive_customer",
    ]

    INTENT_KEYWORDS = {
        "buy": ("buy", "purchase", "عايز اشتري", "شراء", "محتاج منتج", "عاوز منتج"),
        "sell": ("sell", "بيع", "عايز ابيع", "عاوز ابيع"),
        "service": ("service", "خدمة", "محتاج خدمة", "عايز خدمة", "نفذ"),
        "marketing": ("marketing", "تسويق", "اعلان", "حملة", "فيديو", "مبيعات"),
        "problem": ("problem", "مشكلة", "مش شغال", "محتاج حل", "حل"),
        "partnership": ("partner", "شراكة", "تعاون", "موزع", "وكيل"),
        "supplier": ("supplier", "مورد", "توريد", "مصنع", "quotation", "rfq"),
    }

    ROUTES = {
        "buy": ["customer_conversation_agent", "customer_acquisition_agent", "purchasing_agent", "negotiation_agent"],
        "sell": ["sales_agent", "offer_compiler_agent", "customer_acquisition_agent"],
        "service": ["customer_conversation_agent", "service_compiler_agent", "offer_compiler_agent"],
        "marketing": ["marketing_campaign_agent", "video_commerce_agent", "offer_compiler_agent"],
        "problem": ["customer_conversation_agent", "service_compiler_agent", "business_opportunity_factory_agent"],
        "partnership": ["revenue_opportunity_suite_agent", "revenue_compiler_agent", "negotiation_agent"],
        "supplier": ["purchasing_agent", "negotiation_agent", "revenue_opportunity_suite_agent"],
        "unknown": ["customer_conversation_agent", "customer_acquisition_agent"],
    }

    def classify_intent(self, signal: str) -> str:
        text = (signal or "").lower()
        scores = {intent: sum(1 for k in keys if k in text) for intent, keys in self.INTENT_KEYWORDS.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] else "unknown"

    def assess(self, payload: dict[str, Any]) -> HumanOpportunity:
        subject_id = str(payload.get("subject_id") or payload.get("contact_id") or "anonymous")
        signal = str(payload.get("signal") or payload.get("message") or "").strip()
        evidence = [str(x) for x in (payload.get("evidence") or []) if str(x).strip()]
        channels = [str(x) for x in (payload.get("allowed_channels") or []) if str(x).strip()]
        opt_out = bool(payload.get("opt_out", False))
        intent = self.classify_intent(signal)
        role_candidates = list(payload.get("roles") or [])
        if not role_candidates:
            role_candidates = ["prospect"]
            if intent == "buy": role_candidates += ["buyer"]
            if intent == "sell": role_candidates += ["seller"]
            if intent == "supplier": role_candidates += ["supplier"]
            if intent == "partnership": role_candidates += ["partner"]
        role_candidates = [r for r in role_candidates if r in self.ROLES] or ["prospect"]
        need = str(payload.get("need") or signal).strip()
        fit = min(100.0, 25.0 + 15.0 * len(evidence) + (20.0 if intent != "unknown" else 0.0))
        opportunity = min(100.0, fit + (15.0 if channels else 0.0) + (10.0 if payload.get("business_context") else 0.0))
        status = "opted_out" if opt_out else ("needs_validation" if not evidence else "opportunity")
        approval = intent in {"buy", "sell", "supplier", "partnership"}
        return HumanOpportunity(
            subject_id=subject_id, signal=signal, role_candidates=role_candidates,
            intent=intent, need=need, evidence=evidence, fit_score=fit,
            opportunity_score=opportunity, recommended_agents=self.ROUTES[intent],
            recommended_offers=list(payload.get("recommended_offers") or []),
            allowed_channels=channels, status=status, approval_required=approval,
            opt_out=opt_out,
        )

    def next_actions(self, opportunity: HumanOpportunity) -> list[str]:
        if opportunity.opt_out:
            return ["stop_contact"]
        if not opportunity.signal:
            return ["collect_signal"]
        if not opportunity.evidence:
            return ["verify_evidence", "discover_need"]
        return ["route_to_best_agent", "compile_offer", "execute_low_risk", "verify_result", "measure_outcome"]

    def evaluate(self, payload: dict[str, Any]) -> dict[str, Any]:
        opportunity = self.assess(payload)
        return {
            "opportunity_created": bool(opportunity.signal) and not opportunity.opt_out,
            "opportunity": opportunity.__dict__,
            "next_actions": self.next_actions(opportunity),
            "autonomous_low_risk_execution": not opportunity.approval_required and not opportunity.opt_out,
            "approval_boundary": "Required for payments, binding contracts, regulated/high-impact actions, or irreversible commitments.",
            "privacy_boundary": "Use only lawful public/consented/permitted contact data and official channels; never bulk-spam or bypass platform controls.",
            "truth_boundary": "Do not invent identity, need, price, inventory, supplier/customer facts, results, or completed actions.",
        }
