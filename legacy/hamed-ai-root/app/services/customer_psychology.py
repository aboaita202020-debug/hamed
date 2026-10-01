"""Ethical customer psychology and professional communication engine.

Infers conversation state from explicit language signals only. It is designed to
improve service and communication, not to manipulate, profile protected traits,
or exploit vulnerabilities.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re


@dataclass
class CustomerPsychologyProfile:
    state: str
    confidence: float
    signals: list[str] = field(default_factory=list)
    communication_style: str = "professional"
    objections: list[str] = field(default_factory=list)
    recommended_next_step: str = "clarify_need"


class CustomerPsychologyEngine:
    STATES = ("exploring", "comparing", "interested", "hesitant", "urgent", "ready_to_buy", "needs_support")

    def analyze(self, message: str) -> CustomerPsychologyProfile:
        text = (message or "").strip().lower()
        if not text:
            return CustomerPsychologyProfile("exploring", 0.2, ["empty_message"])

        signals: list[str] = []
        objections: list[str] = []
        scores = {state: 0 for state in self.STATES}

        rules = {
            "urgent": [r"مستعجل", r"النهارده", r"فور[يى]", r"urgent", r"today"],
            "ready_to_buy": [r"عايز اشتري", r"اطلب", r"احجز", r"buy", r"order", r"ready"],
            "hesitant": [r"متردد", r"مش متأكد", r"غالي", r"خايف", r"مقلق", r"expensive", r"not sure"],
            "comparing": [r"قارن", r"بديل", r"غيرك", r"سعر.*شركة", r"compare", r"alternative", r"competitor"],
            "interested": [r"مهتم", r"مناسب", r"ممكن تفاصيل", r"interested", r"details"],
            "needs_support": [r"مشكلة", r"مش شغال", r"شكوى", r"help", r"problem", r"complaint"],
        }
        for state, patterns in rules.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    scores[state] += 1
                    signals.append(f"explicit:{state}")
                    break

        if re.search(r"سعر|تكلفة|price|cost", text):
            objections.append("price")
        if re.search(r"جودة|ضمان|quality|warranty", text):
            objections.append("quality_or_warranty")
        if re.search(r"توصيل|شحن|delivery|shipping", text):
            objections.append("delivery")
        if re.search(r"ثقة|مضمون|موثوق|trust|reliable", text):
            objections.append("trust")

        best = max(scores, key=scores.get)
        if scores[best] == 0:
            best = "exploring"
        confidence = min(0.95, 0.35 + 0.15 * scores[best])
        style = "concise" if best == "urgent" else "reassuring" if best == "hesitant" else "evidence_first" if best == "comparing" else "professional"
        next_step = {
            "urgent": "give_clear_fast_answer",
            "ready_to_buy": "confirm_requirements_and_next_step",
            "hesitant": "address_objections_without_pressure",
            "comparing": "provide_verified_comparison",
            "interested": "clarify_need_and_offer_relevant_option",
            "needs_support": "resolve_issue_then_follow_up",
            "exploring": "ask_one_useful_clarifying_question",
        }[best]
        return CustomerPsychologyProfile(best, confidence, signals, style, objections, next_step)

    def communication_guidance(self, profile: CustomerPsychologyProfile) -> dict:
        return {
            "tone": profile.communication_style,
            "principles": [
                "listen_before_selling",
                "answer_directly",
                "use_verified_facts_only",
                "explain value and tradeoffs",
                "never pressure_or_deceive",
                "respect_opt_out_and_boundaries",
                "identify_as_ai_when_relevant",
            ],
            "next_step": profile.recommended_next_step,
        }
