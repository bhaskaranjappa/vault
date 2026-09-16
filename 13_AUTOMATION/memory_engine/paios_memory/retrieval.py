"""Structured + lexical retrieval with deterministic relevance gating.

Implements the Phase 8 pipeline:
  query -> candidate retrieval -> relevance scoring ->
  freshness/source/conflict checks -> sensitivity filter -> threshold -> ranking

This is NOT semantic/vector retrieval. Future semantic adapters plug in by
implementing SemanticAdapter and passing it to Retriever (score_named hook);
their contribution is added as the `semantic_match` term of the same
deterministic scoring formula.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Protocol

from .records import MemoryRecord, SENSITIVITY_ORDER

# Deterministic weights (implementation-defined, documented in IMPLEMENTATION.md)
WEIGHTS = {
    "task_match": 3.0,
    "project_match": 2.0,
    "lexical_match": 3.0,
    "freshness": 1.0,
    "source_quality": 2.0,
    "confidence": 1.0,
}
PENALTIES = {
    "conflict": 1.5,
    "sensitivity_boundary": 0.5,
    "redundancy": 1.0,
}

SOURCE_QUALITY = {
    "OWNER": 1.0,
    "CANONICAL_FILE": 1.0,
    "RUNTIME": 0.8,
    "CONVERSATION": 0.5,
    "EXTERNAL_SOURCE": 0.6,
    "AGENT": 0.5,
}
CONFIDENCE_SCORE = {"HIGH": 1.0, "MEDIUM": 0.6, "LOW": 0.3, "UNKNOWN": 0.0}

TOKEN_RE = re.compile(r"[a-z0-9_]{3,}")


def tokenize(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


class SemanticAdapter(Protocol):
    """Extension point for future semantic/vector retrieval.

    Implementations return a relevance contribution in [0.0, 1.0] for a
    record against a query. Nothing in this engine depends on vectors.
    """
    name: str
    def score(self, query: str, record: MemoryRecord) -> float: ...


@dataclass
class RetrievalQuery:
    text: str
    task: Optional[str] = None
    project: Optional[str] = None
    tags: list = field(default_factory=list)
    max_sensitivity: str = "INTERNAL"
    min_relevance: float = 3.0
    top_k: int = 8
    include_conflicting: bool = True


@dataclass
class ScoredMemory:
    record: MemoryRecord
    score: float
    breakdown: dict

    def __repr__(self) -> str:  # pragma: no cover
        return f"ScoredMemory({self.record.memory_id}, {self.score:.2f})"


def _parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def freshness_score(rec: MemoryRecord, now: datetime) -> float:
    """1.0 for records captured today, decaying ~half-life 90 days."""
    ts = _parse_ts(rec.captured_at)
    if ts is None:
        return 0.0
    age_days = max(0.0, (now - ts).total_seconds() / 86400.0)
    return math.exp(-age_days / 130.0)  # ~0.5 at 90 days


class Retriever:
    def __init__(self, store, semantic_adapter: SemanticAdapter | None = None):
        self.store = store
        self.semantic_adapter = semantic_adapter

    def retrieve(self, query: RetrievalQuery, now: datetime | None = None) -> list[ScoredMemory]:
        now = now or datetime.now(timezone.utc)
        ceiling = SENSITIVITY_ORDER[query.max_sensitivity]
        q_tokens = tokenize(query.text) | {t.lower() for t in query.tags}
        seen_contents: list[set] = []
        scored: list[ScoredMemory] = []

        for rec in self.store.all_records():
            # hard filters ---------------------------------------------------
            if rec.status == "INVALIDATED":
                continue
            if rec.status == "SUPERSEDED" and not self._is_latest_conflict_chain(rec):
                # superseded records are excluded from normal retrieval;
                # they remain on disk for audit
                continue
            if not query.include_conflicting and rec.status == "CONFLICTING":
                continue
            if SENSITIVITY_ORDER[rec.sensitivity] > ceiling:
                continue
            if query.project and rec.project and rec.project != query.project:
                continue
            if query.task and rec.task and rec.task != query.task:
                continue
            if rec.valid_from and (ts := _parse_ts(rec.valid_from)) and now < ts:
                continue
            if rec.valid_until and (ts := _parse_ts(rec.valid_until)) and now > ts:
                continue

            # scoring --------------------------------------------------------
            r_tokens = tokenize(rec.content) | {t.lower() for t in rec.tags}
            overlap = q_tokens & r_tokens
            lexical = min(1.0, len(overlap) / max(1, min(len(q_tokens), 6)))
            task_match = 1.0 if (query.task and rec.task == query.task) else 0.0
            project_match = 1.0 if (query.project and rec.project == query.project) else 0.0
            semantic = 0.0
            if self.semantic_adapter is not None:
                semantic = max(0.0, min(1.0, self.semantic_adapter.score(query.text, rec)))

            breakdown = {
                "task_match": task_match * WEIGHTS["task_match"],
                "project_match": project_match * WEIGHTS["project_match"],
                "lexical_match": lexical * WEIGHTS["lexical_match"],
                "semantic_match": semantic * WEIGHTS["lexical_match"],
                "freshness": freshness_score(rec, now) * WEIGHTS["freshness"],
                "source_quality": SOURCE_QUALITY.get(rec.source_kind, 0.4) * WEIGHTS["source_quality"],
                "confidence": CONFIDENCE_SCORE.get(rec.confidence, 0.0) * WEIGHTS["confidence"],
                "conflict_penalty": -(PENALTIES["conflict"] if rec.status == "CONFLICTING" else 0.0),
                "sensitivity_penalty": -(PENALTIES["sensitivity_boundary"]
                                         if SENSITIVITY_ORDER[rec.sensitivity] == ceiling else 0.0),
            }
            # redundancy: heavily overlapping with an already-accepted record
            redundancy = 0.0
            for prev in seen_contents:
                if overlap and len(overlap & prev) / len(overlap) > 0.8:
                    redundancy = PENALTIES["redundancy"]
                    break
            breakdown["redundancy_penalty"] = -redundancy
            score = sum(breakdown.values())

            if score >= query.min_relevance:
                scored.append(ScoredMemory(rec, score, breakdown))
                seen_contents.append(r_tokens)

        scored.sort(key=lambda s: (-s.score, s.record.memory_id))
        return scored[:query.top_k]

    @staticmethod
    def _is_latest_conflict_chain(rec: MemoryRecord) -> bool:
        # Superseded records are never returned by normal retrieval.
        return False
