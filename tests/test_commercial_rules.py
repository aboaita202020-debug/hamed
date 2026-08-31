from app.agents.commercial_rules import can_final_deliver, can_start_work, demo_allowed


def test_demo_is_allowed_before_payment():
    assert demo_allowed() is True


def test_work_requires_at_least_ten_percent_deposit():
    assert can_start_work(20_000, 1_999) is False
    assert can_start_work(20_000, 2_000) is True


def test_final_delivery_requires_full_payment():
    assert can_final_deliver(20_000, 19_999) is False
    assert can_final_deliver(20_000, 20_000) is True
