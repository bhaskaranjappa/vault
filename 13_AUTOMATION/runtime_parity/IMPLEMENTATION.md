# PAIOS Cross-Runtime Parity Engine — Implementation Notes

Portable, runtime-independent parity layer (`paios_runtime`, stdlib-only)
implementing `03_PROTOCOLS/AIOS_RUNTIME_ADAPTER_PROTOCOL_V1.md`. It defines
how PAIOS semantics execute consistently across runtime adapters without any
runtime redefining canonical policy. This module does not duplicate the
canonical protocol.

## Architecture

```
Canonical Knowledge → AIOS Spec → Protocols
  → Runtime Adapters (paios_runtime)   ← this engine
      ├─ RuntimeAdapter contract       (adapters.py)
      ├─ CapabilityRegistry            (capabilities.py)
      ├─ ExecutionRequest/Result       (execution.py)
      ├─ SubstitutionChain             (substitution.py)
      ├─ ParityEnforcer                (parity.py)
      ├─ RuntimeRegistry / selection   (parity.py)
      ├─ Untrusted-content boundary    (untrusted.py)
      └─ Real-runtime inspection       (real_runtimes.py)
  → Runtime Mechanisms (per-adapter, vendor-specific)
  → Verification Evidence (durable, append-only)
```

## Modules

| Module | Responsibility |
|--------|----------------|
| `capabilities.py` | `Lifecycle` (SUPPORTED→…→VERIFIED), `VerificationState` (VERIFIED/CLAIMED/UNKNOWN/UNSUPPORTED — UNKNOWN distinct from UNSUPPORTED), `RuntimeCapabilityRecord`, durable `CapabilityRegistry` with deterministic `eligible()` |
| `execution.py` | `ExecutionRequest` (task/authority/context/route/acceptance/deadline/retry/idempotency/evidence), `ExecutionResult` (execution id, runtime, status, evidence, substitutions), deterministic `RequestFingerprint` via SHA-256 |
| `adapters.py` | `RuntimeAdapter` contract + deterministic reference adapters: success, deterministic failure, UNKNOWN, timeout-simulated, capability-mismatch, unavailable |
| `substitution.py` | `SubstitutionChain`/`SubstitutionRecord` — explicit, reason-coded failover preserving task identity, authority and acceptance |
| `parity.py` | `ParityEnforcer` checks the 10 invariants; `RuntimeRegistry.select()` performs post-routing runtime selection with capability revalidation and health checks |
| `untrusted.py` | runtime output = untrusted data; injection markers refused |
| `real_runtimes.py` | re-runnable inspection of real runtimes recording only directly observable evidence |

## Key invariants

- **Runtime selection ≠ model selection.** The decision chain is
  `TASK REQUIREMENTS → MODEL/TOOL ROUTE → RUNTIME ADAPTER → EXECUTION → VERIFICATION`.
- **VERIFIED requires direct observable evidence.** A record claiming
  VERIFIED without evidence_refs is invalid at construction. OpenCode with an
  installed CLI is CLAIMED, not VERIFIED.
- **Substitution never silently changes anything.** It requires a concrete
  failure result with a mapped reason, refuses changed authority/acceptance,
  and appends an explicit substitution record id to the result.
- **The portable layer enforces parity**, not the runtimes: fingerprint
  match, error-implies-failure, TIMEOUT-claims-no-output, evidence-on-COMPLETED,
  untrusted-output inspection.
- **Runtime output is data, never authority** (shared boundary semantics with
  Phases 11/12).

## Reference adapter

`ReferenceRuntimeAdapter` is deterministic and side-effect-free. Behavior is
driven by `request.inputs["behavior"]`: `ok | fail | unknown | timeout |
mismatch`. It exists for testing only and is never described as a production
runtime.

## Real-runtime verification status (2026-09-17)

| Runtime | Status | Basis |
|---|---|---|
| ZCode | VERIFIED | repository-local observable behavior: Phase 8–12 implementations, tests, commits (limited to repo-local capability) |
| OpenCode | CLAIMED | CLI 1.18.31 installed; `opencode run` hang observed 2026-09-16; model execution unverified |
| Hermes Agent | UNKNOWN | live validation deferred |
| Grok Bot | UNKNOWN | runtime access unavailable |
| Other roster runtimes | UNKNOWN | no observable adapter boundary |

## Integration

- **Phase 10:** routing profile → route decision ref → `RuntimeRegistry.select()`
  with capability revalidation (RP-07).
- **Phase 9:** workers execute through the adapter boundary; completed worker
  records carry the adapter's output/evidence (RP-08).
- **Phase 12:** automation executor adapters can delegate to the runtime
  boundary; automation authority, idempotency and acceptance pass through
  unchanged (RP-09).
