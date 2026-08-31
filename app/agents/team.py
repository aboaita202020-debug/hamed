"""Hamed's specialist team and dynamic delegation policy.

The team starts with 20 focused roles. The coordinator may spawn additional
roles for a task, but every spawned role remains bounded by the same tool and
authorization policies as the parent agent.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Specialist:
    key: str
    name: str
    mission: str
    skills: tuple[str, ...]


DEFAULT_TEAM: tuple[Specialist, ...] = (
    Specialist("sales", "Sales Agent", "بيع وتحويل العملاء إلى صفقات", ("qualification", "offers", "negotiation")),
    Specialist("leadgen", "Lead Generation Agent", "اكتشاف العملاء والفرص التجارية", ("prospecting", "lead_scoring")),
    Specialist("research", "Research Agent", "البحث والتحقق من المعلومات", ("research", "fact_checking")),
    Specialist("market", "Market Intelligence Agent", "تحليل السوق والمنافسين", ("market_analysis", "competitor_analysis")),
    Specialist("pricing", "Pricing Agent", "التسعير وحساب الهامش", ("pricing", "margin")),
    Specialist("finance", "Finance Agent", "تحليل الإيرادات والتكاليف والربحية", ("finance", "forecasting")),
    Specialist("marketing", "Marketing Agent", "التسويق والحملات والتحويل", ("campaigns", "conversion")),
    Specialist("copy", "Copywriting Agent", "كتابة العروض والمحتوى التجاري", ("copywriting", "proposals")),
    Specialist("creative", "Creative Agent", "التصميم والأفكار الإبداعية", ("creative", "branding")),
    Specialist("web", "Web Agent", "إنشاء وتطوير المواقع", ("web", "frontend", "backend")),
    Specialist("commerce", "E-commerce Agent", "إنشاء وإدارة المتاجر", ("ecommerce", "catalog")),
    Specialist("automation", "Automation Agent", "أتمتة سير العمل والتكاملات", ("automation", "integrations")),
    Specialist("engineering", "Engineering Agent", "هندسة البرمجيات والاختبارات", ("software", "testing")),
    Specialist("qa", "QA Agent", "اختبار الجودة واكتشاف الأخطاء", ("qa", "validation")),
    Specialist("security", "Security Agent", "الأمن واكتشاف المخاطر التقنية", ("security", "risk")),
    Specialist("operations", "Operations Agent", "تنظيم التنفيذ والمتابعة", ("operations", "scheduling")),
    Specialist("customer_success", "Customer Success Agent", "متابعة العميل والتسليم والدعم", ("retention", "support")),
    Specialist("legal_review", "Compliance Agent", "فحص الالتزامات والمخاطر قبل الإجراءات الحساسة", ("compliance", "policy_review")),
    Specialist("analytics", "Analytics Agent", "قياس الأداء وتحليل النتائج", ("analytics", "reporting")),
    Specialist("critic", "Red-Team Critic Agent", "مراجعة قرارات الفريق ومحاولة كشف الأخطاء", ("critique", "verification")),
)


class AgentTeam:
    def __init__(self, specialists: tuple[Specialist, ...] = DEFAULT_TEAM) -> None:
        self.specialists = {agent.key: agent for agent in specialists}
        self.dynamic_agents: dict[str, Specialist] = {}

    @property
    def all_agents(self) -> dict[str, Specialist]:
        return {**self.specialists, **self.dynamic_agents}

    def add_specialist(self, key: str, name: str, mission: str, skills: list[str] | tuple[str, ...]) -> Specialist:
        if key in self.all_agents:
            raise ValueError(f"Agent already exists: {key}")
        agent = Specialist(key, name, mission, tuple(skills))
        self.dynamic_agents[key] = agent
        return agent

    def select(self, task: str, limit: int = 5) -> list[Specialist]:
        text = task.lower()
        keywords = {
            "sales": ("بيع", "عميل", "صفقة", "عرض", "تفاوض"),
            "leadgen": ("عملاء", "leads", "prospect"),
            "research": ("بحث", "تحقق", "معلومة"),
            "market": ("سوق", "منافس", "أسعار"),
            "pricing": ("سعر", "تسعير", "هامش", "تكلفة"),
            "finance": ("ربح", "إيراد", "تكلفة", "مال"),
            "marketing": ("تسويق", "إعلان", "حملة", "مبيعات"),
            "web": ("موقع", "website", "ويب"),
            "commerce": ("متجر", "ecommerce", "منتجات"),
            "automation": ("أتمتة", "ربط", "تكامل"),
            "engineering": ("كود", "برمجة", "تطبيق", "نظام"),
            "qa": ("اختبار", "bug", "جودة"),
            "security": ("أمان", "اختراق", "ثغرة", "security"),
            "operations": ("تنفيذ", "تشغيل", "مهمة"),
            "customer_success": ("دعم", "تسليم", "متابعة"),
            "analytics": ("تحليل", "تقرير", "بيانات", "أداء"),
            "critic": ("مراجعة", "تأكد", "مخاطر"),
        }
        scored = []
        for key, agent in self.all_agents.items():
            score = sum(1 for word in keywords.get(key, ()) if word in text)
            scored.append((score, key, agent))
        scored.sort(key=lambda x: (-x[0], x[1]))
        chosen = [agent for score, _, agent in scored if score > 0][:limit]
        if not chosen:
            chosen = [self.specialists["operations"], self.specialists["critic"]]
        return chosen

    def delegate(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        chosen = self.select(task)
        return {
            "task": task,
            "delegated_to": [agent.key for agent in chosen],
            "roles": [{"key": a.key, "name": a.name, "mission": a.mission, "skills": list(a.skills)} for a in chosen],
            "can_spawn_more": True,
            "context": context or {},
        }
