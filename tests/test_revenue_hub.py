from app.services.revenue_hub import RevenueHub


def test_full_revenue_pipeline_modes():
    modes = {x.mode for x in RevenueHub().build_pipeline()}
    assert "lead_hunting" in modes
    assert "affiliate" in modes
    assert "b2b_deals" in modes
    assert "subscriptions" in modes
    assert "agency_growth" in modes
    assert "revenue_brain" in modes
    assert "daily_revenue_target" in modes
    assert "profit_leak_detector" in modes
    assert "unused_capacity_hunter" in modes
    assert "dead_stock_exchange" in modes


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


def test_revenue_brain_selects_best_observed_opportunity():
    engine = RevenueHub()
    result = engine.revenue_brain([
        {"title": "small", "next_action": "a", "evidence_count": 1, "customer_fit": 0.3, "estimated_value": 1000, "effort": 2, "risk": 0.1},
        {"title": "strong", "next_action": "b", "evidence_count": 5, "customer_fit": 1.0, "estimated_value": 100000, "effort": 1, "risk": 0.0},
    ], daily_target=1000)
    assert result["focus"]["title"] == "strong"
    assert result["guaranteed_revenue"] is False


def test_daily_revenue_plan_math():
    result = RevenueHub().daily_revenue_plan(target=1000, average_deal_value=250, close_rate=0.5)
    assert result["deals_needed"] == 4
    assert result["leads_needed"] == 8
