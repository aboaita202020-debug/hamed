"""Commercial opportunity scoring and normalized supplier offers."""
from dataclasses import dataclass, field
from .finance import Opportunity


@dataclass(frozen=True)
class SupplierOffer:
    supplier: str
    product: str
    unit_price: float
    quantity: int
    shipping: float = 0.0
    taxes_and_fees: float = 0.0
    source: str = ""
    evidence: list[str] = field(default_factory=list)

    @property
    def total_cost(self) -> float:
        return self.unit_price * self.quantity + self.shipping + self.taxes_and_fees

    def evaluate(self, expected_unit_sale_price: float) -> Opportunity:
        return Opportunity(
            purchase_cost=self.unit_price,
            quantity=self.quantity,
            expected_sale_price=expected_unit_sale_price,
            shipping=self.shipping,
            taxes_and_fees=self.taxes_and_fees,
        )


def rank_offers(offers: list[SupplierOffer], expected_unit_sale_price: float) -> list[tuple[SupplierOffer, Opportunity]]:
    evaluated = [(offer, offer.evaluate(expected_unit_sale_price)) for offer in offers]
    return sorted(evaluated, key=lambda item: (item[1].margin_percent, item[1].gross_profit), reverse=True)
