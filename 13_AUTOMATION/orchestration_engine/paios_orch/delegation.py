"""Bounded delegation per 03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md (prompt §7-8).

Core invariant: effective child scope/authority must never exceed parent
effective scope. Child output can never redefine authority. Scope escalation
and self-granted authority are rejected at delegation time.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from .tasks import TaskContract

SCOPE_ESCALATION_REJECTED = "SCOPE_ESCALATION_REJECTED"
AUTHORITY_ESCALATION_REJECTED = "AUTHORITY_ESCALATION_REJECTED"


@dataclass
class Delegation:
    delegation_id: str
    parent_task_id: str
    child_task_id: str
    parent_worker_id: Optional[str]
    child_worker_id: Optional[str]
    objective: str
    scope: str
    allowed_tools: list
    authority_scope: str
    constraints: list
    context_package: Optional[str]
    acceptance_criteria: list
    evidence_requirements: list
    created_at: str

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, d: dict) -> "Delegation":
        return cls(**d)


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def scope_contains(parent_scope: str, child_scope: str) -> bool:
    """Conservative containment check: a child scope is within the parent scope
    when the child does not claim capabilities the parent scope forbids.

    Parent scope format: comma/semicolon-separated terms, optionally with
    'not <term>' prohibitions. Child scope must not introduce a positive term
    the parent prohibits, and must not add positive terms absent from a
    non-empty parent allow-list when the parent uses restrictive phrasing.
    Free-form scopes are treated as compatible only when no prohibition is
    violated (fail-visible rather than silently permissive).
    """
    import re

    def terms(scope: str) -> tuple:
        pos, neg = set(), set()
        for raw in re.split(r"[;,]", scope or ""):
            t = raw.strip().lower()
            if not t:
                continue
            m = re.match(r"(?:not|no|except|without)\s+(.*)", t)
            if m:
                neg.add(m.group(1).strip())
            else:
                pos.add(t)
        return pos, neg

    p_pos, p_neg = terms(parent_scope)
    c_pos, c_neg = terms(child_scope)
    # child may not do anything the parent prohibits
    if c_pos & p_neg:
        return False
    # if parent declares an explicit allow-list, child positives must be inside it
    if p_pos and not c_pos.issubset(p_pos):
        return False
    return True


def delegate(parent: TaskContract, *, objective: str, scope: str,
             allowed_tools: list, authority_scope: str, constraints: list,
             acceptance_criteria: list, evidence_requirements: list,
             context_package: Optional[str] = None,
             parent_worker_id: Optional[str] = None) -> Delegation:
    """Create a bounded child delegation. Raises on escalation attempts."""
    if not scope_contains(parent.scope, scope):
        raise PermissionError(SCOPE_ESCALATION_REJECTED)
    if not scope_contains(parent.authority_scope, authority_scope):
        raise PermissionError(AUTHORITY_ESCALATION_REJECTED)

    child = TaskContract(
        task_id=TaskContract.new_id(), parent_task_id=parent.task_id,
        objective=objective, scope=scope, inputs=[], allowed_tools=list(allowed_tools),
        authority_scope=authority_scope, constraints=list(constraints),
        acceptance_criteria=list(acceptance_criteria),
        expected_output=objective, evidence_requirements=list(evidence_requirements),
        context_package=context_package, created_at=_now())
    return Delegation(
        delegation_id="DLG-" + uuid.uuid4().hex[:10],
        parent_task_id=parent.task_id, child_task_id=child.task_id,
        parent_worker_id=parent_worker_id, child_worker_id=None,
        objective=objective, scope=scope, allowed_tools=list(allowed_tools),
        authority_scope=authority_scope, constraints=list(constraints),
        context_package=context_package, acceptance_criteria=list(acceptance_criteria),
        evidence_requirements=list(evidence_requirements), created_at=_now())
