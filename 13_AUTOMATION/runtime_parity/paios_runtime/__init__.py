"""Portable PAIOS cross-runtime parity layer (Phase 13,
AIOS_RUNTIME_ADAPTER_PROTOCOL_V1).

Vendor-neutral runtime adapter contract, capability registry with the
canonical lifecycle, a common execution request/result model, runtime
substitution with explicit records, parity enforcement, and a deterministic
side-effect-free reference adapter. Runtime output is untrusted data.
"""

from .adapters import (
    ReferenceRuntimeAdapter, RuntimeAdapter, RuntimeUnavailableAdapter,
    TimingOutAdapter, UnknownResultAdapter,
)
from .capabilities import (
    CapabilityRegistry, Lifecycle, RuntimeCapabilityRecord, RUNTIMES,
    VerificationState,
)
from .execution import ExecutionRequest, ExecutionResult, ExecutionStatus
from .parity import ParityViolation, ParityEnforcer, ParityCheck, RuntimeRegistry
from .substitution import SubstitutionRecord, SubstitutionChain, SubstitutionBlocked
from .untrusted import UntrustedContent, inspect_runtime_output
from .real_runtimes import inspect_real_runtimes, InspectionOutcome
from .zcode_adapter import CodexRuntimeAdapter, ZCodeRuntimeError

__all__ = [
    "ReferenceRuntimeAdapter", "RuntimeAdapter", "RuntimeUnavailableAdapter",
    "TimingOutAdapter", "UnknownResultAdapter",
    "CapabilityRegistry", "Lifecycle", "RuntimeCapabilityRecord", "RUNTIMES",
    "VerificationState",
    "ExecutionRequest", "ExecutionResult", "ExecutionStatus",
    "ParityViolation", "ParityEnforcer",
    "RuntimeRegistry", "SubstitutionRecord", "SubstitutionChain",
    "SubstitutionBlocked", "ParityCheck", "UntrustedContent",
    "inspect_runtime_output", "inspect_real_runtimes", "InspectionOutcome",
    "CodexRuntimeAdapter", "ZCodeRuntimeError",
]
