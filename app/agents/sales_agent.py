"""Sales policy primitives. The model can draft; policy decides what may be sent."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SalesLimits:
    minimum_price: float
    maximum_discount_percent: float = 0.0

    def validate_price(self, price: float, list_price: float) -> bool:
        if price < self.minimum_price:
            return False
        if list_price > 0:
            discount = (list_price - price) / list_price * 100
            return discount <= self.maximum_discount_percent
        return True


def negotiate_within_limits(proposed_price: float, list_price: float, limits: SalesLimits) -> str:
    if limits.validate_price(proposed_price, list_price):
        return "approved_within_limits"
    return "escalate_for_approval"
