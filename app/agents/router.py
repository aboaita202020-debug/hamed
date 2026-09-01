"""Task router for Hamed's specialist agents and multi-brain provider selection."""
from .registry import AGENT_REGISTRY, CLIENT_RESEARCH_AGENTS, LEARNING_COUNCIL

KEYWORDS = {
    "code": ("python", "javascript", "code", "برمج", "كود", "موقع", "تطبيق", "github", "docker"),
    "sales": ("بيع", "مبيعات", "sales", "عميل", "عملاء", "lead", "leads", "سعر", "عرض"),
    "marketing": ("تسويق", "marketing", "إعلان", "ads", "seo", "محتوى", "social", "سوشيال"),
    "research": ("ابحث", "بحث", "research", "دراسة", "مصادر", "منافس", "سوق"),
    "learning": ("تعلم", "اتعلم", "علم النفس", "psychology", "استراتيجية بيع", "خدمة العملاء"),
    "documents": ("pdf", "excel", "xlsx", "csv", "ملف", "مستند", "تقرير"),
    "industry": ("مصنع", "تصنيع", "تعبئة", "تغليف", "مستحضرات", "عقارات", "لوجستيات"),
}

class AgentRouter:
    def select(self, text: str, limit: int = 6) -> list[str]:
        t = text.lower()
        selected: list[str] = ["chief", "planner"]
        for domain, words in KEYWORDS.items():
            if any(w.lower() in t for w in words):
                matches = [a.id for a in AGENT_REGISTRY.values() if a.domain == domain]
                selected.extend(matches[:2])
        if any(w in t for w in ("عميل", "عملاء", "lead", "leads", "زبون")):
            selected.extend(CLIENT_RESEARCH_AGENTS)
        if any(w in t for w in ("تعلم", "علم النفس", "مبيعات", "بيع", "خدمة العملاء", "strategy")):
            selected.extend(LEARNING_COUNCIL)
        selected.append("reviewer")
        return list(dict.fromkeys(selected))[:limit]

    def system_context(self, text: str) -> str:
        ids = self.select(text)
        profiles = [AGENT_REGISTRY[i] for i in ids]
        lines = [f"- {p.name}: {p.goal}" for p in profiles]
        return "Selected specialist team:\n" + "\n".join(lines)
