from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ComponentStatus:
    name: str
    status: str = "ok"
    details: dict[str, Any] = field(default_factory=dict)

class HAMEDCore:
    def __init__(self) -> None:
        self.started_at = datetime.now(timezone.utc)
        self.components: dict[str, ComponentStatus] = {}
    def register(self, name: str, status: str = "ok", **details: Any) -> None:
        self.components[name] = ComponentStatus(name, status, details)
    def health(self) -> dict[str, Any]:
        failed = [c.name for c in self.components.values() if c.status != "ok"]
        return {"status": "ok" if not failed else "degraded", "failed_components": failed, "components": {n: c.status for n, c in self.components.items()}}
    def readiness(self) -> dict[str, Any]:
        h = self.health()
        return {"ready": h["status"] == "ok", **h}

core = HAMEDCore()
