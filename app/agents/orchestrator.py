"""Hamed supervisor/orchestrator with a hard authorization boundary."""
from dataclasses import dataclass, field
from typing import Any

from .provider import AIProvider


SYSTEM_PROMPT = """You are Hamed AI, a professional commercial operations assistant.
Think independently, research and analyze, but never claim an external action happened unless a tool confirms it.
Never invent prices, suppliers, inventory, customer facts, delivery dates, or financial results.
High-impact actions such as purchases, payments, contracts, publishing, and irreversible changes require explicit approval outside the model.
Communicate naturally in Egyptian Arabic when the user writes Arabic, and use English when appropriate.
"""


@dataclass
class Session:
    messages: list[dict[str, str]] = field(default_factory=list)


class HamedOrchestrator:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider
        self.sessions: dict[str, Session] = {}

    def reset(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)

    def respond(self, session_id: str, user_text: str) -> str:
        if not user_text.strip():
            return "اكتب لي طلبك وسأساعدك."
        session = self.sessions.setdefault(session_id, Session())
        session.messages.append({"role": "user", "content": user_text.strip()})
        reply = self.provider.generate_response(session.messages[-40:], system=SYSTEM_PROMPT)
        session.messages.append({"role": "assistant", "content": reply})
        return reply

    @staticmethod
    def approval_required(action: str) -> bool:
        high_impact = {
            "purchase", "payment", "transfer", "contract", "publish",
            "account_change", "irreversible"
        }
        return action in high_impact
