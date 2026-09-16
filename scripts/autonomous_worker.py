"""Always-on Hamed work + learning loop.

Runs a first cycle immediately, then continues in the background. Learning and
planning are autonomous; purchases, payments, contracts and other irreversible
or high-impact actions remain behind the existing permission/approval layer.
"""
from __future__ import annotations

import json
import os
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.learning import LearningCouncil
from app.agents.provider import MultiBrainProvider
from app.agents.orchestrator import HamedOrchestrator

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "autonomous_state.json"
PORT = int(os.getenv("HAMED_AUTONOMOUS_PORT", "8010"))
INTERVAL = int(os.getenv("HAMED_AUTONOMOUS_INTERVAL", "1800"))
TOPICS = [
    "sales and customer discovery",
    "B2B brokerage and supplier buyer opportunities",
    "affiliate marketing and product demand",
    "e-commerce growth and store optimization",
    "negotiation and pricing",
    "customer psychology and objections",
    "service business opportunities",
    "marketing campaigns and lead generation",
]

_state = {
    "status": "starting",
    "started_at": None,
    "last_cycle_at": None,
    "last_topic": None,
    "cycles": 0,
    "lessons": 0,
    "opportunity_reports": 0,
    "last_error": None,
}
_lock = threading.Lock()


def save_state() -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(_state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def run_cycle(provider: MultiBrainProvider, learner: LearningCouncil, orchestrator: HamedOrchestrator, index: int) -> None:
    topic = TOPICS[index % len(TOPICS)]
    with _lock:
        _state["status"] = "learning_and_working"
        _state["last_topic"] = topic
        _state["last_cycle_at"] = datetime.now(timezone.utc).isoformat()
        _state["last_error"] = None
        save_state()

    # 1) Learn: evidence-oriented commercial lesson.
    item = learner.study(topic)

    # 2) Work: turn the lesson into concrete, low-risk business opportunities and next steps.
    task = (
        "Act as Hamed's autonomous business operating council. Based on the learning report below, "
        "identify 5 concrete opportunities for Arab markets, with customer, problem, offer, acquisition "
        "channel, estimated effort, risks, verification steps and first action. Do not invent companies, "
        "prices or facts. Separate assumptions from evidence. Do not recommend purchases or irreversible "
        "actions without authorization.\n\nLEARNING REPORT:\n" + item.evidence
    )
    report = orchestrator.consult_brains(task, context=f"Current learning topic: {topic}")

    # Persist a compact operational record so learning/work survives restarts.
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "topic": topic,
        "learning": item.evidence[:12000],
        "opportunities": report,
    }
    log_path = ROOT / "data" / "autonomous_activity.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    with _lock:
        _state["cycles"] += 1
        _state["lessons"] += 1
        _state["opportunity_reports"] += 1
        _state["status"] = "idle_until_next_cycle"
        save_state()


def loop() -> None:
    provider = MultiBrainProvider()
    learner = LearningCouncil(provider)
    orchestrator = HamedOrchestrator(brain_provider=provider)
    index = 0
    while True:
        try:
            run_cycle(provider, learner, orchestrator, index)
            index += 1
        except Exception as exc:
            with _lock:
                _state["status"] = "error_waiting_to_retry"
                _state["last_error"] = f"{type(exc).__name__}: {exc}"
                save_state()
        time.sleep(max(60, INTERVAL))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/health", "/status"):
            self.send_response(404)
            self.end_headers()
            return
        with _lock:
            body = json.dumps({"ok": True, "service": "hamed-autonomous-worker", **_state}, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        return


def main() -> None:
    with _lock:
        _state["status"] = "starting"
        _state["started_at"] = datetime.now(timezone.utc).isoformat()
        save_state()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=loop, daemon=True, name="hamed-autonomous-loop").start()
    print(f"Hamed autonomous worker running on http://127.0.0.1:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
