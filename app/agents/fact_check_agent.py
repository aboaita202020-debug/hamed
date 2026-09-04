"""FactCheckAgent — spec section 28 guardrail: 'لا يخترع بيانات أو أسعارًا'.

Cross-checks a claim against whatever web_search returns. If no
provider is configured, it explicitly reports LOW confidence instead
of asserting the claim is true.
"""
from __future__ import annotations

from .base_agent import BaseAgent, AgentResult


class FactCheckAgent(BaseAgent):
    name = "fact_check_agent"

    def run(self, payload: dict) -> AgentResult:
        """payload: {"claim": str, "query": str}"""
        query = payload.get("query") or payload.get("claim", "")
        result = self.tools.execute(actor=self.name, tool_name="web_search", query=query)

        if not result.success:
            return AgentResult(
                success=True,
                data={"claim": payload.get("claim"), "verified": False,
                      "confidence": 0.0, "reason": result.error},
            )

        sources = result.data
        confidence = max((s.get("confidence", 0.0) for s in sources), default=0.0)
        return AgentResult(
            success=True,
            data={
                "claim": payload.get("claim"),
                "verified": confidence >= 0.6,
                "confidence": confidence,
                "sources": sources,
            },
        )
