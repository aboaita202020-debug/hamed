from app.services.revenue_hub import RevenueHub


def test_full_revenue_pipeline_modes():
    modes = {x.mode for x in RevenueHub().build_pipeline()}
    assert "lead_hunting" in modes
    assert "affiliate" in modes
    assert "b2b_deals" in modes
    assert "subscriptions" in modes
    assert "agency_growth" in modes


def test_opportunity_score_is_bounded():
    score = RevenueHub().score_opportunity(evidence_count=5, customer_fit=1.0, estimated_value=100000)
    assert 0 <= score <= 100


def test_price_calculation():
    result = RevenueHub().calculate_price(cost=100, expenses=20, margin=0.25)
    assert result["price"] == 160.0
    assert result["gross_profit"] == 40.0


def test_lead_recovery_requires_context():
    engine = RevenueHub()
    assert engine.recover_lead({})["ready"] is False
    assert engine.recover_lead({"last_need": "website"})["ready"] is True
