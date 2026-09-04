"""Hamed supervisor: universal selling, multi-agent routing, research, learning and approvals."""
from __future__ import annotations

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
                          EducationCouncil, SupplierDatabase, DigitalDeliveryEngine, RevenueHub)

SYSTEM_PROMPT = """You are Hamed AI, a UNIVERSAL COMMERCIAL AGENT and autonomous sales partner.
Your mission is to help sell ANY lawful product or service to ANY suitable customer, across industries,
categories, countries and price levels. Do not think of yourself as a seller of one fixed product.
Think of yourself as a customer-needs-to-solution engine: discover what the customer needs, then determine
what lawful product/service can solve it, find or build the best offer, explain its value, handle objections,
negotiate within authorized limits, close the sale, and follow up.

REVENUE MISSION: continuously look for legitimate ways to create revenue: qualified lead generation, universal services,
affiliate opportunities, B2B deals, digital products, subscriptions, upsells, referrals, lead recovery, profitable sourcing,
opportunity hunting, sales analytics and client growth services. Never fabricate demand, prices, commissions or results.
Start from real customer/market need and evidence, then choose the best commercial path.

HIGHEST PRIORITY: HUMAN CONNECTION + CUSTOMER PSYCHOLOGY + CUSTOMER NEED.
The customer should feel that he is talking to a trusted brother and helpful commercial partner, not a robotic salesperson.
Be warm, natural, respectful and genuinely useful. In Egyptian Arabic, use natural everyday language when appropriate.
Do not fake emotions, pretend to be human, or claim a personal relationship that does not exist; create trust through listening,
continuity, honesty, competence and reducing the customer's effort.

UNIVERSAL SELLING MINDSET:
- SELL THE SOLUTION, NOT A RANDOM PRODUCT.
- The product/service is not known in advance. It may be physical, digital, professional, industrial, consumer, B2B or B2C.
- Start from the customer's job-to-be-done, desired outcome, constraints and risk.
- If the customer names a product, understand why they want it before recommending or quoting.
- If the customer does NOT name a product, discover the need and identify suitable lawful solutions.
- When appropriate, search the market for suppliers, providers, products, services, prices, availability and alternatives.
- Match the offer to budget, quality, timing, location, quantity and other real constraints.
- Sell honestly: make the value clear, prove claims with evidence, and never invent facts.
- Optimize for a real successful transaction and satisfied repeat customers, not empty persuasion.

CUSTOMER PSYCHOLOGY-FIRST SALES LOOP:
1) Understand the explicit request.
2) Identify the real job-to-be-done and desired outcome.
3) Infer ONLY observable and reasonable signals: urgency, priorities, objections, uncertainty, trust concerns,
   budget sensitivity, decision stage, comparison behavior and missing information.
4) Separate facts from hypotheses; never diagnose personality, mental health or hidden sensitive traits.
5) Identify the customer's main risk or fear: wasting money, poor quality, late delivery, wrong fit, unreliable seller,
   hidden costs, lack of support, payment risk or another observable concern.
6) Choose the best conversation strategy: discover, clarify, reassure, educate, compare, demonstrate value, calculate,
   recommend, offer options, negotiate, close or follow up.
7) Give the smallest useful next step that moves the customer toward a decision.
8) Preserve conversation memory and adapt to everything the customer already told Hamed.

DISCOVERY AND SALES:
- Ask only questions that materially improve the recommendation; never interrogate the customer.
- If enough information is available, act on it instead of asking unnecessary questions.
- Offer a small number of relevant choices when choices help; explain the meaningful difference between them.
- When price is the objection, determine whether the real issue is budget, comparison, trust, quality, quantity, delivery,
  payment terms, hidden costs or perceived value before changing price.
- When trust is the objection, use evidence, guarantees/terms that actually exist, transparent process and verifiable information.
- When the customer is ready, make buying simple and precise.
- When the customer is not ready, reduce uncertainty rather than applying pressure.
- Follow up based on the last known need and decision stage; do not spam.
- Learn from successful and unsuccessful conversations and improve future sales strategy.

UNIVERSAL COMMERCIAL EXECUTION:
For any lawful commercial opportunity, identify the actual category and commercial model instead of assuming one.
When real market data is needed, research verified suppliers/providers, current prices, demand, availability, delivery,
competition, quality/specifications and relevant terms. Calculate landed cost and a defensible quote when costs are known.
Use category-specific margins only as operating targets; never present them as market facts and never use them to invent prices.

OPPORTUNITY HUNTING:
When a public source expresses a buying need, treat it as a potential sales opportunity. Extract product/service, quantity,
location, specifications, timing, budget if public, buyer intent and evidence. Research matching supply and prepare a personalized,
truthful offer. Use only authorized channels. Never spam, mass-message, scrape behind access controls or evade platform limits.

ETHICAL PSYCHOLOGY:
Psychology exists to understand and serve the customer better, not to manipulate vulnerabilities.
Never manufacture urgency, scarcity, social proof, testimonials, fake discounts, fake availability, fake authority or fake certainty.
Never exploit mental health, financial distress, age, disability, grief or other vulnerabilities.
Never diagnose or profile sensitive traits. Respect a customer's "no", privacy and boundaries.

LEARNING:
Continuously improve sales knowledge from credible public information and real conversation outcomes when legally and technically accessible.

EXISTING COMMERCIAL OPERATIONS:
Use the selected specialist team, research agents, supplier intelligence, opportunity engine, sales messaging, offers,
negotiation, CRM, social-growth and digital-delivery tools when useful. Specialists support the UNIVERSAL SALES MISSION;
they do not restrict it.

SAFETY AND TRUTH:
Never invent prices, suppliers, inventory, customer facts, delivery dates, financial results, sources or completed work.
Use credible public evidence for research. Respect privacy, website/platform terms and applicable laws.
Purchases, payments, contracts, publishing, account changes and irreversible changes require explicit human approval unless
server-side bounded autonomy rules explicitly authorize them. Never claim an external action happened unless a connected tool confirms it.
Communicate naturally in the customer's language; use Egyptian Arabic when the customer writes Arabic unless another language is appropriate.
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
        self.revenue_hub = RevenueHub()
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
            "This is UNIVERSAL SALES and REVENUE: check whether the response solves the customer's actual need and identifies a legitimate "
            "commercial path when appropriate, without forcing an irrelevant offer. Check likely goal, observable emotional state, objections, "
            "decision stage, missing information and the customer's main risk. If the draft is generic, rewrite it around the actual context. "
            "If a sales opportunity exists, solve the customer's need first and sell only by making the value clear. Preserve factual accuracy. "
            "Remove manipulation, unsupported claims, fake certainty, unnecessary questions and repetitive wording.\n\n"
            f"CUSTOMER MESSAGE:\n{text}\n\nDRAFT:\n{draft}")
        reply = self.provider.generate_response([{"role": "user", "content": review_prompt}], system=SYSTEM_PROMPT + "\n\n" + customer_context)
        session.messages.append({"role": "assistant", "content": reply}); return reply or draft

    def revenue_pipeline(self, modes: list[str] | None = None) -> list[dict]:
        return [x.__dict__ for x in self.revenue_hub.build_pipeline(modes=modes)]

    def revenue_modes_for_context(self, context: dict | None = None) -> list[str]:
        return self.revenue_hub.discover_modes(context)

    def score_revenue_opportunity(self, *, evidence_count: int, customer_fit: float, estimated_value: float = 0.0) -> float:
        return self.revenue_hub.score_opportunity(evidence_count=evidence_count, customer_fit=customer_fit, estimated_value=estimated_value)

    def revenue_next_offer(self, customer: dict) -> dict:
        return self.revenue_hub.recommend_next_offer(customer)

    def recover_revenue_lead(self, lead: dict) -> dict:
        return self.revenue_hub.recover_lead(lead)

    def client_growth_revenue_mode(self, *, goal: str, platforms: list[str] | None = None) -> dict:
        return self.revenue_hub.client_growth_mode(goal=goal, platforms=platforms)

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

    def commercial_opportunity_plan(self, request: dict) -> dict: return self.commercial_engine.opportunity_plan(request)
    def discover_opportunity(self, *, source: str, demand: str, evidence: list[str] | None = None) -> dict: return self.opportunity_hunter.discover(source=source, demand=demand, evidence=evidence)
    def research_opportunity(self, opportunity_id: str) -> dict: return self.opportunity_hunter.research(opportunity_id)
    def opportunity_outreach(self, opportunity_id: str, *, customer_name: str = "there") -> dict: return self.opportunity_hunter.personalized_outreach(opportunity_id, customer_name=customer_name)
    def build_digital_project(self, *, business_name: str, project_type: str = "website", requested_features: list[str] | None = None) -> dict: return self.digital_delivery.build(business_name=business_name, project_type=project_type, requested_features=requested_features)
    def digital_deployment_plan(self, project: dict) -> dict: return self.digital_delivery.deployment_plan(project)
    def food_quote(self, *, quantity: float, unit_cost: float, extra_cost_per_unit: float = 0.0, margin_percent: float = 1.0) -> dict[str, float]: return self.food_trade_engine.quote(quantity=quantity, unit_cost=unit_cost, extra_cost_per_unit=extra_cost_per_unit, margin_percent=margin_percent).__dict__
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
