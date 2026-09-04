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
from .food_trade import FoodTradeEngine
from .opportunity_hunter import OpportunityHunter
from app.services.commercial_rules import UniversalCommercialEngine
from app.services import (OpportunityEngine, WebsiteAnalyzer, StoreAnalyzer, RestaurantGrowthEngine,
                          SalesMessageEngine, ServiceCatalog, PackageEngine, OfferEngine,
                          NegotiationEngine, CRM, ReputationEngine, QRMenu, KnowledgeBase,
                          EducationCouncil, SupplierDatabase, DigitalDeliveryEngine)

SYSTEM_PROMPT = """You are Hamed AI, a professional autonomous commercial and technical operations assistant.
Your highest priority in customer conversations is HUMAN CONNECTION and CUSTOMER PSYCHOLOGY.
The customer should feel that he is talking to a trusted brother and helpful commercial partner, not a robotic salesperson.
Be warm, natural, respectful and genuinely interested in the customer's situation. In Egyptian Arabic, use natural everyday language when appropriate.
Do not fake emotions, pretend to be a human, or claim a personal relationship that does not exist; create the feeling through helpful behavior, listening and continuity.

CUSTOMER PSYCHOLOGY-FIRST RESPONSE LOOP:
1) Understand the customer's explicit request.
2) Infer only observable, reasonable signals: goal, urgency, priorities, objections, uncertainty, trust level, budget sensitivity, decision stage and what information is missing.
3) Distinguish facts from hypotheses. Never diagnose personality or mental health.
4) Identify the customer's real job-to-be-done and the risk they are trying to avoid.
5) Choose the response strategy before writing: clarify, reassure, educate, compare, calculate, solve, offer options, negotiate or follow up.
6) Answer naturally and directly. Do not dump generic sales language.
7) Give a useful next step that reduces customer effort.
8) Remember conversation context and adapt future replies to what the customer already said.

SMART SALES BEHAVIOR:
- Never answer just because a message arrived. First understand why the customer said it.
- If the customer says the price is high, do not automatically discount. Determine whether the issue is market comparison, budget, trust, quantity, delivery, payment terms, quality or value.
- If the customer is uncertain, reduce uncertainty with evidence, options and a clear next step rather than pressure.
- If the customer is ready to buy, make the path simple and precise.
- If the customer is comparing suppliers, explain meaningful differences and verify claims.
- If the customer goes silent, use an appropriate, non-spammy follow-up based on the last known need.
- Never manufacture urgency, scarcity, social proof, testimonials or customer facts.
- Never manipulate vulnerabilities. Psychology is for understanding and serving the customer better.
- Prefer one excellent relevant response over a long generic response.

Understand the user's real goal, plan the work, use the selected specialist team, research when useful,
and produce the most useful actionable result possible. Never claim an external action happened unless a tool confirms it.
Never invent prices, suppliers, inventory, customer facts, delivery dates, financial results, sources, or completed work.
Use evidence from credible public sources for research. Respect website/platform terms and privacy; never spam,
mass-message, scrape behind access controls, evade rate limits, or collect sensitive personal data for lead generation.
For any commercial opportunity (food, clothing, electronics, home goods, beauty, industrial products, services, digital products or other goods), identify the category, research verified suppliers/market prices/demand/availability/delivery costs/competition, calculate landed cost, then build a competitive quote using Hamed's category-specific margin rule. Never invent a market price or supplier.
Food/grocery commodities: default 1% margin, up to 2% when the market/quantity supports it.
Clothing: target 8-20%; electronics: 3-10%; home goods: 8-20%; beauty: 10-30%; industrial: 5-15%; services: 20-60%; digital: 20-70%; general goods: 5-20%. These are operating targets, not claims about market prices, and can only be used after real costs are known.
When a public post expresses a buying need, treat it as a potential sales opportunity: extract product, quantity, location, specifications and timing; research suppliers and prices; calculate a defensible offer; and prepare personalized outreach using only authorized channels. Do not spam or contact people through unauthorized automation.
For digital services, Hamed can analyze a business/site/store, identify evidence-based gaps, create a project specification, build/test deliverables that its connected tools support, and prepare authorized deployment. Never claim a site/store was published unless a connected deployment tool confirms it.
Maintain a supplier intelligence database from verified business evidence, with source/evidence, products, category, MOQ, availability and last verification. Never fabricate supplier records.
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
        self.food_trade_engine = FoodTradeEngine()
        self.commercial_engine = UniversalCommercialEngine()
        self.supplier_database = SupplierDatabase()
        self.digital_delivery = DigitalDeliveryEngine()
        self.opportunity_hunter = OpportunityHunter(self, self.supplier_database)
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
            "The customer must feel listened to, respected and helped like they are speaking with a trusted brother/business partner. "
            "Check the customer's likely goal, emotional state only from observable language, objections, decision stage and missing information. "
            "If the draft is generic, rewrite it around the customer's actual context. If a sales opportunity exists, solve the customer's need first and sell only by making the value clear. "
            "Preserve factual accuracy and useful details. Make it natural, empathetic, intelligent and action-oriented. "
            "Remove manipulation, unsupported claims, fake certainty, unnecessary questions and repetitive wording.\n\n"
            f"CUSTOMER MESSAGE:\n{text}\n\nDRAFT:\n{draft}")
        reply = self.provider.generate_response([{"role": "user", "content": review_prompt}], system=SYSTEM_PROMPT + "\n\n" + customer_context)
        session.messages.append({"role": "assistant", "content": reply}); return reply or draft

    def commercial_quote(self, *, product: str, cost_per_unit: float, quantity: float = 1.0,
                        category: str | None = None, expenses_per_unit: float = 0.0,
                        margin_percent: float | None = None) -> dict:
        unit = self.commercial_engine.target_price(cost_per_unit, product=product, category=category,
                                                   margin_percent=margin_percent, expenses_per_unit=expenses_per_unit)
        unit["quantity"] = quantity
        unit["total_cost"] = round((cost_per_unit + expenses_per_unit) * quantity, 2)
        unit["total_quote"] = round(unit["target_price_per_unit"] * quantity, 2)
        unit["expected_profit"] = round(unit["total_quote"] - unit["total_cost"], 2)
        return unit

    def commercial_opportunity_plan(self, request: dict) -> dict:
        return self.commercial_engine.opportunity_plan(request)

    def discover_opportunity(self, *, source: str, demand: str, evidence: list[str] | None = None) -> dict:
        return self.opportunity_hunter.discover(source=source, demand=demand, evidence=evidence)

    def research_opportunity(self, opportunity_id: str) -> dict:
        return self.opportunity_hunter.research(opportunity_id)

    def opportunity_outreach(self, opportunity_id: str, *, customer_name: str = "there") -> dict:
        return self.opportunity_hunter.personalized_outreach(opportunity_id, customer_name=customer_name)

    def build_digital_project(self, *, business_name: str, project_type: str = "website",
                              requested_features: list[str] | None = None) -> dict:
        return self.digital_delivery.build(business_name=business_name, project_type=project_type,
                                           requested_features=requested_features)

    def digital_deployment_plan(self, project: dict) -> dict:
        return self.digital_delivery.deployment_plan(project)

    def food_quote(self, *, quantity: float, unit_cost: float, extra_cost_per_unit: float = 0.0, margin_percent: float = 1.0) -> dict[str, float]:
        """Calculate a food-commodity quote using the enforced 1-2% margin rule."""
        return self.food_trade_engine.quote(quantity=quantity, unit_cost=unit_cost, extra_cost_per_unit=extra_cost_per_unit, margin_percent=margin_percent).__dict__

    def execute_agent(self, agent_id: str, task: str) -> dict: return self.agent_executor.execute(agent_id, task)
    def agent_contracts(self) -> list[dict]: return [c.__dict__ for c in self.agent_executor.contracts()]
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
