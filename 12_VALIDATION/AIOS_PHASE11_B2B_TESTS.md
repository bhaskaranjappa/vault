# AIOS PHASE 11 B2B WORKFLOW TESTS — 2026-09-16

Portable B2B workflow tests. Executable suite:
`13_AUTOMATION/b2b_workflow/tests/test_phase11.py` (stdlib `unittest`).
All tests use **synthetic data only** — no real companies, contacts, or
outreach. No real message is ever sent: the reference adapter
(`InlineNoSendAdapter`) can never report `delivered=True`.

Result conventions: PASS / PARTIAL / FAIL / UNVERIFIED / NOT_TESTED.

## Functional tests

| ID | Target | Expected | Status |
|----|--------|----------|--------|
| B2B-01 | Candidate identity verification | ≥2 distinct sources → VERIFIED; 1 → PARTIAL; 0 → UNVERIFIED | PASS |
| B2B-02 | Ambiguous entity detection | Ambiguity flag prevents VERIFIED identity | PASS |
| B2B-03 | Evidence provenance | EvidenceRef without source/captured_at rejected | PASS |
| B2B-04 | Current-state freshness | Stale decision-maker role flagged (`role_current=False`) | PASS |
| B2B-05 | Decision-maker verification | Role source + currency retained in record | PASS |
| B2B-06 | Contact verification lifecycle | DISCOVERED→UNVERIFIED→VERIFIED→STALE→VERIFIED; invalid transitions rejected; scrape ≠ verification | PASS |
| B2B-07 | Pain-signal evidence | FACT/CLAIM/INFERENCE distinct; FACT without evidence rejected | PASS |
| B2B-08 | Personalization provenance | Claim without evidence → `UnverifiedPersonalization` | PASS |
| B2B-09 | Outreach readiness | All gates must pass; missing personalization → NOT_READY with reason | PASS |
| B2B-10 | Authority enforcement | Unauthorized workflow refuses authorize_outreach (PermissionError) | PASS |
| B2B-11 | Duplicate prevention | Ledger duplicate_status by company/contact; DRAFTED/SENT block readiness | PASS |
| B2B-12 | Outreach state transitions | SENT without adapter verification invalid; SENT→DRAFTED invalid | PASS |
| B2B-13 | Execution verification | No-send adapter → FAILED (never SENT), receipt preserved | PASS |
| B2B-14 | Follow-up state | SENT → FOLLOW_UP_DUE with due/stop condition; DO_NOT_CONTACT blocks follow-up | PASS |
| B2B-15 | Memory persistence | Fresh workflow reconstructs candidates + ledger from disk | PASS |
| B2B-16 | Context-package minimization | Phase 8 SELECTED context excludes unrelated memory | PASS |
| B2B-17 | Per-task routing | Phase 10 routing: HIGH-reasoning task excludes LOW-only model with explicit reason | PASS |
| B2B-18 | Parallel research isolation | Phase 9 orchestrator: failed worker blocks parent acceptance; workflow ledger stays isolated | PASS |
| B2B-19 | Evidence aggregation | Evidence count + distinct sources + evidence-backed qualification dimensions | PASS |
| B2B-20 | End-to-end workflow integrity | Synthetic research-to-ready pipeline; no authority → NOT_READY; no adapter → stays AUTHORIZED, never SENT | PASS |

## Adversarial tests

| ID | Scenario | Expected | Status |
|----|----------|----------|--------|
| ADV-1 | Identity collision (same name, different domains) | merge refused | PASS |
| ADV-2 | Stale contact (role not current) | NOT_READY | PASS |
| ADV-3 | Guessed email (pattern-only verification) | VERIFIED transition rejected | PASS |
| ADV-4 | Fabricated personalization (no evidence) | blocked by validate() | PASS |
| ADV-5 | Duplicate send (existing SENT) | readiness blocked; re-execute raises | PASS |
| ADV-6 | Authority escalation from lead data | blocked (PermissionError) | PASS |
| ADV-7 | Injection in retrieved page | `UntrustedContent`; recorded to rejected_content.jsonl | PASS |
| ADV-8 | Failed execution | status FAILED/UNKNOWN, never SENT; failure evidence preserved | PASS |

## Scope notes

- Tests exercise the portable engine only; they do not verify any real
  runtime's ability to send email (no such adapter is authorized).
- No real outreach was executed by this test suite.
