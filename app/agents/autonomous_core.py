"""24/7 autonomous Hamed core.

Runs independently of Telegram. It plans bounded, reversible commercial work,
keeps lightweight persistent state, learns from research and public educational
material, and never performs purchases, payments, contracts, account changes,
publishing, or irreversible actions without an explicit authorization path.
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional


class AutonomousCore:
    def __init__(self, orchestrator, notify: Optional[Callable[[str], None]] = None) -> None:
        self.orchestrator = orchestrator
        self.notify = notify
        self.enabled = os.getenv("HAMED_AUTONOMOUS_MODE", "true").lower() == "true"
        self.opportunity_enabled = os.getenv("HAMED_OPPORTUNITY_HUNTER", "true").lower() == "true"
        self.interval = max(300, int(os.getenv("HAMED_OPPORTUNITY_INTERVAL", os.getenv("HAMED_AUTONOMOUS_INTERVAL", "1800"))))
        self.state_path = Path(os.getenv("HAMED_AUTONOMOUS_STATE", "hamed_autonomous_state.json"))
        self._stop = threading.Event()
        self._thread = None
        self.state = self._load_state()

    def _load_state(self) -> dict:
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except Exception:
            return {"cycles": 0, "lessons": [], "opportunities": [], "last_run": None}

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
            "current public buying requests for food, clothing, electronics, home goods and industrial products",
            "businesses with weak websites or online stores that publicly show a need for digital improvement",
            "current demand for digital services, ecommerce, marketing, SEO, automation and AI services",
            "affiliate and commercial opportunities with clear public evidence and ethical outreach paths",
            "sales, marketing and customer psychology: discovery, buyer signals, objections and conversion",
            "sales training videos and public transcripts about consultative selling, negotiation and objection handling",
        ]
        topic = topics[self.state.get("cycles", 0) % len(topics)]

        # Broad learning pass: articles + research + public educational videos/transcripts when available.
        try:
            learning_item = self.orchestrator.learning_council.study(topic)
            evidence = learning_item.evidence
        except Exception:
            evidence = self.orchestrator.research_for_learning(topic)

        summary = self.orchestrator.provider.generate_response(
            [{"role": "user", "content": "Analyze this research for actionable, ethical commercial opportunities and better customer responses.\n\n" + evidence[:12000]}],
            system=(
                "You are Hamed's autonomous learning and opportunity-hunting layer. Identify concrete, "
                "evidence-backed lessons and opportunities. For sales, infer only observable customer signals; "
                "classify objections such as price, trust, fit, timing, authority and logistics when supported. "
                "Turn lessons into better discovery questions, value framing, personalized offers and next steps. "
                "For each opportunity extract product/service, quantity when present, location, customer need, "
                "supplier/research targets and next reversible step. Never invent facts. Never propose bypassing "
                "platform rules, spam, deception, unauthorized access, purchases, payments, contracts, publishing, "
                "or irreversible actions. Psychology is for understanding needs, never manipulation or exploitation."
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
                    source="autonomous_web_research", demand=summary[:4000], evidence=[evidence[:6000]]
                )
                item["opportunity_id"] = discovered["opportunity_id"]
            except Exception as exc:
                item["hunter_error"] = type(exc).__name__

        self._save_state()
        if self.notify:
            self.notify("🧠 Hamed autonomous learning/opportunity cycle completed.\n\n" + summary[:3500])
