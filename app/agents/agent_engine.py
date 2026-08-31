"""Autonomous execution engine for Hamed AI.

The engine provides planning, specialist brain selection, verification and
bounded retries. It never stores provider secrets in source code.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable

from .multi_brain import MultiBrainRouter

logger = logging.getLogger(__name__)


@dataclass
class AgentTask:
    goal: str
    context: dict[str, Any] = field(default_factory=dict)
    max_steps: int = 8


@dataclass
class AgentResult:
    status: str
    answer: str
    steps: list[dict[str, Any]]
    provider_names: list[str]


class HamedAgentEngine:
    """Plan -> execute -> verify -> recover loop for commercial tasks."""

    def __init__(self, brain: MultiBrainRouter, tools: dict[str, Callable[..., Any]] | None = None) -> None:
        self.brain = brain
        self.tools = tools or {}

    def _plan(self, task: AgentTask) -> list[dict[str, Any]]:
        prompt = {
            "goal": task.goal,
            "context": task.context,
            "available_tools": sorted(self.tools),
            "rules": [
                "Break the goal into concrete steps.",
                "Prefer reversible and verifiable actions.",
                "Never invent tool results or payment verification.",
                "Respect application-side commercial and authorization rules.",
            ],
            "output": "JSON array of steps with keys action, purpose, tool(optional), input(optional).",
        }
        raw = self.brain.generate_response([{"role": "user", "content": json.dumps(prompt, ensure_ascii=False)}], system="You are Hamed's planning brain. Return valid JSON only.")
        try:
            data = json.loads(raw)
            return data if isinstance(data, list) else [{"action": "respond", "purpose": raw}]
        except Exception:
            return [{"action": "respond", "purpose": raw}]

    def run(self, task: AgentTask) -> AgentResult:
        plan = self._plan(task)[: task.max_steps]
        steps: list[dict[str, Any]] = []
        for index, step in enumerate(plan, 1):
            tool_name = step.get("tool")
            record = {"step": index, "action": step.get("action", "unknown"), "purpose": step.get("purpose", "")}
            if tool_name and tool_name in self.tools:
                try:
                    result = self.tools[tool_name](step.get("input", {}))
                    record["result"] = result
                    record["status"] = "completed"
                except Exception as exc:
                    logger.exception("Tool %s failed", tool_name)
                    record["status"] = "failed"
                    record["error"] = str(exc)
            else:
                record["status"] = "planned"
            steps.append(record)

        verification_prompt = {
            "goal": task.goal,
            "plan": plan,
            "execution": steps,
            "instruction": "Assess whether the goal is complete. Do not claim completion without evidence. Return JSON with complete, answer, missing_steps.",
        }
        raw = self.brain.generate_response([{"role": "user", "content": json.dumps(verification_prompt, ensure_ascii=False)}], system="You are Hamed's verification brain. Return valid JSON only.")
        try:
            verdict = json.loads(raw)
        except Exception:
            verdict = {"complete": False, "answer": raw, "missing_steps": ["structured verification"]}
        status = "completed" if verdict.get("complete") else "partial"
        return AgentResult(status=status, answer=str(verdict.get("answer", "")), steps=steps, provider_names=self.brain.provider_names)
