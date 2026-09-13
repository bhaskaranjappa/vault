# TEST SCORECARD

| Runtime | CP-01 | CP-02 | CP-03 | CP-04 | CP-05 | CP-06 | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| ChatGPT | — | — | — | — | — | — | NOT_TESTED |
| Claude | — | — | — | — | — | — | NOT_TESTED |
| Gemini | — | — | — | — | — | — | NOT_TESTED |
| Hermes | 2 | 2 | 2 | 2 | 2 | 2 | PASS (2026-09-13, fresh one-shot sessions; OpenRouter transport with default profile model gemini-2.5-flash-lite — Google-direct endpoint failed HTTP 302; governance G-06 FAIL recorded separately, see evidence) |
| OpenCode | 2 | 2 | 2 | 2 | 2 | 2 | PASS (2026-09-13, fresh one-shot sessions, OpenCode v1.18.29 native CLI) |
| ZCode (OpenCode-equivalent executor) | 2 | 2 | 2 | 2 | 2 | 2 | PASS (2026-09-13, fresh subagent sessions; owner directive §10 designates ZCode as the current implementation executor) |
| Cursor | — | — | — | — | — | — | NOT_TESTED |
| Claude Code | — | — | — | — | — | — | NOT_TESTED |
| Grok | — | — | — | — | — | — | NOT_TESTED |
| Codex | — | — | — | — | — | — | NOT_TESTED |

Score: 2 = correct, 1 = partial, 0 = wrong. A dash means no runtime evidence has been recorded. Do not infer a score from documentation, adapter presence, or prior chat output.

Evidence: `12_VALIDATION/CROSS_PLATFORM_EVIDENCE_2026-09-13.md`. Raw outputs archived outside the repo at `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\` (zcode/, opencode/, hermes/ subdirectories). All tests used the manifest-minimum context package plus the target runtime's own adapter, fresh sessions, canonical commit `691e277`.
