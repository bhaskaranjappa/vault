"""Portable PAIOS automation engine (Phase 12, AIOS_AUTOMATION_PROTOCOL_V1).

Runtime-independent automation control layer: durable automation intents,
logical triggers, an explicit state machine, durable run records, an
authority verification hook, idempotency, bounded retry, acceptance
evaluation and evidence logging. Scheduling/execution are adapter concerns.
"""

from .automation import (
    AutomationIntent, AutomationState, InvalidAutomationTransition,
    AutomationLedger, Trigger, TriggerType, ConditionRegistry,
    ConditionEvaluation, ExecutorAdapter, ExecutionResult,
    AuthorityVerifier, AuthorityDecision, SecretRejected, reject_secrets,
    InlineNoOpAdapter,
)
from .events import AutomationEventLog
from .engine import (AutomationEngine, UntrustedContent, DuplicateRunBlocked,
                     INJECTION_MARKERS)

__all__ = [
    "AutomationIntent", "AutomationState", "InvalidAutomationTransition",
    "AutomationLedger", "Trigger", "TriggerType", "ConditionRegistry",
    "ConditionEvaluation", "ExecutorAdapter", "ExecutionResult",
    "AuthorityVerifier", "AuthorityDecision", "SecretRejected",
    "reject_secrets", "InlineNoOpAdapter", "AutomationEventLog", "AutomationEngine",
    "UntrustedContent", "DuplicateRunBlocked", "INJECTION_MARKERS",
]
