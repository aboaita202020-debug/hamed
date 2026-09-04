from app.agents.autonomous_execution import AutonomousExecutionEngine


def test_execution_requires_evidence():
    result = AutonomousExecutionEngine().execute({})
    assert result["results"][0]["status"] == "blocked"


def test_execution_runs_reversible_steps_without_owner_prompt():
    calls = []
    engine = AutonomousExecutionEngine(lambda action, opportunity: calls.append(action) or "ok")
    result = engine.execute({"evidence": "verified public evidence"})
    assert result["autonomous"] is True
    assert result["guaranteed_revenue"] is False
    assert calls == [
        "market_research", "cash_velocity_scan", "single_approver_filter",
        "payment_preclearance", "opportunity_hunt", "lead_generation",
        "offer_build", "dynamic_pricing", "deposit_offer", "customer_reply",
        "negotiate", "lead_recovery", "followup", "referral", "revenue_tracking",
    ]
