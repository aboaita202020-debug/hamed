"""Bounded autonomous authority for Hamed's commercial actions.

Hamed can operate autonomously for routine, reversible work. High-impact
financial/legal/account actions remain protected by server-side limits.
The model cannot change these limits.
"""
from dataclasses import dataclass
import os
from typing import Optional


@dataclass(frozen=True)
class AutonomyPolicy:
    # Autonomous routine operation is enabled by default.
    enabled: bool = os.getenv("HAMED_AUTONOMOUS_MODE", "true").lower() == "true"
    # Financial autonomy stays OFF unless the owner explicitly configures a limit.
    max_purchase_value: float = float(os.getenv("HAMED_MAX_PURCHASE_VALUE", "0"))
    max_payment_value: float = float(os.getenv("HAMED_MAX_PAYMENT_VALUE", "0"))
    max_discount_percent: float = float(os.getenv("HAMED_MAX_DISCOUNT_PERCENT", "20"))

    def allows(self, action: str, value: Optional[float] = None) -> bool:
        if not self.enabled:
            return False
        if action == "purchase":
            return value is not None and value >= 0 and value <= self.max_purchase_value
        if action in {"payment", "transfer"}:
            return value is not None and value >= 0 and value <= self.max_payment_value
        if action in {"contract", "account_change", "irreversible", "publish"}:
            return False
        # Routine/reversible work can proceed autonomously.
        return True


policy = AutonomyPolicy()
