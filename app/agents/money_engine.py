"""Safe revenue opportunity discovery using public web evidence."""
from __future__ import annotations

from typing import Any
from .provider import public_web_research

REVENUE_QUERIES = [
    "Arabic ecommerce stores problems conversion rate checkout SEO 2026",
    "affiliate programs Middle East Arabic ecommerce SaaS 2026",
    "small business websites digital marketing demand Middle East 2026",
    "B2B lead generation opportunities Egypt Gulf 2026",
]


def scan_revenue_opportunities(max_results: int = 8) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for query in REVENUE_QUERIES:
        try:
            evidence = public_web_research(query, max_results=max_results)
            records.append({"query": query, "status": "ok", "evidence": evidence})
        except Exception as exc:
            records.append({"query": query, "status": "error", "error": type(exc).__name__})
    return {
        "status": "ok" if any(r["status"] == "ok" for r in records) else "degraded",
        "mode": "research_only",
        "safe_mode": True,
        "monetization_paths": ["affiliate", "website_service", "marketing_service", "b2b_leads"],
        "records": records,
        "approval_required_for": ["purchase", "payment", "contract", "publish", "account_change"],
    }
