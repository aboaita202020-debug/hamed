"""Always-on Hamed learning-first autonomous loop.

Hamed completes a broad internet-learning phase before generating business opportunities.
Learning is autonomous; purchases, payments, contracts and irreversible/high-impact actions
remain behind the existing permission/approval layer.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.learning import LearningMemory
from app.provider_router import provider_router
from app.orchestrator import Orchestrator


class LearningCouncil:
    def __init__(self, provider):
        self.provider = provider
        self.memory = LearningMemory()

    def study(self, topic):
        prompt = f"Study this business topic and return evidence-backed practical lessons: {topic}"
        result = self.provider.generate(prompt)
        text = getattr(result, "text", str(result))
        return type("StudyResult", (), {"evidence": text})()

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "autonomous_state.json"
PORT = int(os.getenv("HAMED_AUTONOMOUS_PORT", "8010"))
INTERVAL = int(os.getenv("HAMED_AUTONOMOUS_INTERVAL", "1800"))

# Phase 1: build the knowledge base first. Each cycle researches one topic from the public web.
LEARNING_TOPICS = [
    "sales fundamentals, consultative selling, customer discovery and buyer signals",
    "B2B sales, brokerage, supplier discovery and buyer discovery",
    "negotiation, pricing, objections, value framing and deal structures",
    "customer psychology, behavioral economics and ethical persuasion",
    "marketing strategy, positioning, segmentation and go-to-market",
    "digital marketing, SEO, content marketing and conversion optimization",
    "lead generation, outbound sales, prospecting and CRM workflows",
    "e-commerce growth, marketplaces, product pages, CRO and retention",
    "affiliate marketing, product research, demand signals and attribution",
    "service businesses, freelancing, productized services and recurring revenue",
    "competitive intelligence, market research and industry analysis",
    "economic intelligence, pricing signals, supply chains and import opportunities",
    "customer service, retention, loyalty, reviews and complaint handling",
    "business analytics, unit economics, margins, CAC, LTV and ROI",
    "startup strategy, business models, validation and opportunity discovery",
    "Arabic markets, Arab consumer behavior and cross-border commerce",
    "website building, online stores, landing pages and digital conversion",
    "sales automation, AI agents, workflow automation and responsible autonomy",
    "successful entrepreneurs, business case studies and lessons from failures",
    "books, academic research, courses, interviews, podcasts and educational videos for business",
]

_state = {
    "status": "starting",
    "started_at": None,
    "last_cycle_at": None,
    "last_topic": None,
    "phase": "internet_learning",
    "learning_topics_total": len(LEARNING_TOPICS),
    "learning_topics_completed": 0,
    "cycles": 0,
    "lessons": 0,
    "opportunity_reports": 0,
    "agents_total": 0,
    "agents_dispatched_last_cycle": 0,
    "agents_completed_last_cycle": 0,
    "last_error": None,
}
_lock = threading.Lock()


def save_state() -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(_state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def ensure_local_brain() -> None:
    if os.getenv("HAMED_OLLAMA_ENABLED", "1").lower() in {"0", "false", "no"}:
        return
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    try:
        import requests
        requests.get(base_url + "/api/tags", timeout=2)
        return
    except Exception:
        pass
    if os.name != "nt":
        return
    try:
        subprocess.Popen(["ollama", "serve"], cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        time.sleep(3)
    except (FileNotFoundError, OSError):
        pass


def log_learning(topic: str, item, phase: str) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": phase,
        "topic": topic,
        "learning": item.evidence[:20000],
    }
    log_path = ROOT / "data" / "autonomous_learning.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_learning_cycle(learner: LearningCouncil, index: int) -> bool:
    topic = LEARNING_TOPICS[index]
    with _lock:
        _state["status"] = "internet_learning"
        _state["phase"] = "internet_learning"
        _state["last_topic"] = topic
        _state["last_cycle_at"] = datetime.now(timezone.utc).isoformat()
        _state["last_error"] = None
        save_state()

    item = learner.study(topic)
    log_learning(topic, item, "internet_learning")
    with _lock:
        _state["learning_topics_completed"] += 1
        _state["cycles"] += 1
        _state["lessons"] += 1
        save_state()
    return True


def run_opportunity_cycle(provider, learner: LearningCouncil, orchestrator: Orchestrator, index: int) -> None:
    topic = LEARNING_TOPICS[index % len(LEARNING_TOPICS)]
    with _lock:
        _state["status"] = "learning_and_working"
        _state["phase"] = "continuous_learning_and_work"
        _state["last_topic"] = topic
        _state["last_cycle_at"] = datetime.now(timezone.utc).isoformat()
        _state["last_error"] = None
        save_state()

    item = learner.study(topic)
    task = (
        "Act as Hamed's autonomous business operating council. Use the current evidence-backed learning report "
        "to identify 5 concrete opportunities for Arab markets. Include customer, problem, offer, acquisition "
        "channel, estimated effort, risks, verification steps and first action. Do not invent companies, prices "
        "or facts. Separate evidence from assumptions. Never recommend purchases or irreversible actions without authorization.\n\n"
        "LEARNING REPORT:\n" + item.evidence
    )
    growth_task = (
        "Run HAMED Growth Engine on this evidence. Identify measurable growth experiments, target customer, problem, offer, acquisition channel, KPI, test, expected signal, and next iteration. Separate evidence from assumptions.\n\nLEARNING REPORT:\n" + item.evidence
    )
    # Every logical agent participates in the autonomous work cycle. The orchestrator keeps
    # the physical worker pool bounded (20 by default), so 2020 logical agents do not become
    # 2020 OS processes. A smaller executive synthesis pass remains for cross-functional output.
    all_agent_names = list(orchestrator.agents)
    with _lock:
        _state["agents_total"] = len(all_agent_names)
        _state["agents_dispatched_last_cycle"] = len(all_agent_names)
        _state["agents_completed_last_cycle"] = 0
        save_state()
    swarm_task = (
        "Participate as your specialized HAMED agent in the autonomous business operating cycle. "
        "Use the learning evidence below. Produce one concrete finding, improvement, opportunity, "
        "risk, customer insight, experiment, or operational action relevant to your specialization. "
        "Do not invent facts; separate evidence from assumptions. Do not execute financial, legal, "
        "purchase, contract, or irreversible actions. Return concise, actionable output.\n\n"
        "LEARNING REPORT:\n" + item.evidence
    )
    report = orchestrator.collaborate(swarm_task, agent_names=all_agent_names)
    with _lock:
        _state["agents_completed_last_cycle"] = len(report)
        save_state()
    growth_report = orchestrator.collaborate(growth_task, agent_names=["marketing", "analytics", "sales", "customer_psychology"])
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), "topic": topic, "learning": item.evidence[:12000], "growth": growth_report, "opportunities": report}

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
    ensure_local_brain()
    provider = provider_router
    learner = LearningCouncil(provider)
    orchestrator = Orchestrator()
    index = 0
    work_index = 0

    # Learning and business work run together from the first cycle; learning never blocks revenue discovery.
    while True:
        try:
            run_learning_cycle(learner, index % len(LEARNING_TOPICS))
            run_opportunity_cycle(provider, learner, orchestrator, work_index)
            index += 1
            work_index += 1
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
