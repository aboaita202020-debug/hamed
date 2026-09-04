"""
Public surface of the agents package.

This re-export is what makes both of these work, fixing the original
`ImportError: cannot import name 'HamedOrchestrator' from app.agents.orchestrator`:

    from app.agents import HamedOrchestrator
    from app.agents.orchestrator import HamedOrchestrator
"""
from .orchestrator import HamedOrchestrator
from .base_agent import BaseAgent, AgentResult
from .opportunity_hunter_agent import OpportunityHunterAgent
from .sales_agent import SalesAgent
from .negotiation_agent import NegotiationAgent
from .revenue_agent import RevenueAgent
from .reporting_agent import ReportingAgent
from .fact_check_agent import FactCheckAgent

__all__ = [
    "HamedOrchestrator",
    "BaseAgent",
    "AgentResult",
    "OpportunityHunterAgent",
    "SalesAgent",
    "NegotiationAgent",
    "RevenueAgent",
    "ReportingAgent",
    "FactCheckAgent",
]
