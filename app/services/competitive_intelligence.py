"""Competitive Intelligence Engine for Hamed.

Turns lawful, publicly observable competitor/store signals into structured
findings, gaps, and relevant service opportunities. It never invents evidence
or recommends bypassing access controls.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CompetitorFinding:
    competitor: str
    signal: str
    evidence: str
    impact: str
    confidence: float


@dataclass(frozen=True)
class CompetitiveOpportunity:
    competitor: str
    gap: str
    recommended_service: str
    rationale: str
    next_action: str


class CompetitiveIntelligenceEngine:
    """Analyze public competitor signals and convert gaps into client offers."""

    ALLOWED_SIGNAL_TYPES = (
        "storefront",
        "product",
        "pricing",
        "content",
        "seo",
        "social",
        "customer_experience",
        "offer",
    )

    SERVICE_MAP = {
        "storefront": "Store UX/CRO improvement",
        "product": "Product-page and catalog optimization",
        "pricing": "Pricing and offer optimization",
        "content": "Content and AI-UGC production",
        "seo": "SEO and technical SEO improvement",
        "social": "Social media and growth strategy",
        "customer_experience": "Customer experience improvement",
        "offer": "Offer, positioning and conversion optimization",
    }

    def analyze(self, competitor: str, signals: list[dict[str, Any]]) -> dict[str, Any]:
        findings: list[CompetitorFinding] = []
        opportunities: list[CompetitiveOpportunity] = []

        for raw in signals:
            kind = str(raw.get("type", "")).strip().lower()
            evidence = str(raw.get("evidence", "")).strip()
            signal = str(raw.get("signal", "")).strip()
            if kind not in self.ALLOWED_SIGNAL_TYPES or not signal or not evidence:
                continue

            confidence = float(raw.get("confidence", 0.5))
            confidence = max(0.0, min(1.0, confidence))
            impact = str(raw.get("impact", "needs_validation")).strip() or "needs_validation"
            finding = CompetitorFinding(
                competitor=competitor,
                signal=signal,
                evidence=evidence,
                impact=impact,
                confidence=confidence,
            )
            findings.append(finding)

            if raw.get("gap"):
                gap = str(raw["gap"]).strip()
                opportunities.append(
                    CompetitiveOpportunity(
                        competitor=competitor,
                        gap=gap,
                        recommended_service=self.SERVICE_MAP[kind],
                        rationale=f"Observed {kind} signal: {signal}",
                        next_action="verify_public_evidence_then_prepare_personalized_offer",
                    )
                )

        return {
            "competitor": competitor,
            "findings": [asdict(x) for x in findings],
            "opportunities": [asdict(x) for x in opportunities],
            "evidence_policy": "public_observable_only",
            "workflow": [
                "COLLECT_PUBLIC_SIGNALS",
                "VERIFY_EVIDENCE",
                "ANALYZE_GAPS",
                "MAP_TO_SERVICE",
                "PREPARE_PERSONALIZED_OUTREACH",
                "CRM_TRACK",
                "LEARN_FROM_OUTCOME",
            ],
        }
