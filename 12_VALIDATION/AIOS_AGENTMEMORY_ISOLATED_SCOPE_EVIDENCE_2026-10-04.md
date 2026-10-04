# EVALUATION EVIDENCE — agentmemory isolated agent scope (follow-up, 2026-10-04)

Status: EVALUATION ONLY — no PAIOS integration, no architecture change, no new runtime dependency.
Supersedes nothing; extends `12_VALIDATION/AIOS_AGENTMEMORY_EVAL_EVIDENCE_2026-10-03.md` (kept intact).
Question: can agentmemory's agent-scoped memory safely support PAIOS multi-runtime memory continuity?

## Environment

| Item | Value |
|---|---|
| PAIOS HEAD | `f956b431d1560c4652fc034d66548c0f00587125` (main, Phase 14 CLOSED) |
| Date | 2026-10-04, ~20:35–21:30 IST |
| agentmemory | upstream commit `2a00e7b38fc4ae4e38af4134586be0bbe9612706` (main, v0.9.29 source build; clone at `C:\Users\ABhas\projects\_eval_tmp\agentmemory`) |
| iii-engine | v0.22.1 pinned native binary (`%USERPROFILE%\.agentmemory\bin\iii.exe`) |
| OS/runtime | Windows 11 (win32), Node v25.6.0, Git Bash; Python 3.14 for assertions |
| Configuration | `CI=1 AGENTMEMORY_AGENT_SCOPE=isolated node dist/cli.mjs --data-dir C:\Users\ABhas\projects\_eval_tmp\am_data_iso`; keyless, zero-LLM (BM25 only); injection OFF |
| Data dir | `C:\Users\ABhas\projects\_eval_tmp\am_data_iso` (outside PAIOS repo) |
| Agent identities | `agent-scout`, `agent-logger` (per-call `agentId` on every request) |
| REST auth | bearer secret auto-generated at `%USERPROFILE%\.agentmemory\secret` |
| Endpoints tested | `/remember`, `/smart-search`, `/search` (BM25), `/context`, `/observe`, `/capture`, `/capture/drain`, `/observations`, `/sessions`, `/health`, `/status` |

## Configuration findings (FACT, from source + live probe)

- F1. Agent identity enters per call via the `agentId` field on REST bodies; server-side default identity is the `AGENT_ID` env var of the worker process.
- F2. `AGENTMEMORY_AGENT_SCOPE=isolated` is ONLY active when `AGENT_ID` is also set: `loadAgentScope()` (`src/config.ts:380-394`) returns null when `AGENT_ID` is unset, so `isAgentScopeIsolated()` is false and the runtime silently runs in shared mode. Verified live: first boot with scope=isolated but no `AGENT_ID` accepted an agentId-less read and returned agent-scout's private memory instead of refusing.
- F3. The documented hard-refusal branch in `mem::smart-search` / `mem::search` / `mem::context` ("isolated is set but no agent id is available — refusing to read cross-agent rows") is unreachable dead code: isolated=true requires `AGENT_ID` set (F2), which always yields a non-empty `envAgentId`, so the guard condition can never be true.
- F4. With `AGENT_ID=agent-scout` + isolated, an agentId-less read returns only scout records (env-default filtering verified live).

## Test results

| # | Test | Result | Evidence (actual observed behavior) |
|---|---|---|---|
| 1 | Own-memory retrieval | PASS | scout wrote `SCOUT_SECRET_7319` → id `mem_mutyfy8o_95f8716a0e8e` v1, agentId=agent-scout, project=iso-eval, origin.channel=agent; retrieved by same agentId. logger likewise (`mem_mutygb71_fd0b9080e947`). |
| 2 | Cross-agent isolation | PASS (per-call agentId on all tested retrieval surfaces) | scout→LOGGER_SECRET_4826: 0 results; logger→SCOUT_SECRET_7319: 0 results; broad queries ("marker stored under isolated scope", "CONCURRENT iso-eval") return only own-agent records via `/smart-search`, `/search`, `/context` (logger reading scout's session got 0 blocks / 0 tokens). NOT a security boundary — see T7. |
| 3 | Concurrent writes | PASS | 10+10 interleaved background writes: 20/20 accepted, 20/20 distinct ids, every record carried the correct agentId, versions ≥1, no corruption observed; post-write scoped recalls returned only own-agent records. |
| 4 | Concurrent retrieval | PASS | 10 concurrent mixed-agent searches: 10/10 responses correct and isolated; latencies 0.22–0.25 s; server stayed healthy (circuit breaker closed). |
| 5 | Restart persistence + isolation (hard gate) | PASS | Clean stop (ports closed, iii.exe terminated), restart on same data dir, no re-creation: scout recalled 12 own records incl. retry probe; logger 11; both cross-queries returned 0; ownership survived. |
| 6 | Implementation inspection | PASS with findings | Paths: `src/config.ts` (scope loader), `src/functions/smart-search.ts` (filterAgentId + post-filter of hybrid results), `src/functions/search.ts` (same pattern), `src/functions/context.ts` (same pattern; blocks filtered by `s.agentId === filterAgentId`), `src/triggers/api.ts` (REST propagates agentId on remember/search/smart-search/context). Findings F1–F4 + S1–S3 below. MCP uses the same `mem::` functions, so REST and MCP share isolation logic (MCP surface itself not exercised — no MCP client wired; marked UNKNOWN at transport level). |
| 7 | Scope-escape probes | PASS as scoping / FAIL as security boundary | `agentId:"*"` (wildcard) returns ALL agents' records (22) — documented opt-out; omitting agentId with no server `AGENT_ID` returns ALL records (shared-mode degradation, F2); whitespace agentId → unscoped (fail-closed: 0 results on that query); project-only query returned both agents' 22 records — project is confirmed NOT a security boundary (re-confirms 2026-10-03 finding). |
| 8 | Duplicate/retry interaction | PASS | Identical scout capture x3: deterministic version chain v1→v2→v3 with `supersedes` lineage, same agentId throughout, no duplicate rows, no scope crossing; logger query for the probe: 0 results. |
| 9 | Failure recovery | PARTIAL | 4 `/observe` events accepted (200 + eventId), server killed within the 3.5 s `durableAfterMs` window → ALL FOUR silently lost (boot drain: claimed 0 / delivered 0; not searchable). Positive half: 2 events kept alive >3.5 s persisted as observations and survived restart (`/observations` for session `iso-eval-s9-scout` shows exactly the 2 durable records; session survived). No cross-agent ownership created (session capture carries NO agentId — unscoped writes hidden from scoped reads, visible to unscoped reads). No duplicate explosion. |
| 10 | Context injection analysis | ANALYSIS (no injection enabled) | `AGENTMEMORY_INJECT_CONTEXT` (`src/config.ts:504-506`) is opt-in, default OFF, loud startup warning when ON; injection is deterministic to disable (env absent/false). Injection feeds from the same context path that applies the agentId filter (`src/functions/context.ts` propagates agentId → block filter), so a correctly parameterized hook would inject only the hook's agent scope. Selector details of the Claude-Code hooks themselves were read at source level only, not runtime-qualified. |

## Security / scope findings

- S1 (OBSERVATION): agentId isolation is cooperative client scoping, not adversarial security. Any client holding the bearer secret can pass `agentId:"*"`, omit agentId (when no server `AGENT_ID`), or claim any other agent's id and read that agent's memories. The real access boundary is the REST bearer secret.
- S2 (FACT): `project` is never a security boundary (source + live probe).
- S3 (FACT): isolated mode without server `AGENT_ID` silently degrades to shared mode; the "refusing to read cross-agent rows" error is unreachable code (F2/F3).
- S4 (OBSERVATION): for PAIOS multi-runtime continuity this is acceptable operationally — PAIOS runtimes are trusted local processes sharing the host — but accidental cross-runtime contamination prevention requires every caller to always pass an explicit agentId, because default reads are unscoped.

## Classification

- FACT: all rows in the test table labeled PASS/PARTIAL were executed live on 2026-10-04 with the commands above.
- OBSERVATION: S1, S4; latency magnitudes; concurrency behavior at n=20.
- INFERENCE: MCP transport shares isolation logic with REST (same `mem::` functions) — not runtime-verified.
- CLAIM (upstream, unverified here): README's "hard refusal" isolation semantics.
- UNKNOWN: MCP transport behavior; behavior at much larger corpus sizes; multi-instance (–instance 1) isolation.

## Limitations / unresolved

- T9 PARTIAL: accepted-but-not-durable captures (within 3.5 s) are silently lost on abrupt kill despite 200 responses. Not retested with graceful shutdown.
- Isolated-mode refusal semantics cannot be exercised at all (dead code, F3).
- One transient free-tier latency TIMEOUT was observed on the 2026-10-04 Phase-14 Hermes suite, unrelated to this evaluation; no agentmemory timeouts observed except design-level durability window.

## Decision

**PARTIAL — leaning PASS FOR NEXT STAGE.**

Why: every hard gate that concerns correct multi-runtime operation passed live (own retrieval, per-call isolation on all tested surfaces, 20/20 concurrent writes, 10/10 concurrent retrievals, restart persistence + isolation, deterministic retry versioning). What blocks an unqualified PASS is (a) the silently-degrading isolated mode + unreachable refusal (F2/F3), (b) the documented wildcard/unscoped cross-agent read paths (S1 — by design, but security-relevant), and (c) the silent pre-durability capture loss (T9). None of these are PAIOS integration assumptions; they are upstream behavior that PAIOS wrapper policy must account for (always pass explicit agentId; never rely on project; treat bearer secret as the boundary; do not promise crash-proof capture).

Smallest next experiment, if pursued: a single-session PAIOS-wrapper prototype test — one thin adapter that (1) always injects an explicit agentId per PAIOS runtime, (2) refuses wildcard/unscoped reads, and (3) verifies on startup that `AGENT_ID`+isolated mode are actually active — exercised only by Tests 1–5 above. No broader testing.
