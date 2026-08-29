from app.agents.decision_engine import classify_request, requires_approval
from app.agents.workflow import prepare_action, execute_approved


def test_commercial_request_routes_to_research():
    d = classify_request("ابحث لي عن مورد وسعر منتج")
    assert d.needs_research is True
    assert d.intent == "commercial_opportunity"


def test_sensitive_actions_require_approval():
    assert requires_approval("purchase") is True
    assert requires_approval("research") is False


def test_pending_purchase_cannot_execute_until_approved():
    p = prepare_action("purchase", "شراء 10 وحدات")
    assert p.approval is not None
    assert execute_approved(p) is False
    p.approval.approved = True
    assert execute_approved(p) is True
