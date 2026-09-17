"""Need/pain signals (Phase 11 §8).

Only recorded when evidence supports them. FACT / CLAIM / INFERENCE stay
distinct: an open AI-engineering role is a FACT; "they probably need contract
help" is an INFERENCE and is never presented as a FACT.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from .evidence import EvidenceRef, FactKind

SIGNAL_TYPES = (
    "ai_hiring", "genai_product_expansion", "documented_ai_initiative",
    "engineering_bottleneck", "rag_agent_llm_deployment",
    "contract_engineering_need", "explicit_technical_challenge",
)


@dataclass
class PainSignal:
    signal_id: str
    company_id: str
    signal_type: str
    kind: FactKind                       # FACT | CLAIM | INFERENCE
    description: str
    evidence: EvidenceRef
    created_at: str = ""

    @staticmethod
    def new_id() -> str:
        return "SIG-" + uuid.uuid4().hex[:10]

    def __post_init__(self):
        if self.signal_type not in SIGNAL_TYPES:
            raise ValueError(f"invalid signal type: {self.signal_type}")
        if self.kind == FactKind.INFERENCE and self.evidence.kind == FactKind.FACT:
            # An inference may cite a fact as its basis, but is recorded as INFERENCE.
            pass
        if not self.description:
            raise ValueError("signal description is required")
        self.created_at = self.created_at or self.evidence.captured_at

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["kind"] = self.kind.value
        d["evidence"] = self.evidence.to_dict()
        return d
