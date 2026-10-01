"""Commercial workflow for Hamed's voice sales agent."""
from dataclasses import dataclass, field
from typing import Any

from app.agents.learning_engine import CommercialLearningEngine, LearningRecord, Skill
from app.agents.sales_agent import SalesLimits, negotiate_within_limits
from .sales_context import SalesContext


@dataclass(frozen=True)
class SalesPlan:
    objective: str
    discovery_questions: tuple[str, ...]
    value_points: tuple[str, ...]
    recommended_services: tuple[str, ...]
    next_step: str
    requires_approval: bool = False


@dataclass
class CallOutcome:
    status: str
    objection: str = ""
    service: str = ""
    notes: str = ""
    price: float | None = None
    success: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class CommercialVoiceOrchestrator:
    """Coordinates discovery, offer strategy, guarded negotiation and learning."""

    def __init__(self, learning: CommercialLearningEngine | None = None) -> None:
        self.learning = learning or CommercialLearningEngine()

    def build_plan(self, context: SalesContext) -> SalesPlan:
        services = context.recommended_services or context.likely_needs
        questions = (
            "ما أهم هدف تريد تحقيقه من الموقع أو التسويق خلال الفترة القادمة؟",
            "ما أكثر شيء تشعر أنه يمنع النشاط من الحصول على نتائج أفضل؟",
            "هل جربتم حلًا لهذه المشكلة من قبل، وما الذي لم يعمل؟",
            "ما الأولوية عندكم حاليًا: زيادة العملاء أم تحسين التحويل أم تقليل التكلفة؟",
        )
        values = tuple(
            f"حل {problem} بطريقة مرتبطة بهدف العميل"
            for problem in context.observed_problems
        ) or ("تحسين النتيجة التجارية بدل بيع خدمة غير مطلوبة",)
        return SalesPlan(
            objective=context.objective,
            discovery_questions=questions,
            value_points=values,
            recommended_services=services,
            next_step="send_audit_or_proposal" if services else "schedule_discovery",
        )

    def negotiate(self, proposed_price: float, list_price: float, minimum_price: float, max_discount_percent: float = 0.0) -> str:
        limits = SalesLimits(minimum_price=minimum_price, maximum_discount_percent=max_discount_percent)
        return negotiate_within_limits(proposed_price, list_price, limits)

    def record_outcome(self, skill: Skill, outcome: CallOutcome) -> LearningRecord | None:
        if outcome.success is None or not outcome.notes:
            return None
        return self.learning.learn_from_outcome(
            skill=skill,
            lesson=outcome.notes,
            outcome=outcome.status,
            success=outcome.success,
            source="voice_call_outcome",
        )

    def summary(self) -> dict[str, Any]:
        return self.learning.summarize()
