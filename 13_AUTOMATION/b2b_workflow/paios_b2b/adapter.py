"""Execution boundary (Phase 11 §14, §22).

The workflow NEVER contains provider-specific sending logic. Chain:
  OutreachIntent -> Router -> Authorized Communication Adapter -> Execution
                 -> Execution Verification

States stay separate: INTENT / AUTHORIZED / EXECUTED / VERIFIED. A workflow
may finish research without ever reaching EXECUTED. The reference adapter
sends nothing — it exists so the portable workflow can be tested without any
real outreach. A real adapter must be policy-authorized AND provide an
execution verification receipt; without one, status cannot become SENT.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OutreachIntent:
    outreach_id: str
    company_id: str
    contact_id: str
    channel: str
    message_ref: str
    authority_scope: str          # copied from the readiness-approved record
    intent_state: str = "INTENT"  # INTENT | AUTHORIZED | EXECUTED | VERIFIED

    def authorize(self, authority_scope: str) -> None:
        if not authority_scope or authority_scope == "unauthorized":
            raise PermissionError("authorization requires a real policy scope")
        self.authority_scope = authority_scope
        self.intent_state = "AUTHORIZED"


@dataclass
class ExecutionReceipt:
    adapter_id: str
    outreach_id: str
    delivered: bool
    provider_ref: Optional[str]          # provider message id, if any
    detail: str = ""
    verified: bool = False               # True only after independent verification

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class CommunicationAdapter:
    """Base adapter: refuses to execute (portable boundary)."""

    adapter_id = "abstract"

    def execute(self, intent: OutreachIntent) -> ExecutionReceipt:
        raise NotImplementedError(
            f"{self.adapter_id} adapter does not support execution")


class InlineNoSendAdapter(CommunicationAdapter):
    """Reference adapter used by tests and research-only runs. It NEVER sends
    anything and always reports not-delivered, so a test cannot accidentally
    claim SENT."""

    adapter_id = "inline-nosend"

    def execute(self, intent: OutreachIntent) -> ExecutionReceipt:
        if intent.intent_state != "AUTHORIZED":
            raise PermissionError("intent must be AUTHORIZED before execution")
        return ExecutionReceipt(
            adapter_id=self.adapter_id, outreach_id=intent.outreach_id,
            delivered=False, provider_ref=None,
            detail="no-send adapter: intent recorded, nothing transmitted",
            verified=False)
