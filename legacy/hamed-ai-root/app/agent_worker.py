"""Safe autonomous worker for Hamed AI."""
from __future__ import annotations

import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .services.mission_runtime import MissionRuntime


class HamedWorker:
    def __init__(self, interval_seconds: int = 900, state_path: str = "data/worker_state.json", mission_path: str = "data/missions.json") -> None:
        self.interval_seconds = max(60, interval_seconds)
        self.state_path = Path(state_path)
        self.missions = MissionRuntime(mission_path)
        self.running = False
        self.last_run: str | None = None
        self.last_result: dict[str, Any] = {}
        self._thread: threading.Thread | None = None

    def _save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps({"last_run": self.last_run, "last_result": self.last_result}, ensure_ascii=False, indent=2), encoding="utf-8")

    def submit_mission(self, goal: str, tasks: list[str] | None = None) -> dict[str, Any]:
        return self.missions.submit(goal, tasks)

    def run_mission_once(self, mission_id: str, executor: Callable[[str], Any]) -> dict[str, Any]:
        return self.missions.run_once(mission_id, executor)

    def run_once(self, *, hooks: list[Callable[[], dict[str, Any]]] | None = None) -> dict[str, Any]:
        started = datetime.now(timezone.utc).isoformat()
        results: list[dict[str, Any]] = []
        for hook in hooks or []:
            try:
                results.append(hook())
            except Exception as exc:  # pragma: no cover
                results.append({"status": "error", "error": str(exc)})
        self.last_run = started
        self.last_result = {"status": "ok" if all(r.get("status") != "error" for r in results) else "partial", "results": results, "safe_mode": True, "mission_count": len(self.missions.list())}
        self._save()
        return self.last_result

    def start(self, *, hooks: list[Callable[[], dict[str, Any]]] | None = None) -> None:
        if self.running:
            return
        self.running = True

        def loop() -> None:
            while self.running:
                self.run_once(hooks=hooks)
                for _ in range(self.interval_seconds):
                    if not self.running:
                        return
                    time.sleep(1)

        self._thread = threading.Thread(target=loop, name="hamed-worker", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.running = False

    def status(self) -> dict[str, Any]:
        return {"running": self.running, "interval_seconds": self.interval_seconds, "last_run": self.last_run, "last_result": self.last_result, "safe_mode": True, "missions": len(self.missions.list())}
