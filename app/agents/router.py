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

CLIENT_WORDS = ("عميل", "عملاء", "زبون", "زبائن", "lead", "leads", "prospect", "prospects", "عملاء محتملين", "عملاء محتملون", "prospecting", "social media", "سوشيال")
LEARNING_WORDS = ("تعلم", "اتعلم", "علم النفس", "psychology", "استراتيجية بيع", "خدمة العملاء", "sales science")

class AgentRouter:
    def select(self, text: str, limit: int = 12) -> list[str]:
        t = text.lower()
        selected: list[str] = ["chief", "planner"]
        for domain, words in KEYWORDS.items():
            if any(w.lower() in t for w in words):
                selected.extend(a.id for a in AGENT_REGISTRY.values() if a.domain == domain)
        if any(w in t for w in CLIENT_WORDS):
            selected.extend(CLIENT_RESEARCH_AGENTS)
        if any(w in t for w in LEARNING_WORDS):
            selected.extend(LEARNING_COUNCIL)
        selected.append("reviewer")
        return list(dict.fromkeys(selected))[:limit]

    def system_context(self, text: str) -> str:
        profiles = [AGENT_REGISTRY[i] for i in self.select(text)]
        return "Selected specialist team:\n" + "\n".join(f"- {p.name}: {p.goal}" for p in profiles)
