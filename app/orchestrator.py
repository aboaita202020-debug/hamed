from __future__ import annotations

from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json
import threading
from datetime import datetime, timezone
from pathlib import Path

from .agent_bus import agent_bus
from .agents import DEFAULT_AGENTS, AgentResult


ACTIVITY_PATH = Path(__file__).resolve().parent.parent / "data" / "agent_activity.jsonl"
_ACTIVITY_LOCK = threading.Lock()


def _activity(event: str, agent: str, status: str, objective: str, output: Any = None) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "agent": agent,
        "status": status,
        "objective": objective[:1200],
    }
    if output is not None:
        record["output"] = str(output)[:4000]
    try:
        ACTIVITY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _ACTIVITY_LOCK:
            with ACTIVITY_PATH.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass


class Orchestrator:
    def __init__(self) -> None:
        self.agents = {agent.name: agent for agent in DEFAULT_AGENTS}

    def dispatch(self, agent_name: str, payload: dict[str, Any]) -> AgentResult:
        agent = self.agents.get(agent_name)
        if agent is None:
            raise KeyError(f"Unknown agent: {agent_name}")
        return agent.run(payload)

    def collaborate(self, objective: str, agent_names: list[str] | None = None) -> list[dict[str, Any]]:
        names = agent_names or list(self.agents)
        context: dict[str, Any] = {"objective": objective, "collaboration": True, "swarm_size": len(self.agents)}
        results: list[dict[str, Any]] = []
        max_workers = max(1, min(int(os.getenv("HAMED_AGENT_WORKERS", "20")), len(names)))
        def run_one(name: str):
            _activity("started", name, "working", objective)
            try:
                result = self.dispatch(name, {"objective": objective, "context": context})
                _activity("completed", result.agent, result.status, objective, result.output)
                return {"agent": result.agent, "status": result.status, "output": result.output}
            except Exception as exc:
                _activity("error", name, "error", objective, f"{type(exc).__name__}: {exc}")
                raise
        # Agents execute as a cooperative worker pool rather than 2020 OS processes.
        # This lets all logical agents participate without requiring 2020 servers.
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="hamed-agent") as pool:
            futures = {pool.submit(run_one, name): name for name in names}
            for future in as_completed(futures):
                item = future.result()
                results.append(item)
                context[item["agent"]] = item["output"]
                agent_bus.broadcast(item["agent"], "finding", item["output"], names)
        order = {name: i for i, name in enumerate(names)}
        results.sort(key=lambda item: order.get(item["agent"], len(order)))
        return results

    def run(self, objective: str) -> list[dict[str, Any]]:
        return self.collaborate(objective)

orchestrator = Orchestrator()
