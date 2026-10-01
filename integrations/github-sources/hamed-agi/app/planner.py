from __future__ import annotations

from dataclasses import dataclass

from .models import Mission


@dataclass(frozen=True)
class PlanStep:
    id: str
    tool: str
    purpose: str
    requires_authorization: bool = False


class OrviaPlanner:
    """Build safe, auditable mission plans without granting authorization."""

    def plan(self, objective: str, target: str | None = None) -> Mission:
        steps = [
            PlanStep("research", "web_research", "collect public evidence"),
            PlanStep("commerce", "ecommerce_analyzer", "analyze public store signals"),
            PlanStep("seo", "seo_analyzer", "analyze public SEO signals"),
            PlanStep("performance", "performance_analyzer", "analyze public performance signals"),
            PlanStep("opportunity", "opportunity_engine", "convert evidence into opportunities"),
            PlanStep("verify", "verification", "verify evidence before promotion"),
            PlanStep("report", "report_generator", "produce an auditable report"),
            PlanStep("crm", "crm", "record qualified business context"),
            PlanStep("proposal", "proposal_generator", "draft a non-binding offer"),
        ]
        if target:
            steps.insert(4, PlanStep(
                "security", "sentinel_authorized_scan",
                "run security assessment only after explicit authorization",
                requires_authorization=True,
            ))
        return Mission(
            objective=objective,
            status="planned",
            actions=[s.tool for s in steps],
            metadata={
                "planner": "orvia_planner_v1",
                "target": target,
                "steps": [s.__dict__ for s in steps],
                "policy": "public_research_allowed; active_security_requires_explicit_authorization; destructive_actions_blocked",
            },
        )


planner = OrviaPlanner()
