"""Routing decision records with provenance, plus persistence.

A RoutingDecision is fully reproducible from its inputs: same profile +
registry + constraints -> same selection, alternatives, and decision hash.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .capabilities import TaskCapabilityProfile
from .models import ModelCandidate
from .tools import ToolCandidate


def _hash(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str)
                          .encode()).hexdigest()[:12]


@dataclass
class RoutingDecision:
    task_id: Optional[str]
    requirements: dict
    selected_model: Optional[dict]
    selected_tools: list
    reasoning_level: str
    constraints: dict
    alternatives: list
    fallback_chain: list
    decision_reason: str
    evidence_refs: list
    verification_state: str = "REQUESTED"        # requested route, not runtime fact
    rejected: list = field(default_factory=list)
    routing_id: str = field(default_factory=lambda: "RTG-" + uuid.uuid4().hex[:10])
    created_at: Optional[str] = None
    context_package_id: Optional[str] = None
    worker_id: Optional[str] = None
    input_hash: str = ""

    def finalize(self) -> "RoutingDecision":
        from .records_util import utc_now
        core = {
            "task_id": self.task_id, "requirements": self.requirements,
            "selected_model": self.selected_model,
            "selected_tools": self.selected_tools,
            "reasoning_level": self.reasoning_level,
            "constraints": self.constraints,
        }
        self.input_hash = _hash(core)
        self.created_at = self.created_at or utc_now()
        return self

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @classmethod
    def from_dict(cls, d: dict) -> "RoutingDecision":
        dec = cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
        return dec


class DecisionStore:
    def __init__(self, root: str | Path):
        self.dir = Path(root) / "routing_decisions"
        self.dir.mkdir(parents=True, exist_ok=True)

    def save(self, decision: RoutingDecision) -> RoutingDecision:
        decision.finalize()
        (self.dir / f"{decision.routing_id}.json").write_text(
            json.dumps(decision.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8")
        return decision

    def load(self, routing_id: str) -> RoutingDecision:
        return RoutingDecision.from_dict(json.loads(
            (self.dir / f"{routing_id}.json").read_text(encoding="utf-8")))

    def all(self) -> list:
        return [RoutingDecision.from_dict(json.loads(p.read_text(encoding="utf-8")))
                for p in sorted(self.dir.glob("RTG-*.json"))]
