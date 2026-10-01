from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    topic: str
    payload: dict[str, Any]
    created_at: str

class AgentCommunicationBus:
    def __init__(self) -> None:
        self.messages: list[AgentMessage] = []

    def send(self, sender: str, recipient: str, topic: str, payload: dict[str, Any]) -> AgentMessage:
        message = AgentMessage(sender, recipient, topic, payload, datetime.now(timezone.utc).isoformat())
        self.messages.append(message)
        return message

    def broadcast(self, sender: str, topic: str, payload: dict[str, Any], recipients: list[str]) -> list[AgentMessage]:
        return [self.send(sender, recipient, topic, payload) for recipient in recipients if recipient != sender]

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        return [m.__dict__ for m in self.messages[-limit:]]

    def status(self) -> dict[str, Any]:
        return {"messages": len(self.messages), "active": True, "mode": "agent-to-agent collaboration"}

agent_bus = AgentCommunicationBus()
