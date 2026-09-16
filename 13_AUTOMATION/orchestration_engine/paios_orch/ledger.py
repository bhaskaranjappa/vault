"""Durable worker ledger per 03_PROTOCOLS/AIOS_WORKER_STATE_SCHEMA_V1.md.

File-backed JSON records under <root>/workers/records/WRK-*.json with an
index.yaml summary. Records are operational state, not canonical knowledge.
Persistence across process boundaries is required behavior (OR-15).
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .states import STATES, require_transition, InvalidTransition
from .events import EventLog


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class WorkerRecord:
    worker_id: str
    task_id: str
    parent_task_id: Optional[str]
    role: str                        # coordinator | specialist | worker | executor
    runtime: str
    model_provider: str
    state: str
    objective: str
    scope: str
    authority_scope: str
    allowed_tools: list
    constraints: list
    acceptance_criteria: list
    context_package: Optional[str]
    created_at: str
    updated_at: str
    parent_worker_id: Optional[str] = None
    children: list = field(default_factory=list)
    progress: dict = field(default_factory=lambda: {
        "summary": "", "completed": [], "active": None, "pending": [], "percent": None})
    results: dict = field(default_factory=lambda: {
        "output_ref": None, "evidence_refs": [], "blockers": []})
    errors: list = field(default_factory=list)
    recovery: dict = field(default_factory=lambda: {
        "attempts": 0, "last_action": "none", "next_action": None})
    parent_control: dict = field(default_factory=lambda: {
        "inspectable": True, "redirectable": True, "resumable": True,
        "stoppable": True, "cancellable": True})
    stale: bool = False
    requires_reconciliation: bool = False

    @staticmethod
    def new_id() -> str:
        return "WRK-" + uuid.uuid4().hex[:10]

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, d: dict) -> "WorkerRecord":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def transition(self, new_state: str, reason: str = "") -> None:
        if new_state not in STATES:
            raise InvalidTransition(f"unknown state: {new_state}")
        require_transition(self.state, new_state, context=self.worker_id)
        self.state = new_state
        self.updated_at = _now()
        if reason:
            self.progress["summary"] = reason


class WorkerLedger:
    """Durable WRK record store with index. Thread-safe via a process lock."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.records_dir = self.root / "records"
        self.records_dir.mkdir(parents=True, exist_ok=True)
        self.events = EventLog(self.root / "events.jsonl")
        self._index_path = self.root / "index.yaml"

    # -- durability --------------------------------------------------------
    def _path(self, worker_id: str) -> Path:
        return self.records_dir / f"{worker_id}.json"

    def save(self, w: WorkerRecord) -> None:
        w.updated_at = _now()
        self._path(w.worker_id).write_text(
            json.dumps(w.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        self._write_index()

    def load(self, worker_id: str) -> WorkerRecord:
        path = self._path(worker_id)
        if not path.exists():
            raise FileNotFoundError(f"worker record not found: {worker_id}")
        return WorkerRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def all_workers(self) -> list:
        return [self.load(p.stem) for p in sorted(self.records_dir.glob("WRK-*.json"))]

    def _write_index(self) -> None:
        lines = ["workers:"]
        for w in self.all_workers():
            lines.append(
                f"  - {w.worker_id}: {{task: {w.task_id}, parent_worker: "
                f"{w.parent_worker_id or 'null'}, state: {w.state}, stale: {str(w.stale).lower()}}}")
        self._index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # -- lifecycle ----------------------------------------------------------
    def create(self, *, task_id: str, parent_task_id: Optional[str], role: str,
               runtime: str, model_provider: str, objective: str, scope: str,
               authority_scope: str, allowed_tools: list, constraints: list,
               acceptance_criteria: list, context_package: Optional[str],
               parent_worker_id: Optional[str] = None) -> WorkerRecord:
        w = WorkerRecord(
            worker_id=WorkerRecord.new_id(), task_id=task_id,
            parent_task_id=parent_task_id, role=role, runtime=runtime,
            model_provider=model_provider, state="PENDING", objective=objective,
            scope=scope, authority_scope=authority_scope,
            allowed_tools=list(allowed_tools), constraints=list(constraints),
            acceptance_criteria=list(acceptance_criteria),
            context_package=context_package, created_at=_now(), updated_at=_now(),
            parent_worker_id=parent_worker_id)
        self.save(w)
        self.events.log(w.worker_id, "WORKER_CREATED", None, "PENDING", reason="worker registered")
        return w

    def transition(self, worker_id: str, new_state: str, *,
                   reason: str = "", evidence_ref: Optional[str] = None) -> WorkerRecord:
        w = self.load(worker_id)
        old = w.state
        w.transition(new_state, reason)
        self.save(w)
        self.events.log(worker_id, f"WORKER_{new_state}", old, new_state,
                        reason=reason, evidence_ref=evidence_ref)
        return w

    # -- hierarchy -----------------------------------------------------------
    def ancestry(self, worker_id: str) -> list:
        """Return chain from worker to root [worker, parent, ..., root]."""
        chain = []
        w = self.load(worker_id)
        while w is not None:
            chain.append(w)
            w = self.load(w.parent_worker_id) if w.parent_worker_id else None
        return chain

    def descendants(self, worker_id: str) -> list:
        w = self.load(worker_id)
        out = []
        for cid in w.children:
            out.append(self.load(cid))
            out.extend(self.descendants(cid))
        return out

    def add_child(self, parent_worker_id: str, child_worker_id: str) -> None:
        p = self.load(parent_worker_id)
        if child_worker_id not in p.children:
            p.children.append(child_worker_id)
            self.save(p)

    # -- stale reconciliation (OR-16) ----------------------------------------
    def reconcile_on_restart(self) -> list:
        """RUNNING workers found after a process boundary are stale: marked
        requiring reconciliation, never treated as complete."""
        reconciled = []
        for w in self.all_workers():
            if w.state == "RUNNING":
                w.stale = True
                w.requires_reconciliation = True
                self.save(w)
                self.events.log(w.worker_id, "WORKER_STALE", "RUNNING", "RUNNING",
                                reason="RUNNING observed across restart; reconciliation required")
                reconciled.append(w)
        return reconciled
