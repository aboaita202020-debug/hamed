"""15-role Brain Council for Hamed AI.

The council separates *expert roles* from model providers. Multiple roles can
run on the same configured provider, while the final judge combines their
independent assessments. No API key is required until the council is invoked.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Optional


@dataclass(frozen=True)
class BrainRole:
    name: str
    specialty: str
    system_prompt: str


@dataclass
class BrainOpinion:
    brain: str
    specialty: str
    answer: str
    confidence: int = 0
    risks: str = ""
    recommendation: str = ""


BRAIN_ROLES = (
    BrainRole("strategist", "strategy and decision making", "Act as Hamed's chief strategist. Optimize for durable business outcomes."),
    BrainRole("master_reasoner", "deep reasoning", "Reason rigorously. Challenge assumptions and identify hidden dependencies."),
    BrainRole("researcher", "research and evidence", "Separate facts from assumptions. Prefer verifiable evidence and flag uncertainty."),
    BrainRole("business_brain", "business models and markets", "Analyze business models, customers, markets, unit economics and scalability."),
    BrainRole("sales_master", "sales", "Optimize customer acquisition, qualification, objection handling and closing."),
    BrainRole("negotiator", "negotiation", "Design ethical negotiation strategies that protect value, margins and relationships."),
    BrainRole("psychology_brain", "customer psychology", "Analyze buyer motivations, objections, intent and decision friction without manipulation."),
    BrainRole("opportunity_hunter", "opportunity discovery", "Find concrete commercial opportunities and rank them by evidence, upside and feasibility."),
    BrainRole("procurement_brain", "procurement and suppliers", "Evaluate suppliers, total landed cost, terms, quality and purchasing leverage."),
    BrainRole("marketing_brain", "marketing", "Develop measurable positioning, acquisition, content and campaign strategies."),
    BrainRole("financial_analyst", "finance and unit economics", "Calculate costs, revenue, margin, cash impact and downside scenarios."),
    BrainRole("competitive_intelligence", "competitor analysis", "Assess competitors, differentiation, threats, pricing and market gaps."),
    BrainRole("creative_brain", "creative solutions", "Generate original practical solutions, offers and experiments while respecting constraints."),
    BrainRole("engineering_brain", "software engineering", "Review architecture, implementation risks, tests, reliability and maintainability."),
    BrainRole("ceo_final_judge", "executive synthesis", "Act as final judge. Compare evidence, risks and recommendations and select the strongest action."),
)


class BrainCouncil:
    """Run expert roles and synthesize a decision through a final judge."""

    def __init__(self, provider: Any):
        self.provider = provider
        self.roles = {role.name: role for role in BRAIN_ROLES}

    def _ask(self, role: BrainRole, task: str, context: str = "") -> str:
        prompt = (
            f"Role: {role.name}\nSpecialty: {role.specialty}\n\n"
            f"Task:\n{task}\n\nContext:\n{context}\n\n"
            "Return concise structured advice with: ANALYSIS, CONFIDENCE (0-100), "
            "RISKS, RECOMMENDATION. Do not invent evidence."
        )
        return self.provider.generate_response(
            [{"role": "user", "content": prompt}],
            system=role.system_prompt,
        )

    @staticmethod
    def _parse(text: str) -> tuple[int, str, str]:
        confidence = 0
        risks = ""
        recommendation = ""
        for raw in text.splitlines():
            line = raw.strip()
            upper = line.upper()
            if upper.startswith("CONFIDENCE"):
                digits = "".join(ch for ch in line.split(":", 1)[-1] if ch.isdigit())
                if digits:
                    confidence = max(0, min(100, int(digits)))
            elif upper.startswith("RISKS") and ":" in line:
                risks = line.split(":", 1)[1].strip()
            elif upper.startswith("RECOMMENDATION") and ":" in line:
                recommendation = line.split(":", 1)[1].strip()
        return confidence, risks, recommendation

    def deliberate(self, task: str, context: str = "", roles: Optional[list[str]] = None) -> dict:
        """Consult selected expert roles, then ask the CEO judge to synthesize.

        The final judge is always included. If provider calls fail, the council
        returns partial results instead of crashing the application.
        """
        selected = roles or [r.name for r in BRAIN_ROLES if r.name != "ceo_final_judge"]
        selected = [name for name in selected if name in self.roles and name != "ceo_final_judge"]
        opinions: list[BrainOpinion] = []

        for name in selected:
            role = self.roles[name]
            try:
                answer = self._ask(role, task, context)
                confidence, risks, recommendation = self._parse(answer)
                opinions.append(BrainOpinion(name, role.specialty, answer, confidence, risks, recommendation))
            except Exception as exc:
                opinions.append(BrainOpinion(name, role.specialty, f"brain_error:{type(exc).__name__}"))

        evidence = "\n\n".join(
            f"[{o.brain}] confidence={o.confidence}\n{o.answer}" for o in opinions
        )
        judge_role = self.roles["ceo_final_judge"]
        try:
            final_answer = self._ask(
                judge_role,
                "Synthesize the expert opinions below. Resolve disagreements explicitly, prioritize evidence, "
                "state the chosen action, confidence, key risks, and what must be verified before execution.\n\n" + evidence,
                context,
            )
        except Exception as exc:
            final_answer = f"judge_error:{type(exc).__name__}"

        return {
            "task": task,
            "brains_consulted": len(opinions),
            "total_brains": len(BRAIN_ROLES),
            "opinions": [asdict(o) for o in opinions],
            "final_judgment": final_answer,
        }

    def roster(self) -> list[dict[str, str]]:
        return [{"name": r.name, "specialty": r.specialty} for r in BRAIN_ROLES]
