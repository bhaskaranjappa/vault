"""Candidate company records and qualification (Phase 11 §4-5).

Identity is established through an identity_confidence field fed by
distinct corroborating sources. Two candidates with the same name are never
merged without sufficient disambiguating evidence (adversarial: identity
collision). Qualification is transparent per-dimension evidence — no
arbitrary universal "best lead" score.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from .evidence import EvidenceRef


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class CandidateRecord:
    company_id: str
    name: str
    domain: Optional[str] = None
    geography: Optional[str] = None
    product_category: Optional[str] = None
    ai_activity: Optional[str] = None
    signals: list = field(default_factory=list)          # verified signal summaries
    evidence: list = field(default_factory=list)          # EvidenceRef list
    identity_confidence: str = "UNVERIFIED"               # UNVERIFIED|PARTIAL|VERIFIED
    identity_ambiguity: Optional[str] = None              # description of collision risk
    captured_at: Optional[str] = None
    sources: list = field(default_factory=list)           # distinct source ids

    @staticmethod
    def new_id() -> str:
        return "CO-" + uuid.uuid4().hex[:10]

    def __post_init__(self):
        self.captured_at = self.captured_at or _now()

    def add_evidence(self, ref: EvidenceRef) -> None:
        self.evidence.append(ref)
        if ref.source not in self.sources:
            self.sources.append(ref.source)

    def distinct_source_count(self) -> int:
        return len(self.sources)

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["evidence"] = [e.to_dict() for e in self.evidence]
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "CandidateRecord":
        rec = cls(**{k: v for k, v in d.items()
                     if k in cls.__dataclass_fields__ and k != "evidence"})
        rec.evidence = [EvidenceRef.from_dict(e) for e in d.get("evidence", [])]
        return rec


# Transparent qualification dimensions; each is evidence-backed or UNKNOWN.
QUALIFICATION_DIMENSIONS = (
    "technical_fit", "likely_genai_need", "evidence_strength", "timing_signal",
    "contract_suitability", "geography_fit", "product_relevance",
    "decision_maker_accessibility", "contact_confidence", "outreach_readiness",
)


@dataclass
class QualificationProfile:
    company_id: str
    dimensions: dict = field(default_factory=dict)   # dim -> {value, evidence_ref, kind}
    notes: list = field(default_factory=list)

    def __post_init__(self):
        unknown = set(self.dimensions) - set(QUALIFICATION_DIMENSIONS)
        if unknown:
            raise ValueError(f"unknown qualification dimensions: {sorted(unknown)}")

    def set_dimension(self, name: str, value, ref: EvidenceRef) -> None:
        if name not in QUALIFICATION_DIMENSIONS:
            raise ValueError(f"unknown dimension: {name}")
        self.dimensions[name] = {"value": value, "evidence": ref.to_dict()}

    def unsupported_dimensions(self) -> list:
        """Dimensions set without evidence — invalid by policy."""
        return [k for k, v in self.dimensions.items() if not v.get("evidence")]

    def to_dict(self) -> dict:
        return dict(self.__dict__)
