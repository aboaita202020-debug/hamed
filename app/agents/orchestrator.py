"""
HamedOrchestrator — the central brain (spec section 4).

This is the class that previously failed to import
(`ImportError: cannot import name 'HamedOrchestrator' from
app.agents.orchestrator`). The fix has two parts:

  1. Structural: this module lives at `app/agents/orchestrator.py` and
     defines the class at module level with the exact name
     `HamedOrchestrator`, and `app/agents/__init__.py` re-exports it —
     so both `from app.agents.orchestrator import HamedOrchestrator`
     and `from app.agents import HamedOrchestrator` work.
  2. No circular imports: agents import from `app.tools` / `app.db` /
     `app.permissions`, never from `app.agents.orchestrator`, so the
     orchestrator can safely import every agent module without a cycle.

Responsibilities implemented here (spec section 4):
  - understands a goal (routes a task to the right Agent by name)
  - distributes work, collects results
  - retries on transient failure
  - records every agent run (agent_runs table) for observability
  - applies the Permission Layer indirectly (each Agent's Tool calls
    already go through it — the Orchestrator itself does not bypass it)
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from app.db.database import Database, get_database
from app.db.repository import Repository
from app.permissions import PermissionLayer
from app.tools.tool_registry import ToolRegistry
from app.tools.web_search_tool import WebSearchTool, SearchProvider
from app.tools.crm_tool import CRMTool
from app.logging_config import get_logger

from .base_agent import BaseAgent, AgentResult
from .opportunity_hunter_agent import OpportunityHunterAgent
from .sales_agent import SalesAgent
from .negotiation_agent import NegotiationAgent
from .revenue_agent import RevenueAgent
from .reporting_agent import ReportingAgent
from .fact_check_agent import FactCheckAgent

logger = get_logger(__name__)


@dataclass
class OrchestratorResult:
    agent: str
    result: AgentResult
    attempts: int = 1


class HamedOrchestrator:
    """Central coordinator. Construct once per process (or per test)."""

    def __init__(
        self,
        db: Optional[Database] = None,
        search_provider: Optional[SearchProvider] = None,
        max_retries: int = 2,
    ):
        self.db = db or get_database()
        self.repo = Repository(self.db)
        self.permissions = PermissionLayer(self.repo)
        self.tools = ToolRegistry(self.permissions)
        self.max_retries = max_retries

        # Register built-in tools
        self.tools.register(WebSearchTool(provider=search_provider))
        self.tools.register(CRMTool(self.repo))

        # Register built-in agents
        self.agents: dict[str, BaseAgent] = {}
        for agent_cls in (
            OpportunityHunterAgent,
            SalesAgent,
            NegotiationAgent,
            RevenueAgent,
            ReportingAgent,
            FactCheckAgent,
        ):
            self.register_agent(agent_cls(self.tools, self.repo))

    def register_agent(self, agent: BaseAgent) -> None:
        """Allows extending to 40/80 agents later without touching this
        class's internals (spec section 11)."""
        self.agents[agent.name] = agent

    def dispatch(self, agent_name: str, payload: dict) -> OrchestratorResult:
        """Route a task to one Agent, with retry-on-failure and a full
        agent_runs audit trail (spec section 4 & 19)."""
        if agent_name not in self.agents:
            return OrchestratorResult(
                agent=agent_name,
                result=AgentResult(success=False, error=f"unknown_agent:{agent_name}"),
            )

        agent = self.agents[agent_name]
        attempts = 0
        last_result: Optional[AgentResult] = None

        while attempts < max(1, self.max_retries):
            attempts += 1
            run_id = self.repo.start_agent_run(agent_name, str(payload)[:500])
            try:
                last_result = agent.run(payload)
                status = "DONE" if last_result.success else "FAILED"
                self.repo.finish_agent_run(run_id, status, error=last_result.error)
                if last_result.success:
                    break
            except Exception as exc:  # an Agent must never crash the Orchestrator
                logger.exception("Agent '%s' raised an unhandled exception", agent_name)
                self.repo.finish_agent_run(run_id, "FAILED", error=str(exc))
                last_result = AgentResult(success=False, error=str(exc))

            if attempts < self.max_retries:
                time.sleep(0.05)  # tiny backoff; keep tests fast

        return OrchestratorResult(agent=agent_name, result=last_result, attempts=attempts)

    def run_pipeline(self, steps: list[tuple[str, dict]]) -> list[OrchestratorResult]:
        """Run several agents in sequence, e.g. the example flow in spec
        section 7: Opportunity Hunter -> Research -> Sales -> Proposal."""
        results = []
        for agent_name, payload in steps:
            outcome = self.dispatch(agent_name, payload)
            results.append(outcome)
            if not outcome.result.success:
                logger.info("Pipeline stopped at '%s': %s", agent_name, outcome.result.error)
                break
        return results

    def dashboard(self) -> dict:
        return self.dispatch("reporting_agent", {}).result.data or {}
