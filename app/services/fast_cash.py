"""Fast-cash offer layer for Hamed AI.

Turns qualified needs into small, productized services that are quick to sell
and deliver. Prices are configurable and are never treated as guaranteed revenue.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional
import os


@dataclass(frozen=True)
class FastCashOffer:
    key: str
    title: str
    service: str
    delivery_hours: float
    price: float
    currency: str = "EGP"
    recurring: bool = False
    trial: bool = False
    channel: str = "whatsapp"


class FastCashEngine:
    """Select fast-to-cash offers from evidence-backed customer needs."""

    DEFAULTS = {
        "landing_page_1_day": ("Landing Page in 1 Day", "landing_page", 24.0, 1500.0, False, False),
        "whatsapp_reply_setup": ("WhatsApp Business Reply Setup", "whatsapp_automation", 3.0, 750.0, False, False),
        "social_catalog_cleanup": ("Instagram/Facebook Catalog Cleanup", "social_catalog", 6.0, 900.0, False, False),
        "starter_store_48h": ("Starter Online Store in 48 Hours", "ecommerce_store", 48.0, 3500.0, False, False),
        "content_reply_monthly": ("Daily Replies + Weekly Content", "customer_support_content", 24.0, 200.0, True, False),
        "fast_audit": ("Fast Digital Presence Audit", "digital_audit", 4.0, 500.0, False, True),
    }

    def offers(self) -> List[FastCashOffer]:
        result = []
        for key, (title, service, hours, default_price, recurring, trial) in self.DEFAULTS.items():
            env_key = "HAMED_FAST_CASH_PRICE_" + key.upper()
            raw = os.getenv(env_key, str(default_price))
            try:
                price = float(raw)
            except (TypeError, ValueError):
                price = default_price
            if price < 0:
                price = default_price
            result.append(FastCashOffer(key, title, service, hours, price, "EGP", recurring, trial))
        return result

    def recommend(self, context: Optional[Dict[str, Any]] = None, limit: int = 3) -> List[Dict[str, Any]]:
        """Recommend offers only when the context contains an observable need."""
        data = context or {}
        text = " ".join(str(v) for v in data.values()).lower()
        if not text:
            return []

        keywords = []
        if any(x in text for x in ("موقع", "website", "landing page", "صفحة")):
            keywords.extend(["landing_page_1_day", "fast_audit"])
        if any(x in text for x in ("متجر", "store", "ecommerce", "بيع اونلاين", "بيع أونلاين")):
            keywords.extend(["starter_store_48h", "social_catalog_cleanup"])
        if any(x in text for x in ("واتساب", "whatsapp", "ردود", "رسائل")):
            keywords.extend(["whatsapp_reply_setup", "content_reply_monthly"])
        if any(x in text for x in ("انستجرام", "instagram", "فيسبوك", "facebook", "catalog", "كتالوج")):
            keywords.extend(["social_catalog_cleanup", "whatsapp_reply_setup"])

        by_key = {offer.key: offer for offer in self.offers()}
        selected = []
        for key in keywords:
            if key in by_key and key not in {item["key"] for item in selected}:
                offer = by_key[key]
                selected.append(self._serialize(offer, "evidence-backed need"))
            if len(selected) >= max(1, limit):
                break
        return selected

    def flash_offer(self, offer_key: str, discount_percent: float = 0.0) -> Dict[str, Any]:
        """Prepare a limited offer; discounts are capped and never promise results."""
        if not 0 <= discount_percent <= 30:
            raise ValueError("discount_percent must be between 0 and 30")
        offer = next((x for x in self.offers() if x.key == offer_key), None)
        if offer is None:
            raise ValueError("unknown offer")
        price = round(offer.price * (1 - discount_percent / 100.0), 2)
        return self._serialize(offer, "limited flash offer", price=price, discount_percent=discount_percent)

    def next_after_confirmed_purchase(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest an upsell/referral only after a confirmed purchase exists."""
        if not customer.get("payment_confirmed"):
            return {"ready": False, "reason": "payment_confirmation_required"}
        return {
            "ready": True,
            "next_action": "prepare_relevant_upsell_or_referral",
            "guaranteed_revenue": False,
        }

    @staticmethod
    def _serialize(offer: FastCashOffer, reason: str, price: Optional[float] = None, discount_percent: float = 0.0) -> Dict[str, Any]:
        result = asdict(offer)
        if price is not None:
            result["price"] = price
        result["reason"] = reason
        result["discount_percent"] = discount_percent
        result["guaranteed_revenue"] = False
        return result
