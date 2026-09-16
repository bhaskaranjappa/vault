"""Portable dispatcher (prompt §16 / OR-19).

Dispatch policy decides: EXECUTE | DELEGATE | PARALLELIZE | WAIT_DEPENDENCY |
RETRY | REDIRECT | REPLACE | STOP. Execution is NOT performed here — the
policy returns a decision that a runtime adapter (Executor) carries out.
"""

from __future__ import annotations

from dataclasses import dataclass

from .deps import DependencyGraph
from .states import terminal


@dataclass
class DispatchDecision:
    action: str                 # EXECUTE | DELEGATE | PARALLELIZE | WAIT_DEPENDENCY | RETRY | REDIRECT | REPLACE | STOP
    task_id: str | None = None
    worker_id: str | None = None
    reason: str = ""


class Dispatcher:
    def __init__(self, deps: DependencyGraph | None = None):
        self.deps = deps or DependencyGraph()

    def decide_task(self, task_id: str, task_states: dict, *, ready: str | None = None) -> DispatchDecision:
        """Task-level decision before any worker exists."""
        state = task_states.get(task_id, "PENDING")
        if terminal(state):
            return DispatchDecision("STOP", task_id=task_id, reason=f"task already {state}")
        readiness = ready or self.deps.readiness(task_id, task_states)
        if readiness == "POISONED":
            return DispatchDecision("STOP", task_id=task_id,
                                    reason=self.deps.blocker_for(task_id, task_states))
        if readiness == "BLOCKED":
            return DispatchDecision("WAIT_DEPENDENCY", task_id=task_id,
                                    reason=self.deps.blocker_for(task_id, task_states))
        return DispatchDecision("EXECUTE", task_id=task_id, reason="dependencies satisfied")

    def decide_worker(self, worker) -> DispatchDecision:
        """Worker-level decision based on current record state."""
        s = worker.state
        if s == "PENDING":
            return DispatchDecision("EXECUTE", worker_id=worker.worker_id, reason="worker pending start")
        if s == "RUNNING":
            if worker.stale or worker.requires_reconciliation:
                return DispatchDecision("REDIRECT", worker_id=worker.worker_id,
                                        reason="stale RUNNING state requires reconciliation")
            return DispatchDecision("EXECUTE", worker_id=worker.worker_id, reason="already running")
        if s == "BLOCKED":
            return DispatchDecision("WAIT_DEPENDENCY", worker_id=worker.worker_id,
                                    reason="; ".join(worker.results.get("blockers", [])) or "blocked")
        if s == "FAILED":
            if worker.recovery.get("attempts", 0) >= 3:
                return DispatchDecision("REPLACE", worker_id=worker.worker_id,
                                        reason="max recovery attempts exceeded")
            return DispatchDecision("RETRY", worker_id=worker.worker_id,
                                    reason="recoverable failure with concrete recovery path")
        if s in ("STOPPED", "CANCELLED"):
            return DispatchDecision("STOP", worker_id=worker.worker_id, reason=f"worker {s}")
        if s == "COMPLETE":
            return DispatchDecision("STOP", worker_id=worker.worker_id, reason="worker complete")
        return DispatchDecision("STOP", worker_id=worker.worker_id, reason=f"unknown state {s}")
