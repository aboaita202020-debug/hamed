from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def daily_report(core: dict[str, Any], opportunities: list[dict[str, Any]], customers: dict[str, Any], revenue: dict[str, Any]) -> dict[str, Any]:
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "system": core, "opportunities": opportunities,
            "customers": customers, "revenue": revenue,
            "execution_policy": "financial_and_legal_actions_require_human_approval"}
