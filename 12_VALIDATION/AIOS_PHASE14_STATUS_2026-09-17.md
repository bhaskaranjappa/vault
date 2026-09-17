# AIOS V1+ PHASE 14 STATUS — 2026-09-17

Status: IMPLEMENTATION COMPLETE — REAL RUNTIME EXECUTION VERIFIED (Codex CLI, bounded read-only)
Phase: Real Runtime Adapter Integration

## Implementation status

- Real adapter: `13_AUTOMATION/runtime_parity/paios_runtime/zcode_adapter.py`
  (`CodexRuntimeAdapter` around the OpenAI Codex CLI)
- Docs: `13_AUTOMATION/runtime_parity/ZCODE_ADAPTER.md`
- Tests: `12_VALIDATION/AIOS_PHASE14_REAL_RUNTIME_TESTS.md` — 27/27 PASS
  (13 real-execution tests invoking the actual runtime, 6 integration,
  8 adversarial). RT-20 real failover is NOT_APPLICABLE (recorded honestly);
  the substitution mechanism passes at contract level.
- Phase 13 superseded on this single point: "REAL RUNTIME EXECUTION VERIFIED"
  now has direct observable evidence (bounded `codex exec` runs through the
  canonical adapter). All other Phase 13 statements stand unchanged.

## Real runtime boundary (verified live)

- `codex exec` (OpenAI Codex CLI 0.144.1), ChatGPT-account auth,
  model `gpt-5.5` verified; read-only sandbox, working-dir isolation,
  stdin prompt, plain/JSON output, external timeout — all directly observed.
- Real executions performed: multiple bounded read-only runs (echo probes,
  file-inspection end-to-end task, authority-echo probe, invalid-model
  failure, 1s timeout, duplicate fingerprint check). Zero repository
  mutation; sandbox write-refusal observed and verified.

## Capability lifecycle status

| Runtime | Lifecycle | Verification | Basis |
|---|---|---|---|
| codex-cli (ZCode-class) | VERIFIED | VERIFIED | direct live execution through the adapter |
| opencode | INSTALLED | CLAIMED / execution UNVERIFIED | CLI present; `opencode run` hang re-observed 2026-09-17 (exit 124, 120s, zero output) |
| grok 0.2.102 | INSTALLED | CLAIMED (auth) | installed; not signed in (real probe) |
| hermes 0.21.3 | INSTALLED | CLAIMED (auth) | installed; provider endpoint unavailable (real probe) |
| kimi 0.43.0 | INSTALLED | CLAIMED (auth) | installed; 403 quota exhausted (real probe) |
| reference-local | INSTALLED | CLAIMED | synthetic test adapter, never production |

## Phase 9/10/12 integration

- Phase 10: model route → runtime selection kept separate (RT-09) — PASS.
- Phase 9: worker through adapter boundary, ledger not bypassed (RT-10) — PASS.
- Phase 12: automation delegates through the boundary, lifecycle stays
  canonical (RT-11, AD-14-06) — PASS.

## Process-boundary persistence

Real subprocess A/B test passes (RT-18): execution result + fingerprint
written by Process A, reloaded and verified by independent Process B.

## Real failover result

NOT_APPLICABLE as real cross-runtime failover: no second VERIFIED runtime
exists. Recorded honestly; substitution mechanism proven at contract level
(RT-20). No fabricated parity.

## Regressions

Phase 8 = 17/17 · Phase 9 = 31/31 · Phase 10 = 27/27 · Phase 11 = 28/28 ·
Phase 12 = 30/30 · Phase 13 = 28/28 (incl. 8 adversarial) — all PASS.
Phase 14 = 27/27 (incl. 8 adversarial).

## Known limitations / unverified

- Only `gpt-5.5` verified on the codex boundary; account tier rejects the
  configured default model (400, observed).
- Usage metadata parsed only in JSON mode.
- No cancellation, streaming, parallelism, or background execution claimed.
- OpenCode unusable; grok/hermes/kimi unauthenticated or quota-blocked.
- No scheduler support claimed (Phase 12 limitation stands).

## Next integration step

Extend parity measurement across a second runtime once one becomes
authenticated/usable (OpenCode hang resolution, grok login, or hermes
provider recovery), then run the Phase 13 RP suite against real adapters on
both sides. Next canonical phase per PLAN.md.
