from app.agents.food_trade import FoodTradeEngine


def test_food_quote_one_percent():
    q = FoodTradeEngine().quote(quantity=15000, unit_cost=20, margin_percent=1)
    assert round(q.unit_sale_price, 2) == 20.20
    assert round(q.expected_profit, 2) == 3000.00


def test_food_quote_two_percent_with_extra_cost():
    q = FoodTradeEngine().quote(quantity=1000, unit_cost=20, extra_cost_per_unit=0.50, margin_percent=2)
    assert round(q.unit_sale_price, 2) == 20.91
    assert round(q.expected_profit, 2) == 410.00


def test_food_margin_is_bounded():
    engine = FoodTradeEngine()
    for value in (0, 2.1, 5):
        try:
            engine.quote(quantity=1, unit_cost=20, margin_percent=value)
        except ValueError:
            pass
        else:
            raise AssertionError("margin outside 1-2% must be rejected")


def test_high_volume_defaults_to_one_percent():
    assert FoodTradeEngine().recommended_margin(quantity=15000) == 1.0
