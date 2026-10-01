"""Website/e-commerce factory planning primitives."""
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class SiteBrief:
    business: str
    audience: str
    goal: str
    pages: tuple[str, ...]
    features: tuple[str, ...] = ()


def create_brief(business: str, audience: str, goal: str = "generate qualified leads") -> SiteBrief:
    return SiteBrief(business, audience, goal, ("home", "services", "about", "contact", "privacy"), ("mobile", "analytics", "lead_form"))


def improvement_plan(issues: list[str]) -> dict:
    return {"issues": issues, "priorities": list(enumerate(issues, 1)), "publish_requires_authorization": True}
