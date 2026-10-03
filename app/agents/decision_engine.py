"""Deterministic routing for commercial requests and high-impact actions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    intent: str
    needs_research: bool
    needs_approval: bool


RESEARCH_INTENTS = {"supplier_search", "product_search", "market_price", "commercial_opportunity"}
APPROVAL_ACTIONS = {"purchase", "payment", "transfer", "contract", "publish", "account_change", "irreversible"}


def classify_request(text: str) -> Decision:
    t = text.lower()
    research = any(k in t for k in ("ابحث", "دور", "مورد", "سعر", "منتج", "supplier", "search", "price"))
    intent = "commercial_opportunity" if research else "general"
    return Decision(intent, research, False)


def requires_approval(action: str) -> bool:
    return action in APPROVAL_ACTIONS
