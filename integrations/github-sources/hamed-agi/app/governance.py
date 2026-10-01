from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Approval:
    required: bool
    reason: str
    created_at: str

HIGH_IMPACT = {"purchase", "payment", "transfer", "contract", "legal_commitment", "send_money", "place_order", "financial_transaction"}

def approval_for(action: str, value: float | None = None) -> Approval:
    required = action.strip().lower() in HIGH_IMPACT or value is not None
    reason = "human approval required for financial or legally binding action" if required else "reversible/non-binding action"
    return Approval(required, reason, datetime.now(timezone.utc).isoformat())

def audit_event(action: str, status: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "action": action, "status": status, "details": details or {}}
