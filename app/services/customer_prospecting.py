"""Evidence-first prospecting for lawful, personalized commercial outreach."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProspectAssessment:
    qualified: bool
    opportunity_type: str
    evidence: tuple[str, ...]
    observed_needs: tuple[str, ...]
    recommended_service: str | None
    outreach_allowed: bool
    reason: str


class CustomerProspectingEngine:
    """Turn public/authorized business evidence into a conservative sales lead."""

    DIGITAL_GAP_TERMS = (
        "no website", "without website", "doesn't have a website", "no store",
        "without online store", "doesn't have an online store", "no ecommerce",
        "مفيش موقع", "معندوش موقع", "ما عندوش موقع", "بدون موقع",
        "مفيش متجر", "معندوش متجر", "ما عندوش متجر", "بدون متجر", "متجر إلكتروني",
    )

    def assess(self, evidence: dict[str, Any]) -> ProspectAssessment:
        public_evidence = tuple(str(x) for x in (evidence.get("evidence") or []) if str(x).strip())
        text = " ".join(str(evidence.get(k) or "") for k in ("bio", "post", "about", "website", "store"))
        lowered = text.lower()
        has_digital_gap = any(term in lowered for term in self.DIGITAL_GAP_TERMS)
        needs = [str(x) for x in (evidence.get("needs") or []) if str(x).strip()]
        if has_digital_gap:
            needs.append("digital storefront")
        if not public_evidence:
            return ProspectAssessment(False, "unknown", (), tuple(dict.fromkeys(needs)), None, False, "missing public evidence")
        if has_digital_gap:
            return ProspectAssessment(
                True,
                "digital_presence_gap",
                public_evidence,
                tuple(dict.fromkeys(needs)),
                "website_or_ecommerce_store",
                True,
                "observable public evidence indicates a digital presence gap",
            )
        if evidence.get("explicit_buying_need"):
            return ProspectAssessment(True, "buying_need", public_evidence, tuple(dict.fromkeys(needs)), "matching_offer", True, "explicit buying need")
        return ProspectAssessment(False, "nurture", public_evidence, tuple(dict.fromkeys(needs)), None, False, "no sufficiently specific commercial need")

    def build_outreach(self, *, name: str, assessment: ProspectAssessment) -> dict[str, Any]:
        if not assessment.outreach_allowed:
            return {"approved": False, "message": "", "reason": assessment.reason}
        if assessment.opportunity_type == "digital_presence_gap":
            message = (
                f"أهلًا {name}، لاحظت من المعلومات العامة عن نشاطك إن وجودك الرقمي ممكن يتطور، "
                "خصوصًا لو محتاج موقع أو متجر إلكتروني. إحنا بنصمم ونطوّر الحل كاملًا حسب طبيعة النشاط. "
                "لو حابب، أقدر أبعث لك تصور مختصر مناسب لنشاطك من غير التزام."
            )
        else:
            message = f"أهلًا {name}، لاحظت احتياجًا واضحًا في المعلومات العامة المتاحة. أقدر أشاركك حلًا محددًا بناءً على الاحتياج الفعلي، لو مناسب لك."
        return {
            "approved": True,
            "message": message,
            "evidence": list(assessment.evidence),
            "opportunity_type": assessment.opportunity_type,
            "recommended_service": assessment.recommended_service,
        }
