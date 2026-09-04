import os
from datetime import datetime, timedelta, timezone

import pytest

from app.payments.manual_payment import (
    AuthorizationError,
    InvalidTransition,
    ManualPaymentService,
    PaymentError,
    PaymentState,
    ProductionAuthUnavailable,
    ReviewerIdentity,
)


def reviewer_auth(context):
    return context if isinstance(context, ReviewerIdentity) else None


def service(*, notifier=None, clock=None):
    return ManualPaymentService(
        reviewer_authenticator=reviewer_auth,
        notifier=notifier,
        clock=clock or (lambda: datetime.now(timezone.utc)),
    )


def submitted(svc):
    payment = svc.create_payment("customer-1", 100)
    svc.submit_proof(payment.payment_id, "customer-1", "TX123")
    return payment


def test_01_payment_creation():
    payment = service().create_payment("c1", 100)
    assert payment.state is PaymentState.PENDING
    assert payment.amount == 100


def test_02_unique_reference_code():
    svc = service()
    refs = {svc.create_payment("c", 10).reference_code for _ in range(20)}
    assert len(refs) == 20


def test_03_submit_payment():
    payment = service().create_payment("c1", 100)
    result = service()  # independent service should not see another customer's payment
    with pytest.raises(Exception):
        result.submit_proof(payment.payment_id, "c1", "TX")

    svc = service()
    payment = svc.create_payment("c1", 100)
    svc.submit_proof(payment.payment_id, "c1", "TX")
    assert payment.state is PaymentState.UNDER_REVIEW


def test_04_screenshot_does_not_confirm_payment():
    payment = submitted(service())
    assert payment.state is PaymentState.UNDER_REVIEW


def test_05_state_transition_validation():
    svc = service()
    payment = svc.create_payment("c1", 100)
    with pytest.raises(InvalidTransition):
        svc.confirm(payment.payment_id, ReviewerIdentity("r1"))


def test_06_missing_reviewer_configuration_blocks_confirmation(monkeypatch):
    monkeypatch.delenv("HAMED_PAYMENT_REVIEWER_IDS", raising=False)
    svc = service()
    payment = submitted(svc)
    with pytest.raises(AuthorizationError):
        svc.confirm(payment.payment_id, ReviewerIdentity("r1"))


def test_07_empty_reviewer_allowlist_blocks_confirmation(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "   ")
    svc = service()
    payment = submitted(svc)
    with pytest.raises(AuthorizationError):
        svc.confirm(payment.payment_id, ReviewerIdentity("r1"))


def test_08_unauthorized_reviewer_blocks_confirmation(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "r2")
    svc = service()
    payment = submitted(svc)
    with pytest.raises(AuthorizationError):
        svc.confirm(payment.payment_id, ReviewerIdentity("r1"))


def test_09_reviewer_impersonation_is_not_accepted(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "r1")
    svc = service()
    payment = submitted(svc)
    # A plain request-body-looking string is not a trusted identity.
    with pytest.raises(AuthorizationError):
        svc.confirm(payment.payment_id, "r1")


def test_10_unauthenticated_identity_blocks(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "r1")
    svc = service()
    payment = submitted(svc)
    with pytest.raises(AuthorizationError):
        svc.confirm(payment.payment_id, None)


def test_11_no_fake_static_token_authentication():
    source = open("app/payments/manual_payment.py", encoding="utf-8").read()
    assert "STATIC_TOKEN" not in source
    assert "static-token" not in source.lower()
    assert "reviewer_id" not in source


def test_12_double_confirmation_blocked(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "r1")
    svc = service()
    payment = submitted(svc)
    svc.confirm(payment.payment_id, ReviewerIdentity("r1"))
    with pytest.raises(InvalidTransition):
        svc.confirm(payment.payment_id, ReviewerIdentity("r1"))


def test_13_amount_modification_is_not_supported():
    payment = service().create_payment("c1", 100)
    original = payment.amount
    assert not hasattr(service(), "update_amount")
    assert payment.amount == original


def test_14_direct_status_modification_is_not_supported():
    payment = service().create_payment("c1", 100)
    assert not hasattr(service(), "set_status")
    assert payment.state is PaymentState.PENDING


def test_15_fulfillment_before_confirmation_blocked():
    svc = service()
    payment = submitted(svc)
    with pytest.raises(PaymentError):
        svc.fulfill(payment.payment_id)


def test_16_revenue_before_confirmation_blocked():
    svc = service()
    payment = submitted(svc)
    with pytest.raises(PaymentError):
        svc.record_revenue(payment.payment_id)


def test_17_audit_event_creation():
    svc = service()
    payment = submitted(svc)
    assert any(e["action"] == "payment_created" for e in svc.audit_events)
    assert any(e["action"] == "payment_submitted" for e in svc.audit_events)
    assert all("timestamp" in e for e in svc.audit_events)
    assert all("amount" in e and "reference_code" in e for e in svc.audit_events)


def test_18_telegram_reviewer_notification_hook():
    notifications = []
    svc = service(notifier=lambda p: notifications.append((p.payment_id, p.reference_code)))
    payment = submitted(svc)
    assert notifications == [(payment.payment_id, payment.reference_code)]


def test_19_notification_failure_does_not_confirm(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "r1")
    def broken(_):
        raise RuntimeError("telegram down")
    svc = service(notifier=broken)
    payment = submitted(svc)
    assert payment.state is PaymentState.UNDER_REVIEW
    assert any(e["action"] == "notification_failed" for e in svc.audit_events)


def test_20_reject_flow(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "r1")
    svc = service()
    payment = submitted(svc)
    result = svc.reject(payment.payment_id, ReviewerIdentity("r1"), note="proof mismatch")
    assert result.state is PaymentState.REJECTED
    assert result.reviewer == "r1"


def test_21_expiration_flow():
    now = [datetime.now(timezone.utc)]
    svc = service(clock=lambda: now[0])
    payment = svc.create_payment("c1", 100, expires_hours=1)
    now[0] = payment.expires_at + timedelta(seconds=1)
    with pytest.raises(InvalidTransition):
        svc.submit_proof(payment.payment_id, "c1", "TX")


def test_22_sensitive_secrets_absent_from_audit(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "r1")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "SUPERSECRET")
    svc = service()
    payment = submitted(svc)
    svc.confirm(payment.payment_id, ReviewerIdentity("r1"))
    serialized = repr(svc.audit_events)
    assert "SUPERSECRET" not in serialized


def test_23_customer_cannot_confirm_payment(monkeypatch):
    monkeypatch.setenv("HAMED_PAYMENT_REVIEWER_IDS", "customer-1")
    svc = service()
    payment = submitted(svc)
    with pytest.raises(AuthorizationError):
        svc.confirm(payment.payment_id, "customer-1")


def test_24_customer_cannot_access_another_customer_payment():
    svc = service()
    payment = svc.create_payment("customer-a", 100)
    with pytest.raises(Exception):
        svc.get_customer_payment(payment.payment_id, "customer-b")
