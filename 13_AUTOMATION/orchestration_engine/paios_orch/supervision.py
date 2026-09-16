"""Portable supervision operations (prompt §11-12 / OR-07..OR-11).

Each operation is a portable DESIRED action; whether the runtime can actually
execute it is decided by the Executor adapter (capabilities discovery in
executor.py). Evidence is preserved on failure; recovery never widens scope.
"""

from __future__ import annotations

from .ledger import WorkerLedger, WorkerRecord
from .events import EventLog


class SupervisionError(Exception):
    pass


class Supervisor:
    def __init__(self, ledger: WorkerLedger, executor=None):
        self.ledger = ledger
        self.executor = executor      # optional Executor adapter
        self.events: EventLog = ledger.events

    def inspect(self, worker_id: str) -> dict:
        w = self.ledger.load(worker_id)
        return {
            "worker_id": w.worker_id, "task_id": w.task_id, "state": w.state,
            "stale": w.stale, "requires_reconciliation": w.requires_reconciliation,
            "progress": dict(w.progress), "blockers": list(w.results["blockers"]),
            "errors": list(w.errors), "recovery": dict(w.recovery),
            "children": list(w.children),
        }

    def redirect(self, worker_id: str, bounded_update: dict) -> WorkerRecord:
        """bounded_update may adjust pending actions/summary but never scope,
        authority, or allowed_tools."""
        w = self.ledger.load(worker_id)
        forbidden = {"scope", "authority_scope", "allowed_tools", "task_id",
                     "parent_task_id", "worker_id"}
        if forbidden & set(bounded_update):
            raise SupervisionError(f"redirect may not modify: {sorted(forbidden & set(bounded_update))}")
        w.progress.update({k: v for k, v in bounded_update.items() if k in w.progress})
        self.ledger.save(w)
        self.events.log(worker_id, "WORKER_REDIRECTED", w.state, w.state,
                        reason="bounded redirect", evidence_ref=bounded_update.get("evidence_ref"))
        return w

    def resume(self, worker_id: str, *, reason: str = "") -> WorkerRecord:
        w = self.ledger.load(worker_id)
        if w.state in ("STOPPED", "FAILED", "BLOCKED"):
            w.transition("RUNNING", reason or "resume")
            self.ledger.save(w)
            self.events.log(worker_id, "WORKER_RESUMED", w.state, "RUNNING", reason=reason)
            return self.ledger.load(worker_id)
        if w.state == "RUNNING":
            return w
        raise SupervisionError(f"worker {worker_id} in state {w.state} cannot be resumed")

    def stop(self, worker_id: str, *, reason: str = "") -> WorkerRecord:
        w = self.ledger.load(worker_id)
        w.transition("STOPPED", reason or "stopped by supervisor")
        self.ledger.save(w)
        self.events.log(worker_id, "WORKER_STOPPED", "RUNNING", "STOPPED", reason=reason)
        return self.ledger.load(worker_id)

    def cancel(self, worker_id: str, *, reason: str = "") -> WorkerRecord:
        w = self.ledger.load(worker_id)
        w.transition("CANCELLED", reason or "cancelled by supervisor")
        self.ledger.save(w)
        self.events.log(worker_id, "WORKER_CANCELLED", w.state, "CANCELLED", reason=reason)
        return self.ledger.load(worker_id)

    def replace(self, worker_id: str, *, reason: str = "", **new_worker_kwargs) -> WorkerRecord:
        """Stop the failed worker (preserving its evidence) and create a
        replacement with the SAME bounded contract; never a wider one."""
        old = self.ledger.load(worker_id)
        if old.state not in ("FAILED", "STOPPED", "BLOCKED", "RUNNING"):
            raise SupervisionError(f"cannot replace worker in state {old.state}")
        if old.state in ("RUNNING", "FAILED"):
            old.transition("STOPPED", reason or "replaced")
            self.ledger.save(old)
        new = self.ledger.create(
            task_id=old.task_id, parent_task_id=old.parent_task_id, role=old.role,
            runtime=new_worker_kwargs.get("runtime", old.runtime),
            model_provider=new_worker_kwargs.get("model_provider", old.model_provider),
            objective=old.objective, scope=old.scope,
            authority_scope=old.authority_scope,
            allowed_tools=old.allowed_tools, constraints=old.constraints,
            acceptance_criteria=old.acceptance_criteria,
            context_package=old.context_package, parent_worker_id=old.parent_worker_id)
        # link replacement lineage; prior evidence preserved on the old record
        old.progress["summary"] = (old.progress.get("summary") or "") + \
            f" [replaced by {new.worker_id}; evidence preserved]"
        self.ledger.save(old)
        if old.parent_worker_id:
            self.ledger.add_child(old.parent_worker_id, new.worker_id)
        self.events.log(worker_id, "WORKER_REPLACED", old.state, old.state,
                        reason=reason, evidence_ref=new.worker_id)
        return new

    # -- recovery (prompt §12) ------------------------------------------------
    def recover(self, worker_id: str, *, strategy: str, reason: str = "") -> dict:
        """strategy: retry | resume | redirect | replace | stop.
        Never widens scope/authority; failure evidence is never discarded."""
        w = self.ledger.load(worker_id)
        if w.state != "FAILED" and strategy != "stop":
            raise SupervisionError(f"recover() expects FAILED worker, got {w.state}")
        failure_evidence = list(w.errors)
        w.recovery["attempts"] += 1
        w.recovery["last_action"] = strategy
        w.recovery["next_action"] = None
        self.ledger.save(w)

        if strategy == "retry" or strategy == "resume":
            resumed = self.resume(worker_id, reason=reason or "recovery retry")
            self.events.log(worker_id, "RECOVERY_ATTEMPTED", "FAILED", "RUNNING",
                            reason=reason, extra={"strategy": strategy,
                                                  "failure_evidence_preserved": bool(failure_evidence)})
            return {"action": strategy, "worker": resumed}
        if strategy == "redirect":
            redirectee = self.redirect(worker_id, {"pending": w.progress.get("pending", []),
                                                   "summary": reason or "redirected recovery"})
            self.events.log(worker_id, "RECOVERY_ATTEMPTED", "FAILED", "FAILED",
                            reason=reason, extra={"strategy": "redirect"})
            return {"action": "redirect", "worker": redirectee}
        if strategy == "replace":
            new = self.replace(worker_id, reason=reason or "recovery replacement")
            return {"action": "replace", "worker": new}
        if strategy == "stop":
            stopped = self.stop(worker_id, reason=reason or "recovery stop")
            return {"action": "stop", "worker": stopped}
        raise SupervisionError(f"unknown recovery strategy: {strategy}")
