"""Runtime capability registry (Protocol §3).

Lifecycle: SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED →
VERIFIED. Configuration never implies VERIFIED. UNKNOWN (no evidence) is
distinct from UNSUPPORTED (evidence of absence).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class Lifecycle:
    SUPPORTED = "SUPPORTED"
    INSTALLED = "INSTALLED"
    ENABLED = "ENABLED"
    CONFIGURED = "CONFIGURED"
    AUTHENTICATED = "AUTHENTICATED"
    VERIFIED = "VERIFIED"
    ORDER = (SUPPORTED, INSTALLED, ENABLED, CONFIGURED, AUTHENTICATED, VERIFIED)

    @classmethod
    def rank(cls, state: str) -> int:
        if state not in cls.ORDER:
            raise ValueError(f"unknown lifecycle state: {state}")
        return cls.ORDER.index(state)

    @classmethod
    def satisfies(cls, state: str, floor: str) -> bool:
        return cls.rank(state) >= cls.rank(floor)


class VerificationState:
    """Evidence-based verification status — orthogonal to configuration."""
    VERIFIED = "VERIFIED"       # direct observable behavior recorded
    CLAIMED = "CLAIMED"         # asserted by docs/config, not observed
    UNKNOWN = "UNKNOWN"         # no evidence either way
    UNSUPPORTED = "UNSUPPORTED" # evidence of absence
    ALL = (VERIFIED, CLAIMED, UNKNOWN, UNSUPPORTED)


@dataclass
class RuntimeCapabilityRecord:
    runtime_id: str
    capabilities: set = field(default_factory=set)       # declared capability names
    model_access: str = "UNKNOWN"                        # e.g. NONE | SINGLE | MULTI
    tool_access: str = "UNKNOWN"
    context_limits: str = "UNKNOWN"
    execution_mode: str = "UNKNOWN"                      # e.g. SYNC | ASYNC | BOTH
    streaming: bool = False
    parallelism: bool = False
    long_running: bool = False
    structured_output: bool = False
    web_capability: str = "UNKNOWN"
    auth_state: str = "UNKNOWN"                          # AUTHENTICATED | UNAUTHENTICATED | UNKNOWN
    lifecycle: str = Lifecycle.SUPPORTED
    verification: str = VerificationState.UNKNOWN        # explicit, evidence-based
    evidence_refs: list = field(default_factory=list)
    last_verified_at: str | None = None
    runtime_adapter_ref: str | None = None
    limitations: list = field(default_factory=list)

    def __post_init__(self):
        if not self.runtime_id:
            raise ValueError("capability record requires runtime_id")
        if self.verification not in VerificationState.ALL:
            raise ValueError(f"invalid verification state: {self.verification}")
        Lifecycle.rank(self.lifecycle)   # validates
        # Configuration alone must never imply VERIFIED (Protocol §3).
        if self.verification == VerificationState.VERIFIED and not self.evidence_refs:
            raise ValueError("VERIFIED requires evidence_refs (no fabricated verification)")

    def mark_verified(self, *, evidence_ref: str, timestamp: str) -> "RuntimeCapabilityRecord":
        """The only path to VERIFIED: direct observable evidence."""
        self.verification = VerificationState.VERIFIED
        self.lifecycle = Lifecycle.VERIFIED
        self.evidence_refs.append(evidence_ref)
        self.last_verified_at = timestamp
        return self

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["capabilities"] = sorted(self.capabilities)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "RuntimeCapabilityRecord":
        d = dict(d)
        d["capabilities"] = set(d.get("capabilities", []))
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class CapabilityRegistry:
    """Durable runtime capability registry (JSON on disk)."""

    def __init__(self, root: str | Path):
        self.path = Path(root) / "runtime_capabilities.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._records: dict = {}
        if self.path.exists():
            for rid, rec in json.loads(self.path.read_text(encoding="utf-8")).items():
                self._records[rid] = RuntimeCapabilityRecord.from_dict(rec)

    def register(self, record: RuntimeCapabilityRecord) -> RuntimeCapabilityRecord:
        self._records[record.runtime_id] = record
        self._persist()
        return record

    def get(self, runtime_id: str) -> RuntimeCapabilityRecord | None:
        return self._records.get(runtime_id)

    def all(self) -> list:
        return list(self._records.values())

    def eligible(self, required_capabilities: set, *, min_lifecycle: str = Lifecycle.SUPPORTED,
                 require_verified: bool = False) -> list:
        """Deterministic eligibility: capability coverage + lifecycle floor +
        optional VERIFIED requirement."""
        out = []
        for r in self._records.values():
            if not required_capabilities.issubset(r.capabilities):
                continue
            if not Lifecycle.satisfies(r.lifecycle, min_lifecycle):
                continue
            if require_verified and r.verification != VerificationState.VERIFIED:
                continue
            out.append(r)
        return sorted(out, key=lambda r: (r.verification != VerificationState.VERIFIED,
                                          r.runtime_id))

    def _persist(self) -> None:
        self.path.write_text(
            json.dumps({r.runtime_id: r.to_dict() for r in self._records.values()},
                       indent=2, ensure_ascii=False), encoding="utf-8")


#: Canonical runtime roster from AIOS_RUNTIME_INTEGRATION_MATRIX_V1.md §2.
RUNTIMES = ("grok-bot", "hermes-agent", "zcode", "opencode", "claude-code",
            "chatgpt", "claude", "gemini", "codex", "cursor",
            "reference-local")
