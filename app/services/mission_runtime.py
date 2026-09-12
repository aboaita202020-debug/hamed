"""Persistent, idempotent mission runtime for Hamed autonomous work."""
from __future__ import annotations

import hashlib
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


class MissionRuntime:
    """Small durable mission queue for safe autonomous planning/execution.

    The runtime persists only mission metadata/results. Actual high-impact actions
    must still be implemented behind the existing permission/approval layer.
    """

    def __init__(self, state_path: str = "data/missions.json") -> None:
        self.state_path = Path(state_path)
        self._lock = threading.RLock()
        self._state = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return {"missions": {}}
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) and isinstance(data.get("missions"), dict) else {"missions": {}}
        except (OSError, ValueError, TypeError):
            return {"missions": {}}

    def _save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.state_path)

    @staticmethod
    def mission_id(goal: str) -> str:
        return hashlib.sha256(goal.strip().encode("utf-8")).hexdigest()[:16]

    def submit(self, goal: str, tasks: list[str] | None = None) -> dict[str, Any]:
        goal = goal.strip()
        if not goal:
            raise ValueError("mission goal is required")
        with self._lock:
            mid = self.mission_id(goal)
            mission = self._state["missions"].get(mid)
            if mission is None:
                mission = {
                    "id": mid,
                    "goal": goal,
                    "tasks": [{"id": self.task_id(mid, task), "description": task, "status": "pending", "result": None} for task in (tasks or [goal])],
                    "status": "pending",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
                self._state["missions"][mid] = mission
                self._save()
            return mission

    @staticmethod
    def task_id(mission_id: str, description: str) -> str:
        return hashlib.sha256(f"{mission_id}:{description.strip()}".encode("utf-8")).hexdigest()[:16]

    def get(self, mission_id: str) -> dict[str, Any] | None:
        with self._lock:
            mission = self._state["missions"].get(mission_id)
            return json.loads(json.dumps(mission, ensure_ascii=False)) if mission else None

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            return json.loads(json.dumps(list(self._state["missions"].values()), ensure_ascii=False))

    def run_once(self, mission_id: str, executor: Callable[[str], Any]) -> dict[str, Any]:
        with self._lock:
            mission = self._state["missions"].get(mission_id)
            if mission is None:
                raise KeyError(mission_id)
            task = next((t for t in mission["tasks"] if t["status"] == "pending"), None)
            if task is None:
                mission["status"] = "completed"
                self._save()
                return mission
            task["status"] = "running"
            mission["status"] = "running"
            mission["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._save()

        try:
            result = executor(task["description"])
            status = "completed"
        except Exception as exc:  # defensive boundary; task can be retried safely
            result = {"error": str(exc), "type": type(exc).__name__}
            status = "failed"

        with self._lock:
            task["status"] = status
            task["result"] = result
            mission["updated_at"] = datetime.now(timezone.utc).isoformat()
            if status == "failed":
                mission["status"] = "failed"
            elif all(t["status"] == "completed" for t in mission["tasks"]):
                mission["status"] = "completed"
            else:
                mission["status"] = "pending"
            self._save()
            return json.loads(json.dumps(mission, ensure_ascii=False))
