"""Durable automation intents, state machine and persistence (Protocol §1, §4, §6, §10).

A trigger firing is never success: execution must complete and pass
acceptance criteria before an automation reaches SUCCEEDED. State lives in
11_STATE/automation records — never in model memory.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class AutomationState:
    DRAFT = "DRAFT"
    ENABLED = "ENABLED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    DISABLED = "DISABLED"
    ALL = (DRAFT, ENABLED, RUNNING, SUCCEEDED, FAILED, RETRYING, DISABLED)

    TRANSITIONS = {
        DRAFT: {ENABLED, DISABLED},
        ENABLED: {RUNNING, DISABLED},
        RUNNING: {SUCCEEDED, FAILED},   # in-flight disable is runtime-dependent
        SUCCEEDED: {ENABLED, DISABLED},   # terminal, but owner can retire it
        FAILED: {RETRYING, DISABLED, ENABLED},
        RETRYING: {RUNNING, FAILED, DISABLED},
        DISABLED: {ENABLED},         # explicit re-enable after disablement
    }


class InvalidAutomationTransition(Exception):
    pass


class SecretRejected(Exception):
    """A credential-like value was found in a field bound for persistence."""


# Heuristic secret detector (AD-05): reject obvious credential-like values.
_SECRET_PATTERNS = (
    re.compile(r"(?i)\b(sk|pk|api[_-]?key|token|secret|password|passwd|pwd)[_\-]?\s*[:=]\s*\S+"),
    re.compile(r"\b(?:ghp|gho|ghs|ghu|xox[baprs]|AKIA|AIza)[A-Za-z0-9_\-]{10,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def reject_secrets(value) -> None:
    """Raise SecretRejected when a credential-like value is embedded."""
    text = json.dumps(value, default=str) if not isinstance(value, str) else value
    for pat in _SECRET_PATTERNS:
        if pat.search(text):
            raise SecretRejected(f"credential-like value rejected from persistence: {pat.pattern}")


# ---------------------------------------------------------------------------
# Triggers (Protocol §3, §14) — logical only; real scheduling is an adapter.
# ---------------------------------------------------------------------------

class TriggerType:
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"
    RECURRING = "RECURRING"
    CONDITION = "CONDITION"
    EVENT = "EVENT"
    ALL = (MANUAL, SCHEDULED, RECURRING, CONDITION, EVENT)


@dataclass
class Trigger:
    trigger_type: str
    # SCHEDULED/RECURRING metadata
    frequency: Optional[str] = None          # e.g. DAILY
    window: Optional[str] = None
    timezone: Optional[str] = None
    # CONDITION metadata
    condition: Optional[str] = None
    # EVENT metadata
    event_name: Optional[str] = None
    # fire bookkeeping (idempotency support)
    last_fired_at: Optional[str] = None

    def __post_init__(self):
        if self.trigger_type not in TriggerType.ALL:
            raise ValueError(f"unknown trigger type: {self.trigger_type}")
        if self.trigger_type == TriggerType.CONDITION and not self.condition:
            raise ValueError("CONDITION trigger requires a condition expression")

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, d: dict) -> "Trigger":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class ConditionEvaluation:
    """Logical condition result: TRUE / FALSE / UNKNOWN. External content can
    be an input to evaluation but can never redefine the condition itself."""
    value: str                                # TRUE | FALSE | UNKNOWN
    reason: str = ""

    def __post_init__(self):
        if self.value not in ("TRUE", "FALSE", "UNKNOWN"):
            raise ValueError(f"invalid condition value: {self.value}")


class ConditionRegistry:
    """Named, engine-registered condition evaluators. Retrieved content cannot
    register new conditions (AD: untrusted content cannot redefine the rule)."""

    def __init__(self):
        self._evaluators: dict = {}

    def register(self, name: str, evaluator) -> None:
        self._evaluators[name] = evaluator

    def evaluate(self, condition: str, context: dict | None = None) -> ConditionEvaluation:
        evaluator = self._evaluators.get(condition)
        if evaluator is None:
            return ConditionEvaluation("UNKNOWN", f"no registered evaluator for condition {condition!r}")
        try:
            result = evaluator(context or {})
        except Exception as exc:            # evaluator failure is UNKNOWN, never TRUE
            return ConditionEvaluation("UNKNOWN", f"evaluator error: {exc}")
        if result not in ("TRUE", "FALSE"):
            return ConditionEvaluation("UNKNOWN", "evaluator returned non-boolean result")
        return ConditionEvaluation(result)


# ---------------------------------------------------------------------------
# Authority (Protocol §2; BOT_AUTHORITY_PROTOCOL) — hook, never a backend.
# ---------------------------------------------------------------------------

class AuthorityDecision:
    AUTHORIZED = "AUTHORIZED"
    UNAUTHORIZED = "UNAUTHORIZED"
    UNKNOWN = "UNKNOWN"


@dataclass
class AuthorityResult:
    decision: str                             # AUTHORIZED | UNAUTHORIZED | UNKNOWN
    reason: str = ""
    effective_scope: str = ""


class AuthorityVerifier:
    """Portable authority verification hook. The default implementation
    verifies against an explicit, injected policy scope string; production
    deployments supply their own subclass. No backend is invented here."""

    def __init__(self, policy_scope: str = ""):
        self.policy_scope = policy_scope      # empty => nothing is authorized

    def verify(self, automation: "AutomationIntent", action: str = "execute") -> AuthorityResult:
        if not self.policy_scope:
            return AuthorityResult(AuthorityDecision.UNAUTHORIZED,
                                   "no owner policy scope loaded")
        if action == "activate" and automation.reversible == "IRREVERSIBLE" \
                and not automation.high_impact_policy_authorized:
            return AuthorityResult(
                AuthorityDecision.UNAUTHORIZED,
                "irreversible action requires explicit policy-level authorization")
        if automation.authority_scope and automation.authority_scope not in self.policy_scope:
            return AuthorityResult(AuthorityDecision.UNAUTHORIZED,
                                   "requested authority scope is outside current policy")
        return AuthorityResult(AuthorityDecision.AUTHORIZED,
                               effective_scope=automation.authority_scope or self.policy_scope)


# ---------------------------------------------------------------------------
# Executor adapter boundary (Protocol §14)
# ---------------------------------------------------------------------------

@dataclass
class ExecutionResult:
    status: str                               # COMPLETED | FAILED | UNKNOWN
    output_ref: Optional[str] = None
    error: Optional[str] = None
    verification: Optional[dict] = None
    detail: str = ""

    def __post_init__(self):
        if self.status not in ("COMPLETED", "FAILED", "UNKNOWN"):
            raise ValueError(f"invalid execution status: {self.status}")


class ExecutorAdapter:
    """Runtime-neutral executor boundary. Engines must never assume a runtime
    supports scheduling, cancellation, background work or model switching —
    those are adapter capabilities discovered via ``capabilities``."""

    adapter_id = "abstract"

    #: capability names this adapter actually supports
    capabilities: tuple = ()

    def execute(self, automation: "AutomationIntent", run) -> ExecutionResult:
        raise NotImplementedError

    def verify(self, automation: "AutomationIntent", run) -> dict:
        return {"verified": False, "reason": "adapter does not implement verification"}

    def cancel(self, run) -> bool:
        raise NotImplementedError("cancellation is runtime-dependent")


class InlineNoOpAdapter(ExecutorAdapter):
    """Reference adapter for tests and dry-runs. It performs no external
    action and can never produce an external side effect."""

    adapter_id = "inline-noop"
    capabilities = ("execute", "verify")

    def execute(self, automation: "AutomationIntent", run) -> ExecutionResult:
        return ExecutionResult(status="COMPLETED",
                               detail="inline no-op adapter: synthetic completion, no external effect")

    def verify(self, automation: "AutomationIntent", run) -> dict:
        return {"verified": True, "adapter": self.adapter_id}


# ---------------------------------------------------------------------------
# Automation intent + ledger
# ---------------------------------------------------------------------------

@dataclass
class AutomationIntent:
    automation_id: str
    task_ref: Optional[str]
    objective: str
    scope: str
    authority_scope: str
    trigger: Trigger
    inputs: list = field(default_factory=list)           # input/context references
    context_package_id: Optional[str] = None
    output_location: Optional[str] = None
    acceptance_criteria: list = field(default_factory=list)
    evidence_requirements: list = field(default_factory=list)
    failure_policy: str = "record_and_stop"              # record_and_stop | retry_bounded
    retry_limit: int = 0
    retry_backoff_seconds: int = 0
    idempotency_key: Optional[str] = None                # deterministic dedup key
    idempotency_window: Optional[str] = None             # e.g. "2026-09-17" execution window
    enabled: bool = False
    reversible: str = "REVERSIBLE"                       # REVERSIBLE | IRREVERSIBLE
    high_impact_policy_authorized: bool = False
    state: str = AutomationState.DRAFT
    runtime_adapter_ref: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.automation_id or not self.objective:
            raise ValueError("automation requires automation_id and objective")
        if self.reversible not in ("REVERSIBLE", "IRREVERSIBLE"):
            raise ValueError(f"invalid reversibility: {self.reversible}")
        if not self.created_at:
            self.created_at = now_iso()
        self.updated_at = now_iso()
        self.check_secrets()

    def check_secrets(self) -> None:
        reject_secrets([self.objective, self.scope, self.inputs,
                        self.acceptance_criteria, self.evidence_requirements])

    @staticmethod
    def new_id() -> str:
        return "AUT-" + uuid.uuid4().hex[:10]

    def transition(self, new_state: str, *, reason: str = "") -> None:
        if new_state not in AutomationState.ALL:
            raise InvalidAutomationTransition(f"unknown automation state: {new_state}")
        if new_state not in AutomationState.TRANSITIONS[self.state]:
            raise InvalidAutomationTransition(
                f"invalid automation transition {self.state} -> {new_state} ({reason})")
        self.state = new_state
        self.updated_at = now_iso()

    def idempotency_token(self) -> str:
        """automation_id + logical input + execution window (Protocol §6)."""
        parts = [self.automation_id, self.idempotency_key or self.objective,
                 self.idempotency_window or ""]
        return "|".join(parts)

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["trigger"] = self.trigger.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AutomationIntent":
        d = dict(d)
        d["trigger"] = Trigger.from_dict(d["trigger"])
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class AutomationLedger:
    """Durable automation + run record storage under <root>/records and
    <root>/runs. Run history is append-only — prior runs are never overwritten."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.records_dir = self.root / "records"
        self.runs_dir = self.root / "runs"
        self.records_dir.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    # -- automations --------------------------------------------------------
    def _aut_path(self, automation_id: str) -> Path:
        return self.records_dir / f"{automation_id}.json"

    def save_automation(self, aut: AutomationIntent) -> None:
        aut.check_secrets()
        self._aut_path(aut.automation_id).write_text(
            json.dumps(aut.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    def load_automation(self, automation_id: str) -> AutomationIntent:
        return AutomationIntent.from_dict(json.loads(
            self._aut_path(automation_id).read_text(encoding="utf-8")))

    def all_automations(self) -> list:
        out = []
        for p in sorted(self.records_dir.glob("AUT-*.json")):
            out.append(AutomationIntent.from_dict(json.loads(p.read_text(encoding="utf-8"))))
        return out

    # -- runs ----------------------------------------------------------------
    def save_run(self, run: "RunRecord") -> None:
        reject_secrets(run.to_dict())
        path = self.runs_dir / f"{run.run_id}.json"
        if path.exists():                    # append-only history for closeout
            history = self.runs_dir / f"{run.run_id}.history.jsonl"
            with history.open("a", encoding="utf-8") as f:
                f.write(json.dumps(run.to_dict(), ensure_ascii=False) + "\n")
        path.write_text(json.dumps(run.to_dict(), indent=2, ensure_ascii=False),
                        encoding="utf-8")

    def load_run(self, run_id: str) -> "RunRecord":
        return RunRecord.from_dict(json.loads(
            (self.runs_dir / f"{run_id}.json").read_text(encoding="utf-8")))

    def runs_for(self, automation_id: str) -> list:
        out = []
        for p in sorted(self.runs_dir.glob("RUN-*.json")):
            run = RunRecord.from_dict(json.loads(p.read_text(encoding="utf-8")))
            if run.automation_id == automation_id:
                out.append(run)
        return out


@dataclass
class RunRecord:
    run_id: str
    automation_id: str
    trigger_type: str
    started_at: str
    executor: str
    authority_scope: str = ""
    authority_decision: str = ""
    context_package_id: Optional[str] = None
    checkpoint_id: Optional[str] = None
    route_ref: Optional[str] = None                  # Phase 10 decision reference
    task_ref: Optional[str] = None                   # Phase 9 task reference
    worker_refs: list = field(default_factory=list)
    actions_attempted: list = field(default_factory=list)
    result: str = "PENDING"                          # PENDING|COMPLETED|FAILED|UNKNOWN|RECONCILE
    acceptance: Optional[dict] = None                # per-criterion evaluation
    error: Optional[str] = None
    recovery_attempts: int = 0
    retry_reasons: list = field(default_factory=list)
    evidence_refs: list = field(default_factory=list)
    idempotency_token: Optional[str] = None
    final_state: str = "RUNNING"
    ended_at: Optional[str] = None

    @staticmethod
    def new_id() -> str:
        return "RUN-" + uuid.uuid4().hex[:10]

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @classmethod
    def from_dict(cls, d: dict) -> "RunRecord":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
