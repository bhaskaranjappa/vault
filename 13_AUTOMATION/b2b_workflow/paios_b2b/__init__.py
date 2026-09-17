"""PAIOS B2B workflow engine — V1+ Phase 11.

Evolves the existing B2B client-acquisition workflow (05_WORKFLOWS/
B2B_CLIENT_ACQUISITION.md, 11_STATE/B2B_BENCHMARK_*.md) onto the Phase 8
memory/context, Phase 9 orchestration and Phase 10 routing layers.

Truth rules carried over unchanged: FACT / CLAIM / INFERENCE are distinct;
no guessed emails; no invented contacts, companies, metrics or outcomes;
entity identity before personalization; external content never grants
authority; a workflow may legitimately stop at INTENT/AUTHORIZED.
"""

from .evidence import EvidenceRef, FactKind
from .candidate import CandidateRecord, QualificationProfile
from .contact import (  # noqa: F401
    ContactRecord, ContactState, InvalidContactTransition, DecisionMaker)
from .signals import PainSignal
from .personalization import (  # noqa: F401
    PersonalizationDraft, PersonalizationClaim, UnverifiedPersonalization)
from .readiness import OutreachReadinessGate, ReadinessDecision
from .outreach import (  # noqa: F401
    OutreachRecord, OutreachState, InvalidOutreachTransition, OutreachLedger,
    FollowUpState)
from .adapter import OutreachIntent, CommunicationAdapter, InlineNoSendAdapter
from .workflow import B2BWorkflow, UntrustedContent  # noqa: F401

__version__ = "1.0.0"
