"""Reasoning-effort routing: LOW / MEDIUM / HIGH / MAXIMUM."""

from __future__ import annotations

from .capabilities import REASONING_LEVELS, REASONING_RANK

# Task-complexity classes map to reasoning effort. This is a policy table,
# not a benchmark: complexity classification is the caller's judgment.
COMPLEXITY_ROUTING = {
    "ROUTINE_TRANSFORMATION": "LOW",
    "ORDINARY_ENGINEERING": "MEDIUM",
    "ORDINARY_RESEARCH": "MEDIUM",
    "COMPLEX_DIAGNOSIS": "HIGH",
    "COMPLEX_DESIGN": "HIGH",
    "HIGH_UNCERTAINTY": "MAXIMUM",
    "NOVEL_HARD_PROBLEM": "MAXIMUM",
}


def route_reasoning(complexity: str, *, uncertainty: str = "NORMAL") -> str:
    """Deterministic reasoning-effort selection.

    Do not force MAXIMUM universally; unusual difficulty or explicit high
    uncertainty escalates one step above the complexity default.
    """
    if complexity not in COMPLEXITY_ROUTING:
        raise ValueError(f"unknown complexity class: {complexity}")
    level = COMPLEXITY_ROUTING[complexity]
    if uncertainty == "HIGH":
        idx = min(REASONING_RANK[level] + 1, REASONING_RANK["MAXIMUM"])
        level = REASONING_LEVELS[idx]
    return level
