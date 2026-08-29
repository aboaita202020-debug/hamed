from app.agents.autonomy import AutonomyPolicy


def test_autonomy_is_disabled_by_default():
    policy = AutonomyPolicy(enabled=False, max_purchase_value=1000, max_payment_value=1000)
    assert policy.allows("purchase", 500) is False


def test_purchase_is_allowed_within_configured_limit():
    policy = AutonomyPolicy(enabled=True, max_purchase_value=1000, max_payment_value=500)
    assert policy.allows("purchase", 500) is True
    assert policy.allows("purchase", 1001) is False


def test_high_impact_actions_stay_blocked():
    policy = AutonomyPolicy(enabled=True, max_purchase_value=1000000, max_payment_value=1000000)
    assert policy.allows("contract", 100) is False
    assert policy.allows("publish", 100) is False
    assert policy.allows("irreversible", 100) is False


def test_routine_sales_can_be_autonomous():
    policy = AutonomyPolicy(enabled=True)
    assert policy.allows("sales_message") is True
    assert policy.allows("negotiation") is True
