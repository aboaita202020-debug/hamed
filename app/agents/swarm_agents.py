"""Scalable 2020-agent cooperative swarm for Hamed AGI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base_agent import BaseAgent, AgentResult


@dataclass(frozen=True)
class SwarmSpec:
    name: str
    role: str
    department: str
    capabilities: tuple[str, ...]
    leader: bool = False


class SwarmAgent(BaseAgent):
    def __init__(self, tools, repo, spec: SwarmSpec, brain_provider=None):
        self.spec = spec
        self.name = spec.name
        self.brain_provider = brain_provider
        super().__init__(tools, repo)

    def run(self, payload: dict) -> AgentResult:
        objective = str(payload.get("objective") or payload.get("goal") or payload.get("message") or "").strip()
        context = payload.get("context") or {}
        peer_findings = payload.get("peer_findings") or {}
        if self.brain_provider is None:
            return AgentResult(
                success=False,
                error="brain_provider_not_configured",
                data={"agent": self.name, "department": self.spec.department},
            )
        prompt = (
            f"You are {self.name}, one of 2020 cooperating Hamed AGI assistants.\n"
            f"Department: {self.spec.department}\nRole: {self.spec.role}\n"
            f"Capabilities: {', '.join(self.spec.capabilities)}\n"
            f"Leader: {self.spec.leader}\n\n"
            f"Objective:\n{objective}\n\n"
            f"Shared context:\n{context}\n\n"
            f"Peer findings available to you:\n{peer_findings}\n\n"
            "Work as a specialist, not as the final decision maker. Return: "
            "FINDINGS, EVIDENCE_OR_MISSING_DATA, NEXT_ACTION, RISKS, PEER_MESSAGE. "
            "Do not claim that an external action happened unless the tool result proves it."
        )
        try:
            answer = self.brain_provider.generate_response(
                [{"role": "user", "content": prompt}],
                system=(
                    "You are a cooperative commercial AGI specialist. "
                    "Share useful findings with peer agents, distinguish evidence from inference, "
                    "respect approval gates, and never execute purchases/payments/contracts without authorization."
                ),
            )
            return AgentResult(
                success=True,
                data={
                    "agent": self.name,
                    "department": self.spec.department,
                    "role": self.spec.role,
                    "leader": self.spec.leader,
                    "capabilities": list(self.spec.capabilities),
                    "analysis": answer,
                    "peer_message": answer,
                },
            )
        except Exception as exc:
            return AgentResult(
                success=False,
                error=f"{type(exc).__name__}: {exc}",
                data={"agent": self.name, "department": self.spec.department},
            )


DEPARTMENTS = [
    ("Research & Intelligence", 202, ("research", "trends", "sources", "verification")),
    ("E-commerce & Product", 202, ("stores", "UX", "conversion", "products")),
    ("Cybersecurity & Sentinel", 252, ("security", "threat_intel", "authorized_assessment")),
    ("Marketing & Growth", 202, ("content", "SEO", "growth", "campaigns")),
    ("Sales & Revenue", 202, ("leads", "offers", "revenue", "pipeline")),
    ("Negotiation & Customer Psychology", 152, ("negotiation", "behavior", "messaging")),
    ("Websites & Software", 152, ("web", "software", "automation", "QA")),
    ("Analytics & Decision", 152, ("metrics", "risk", "decisions", "experiments")),
    ("B2B & Business Opportunities", 152, ("B2B", "partnerships", "opportunities")),
    ("Learning & Knowledge", 152, ("learning", "knowledge", "feedback")),
    ("Automation & Operations", 100, ("workflow", "operations", "routing")),
    ("Reporting, CRM & Kids Media", 100, ("CRM", "reporting", "kids_trends", "youtube_analytics")),
]

ROLE_BANK = {
    "Research & Intelligence": ("market researcher", "trend researcher", "source verifier", "competitor researcher", "public-data analyst"),
    "E-commerce & Product": ("store analyst", "UX analyst", "conversion analyst", "product researcher", "catalog analyst"),
    "Cybersecurity & Sentinel": ("web security analyst", "API security analyst", "threat intelligence analyst", "vulnerability analyst", "verification analyst"),
    "Marketing & Growth": ("content strategist", "SEO analyst", "growth analyst", "campaign analyst", "creative strategist"),
    "Sales & Revenue": ("lead researcher", "sales analyst", "offer strategist", "revenue analyst", "pipeline analyst"),
    "Negotiation & Customer Psychology": ("negotiation analyst", "customer psychology analyst", "objection analyst", "messaging analyst", "buyer journey analyst"),
    "Websites & Software": ("web architect", "software analyst", "automation analyst", "QA analyst", "integration analyst"),
    "Analytics & Decision": ("data analyst", "experiment analyst", "risk analyst", "decision analyst", "KPI analyst"),
    "B2B & Business Opportunities": ("B2B researcher", "partnership analyst", "market matcher", "opportunity researcher", "business model analyst"),
    "Learning & Knowledge": ("knowledge researcher", "learning analyst", "feedback analyst", "knowledge curator", "self-improvement analyst"),
    "Automation & Operations": ("workflow planner", "operations analyst", "task router", "process analyst", "reliability analyst"),
    "Reporting, CRM & Kids Media": ("CRM analyst", "reporting analyst", "kids media trend analyst", "YouTube analytics analyst", "content performance analyst"),
}


def build_swarm_specs(existing_names: set[str], target: int = 2020) -> list[SwarmSpec]:
    specs: list[SwarmSpec] = []
    for department, count, capabilities in DEPARTMENTS:
        key = department.lower().replace(" & ", "_").replace(" ", "_")
        roles = ROLE_BANK[department]
        for index in range(count):
            name = f"swarm_{key}_{index + 1:03d}"
            if name in existing_names:
                continue
            specs.append(
                SwarmSpec(
                    name=name,
                    role=roles[index % len(roles)],
                    department=department,
                    capabilities=capabilities,
                    leader=index == 0,
                )
            )
    remaining = max(0, target - len(existing_names))
    return specs[:remaining]
