# V1 RELEASE GATES

V1 is a release decision based on evidence, not file presence.

| Gate | Requirement | Current status |
|---|---|---|
| A — Canonical | Private GitHub repo; canonical tree; provenance/conflict rules; no material broken links | PARTIAL — repository structure reconciled; final link audit and evidence review remain |
| B — Reproducibility | Clean/reproducible clone; branch and commit recorded; canonical files load correctly | NOT_TESTED from this environment |
| C — Portable context | Manifest valid; all adapters mapped; minimum-context routing works | PARTIAL — adapter mechanisms documented; runtime ingestion untested |
| D — Runtime parity | Mandatory runtimes execute CP-01–CP-06 with evidence | NOT_TESTED |
| E — Hermes | Fresh local runtime state; canonical context ingestion; approval preservation | NOT_TESTED |
| F — Workflow | B2B research-only workflow; evidence/schema/scoring traceable; unsupported claims blocked | PARTIAL — five-company research benchmark exists; fresh runtime benchmark pending |
| G — Governance | Human approval enforced; no autonomous cold outreach; irreversible actions blocked | NOT_TESTED in runtime |
| H — Automation | Only validated R0/R1 automation; logs and reversal paths | NOT_STARTED — correctly blocked until earlier gates pass |

## Mandatory runtime evidence

Before V1, the required Tier-1 runtime evidence is:
- OpenCode
- Hermes
- Claude
- Gemini

Tier-2 and Tier-3 runtimes may be recorded as `UNTESTED`, `BLOCKED`, or `PARTIAL` when the V1 mandatory-runtime rule permits it.

## Evidence rule

A gate becomes `PASS` only when its acceptance criteria are demonstrated by reproducible evidence. Documentation support, adapter presence, or prior conversation claims are insufficient.

## Safety boundary

B2B research, scoring, drafting, and internal state preparation may be automated when validated. External outreach requires explicit human approval. Irreversible/high-impact actions remain non-autonomous.