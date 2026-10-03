"""Opportunity Hunter: turn verified public demand/business evidence into sales plans."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Opportunity:
    opportunity_id: str
    source: str
    demand: str
    category: str
    product_or_service: str
    quantity: float | None = None
    location: str = ""
    specifications: str = ""
    timing: str = ""
    evidence: list[str] = field(default_factory=list)
    status: str = "research"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class OpportunityHunter:
    """Coordinates discovery, research and commercial planning without unauthorized outreach."""

    def __init__(self, orchestrator, supplier_database) -> None:
        self.orchestrator = orchestrator
        self.suppliers = supplier_database
        self.opportunities: dict[str, Opportunity] = {}

    def discover(self, *, source: str, demand: str, evidence: list[str] | None = None,
                 opportunity_id: str | None = None) -> dict[str, Any]:
        if not source.strip() or not demand.strip():
            raise ValueError("source and demand are required")
        import uuid
        oid = opportunity_id or str(uuid.uuid4())
        parsed = self._parse_demand(demand)
        item = Opportunity(oid, source, demand, parsed["category"], parsed["product_or_service"],
                           parsed["quantity"], parsed["location"], parsed["specifications"],
                           parsed["timing"], list(evidence or []))
        self.opportunities[oid] = item
        return asdict(item)

    def research(self, opportunity_id: str) -> dict[str, Any]:
        item = self.opportunities[opportunity_id]
        query = (f"Find verified suppliers and current market evidence for {item.product_or_service}; "
                 f"category {item.category}; quantity {item.quantity}; location {item.location}. "
                 "Return primary sources, prices when explicitly published, MOQ, availability and delivery evidence.")
        report = self.orchestrator.research_agent.research(query)
        item.evidence.append(report.findings[:12000])
        item.status = "researched"
        return {"opportunity": asdict(item), "research": report.findings}

    def plan(self, opportunity_id: str) -> dict[str, Any]:
        item = self.opportunities[opportunity_id]
        plan = self.orchestrator.commercial_opportunity_plan({
            "product": item.product_or_service, "category": item.category,
            "quantity": item.quantity, "location": item.location, "evidence": item.evidence,
        })
        item.status = "ready_for_quote"
        return {"opportunity": asdict(item), "plan": plan}

    def personalized_outreach(self, opportunity_id: str, *, customer_name: str = "there") -> dict[str, Any]:
        item = self.opportunities[opportunity_id]
        if not item.evidence:
            raise ValueError("personalized outreach requires verified evidence")
        return self.orchestrator.sales_message_engine.generate({
            "name": customer_name, "problem": f"your stated need for {item.product_or_service}",
            "service": "a verified supply/solution offer", "evidence": item.evidence,
        })

    @staticmethod
    def _parse_demand(text: str) -> dict[str, Any]:
        import re
        lower = text.lower()
        category = "general"
        aliases = {
            "food": ("سكر", "أرز", "مكرونة", "زيت", "غذاء", "food", "sugar", "rice"),
            "clothing": ("ملابس", "ملابس", "clothing", "shoes", "أحذية", "تيشيرت"),
            "electronics": ("موبايل", "هاتف", "لابتوب", "إلكترون", "electronics", "phone", "laptop"),
            "beauty": ("عطر", "تجميل", "مستحضرات", "beauty", "perfume"),
            "home": ("أثاث", "منزل", "home", "furniture"),
            "industrial": ("مصنع", "معدات", "ماكينات", "industrial", "machinery"),
            "digital": ("موقع", "متجر", "تطبيق", "برمجة", "seo", "website", "store", "app", "software"),
            "services": ("خدمة", "تسويق", "تصميم", "marketing", "service", "design"),
        }
        for key, words in aliases.items():
            if any(w in lower for w in words):
                category = key
                break
        nums = re.findall(r"\b\d+(?:[.,]\d+)?\b", text)
        quantity = float(nums[0].replace(",", "")) if nums else None
        product = text.strip()
        location = ""
        return {"category": category, "product_or_service": product, "quantity": quantity,
                "location": location, "specifications": "", "timing": ""}
