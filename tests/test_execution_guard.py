from app.agents.execution_guard import authorize


def test_purchase_is_blocked_without_approval():
    decision = authorize("purchase")
    assert decision.allowed is False
    assert decision.reason == "explicit_human_approval_required"


def test_purchase_is_allowed_after_approval():
    decision = authorize("purchase", approved=True)
    assert decision.allowed is True


def test_read_only_action_is_allowed():
    assert authorize("research").allowed is True
