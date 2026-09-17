"""Runtime adapter boundary (Protocol §2) + deterministic reference adapters (§14).

The reference adapter is intentionally side-effect-free and exists for
testing only. It is NOT a production runtime and must never be described
as one.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from .execution import ExecutionRequest, ExecutionResult, ExecutionStatus


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class RuntimeHealth:
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class RuntimeAdapter:
    """Vendor-neutral adapter contract. Concrete runtimes subclass this and
    must declare capabilities honestly; cancellation is runtime-dependent."""

    runtime_id: str = "abstract"
    adapter_id: str = "abstract-adapter"
    adapter_version: str = "0.0.0"
    #: capability names this adapter actually provides (Protocol §2)
    provided_capabilities: frozenset = frozenset()

    def health(self) -> str:
        return RuntimeHealth.UNKNOWN

    def capabilities(self) -> frozenset:
        return self.provided_capabilities

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        raise NotImplementedError

    def verify(self, result: ExecutionResult) -> dict:
        return {"verified": False, "reason": "adapter does not implement verification"}

    def cancel(self, execution_id: str) -> bool:
        raise NotImplementedError("cancellation is runtime-dependent and not "
                                  "supported by this adapter")

    # -- shared result construction ----------------------------------------
    def _result(self, request: ExecutionRequest, status: str, **kw) -> ExecutionResult:
        return ExecutionResult(
            execution_id=ExecutionResult.new_execution_id(),
            runtime_id=self.runtime_id, adapter_id=self.adapter_id,
            request_fingerprint=request.fingerprint(), status=status,
            started_at=kw.pop("started_at", _now()), ended_at=kw.pop("ended_at", _now()),
            **kw)


class ReferenceRuntimeAdapter(RuntimeAdapter):
    """Deterministic, side-effect-free reference runtime for tests (Protocol
    §14). Behavior is driven entirely by the request inputs:
      - inputs["behavior"] in {"ok", "fail", "unknown", "timeout", "mismatch"}
    It generates evidence but performs no external action whatsoever."""

    runtime_id = "reference-local"
    adapter_id = "reference-local-adapter"
    adapter_version = "1.0.0"
    provided_capabilities = frozenset({"execute", "verify", "structured_output",
                                       "evidence_generation"})

    def health(self) -> str:
        return RuntimeHealth.AVAILABLE

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        behavior = request.inputs.get("behavior", "ok")
        if behavior == "fail":
            return self._result(request, ExecutionStatus.FAILED,
                                error_type="deterministic_failure",
                                error="reference adapter: deterministic failure requested")
        if behavior == "unknown":
            return self._result(request, ExecutionStatus.UNKNOWN,
                                error_type="ambiguous_outcome",
                                error="reference adapter: outcome recorded as UNKNOWN")
        if behavior == "timeout":
            return self._result(request, ExecutionStatus.TIMEOUT,
                                error_type="deadline_exceeded",
                                error="reference adapter: deadline exceeded (simulated)")
        if behavior == "mismatch":
            return self._result(request, ExecutionStatus.FAILED,
                                error_type="capability_mismatch",
                                error="reference adapter: capability mismatch requested")
        evidence = [f"reference://{request.task_id}/evidence"]
        return self._result(request, ExecutionStatus.COMPLETED,
                            output_ref=f"reference://{request.task_id}/output",
                            evidence_refs=evidence)

    def verify(self, result: ExecutionResult) -> dict:
        if result.status == ExecutionStatus.COMPLETED and result.output_ref:
            return {"verified": True, "adapter": self.adapter_id,
                    "fingerprint_match": True}
        return {"verified": False, "reason": f"status {result.status} is not verifiable as success"}


class RuntimeUnavailableAdapter(RuntimeAdapter):
    """Adapter whose runtime reports UNAVAILABLE (for failover tests)."""
    runtime_id = "reference-unavailable"
    adapter_id = "reference-unavailable-adapter"
    provided_capabilities = frozenset({"execute"})

    def health(self) -> str:
        return RuntimeHealth.UNAVAILABLE

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        return self._result(request, ExecutionStatus.FAILED,
                            error_type="runtime_unavailable",
                            error="runtime reports UNAVAILABLE")


class TimingOutAdapter(RuntimeAdapter):
    """Adapter that always reports TIMEOUT (deadline enforcement tests)."""
    runtime_id = "reference-timeout"
    adapter_id = "reference-timeout-adapter"
    provided_capabilities = frozenset({"execute"})

    def health(self) -> str:
        return RuntimeHealth.DEGRADED

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        return self._result(request, ExecutionStatus.TIMEOUT,
                            error_type="deadline_exceeded",
                            error="adapter exceeded its deadline")


class UnknownResultAdapter(RuntimeAdapter):
    """Adapter whose execution outcome is genuinely ambiguous."""
    runtime_id = "reference-unknown"
    adapter_id = "reference-unknown-adapter"
    provided_capabilities = frozenset({"execute"})

    def health(self) -> str:
        return RuntimeHealth.AVAILABLE

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        return self._result(request, ExecutionStatus.UNKNOWN,
                            error_type="ambiguous_outcome",
                            error="delivery receipt not received (simulated)")
