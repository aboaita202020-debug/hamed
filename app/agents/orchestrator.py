"""Central coordinator for Hamed AI, including the 15-brain council and Opportunity Machine."""
from __future__ import annotations
import time
from dataclasses import dataclass
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
from .opportunity_machine_agent import OpportunityMachineAgent
from .customer_relationship_agent import CustomerRelationshipAgent
from .customer_psychology_agent import CustomerPsychologyAgent
from .sales_agent import SalesAgent
from .negotiation_agent import NegotiationAgent
from .revenue_agent import RevenueAgent
from .reporting_agent import ReportingAgent
from .fact_check_agent import FactCheckAgent
from .brain_council import BrainCouncil, BRAIN_ROLES
logger = get_logger(__name__)
@dataclass
class OrchestratorResult:
    agent: str
    result: AgentResult
    attempts: int = 1
class HamedOrchestrator:
    """Central coordinator for business agents and autonomous opportunity missions."""
    def __init__(self, db: Optional[Database] = None, search_provider: Optional[SearchProvider] = None, max_retries: int = 2, brain_provider=None):
        self.db = db or get_database()
        self.repo = Repository(self.db)
        self.permissions = PermissionLayer(self.repo)
        self.tools = ToolRegistry(self.permissions)
        self.max_retries = max_retries
        self.brain_provider = brain_provider
        self.brain_council = BrainCouncil(brain_provider) if brain_provider is not None else None
        self.tools.register(WebSearchTool(provider=search_provider))
        self.tools.register(CRMTool(self.repo))
        self.agents: dict[str, BaseAgent] = {}
        for agent_cls in (OpportunityHunterAgent, OpportunityMachineAgent, CustomerRelationshipAgent, CustomerPsychologyAgent, SalesAgent, NegotiationAgent, RevenueAgent, ReportingAgent, FactCheckAgent):
            self.register_agent(agent_cls(self.tools, self.repo))
    def register_agent(self, agent: BaseAgent) -> None:
        self.agents[agent.name] = agent
    def dispatch(self, agent_name: str, payload: dict) -> OrchestratorResult:
        if agent_name not in self.agents:
            return OrchestratorResult(agent_name, AgentResult(success=False, error=f"unknown_agent:{agent_name}"))
        agent = self.agents[agent_name]
        attempts = 0
        last_result: Optional[AgentResult] = None
        while attempts < max(1, self.max_retries):
            attempts += 1
            run_id = self.repo.start_agent_run(agent_name, str(payload)[:500])
            try:
                last_result = agent.run(payload)
                self.repo.finish_agent_run(run_id, "DONE" if last_result.success else "FAILED", error=last_result.error)
                if last_result.success: break
            except Exception as exc:
                logger.exception("Agent '%s' raised an unhandled exception", agent_name)
                self.repo.finish_agent_run(run_id, "FAILED", error=str(exc))
                last_result = AgentResult(success=False, error=str(exc))
            if attempts < self.max_retries: time.sleep(0.05)
        return OrchestratorResult(agent_name, last_result, attempts)
    def brain_roster(self) -> list[dict[str, str]]:
        return [{"name": role.name, "specialty": role.specialty} for role in BRAIN_ROLES]
    def consult_brains(self, task: str, context: str = "", roles: Optional[list[str]] = None) -> dict:
        if self.brain_council is None:
            return {"success": False, "error": "brain_provider_not_configured", "brains": self.brain_roster()}
        return {"success": True, **self.brain_council.deliberate(task, context, roles)}
    def run_pipeline(self, steps: list[tuple[str, dict]]) -> list[OrchestratorResult]:
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
