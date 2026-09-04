"""24/7 autonomous Hamed core.

Runs independently of Telegram. It continuously learns, hunts evidence-backed
commercial opportunities and prioritizes reversible revenue work. External
purchases, payments, contracts, publishing, account changes and irreversible
actions remain bounded by server-side authorization rules.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

from app.services.revenue_ceo import RevenueCEO


class AutonomousCore:
    def __init__(self, orchestrator, notify: Optional[Callable[[str], None]] = None) -> None:
        self.orchestrator = orchestrator
        self.notify = notify
        self.enabled = os.getenv("HAMED_AUTONOMOUS_MODE", "true").lower() == "true"
        self.opportunity_enabled = os.getenv("HAMED_OPPORTUNITY_HUNTER", "true").lower() == "true"
        self.interval = max(300, int(os.getenv("HAMED_OPPORTUNITY_INTERVAL", os.getenv("HAMED_AUTONOMOUS_INTERVAL", "1800"))))
        self.daily_target = max(0.0, float(os.getenv("HAMED_DAILY_REVENUE_TARGET", "0")))
        self.state_path = Path(os.getenv("HAMED_AUTONOMOUS_STATE", "hamed_autonomous_state.json"))
        self._stop = threading.Event()
        self._thread = None
        self.state = self._load_state()
        self.revenue_ceo = RevenueCEO()

    def _load_state(self) -> dict:
        try:
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            state.setdefault("cycles", 0)
            state.setdefault("lessons", [])
            state.setdefault("opportunities", [])
            state.setdefault("revenue_focus", None)
            state.setdefault("ceo_revenue_focus", None)
            state.setdefault("last_run", None)
            return state
        except Exception:
            return {"cycles": 0, "lessons": [], "opportunities": [], "revenue_focus": None, "ceo_revenue_focus": None, "last_run": None}

    def _save_state(self) -> None:
        try:
            self.state_path.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print("Autonomous state save error:", type(exc).__name__, exc, flush=True)

    def start(self) -> None:
        if not self.enabled or (self._thread and self._thread.is_alive()):
            return
        self._thread = threading.Thread(target=self._loop, name="hamed-autonomous-core", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _loop(self) -> None:
        print("Hamed Autonomous Core: ONLINE (24/7 bounded mode)", flush=True)
        while not self._stop.is_set():
            try:
                self.run_cycle()
            except Exception as exc:
                print("Autonomous cycle error:", type(exc).__name__, exc, flush=True)
            self._stop.wait(self.interval)

    def run_cycle(self) -> None:
        now = datetime.now(timezone.utc).isoformat()
        topics = [
            "public buying requests, RFQs, tenders and procurement needs for products and services",
            "B2B buyers, suppliers, distributors, agents, wholesalers and export opportunities",
            "lawful wholesale arbitrage, clearance stock, inventory liquidation and bulk-deal opportunities",
            "local alternatives to imports, private-label products and product-demand validation",
            "digital services, AI agents, websites, CRM, customer support, sales and marketing services businesses need",
            "affiliate programs, brokerage, referrals, commission partnerships and service-reseller opportunities",
            "pricing, competitor gaps, market intelligence and evidence-backed revenue opportunity scoring",
            "seasonal demand, repeat orders, upsell, cross-sell, lead recovery and customer retention",
            "cross-border trade, demand prediction, supplier negotiation, corporate accounts and recurring revenue",
            "unused capacity, dead stock, bundles, churn, referral networks, revenue experiments and profit leaks",
            "deal hunting, price arbitrage, buyer intent, quote auctions, customer lifetime value and cashflow",
            "sales, negotiation and customer psychology: discovery, buyer signals, objections and conversion",
        ]
        topic = topics[self.state.get("cycles", 0) % len(topics)]

        try:
            learning_item = self.orchestrator.learning_council.study(topic)
            evidence = learning_item.evidence
        except Exception:
            evidence = self.orchestrator.research_for_learning(topic)

        summary = self.orchestrator.provider.generate_response(
            [{"role": "user", "content": "Analyze this research for actionable, ethical commercial opportunities and better customer responses.\n\n" + evidence[:12000]}],
            system=(
                "You are Hamed's autonomous revenue radar. Identify concrete, evidence-backed and lawful revenue opportunities. "
                "Consider brokerage, service reselling, RFQs, tenders, wholesale arbitrage, export, import substitution, "
                "distribution, private label, bulk deals, clearance, product validation, competitor gaps, quote comparison, "
                "procurement services, sales/customer-service services, AI website agents, CRM services, pricing consulting, "
                "inventory optimization, repeat orders, commission partnerships, market intelligence, seasonal demand, "
                "cross-border trade, demand prediction, supplier negotiation, corporate accounts, recurring revenue, unused capacity, "
                "dead stock, bundle optimization, churn prevention, referral networks, measurable revenue experiments, profit leaks, "
                "deal hunting, price arbitrage, buyer intent, quote auctions, customer lifetime value and cashflow. "
                "For each opportunity extract product/service, customer need, location, quantity when present, supplier/research targets, "
                "evidence, estimated value only when supported, speed, effort, risk and next reversible step. "
                "Rank opportunities by evidence, customer fit, value, speed, effort and risk. Never invent facts, prices, suppliers, "
                "demand, commissions or results. Never spam, deceive, bypass platform rules, scrape behind access controls, "
                "or exploit vulnerabilities. External purchases, payments, contracts, publishing and irreversible actions "
                "must stay behind authorized execution controls. Psychology is for understanding needs, never manipulation."
            ),
        )
        item = {"time": now, "topic": topic, "summary": summary[:6000], "evidence": evidence[:6000]}
        self.state["cycles"] = int(self.state.get("cycles", 0)) + 1
        self.state["last_run"] = now
        self.state.setdefault("lessons", []).append({"time": now, "topic": topic, "evidence": evidence[:6000]})
        self.state["lessons"] = self.state["lessons"][-100:]
        self.state.setdefault("opportunities", []).append(item)
        self.state["opportunities"] = self.state["opportunities"][-50:]

        if self.opportunity_enabled:
            try:
                discovered = self.orchestrator.discover_opportunity(
                    source="autonomous_revenue_radar", demand=summary[:4000], evidence=[evidence[:6000]]
                )
                item["opportunity_id"] = discovered["opportunity_id"]
            except Exception as exc:
                item["hunter_error"] = type(exc).__name__

        try:
            candidates = []
            for opportunity in self.state.get("opportunities", [])[-20:]:
                candidates.append({
                    "title": opportunity.get("topic", "observed opportunity"),
                    "next_action": "research_and_prepare_offer",
                    "evidence": 1 if opportunity.get("evidence") else 0,
                    "fit": 0.5 if opportunity.get("opportunity_id") else 0.0,
                    "value": 0.0,
                    "speed": 0.5,
                    "effort": 1.0,
                    "risk": 0.0,
                })
            focus = self.orchestrator.revenue_hub.revenue_brain(candidates, daily_target=self.daily_target)
            self.state["revenue_focus"] = {"time": now, **focus}
            item["revenue_focus"] = focus
        except Exception as exc:
            item["revenue_brain_error"] = type(exc).__name__

        try:
            ceo_focus = self.revenue_ceo.decide(
                self.state.get("opportunities", [])[-20:], daily_target=self.daily_target
            )
            self.state["ceo_revenue_focus"] = {"time": now, **ceo_focus}
            item["ceo_revenue_focus"] = ceo_focus
        except Exception as exc:
            item["ceo_revenue_brain_error"] = type(exc).__name__

        self._save_state()
        if self.notify:
            focus_text = ""
            focus = self.state.get("ceo_revenue_focus", {}).get("focus")
            if focus:
                focus_text = "\n\n👑 CEO Revenue Brain: " + str(focus.get("title", "next opportunity"))
            self.notify("🧠 Hamed Revenue Radar completed a new learning/opportunity cycle." + focus_text + "\n\n" + summary[:3500])
