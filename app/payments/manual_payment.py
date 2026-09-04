"""Secure manual-payment workflow for Hamed AI.

This module deliberately fails closed for production confirmation when no trusted
reviewer identity provider is configured. A reviewer id supplied by an HTTP
request body is never accepted as authentication.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
import os
import secrets
import string
from typing import Callable, Optional


class PaymentState(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PaymentError(Exception):
    """Base payment workflow error."""


class AuthorizationError(PaymentError):
    """Raised when the trusted reviewer identity is not authorized."""


class ProductionAuthUnavailable(AuthorizationError):
    """Raised when no trusted reviewer authentication mechanism exists."""


class InvalidTransition(PaymentError):
    """Raised when a payment state transition is not permitted."""


class PaymentNotFound(PaymentError):
    """Raised when a payment is not visible to the supplied customer."""


@dataclass(frozen=True)
class ReviewerIdentity:
    subject: str


@dataclass
class Payment:
    payment_id: str
    customer_id: str
    amount: float
    currency: str
    reference_code: str
    state: PaymentState = PaymentState.PENDING
    proof: Optional[str] = None
    reviewer: Optional[str] = None
    review_note: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    submitted_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("amount must be positive")
        if not self.currency or not self.currency.isalpha() or len(self.currency) != 3:
            raise ValueError("currency must be a 3-letter code")


class ManualPaymentService:
    """In-memory first-stage payment workflow with strict server-side gates.

    Storage is intentionally injected/replaceable. For real money, use durable
    transactional storage and a real authenticated reviewer identity provider.
    """

    def __init__(
        self,
        *,
        reviewer_authenticator: Optional[Callable[[object], Optional[ReviewerIdentity]]] = None,
        notifier: Optional[Callable[[Payment], None]] = None,
        clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        reference_factory: Optional[Callable[[], str]] = None,
    ) -> None:
        self._payments: dict[str, Payment] = {}
        self._audit: list[dict] = []
        self._reviewer_authenticator = reviewer_authenticator
        self._notifier = notifier
        self._clock = clock
        self._reference_factory = reference_factory or self._new_reference

    @property
    def audit_events(self) -> list[dict]:
        return list(self._audit)

    def create_payment(self, customer_id: str, amount: float, currency: str = "EGP", *, expires_hours: int = 24) -> Payment:
        if not customer_id:
            raise ValueError("customer_id is required")
        reference = self._unique_reference()
        now = self._clock()
        payment = Payment(
            payment_id=secrets.token_urlsafe(16),
            customer_id=customer_id,
            amount=float(amount),
            currency=currency.upper(),
            reference_code=reference,
            created_at=now,
            expires_at=now + timedelta(hours=expires_hours) if expires_hours > 0 else None,
        )
        self._payments[payment.payment_id] = payment
        self._audit_event("system", "payment_created", payment, "pending", {})
        return payment

    def get_customer_payment(self, payment_id: str, customer_id: str) -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None or payment.customer_id != customer_id:
            raise PaymentNotFound("payment not found")
        return payment

    def submit_proof(self, payment_id: str, customer_id: str, proof: str) -> Payment:
        payment = self.get_customer_payment(payment_id, customer_id)
        self._transition(payment, PaymentState.SUBMITTED)
        payment.proof = str(proof)[:2000]
        payment.submitted_at = self._clock()
        self._transition(payment, PaymentState.UNDER_REVIEW)
        self._audit_event("customer", "payment_submitted", payment, "under_review", {})
        if self._notifier:
            try:
                self._notifier(payment)
            except Exception as exc:
                self._audit.append({"actor": "system", "action": "notification_failed", "status": "error", "payment_id": payment.payment_id, "error_type": type(exc).__name__, "timestamp": self._clock().isoformat()})
        return payment

    def confirm(self, payment_id: str, auth_context: object, *, note: str = "") -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None:
            raise PaymentNotFound("payment not found")
        reviewer = self._authenticate_reviewer(auth_context)
        self._ensure_not_expired(payment)
        if payment.state != PaymentState.UNDER_REVIEW:
            raise InvalidTransition("only under_review payments can be confirmed")
        payment.state = PaymentState.CONFIRMED
        payment.reviewer = reviewer.subject
        payment.review_note = note[:1000]
        payment.reviewed_at = self._clock()
        self._audit_event(reviewer.subject, "payment_confirmed", payment, "confirmed", {"note": payment.review_note})
        return payment

    def reject(self, payment_id: str, auth_context: object, *, note: str = "") -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None:
            raise PaymentNotFound("payment not found")
        reviewer = self._authenticate_reviewer(auth_context)
        self._ensure_not_expired(payment)
        if payment.state != PaymentState.UNDER_REVIEW:
            raise InvalidTransition("only under_review payments can be rejected")
        payment.state = PaymentState.REJECTED
        payment.reviewer = reviewer.subject
        payment.review_note = note[:1000]
        payment.reviewed_at = self._clock()
        self._audit_event(reviewer.subject, "payment_rejected", payment, "rejected", {"note": payment.review_note})
        return payment

    def fulfill(self, payment_id: str) -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None:
            raise PaymentNotFound("payment not found")
        if payment.state != PaymentState.CONFIRMED:
            raise PaymentError("fulfillment blocked until payment is confirmed")
        return payment

    def record_revenue(self, payment_id: str) -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None:
            raise PaymentNotFound("payment not found")
        if payment.state != PaymentState.CONFIRMED:
            raise PaymentError("revenue recognition blocked until payment is confirmed")
        return payment

    def expire(self, payment_id: str) -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None:
            raise PaymentNotFound("payment not found")
        if payment.state in {PaymentState.PENDING, PaymentState.SUBMITTED, PaymentState.UNDER_REVIEW}:
            payment.state = PaymentState.EXPIRED
            self._audit_event("system", "payment_expired", payment, "expired", {})
        return payment

    def _authenticate_reviewer(self, auth_context: object) -> ReviewerIdentity:
        if self._reviewer_authenticator is None:
            raise ProductionAuthUnavailable("trusted reviewer authentication is not configured")
        identity = self._reviewer_authenticator(auth_context)
        if identity is None or not identity.subject:
            raise AuthorizationError("authenticated reviewer identity required")
        allowed = {x.strip() for x in os.getenv("HAMED_PAYMENT_REVIEWER_IDS", "").split(",") if x.strip()}
        if not allowed:
            raise AuthorizationError("reviewer allowlist is missing or empty")
        if identity.subject not in allowed:
            raise AuthorizationError("reviewer is not authorized")
        return identity

    def _ensure_not_expired(self, payment: Payment) -> None:
        if payment.expires_at and self._clock() >= payment.expires_at:
            payment.state = PaymentState.EXPIRED
            self._audit_event("system", "payment_expired", payment, "expired", {})
            raise InvalidTransition("payment has expired")

    @staticmethod
    def _transition(payment: Payment, target: PaymentState) -> None:
        allowed = {
            PaymentState.PENDING: {PaymentState.SUBMITTED},
            PaymentState.SUBMITTED: {PaymentState.UNDER_REVIEW},
            PaymentState.UNDER_REVIEW: {PaymentState.CONFIRMED, PaymentState.REJECTED},
        }
        if target not in allowed.get(payment.state, set()):
            raise InvalidTransition(f"invalid transition: {payment.state} -> {target}")
        payment.state = target

    def _unique_reference(self) -> str:
        for _ in range(10):
            candidate = self._reference_factory()
            if all(p.reference_code != candidate for p in self._payments.values()):
                return candidate
        raise PaymentError("could not allocate unique reference code")

    @staticmethod
    def _new_reference() -> str:
        alphabet = string.ascii_uppercase + string.digits
        return "HAMD" + "".join(secrets.choice(alphabet) for _ in range(6))

    def _audit_event(self, actor: str, action: str, payment: Payment, status: str, details: dict) -> None:
        self._audit.append({
            "actor": actor,
            "action": action,
            "status": status,
            "payment_id": payment.payment_id,
            "reference_code": payment.reference_code,
            "amount": payment.amount,
            "currency": payment.currency,
            "details": details,
            "timestamp": self._clock().isoformat(),
        })
