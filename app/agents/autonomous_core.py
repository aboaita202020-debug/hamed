"""24/7 autonomous Hamed core.

Runs independently of Telegram. It plans bounded, reversible commercial work,
keeps lightweight persistent state, learns from research, and never performs
purchases, payments, contracts, account changes, publishing, or irreversible
actions without an explicit authorization path.
"""
from __future__ import annotations

import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional


class AutonomousCore:
    def __init__(self, orchestrator, notify: Optional[Callable[[str], None]] = None) -> None:
        self.orchestrator = orchestrator
        self.notify = notify
        self.enabled = os.getenv("HAMED_AUTONOMOUS_MODE", "true").lower() == "true"
        self.interval = max(300, int(os.getenv("HAMED_AUTONOMOUS_INTERVAL", "1800")))
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
            "customer psychology and ethical sales objections",
            "ecommerce stores that could benefit from marketing, websites or online stores",
            "affiliate marketing opportunities and conversion strategies",
            "small businesses without websites or ecommerce stores and ethical outreach opportunities",
        ]
        # Rotate research topics so the core continuously learns without hammering providers.
        topic = topics[self.state.get("cycles", 0) % len(topics)]
        evidence = self.orchestrator.research_for_learning(topic)
        summary = self.orchestrator.provider.generate_response(
            [{"role": "user", "content": "Analyze this research for actionable, ethical commercial opportunities.\n\n" + evidence[:12000]}],
            system=(
                "You are Hamed's autonomous commercial planning layer. "
                "Return concise opportunities, customer needs, suggested services/content, "
                "and next reversible steps. Do not invent facts. Never propose bypassing platform rules, "
                "spam, deception, unauthorized access, purchases, payments, contracts, or irreversible actions."
            ),
        )
        item = {"time": now, "topic": topic, "summary": summary[:6000]}
        self.state["cycles"] = int(self.state.get("cycles", 0)) + 1
        self.state["last_run"] = now
        self.state.setdefault("opportunities", []).append(item)
        self.state["opportunities"] = self.state["opportunities"][-50:]
        self._save_state()
        if self.notify:
            self.notify("🧠 Hamed autonomous cycle completed.\n\n" + summary[:3500])
