"""Unified commercial decision brain for Hamed AI.

This layer turns a raw business request into a structured, approval-aware
execution plan that specialist agents can consume without taking authority
away from the server-side policy layer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any


class Objective(str, Enum):
    SALES = "sales"
    PURCHASING = "purchasing"
    AFFILIATE = "affiliate"
    WEBSITE_SERVICE = "website_service"
    MARKETING = "marketing"
    RESEARCH = "research"
    NEGOTIATION = "negotiation"
    CUSTOMER_SERVICE = "customer_service"
    OTHER = "other"


@dataclass(frozen=True)
class CommercialPlan:
    objective: Objective
    intent: str
    next_steps: list[str] = field(default_factory=list)
    requires_research: bool = False
    approval_required: bool = False
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)


KEYWORDS: dict[Objective, tuple[str, ...]] = {
    Objective.PURCHASING: ("شراء", "مشتريات", "اشتري", "توريد", "مورد", "supplier", "buy", "purchase"),
    Objective.SALES: ("بيع", "مبيعات", "عميل", "بيع منتج", "sales", "sell", "customer"),
    Objective.AFFILIATE: ("تسويق بالعمولة", "افلييت", "affiliate", "commission", "عمولة"),
    Objective.WEBSITE_SERVICE: ("موقع", "متجر", "متجر الكتروني", "متجر إلكتروني", "website", "store", "seo", "واتساب"),
    Objective.MARKETING: ("تسويق", "حملة", "اعلان", "إعلان", "محتوى", "marketing", "campaign"),
    Objective.RESEARCH: ("ابحث", "بحث", "دورلي", "معلومات", "مقارنة", "research", "find"),
    Objective.NEGOTIATION: ("تفاوض", "فاصل", "خصم", "السعر", "سومة", "negotiate", "discount", "price"),
    Objective.CUSTOMER_SERVICE: ("شكوى", "مشكلة في الطلب", "خدمة العملاء", "استرجاع", "complaint", "support", "refund"),
}

HIGH_IMPACT = {"purchase", "payment", "transfer", "contract", "publish", "account_change", "irreversible"}


def _score(text: str, words: tuple[str, ...]) -> int:
    lowered = text.lower()
    return sum(1 for word in words if word.lower() in lowered)


def classify(text: str) -> tuple[Objective, float]:
    scores = {objective: _score(text, words) for objective, words in KEYWORDS.items()}
    best = max(scores, key=scores.get)
    best_score = scores[best]
    if best_score == 0:
        return Objective.OTHER, 0.25
    total = sum(scores.values()) or 1
    return best, min(0.99, max(0.35, best_score / total))


def build_plan(text: str, *, action: str | None = None) -> CommercialPlan:
    objective, confidence = classify(text)
    requires_research = objective in {
        Objective.PURCHASING,
        Objective.AFFILIATE,
        Objective.WEBSITE_SERVICE,
        Objective.RESEARCH,
        Objective.MARKETING,
    }
    approval_required = bool(action and action in HIGH_IMPACT)

    steps: list[str]
    notes: list[str] = []
    if objective is Objective.PURCHASING:
        steps = [
            "جمع مواصفات المنتج والكمية والسوق المستهدف",
            "البحث عن الموردين ومقارنة التكلفة والشروط",
            "حساب landed cost والربح والهامش والمخاطر",
            "ترتيب أفضل الفرص وإعداد توصية شراء",
            "طلب موافقة قبل تنفيذ الشراء أو الدفع",
        ]
    elif objective is Objective.SALES:
        steps = [
            "تحديد العميل والاحتياج",
            "التحقق من المشكلة أو فرصة القيمة",
            "اختيار المنتج أو الخدمة المناسبة",
            "عرض القيمة والخيارات",
            "التعامل مع الاعتراضات والتفاوض ضمن الحدود",
            "تسجيل النتيجة والمتابعة",
        ]
    elif objective is Objective.AFFILIATE:
        steps = [
            "اكتشاف البرامج والمنتجات المناسبة",
            "تقييم الجودة والطلب وملاءمة الجمهور والعمولة",
            "تقدير القيمة الاقتصادية والمخاطر",
            "إعداد محتوى/حملة قابلة للقياس مع الإفصاح عند اللزوم",
            "متابعة التحويلات والنتائج وتحسين الاستراتيجية",
        ]
    elif objective is Objective.WEBSITE_SERVICE:
        steps = [
            "جمع بيانات النشاط والموقع الحالي إن وجد",
            "فحص المشكلة أو فجوة التحويل بمعلومات قابلة للتحقق",
            "اختيار خدمة إصلاح أو إعادة تصميم أو إنشاء موقع/متجر",
            "إعداد عرض مخصص يوضح المشكلة والقيمة والحل",
            "التواصل والتفاوض ضمن الصلاحيات",
            "تنفيذ التسليم والنشر بعد الموافقات اللازمة",
        ]
    elif objective is Objective.NEGOTIATION:
        steps = [
            "تحديد الهدف والحد الأدنى المقبول",
            "فهم اعتراض واحتياجات الطرف الآخر",
            "حماية القيمة واستخدام بدائل غير السعر عند الإمكان",
            "تقديم خيارات منظمة",
            "تصعيد أي استثناء خارج الحدود",
        ]
    elif objective is Objective.RESEARCH:
        steps = [
            "تحديد سؤال البحث",
            "البحث عن مصادر موثوقة",
            "تمييز الحقائق عن التقديرات والاستنتاجات",
            "تلخيص الأدلة مع الروابط عند توفرها",
            "تحويل النتائج إلى قرار أو تجربة قابلة للقياس",
        ]
    elif objective is Objective.MARKETING:
        steps = [
            "تحديد المنتج والجمهور والهدف",
            "صياغة عرض قيمة واضح",
            "إعداد أكثر من رسالة/زاوية",
            "اختبار الأداء وقياس النتائج",
            "تحسين الحملة بناءً على البيانات",
        ]
    elif objective is Objective.CUSTOMER_SERVICE:
        steps = [
            "فهم المشكلة والتحقق من بيانات الطلب",
            "تقديم حل واضح أو تصعيد مناسب",
            "توثيق الحالة والنتيجة",
            "التقاط السبب الجذري لتقليل تكرار المشكلة",
        ]
    else:
        steps = ["فهم الطلب", "تحديد البيانات الناقصة", "اختيار الوكيل والأداة المناسبة", "تنفيذ الخطوة المسموح بها", "تسجيل النتيجة"]
        notes.append("النية غير محددة بما يكفي؛ لا تفترض معلومات غير موجودة.")

    if approval_required:
        notes.append("الإجراء عالي التأثير ويحتاج موافقة خادم/مالك قبل التنفيذ.")
    return CommercialPlan(
        objective=objective,
        intent=text.strip(),
        next_steps=steps,
        requires_research=requires_research,
        approval_required=approval_required,
        confidence=confidence,
        notes=notes,
    )


def extract_money(text: str) -> float | None:
    """Best-effort extraction for an explicitly stated numeric amount."""
    match = re.search(r"(?:^|\s)(\d+(?:[.,]\d+)?)\s*(?:جنيه|ج|egp|usd|دولار)?(?:\s|$)", text, flags=re.I)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))
