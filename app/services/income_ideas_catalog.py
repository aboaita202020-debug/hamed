"""Monetization catalog extracted from the Hamed income-ideas plan."""
from __future__ import annotations
from typing import Any

INCOME_IDEAS = "+json.dumps(items, ensure_ascii=False, indent=2)+"""

def get_idea(idea_id: int):
    for idea in INCOME_IDEAS:
        if idea["id"] == idea_id:
            return idea
    return None


def search_ideas(query: str = "", category: str = "", limit: int = 10):
    q = query.strip().lower()
    c = category.strip().lower()
    results = []
    for idea in INCOME_IDEAS:
        if c and c not in idea["category"].lower():
            continue
        if q:
            haystack = (idea["idea"] + " " + " ".join(idea["agents"]) + " " + idea["category"]).lower()
            if q not in haystack:
                continue
        results.append(idea)
        if len(results) >= max(1, limit):
            break
    return results
""