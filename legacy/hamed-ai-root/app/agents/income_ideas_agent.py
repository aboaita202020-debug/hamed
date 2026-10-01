"""Expose the income-ideas catalog as a first-class Hamed agent."""
from __future__ import annotations
from .base_agent import BaseAgent, AgentResult
from app.services.income_ideas_catalog import get_idea, search_ideas, INCOME_IDEAS


class IncomeIdeasAgent(BaseAgent):
    name = "income_ideas_agent"

    def run(self, payload: dict) -> AgentResult:
        try:
            action = str(payload.get("action") or "list").strip().lower()
            if action == "get":
                idea = get_idea(int(payload.get("id", 0)))
                if idea is None:
                    return AgentResult(success=False, error="income_idea_not_found")
                return AgentResult(success=True, data={"status": "found", "idea": idea})
            if action == "search":
                results = search_ideas(
                    query=str(payload.get("query") or ""),
                    category=str(payload.get("category") or ""),
                    limit=int(payload.get("limit", 10)),
                )
                return AgentResult(success=True, data={"status": "found", "count": len(results), "ideas": results})
            return AgentResult(success=True, data={
                "status": "catalog_ready",
                "count": len(INCOME_IDEAS),
                "ideas": INCOME_IDEAS,
            })
        except (TypeError, ValueError) as exc:
            return AgentResult(success=False, error=f"invalid_income_ideas_request:{exc}")
        except Exception as exc:
            return AgentResult(success=False, error=str(exc))
