"""Minimal structured audit events."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json


@dataclass(frozen=True)
class AuditEvent:
    actor: str
    action: str
    status: str
    details: dict
    timestamp: str

    @classmethod
    def create(cls, actor: str, action: str, status: str, details: dict | None = None) -> "AuditEvent":
        return cls(actor, action, status, details or {}, datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
