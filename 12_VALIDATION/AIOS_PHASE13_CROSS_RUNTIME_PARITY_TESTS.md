# AIOS PHASE 13 — CROSS-RUNTIME PARITY TESTS

Status: CANONICAL V1+ — PHASE 13
Read: `03_PROTOCOLS/AIOS_RUNTIME_ADAPTER_PROTOCOL_V1.md`

Executable suite: `13_AUTOMATION/runtime_parity/tests/test_phase13.py`
(stdlib `unittest`). All tests use the deterministic, side-effect-free
reference adapter and synthetic data. No real external execution occurs.
Result conventions: PASS / PARTIAL / FAIL / UNVERIFIED / NOT_TESTED.

| ID | Target | Expected | Status |
|----|--------|----------|--------|
| RP-01 | Runtime adapter contract | identity/health/capabilities/execute/verify/cancel surface; cancel honestly runtime-dependent | PASS |
| RP-02 | Capability discovery | declared capability set queryable; durable registry record | PASS |
| RP-03 | Lifecycle state distinction | CONFIGURED ≠ VERIFIED; VERIFIED without evidence invalid; mark_verified is the only promotion | PASS |
| RP-04 | Execution request schema | task/authority/context/route/acceptance/deadline/retry/idempotency/evidence; empty authority rejected | PASS |
| RP-05 | Execution result schema | execution id, runtime, adapter, fingerprint, status, timestamps, output, evidence, error, verification, substitutions | PASS |
| RP-06 | Runtime identity preservation | runtime/adapter ids on results; fingerprint stable across adapters | PASS |
| RP-07 | Phase 10 routing integration | model route selected first; runtime selection a distinct later decision | PASS |
| RP-08 | Phase 9 worker integration | worker executes through adapter boundary; identity/authority/acceptance preserved | PASS |
| RP-09 | Phase 12 automation integration | automation delegates to adapter; authority/idempotency/acceptance pass through | PASS |
| RP-10 | Authority propagation | authority context carried unchanged; empty authority rejected pre-execution | PASS |
| RP-11 | Acceptance propagation | COMPLETED without evidence fails parity check | PASS |
| RP-12 | Idempotency propagation | same token+identity → same fingerprint across runtimes | PASS |
| RP-13 | Evidence propagation | evidence refs + execution id + fingerprint + runtime id present | PASS |
| RP-14 | UNKNOWN propagation | UNKNOWN never verifies as success | PASS |
| RP-15 | Timeout/failure handling | TIMEOUT distinct status; no output claimed; deadline error type | PASS |
| RP-16 | Runtime substitution | explicit substitution record; task/authority/acceptance preserved | PASS |
| RP-17 | Capability mismatch fallback | mismatch reason recorded; substitute revalidated | PASS |
| RP-18 | Untrusted runtime output | injection refused; authority-grabbing output flagged by parity check | PASS |
| RP-19 | Process-boundary persistence | real subprocess A/B: registry + result survive OS process boundary | PASS |
| RP-20 | End-to-end execution | inspect → select → execute → verify → parity check; durable registry | PASS |

## Adversarial tests

| ID | Scenario | Expected | Status |
|----|----------|----------|--------|
| ADV-1 | Runtime attempting scope escalation | substituted authority context blocked | PASS |
| ADV-2 | Runtime output attempting authority escalation | UntrustedContent | PASS |
| ADV-3 | Silent runtime substitution | blocked without concrete failure result | PASS |
| ADV-4 | Capability falsely marked VERIFIED | rejected without evidence | PASS |
| ADV-5 | Failed execution reported as success | forged COMPLETED with error → parity violation | PASS |
| ADV-6 | Verification failure reported as success | UNKNOWN never verifies | PASS |
| ADV-7 | Duplicate cross-runtime execution | same token → same fingerprint (detectable) | PASS |
| ADV-8 | Fallback changing task scope | mutated acceptance criteria blocked | PASS |

## Scope notes

- The reference adapter is NOT a production runtime and is never described as one.
- Real runtimes: ZCode VERIFIED (repository-local observable behavior only);
  OpenCode CLAIMED (CLI installed; model execution unverified — 2026-09-16
  runtime hang remains on record); Hermes/Grok/other roster runtimes UNKNOWN.
- No real external communication occurred during this test suite.
