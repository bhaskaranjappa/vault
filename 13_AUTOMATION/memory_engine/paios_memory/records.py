"""Memory record model for the PAIOS Phase 8 file-backed memory engine.

Implements the logical schema from 03_PROTOCOLS/AIOS_MEMORY_ARCHITECTURE_V1.md.
Standard library only. Records serialize to JSON-compatible dicts; the
file-backed store writes them as JSON files under 11_STATE/memory/records/.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

TYPES = ("FACT", "PREFERENCE", "DECISION", "OBSERVATION", "PROCEDURE",
         "PROJECT_STATE", "CONTACT", "OTHER")
STATUSES = ("ACTIVE", "SUPERSEDED", "INVALIDATED", "CONFLICTING", "HISTORICAL")
CLASSIFICATIONS = ("STATED", "INFERRED", "RUNTIME_OBSERVED")
SOURCE_KINDS = ("OWNER", "CANONICAL_FILE", "RUNTIME", "CONVERSATION",
                "EXTERNAL_SOURCE", "AGENT")
SENSITIVITY_LEVELS = ("PUBLIC", "INTERNAL", "PERSONAL", "SENSITIVE")
# Ordered from least to most restrictive; used for sensitivity ceilings.
SENSITIVITY_ORDER = {name: i for i, name in enumerate(SENSITIVITY_LEVELS)}
CONFIDENCE_LEVELS = ("HIGH", "MEDIUM", "LOW", "UNKNOWN")

SECRET_PATTERNS = (
    re.compile(r"(?i)\b(sk-|ghp_|gho_|github_pat_|xoxb-|AKIA)[A-Za-z0-9_-]{8,}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|password|passwd|token|bearer)\b\s*[:=]\s*\S+"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_memory_id() -> str:
    return "MEM-" + uuid.uuid4().hex[:12]


def detect_secret(content: str) -> bool:
    """Heuristic secret detector; a positive match rejects the write."""
    return any(p.search(content) for p in SECRET_PATTERNS)


@dataclass
class MemoryRecord:
    content: str
    type: str = "OTHER"
    status: str = "ACTIVE"
    classification: str = "STATED"
    source_kind: str = "OWNER"
    source_ref: str = ""
    captured_at: Optional[str] = None
    confidence: str = "MEDIUM"
    project: Optional[str] = None
    task: Optional[str] = None
    tags: list = field(default_factory=list)
    sensitivity: str = "INTERNAL"
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    related_memories: list = field(default_factory=list)
    conflict_refs: list = field(default_factory=list)
    memory_id: str = field(default_factory=new_memory_id)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def validate(self) -> None:
        if not self.content or not self.content.strip():
            raise ValueError("memory content must be non-empty")
        if self.type not in TYPES:
            raise ValueError(f"invalid type: {self.type}")
        if self.status not in STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        if self.classification not in CLASSIFICATIONS:
            raise ValueError(f"invalid classification: {self.classification}")
        if self.source_kind not in SOURCE_KINDS:
            raise ValueError(f"invalid source kind: {self.source_kind}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"invalid confidence: {self.confidence}")
        if self.sensitivity not in SENSITIVITY_LEVELS:
            raise ValueError(f"invalid sensitivity: {self.sensitivity}")
        if not self.source_ref.strip():
            raise ValueError("source_ref (provenance) is required")
        if detect_secret(self.content):
            raise ValueError("content rejected: looks like a secret/credential")

    def to_dict(self) -> dict:
        return {
            "memory_id": self.memory_id,
            "content": self.content,
            "type": self.type,
            "status": self.status,
            "classification": self.classification,
            "source": {
                "kind": self.source_kind,
                "ref": self.source_ref,
                "captured_at": self.captured_at or utc_now(),
            },
            "confidence": self.confidence,
            "project": self.project,
            "task": self.task,
            "tags": list(self.tags),
            "sensitivity": self.sensitivity,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "related_memories": list(self.related_memories),
            "conflict_refs": list(self.conflict_refs),
            "created_at": self.created_at or utc_now(),
            "updated_at": self.updated_at or utc_now(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "MemoryRecord":
        src = d.get("source", {})
        rec = cls(
            content=d["content"],
            type=d.get("type", "OTHER"),
            status=d.get("status", "ACTIVE"),
            classification=d.get("classification", "STATED"),
            source_kind=src.get("kind", "CONVERSATION"),
            source_ref=src.get("ref", ""),
            captured_at=src.get("captured_at"),
            confidence=d.get("confidence", "UNKNOWN"),
            project=d.get("project"),
            task=d.get("task"),
            tags=list(d.get("tags", [])),
            sensitivity=d.get("sensitivity", "INTERNAL"),
            valid_from=d.get("valid_from"),
            valid_until=d.get("valid_until"),
            related_memories=list(d.get("related_memories", [])),
            conflict_refs=list(d.get("conflict_refs", [])),
            memory_id=d["memory_id"],
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )
        if rec.status not in STATUSES or rec.source_kind not in SOURCE_KINDS:
            # tolerate legacy/unknown enum values rather than crash on load
            pass
        return rec
