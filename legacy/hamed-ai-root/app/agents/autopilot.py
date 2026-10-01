"""Business Autopilot: turns one commercial goal into a safe, testable pipeline.

The autopilot can research, score, design offers and prepare follow-ups. It
never performs purchases, payments, contracts, publishing, or irreversible
account changes; those remain behind the existing server-side approval gate.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class AutopilotPlan:
    goal: str
    domain: str
    pipeline: list[str]
    autonomous_steps: list[str]
    approval_steps: list[str]


def classify_goal(goal: str) -> str:
    text = goal.lower()
    if any(k in text for k in ("affiliate", "عمولة", "افلييت")):
        return "affiliate"
    if any(k in text for k in ("موقع", "متجر", "website", "store", "seo")):
        return "website"
    if any(k in text for k in ("شراء", "منتج", "مورد", "supplier", "resell", "إعادة بيع")):
        return "commerce"
    if any(k in text for k in ("عميل", "عملاء", "بيع", "خدمة", "service", "lead", "عميل محتمل")):
        return "services"
    if any(k in text for k in ("تسويق", "marketing", "حملة", "campaign")):
        return "marketing"
    return "general"


def build_autopilot_plan(goal: str) -> AutopilotPlan:
    domain = classify_goal(goal)
    common = ["research", "fact_check", "score_opportunities", "measure_and_learn"]
    pipelines = {
        "commerce": ["supplier_research", "market_research", "finance_analysis", "negotiation_plan", "sales_plan"],
        "affiliate": ["affiliate_research", "audience_fit", "content_plan", "experiment", "performance_review"],
        "services": ["lead_discovery", "customer_research", "service_offer", "sales_plan", "follow_up"],
        "website": ["website_audit", "conversion_analysis", "site_brief", "service_offer", "sales_plan"],
        "marketing": ["market_research", "customer_psychology", "campaign_plan", "experiment", "performance_review"],
        "general": ["opportunity_discovery", "business_model", "risk_review", "execution_plan"],
    }
    approval = ["purchase", "payment", "contract", "publish", "irreversible", "account_change"]
    return AutopilotPlan(goal=goal, domain=domain, pipeline=common + pipelines[domain],
                         autonomous_steps=common + pipelines[domain], approval_steps=approval)


def run_autopilot(orchestrator: Any, goal: str, *, execute: bool = True) -> dict[str, Any]:
    plan = build_autopilot_plan(goal)
    result: dict[str, Any] = {"status": "planned", "plan": asdict(plan), "results": []}
    if not execute:
        return result

    # Dispatch only agents that are present. Missing optional specialists are
    # reported rather than silently skipped or fabricated.
    agent_map = {
        "research": "economic_intelligence_agent",
        "fact_check": "fact_check_agent",
        "opportunity_discovery": "opportunity_hunter",
        "lead_discovery": "customer_acquisition_agent",
        "customer_research": "customer_relationship_agent",
        "customer_psychology": "customer_psychology_agent",
        "affiliate_research": "revenue_opportunity_suite_agent",
        "market_research": "economic_intelligence_agent",
        "supplier_research": "opportunity_hunter",
        "website_audit": "website_ecommerce_intelligence_agent",
        "service_offer": "service_compiler_agent",
        "sales_plan": "sales_agent",
        "negotiation_plan": "negotiation_agent",
        "finance_analysis": "revenue_agent",
        "business_model": "business_opportunity_factory_agent",
        "execution_plan": "universal_customer_execution_agent",
        "risk_review": "fact_check_agent",
        "follow_up": "customer_conversation_agent",
        "experiment": "reporting_agent",
        "performance_review": "reporting_agent",
    }
    for step in plan.pipeline:
        agent_name = agent_map.get(step)
        if not agent_name:
            result["results"].append({"step": step, "status": "planned_only"})
            continue
        if agent_name not in orchestrator.agents:
            result["results"].append({"step": step, "agent": agent_name, "status": "unavailable"})
            continue
        outcome = orchestrator.dispatch(agent_name, {"goal": goal, "query": goal, "objective": goal})
        result["results"].append({"step": step, "agent": agent_name, "success": outcome.result.success,
                                   "data": outcome.result.data, "error": outcome.result.error})
        if not outcome.result.success:
            result["status"] = "partial"
    return result
