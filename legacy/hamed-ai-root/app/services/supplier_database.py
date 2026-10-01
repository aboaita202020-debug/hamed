"""Local supplier intelligence store for Hamed AI.

Stores only business facts supplied by authorized research/integrations. It never
fabricates prices, stock, contact details, or trust scores.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


@dataclass
class SupplierRecord:
    supplier_id: str
    name: str
    category: str
    products: list[str] = field(default_factory=list)
    country: str = ""
    city: str = ""
    website: str = ""
    public_contacts: list[str] = field(default_factory=list)
    moq: str | None = None
    price_notes: str | None = None
    availability: str | None = None
    delivery_notes: str | None = None
    evidence: list[str] = field(default_factory=list)
    confidence: float = 0.0
    verified_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SupplierDatabase:
    def __init__(self) -> None:
        self.records: dict[str, SupplierRecord] = {}

    def add(self, supplier: SupplierRecord) -> SupplierRecord:
        if not supplier.name.strip() or not supplier.category.strip():
            raise ValueError("supplier name and category are required")
        if not supplier.evidence:
            raise ValueError("supplier evidence is required")
        if not 0 <= supplier.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        self.records[supplier.supplier_id] = supplier
        return supplier

    def upsert(self, *, name: str, category: str, evidence: list[str], **fields: Any) -> SupplierRecord:
        key = next((sid for sid, r in self.records.items()
                    if r.name.casefold() == name.casefold() and r.category.casefold() == category.casefold()), None)
        supplier = self.records[key] if key else SupplierRecord(
            supplier_id=str(uuid.uuid4()), name=name, category=category, evidence=[]
        )
        for field_name, value in fields.items():
            if hasattr(supplier, field_name) and value is not None:
                setattr(supplier, field_name, value)
        supplier.evidence = list(dict.fromkeys([*supplier.evidence, *evidence]))
        supplier.verified_at = datetime.now(timezone.utc).isoformat()
        return self.add(supplier)

    def search(self, *, category: str | None = None, product: str | None = None,
               country: str | None = None) -> list[SupplierRecord]:
        def match(r: SupplierRecord) -> bool:
            haystack = " ".join([r.name, r.category, *r.products]).casefold()
            return ((not category or r.category.casefold() == category.casefold())
                    and (not product or product.casefold() in haystack)
                    and (not country or r.country.casefold() == country.casefold()))
        return [r for r in self.records.values() if match(r)]

    def export(self) -> list[dict[str, Any]]:
        return [asdict(r) for r in self.records.values()]

    def clear(self) -> None:
        self.records.clear()
