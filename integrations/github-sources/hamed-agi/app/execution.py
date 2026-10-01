from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .memory_store import memory_store
from .planner import planner
from .tooling import tool_registry


class ExecutionLoop:
    """Execute planned missions with per-step auditability and fail-safe behavior."""

    def run(
        self,
        objective: str,
        *,
        target: str | None = None,
        authorized: bool = False,
        dry_run: bool = True,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        mission = planner.plan(objective, target=target)
        started = datetime.now(timezone.utc).isoformat()
        results: list[dict[str, Any]] = []
        blocked: list[dict[str, Any]] = []
        ctx = dict(context or {})
        if target:
            ctx["target"] = target

        for step in mission.metadata["steps"]:
            try:
                result = tool_registry.execute(
                    step["tool"],
                    authorized=authorized,
                    dry_run=dry_run,
                    **ctx,
                )
                item = {"step": step["id"], "tool": step["tool"], "status": "ok", "result": result}
                results.append(item)
                ctx[f"{step['id']}_result"] = result
            except PermissionError as exc:
                item = {"step": step["id"], "tool": step["tool"], "status": "blocked", "reason": str(exc)}
                blocked.append(item)
                results.append(item)
            except Exception as exc:  # noqa: BLE001 - fail-safe execution boundary
                results.append({"step": step["id"], "tool": step["tool"], "status": "error", "reason": str(exc)})

        completed = datetime.now(timezone.utc).isoformat()
        status = "completed" if not any(x["status"] == "error" for x in results) else "degraded"
        output = {
            "status": status,
            "objective": objective,
            "target": target,
            "started_at": started,
            "completed_at": completed,
            "dry_run": dry_run,
            "authorized": authorized,
            "plan": mission.metadata,
            "results": results,
            "blocked_steps": blocked,
            "execution_policy": "no_destructive_actions; financial_and_legal_actions_require_human_approval",
        }
        memory_store.record("execution_cycle", output, source="orvia_execution_loop")
        return output


execution_loop = ExecutionLoop()
