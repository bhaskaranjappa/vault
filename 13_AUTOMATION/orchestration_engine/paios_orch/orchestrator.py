"""Orchestrator facade (prompt §5-16).

Wires ledger + dispatcher + supervisor + acceptor + optional Phase 8 context
and checkpoint integration into one portable entrypoint. Also handles restart
reconciliation (stale RUNNING workers) per OR-16.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .ledger import WorkerLedger, WorkerRecord
from .tasks import TaskContract, validate_task_contract
from .deps import DependencyGraph
from .dispatcher import Dispatcher, DispatchDecision
from .supervision import Supervisor
from .acceptance import ParentAcceptor, AcceptanceResult
from .delegation import delegate as make_delegation, Delegation
from .events import EventLog


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Orchestrator:
    def __init__(self, state_root: str | Path, executor=None, checkpoint_store=None):
        self.root = Path(state_root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.ledger = WorkerLedger(self.root / "workers")
        self.deps = DependencyGraph()
        self.dispatcher = Dispatcher(self.deps)
        self.supervisor = Supervisor(self.ledger, executor)
        self.acceptor = ParentAcceptor(self.ledger)
        self.executor = executor
        self.checkpoint_store = checkpoint_store   # optional Phase 8 CheckpointStore
        self._tasks_path = self.root / "tasks.json"

    # -- task registry (durable) ----------------------------------------------
    def register_task(self, task: TaskContract) -> list:
        defects = validate_task_contract(task)
        if defects:
            raise ValueError(f"invalid task contract: {defects}")
        tasks = self._load_tasks()
        tasks[task.task_id] = task.to_dict()
        self._save_tasks(tasks)
        return defects

    def get_task(self, task_id: str) -> TaskContract:
        return TaskContract.from_dict(self._load_tasks()[task_id])

    def _load_tasks(self) -> dict:
        if self._tasks_path.exists():
            return json.loads(self._tasks_path.read_text(encoding="utf-8"))
        return {}

    def _save_tasks(self, tasks: dict) -> None:
        self._tasks_path.write_text(json.dumps(tasks, indent=2, ensure_ascii=False),
                                    encoding="utf-8")

    # -- task creation ----------------------------------------------------------
    def create_task(self, *, parent_task_id: Optional[str] = None, objective: str,
                    scope: str, allowed_tools: list, authority_scope: str,
                    constraints: list, acceptance_criteria: list,
                    expected_output: str, evidence_requirements: list,
                    inputs: list | None = None,
                    context_package: Optional[str] = None) -> TaskContract:
        task = TaskContract(
            task_id=TaskContract.new_id(), parent_task_id=parent_task_id,
            objective=objective, scope=scope, inputs=list(inputs or []),
            allowed_tools=list(allowed_tools), authority_scope=authority_scope,
            constraints=list(constraints), acceptance_criteria=list(acceptance_criteria),
            expected_output=expected_output,
            evidence_requirements=list(evidence_requirements),
            context_package=context_package, created_at=_now())
        self.register_task(task)
        return task

    # -- worker spawn -------------------------------------------------------------
    def spawn_worker(self, task_id: str, *, role: str = "worker", runtime: str = "portable",
                     model_provider: str = "unknown",
                     parent_worker_id: Optional[str] = None) -> WorkerRecord:
        task = self.get_task(task_id)
        w = self.ledger.create(
            task_id=task_id, parent_task_id=task.parent_task_id, role=role,
            runtime=runtime, model_provider=model_provider, objective=task.objective,
            scope=task.scope, authority_scope=task.authority_scope,
            allowed_tools=task.allowed_tools, constraints=task.constraints,
            acceptance_criteria=task.acceptance_criteria,
            context_package=task.context_package, parent_worker_id=parent_worker_id)
        if parent_worker_id:
            self.ledger.add_child(parent_worker_id, w.worker_id)
        return w

    # -- delegation ----------------------------------------------------------------
    def delegate(self, parent_task_id: str, *, objective: str, scope: str,
                 allowed_tools: list, authority_scope: str, constraints: list,
                 acceptance_criteria: list, evidence_requirements: list,
                 context_package: Optional[str] = None,
                 parent_worker_id: Optional[str] = None) -> Delegation:
        parent = self.get_task(parent_task_id)
        dlg = make_delegation(
            parent, objective=objective, scope=scope, allowed_tools=allowed_tools,
            authority_scope=authority_scope, constraints=constraints,
            acceptance_criteria=acceptance_criteria,
            evidence_requirements=evidence_requirements,
            context_package=context_package, parent_worker_id=parent_worker_id)
        # persist child task contract
        child_task = TaskContract(
            task_id=dlg.child_task_id, parent_task_id=parent.task_id,
            objective=objective, scope=scope, inputs=[], allowed_tools=list(allowed_tools),
            authority_scope=authority_scope, constraints=list(constraints),
            acceptance_criteria=list(acceptance_criteria), expected_output=objective,
            evidence_requirements=list(evidence_requirements),
            context_package=context_package, created_at=_now())
        self.register_task(child_task)
        if parent_worker_id:
            dlg.child_worker_id = None      # assigned when the child worker spawns
        return dlg

    def spawn_delegated_worker(self, dlg: Delegation, *, role: str = "worker",
                               runtime: str = "portable",
                               model_provider: str = "unknown",
                               parent_worker_id: Optional[str] = None) -> WorkerRecord:
        task = self.get_task(dlg.child_task_id)
        w = self.ledger.create(
            task_id=task.task_id, parent_task_id=task.parent_task_id, role=role,
            runtime=runtime, model_provider=model_provider, objective=task.objective,
            scope=task.scope, authority_scope=task.authority_scope,
            allowed_tools=task.allowed_tools, constraints=task.constraints,
            acceptance_criteria=task.acceptance_criteria,
            context_package=task.context_package, parent_worker_id=parent_worker_id)
        if parent_worker_id:
            self.ledger.add_child(parent_worker_id, w.worker_id)
        return w

    # -- lifecycle helpers -----------------------------------------------------------
    def start(self, worker_id: str, *, reason: str = "start") -> WorkerRecord:
        w = self.ledger.transition(worker_id, "RUNNING", reason=reason)
        if self.executor and self.executor.supports("start_worker"):
            pkg = None
            if w.context_package:
                try:
                    from paios_memory.context import load_context_package
                    pkg = load_context_package(self._memory_root(), w.context_package)
                except Exception:
                    pkg = None
            self.executor.start_worker(worker_id, pkg)
        return w

    def complete(self, worker_id: str, *, output_ref: str | None = None,
                 evidence_refs: list | None = None, reason: str = "acceptance passed") -> WorkerRecord:
        """COMPLETE requires an explicit acceptance-style check by the caller;
        this method only records it and never fires from a bare stop."""
        w = self.ledger.load(worker_id)
        w.results["output_ref"] = output_ref or w.results["output_ref"]
        w.results["evidence_refs"] = list(evidence_refs or w.results["evidence_refs"])
        self.ledger.save(w)
        return self.ledger.transition(worker_id, "COMPLETE", reason=reason,
                                      evidence_ref=output_ref)

    def fail(self, worker_id: str, *, error_type: str, message: str) -> WorkerRecord:
        w = self.ledger.load(worker_id)
        w.errors.append({"time": _now(), "type": error_type, "message": message,
                         "recovered": False})
        self.ledger.save(w)
        return self.ledger.transition(worker_id, "FAILED", reason=message)

    def block(self, worker_id: str, *, blocker: str) -> WorkerRecord:
        w = self.ledger.load(worker_id)
        if blocker not in w.results["blockers"]:
            w.results["blockers"].append(blocker)
        self.ledger.save(w)
        return self.ledger.transition(worker_id, "BLOCKED", reason=blocker)

    # -- restart reconciliation ---------------------------------------------------
    def reconcile_after_restart(self) -> list:
        return self.ledger.reconcile_on_restart()

    # -- checkpoint integration (prompt §15) ---------------------------------------
    def write_checkpoint(self, task_id: str, *, phase: str = "orchestration",
                         evidence_refs: list | None = None) -> Optional[str]:
        if self.checkpoint_store is None:
            return None
        from paios_memory.checkpoint import Checkpoint
        task = self.get_task(task_id)
        workers = [
            {"worker_id": w.worker_id, "role": w.role, "state": w.state,
             "result_ref": w.results.get("output_ref")}
            for w in self.ledger.all_workers() if w.task_id == task_id
        ]
        incomplete = [w for w in self.ledger.all_workers()
                      if w.task_id == task_id and w.state not in ("COMPLETE", "CANCELLED")]
        chk = Checkpoint(
            task_id=task_id, objective=task.objective, scope=task.scope,
            acceptance_criteria=list(task.acceptance_criteria),
            completed=[{"action": w.progress.get("summary") or w.worker_id,
                        "status": w.state,
                        "evidence": list(w.results.get("evidence_refs", []))}
                       for w in self.ledger.all_workers() if w.task_id == task_id
                       and w.state in ("COMPLETE", "CANCELLED")],
            current_state={"phase": phase,
                           "active_action": incomplete[0].progress.get("active") if incomplete else None,
                           "observations": []},
            blockers=[b for w in incomplete for b in w.results.get("blockers", [])],
            next_actions=[f"reconcile worker {w.worker_id} ({w.state})" for w in incomplete],
            context_package=task.context_package,
            authority_scope=task.authority_scope, workers=workers,
            evidence_refs=list(evidence_refs or []))
        chk = self.checkpoint_store.create_checkpoint(chk)
        return chk.checkpoint_id

    def _memory_root(self) -> str:
        return str(self.root.parent / "memory_root")
