from app.services.revenue_ceo import RevenueCEO


def test_ceo_selects_fast_evidence_backed_focus():
    result = RevenueCEO().decide([
        {"title": "slow", "next_action": "research", "evidence": 5, "fit": 1.0, "value": 100000, "speed": 0.2, "effort": 3, "risk": 0.1},
        {"title": "fast", "next_action": "offer", "evidence": 5, "fit": 1.0, "value": 50000, "speed": 1.0, "effort": 1, "risk": 0.0},
    ], daily_target=1000)
    assert result["focus"]["title"] == "fast"
    assert result["guaranteed_revenue"] is False


def test_ceo_accepts_research_text_as_evidence():
    result = RevenueCEO().decide([{"title": "research", "evidence": "verified public evidence", "fit": 0.5}])
    assert result["focus"]["ceo_score"] > 0


def test_ceo_guardrails_are_enabled():
    guards = RevenueCEO().guardrails()
    assert all(guards.values())
