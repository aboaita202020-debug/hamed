"""Central coordinator for Hamed AGI revenue expansion and autonomous opportunity discovery."""
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
from .opportunity_machine_agent import OpportunityMachineAgent
from .customer_relationship_agent import CustomerRelationshipAgent
from .customer_psychology_agent import CustomerPsychologyAgent
from .customer_acquisition_agent import CustomerAcquisitionAgent
from .customer_conversation_agent import CustomerConversationAgent
from .offer_compiler_agent import OfferCompilerAgent
from .revenue_compiler_agent import RevenueCompilerAgent
from .marketing_campaign_agent import MarketingCampaignAgent
from .freelance_revenue_agent import FreelanceRevenueAgent
from .video_commerce_agent import VideoCommerceAgent
from .video_production_agent import VideoProductionAgent
from .service_compiler_agent import ServiceCompilerAgent
from .revenue_opportunity_suite_agent import RevenueOpportunitySuiteAgent
from .revenue_expansion_suite_agent import RevenueExpansionSuiteAgent
from .business_opportunity_factory_agent import BusinessOpportunityFactoryAgent
from .revenue_infrastructure_suite_agent import RevenueInfrastructureSuiteAgent
from .universal_customer_execution_agent import UniversalCustomerExecutionAgent
from .universal_human_opportunity_agent import UniversalHumanOpportunityAgent
from .website_ecommerce_intelligence_agent import WebsiteEcommerceIntelligenceAgent
from .million_idea_agent import MillionIdeaAgent
from .revenue_path_agent import RevenuePathAgent
from .income_ideas_agent import IncomeIdeasAgent
from .business_asset_network_agent import BusinessAssetNetworkAgent
from .economic_intelligence_agent import EconomicIntelligenceAgent
from .sales_agent import SalesAgent
from .negotiation_agent import NegotiationAgent
from .revenue_agent import RevenueAgent
from .reporting_agent import ReportingAgent
from .fact_check_agent import FactCheckAgent
from .brain_council import BrainCouncil, BRAIN_ROLES
from .workflow import PendingAction, prepare_action
from .swarm_agents import SwarmAgent, build_swarm_specs
from app.agent_bus import agent_bus
logger = get_logger(__name__)

@dataclass
class OrchestratorResult:
    agent: str
    result: AgentResult
    attempts: int = 1

@dataclass
class SessionState:
    messages: list[dict[str, str]] = field(default_factory=list)
    pending_actions: dict[str, PendingAction] = field(default_factory=dict)

class HamedOrchestrator:
    def __init__(self, db: Optional[Database] = None, search_provider: Optional[SearchProvider] = None, max_retries: int = 2, brain_provider=None):
        if db is not None and not isinstance(db, Database) and brain_provider is None:
            brain_provider = db; db = None
        self.db = db or get_database(); self.repo = Repository(self.db); self.permissions = PermissionLayer(self.repo)
        self.tools = ToolRegistry(self.permissions); self.max_retries = max_retries; self.brain_provider = brain_provider
        self.brain_council = BrainCouncil(brain_provider) if brain_provider is not None else None
        self.tools.register(WebSearchTool(provider=search_provider)); self.tools.register(CRMTool(self.repo)); self.agents: dict[str, BaseAgent] = {}
        self.sessions: dict[str, SessionState] = {}
        for agent_cls in (OpportunityHunterAgent, OpportunityMachineAgent, CustomerRelationshipAgent, CustomerPsychologyAgent, CustomerAcquisitionAgent, CustomerConversationAgent, OfferCompilerAgent, RevenueCompilerAgent, MarketingCampaignAgent, FreelanceRevenueAgent, VideoCommerceAgent, VideoProductionAgent, ServiceCompilerAgent, RevenueOpportunitySuiteAgent, RevenueExpansionSuiteAgent, BusinessOpportunityFactoryAgent, RevenueInfrastructureSuiteAgent, UniversalCustomerExecutionAgent, UniversalHumanOpportunityAgent, WebsiteEcommerceIntelligenceAgent, MillionIdeaAgent, RevenuePathAgent, IncomeIdeasAgent, BusinessAssetNetworkAgent, EconomicIntelligenceAgent, SalesAgent, NegotiationAgent, RevenueAgent, ReportingAgent, FactCheckAgent):
            self.register_agent(agent_cls(self.tools, self.repo))
        # Keep the original specialist agents and add a large logical swarm.
        # The swarm agents are executable workers backed by the same model router;
        # they are not fake names or separate OS processes.
        existing = set(self.agents)
        for spec in build_swarm_specs(existing, target=2020):
            self.register_agent(SwarmAgent(self.tools, self.repo, spec, brain_provider=self.brain_provider))

    def register_agent(self, agent: BaseAgent) -> None: self.agents[agent.name] = agent
    def session(self, session_id: str) -> SessionState: return self.sessions.setdefault(session_id, SessionState())

    def respond(self, session_id: str, message: str) -> str:
        """Unified text channel: preserve conversation context and use the central brain."""
        state = self.session(session_id); state.messages.append({"role": "user", "content": message})
        system = ("أنت حامد AGI، نظام تشغيل تجاري مستقل. ساعد المستخدم بالعربية المهنية. "
                  "ابحث وحلل وخطط، لكن لا تدّعِ تنفيذ شراء أو دفع أو تعاقد أو نشر دون نتيجة مؤكدة وموافقة لازمة. "
                  "ميّز الحقائق عن التقديرات وعرّف نفسك كذكاء اصطناعي عند الحاجة.")
        if self.brain_provider is None:
            reply = "أنا حامد AGI. أستطيع تحليل الهدف وتحويله إلى بحث وفرص وخطة تنفيذ آمنة، لكن لا يوجد مزود نموذج مفعّل حاليًا."
        else:
            try:
                reply = self.brain_provider.generate_response(state.messages[-12:], system=system)
            except Exception as exc:
                logger.warning("chat provider unavailable: %s", exc)
                reply = "حاليًا لا أستطيع الوصول إلى محرك الذكاء المتاح. تم حفظ طلبك ويمكن إعادة المحاولة لاحقًا."
        state.messages.append({"role": "assistant", "content": reply}); return reply

    def prepare_high_impact_action(self, session_id: str, action: str, description: str, value: float | None = None) -> str:
        state = self.session(session_id); pending = prepare_action(action, description, value); state.pending_actions[action] = pending
        if pending.approval is None: return "الإجراء مصنف منخفض المخاطر ويمكن متابعته ضمن الصلاحيات الحالية."
        return "تم إنشاء طلب موافقة. لن يتم التنفيذ قبل الموافقة الصريحة."

    def dispatch(self, agent_name: str, payload: dict) -> OrchestratorResult:
        if agent_name not in self.agents: return OrchestratorResult(agent_name, AgentResult(success=False, error=f"unknown_agent:{agent_name}"))
        attempts = 0; last_result: Optional[AgentResult] = None
        while attempts < max(1, self.max_retries):
            attempts += 1; run_id = self.repo.start_agent_run(agent_name, str(payload)[:500])
            try:
                last_result = self.agents[agent_name].run(payload); self.repo.finish_agent_run(run_id, "DONE" if last_result.success else "FAILED", error=last_result.error)
                if last_result.success: break
            except Exception as exc:
                logger.exception("Agent '%s' raised an unhandled exception", agent_name); self.repo.finish_agent_run(run_id, "FAILED", error=str(exc)); last_result = AgentResult(success=False, error=str(exc))
            if attempts < self.max_retries: time.sleep(0.05)
        return OrchestratorResult(agent_name, last_result, attempts)

    def swarm_status(self) -> dict:
        departments = {}
        for agent in self.agents.values():
            department = getattr(agent, "spec", None)
            department = getattr(department, "department", "core")
            departments[department] = departments.get(department, 0) + 1
        return {
            "total_agents": len(self.agents),
            "target_agents": 2020,
            "target_reached": len(self.agents) == 2020,
            "departments": departments,
            "provider_available": self.brain_provider is not None,
            "communication_bus": "shared agent context + persisted agent runs",
        }

    def run_swarm(self, objective: str, agent_names: Optional[list[str]] = None, limit: int | None = None) -> dict:
        names = agent_names or list(self.agents)
        if limit is not None:
            names = names[:max(0, int(limit))]
        peer_findings = {}
        results = []
        for name in names:
            outcome = self.dispatch(name, {
                "objective": objective,
                "context": {"swarm_size": len(self.agents), "cooperation": True},
                "peer_findings": peer_findings,
            })
            item = {
                "agent": outcome.agent,
                "success": outcome.result.success,
                "data": outcome.result.data,
                "error": outcome.result.error,
            }
            results.append(item)
            if outcome.result.success:
                peer_findings[name] = outcome.result.data
                agent_bus.publish(name, "swarm_finding", outcome.result.data)
        return {
            "objective": objective,
            "agents_requested": len(names),
            "agents_completed": sum(1 for item in results if item["success"]),
            "results": results,
            "peer_findings": len(peer_findings),
        }

    def brain_roster(self) -> list[dict[str, str]]: return [{"name": role.name, "specialty": role.specialty} for role in BRAIN_ROLES]
    def consult_brains(self, task: str, context: str = "", roles: Optional[list[str]] = None) -> dict:
        if self.brain_council is None: return {"success": False, "error": "brain_provider_not_configured", "brains": self.brain_roster()}
        return {"success": True, **self.brain_council.deliberate(task, context, roles)}
    def run_pipeline(self, steps: list[tuple[str, dict]]) -> list[OrchestratorResult]:
        results = []
        for agent_name, payload in steps:
            outcome = self.dispatch(agent_name, payload); results.append(outcome)
            if not outcome.result.success: logger.info("Pipeline stopped at '%s': %s", agent_name, outcome.result.error); break
        return results
    def dashboard(self) -> dict: return self.dispatch("reporting_agent", {}).result.data or {}
