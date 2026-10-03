"""
BaseAgent — every specialized Agent (Sales, Revenue, Opportunity Hunter...)
inherits from this (spec section 30: "كل Agent قابل للاختبار منفردًا").

An Agent:
  - has a unique `name`
  - receives the shared ToolRegistry + Repository via the constructor
    (dependency injection, never a global import) so it can be tested
    in isolation with fakes/mocks.
  - implements `run(payload: dict) -> AgentResult`
  - every run is wrapped by the Orchestrator with an agent_runs log
    entry (started/finished/error) automatically.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.tools.tool_registry import ToolRegistry
from app.db.repository import Repository
from app.logging_config import get_logger


@dataclass
class AgentResult:
    success: bool
    data: Any = None
    error: str = ""
    next_actions: list[str] = field(default_factory=list)


class BaseAgent:
    name: str = "base_agent"

    def __init__(self, tools: ToolRegistry, repo: Repository):
        self.tools = tools
        self.repo = repo
        self.logger = get_logger(f"agent.{self.name}")

    def run(self, payload: dict) -> AgentResult:  # pragma: no cover - interface
        raise NotImplementedError(f"{self.__class__.__name__} must implement run()")
