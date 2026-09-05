"""Customer acquisition discovery and qualification engine for Hamed AI."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

HOT_SIGNALS = ("need", "looking for", "wanted", "request", "rfq", "quote", "supplier", "buy", "purchase", "محتاج", "عايز", "مطلوب", "توريد", "شراء", "سعر")

@dataclass(frozen=True)
class LeadSignal:
    source: str
    text: str
    url: str = ""
    contact: str = ""
    evidence: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class LeadAssessment:
    score: float
    temperature: str
    reasons: tuple[str, ...]
    next_action: str

class CustomerAcquisitionEngine:
    """Turns lawful/public demand signals into prioritized acquisition missions.

    It does not scrape private data, bypass platform controls, or send unsolicited
    bulk messages. Outreach must use an authorized channel and respect opt-out.
    """
    def assess(self, signal: LeadSignal) -> LeadAssessment:
        text = signal.text.lower()
        hits = sum(1 for s in HOT_SIGNALS if s.lower() in text)
        score = min(100.0, 25.0 + hits * 10.0)
        if signal.contact:
            score += 10.0
        if signal.evidence:
            score += 10.0
        score = min(100.0, score)
        temperature = "hot" if score >= 70 else "warm" if score >= 45 else "cold"
        next_action = "personalized_outreach" if temperature in {"hot", "warm"} else "nurture_or_research"
        reasons = tuple(["purchase_intent_signal"] if hits else ["fit_signal_only"])
        return LeadAssessment(score, temperature, reasons, next_action)

    def build_mission(self, signal: LeadSignal, offer: str) -> dict[str, Any]:
        assessment = self.assess(signal)
        return {
            "type": "customer_acquisition",
            "source": signal.source,
            "url": signal.url,
            "lead_contact": signal.contact,
            "evidence": signal.evidence or signal.text,
            "offer": offer,
            "score": assessment.score,
            "temperature": assessment.temperature,
            "next_action": assessment.next_action,
            "requires_authorized_channel": True,
            "respect_opt_out": True,
            "no_bulk_spam": True,
        }
