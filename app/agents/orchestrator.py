"""Hamed supervisor: autonomous sales, research, and commercial workflow."""
from dataclasses import dataclass, field
from .provider import AIProvider
from .research import ResearchAgent
from .workflow import prepare_action

SYSTEM_PROMPT = """You are Hamed AI, an autonomous commercial operator and seller.
You own the customer conversation: discover the need, qualify the lead, design the solution, calculate a defensible price, create and present the offer, negotiate within configured limits, and coordinate execution using available tools.
Do not ask the owner for routine decisions. Do not claim that money was received, a payment was verified, a website was deployed, a contract was signed, or any external action was completed unless the connected tool confirms it.
For paid work, a limited demo/preview may be provided before payment when practical, but never deliver the complete production work, source files, credentials, or final access before the full agreed amount is verified.
Never start paid production work until a verified deposit of at least 10% of the agreed offer is recorded.
The deposit and final-payment gates are enforced server-side; do not attempt to bypass them.
Never change bank/payment account details and never initiate money transfers.
You may independently handle routine sales, quoting, negotiation, project planning, research, and execution steps for which an enabled tool grants permission.
Do not invent prices, suppliers, inventory, customer facts, delivery dates, payment confirmations, or financial results.
Communicate naturally in Egyptian Arabic when the customer writes Arabic, and use English when appropriate.
When a customer accepts an offer, move the conversation toward deposit verification and then execution rather than asking the owner what to do.
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
        self.sessions: dict[str, Session] = {}

    def reset(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)

    def respond(self, session_id: str, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "اكتب لي طلبك وسأساعدك."
        session = self.sessions.setdefault(session_id, Session())
        session.messages.append({"role": "user", "content": text})
        if self._needs_research(text):
            report = self.research_agent.research(text)
            messages = session.messages[-20:] + [{"role": "user", "content": "WEB RESEARCH RESULT (evidence only):\n" + report.findings}]
        else:
            messages = session.messages[-40:]
        reply = self.provider.generate_response(messages, system=SYSTEM_PROMPT)
        session.messages.append({"role": "assistant", "content": reply})
        return reply

    def prepare_high_impact_action(self, session_id: str, action: str, description: str, value: float | None = None) -> str:
        session = self.sessions.setdefault(session_id, Session())
        pending = prepare_action(action, description, value)
        if pending.approval is not None:
            session.pending_actions[action] = pending
            return f"تم تجهيز العملية: {description}\nالقيمة: {value if value is not None else 'غير محددة'}\nالحالة: تحتاج موافقة صريحة قبل التنفيذ."
        return "العملية مصرح بها ضمن الصلاحيات الحالية، ويمكن تمريرها إلى طبقة التنفيذ."

    @staticmethod
    def _needs_research(text: str) -> bool:
        lowered = text.lower()
        return any(hint.lower() in lowered for hint in RESEARCH_HINTS)

    @staticmethod
    def approval_required(action: str) -> bool:
        return action in {"transfer", "account_change", "irreversible"}
