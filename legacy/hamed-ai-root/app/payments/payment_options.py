"""Unified customer-facing payment options for Hamed AI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PaymentMethod = Literal["paymob", "vodafone_cash", "instapay"]


@dataclass(frozen=True)
class PaymentOption:
    method: PaymentMethod
    label: str
    currency: str
    automated_confirmation: bool
    enabled: bool


def egypt_payment_options() -> list[PaymentOption]:
    """Return the Egypt payment menu without exposing credentials or secrets."""
    return [
        PaymentOption("paymob", "بطاقة / Checkout", "EGP", True, True),
        PaymentOption("vodafone_cash", "Vodafone Cash", "EGP", False, True),
        PaymentOption("instapay", "InstaPay", "EGP", False, True),
    ]


def get_payment_option(method: PaymentMethod) -> PaymentOption:
    for option in egypt_payment_options():
        if option.method == method:
            return option
    raise ValueError(f"Unsupported payment method: {method}")
