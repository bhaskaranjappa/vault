"""Deterministic capability-based model and tool routing.

Sequence (Phase 10 contract):
  eliminate incompatible -> eliminate unverified (where required) ->
  apply constraints -> rank deterministically -> select -> retain alternatives

Selection is task-specific. There is deliberately no global "best model" score.
Ranking key (deterministic, evidence-based only):
  lifecycle rank (desc), evidence count (desc), model_id (asc)
No invented quality/cost/latency scores participate in ranking.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .capabilities import LIFECYCLE_RANK, TaskCapabilityProfile
from .models import ModelCandidate
from .tools import TOOL_TYPE_PREFERENCE, ToolCandidate

# Concrete fallback reasons; silent switching without one of these is a bug.
FALLBACK_REASONS = ("TIMEOUT", "PROVIDER_FAILURE", "UNAVAILABLE",
                    "CAPABILITY_MISMATCH", "CONTEXT_LIMIT",
                    "COST_CONSTRAINT", "LATENCY_CONSTRAINT")


def _lifecycle_floor(profile: TaskCapabilityProfile) -> str:
    """Explicit reliability requirement sets the lifecycle floor; an UNKNOWN
    requirement imposes no floor (unknown stays unknown, fail-visible later
    at constraint checks instead)."""
    req = (profile.reliability_requirement or "").upper()
    return req if req in LIFECYCLE_RANK else "SUPPORTED"


def filter_models(profile: TaskCapabilityProfile, candidates: list) -> tuple[list, list]:
    """Return (eligible, rejected) with per-candidate rejection reasons."""
    eligible, rejected = [], []
    required = profile.required_model_capabilities()
    floor = _lifecycle_floor(profile)
    for m in candidates:
        reason = None
        missing = required - set(m.capabilities)
        if missing:
            reason = f"capability_mismatch:{'+'.join(sorted(missing))}"
        elif not m.supports_reasoning(profile.reasoning_level):
            reason = f"reasoning_level_unsupported:{profile.reasoning_level}"
        elif not m.runtime_available:
            reason = "unavailable"
        elif profile.context_size and (m.context_window is None
                                       or m.context_window < profile.context_size):
            reason = ("context_limit:unknown" if m.context_window is None
                      else f"context_limit:{m.context_window}<{profile.context_size}")
        elif LIFECYCLE_RANK[m.lifecycle] < LIFECYCLE_RANK[floor]:
            reason = f"verification_insufficient:{m.lifecycle}<{floor}"
        elif profile.privacy_requirement in ("INTERNAL_ONLY", "CONFIDENTIAL_LOCAL_ONLY") and not m.local:
            reason = "privacy_conflict:external_provider"
        elif profile.max_cost_usd_per_1k is not None and (
                m.cost_usd_per_1k is None or m.cost_usd_per_1k > profile.max_cost_usd_per_1k):
            reason = ("cost_constraint:cost_unknown" if m.cost_usd_per_1k is None
                      else f"cost_constraint:{m.cost_usd_per_1k}")
        elif profile.max_latency_ms is not None and (
                m.latency_ms is None or m.latency_ms > profile.max_latency_ms):
            reason = ("latency_constraint:latency_unknown" if m.latency_ms is None
                      else f"latency_constraint:{m.latency_ms}")
        (rejected if reason else eligible).append((m, reason) if reason else m)
    return eligible, [r for _, r in rejected]


def rank_models(eligible: list) -> list:
    return sorted(eligible, key=lambda m: (-LIFECYCLE_RANK[m.lifecycle],
                                           -len(m.evidence_refs), m.model_id))


def filter_tools(profile: TaskCapabilityProfile, candidates: list, *,
                 authority_allowed_tools: list | None = None,
                 network_allowed: bool = True,
                 max_data_sensitivity: str = "INTERNAL") -> tuple[list, list]:
    from .records_util import sensitivity_rank
    eligible, rejected = [], []
    for t in candidates:
        reason = None
        if profile.tool_requirements and not (set(profile.tool_requirements) & t.capabilities):
            reason = f"capability_mismatch:needs:{'+'.join(profile.tool_requirements)}"
        elif not network_allowed and t.network_required:
            reason = "network_not_permitted"
        elif authority_allowed_tools is not None and t.tool_id not in authority_allowed_tools:
            reason = "authority_not_permitted"
        elif t.verification_state not in LIFECYCLE_RANK or \
                LIFECYCLE_RANK[t.verification_state] < LIFECYCLE_RANK["CONFIGURED"]:
            reason = f"verification_insufficient:{t.verification_state}"
        elif profile.current_data_required and t.network_required is False:
            reason = "stale_source:current_data_required"
        elif profile.internal_data_sufficient and t.type == "web":
            reason = "internal_data_sufficient:external_not_needed"
        elif sensitivity_rank(t.data_sensitivity) > sensitivity_rank(max_data_sensitivity):
            reason = "sensitivity_boundary"
        (rejected if reason else eligible).append((t, reason) if reason else t)
    return eligible, [r for _, r in rejected]


def rank_tools(eligible: list) -> list:
    """Internal-data-first: PLAN §18 preference order, then verification,
    then evidence count, then id — fully deterministic."""
    return sorted(eligible, key=lambda t: (t.preference_rank(),
                                           -LIFECYCLE_RANK[t.verification_state],
                                           -len(t.evidence_refs), t.tool_id))


@dataclass
class ModelRoute:
    selected: ModelCandidate
    alternatives: list = field(default_factory=list)   # ordered fallback chain
    rejected: list = field(default_factory=list)       # (model_id, reason)
    decision_reason: str = ""


@dataclass
class ToolRoute:
    selected: list = field(default_factory=list)       # ordered tool ids
    alternatives: list = field(default_factory=list)
    rejected: list = field(default_factory=list)
    decision_reason: str = ""


def route_models(profile: TaskCapabilityProfile, candidates: list) -> ModelRoute:
    """Deterministic model route: filter -> rank -> select + fallback chain."""
    eligible, rejected = filter_models(profile, candidates)
    if not eligible:
        return ModelRoute(selected=None, rejected=rejected,
                          decision_reason="no eligible model satisfies the capability contract")
    ranked = rank_models(eligible)
    return ModelRoute(
        selected=ranked[0], alternatives=ranked[1:], rejected=rejected,
        decision_reason=(
            f"capability match + lifecycle {ranked[0].lifecycle} + "
            f"{len(ranked[0].evidence_refs)} evidence refs within constraints"))


def route_tools(profile: TaskCapabilityProfile, candidates: list, *,
                authority_allowed_tools: list | None = None,
                network_allowed: bool = True,
                max_data_sensitivity: str = "INTERNAL") -> ToolRoute:
    """Deterministic tool route: internal-data-first preference order."""
    eligible, rejected = filter_tools(
        profile, candidates, authority_allowed_tools=authority_allowed_tools,
        network_allowed=network_allowed, max_data_sensitivity=max_data_sensitivity)
    if not eligible:
        return ToolRoute(rejected=rejected,
                         decision_reason="no eligible tool satisfies requirements + constraints")
    ranked = rank_tools(eligible)
    return ToolRoute(
        selected=[t.tool_id for t in ranked],
        alternatives=[], rejected=rejected,
        decision_reason=(
            "preference order " + ">".join(t.tool_id for t in ranked) +
            ("; internal-data-first applied" if profile.internal_data_sufficient else "")))
