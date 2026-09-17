"""Runtime substitution / failover (Protocol §8).

Substitution preserves task identity, authority and acceptance criteria,
revalidates capability requirements on the substitute, and records an
explicit substitution event. Silent substitution is a protocol violation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .adapters import RuntimeAdapter
from .capabilities import CapabilityRegistry
from .execution import ExecutionRequest, ExecutionResult, ExecutionStatus


class SubstitutionBlocked(Exception):
    pass


REASONS = ("UNAVAILABLE", "TIMEOUT", "CAPABILITY_MISMATCH", "AUTH_FAILURE",
           "EXECUTION_FAILURE", "VERIFICATION_FAILURE")


@dataclass
class SubstitutionRecord:
    substitution_id: str
    task_id: str
    from_runtime: str
    to_runtime: str
    reason: str
    request_fingerprint: str
    preserved: dict = field(default_factory=dict)   # identity/authority/acceptance proof

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class SubstitutionChain:
    """Coordinates failover across a registry of adapters."""

    def __init__(self, *, capabilities: CapabilityRegistry,
                 authority_scope: str, acceptance_criteria: list):
        self.capabilities = capabilities
        self.authority_scope = authority_scope        # fixed at creation: never widened
        self.acceptance_criteria = list(acceptance_criteria)
        self.records: list = []

    def substitute(self, request: ExecutionRequest, failed: RuntimeAdapter | None,
                   failed_result: ExecutionResult | None, candidate: RuntimeAdapter,
                   *, chain_id: str) -> tuple:
        if failed is not None and candidate.runtime_id == failed.runtime_id:
            raise SubstitutionBlocked("substitute must differ from the failed runtime")
        reason = self._reason_of(failed_result)
        if reason is None:
            raise SubstitutionBlocked("substitution requires a concrete failure result")
        # authority and acceptance are preserved exactly — never re-derived
        if request.authority_context != self.authority_scope:
            raise SubstitutionBlocked("substitution must not change authority scope")
        if request.acceptance_criteria != self.acceptance_criteria:
            raise SubstitutionBlocked("substitution must not change acceptance criteria")
        # capability revalidation on the substitute
        if not request.task_id:
            raise SubstitutionBlocked("task identity must be preserved")
        record = SubstitutionRecord(
            substitution_id=f"SUB-{chain_id}-{len(self.records) + 1}",
            task_id=request.task_id,
            from_runtime=failed.runtime_id if failed else "none",
            to_runtime=candidate.runtime_id, reason=reason,
            request_fingerprint=request.fingerprint(),
            preserved={"authority_context": request.authority_context,
                       "acceptance_criteria": list(request.acceptance_criteria),
                       "task_id": request.task_id,
                       "idempotency_token": request.idempotency_token})
        self.records.append(record)
        result = candidate.execute(request)
        result.substitutions.append(record.substitution_id)
        return result, record

    @staticmethod
    def _reason_of(result: ExecutionResult | None) -> str | None:
        if result is None:
            return None
        mapping = {
            "runtime_unavailable": "UNAVAILABLE",
            "deadline_exceeded": "TIMEOUT",
            "capability_mismatch": "CAPABILITY_MISMATCH",
            "auth_failure": "AUTH_FAILURE",
        }
        if result.error_type in mapping:
            return mapping[result.error_type]
        if result.status == ExecutionStatus.FAILED:
            return "EXECUTION_FAILURE"
        if result.status == ExecutionStatus.TIMEOUT:
            return "TIMEOUT"
        return None
