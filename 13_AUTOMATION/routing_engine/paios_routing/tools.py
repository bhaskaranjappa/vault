"""Tool candidate registry entries for PAIOS routing."""

from __future__ import annotations

from dataclasses import dataclass, field

from .capabilities import LIFECYCLE_RANK

# PLAN.md §18 tool routing preference order (index = preference rank)
TOOL_TYPE_PREFERENCE = ("internal", "connector", "web", "browser", "desktop", "user")

DATA_SENSITIVITIES = ("PUBLIC", "INTERNAL", "PERSONAL", "SENSITIVE")


@dataclass
class ToolCandidate:
    tool_id: str
    type: str                                    # internal|connector|web|browser|desktop|user
    capabilities: set = field(default_factory=set)   # e.g. filesystem, git, search, fetch, parse
    supported_operations: set = field(default_factory=set)  # e.g. read, write, query
    provider: str = "unknown"
    lifecycle: str = "SUPPORTED"
    authenticated: bool = False
    permission_state: str = "UNKNOWN"            # e.g. read-only / read-write / UNKNOWN
    verification_state: str = "SUPPORTED"
    data_sensitivity: str = "INTERNAL"           # max sensitivity it may touch
    network_required: bool = True
    runtime_adapter: str = "unknown"
    evidence_refs: list = field(default_factory=list)
    limitations: list = field(default_factory=list)

    def __post_init__(self):
        if not self.tool_id:
            raise ValueError("tool_id is required")
        if self.type not in TOOL_TYPE_PREFERENCE:
            raise ValueError(f"invalid tool type: {self.type}")
        if self.lifecycle not in LIFECYCLE_RANK:
            raise ValueError(f"invalid lifecycle: {self.lifecycle}")
        if not self.evidence_refs and self.verification_state == "VERIFIED":
            raise ValueError("VERIFIED tool requires evidence_refs")

    def preference_rank(self) -> int:
        return TOOL_TYPE_PREFERENCE.index(self.type)

    def to_dict(self) -> dict:
        return {
            "tool_id": self.tool_id, "type": self.type,
            "capabilities": sorted(self.capabilities),
            "supported_operations": sorted(self.supported_operations),
            "provider": self.provider, "lifecycle": self.lifecycle,
            "authenticated": self.authenticated,
            "permission_state": self.permission_state,
            "verification_state": self.verification_state,
            "data_sensitivity": self.data_sensitivity,
            "network_required": self.network_required,
            "runtime_adapter": self.runtime_adapter,
            "evidence_refs": list(self.evidence_refs),
            "limitations": list(self.limitations),
        }
