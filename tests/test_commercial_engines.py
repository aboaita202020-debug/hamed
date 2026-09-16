from app.agents.business_engines import Opportunity, rank_opportunities
from app.agents.lead_discovery import Lead, qualify
from app.agents.experiment_engine import Experiment, next_learning_action
from app.agents.finance_engine import landed_cost, unit_economics


def test_opportunity_math_and_rank():
    a = Opportunity("1", "service", "A", "B", expected_revenue=1000, cost=200, probability=.8)
    b = Opportunity("2", "service", "B", "B", expected_revenue=700, cost=100, probability=.5)
    assert a.expected_profit == 800
    assert a.expected_value == 640
    assert rank_opportunities([b, a])[0] == a


def test_lead_qualification():
    assert len(qualify([Lead("a", "b", "x", "s", verified=True), Lead("c", "d", "x", "s", verified=True, opted_out=True)])) == 1


def test_experiment_learning():
    e = Experiment("increase replies", 10, metric="reply_rate")
    e.record(12)
    assert next_learning_action(e) == "keep_and_repeat"


def test_finance():
    assert landed_cost(10, 100, 50, 20, 5) == 1075
    assert unit_economics(20, 10)["unit_profit"] == 10
