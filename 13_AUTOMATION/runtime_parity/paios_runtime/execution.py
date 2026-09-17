"""Runtime-agnostic execution contract (Protocol §4).

ExecutionRequest/ExecutionResult preserve task identity, authority, context,
route, acceptance, deadline, retry, idempotency and evidence across runtimes.
Status semantics: UNKNOWN is ambiguous, TIMEOUT is a distinct failure, an
adapter error is never success.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from typing import Optional


class ExecutionStatus:
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    TIMEOUT = "TIMEOUT"
    ALL = (PENDING, RUNNING, COMPLETED, FAILED, UNKNOWN, TIMEOUT)


@dataclass
class ExecutionRequest:
    task_id: str
    objective: str
    authority_context: str                       # effective scope string; never derived from runtime
    context_package_id: Optional[str] = None
    model_route_ref: Optional[str] = None        # Phase 10 decision reference
    tool_route_ref: Optional[str] = None
    acceptance_criteria: list = field(default_factory=list)
    deadline: Optional[str] = None               # ISO-8601
    retry_policy: str = "record_and_stop"        # record_and_stop | retry_bounded
    retry_limit: int = 0
    idempotency_token: Optional[str] = None
    evidence_requirements: list = field(default_factory=list)
    inputs: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.task_id or not self.objective:
            raise ValueError("execution request requires task_id and objective")
        if not self.authority_context:
            raise ValueError("execution request requires an authority context")

    def fingerprint(self) -> str:
        """Deterministic request fingerprint for cross-runtime evidence."""
        payload = json.dumps({
            "task_id": self.task_id, "objective": self.objective,
            "authority_context": self.authority_context,
            "context_package_id": self.context_package_id,
            "model_route_ref": self.model_route_ref,
            "acceptance_criteria": self.acceptance_criteria,
            "idempotency_token": self.idempotency_token,
            "inputs": self.inputs,
        }, sort_keys=True, ensure_ascii=False)
        return "FP-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass
class ExecutionResult:
    execution_id: str
    runtime_id: str
    adapter_id: str
    request_fingerprint: str
    status: str
    started_at: str
    ended_at: Optional[str] = None
    output_ref: Optional[str] = None
    evidence_refs: list = field(default_factory=list)
    error: Optional[str] = None
    error_type: Optional[str] = None
    verification: Optional[dict] = None
    substitutions: list = field(default_factory=list)   # substitution record ids

    def __post_init__(self):
        if self.status not in ExecutionStatus.ALL:
            raise ValueError(f"invalid execution status: {self.status}")

    @staticmethod
    def new_execution_id() -> str:
        return "EXE-" + uuid.uuid4().hex[:12]

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, d: dict) -> "ExecutionResult":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
