"""Runtime executor/adapter boundary (prompt §17, §21 / OR-19).

The portable engine defines the orchestration contract; a runtime adapter
implements whichever operations the runtime actually supports. Capability
discovery is explicit: SUPPORTED (portable contract) vs RUNTIME_SUPPORTED vs
RUNTIME_UNSUPPORTED. The portable layer never assumes every operation exists.
"""

from __future__ import annotations

from dataclasses import dataclass, field

PORTABLE_OPERATIONS = (
    "start_worker", "resume_worker", "stop_worker", "cancel_worker",
    "send_update", "collect_result", "inspect", "redirect", "replace",
    "nested_delegation", "parallel", "background_execution", "model_routing",
)


@dataclass
class ExecutorCapabilities:
    """runtime_supported maps operation -> bool for THIS runtime."""
    runtime_id: str
    runtime_supported: dict = field(default_factory=dict)

    def classify(self, op: str) -> str:
        """SUPPORTED = portable contract exists; RUNTIME_SUPPORTED /
        RUNTIME_UNSUPPORTED = actual runtime capability."""
        if op not in PORTABLE_OPERATIONS:
            return "UNSUPPORTED"            # not in the portable contract at all
        return "RUNTIME_SUPPORTED" if self.runtime_supported.get(op) else "RUNTIME_UNSUPPORTED"


class Executor:
    """Base adapter. Every operation defaults to unsupported so the portable
    layer fails visibly rather than assuming runtime capability."""

    runtime_id = "abstract"

    def __init__(self):
        self.capabilities = ExecutorCapabilities(
            runtime_id=self.runtime_id,
            runtime_supported={op: False for op in PORTABLE_OPERATIONS})

    def supports(self, op: str) -> bool:
        return self.capabilities.runtime_supported.get(op, False)

    # -- optional operations ---------------------------------------------------
    def start_worker(self, worker_id: str, context_package: dict | None) -> dict:
        raise NotImplementedError(f"{self.runtime_id} does not support start_worker")

    def resume_worker(self, worker_id: str) -> dict:
        raise NotImplementedError(f"{self.runtime_id} does not support resume_worker")

    def stop_worker(self, worker_id: str) -> dict:
        raise NotImplementedError(f"{self.runtime_id} does not support stop_worker")

    def cancel_worker(self, worker_id: str) -> dict:
        raise NotImplementedError(f"{self.runtime_id} does not support cancel_worker")

    def send_update(self, worker_id: str, update: dict) -> dict:
        raise NotImplementedError(f"{self.runtime_id} does not support send_update")

    def collect_result(self, worker_id: str) -> dict:
        raise NotImplementedError(f"{self.runtime_id} does not support collect_result")


class InlineExecutor(Executor):
    """Reference adapter for in-process execution (tests / local work).
    Executes a worker as a plain Python callable; useful for validating the
    portable contract without any agent runtime."""

    runtime_id = "inline"

    def __init__(self, handlers: dict | None = None):
        super().__init__()
        handlers = handlers or {}
        self.handlers = handlers
        for op in ("start_worker", "resume_worker", "stop_worker",
                   "cancel_worker", "send_update", "collect_result"):
            self.capabilities.runtime_supported[op] = op in handlers or op in (
                "start_worker", "resume_worker", "stop_worker", "cancel_worker")

    def start_worker(self, worker_id: str, context_package: dict | None) -> dict:
        fn = self.handlers.get(worker_id)
        if fn is None:
            return {"worker_id": worker_id, "started": True, "result": None}
        return {"worker_id": worker_id, "started": True, "result": fn(context_package)}

    def resume_worker(self, worker_id: str) -> dict:
        return {"worker_id": worker_id, "resumed": True}

    def stop_worker(self, worker_id: str) -> dict:
        return {"worker_id": worker_id, "stopped": True}

    def cancel_worker(self, worker_id: str) -> dict:
        return {"worker_id": worker_id, "cancelled": True}

    def collect_result(self, worker_id: str) -> dict:
        return {"worker_id": worker_id, "result_ref": None}
