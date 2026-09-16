"""Model fallback chains (Phase 10 §8, §23).

A fallback fires only on a concrete reason (timeout, provider failure,
unavailability, capability mismatch, context limit, cost/latency constraint).
A fallback candidate MUST satisfy the original capability contract — a cheaper
or faster candidate lacking a required capability is never acceptable.

Fallback is recorded, never silent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .capabilities import TaskCapabilityProfile
from .models import ModelCandidate
from .router import FALLBACK_REASONS, filter_models, rank_models


class FallbackTriggered(Exception):
    """Terminal failure: no candidate in the chain can satisfy the contract."""

    def __init__(self, attempted: list, last_reason: str):
        self.attempted = attempted
        self.last_reason = last_reason
        super().__init__(
            f"fallback chain exhausted (attempted: {attempted}); last failure: {last_reason}")


@dataclass
class FallbackStep:
    from_model: Optional[str]
    to_model: Optional[str]
    reason: str
    within_contract: bool
    recorded_at: str = ""

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class FallbackChain:
    """Walks the route's alternative chain on concrete failure reasons.

    Each step re-validates the candidate against the ORIGINAL capability
    profile, so capability regression via fallback is impossible.
    """

    def __init__(self, profile: TaskCapabilityProfile, route):
        self.profile = profile
        self.route = route                      # ModelRoute
        self.steps: list = []
        self.current: Optional[ModelCandidate] = route.selected
        self.attempted: list = []

    def report_failure(self, reason: str) -> Optional[ModelCandidate]:
        """Report a concrete failure of the current candidate; advance the
        chain. Returns the next candidate, or raises FallbackTriggered."""
        if reason not in FALLBACK_REASONS:
            raise ValueError(
                f"fallback requires a concrete reason; '{reason}' is not in "
                f"{FALLBACK_REASONS} — silent switching is prohibited")
        self.attempted.append(self.current.model_id if self.current else None)

        # Re-filter ALL route candidates (selected + alternatives) against the
        # original contract; the previous model is now excluded as failed.
        pool = ([self.route.selected] if self.route.selected else []) + \
            list(self.route.alternatives)
        remaining = [m for m in pool
                     if m.model_id not in self.attempted and m.runtime_available]
        eligible, rejected = filter_models(self.profile, remaining)
        if not eligible:
            raise FallbackTriggered(self.attempted, reason)

        nxt = rank_models(eligible)[0]
        self.steps.append(FallbackStep(
            from_model=self.current.model_id if self.current else None,
            to_model=nxt.model_id, reason=reason, within_contract=True,
            recorded_at=__import__("paios_routing.records_util", fromlist=["utc_now"]).utc_now()))
        self.current = nxt
        return nxt

    def history(self) -> list:
        return [s.to_dict() for s in self.steps]
