"""Server-side commercial rules for autonomous Hamed operations."""

MIN_DEPOSIT_PERCENT = 10.0


def required_deposit(offer_value: float) -> float:
    if offer_value <= 0:
        raise ValueError("Offer value must be positive")
    return offer_value * MIN_DEPOSIT_PERCENT / 100.0


def can_start_work(offer_value: float, verified_deposit: float) -> bool:
    return verified_deposit >= required_deposit(offer_value)


def can_release_final(offer_value: float, verified_total_payment: float) -> bool:
    return offer_value > 0 and verified_total_payment >= offer_value
