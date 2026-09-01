"""Unified payment-provider contract. Verification is explicit; no provider is claimed live without an API."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import uuid

class PaymentStatus(str, Enum):
    CREATED="created"; PENDING="pending"; CONFIRMED="confirmed"; FAILED="failed"

@dataclass(frozen=True)
class PaymentReference:
    reference: str
    provider: str
    amount: float
    status: PaymentStatus

class PaymentProvider:
    name="abstract"
    def create(self, amount: float, metadata: dict | None = None) -> PaymentReference:
        if amount <= 0: raise ValueError("amount must be positive")
        return PaymentReference(uuid.uuid4().hex, self.name, amount, PaymentStatus.PENDING)
    def verify(self, reference: str) -> PaymentStatus:
        raise NotImplementedError("automatic verification is unavailable for this provider")

class VodafoneCashProvider(PaymentProvider):
    name="vodafone_cash"
    def __init__(self, number: str | None = None): self.number=number

class PaymobProvider(PaymentProvider):
    name="paymob"
    def __init__(self, configured: bool = False): self.configured=configured

__all__=["PaymentProvider","VodafoneCashProvider","PaymobProvider","PaymentReference","PaymentStatus"]
