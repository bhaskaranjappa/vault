"""Task contract per the Phase 9 task model (prompt §4 / OR-01).

Task identity is a stable UUID-based id and never changes through resume or
recovery. A task contract is immutable once created; progress lives on the
worker record, not the contract.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

REQUIRED_FIELDS = (
    "task_id", "objective", "scope", "authority_scope",
    "acceptance_criteria", "expected_output",
)


@dataclass(frozen=True)
class TaskContract:
    task_id: str
    parent_task_id: Optional[str]
    objective: str
    scope: str
    inputs: list                      # context/input references
    allowed_tools: list
    authority_scope: str
    constraints: list
    acceptance_criteria: list
    expected_output: str
    evidence_requirements: list
    context_package: Optional[str]    # CTX-<id> reference; built via Phase 8 builder
    created_at: str

    @staticmethod
    def new_id() -> str:
        return "TASK-" + uuid.uuid4().hex[:10]

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, d: dict) -> "TaskContract":
        return cls(**d)


def validate_task_contract(t: TaskContract) -> list:
    """Return list of contract defects (empty = valid)."""
    defects = []
    if not t.task_id or not t.task_id.startswith("TASK-"):
        defects.append("task_id must be a stable TASK-<id>")
    if not t.objective:
        defects.append("objective is required")
    if not t.scope:
        defects.append("scope is required")
    if not t.authority_scope:
        defects.append("authority_scope is required")
    if not t.acceptance_criteria:
        defects.append("acceptance_criteria must be non-empty")
    if not t.expected_output:
        defects.append("expected_output is required")
    return defects
