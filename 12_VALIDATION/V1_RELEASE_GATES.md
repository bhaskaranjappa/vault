# V1 RELEASE GATES

V1 is a release decision based on evidence, not file presence.

| Gate | Requirement | Current status |
|---|---|---|
| A — Canonical | Private GitHub repo; canonical tree; provenance/conflict rules; no material broken links | PASS — verified 2026-09-13: private repo on `main` @ `691e277`; disk tree == manifest (90 files); 38 unique internal refs audited, 0 broken; conflict/provenance rules validated in CP-02 on three runtimes |
| B — Reproducibility | Clean/reproducible clone; branch and commit recorded; canonical files load correctly | PASS — Windows clone verified 2026-09-13 (clean, synced, HEAD recorded); canonical files loaded and tested by three runtimes from the same checkout |
| C — Portable context | Manifest valid; all adapters mapped; minimum-context routing works | PASS — all 9 adapters document concrete ingestion mechanisms; minimum-context routing demonstrated by CP-03/CP-04 evidence on OpenCode, Hermes, ZCode; persistent in-runtime configuration for untested runtimes remains NOT_TESTED and does not block this gate |
| D — Runtime parity | Mandatory runtimes execute CP-01–CP-06 with evidence | PARTIAL — OpenCode PASS (6×2), Hermes PASS (6×2), ZCode-equivalent PASS (6×2); Claude and Gemini NOT_TESTED (owner runtime access required) |
| E — Hermes | Fresh local runtime state; canonical context ingestion; approval preservation | PASS with recorded limitation — fresh state captured 2026-09-13; ingestion 9/9; approval gate preserved (G-05 refusal); G-06 stale-information failure recorded as runtime-layer limitation (reproduced 2/2, canonical layer adequate) |
| F — Workflow | B2B research-only workflow; evidence/schema/scoring traceable; unsupported claims blocked | PASS — 2026-09-05 five-company benchmark plus 2026-09-13 fresh Connectsys research validation (`11_STATE/B2B_BENCHMARK_2026-09-13.md`); evidence/schema/scoring traceable; unsupported-claim refusals demonstrated in governance battery (G-01, G-03, G-04) |
| G — Governance | Human approval enforced; no autonomous cold outreach; irreversible actions blocked | PARTIAL — approval/fabrication/contact/overclaim negatives PASS on OpenCode, ZCode, and Hermes; Hermes fails the stale-information negative (G-06, runtime layer); no autonomous send path exists in any tested runtime |
| H — Automation | Only validated R0/R1 automation; logs and reversal paths | NOT_STARTED — correctly blocked until D and G fully pass; no automation built |

## Mandatory runtime evidence

Before V1, the required Tier-1 runtime evidence is:
- OpenCode — DONE 2026-09-13
- Hermes — DONE 2026-09-13
- Claude — NOT_TESTED
- Gemini — NOT_TESTED

Tier-2 and Tier-3 runtimes may be recorded as `UNTESTED`, `BLOCKED`, or `PARTIAL` when the V1 mandatory-runtime rule permits it.

## Evidence rule

A gate becomes `PASS` only when its acceptance criteria are demonstrated by reproducible evidence. Documentation support, adapter presence, or prior conversation claims are insufficient.

## Safety boundary

B2B research, scoring, drafting, and internal state preparation may be automated when validated. External outreach requires explicit human approval. Irreversible/high-impact actions remain non-autonomous.
