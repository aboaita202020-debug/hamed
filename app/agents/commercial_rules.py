"""Server-side commercial rules for Hamed AI.

These rules are intentionally deterministic: the AI may propose an action, but
payment gates are enforced by application code.
"""
from __future__ import annotations

from dataclasses import dataclass

MIN_DEPOSIT_PERCENT = 10.0


@dataclass(frozen=True)
class PaymentStatus:
    offer_value: float
    verified_amount: float

    @property
    def deposit_required(self) -> float:
        return self.offer_value * (MIN_DEPOSIT_PERCENT / 100.0)

    @property
    def deposit_verified(self) -> bool:
        return self.verified_amount >= self.deposit_required

    @property
    def full_payment_verified(self) -> bool:
        return self.verified_amount >= self.offer_value


def can_start_work(offer_value: float, verified_amount: float) -> bool:
    """Work starts only after a verified deposit of at least 10%."""
    return PaymentStatus(offer_value, verified_amount).deposit_verified


def can_final_deliver(offer_value: float, verified_amount: float) -> bool:
    """Final delivery requires verified payment of the complete agreed amount."""
    return PaymentStatus(offer_value, verified_amount).full_payment_verified


def demo_allowed() -> bool:
    """A limited demo is allowed before payment, but is never final delivery."""
    return True
