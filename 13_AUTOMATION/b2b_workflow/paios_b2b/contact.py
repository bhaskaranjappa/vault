"""Decision-maker identification and contact verification (Phase 11 §6-7).

Lifecycle: DISCOVERED -> UNVERIFIED -> VERIFIED | INVALID | STALE.
A guessed email is never VERIFIED. A scraped contact is not automatically
VERIFIED. Role currency requires a fresh source — stale roles block outreach.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from .evidence import EvidenceRef


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ContactState:
    DISCOVERED = "DISCOVERED"
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    INVALID = "INVALID"
    STALE = "STALE"
    ALL = (DISCOVERED, UNVERIFIED, VERIFIED, INVALID, STALE)

    TRANSITIONS = {
        DISCOVERED: {UNVERIFIED, VERIFIED, INVALID, STALE},
        UNVERIFIED: {VERIFIED, INVALID, STALE},
        VERIFIED: {STALE, INVALID},
        STALE: {VERIFIED, INVALID},      # re-verification path
        INVALID: set(),
    }


class InvalidContactTransition(Exception):
    pass


def _guess_pattern_local_part(email: str, full_name: str) -> bool:
    """Detect first.last / flast / first_initial+last style local parts —
    i.e. an email that could have been guessed from a naming convention."""
    import re
    local = email.split("@")[0].lower().replace(".", "").replace("_", "").replace("-", "")
    parts = re.findall(r"[A-Za-z]+", full_name.lower())
    if not parts:
        return False
    first, last = parts[0], parts[-1]
    candidates = {first + last, first[0] + last, last, first, last + first[0]}
    return local in candidates


@dataclass
class ContactRecord:
    contact_id: str
    company_id: str
    channel_type: str                       # email | linkedin | careers_form | other
    channel_value: str                      # the address/handle/form URL
    state: str = ContactState.DISCOVERED
    full_name: Optional[str] = None
    evidence: list = field(default_factory=list)   # EvidenceRef list
    verification: Optional[str] = None      # description of HOW it was verified
    guessed: bool = False                   # True if pattern-guessed, never verifiable by pattern
    captured_at: Optional[str] = None

    @staticmethod
    def new_id() -> str:
        return "CT-" + uuid.uuid4().hex[:10]

    def __post_init__(self):
        self.captured_at = self.captured_at or _now()
        if self.channel_type not in ("email", "linkedin", "careers_form", "other"):
            raise ValueError(f"invalid channel_type: {self.channel_type}")
        if self.state not in ContactState.ALL:
            raise ValueError(f"invalid contact state: {self.state}")

    def transition(self, new_state: str, ref: EvidenceRef,
                   verification: str | None = None) -> None:
        if new_state not in ContactState.TRANSITIONS[self.state]:
            raise InvalidContactTransition(
                f"invalid contact transition {self.state} -> {new_state}")
        if new_state == ContactState.VERIFIED:
            if self.guessed:
                raise InvalidContactTransition(
                    "a pattern-guessed contact can never be VERIFIED by pattern alone")
            if self.channel_type == "email" and self.full_name and \
                    _guess_pattern_local_part(self.channel_value, self.full_name) and \
                    not (verification or "").strip():
                raise InvalidContactTransition(
                    "email matches a naming-convention pattern; explicit verification "
                    "evidence (e.g. source page listing the address) is required")
            if not verification or not verification.strip():
                raise InvalidContactTransition(
                    "VERIFIED requires a description of the verification evidence")
        self.state = new_state
        self.evidence.append(ref)
        if verification:
            self.verification = verification

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["evidence"] = [e.to_dict() for e in self.evidence]
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ContactRecord":
        rec = cls(**{k: v for k, v in d.items()
                     if k in cls.__dataclass_fields__ and k != "evidence"})
        rec.evidence = [EvidenceRef.from_dict(e) for e in d.get("evidence", [])]
        return rec


@dataclass
class DecisionMaker:
    """A person record. Role currency is separate from identity: a role
    sourced from an old page must not be treated as the CURRENT role."""
    person_id: str
    name: str
    company_id: str
    role_title: Optional[str] = None
    role_source: Optional[str] = None          # EvidenceRef source
    role_source_date: Optional[str] = None
    role_current: bool = False                 # True only with a fresh, current source
    confidence: str = "MEDIUM"
    verification: str = "UNVERIFIED"           # UNVERIFIED | VERIFIED
    evidence: list = field(default_factory=list)

    @staticmethod
    def new_id() -> str:
        return "PR-" + uuid.uuid4().hex[:10]

    def add_evidence(self, ref: EvidenceRef, *, role_current: bool = False) -> None:
        self.evidence.append(ref)
        self.role_source = ref.source
        self.role_source_date = ref.captured_at
        self.role_current = role_current

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["evidence"] = [e.to_dict() for e in self.evidence]
        return d
