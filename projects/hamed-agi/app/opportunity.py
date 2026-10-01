from __future__ import annotations

from .models import Mission, Opportunity


class OpportunityEngine:
    def __init__(self, minimum_score: float = 0.60) -> None:
        self.minimum_score = minimum_score
    def discover(self, mission: Mission) -> list[Opportunity]:
        seeds = [
            Opportunity(title="Conversion audit opportunity", problem="The customer journey may contain friction that reduces completed purchases.", solution="Audit product pages, trust signals, checkout flow and calls-to-action, then run measurable experiments.", evidence=["Collect real public evidence before outreach."], score=0.72),
            Opportunity(title="Marketing growth plan", problem="Traffic and conversion activity may not be aligned around a measurable growth loop.", solution="Build a 30-day plan covering positioning, content, SEO, offers, retention and experiments.", evidence=["Validate the business context before making factual claims."], score=0.68),
        ]
        return [item for item in seeds if item.score >= self.minimum_score]

opportunity_engine = OpportunityEngine()
