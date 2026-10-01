from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RDAgentSpec:
    name: str
    role: str
    squad: str
    capabilities: tuple[str, ...]

SQUADS = [
    ("Discovery", 100, ("source_discovery","github_discovery","trend_discovery")),
    ("Deep Research", 150, ("research","literature_review","source_comparison")),
    ("Experiment", 100, ("benchmarking","prototyping","evaluation")),
    ("Integration", 75, ("integration","tooling","documentation")),
    ("Verification", 50, ("verification","fact_checking","security_review")),
    ("Knowledge Curators", 25, ("knowledge_graph","compression","teaching")),
]

ROLE_BANK = {
    "Discovery": ["web scout","GitHub scout","research scout","university scout","YouTube scout"],
    "Deep Research": ["literature analyst","research synthesizer","market researcher","psychology researcher","technology researcher"],
    "Experiment": ["benchmark engineer","prototype tester","tool evaluator","strategy tester","reproduction analyst"],
    "Integration": ["integration engineer","SDK analyst","workflow engineer","documentation engineer","capability mapper"],
    "Verification": ["fact checker","evidence reviewer","reliability analyst","security reviewer","reproducibility reviewer"],
    "Knowledge Curators": ["knowledge curator","ontology curator","lesson designer","memory auditor","agent teacher"],
}

def build_rd_agents() -> list[RDAgentSpec]:
    result: list[RDAgentSpec] = []
    for squad, count, caps in SQUADS:
        roles = ROLE_BANK[squad]
        for i in range(count):
            result.append(RDAgentSpec(
                name=f"rd_{squad.lower().replace(' ','_')}_{i+1:03d}",
                role=roles[i % len(roles)],
                squad=squad,
                capabilities=caps,
            ))
    assert len(result) == 500
    assert len({a.name for a in result}) == 500
    return result

RD_AGENTS = build_rd_agents()
RD_AGENT_REGISTRY = {a.name: a for a in RD_AGENTS}

def rd_status() -> dict[str, Any]:
    squads = {}
    for agent in RD_AGENTS:
        squads[agent.squad] = squads.get(agent.squad, 0) + 1
    return {"count": len(RD_AGENTS), "squads": squads, "github_discovery_agents": 100}

def select_for_topic(topic: str, limit: int = 25) -> list[dict[str, Any]]:
    topic = topic.lower()
    selected = RD_AGENTS
    if "github" in topic or "tool" in topic:
        selected = [a for a in RD_AGENTS if a.squad == "Discovery"]
    return [{"name": a.name, "role": a.role, "squad": a.squad} for a in selected[:max(1, min(limit, len(selected)))]]
