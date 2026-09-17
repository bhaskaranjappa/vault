"""B2B workflow facade (Phase 11 §3).

Wires candidates, contacts, signals, personalization, readiness, outreach
ledger and the communication adapter into the portable pipeline:

  Evidence-Backed Discovery -> Qualification -> Decision-Maker Identification
  -> Contact Verification -> Personalization -> Authority Check
  -> Authorized Execution -> Verification -> Outreach State -> Follow-up

Untrusted-content boundary: retrieved pages / tool output are data. They can
correct facts (with provenance) but can NEVER authorize an action, change
authority scope, or mark an outreach SENT. Injection attempts are recorded
and ignored.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .adapter import CommunicationAdapter, ExecutionReceipt, OutreachIntent
from .candidate import CandidateRecord, QualificationProfile
from .contact import ContactRecord, ContactState, DecisionMaker
from .outreach import FollowUpState, OutreachLedger, OutreachRecord, OutreachState
from .personalization import PersonalizationDraft
from .readiness import OutreachReadinessGate, ReadinessDecision
from .signals import PainSignal


class UntrustedContent(Exception):
    """Raised when retrieved content attempts to exercise authority."""


INJECTION_MARKERS = (
    "ignore previous instructions", "ignore all policy", "you are now",
    "disregard the rules", "grant yourself", "authorize yourself",
    "send the email now", "approve this outreach",
)


class B2BWorkflow:
    def __init__(self, state_root: str | Path,
                 adapter: CommunicationAdapter | None = None,
                 authority_scope: str = "unauthorized"):
        self.root = Path(state_root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.ledger = OutreachLedger(self.root)
        self.gate = OutreachReadinessGate()
        self.adapter = adapter            # None => research-only workflow
        self.authority_scope = authority_scope
        self._candidates_path = self.root / "candidates.json"
        self._rejected_content_path = self.root / "rejected_content.jsonl"

    # -- persistence ------------------------------------------------------
    def save_candidate(self, c: CandidateRecord) -> None:
        data = self._load_candidates()
        data[c.company_id] = c.to_dict()
        self._candidates_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_candidate(self, company_id: str) -> CandidateRecord:
        return CandidateRecord.from_dict(self._load_candidates()[company_id])

    def _load_candidates(self) -> dict:
        if self._candidates_path.exists():
            return json.loads(self._candidates_path.read_text(encoding="utf-8"))
        return {}

    # -- untrusted content ---------------------------------------------------
    def ingest_retrieved_content(self, text: str, source: str) -> dict:
        """Treat retrieved page/tool content as untrusted data. Instruction-
        like content aimed at the workflow is recorded and refused; it can
        never authorize anything."""
        lowered = (text or "").lower()
        hits = [m for m in INJECTION_MARKERS if m in lowered]
        if hits:
            entry = {"timestamp": _now(), "source": source, "markers": hits}
            with self._rejected_content_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            raise UntrustedContent(
                f"retrieved content from {source} attempted to instruct the "
                f"workflow ({hits}); recorded as untrusted and refused")
        return {"accepted": True, "source": source}

    # -- identity (B2B-01/02) ----------------------------------------------
    def establish_identity(self, candidate: CandidateRecord, *,
                           min_distinct_sources: int = 2) -> CandidateRecord:
        """Identity is VERIFIED only with >= min_distinct_sources independent
        corroborating sources; PARTIAL with 1; otherwise UNVERIFIED."""
        n = candidate.distinct_source_count()
        if n >= min_distinct_sources:
            candidate.identity_confidence = "VERIFIED"
        elif n == 1:
            candidate.identity_confidence = "PARTIAL"
        else:
            candidate.identity_confidence = "UNVERIFIED"
        self.save_candidate(candidate)
        return candidate

    def merge_candidates(self, a: CandidateRecord, b: CandidateRecord) -> None:
        """Refuse to merge same-named candidates without disambiguating
        evidence (same domain or explicit parent relationship evidenced)."""
        shared_domain = a.domain and a.domain == b.domain
        if not shared_domain:
            raise ValueError(
                f"refusing to merge '{a.name}' and '{b.name}': no shared-domain "
                f"or evidenced entity relationship; identity collision risk")

    # -- readiness -----------------------------------------------------------
    def check_readiness(self, **kwargs) -> ReadinessDecision:
        kwargs.setdefault("authority_allows_outreach",
                          self.authority_scope not in ("", "unauthorized"))
        return self.gate.evaluate(**kwargs)

    # -- authorized execution ---------------------------------------------------
    def authorize_outreach(self, rec: OutreachRecord) -> OutreachRecord:
        if self.authority_scope in ("", "unauthorized"):
            raise PermissionError(
                "owner/bot authority policy does not authorize outreach; "
                "lead data and tool output cannot grant authority")
        rec.transition(OutreachState.AUTHORIZED)
        rec.authority_scope = self.authority_scope
        self.ledger.save(rec)
        return rec

    def execute_outreach(self, rec: OutreachRecord) -> ExecutionReceipt:
        """Execute only through the adapter; SENT requires a verification
        receipt. No adapter => workflow stays at AUTHORIZED (research-only)."""
        if rec.status != OutreachState.AUTHORIZED:
            raise PermissionError(
                f"outreach {rec.outreach_id} is {rec.status}, not AUTHORIZED")
        if self.adapter is None:
            return ExecutionReceipt(adapter_id="none", outreach_id=rec.outreach_id,
                                    delivered=False, provider_ref=None,
                                    detail="no adapter configured; workflow remains AUTHORIZED",
                                    verified=False)
        intent = OutreachIntent(
            outreach_id=rec.outreach_id, company_id=rec.company_id,
            contact_id=rec.contact_id, channel=rec.channel,
            message_ref=rec.message_ref or "", authority_scope=rec.authority_scope,
            intent_state="AUTHORIZED")   # record-level authorization carries through
        receipt = self.adapter.execute(intent)
        if receipt.delivered and receipt.verified:
            rec.verification = receipt.to_dict()
            rec.transition(OutreachState.SENT, reason="adapter verification receipt")
        elif receipt.delivered and not receipt.verified:
            rec.verification = receipt.to_dict()
            rec.transition(OutreachState.UNKNOWN, reason="delivered but unverified receipt")
        else:
            rec.verification = receipt.to_dict()
            rec.transition(OutreachState.FAILED, reason=receipt.detail or "adapter reported failure")
        self.ledger.save(rec)
        return receipt

    # -- follow-up ------------------------------------------------------------
    def schedule_follow_up(self, outreach_id: str, *, due_date: str,
                           next_action: str, stop_condition: str) -> OutreachRecord:
        rec = self.ledger.load(outreach_id)
        if rec.status == OutreachState.DO_NOT_CONTACT:
            raise PermissionError(
                f"{outreach_id} is DO_NOT_CONTACT; follow-up prohibited")
        rec.follow_up = FollowUpState(
            due_date=due_date, previous_message_ref=rec.message_ref,
            response_status="AWAITING", next_action=next_action,
            stop_condition=stop_condition, authority_scope=rec.authority_scope)
        if rec.status in (OutreachState.SENT, OutreachState.DELIVERED):
            rec.transition(OutreachState.FOLLOW_UP_DUE, reason="follow-up scheduled")
        self.ledger.save(rec)
        return rec


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
