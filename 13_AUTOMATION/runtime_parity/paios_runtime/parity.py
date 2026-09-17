"""Parity semantics enforcement (Protocol §7) and runtime registry (§2).

The enforcer checks that semantics which MUST be invariant across runtimes
are actually preserved in an execution result chain. Runtime-specific
differences are represented explicitly via capability records, never
silently normalized.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .capabilities import CapabilityRegistry
from .execution import ExecutionRequest, ExecutionResult, ExecutionStatus
from .untrusted import inspect_runtime_output

#: Semantics that must remain invariant across runtimes.
INVARIANTS = (
    "authority", "acceptance", "idempotency", "evidence", "failure",
    "unknown", "untrusted_content", "task_identity", "context_inheritance",
    "routing_contract",
)


class ParityViolation(Exception):
    pass


@dataclass
class ParityCheck:
    request: ExecutionRequest
    result: ExecutionResult
    violations: list = field(default_factory=list)

    @property
    def consistent(self) -> bool:
        return not self.violations


class ParityEnforcer:
    """Validates an execution against the invariants. The check is performed
    by the portable layer — runtimes cannot opt out."""

    def check(self, request: ExecutionRequest, result: ExecutionResult) -> ParityCheck:
        violations = []
        # task identity preserved (fingerprint is derived from identity fields)
        if result.request_fingerprint != request.fingerprint():
            violations.append("task_identity: request fingerprint mismatch")
        # failure semantics: an adapter error must never be COMPLETED
        if result.status == ExecutionStatus.COMPLETED and result.error:
            violations.append("failure: COMPLETED result carries an error")
        if result.status == ExecutionStatus.TIMEOUT and result.output_ref:
            violations.append("failure: TIMEOUT result claims output")
        # authority semantics: result cannot alter the authority context
        payload = result.to_dict()
        if "authority" in str(payload.get("output_ref", "")).lower() and \
                "grant" in str(payload.get("output_ref", "")).lower():
            violations.append("authority: output attempts to exercise authority")
        # untrusted-content boundary: runtime output inspected as data
        try:
            inspect_runtime_output(str(result.output_ref or ""))
        except Exception as exc:
            violations.append(f"untrusted_content: {exc}")
        # evidence semantics: COMPLETED results must carry evidence
        if result.status == ExecutionStatus.COMPLETED and not result.evidence_refs:
            violations.append("evidence: COMPLETED without evidence refs")
        return ParityCheck(request=request, result=result, violations=violations)


class RuntimeRegistry:
    """Durable registry of runtime adapters by id, with health and lookup."""

    def __init__(self, capabilities: CapabilityRegistry):
        self.capabilities = capabilities
        self._adapters: dict = {}

    def register(self, adapter: RuntimeAdapter) -> None:
        self._adapters[adapter.runtime_id] = adapter

    def get(self, runtime_id: str) -> RuntimeAdapter | None:
        return self._adapters.get(runtime_id)

    def select(self, request: ExecutionRequest, *,
               required_capabilities: set, require_verified: bool = False) -> RuntimeAdapter:
        """Select an adapter after model/tool routing: capability coverage +
        health + lifecycle revalidation (Protocol §5). Deterministic order."""
        eligible_records = self.capabilities.eligible(
            required_capabilities, require_verified=require_verified)
        for record in eligible_records:
            adapter = self._adapters.get(record.runtime_id)
            if adapter is None:
                continue
            if adapter.health() == "UNAVAILABLE":
                continue
            if not required_capabilities.issubset(adapter.capabilities()):
                continue
            return adapter
        raise LookupError("no eligible runtime adapter satisfies the capability contract")
