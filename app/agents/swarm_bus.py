"""In-process communication bus for the 2020-agent swarm."""
from __future__ import annotations
from datetime import datetime, timezone
from threading import Lock
from typing import Any

class SwarmBus:
    def __init__(self):
        self._messages: list[dict[str, Any]] = []
        self._lock = Lock()

    def publish(self, sender: str, topic: str, payload: Any) -> None:
        with self._lock:
            self._messages.append({
                "sender": sender,
                "topic": topic,
                "payload": payload,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })

    def recent(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._messages[-max(1, limit):])

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {"active": True, "messages": len(self._messages), "mode": "cooperative-agent-bus"}

swarm_bus = SwarmBus()
