from app.services.execution_adapters import ExecutionAdapters


def test_contact_requires_verified_recipient():
    result = ExecutionAdapters().contact({}, "hello")
    assert result.status == "blocked"


def test_contact_requires_explicit_verification():
    result = ExecutionAdapters().contact({"telegram_chat_id": "123"}, "hello")
    assert result.status == "blocked"
    assert "verified" in result.reason


def test_verified_telegram_contact_is_ready_when_delivery_is_disabled(monkeypatch):
    monkeypatch.setenv("HAMED_AUTO_SEND_TELEGRAM", "false")
    result = ExecutionAdapters().send_telegram(
        {"telegram_chat_id": "123", "verified_contact": True}, "hello"
    )
    assert result.status == "ready"
    assert result.channel == "telegram"


def test_verified_whatsapp_is_ready_when_delivery_is_disabled(monkeypatch):
    monkeypatch.setenv("HAMED_AUTO_SEND_WHATSAPP", "false")
    result = ExecutionAdapters().send_whatsapp(
        {"whatsapp": "+201001234567", "verified_contact": True}, "hello"
    )
    assert result.status == "ready"
    assert result.channel == "whatsapp"


def test_whatsapp_requires_credentials_when_auto_send_enabled(monkeypatch):
    monkeypatch.setenv("HAMED_AUTO_SEND_WHATSAPP", "true")
    monkeypatch.delenv("WHATSAPP_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("WHATSAPP_PHONE_NUMBER_ID", raising=False)
    result = ExecutionAdapters().send_whatsapp(
        {"whatsapp": "+201001234567", "verified_contact": True}, "hello"
    )
    assert result.status == "blocked"
    assert "WHATSAPP_ACCESS_TOKEN" in result.reason


def test_opted_out_contact_is_blocked():
    result = ExecutionAdapters().contact(
        {"telegram_chat_id": "123", "verified_contact": True, "opted_out": True}, "hello"
    )
    assert result.status == "blocked"
    assert "opted out" in result.reason


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
