"""Food trading pricing rules for Hamed AI.

Food commodities use a thin 1-2% margin. Costs are kept separate from profit
so Hamed can quote competitively without inventing supplier or market data.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FoodQuote:
    quantity: float
    unit_cost: float
    extra_cost_per_unit: float
    margin_percent: float
    unit_sale_price: float
    total_cost: float
    total_sales: float
    expected_profit: float


class FoodTradeEngine:
    MIN_MARGIN_PERCENT = 1.0
    MAX_MARGIN_PERCENT = 2.0

    def quote(
        self,
        *,
        quantity: float,
        unit_cost: float,
        extra_cost_per_unit: float = 0.0,
        margin_percent: float = 1.0,
    ) -> FoodQuote:
        if quantity <= 0 or unit_cost < 0 or extra_cost_per_unit < 0:
            raise ValueError("quantity must be positive and costs cannot be negative")
        if not self.MIN_MARGIN_PERCENT <= margin_percent <= self.MAX_MARGIN_PERCENT:
            raise ValueError("food margin must be between 1% and 2%")

        landed_unit_cost = unit_cost + extra_cost_per_unit
        unit_sale_price = landed_unit_cost * (1 + margin_percent / 100)
        total_cost = landed_unit_cost * quantity
        total_sales = unit_sale_price * quantity
        expected_profit = total_sales - total_cost
        return FoodQuote(
            quantity=quantity,
            unit_cost=unit_cost,
            extra_cost_per_unit=extra_cost_per_unit,
            margin_percent=margin_percent,
            unit_sale_price=unit_sale_price,
            total_cost=total_cost,
            total_sales=total_sales,
            expected_profit=expected_profit,
        )

    def recommended_margin(self, *, quantity: float, competitive: bool = True) -> float:
        """Return 1% for competitive/high-volume quotes, otherwise 2%."""
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        return self.MIN_MARGIN_PERCENT if competitive or quantity >= 10000 else self.MAX_MARGIN_PERCENT
