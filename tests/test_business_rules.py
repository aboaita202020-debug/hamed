from app.agents.finance import Opportunity
from app.agents.opportunity import SupplierOffer, rank_offers
from app.agents.permissions import can_execute
from app.agents.sales_agent import SalesLimits, negotiate_within_limits


def test_opportunity_math():
    o = Opportunity(100, 10, 160, shipping=100, taxes_and_fees=50)
    assert o.landed_cost == 1150
    assert o.expected_revenue == 1600
    assert o.gross_profit == 450
    assert round(o.margin_percent, 2) == 28.12


def test_offer_ranking_prefers_margin():
    offers = [
        SupplierOffer("A", "X", 100, 10),
        SupplierOffer("B", "X", 80, 10),
    ]
    ranked = rank_offers(offers, 120)
    assert ranked[0][0].supplier == "B"


def test_high_impact_requires_approval():
    assert not can_execute("purchase", approved=False)
    assert can_execute("purchase", approved=True)
    assert can_execute("research", approved=False)


def test_sales_limits_escalate():
    limits = SalesLimits(minimum_price=90, maximum_discount_percent=10)
    assert negotiate_within_limits(95, 100, limits) == "approved_within_limits"
    assert negotiate_within_limits(80, 100, limits) == "escalate_for_approval"
