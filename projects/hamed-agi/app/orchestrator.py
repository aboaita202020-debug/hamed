from __future__ import annotations

from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from .agent_bus import agent_bus
from .agents import DEFAULT_AGENTS, AgentResult


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
            result = self.dispatch(name, {"objective": objective, "context": context})
            return {"agent": result.agent, "status": result.status, "output": result.output}
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
