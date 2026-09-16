"""Model candidate registry entries for PAIOS routing.

A candidate carries only evidence-backed facts. Anything unknown stays None
(UNKNOWN) and is never populated with invented metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .capabilities import LIFECYCLE_RANK, REASONING_RANK


@dataclass
class ModelCandidate:
    model_id: str
    provider: str
    capabilities: set = field(default_factory=set)
    # capabilities vocabulary: vision, coding, web, browser, structured,
    # long_horizon, parallel
    context_window: Optional[int] = None         # None = UNKNOWN
    reasoning_levels: tuple = ("LOW", "MEDIUM")  # supported reasoning efforts
    cost_usd_per_1k: Optional[float] = None      # None = UNKNOWN
    latency_ms: Optional[int] = None             # None = UNKNOWN
    reliability: str = "UNKNOWN"                 # no invented reliability claims
    lifecycle: str = "SUPPORTED"                 # AIOS lifecycle stage
    evidence_refs: list = field(default_factory=list)
    last_verified: Optional[str] = None
    runtime_available: bool = True
    local: bool = False                          # local/no-network execution
    constraints: list = field(default_factory=list)

    def __post_init__(self):
        if not self.model_id or not self.provider:
            raise ValueError("model_id and provider are required")
        for lvl in self.reasoning_levels:
            if lvl not in REASONING_RANK:
                raise ValueError(f"invalid reasoning level: {lvl}")
        if self.lifecycle not in LIFECYCLE_RANK:
            raise ValueError(f"invalid lifecycle: {self.lifecycle}")
        if not self.evidence_refs and self.lifecycle == "VERIFIED":
            raise ValueError("VERIFIED lifecycle requires evidence_refs")

    def supports_reasoning(self, level: str) -> bool:
        return REASONING_RANK[level] <= max(REASONING_RANK[l]
                                            for l in self.reasoning_levels)

    def to_dict(self) -> dict:
        return {
            "model_id": self.model_id, "provider": self.provider,
            "capabilities": sorted(self.capabilities),
            "context_window": self.context_window,
            "reasoning_levels": list(self.reasoning_levels),
            "cost_usd_per_1k": self.cost_usd_per_1k,
            "latency_ms": self.latency_ms,
            "reliability": self.reliability, "lifecycle": self.lifecycle,
            "evidence_refs": list(self.evidence_refs),
            "last_verified": self.last_verified,
            "runtime_available": self.runtime_available,
            "local": self.local, "constraints": list(self.constraints),
        }
