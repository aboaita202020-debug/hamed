"""Adaptive customer conversation engine for Hamed AI.

Builds the next useful conversation step from the customer's latest response.
It does not impersonate a human, invent facts, or use manipulative pressure.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ConversationTurn:
    message: str
    stage: str
    detected_need: str | None
    customer_state: str
    next_question: str | None
    suggested_action: str

class CustomerConversationEngine:
    """Turns customer replies into adaptive discovery and sales steps."""
    def analyze(self, message: str, context: dict[str, Any] | None = None) -> ConversationTurn:
        text = (message or "").strip().lower()
        context = context or {}
        if not text:
            return ConversationTurn(
                "أهلاً بحضرتك. حابب أعرف نشاطك وإيه أهم حاجة عايز تحسنها حاليًا؟",
                "discovery", None, "unknown",
                "ما أهم نتيجة تريد تحسينها الآن؟", "ask_discovery")

        urgent = any(x in text for x in ("دلوقتي", "عاجل", "urgent", "today", "asap"))
        price = any(x in text for x in ("سعر", "تكلفة", "كام", "price", "cost"))
        sales = any(x in text for x in ("مبيعات", "عملاء", "sales", "customers", "leads"))
        trust = any(x in text for x in ("مضمون", "ضمان", "ثقة", "guarantee", "proof"))
        need = "sales/customer acquisition" if sales else context.get("detected_need")
        state = "urgent" if urgent else "price_sensitive" if price else "trust_seeking" if trust else "engaged"

        if price and not need:
            question = "أكيد. قبل ما أحدد تكلفة مناسبة، إيه النتيجة اللي محتاج تحققها تحديدًا؟"
            action = "clarify_value_before_pricing"
        elif trust:
            question = "مفهوم. تحب نبدأ بتقييم أو تجربة محدودة، ونحدد النتيجة القابلة للقياس قبل أي التزام؟"
            action = "offer_low_risk_pilot"
        elif sales:
            question = "تمام. المشكلة الأكبر عندك في جذب عملاء جدد، ولا تحويل المهتمين إلى مشترين؟"
            action = "qualify_sales_problem"
        elif urgent:
            question = "تمام. إيه المشكلة العاجلة التي تريد حلها أولًا؟"
            action = "prioritize_urgent_problem"
        else:
            question = "ممكن توضحلي أكتر إيه النتيجة اللي نفسك توصل لها؟"
            action = "deepen_discovery"

        return ConversationTurn(
            message, "discovery", need, state, question, action
        )

    def next_turn(self, message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        turn = self.analyze(message, context)
        return {
            "stage": turn.stage,
            "customer_state": turn.customer_state,
            "detected_need": turn.detected_need,
            "next_question": turn.next_question,
            "suggested_action": turn.suggested_action,
            "requires_human_approval": False,
            "truth_required": True,
            "no_impersonation": True,
            "respect_opt_out": True,
        }
