"""Coordinate Hamed's specialist agents and assign brains dynamically."""
from __future__ import annotations

from typing import Any

from .multi_brain import MultiBrainRouter
from .specialists import specialist_system
from .team import AgentTeam


class TeamOrchestrator:
    def __init__(self, brain: MultiBrainRouter, team: AgentTeam | None = None) -> None:
        self.brain = brain
        self.team = team or AgentTeam()

    def delegate(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        plan = self.team.delegate(task, context)
        results = []
        for role in plan["delegated_to"]:
            agent = self.team.all_agents[role]
            prompt = f"Task: {task}\nContext: {context or {}}\nRole: {agent.name}\nMission: {agent.mission}\nSkills: {', '.join(agent.skills)}"
            try:
                answer = self.brain.generate_response([{"role": "user", "content": prompt}], system=specialist_system(role))
                results.append({"agent": role, "answer": answer})
            except Exception as exc:
                results.append({"agent": role, "error": str(exc)})
        return {**plan, "results": results}

    def spawn_for_gap(self, key: str, name: str, mission: str, skills: list[str]) -> dict[str, str]:
        agent = self.team.add_specialist(key, name, mission, skills)
        return {"key": agent.key, "name": agent.name, "mission": agent.mission}
