"""Deterministic commercial calculations; no LLM arithmetic."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Opportunity:
    purchase_cost: float
    quantity: int
    expected_sale_price: float
    shipping: float = 0.0
    taxes_and_fees: float = 0.0

    @property
    def landed_cost(self) -> float:
        return self.purchase_cost * self.quantity + self.shipping + self.taxes_and_fees

    @property
    def expected_revenue(self) -> float:
        return self.expected_sale_price * self.quantity

    @property
    def gross_profit(self) -> float:
        return self.expected_revenue - self.landed_cost

    @property
    def margin_percent(self) -> float:
        if self.expected_revenue <= 0:
            return 0.0
        return self.gross_profit / self.expected_revenue * 100
