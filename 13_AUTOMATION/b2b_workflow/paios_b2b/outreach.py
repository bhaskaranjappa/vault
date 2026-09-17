"""Outreach records, states, duplicate prevention and follow-up (Phase 11 §12-13, §18).

Possible statuses: NOT_CONTACTED, DRAFTED, AUTHORIZED, SENT, DELIVERED,
REPLIED, FOLLOW_UP_DUE, DO_NOT_CONTACT, FAILED, UNKNOWN.
A DRAFT is never SENT. Status may only reach SENT through an execution
verification from the communication adapter, never from intent.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .evidence import EvidenceRef


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class OutreachState:
    NOT_CONTACTED = "NOT_CONTACTED"
    DRAFTED = "DRAFTED"
    AUTHORIZED = "AUTHORIZED"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    REPLIED = "REPLIED"
    FOLLOW_UP_DUE = "FOLLOW_UP_DUE"
    DO_NOT_CONTACT = "DO_NOT_CONTACT"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
    ALL = (NOT_CONTACTED, DRAFTED, AUTHORIZED, SENT, DELIVERED, REPLIED,
           FOLLOW_UP_DUE, DO_NOT_CONTACT, FAILED, UNKNOWN)

    TRANSITIONS = {
        NOT_CONTACTED: {DRAFTED, AUTHORIZED, DO_NOT_CONTACT},
        DRAFTED: {AUTHORIZED, DO_NOT_CONTACT, FAILED},
        AUTHORIZED: {SENT, FAILED, DO_NOT_CONTACT},
        SENT: {DELIVERED, FAILED, UNKNOWN, REPLIED, FOLLOW_UP_DUE},
        DELIVERED: {REPLIED, FOLLOW_UP_DUE, FAILED},
        REPLIED: set(),                       # becomes a conversation; workflow exits this ledger
        FOLLOW_UP_DUE: {SENT, DO_NOT_CONTACT, FAILED},
        DO_NOT_CONTACT: set(),
        FAILED: {DRAFTED, AUTHORIZED},        # retry path requires re-authorization
        UNKNOWN: {DRAFTED, AUTHORIZED, SENT},
    }


class InvalidOutreachTransition(Exception):
    pass


@dataclass
class FollowUpState:
    due_date: Optional[str] = None
    previous_message_ref: Optional[str] = None
    response_status: str = "AWAITING"          # AWAITING | REPLIED | DECLINED | NONE
    next_action: Optional[str] = None
    stop_condition: Optional[str] = None       # e.g. REPLIED, DECLINED, DO_NOT_CONTACT
    evidence_refs: list = field(default_factory=list)
    authority_scope: str = "unauthorized"

    def to_dict(self) -> dict:
        return dict(self.__dict__)


@dataclass
class OutreachRecord:
    outreach_id: str
    company_id: str
    contact_id: str
    task_id: Optional[str]
    channel: str
    message_ref: Optional[str]                  # draft/adapter message reference
    evidence_refs: list
    authority_scope: str
    status: str
    created_at: str
    executed_at: Optional[str] = None
    verification: Optional[dict] = None         # adapter execution verification
    follow_up: Optional[FollowUpState] = None

    @staticmethod
    def new_id() -> str:
        return "OUT-" + uuid.uuid4().hex[:10]

    def transition(self, new_status: str, *, reason: str = "") -> None:
        if new_status not in OutreachState.ALL:
            raise InvalidOutreachTransition(f"unknown outreach status: {new_status}")
        if new_status not in OutreachState.TRANSITIONS[self.status]:
            raise InvalidOutreachTransition(
                f"invalid outreach transition {self.status} -> {new_status} ({reason})")
        if new_status in (OutreachState.SENT, OutreachState.DELIVERED) and \
                not self.verification:
            raise InvalidOutreachTransition(
                "SENT/DELIVERED requires adapter execution verification")
        self.status = new_status
        if new_status == OutreachState.SENT:
            self.executed_at = self.executed_at or _now()

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["follow_up"] = self.follow_up.to_dict() if self.follow_up else None
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "OutreachRecord":
        fu = d.get("follow_up")
        rec = cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
        rec.follow_up = FollowUpState(**fu) if fu else None
        return rec


class OutreachLedger:
    """Durable outreach ledger with duplicate prevention."""

    def __init__(self, root: str | Path):
        self.dir = Path(root) / "outreach"
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, outreach_id: str) -> Path:
        return self.dir / f"{outreach_id}.json"

    def save(self, rec: OutreachRecord) -> None:
        self._path(rec.outreach_id).write_text(
            rec.to_dict().__str__() if False else __import__("json").dumps(
                rec.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    def load(self, outreach_id: str) -> OutreachRecord:
        import json
        return OutreachRecord.from_dict(
            json.loads(self._path(outreach_id).read_text(encoding="utf-8")))

    def all(self) -> list:
        import json
        out = []
        for p in sorted(self.dir.glob("OUT-*.json")):
            out.append(OutreachRecord.from_dict(json.loads(p.read_text(encoding="utf-8"))))
        return out

    def duplicate_status(self, *, company_id: str | None = None,
                         contact_id: str | None = None,
                         channel_value: str | None = None) -> str:
        """Current effective outreach state for the most specific match."""
        matches = [r for r in self.all()
                   if (company_id and r.company_id == company_id)
                   or (contact_id and r.contact_id == contact_id)
                   or (channel_value and getattr(r, "channel", None) == channel_value)]
        if not matches:
            return OutreachState.NOT_CONTACTED
        latest = max(matches, key=lambda r: r.created_at)
        return latest.status

    def create(self, *, company_id: str, contact_id: str, task_id: str | None,
               channel: str, message_ref: str | None, evidence_refs: list,
               authority_scope: str = "unauthorized") -> OutreachRecord:
        rec = OutreachRecord(
            outreach_id=OutreachRecord.new_id(), company_id=company_id,
            contact_id=contact_id, task_id=task_id, channel=channel,
            message_ref=message_ref, evidence_refs=list(evidence_refs),
            authority_scope=authority_scope, status=OutreachState.NOT_CONTACTED,
            created_at=_now())
        self.save(rec)
        return rec
