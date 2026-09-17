"""Personalization engine (Phase 11 §9).

Every personalized claim in a draft must cite verified evidence. If a draft
line references a fact with no supporting EvidenceRef, generation is blocked.
Fabricated familiarity and unverified work claims are prohibited.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from .evidence import EvidenceRef


@dataclass
class PersonalizationClaim:
    """One claim inside a draft, bound to its evidence. evidence=None is
    an unverified claim and blocks validation."""
    statement: str
    fact_referenced: str
    evidence: EvidenceRef | None
    confidence: str = "MEDIUM"

    def __post_init__(self):
        if not self.statement or not self.fact_referenced:
            raise ValueError("claim requires statement and referenced fact")
        if self.confidence not in ("HIGH", "MEDIUM", "LOW"):
            raise ValueError(f"invalid confidence: {self.confidence}")

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["evidence"] = self.evidence.to_dict() if self.evidence else None
        return d


class UnverifiedPersonalization(Exception):
    pass


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class PersonalizationDraft:
    draft_id: str
    company_id: str
    contact_id: str
    body: str
    claims: list = field(default_factory=list)      # PersonalizationClaim list
    created_at: str = ""

    @staticmethod
    def new_id() -> str:
        return "DRF-" + uuid.uuid4().hex[:10]

    def __post_init__(self):
        self.created_at = self.created_at or _now()

    def validate(self) -> None:
        """Every non-generic draft claim must be evidence-backed."""
        for c in self.claims:
            if c.evidence is None or not c.evidence.source:
                raise UnverifiedPersonalization(
                    f"claim lacks evidence: {c.fact_referenced}")

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["claims"] = [c.to_dict() for c in self.claims]
        return d


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
