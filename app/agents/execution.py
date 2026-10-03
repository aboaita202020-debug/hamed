"""Generic specialist execution contract for every registered Hamed agent."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any, Callable
from .registry import AGENT_REGISTRY, AgentProfile

@dataclass(frozen=True)
class AgentContract:
    id: str
    name: str
    role: str
    description: str
    capabilities: tuple[str, ...]
    tasks: tuple[str, ...]
    tools: tuple[str, ...]
    preferred_brain: str
    fallback_brains: tuple[str, ...]
    permissions: tuple[str, ...]
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    success_criteria: tuple[str, ...]

def contract(profile: AgentProfile) -> AgentContract:
    capability = profile.domain
    return AgentContract(
        id=profile.id, name=profile.name, role=profile.domain,
        description=profile.goal, capabilities=(capability,), tasks=(profile.goal,),
        tools=(), preferred_brain="router", fallback_brains=("openai", "claude", "deepseek"),
        permissions=("read_public_data", "generate_analysis"),
        input_schema={"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]},
        output_schema={"type": "object", "properties": {"agent_id": {"type": "string"}, "result": {"type": "string"}}},
        success_criteria=("agent_id is preserved", "result is produced", "no unauthorized action is performed"),
    )

class AgentExecutor:
    def __init__(self, responder: Callable[[str, AgentContract, str], str] | None = None) -> None:
        self.responder = responder
    def contracts(self) -> list[AgentContract]: return [contract(p) for p in AGENT_REGISTRY.values()]
    def get(self, agent_id: str) -> AgentContract:
        if agent_id not in AGENT_REGISTRY: raise KeyError(agent_id)
        return contract(AGENT_REGISTRY[agent_id])
    def execute(self, agent_id: str, task: str) -> dict[str, Any]:
        if not task or not task.strip(): raise ValueError("task is required")
        c = self.get(agent_id)
        result = self.responder(agent_id, c, task) if self.responder else f"Planned specialist task for {c.name}: {task.strip()}"
        return {"agent_id": agent_id, "agent": c.name, "result": result, "status": "completed"}

__all__ = ["AgentContract", "AgentExecutor", "contract"]
