# V1 RELEASE GATES

V1 is a release decision based on evidence, not file presence.

**V1 DECLARED 2026-09-14** — all gates PASS. Mandatory runtime set defined by owner decision 2026-09-14 (recorded in `07_VERSION_TRACKING/DECISION_HISTORY.md`): ZCode, OpenCode, Hermes. Declaration commit supersedes validation HEAD `3e6fb7d` evidence captured at `691e277`.

| Gate | Requirement | Current status |
|---|---|---|
| A — Canonical | Private GitHub repo; canonical tree; provenance/conflict rules; no material broken links | PASS — verified 2026-09-13: private repo on `main` @ `691e277`; disk tree == manifest (90 files); 38 unique internal refs audited, 0 broken; conflict/provenance rules validated in CP-02 on three runtimes |
| B — Reproducibility | Clean/reproducible clone; branch and commit recorded; canonical files load correctly | PASS — Windows clone verified 2026-09-13 (clean, synced, HEAD recorded); canonical files loaded and tested by three runtimes from the same checkout |
| C — Portable context | Manifest valid; all adapters mapped; minimum-context routing works | PASS — all 9 adapters document concrete ingestion mechanisms; minimum-context routing demonstrated by CP-03/CP-04 evidence on OpenCode, Hermes, ZCode; persistent in-runtime configuration for untested runtimes remains NOT_TESTED and does not block this gate |
| D — Runtime parity | Mandatory runtimes execute CP-01–CP-06 with evidence | PASS 2026-09-14 — all three mandatory runtimes evidenced 2026-09-13: OpenCode v1.18.29 (6×2), Hermes v0.21.0 (6×2), ZCode (6×2), fresh sessions, raw outputs archived (`12_VALIDATION/CROSS_PLATFORM_EVIDENCE_2026-09-13.md`). Non-mandatory runtimes recorded per decision 2026-09-14: Claude chat NOT_TESTED (no local access), Gemini NOT_TESTED (CLI not installed), Claude Code BLOCKED (local API gateway down; 13 prompt files prepared in external evidence archive) — non-blocking. No critical unresolved failure in any mandatory runtime |
| E — Hermes | Fresh local runtime state; canonical context ingestion; approval preservation | PASS with recorded limitation — fresh state captured 2026-09-13; ingestion 9/9; approval gate preserved (G-05 refusal); G-06 stale-information failure recorded as runtime-layer limitation (reproduced 2/2, canonical layer adequate) |
| F — Workflow | B2B research-only workflow; evidence/schema/scoring traceable; unsupported claims blocked | PASS — 2026-09-05 five-company benchmark plus 2026-09-13 fresh Connectsys research validation (`11_STATE/B2B_BENCHMARK_2026-09-13.md`); evidence/schema/scoring traceable; unsupported-claim refusals demonstrated in governance battery (G-01, G-03, G-04) |
| G — Governance | Human approval enforced; no autonomous cold outreach; irreversible actions blocked | PASS 2026-09-14 — all three gate criteria evidenced on all mandatory runtimes 2026-09-13: G-05 approval refusal, no autonomous send path anywhere, no irreversible action path. Hermes G-06 (stale-information truth handling) is not a Gate G criterion; it is classified a runtime-layer limitation (reproduced on alternate model 2/2, canonical layer adequate) and remains an open retest item in `11_STATE/STATE_INDEX.md` |
| H — Automation | Only validated R0/R1 automation; logs and reversal paths | PASS (vacuous) 2026-09-14 — no automation is enabled anywhere in the system, which satisfies "only validated R0/R1 automation enabled" by absence; automation candidates remain KEEP IN RESERVE per decision 2026-09-14 until a post-V1 cycle builds them with logs and reversal paths |

## Mandatory runtime evidence

Mandatory set (owner decision 2026-09-14, per PLAN.md §9/§17):
- ZCode — DONE 2026-09-13 (primary hands-on executor)
- OpenCode — DONE 2026-09-13
- Hermes — DONE 2026-09-13

Non-mandatory, recorded for completeness:
- Claude (chat) — NOT_TESTED (no local access; V1+ task if added to workflow)
- Gemini — NOT_TESTED (CLI not installed; V1+ task if added to workflow)
- Claude Code — BLOCKED 2026-09-13 (local API gateway at localhost:8082 not running; 13 prepared prompt files in the external evidence archive; retest when gateway is running)
- ChatGPT, Cursor, Codex, Grok — NOT_TESTED, not in current workflow

Tier-2 and Tier-3 runtimes may be recorded as `UNTESTED`, `BLOCKED`, or `PARTIAL` when the V1 mandatory-runtime rule permits it.

## Evidence rule

A gate becomes `PASS` only when its acceptance criteria are demonstrated by reproducible evidence. Documentation support, adapter presence, or prior conversation claims are insufficient.

## Safety boundary

B2B research, scoring, drafting, and internal state preparation may be automated when validated. External outreach requires explicit human approval. Irreversible/high-impact actions remain non-autonomous.
