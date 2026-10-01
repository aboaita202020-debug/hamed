"""Purchasing specialist: analyze offers; execution remains approval-gated."""
from dataclasses import dataclass
from .opportunity import SupplierOffer, rank_offers


@dataclass(frozen=True)
class PurchasingRecommendation:
    product: str
    expected_unit_sale_price: float
    ranked_offers: list[tuple[SupplierOffer, object]]


def build_recommendation(product: str, offers: list[SupplierOffer], expected_unit_sale_price: float) -> PurchasingRecommendation:
    if not offers:
        raise ValueError("At least one supplier offer is required")
    if expected_unit_sale_price <= 0:
        raise ValueError("Expected sale price must be positive")
    return PurchasingRecommendation(product, expected_unit_sale_price, rank_offers(offers, expected_unit_sale_price))
