# PAIOS B2B Workflow Engine — Implementation Notes

Portable, runtime-independent B2B GenAI client-acquisition workflow engine
(`paios_b2b`, stdlib-only). It extends the canonical B2B workflow
(`05_WORKFLOWS/B2B_CLIENT_ACQUISITION.md`) with executable, evidence-backed
state machines integrated with the Phase 8 memory/context, Phase 9
orchestration, and Phase 10 routing layers. It does not replace the canonical
protocols and does not duplicate them.

## Architecture

```
B2B Objective
  → Task Contract (Phase 9 orchestrator)
  → Evidence-Backed Discovery (candidate.py + evidence.py)
  → Qualification (QualificationProfile)
  → Decision-Maker Identification (contact.py DecisionMaker)
  → Contact Verification (ContactRecord lifecycle)
  → Personalization (personalization.py)
  → Authority Check (workflow.authorize_outreach)
  → Authorized Execution (adapter.py — runtime boundary)
  → Verification (ExecutionReceipt)
  → Outreach State (outreach.py ledger)
  → Follow-up (FollowUpState)
```

## Modules

| Module | Responsibility |
|--------|----------------|
| `evidence.py` | `EvidenceRef` provenance + `FactKind` (FACT/CLAIM/INFERENCE distinct) |
| `candidate.py` | `CandidateRecord` (identity, sources, ambiguity), `QualificationProfile` (evidence-backed dimensions, no universal score) |
| `contact.py` | `ContactRecord` (DISCOVERED/UNVERIFIED/VERIFIED/INVALID/STALE; guessed email cannot reach VERIFIED), `DecisionMaker` (role currency) |
| `signals.py` | `PainSignal` — only evidence-backed signals; kind preserved |
| `personalization.py` | `PersonalizationDraft`/`PersonalizationClaim`; claims without evidence raise `UnverifiedPersonalization` |
| `readiness.py` | `OutreachReadinessGate` — identity/contact/dm/personalization/authority/policy/duplicate checks → READY or NOT_READY with reasons |
| `outreach.py` | `OutreachRecord` 10-state machine, durable `OutreachLedger` with `duplicate_status()`, `FollowUpState` |
| `adapter.py` | `CommunicationAdapter` boundary; `InlineNoSendAdapter` reference adapter that can never deliver |
| `workflow.py` | Facade: identity establishment (source-count based), merge refusal, untrusted-content filter, authority enforcement, execution, follow-up scheduling |

## Key invariants

- **Evidence before personalization.** A draft claim with an evidence-less
  source cannot validate.
- **Scrape ≠ verification; pattern ≠ verification.** Contact `VERIFIED`
  requires explicit verification evidence; guessed emails are rejected.
- **Authority is an input**, never derived from lead data, retrieved content,
  or tool output. `authorize_outreach` refuses on unauthorized scope.
- **A draft is never SENT.** SENT/DELIVERED require an adapter execution
  verification receipt; failure receipts leave FAILED with evidence.
- **Injection is data, never instruction.** Retrieved content matching
  instruction markers raises `UntrustedContent` and is logged to
  `rejected_content.jsonl`.
- **Same-name companies never merge** without a shared domain (or evidenced
  relationship).

## Integration

- **Phase 8:** context packages built with `SELECTED` inheritance only; the
  workflow stores durable verified facts, not search noise (see B2B-16).
- **Phase 9:** parallel company research via orchestrator tasks/workers with
  bounded scopes; parent acceptance requires per-worker evidence (B2B-18).
- **Phase 10:** each workflow stage routes through its own
  `TaskCapabilityProfile` (discovery vs personalization etc.); route results
  are recorded per task (B2B-17).

## Persistence

Candidates live in `<root>/candidates.json`; outreach records in
`<root>/outreach/OUT-*.json`; rejected untrusted content in
`rejected_content.jsonl`. A fresh `B2BWorkflow(root)` reconstructs full state
from disk.

## Runtime adapter boundary

The engine contains no provider-specific sending logic. A real execution
adapter must be supplied and authorized by owner policy; until then the
workflow legitimately ends at AUTHORIZED (research-complete, not executed).
