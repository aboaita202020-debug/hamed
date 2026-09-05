from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import Any, Callable, Iterable
import math
import uuid

IDEA_FAMILIES = (
    "lost_customer_recovery","dead_lead_revival","quote_recovery","missed_demand","buyer_pool","supplier_competition","unused_capacity","unused_assets","product_gaps","bundles","business_matching","distributor_hunting","export_buyer_hunting","private_label","purchasing_club","clearance","seasonal_demand","local_market_gaps","business_pain","ai_outsourcing","process_to_agent","saas_mining","micro_saas","benchmarking","business_health","revenue_leaks","margin_optimization","customer_expansion","referral_network","opportunity_exchange","universal_services","market_intelligence","pricing_intelligence","competitive_monitoring","supplier_intelligence","tender_rfp","logistics_matching","warehouse_matching","equipment_matching","spare_parts","maintenance","inventory","energy_optimization","cloud_cost_optimization","telecom_optimization","predictive_maintenance","fleet_optimization","returns_warranty","demand_forecasting","document_automation","translation_localization","voice_usage","sales_training","learning_marketplace","white_label","enterprise","certification","governance","data_products","business_builder","franchise_scout","acquisition_research","cross_border","affiliate_referral","digital_products","subscriptions"
)
PORTFOLIOS = ("CASH_NOW","RECURRING","SCALE","EXPERIMENT","ASSET")

@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    family: str
    title: str
    problem: str
    payer: str
    solution: str
    evidence: tuple[str, ...]
    expected_revenue: float | None
    expected_cost: float | None
    probability: float
    score: float
    portfolio: str
    next_action: str
    status: str = "READY"
    approval_required: bool = False

class OpportunityMachine:
    """Universal idea generator + multi-mission executor."""
    def __init__(self, max_workers: int = 8): self.max_workers = max(1, int(max_workers))

    @staticmethod
    def expected_value(revenue: float | None, cost: float | None, probability: float) -> float | None:
        if not 0 <= probability <= 1: raise ValueError("probability must be between 0 and 1")
        if revenue is None or cost is None: return None
        if revenue < 0 or cost < 0: raise ValueError("revenue/cost must be non-negative")
        return (revenue - cost) * probability

    @staticmethod
    def score(*, evidence_count: int, customer_fit: float, probability: float, expected_revenue: float | None = None, expected_cost: float | None = None, time_cost: float = 1, risk: float = 0) -> float:
        if evidence_count < 0 or not 0 <= customer_fit <= 1 or not 0 <= probability <= 1 or time_cost <= 0 or not 0 <= risk <= 1: raise ValueError("invalid scoring inputs")
        evidence = min(1, evidence_count / 5)
        ev = OpportunityMachine.expected_value(expected_revenue, expected_cost, probability)
        value = 0 if ev is None else min(1, max(0, ev) / 100000)
        raw = 100 * (.35 * evidence + .30 * customer_fit + .25 * probability + .10 * value)
        return round(raw * (1 - .30 * risk) / max(1, math.sqrt(time_cost)), 2)

    @staticmethod
    def portfolio(family: str, ev: float | None) -> str:
        if family in {"micro_saas","saas_mining","process_to_agent","data_products","enterprise"}: return "SCALE"
        if family in {"subscriptions","business_health","competitive_monitoring","supplier_intelligence"}: return "RECURRING"
        if family in {"product_gaps","business_pain","pricing_intelligence","revenue_experiments"}: return "EXPERIMENT"
        return "CASH_NOW" if ev is not None else "ASSET"

    def discover(self, signal: dict[str, Any]) -> list[Opportunity]:
        problem = str(signal.get("problem", "market problem to validate"))
        payer = str(signal.get("payer", "payer to identify"))
        domain = str(signal.get("domain", "general"))
        evidence = tuple(str(x) for x in signal.get("evidence", []) if str(x).strip())
        fit, probability = float(signal.get("customer_fit", .5)), float(signal.get("probability", .5))
        revenue, cost = signal.get("expected_revenue"), signal.get("expected_cost")
        out = []
        for family in IDEA_FAMILIES:
            ev = self.expected_value(revenue, cost, probability)
            out.append(Opportunity(uuid.uuid4().hex, family, f"{family.replace('_',' ').title()} — {domain}", problem, payer, str(signal.get("solution") or f"Test {family.replace('_',' ')}"), evidence, float(revenue) if revenue is not None else None, float(cost) if cost is not None else None, probability, self.score(evidence_count=len(evidence), customer_fit=fit, probability=probability, expected_revenue=revenue, expected_cost=cost, time_cost=float(signal.get("time_cost",1)), risk=float(signal.get("risk",0))), self.portfolio(family, ev), "verify_evidence_and_design_small_test"))
        return out

    def create_missions(self, opportunities: Iterable[Opportunity], max_missions: int | None = None) -> list[dict[str, Any]]:
        items = sorted(opportunities, key=lambda x: x.score, reverse=True)
        if max_missions is not None: items = items[:max(0, max_missions)]
        return [{"mission_id": o.opportunity_id, "opportunity_id": o.opportunity_id, "family": o.family, "goal": o.solution, "next_action": o.next_action, "portfolio": o.portfolio, "status": "QUEUED", "approval_required": o.approval_required} for o in items]

    def execute_missions(self, missions: Iterable[dict[str, Any]], executor: Callable[[dict[str, Any]], Any]) -> list[dict[str, Any]]:
        items = list(missions)
        if not items: return []
        results = []
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(items))) as pool:
            futures = {pool.submit(executor, m): m for m in items}
            for f in as_completed(futures):
                m = futures[f]
                try: results.append({"mission_id": m["mission_id"], "status": "COMPLETED", "result": f.result()})
                except Exception as exc: results.append({"mission_id": m["mission_id"], "status": "FAILED", "error": f"{type(exc).__name__}: {exc}"})
        return results

    @staticmethod
    def learn(results: Iterable[dict[str, Any]]) -> dict[str, Any]:
        results = list(results); completed = sum(x.get("status") == "COMPLETED" for x in results); failed = sum(x.get("status") == "FAILED" for x in results)
        return {"completed": completed, "failed": failed, "success_rate": completed / len(results) if results else None, "learning_action": "update_opportunity_ranking_and_retry_policy"}

    def snapshot(self, signal: dict[str, Any]) -> dict[str, Any]:
        opportunities = self.discover(signal); missions = self.create_missions(opportunities)
        return {"idea_families": len(IDEA_FAMILIES), "opportunities": [asdict(x) for x in opportunities], "missions": missions, "autonomous_loop": ["DISCOVER","VERIFY","SCORE","MISSION","EXECUTE","MEASURE","LEARN","REPEAT"], "no_guaranteed_income": True}
