"""24/7 autonomous Hamed core with bounded commercial execution."""
from __future__ import annotations
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional
from app.services.revenue_ceo import RevenueCEO
from app.services.execution_adapters import ExecutionAdapters
from app.agents.autonomous_execution import AutonomousExecutionEngine


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
        self.adapters = ExecutionAdapters()
        self.execution = AutonomousExecutionEngine(self._execute_action)

    def _load_state(self) -> dict:
        try:
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            for key, default in (("cycles", 0), ("lessons", []), ("opportunities", []), ("revenue_focus", None), ("ceo_revenue_focus", None), ("executions", []), ("last_run", None)):
                state.setdefault(key, default)
            return state
        except Exception:
            return {"cycles": 0, "lessons": [], "opportunities": [], "revenue_focus": None, "ceo_revenue_focus": None, "executions": [], "last_run": None}

    def _save_state(self) -> None:
        try:
            self.state_path.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print("Autonomous state save error:", type(exc).__name__, exc, flush=True)

    def start(self) -> None:
        if not self.enabled or (self._thread and self._thread.is_alive()): return
        self._thread = threading.Thread(target=self._loop, name="hamed-autonomous-core", daemon=True)
        self._thread.start()

    def stop(self) -> None: self._stop.set()

    def _loop(self) -> None:
        print("Hamed Autonomous Core: ONLINE (24/7 bounded execution)", flush=True)
        while not self._stop.is_set():
            try: self.run_cycle()
            except Exception as exc: print("Autonomous cycle error:", type(exc).__name__, exc, flush=True)
            self._stop.wait(self.interval)

    def _execute_action(self, action: str, opportunity: dict) -> str:
        """Execute reversible work through guarded adapters; never invent a recipient."""
        if action == "market_research":
            return "research queued"
        if action == "offer_build":
            return "offer preparation queued"
        if action == "customer_reply":
            prospect = opportunity.get("prospect") or opportunity.get("customer") or {}
            message = opportunity.get("message") or opportunity.get("offer_message") or ""
            if not isinstance(prospect, dict):
                return "contact blocked: invalid prospect"
            intent = self.adapters.send_telegram(prospect, message)
            return json.dumps(self.adapters.queue(intent), ensure_ascii=False)
        if action == "negotiate":
            return "negotiation plan prepared within policy"
        if action == "followup":
            prospect = opportunity.get("prospect") or opportunity.get("customer") or {}
            if isinstance(prospect, dict) and prospect.get("opted_out"):
                return "follow-up blocked: opted out"
            return "follow-up scheduled as a reversible task"
        return "action acknowledged"

    def run_cycle(self) -> None:
        now = datetime.now(timezone.utc).isoformat()
        topics = [
            "public buying requests, RFQs, tenders and procurement needs",
            "B2B buyers, suppliers, distributors and export opportunities",
            "lawful wholesale arbitrage, clearance stock and bulk deals",
            "private label, import substitution and product-demand validation",
            "digital services, AI agents, websites, CRM and customer support",
            "affiliate, brokerage, referrals, commissions and service reselling",
            "pricing, competitor gaps and market intelligence",
            "seasonal demand, repeat orders, upsell, cross-sell and lead recovery",
            "cross-border trade, demand prediction, supplier negotiation and recurring revenue",
            "unused capacity, dead stock, bundles, churn, referrals, experiments and profit leaks",
            "deal hunting, price arbitrage, buyer intent, quote auctions, lifetime value and cashflow",
        ]
        topic = topics[self.state.get("cycles", 0) % len(topics)]
        try:
            learning_item = self.orchestrator.learning_council.study(topic)
            evidence = learning_item.evidence
        except Exception:
            evidence = self.orchestrator.research_for_learning(topic)
        summary = self.orchestrator.provider.generate_response(
            [{"role": "user", "content": "Analyze this research for actionable, ethical commercial opportunities and next steps.\n\n" + evidence[:12000]}],
            system="Find evidence-backed lawful opportunities. Never invent facts, prices, suppliers, demand, commissions or results. No spam, deception, platform bypass, access-control bypass, or manipulation. External purchases, payments, contracts, publishing and irreversible actions require authorized controls."
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
                discovered = self.orchestrator.discover_opportunity(source="autonomous_revenue_radar", demand=summary[:4000], evidence=[evidence[:6000]])
                item["opportunity_id"] = discovered["opportunity_id"]
            except Exception as exc: item["hunter_error"] = type(exc).__name__
        try:
            ceo_focus = self.revenue_ceo.decide(self.state.get("opportunities", [])[-20:], daily_target=self.daily_target)
            self.state["ceo_revenue_focus"] = {"time": now, **ceo_focus}
            item["ceo_revenue_focus"] = ceo_focus
            if ceo_focus.get("focus"):
                execution = self.execution.execute(ceo_focus["focus"])
                self.state.setdefault("executions", []).append({"time": now, "opportunity": ceo_focus["focus"], "result": execution})
                self.state["executions"] = self.state["executions"][-100:]
                item["execution"] = execution
        except Exception as exc: item["execution_error"] = type(exc).__name__
        self._save_state()
        if self.notify:
            focus = self.state.get("ceo_revenue_focus", {}).get("focus") or {}
            self.notify("🧠 Hamed نفّذ دورة البحث والتجهيز الذاتية.\n🎯 الفرصة: " + str(focus.get("title", "جارٍ بناء قاعدة أدلة")) + "\n\n" + summary[:2500])
