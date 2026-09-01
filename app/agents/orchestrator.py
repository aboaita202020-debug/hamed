"""Hamed supervisor: multi-agent routing, research, learning and approvals."""
from dataclasses import dataclass, field
from .provider import AIProvider
from .research import ResearchAgent
from .workflow import prepare_action
from .router import AgentRouter
from .learning import LearningCouncil
from .customer_intelligence import CustomerIntelligence
from .registry import AGENT_REGISTRY, CLIENT_RESEARCH_AGENTS, LEARNING_COUNCIL
from .execution import AgentExecutor
from app.services import OpportunityEngine, WebsiteAnalyzer, StoreAnalyzer, RestaurantGrowthEngine, SalesMessageEngine, ServiceCatalog, PackageEngine, OfferEngine, NegotiationEngine, CRM, ReputationEngine, QRMenu, KnowledgeBase, EducationCouncil

SYSTEM_PROMPT = """You are Hamed AI, a professional autonomous commercial and technical operations assistant.
Understand the user's real goal, plan the work, use the selected specialist team, research when useful,
and produce the most useful actionable result possible. Never claim an external action happened unless a tool confirms it.
Never invent prices, suppliers, inventory, customer facts, delivery dates, financial results, sources, or completed work.
Use evidence from credible public sources for research. Respect website/platform terms and privacy; never spam,
mass-message, scrape behind access controls, evade rate limits, or collect sensitive personal data for lead generation.
Psychology is for understanding observable communication and customer needs, not diagnosis or manipulation.
Before answering a customer, prioritize their stated goal, identify relevant objections, adapt tone and detail,
and provide a concrete useful next step. Do not pressure, deceive, manufacture urgency, or exploit vulnerabilities.
High-impact actions such as purchases, payments, contracts, publishing, account changes and irreversible changes require explicit human approval.
Communicate naturally in Egyptian Arabic when the user writes Arabic, and use English when appropriate.
"""
RESEARCH_HINTS = ("ابحث", "دورلي", "دور لي", "مورد", "موردين", "موردون", "سعر السوق", "أسعار", "سعر", "منتج مربح", "فرصة", "supplier", "suppliers", "market price", "product opportunity", "find products", "research")

@dataclass
class Session:
    messages: list[dict[str, str]] = field(default_factory=list)
    pending_actions: dict[str, object] = field(default_factory=dict)

class HamedOrchestrator:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider
        self.research_agent = ResearchAgent(provider)
        self.learning_council = LearningCouncil(provider)
        self.router = AgentRouter()
        self.customer_intelligence = CustomerIntelligence()
        self.agent_executor = AgentExecutor()
        self.opportunity_engine = OpportunityEngine()
        self.website_analyzer = WebsiteAnalyzer()
        self.store_analyzer = StoreAnalyzer()
        self.restaurant_engine = RestaurantGrowthEngine()
        self.sales_message_engine = SalesMessageEngine()
        self.service_catalog = ServiceCatalog()
        self.package_engine = PackageEngine()
        self.offer_engine = OfferEngine()
        self.negotiation_engine = NegotiationEngine()
        self.crm = CRM()
        self.reputation_engine = ReputationEngine()
        self.knowledge_base = KnowledgeBase()
        self.education_council = EducationCouncil()
        self.sessions: dict[str, Session] = {}

    def reset(self, session_id: str) -> None: self.sessions.pop(session_id, None)
    def respond(self, session_id: str, user_text: str) -> str:
        text = user_text.strip()
        if not text: return "اكتب لي طلبك وسأساعدك."
        session = self.sessions.setdefault(session_id, Session()); session.messages.append({"role": "user", "content": text})
        specialist_context = self.router.system_context(text); customer_context = self.customer_intelligence.prompt_context(text)
        if self._needs_research(text):
            report = self.research_agent.research(text)
            messages = session.messages[-20:] + [{"role": "user", "content": "WEB RESEARCH RESULT (evidence only):\n" + report.findings}]
        else: messages = session.messages[-40:]
        draft = self.provider.generate_response(messages, system=SYSTEM_PROMPT + "\n\n" + specialist_context + "\n\n" + customer_context)
        review_prompt = ("Review the draft response below before it is sent to the customer. Return only the improved final response. "
            "Preserve factual accuracy and useful details. Make it natural, empathetic, intelligent and action-oriented. "
            "Remove manipulation, unsupported claims, fake certainty, unnecessary questions and repetitive wording.\n\n"
            f"CUSTOMER MESSAGE:\n{text}\n\nDRAFT:\n{draft}")
        reply = self.provider.generate_response([{"role": "user", "content": review_prompt}], system=SYSTEM_PROMPT + "\n\n" + customer_context)
        session.messages.append({"role": "assistant", "content": reply}); return reply or draft

    def execute_agent(self, agent_id: str, task: str) -> dict:
        return self.agent_executor.execute(agent_id, task)
    def agent_contracts(self) -> list[dict]:
        return [c.__dict__ for c in self.agent_executor.contracts()]
    def research_for_learning(self, topic: str) -> str: return self.learning_council.research(topic).evidence
    def available_agents(self) -> list[str]: return [p.name for p in AGENT_REGISTRY.values()]
    def learning_agents(self) -> tuple[str, ...]: return LEARNING_COUNCIL
    def client_research_agents(self) -> tuple[str, ...]: return CLIENT_RESEARCH_AGENTS
    def prepare_high_impact_action(self, session_id: str, action: str, description: str, value: float | None = None) -> str:
        session = self.sessions.setdefault(session_id, Session()); pending = prepare_action(action, description, value)
        if pending.approval is not None:
            session.pending_actions[action] = pending
            return f"تم تجهيز العملية: {description}\nالقيمة: {value if value is not None else 'غير محددة'}\nالحالة: تحتاج موافقة صريحة قبل التنفيذ."
        return "العملية مصرح بها ضمن الصلاحيات الحالية، ويمكن تمريرها إلى طبقة التنفيذ."
    @staticmethod
    def _needs_research(text: str) -> bool: return any(h.lower() in text.lower() for h in RESEARCH_HINTS)
    @staticmethod
    def approval_required(action: str) -> bool: return action in {"purchase", "payment", "transfer", "contract", "publish", "account_change", "irreversible"}
