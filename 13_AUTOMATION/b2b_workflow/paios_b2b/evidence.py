"""Evidence model for the B2B workflow (Phase 11 §3-4, §8).

Every durable workflow fact carries provenance. FACT / CLAIM / INFERENCE are
never merged: a search-result mention is not identity, a scraped contact is
not verification, an inferred need is not a stated need.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FactKind(str, Enum):
    FACT = "FACT"            # directly observed from a citable source
    CLAIM = "CLAIM"          # asserted by a source but not independently verified
    INFERENCE = "INFERENCE"  # derived; never promoted to FACT without evidence


@dataclass(frozen=True)
class EvidenceRef:
    """A single piece of provenance. Immutable; shared by reference."""
    source: str                  # URL, path, or canonical record id
    captured_at: str             # ISO-8601
    kind: FactKind = FactKind.FACT
    quote: str = ""              # short supporting quote, optional
    confidence: str = "MEDIUM"   # HIGH | MEDIUM | LOW

    def __post_init__(self):
        if not self.source or not self.captured_at:
            raise ValueError("evidence requires source and captured_at")
        if self.confidence not in ("HIGH", "MEDIUM", "LOW"):
            raise ValueError(f"invalid confidence: {self.confidence}")

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["kind"] = self.kind.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "EvidenceRef":
        return cls(source=d["source"], captured_at=d["captured_at"],
                   kind=FactKind(d.get("kind", "FACT")),
                   quote=d.get("quote", ""), confidence=d.get("confidence", "MEDIUM"))
