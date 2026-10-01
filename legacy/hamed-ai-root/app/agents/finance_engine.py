"""Commercial finance calculations: transparent estimates, never fabricated data."""
from __future__ import annotations

def landed_cost(unit_cost: float, quantity: float, shipping: float = 0, taxes: float = 0, fees: float = 0) -> float:
    if min(unit_cost, quantity, shipping, taxes, fees) < 0:
        raise ValueError("Costs cannot be negative")
    return unit_cost * quantity + shipping + taxes + fees


def profit(revenue: float, total_cost: float) -> float:
    return revenue - total_cost


def margin_percent(revenue: float, total_cost: float) -> float:
    return profit(revenue, total_cost) / revenue * 100 if revenue else 0.0


def unit_economics(unit_sale_price: float, unit_cost: float, acquisition_cost: float = 0, payment_fee: float = 0) -> dict:
    cost = unit_cost + acquisition_cost + payment_fee
    return {"unit_sale_price": unit_sale_price, "unit_total_cost": cost, "unit_profit": unit_sale_price - cost, "margin_percent": margin_percent(unit_sale_price, cost)}
