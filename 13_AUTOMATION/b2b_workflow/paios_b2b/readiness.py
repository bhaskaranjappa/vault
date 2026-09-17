"""Outreach readiness gate (Phase 11 §10-11).

A lead is outreach-ready only when identity, contact verification,
personalization evidence, authority, policy and duplicate checks all pass.
Otherwise NOT_READY with a reason. Lead data can never grant authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .candidate import CandidateRecord
from .contact import ContactRecord, ContactState, DecisionMaker
from .personalization import PersonalizationDraft


@dataclass
class ReadinessDecision:
    ready: bool
    reasons: list = field(default_factory=list)
    checks: dict = field(default_factory=dict)


class OutreachReadinessGate:
    """Portable readiness decision. Authority is an INPUT from the current
    policy chain — never derived from lead data or retrieved content."""

    def evaluate(self, *, candidate: CandidateRecord,
                 contact: ContactRecord | None,
                 decision_maker: DecisionMaker | None = None,
                 draft: PersonalizationDraft | None = None,
                 authority_allows_outreach: bool = False,
                 policy_constraints_pass: bool = True,
                 duplicate_status: str = "NOT_CONTACTED",
                 require_personalization: bool = True) -> ReadinessDecision:
        checks, reasons = {}, []

        checks["identity_verified"] = candidate.identity_confidence == "VERIFIED"
        if not checks["identity_verified"]:
            reasons.append(f"company identity is {candidate.identity_confidence}")

        # contact method verified (a VERIFIED person with an UNVERIFIED channel
        # is not sufficient — the METHOD must be verified)
        checks["contact_verified"] = (
            contact is not None and contact.state == ContactState.VERIFIED)
        if not checks["contact_verified"]:
            reasons.append("contact method not VERIFIED")

        # decision-maker role currency: stale role blocks readiness
        if decision_maker is not None and not decision_maker.role_current:
            checks["dm_role_current"] = False
            reasons.append("decision-maker role cannot be verified as current")
        else:
            checks["dm_role_current"] = True

        checks["personalization_evidence"] = (
            draft is not None and (bool(draft.claims) or not require_personalization))
        if require_personalization and not checks["personalization_evidence"]:
            reasons.append("no personalization evidence attached")
        if draft is not None:
            draft.validate()   # raises UnverifiedPersonalization on evidence-less claims

        checks["authority_allows"] = bool(authority_allows_outreach)
        if not authority_allows_outreach:
            reasons.append("authority policy does not authorize outreach to this target")

        checks["policy_pass"] = bool(policy_constraints_pass)
        if not policy_constraints_pass:
            reasons.append("policy constraints failed")

        checks["no_duplicate"] = duplicate_status == "NOT_CONTACTED"
        if duplicate_status != "NOT_CONTACTED":
            reasons.append(f"outreach state is {duplicate_status}, not NOT_CONTACTED")

        ready = all(checks.values())
        return ReadinessDecision(ready=ready, reasons=reasons, checks=checks)
