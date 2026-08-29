from app.agents.finance import Opportunity
from app.agents.permissions import can_execute


def test_opportunity_math():
    o = Opportunity(purchase_cost=100, quantity=10, expected_sale_price=150, shipping=50)
    assert o.landed_cost == 1050
    assert o.expected_revenue == 1500
    assert o.gross_profit == 450
    assert o.margin_percent == 30


def test_high_impact_actions_need_approval():
    assert can_execute("purchase", approved=False) is False
    assert can_execute("purchase", approved=True) is True
    assert can_execute("payment", approved=False) is False
    assert can_execute("research", approved=False) is True
