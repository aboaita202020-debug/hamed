"""Bounded autonomous authority for Hamed's commercial actions.

Autonomy is enabled explicitly through environment configuration. The model never
gets to change these limits; the server-side execution guard enforces them.
"""
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AutonomyPolicy:
    enabled: bool = os.getenv("HAMED_AUTONOMOUS_MODE", "false").lower() == "true"
    max_purchase_value: float = float(os.getenv("HAMED_MAX_PURCHASE_VALUE", "0"))
    max_payment_value: float = float(os.getenv("HAMED_MAX_PAYMENT_VALUE", "0"))
    max_discount_percent: float = float(os.getenv("HAMED_MAX_DISCOUNT_PERCENT", "20"))

    def allows(self, action: str, value: float | None = None) -> bool:
        if not self.enabled:
            return False
        if action == "purchase":
            return value is not None and value >= 0 and value <= self.max_purchase_value
        if action in {"payment", "transfer"}:
            return value is not None and value >= 0 and value <= self.max_payment_value
        if action == "contract":
            return False
        if action in {"account_change", "irreversible"}:
            return False
        if action == "publish":
            return False
        return True


policy = AutonomyPolicy()
