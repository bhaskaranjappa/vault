"""Worker/task lifecycle states per 03_PROTOCOLS/AIOS_WORKER_STATE_SCHEMA_V1.md §2-3.

Invalid transitions raise InvalidTransition. COMPLETE requires an explicit
acceptance check — stopping execution can never produce COMPLETE.
"""

from __future__ import annotations


STATES = ("PENDING", "RUNNING", "BLOCKED", "COMPLETE", "FAILED", "CANCELLED", "STOPPED", "UNKNOWN")

TRANSITIONS = {
    "PENDING":   {"RUNNING", "CANCELLED", "BLOCKED"},
    "RUNNING":   {"COMPLETE", "FAILED", "BLOCKED", "CANCELLED", "STOPPED"},
    "BLOCKED":   {"RUNNING", "FAILED", "CANCELLED", "STOPPED"},
    "COMPLETE":  set(),
    "FAILED":    {"RUNNING", "CANCELLED", "STOPPED"},   # retry/resume path
    "CANCELLED": set(),
    "STOPPED":   {"RUNNING", "CANCELLED"},              # resume path
    "UNKNOWN":   {"RUNNING", "FAILED", "CANCELLED", "STOPPED"},  # reconciliation
}


class InvalidTransition(Exception):
    pass


def can_transition(old: str, new: str) -> bool:
    if old not in TRANSITIONS or new not in STATES:
        return False
    return new in TRANSITIONS[old]


def terminal(state: str) -> bool:
    return state in ("COMPLETE", "CANCELLED")


def require_transition(old: str, new: str, *, context: str = "") -> None:
    if not can_transition(old, new):
        raise InvalidTransition(
            f"invalid state transition {old} -> {new}" + (f" ({context})" if context else ""))
