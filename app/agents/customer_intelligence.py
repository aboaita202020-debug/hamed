"""Customer intelligence layer for natural, ethical customer conversations.

This module infers only observable conversational signals. It does not diagnose
mental-health conditions or infer sensitive traits. Its purpose is to help Hamed
understand intent, needs, objections and preferred communication style before
composing a response.
"""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CustomerSignals:
    intent: str
    stage: str
    needs: tuple[str, ...]
    objections: tuple[str, ...]
    tone: str
    urgency: str


class CustomerIntelligence:
    """Lightweight, deterministic signals that can be safely injected into prompts."""

    def analyze(self, text: str) -> CustomerSignals:
        t = text.lower().strip()
        needs: list[str] = []
        objections: list[str] = []

        if re.search(r"\b(سعر|تكلفة|بكام|كام|price|cost|budget)\b", t):
            needs.append("clear pricing/value explanation")
        if any(x in t for x in ("عاوز", "اريد", "محتاج", "ممكن تعمل", "أريد", "need", "want", "can you")):
            needs.append("concrete solution and next step")
        if any(x in t for x in ("مش عارف", "متردد", "محتار", "مش متأكد", "not sure", "hesitant")):
            objections.append("uncertainty")
        if any(x in t for x in ("غالي", "سعره عالي", "expensive", "too much")):
            objections.append("price")
        if any(x in t for x in ("مش واثق", "مضمون", "ضمان", "موثوق", "trust", "guarantee")):
            objections.append("trust")
        if any(x in t for x in ("النهارده", "دلوقتي", "بسرعة", "عاجل", "today", "now", "urgent")):
            urgency = "high"
        else:
            urgency = "normal"

        if objections:
            stage = "objection"
        elif any(x in t for x in ("اشتري", "احجز", "ادفع", "buy", "purchase", "checkout")):
            stage = "decision"
        elif needs:
            stage = "discovery"
        else:
            stage = "conversation"

        if any(x in t for x in ("اشترى", "شراء", "احجز", "اطلب", "buy", "purchase")):
            intent = "purchase_or_action"
        elif any(x in t for x in ("اعرف", "شرح", "ايه", "كيف", "what", "how", "explain")):
            intent = "information"
        else:
            intent = "service_request"

        if any(x in t for x in ("لو سمحت", "من فضلك", "please", "thanks", "شكرا")):
            tone = "polite"
        elif len(text) < 80:
            tone = "concise"
        else:
            tone = "detailed"

        return CustomerSignals(intent, stage, tuple(needs), tuple(objections), tone, urgency)

    def prompt_context(self, text: str) -> str:
        s = self.analyze(text)
        return (
            "CUSTOMER INTELLIGENCE (observable conversational signals only):\n"
            f"intent={s.intent}; stage={s.stage}; urgency={s.urgency}; tone={s.tone};\n"
            f"needs={', '.join(s.needs) or 'not yet clear'}; objections={', '.join(s.objections) or 'none detected'}.\n"
            "Response rules: address the customer's actual goal first; acknowledge relevant "
            "concerns without assuming hidden feelings; be concise unless detail is useful; "
            "offer a concrete next step; never pressure, deceive, diagnose, or exploit vulnerabilities."
        )
