# AIOS PHASE 14 — REAL RUNTIME INTEGRATION TESTS

Status: HISTORICAL TEST RECORD (2026-09-17 run). Phase 14 CLOSED 2026-10-04 —
see `12_VALIDATION/AIOS_PHASE14_CLOSEOUT_2026-10-04.md` for the current state.
The suite has since been extended: the working Codex model rotated upstream
`gpt-5.5` → `gpt-5.6-terra` (recorded 2026-10-03), a second real runtime
(Hermes Agent CLI, `tests/test_phase14_hermes.py`, 13/13) was verified, and
RT-20 became a REAL cross-runtime failover test plus a new RT-21 real
cross-runtime parity test. The table below records the 2026-09-17 run.
Read: `03_PROTOCOLS/AIOS_RUNTIME_ADAPTER_PROTOCOL_V1.md`

Executable suite: `13_AUTOMATION/runtime_parity/tests/test_phase14.py`
(stdlib `unittest`).

**Real vs synthetic execution is explicitly separated.**
`RealExecutionTests` (13 tests) invoke the REAL installed Codex CLI
(`codex exec`, model `gpt-5.5`, ChatGPT-account auth, read-only sandbox) —
approximately 9 bounded real executions per full-suite run, each read-only
and side-effect-free. `IsolationAndIntegrationTests` (6) and
`AdversarialPhase14Tests` (8) use the deterministic reference adapter so
they stay fast and side-effect-free.

| ID | Target | Expected | Status |
|----|--------|----------|--------|
| RT-01 | Actual ZCode-class adapter discovery | codex binary on PATH; runtime_id codex-cli | PASS |
| RT-02 | Actual health probe | AVAILABLE; ChatGPT auth mode observed in ~/.codex/auth.json | PASS |
| RT-03 | Capability lifecycle evidence | INSTALLED→VERIFIED only via mark_verified with evidence; durable across instances | PASS |
| RT-04 | Real execution request | canonical request preserved; fingerprint stable | PASS |
| RT-05 | Real execution result | COMPLETED with real agent output, exit 0, model recorded | PASS |
| RT-06 | Result verification | verify() on real result passes; FAILED result never verifies | PASS |
| RT-07 | Runtime identity preservation | adapter_id/runtime_id/fingerprint on real result | PASS |
| RT-08 | Evidence persistence | real result round-trips through disk | PASS |
| RT-09 | Phase 10 routing integration | model route selected first; runtime selection separate; codex selected with VERIFIED lifecycle | PASS |
| RT-10 | Phase 9 worker integration | worker completes through adapter boundary; ledger state not bypassed | PASS |
| RT-11 | Phase 12 automation integration | automation delegates to runtime boundary; lifecycle authoritative | PASS |
| RT-12 | Authority propagation (real) | authority context travels as data; fingerprint unchanged | PASS |
| RT-13 | Acceptance propagation | evidence-less COMPLETED fails parity check | PASS |
| RT-14 | Idempotency (real) | same canonical request → same fingerprint across two REAL runs; distinct execution ids | PASS |
| RT-15 | Failure normalization (real) | invalid model → 400 error surfaced → FAILED, never success | PASS |
| RT-16 | Timeout handling (real) | 1s deadline → TIMEOUT, deadline_exceeded, no output | PASS |
| RT-17 | UNKNOWN handling (real) | empty output with exit 0 never COMPLETED | PASS |
| RT-18 | Process-boundary persistence | real subprocess A/B: result + fingerprint survive | PASS |
| RT-19 | Real end-to-end task | real codex run reads a file and returns its first line; parity check passes | PASS |
| RT-20 | Runtime failover w/ second VERIFIED runtime | **NOT_APPLICABLE as real failover** — no second VERIFIED runtime exists (recorded honestly); substitution mechanism proven at contract level | PASS (mechanism) / NOT_APPLICABLE (real) |

## Adversarial tests

| ID | Scenario | Expected | Status |
|----|----------|----------|--------|
| AD-14-01 | Runtime scope escalation | canonical authority unchanged | PASS |
| AD-14-02 | Runtime authority escalation (real) | authority-grabbing output fails verification | PASS |
| AD-14-03 | Runtime output injection | UntrustedContent on injection markers | PASS |
| AD-14-04 | False success | forged COMPLETED with error → parity violation | PASS |
| AD-14-05 | False verification | UNKNOWN never verifies | PASS |
| AD-14-06 | Duplicate real execution | same fingerprint cross-adapter; Phase 12 blocks same-token repeat | PASS |
| AD-14-07 | Silent substitution | blocked without concrete failure | PASS |
| AD-14-08 | Fallback scope change | mutated acceptance blocked | PASS |

## Additional observed evidence (outside suite)

- **read-only sandbox honored (real):** a prompt asking codex to append to a
  file inside `-s read-only` produced the proposed command but did NOT
  modify the file (verified by reading the file after the run).
- **OpenCode re-probe (real):** `opencode run` hung again on 2026-09-17
  (exit 124 after 120s, zero output). OpenCode remains CLAIMED /
  execution UNVERIFIED.
- **grok 0.2.102:** installed; not signed in (real probe observed).
- **hermes 0.21.3:** installed; provider endpoint unavailable (real probe).
- **kimi 0.43.0:** installed; 403 monthly quota exhausted (real probe).
- **codex default model `gpt-5.4-mini`** rejected by the account tier
  (400 invalid_request_error, observed repeatedly); `gpt-5.5` (from
  ~/.codex/models_cache.json) verified working.
