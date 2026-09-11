"""Hamed AGI-like cognitive runtime foundation.

This package provides goal decomposition, deliberation, self-critique,
learning records, and gated execution primitives around the existing Hamed
agent ecosystem. It does not claim to be AGI; it is an extensible autonomy
layer.
"""

from .cognitive_runtime import CognitiveRuntime, Goal, PlanStep, Decision, LearningRecord

__all__ = ["CognitiveRuntime", "Goal", "PlanStep", "Decision", "LearningRecord"]
