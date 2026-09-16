"""Measure-and-learn experimentation engine."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Experiment:
    hypothesis: str
    baseline: float
    variant: float | None = None
    metric: str = ""
    period: str = ""
    status: str = "planned"
    notes: str = ""

    def record(self, variant: float, notes: str = "") -> dict[str, Any]:
        self.variant = variant
        self.notes = notes
        self.status = "measured"
        delta = variant - self.baseline
        return {**asdict(self), "delta": delta, "relative_change": (delta / self.baseline if self.baseline else None)}


def next_learning_action(experiment: Experiment) -> str:
    if experiment.status != "measured":
        return "collect_measurement"
    if experiment.variant is None:
        return "collect_measurement"
    return "keep_and_repeat" if experiment.variant > experiment.baseline else "revise_and_retest"
