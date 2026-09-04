from app.agents.cash_velocity import CashVelocityEngine
from app.agents.compliance_checkpoint import ExternalComplianceCheckpoint


def opportunity(**overrides):
    base = {
        "id": "opp-1",
        "route": "ready_to_buy",
        "evidence": "customer explicitly requested the service",
        "expected_profit": 1000,
        "decision_speed": 0.9,
        "payment_ready": 0.9,
        "payment_method": "bank_transfer",
        "fulfillment_ready": 0.9,
        "close_probability": 0.9,
        "risk": 0.0,
    }
    base.update(overrides)
    return base


def test_high_value_opportunity_requires_external_review():
    engine = CashVelocityEngine(ExternalComplianceCheckpoint())
    result = engine.assess(opportunity(expected_profit=5001))
    assert result.status == "blocked"
    assert result.compliance_status == "pending_review"


def test_repeated_opportunity_requires_external_review():
    engine = CashVelocityEngine(ExternalComplianceCheckpoint())
    result = engine.assess(opportunity(occurrence_count=3))
    assert result.status == "blocked"
    assert result.compliance_status == "pending_review"


def test_approved_external_review_can_continue():
    engine = CashVelocityEngine(ExternalComplianceCheckpoint())
    result = engine.assess(opportunity(expected_profit=5001, external_compliance_approved=True))
    assert result.compliance_status == "pending_review"
    assert result.status == "fast_track"


def test_low_value_opportunity_does_not_require_external_review():
    engine = CashVelocityEngine(ExternalComplianceCheckpoint())
    result = engine.assess(opportunity(expected_profit=1000, occurrence_count=1))
    assert result.compliance_status == "not_required"
    assert result.status == "fast_track"
