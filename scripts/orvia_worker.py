"""ORVIA/HAMED autonomous commercial worker for the current root application.

Runs the current `app.autonomous.autonomous_agent` instead of the removed
legacy Telegram worker, and exposes a tiny health endpoint for PaaS workers.
"""
from __future__ import annotations

import json
import os
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from app.autonomous import autonomous_agent

INTERVAL = max(60, int(os.getenv("HAMED_AUTONOMOUS_INTERVAL", "1800")))
PORT = int(os.getenv("PORT", os.getenv("HAMED_WORKER_PORT", "8010")))

_state = {
    "status": "starting",
    "started_at": None,
    "last_cycle_at": None,
    "last_error": None,
    "cycles": 0,
}
_lock = threading.Lock()


def _save_state(status: str, error: str | None = None) -> None:
    with _lock:
        _state["status"] = status
        _state["last_error"] = error


def run_cycle() -> None:
    started = datetime.now(timezone.utc).isoformat()
    _save_state("running")
    with _lock:
        _state["last_cycle_at"] = started
    try:
        result = autonomous_agent.run_cycle()
        with _lock:
            _state["cycles"] += 1
            _state["status"] = str(result.get("status", "completed"))
            _state["last_error"] = None
    except Exception as exc:
        _save_state("error", f"{type(exc).__name__}: {exc}")


def loop() -> None:
    while True:
        run_cycle()
        time.sleep(INTERVAL)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/health", "/status"):
            self.send_response(404)
            self.end_headers()
            return
        with _lock:
            body = json.dumps(
                {"ok": True, "service": "orvia-autonomous-worker", **_state},
                ensure_ascii=False,
            ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        return


def main() -> None:
    with _lock:
        _state["started_at"] = datetime.now(timezone.utc).isoformat()
    threading.Thread(target=loop, daemon=True, name="orvia-autonomous-loop").start()
    print(
        f"ORVIA autonomous worker started; interval={INTERVAL}s port={PORT}",
        flush=True,
    )
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
