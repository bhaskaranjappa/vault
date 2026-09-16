"""Task capability profiles and shared vocabularies for PAIOS routing.

Implements the portable task capability representation for Phase 10
(Model & Tool Routing). All fields are optional; unknown values stay None
(UNKNOWN) and are never invented.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# Canonical lifecycle: SUPPORTED -> INSTALLED -> ENABLED -> CONFIGURED
# -> AUTHENTICATED -> VERIFIED (from 02_AI_STACK/AI_TOOL_REGISTRY.md)
LIFECYCLE_ORDER = ("SUPPORTED", "INSTALLED", "ENABLED", "CONFIGURED",
                   "AUTHENTICATED", "VERIFIED")
LIFECYCLE_RANK = {s: i for i, s in enumerate(LIFECYCLE_ORDER)}

REASONING_LEVELS = ("LOW", "MEDIUM", "HIGH", "MAXIMUM")
REASONING_RANK = {s: i for i, s in enumerate(REASONING_LEVELS)}

LATENCY_TOLERANCES = ("INTERACTIVE", "NORMAL", "BATCH", "UNKNOWN")
COST_CONSTRAINTS = ("MINIMAL", "MODERATE", "UNRESTRICTED", "UNKNOWN")
PRIVACY_LEVELS = ("PUBLIC_OK", "INTERNAL_ONLY", "CONFIDENTIAL_LOCAL_ONLY")


@dataclass
class TaskCapabilityProfile:
    """What a task needs from models/tools. Absent fields impose no rule."""
    task_id: Optional[str] = None
    worker_id: Optional[str] = None
    context_package_id: Optional[str] = None

    reasoning_level: str = "MEDIUM"
    context_size: Optional[int] = None           # tokens required, if known
    vision_required: bool = False
    coding_required: bool = False
    web_required: bool = False
    browser_required: bool = False
    structured_data_required: bool = False
    long_horizon_required: bool = False
    parallelism_required: bool = False

    latency_tolerance: str = "UNKNOWN"
    cost_constraint: str = "UNKNOWN"
    reliability_requirement: str = "UNKNOWN"     # e.g. VERIFIED lifecycle floor
    privacy_requirement: str = "PUBLIC_OK"
    tool_requirements: list = field(default_factory=list)   # required tool types
    output_format: Optional[str] = None

    # data-routing rules (Phase 10 §13/§14)
    internal_data_sufficient: bool = False       # internal/canonical data-first
    current_data_required: bool = False          # fresh external fact needed

    max_cost_usd_per_1k: Optional[float] = None  # configured constraint only
    max_latency_ms: Optional[int] = None         # configured constraint only

    def required_model_capabilities(self) -> set:
        caps = set()
        if self.vision_required:
            caps.add("vision")
        if self.coding_required:
            caps.add("coding")
        if self.web_required:
            caps.add("web")
        if self.browser_required:
            caps.add("browser")
        if self.structured_data_required:
            caps.add("structured")
        if self.long_horizon_required:
            caps.add("long_horizon")
        return caps

    def validate(self) -> None:
        if self.reasoning_level not in REASONING_LEVELS:
            raise ValueError(f"invalid reasoning_level: {self.reasoning_level}")
        if self.latency_tolerance not in LATENCY_TOLERANCES:
            raise ValueError(f"invalid latency_tolerance: {self.latency_tolerance}")
        if self.cost_constraint not in COST_CONSTRAINTS:
            raise ValueError(f"invalid cost_constraint: {self.cost_constraint}")
        if self.privacy_requirement not in PRIVACY_LEVELS:
            raise ValueError(f"invalid privacy_requirement: {self.privacy_requirement}")
