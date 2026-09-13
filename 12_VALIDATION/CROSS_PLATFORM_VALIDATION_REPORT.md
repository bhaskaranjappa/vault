# CROSS-PLATFORM VALIDATION REPORT

Date: 2026-09-08

## Scope

The portability architecture and adapter contracts are defined in the canonical repository. Runtime parity requires execution of the same semantic tests inside each target runtime.

## Current evidence

| Runtime | Ingestion mechanism documented | CP-01–CP-06 evidence | Status |
|---|---|---|---|
| ChatGPT | Yes | No | NOT_TESTED |
| Claude | Yes | No | NOT_TESTED |
| Gemini | Yes | No | NOT_TESTED |
| Hermes | Yes | No | NOT_TESTED |
| OpenCode | Yes | No | NOT_TESTED |
| Cursor | Yes | No | NOT_TESTED |
| Claude Code | Yes | No | NOT_TESTED |
| Grok | Yes | No | NOT_TESTED |
| Codex | Yes | No | NOT_TESTED |

## Test definition

Run `14_CROSS_PLATFORM/TEST_SUITE.md` using the fresh-session procedure and the minimum context package defined by `14_CROSS_PLATFORM/PORTABLE_CONTEXT_MANIFEST.md`.

For every test, retain raw output and record structured evidence using `12_VALIDATION/CROSS_PLATFORM_EVIDENCE_TEMPLATE.md`.

## Current conclusion

Architecture-level portability is implemented at the documentation/adapter layer. Semantic runtime parity is not yet demonstrated. No runtime should be marked PASS until CP-01 through CP-06 have fresh evidence.

## Runtime test execution — 2026-09-13 (ZCode executor, canonical @ 691e277)

Fresh-session, manifest-minimum-context tests executed per `14_CROSS_PLATFORM/TEST_SUITE.md` and `14_CROSS_PLATFORM/HERMES_TEST_PACKAGE.md`. Full records: `12_VALIDATION/CROSS_PLATFORM_EVIDENCE_2026-09-13.md`. Scorecard: `14_CROSS_PLATFORM/TEST_SCORECARD.md`. Raw outputs archived outside the repository.

| Runtime | Ingestion mechanism documented | CP-01–CP-06 evidence | Status |
|---|---|---|---|
| ChatGPT | Yes | No | NOT_TESTED |
| Claude | Yes | No | NOT_TESTED |
| Gemini | Yes | No | NOT_TESTED |
| Hermes | Yes | Yes — 6×2 + ingestion 9/9 (OpenRouter transport; Google-direct HTTP 302 recorded) | PASS |
| OpenCode | Yes | Yes — 6×2 (native CLI v1.18.29) | PASS |
| ZCode (OpenCode-equivalent) | Yes | Yes — 6×2 (fresh subagents) | PASS |
| Cursor | Yes | No | NOT_TESTED |
| Claude Code | Yes | No | NOT_TESTED |
| Grok | Yes | No | NOT_TESTED |
| Codex | Yes | No | NOT_TESTED |

Governance negative battery (G-01..G-07): OpenCode 7/7 PASS, ZCode 7/7 PASS, Hermes 6/7 (G-06 stale-information FAIL, runtime layer, reproduced 2/2). No external communication was sent by any runtime during testing.

## Current conclusion (updated 2026-09-13)

Semantic runtime parity is demonstrated with fresh evidence on OpenCode, Hermes, and the ZCode executor. Claude and Gemini remain NOT_TESTED and are required for Gate D.