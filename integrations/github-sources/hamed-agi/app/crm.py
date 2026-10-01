from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Customer:
    name: str
    contact: str | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

class CRM:
    def __init__(self) -> None:
        self.customers: dict[str, Customer] = {}
    def upsert(self, customer: Customer) -> Customer:
        self.customers[customer.name] = customer
        return customer
    def get(self, name: str) -> Customer | None:
        return self.customers.get(name)
    def summary(self) -> dict[str, int]:
        return {"customers": len(self.customers)}

crm = CRM()
