from dataclasses import dataclass


@dataclass
class RevenueEvent:
    customer: str
    amount: float
    currency: str = "EGP"
    status: str = "pending"

class RevenueEngine:
    def __init__(self):
        self.events: list[RevenueEvent] = []
    def record(self, customer: str, amount: float, currency: str = "EGP", status: str = "pending"):
        event = RevenueEvent(customer, amount, currency, status)
        self.events.append(event)
        return event
    def total_realized(self, currency: str = "EGP") -> float:
        return sum(e.amount for e in self.events if e.currency == currency and e.status == "realized")
    def summary(self) -> dict[str, float]:
        return {currency: self.total_realized(currency) for currency in {e.currency for e in self.events}}

revenue_engine = RevenueEngine()
