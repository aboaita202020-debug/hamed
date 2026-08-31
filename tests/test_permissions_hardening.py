from datetime import datetime, timezone

from app.agents.permissions import ApprovalRequest, Risk, can_execute


def test_approval_requests_get_distinct_creation_times():
    first = ApprovalRequest("purchase", "one")
    second = ApprovalRequest("purchase", "two")
    assert first.created_at.tzinfo == timezone.utc
    assert second.created_at.tzinfo == timezone.utc
    assert second.created_at >= first.created_at


def test_unapproved_purchase_is_blocked_by_default(monkeypatch):
    monkeypatch.setenv("HAMED_AUTONOMOUS_MODE", "false")
    assert not can_execute("purchase", value=100, risk=Risk.LOW)


def test_approved_blocked_action_requires_known_action():
    assert can_execute("contract", approved=True)
    assert not can_execute("arbitrary_command", approved=True)
