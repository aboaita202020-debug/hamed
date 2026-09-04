import os

from app.services.execution_adapters import ExecutionAdapters


def test_contact_requires_verified_recipient():
    result = ExecutionAdapters().contact({}, "hello")
    assert result.status == "blocked"


def test_payment_stays_below_server_limit(monkeypatch):
    monkeypatch.setenv("HAMED_MAX_PAYMENT_VALUE", "100")
    result = ExecutionAdapters().prepare_payment(50)
    assert result.status == "ready"


def test_payment_requires_approval_above_limit(monkeypatch):
    monkeypatch.setenv("HAMED_MAX_PAYMENT_VALUE", "100")
    result = ExecutionAdapters().prepare_payment(101)
    assert result.status == "approval_required"


def test_purchase_requires_supplier_and_limit(monkeypatch):
    monkeypatch.setenv("HAMED_MAX_PURCHASE_VALUE", "1000")
    assert ExecutionAdapters().prepare_purchase(100, "Supplier A").status == "ready"
    assert ExecutionAdapters().prepare_purchase(100, None).status == "blocked"
    assert ExecutionAdapters().prepare_purchase(1001, "Supplier A").status == "approval_required"
