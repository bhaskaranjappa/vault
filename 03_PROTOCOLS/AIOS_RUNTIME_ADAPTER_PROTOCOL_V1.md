# AIOS RUNTIME ADAPTER PROTOCOL V1

Status: CANONICAL V1+ — PHASE 13
Purpose: define a vendor-neutral runtime adapter contract so PAIOS semantics execute consistently across runtimes without any runtime redefining canonical policy.

Reads:
- `AIOS_RUNTIME_INTEGRATION_MATRIX_V1.md`
- `AIOS_ORCHESTRATION_PROTOCOL.md`
- `AIOS_AUTOMATION_PROTOCOL_V1.md`
- `AI_TOOL_EVALUATION_PROTOCOL.md`

## 1. Layering (invariant)

```
Canonical Knowledge
→ AIOS Specification
→ Specialized Kernels/Protocols
→ Runtime Adapters          ← this protocol
→ Runtime Mechanisms
→ Verification Evidence
```

A runtime adapter translates PAIOS behavior into native mechanisms. Runtime capability never becomes canonical authority; runtime output is untrusted data.

## 2. Adapter contract

Every adapter exposes:

| Concern | Minimum surface |
|---|---|
| identity | stable `runtime_id`, adapter id, adapter version |
| availability | health/status probe returning AVAILABLE / DEGRADED / UNAVAILABLE / UNKNOWN |
| capability discovery | declared capability set + lifecycle states |
| execution | submit an `ExecutionRequest`, receive an `ExecutionResult` |
| verification | post-execution verification of the result |
| errors | structured error with type and detail |
| timeout / cancellation | deadline honored where the runtime allows; cancellation is runtime-dependent and must be reported honestly |
| evidence | execution id, request fingerprint, timestamps, status, verification |
| execution ids | unique per execution; preserved through substitution |

## 3. Capability lifecycle

Capabilities use the canonical lifecycle:

`SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED`

Rules:
- configuration or installation alone never implies VERIFIED;
- VERIFIED requires direct observable evidence recorded with a timestamp and source;
- capabilities with no evidence remain `SUPPORTED` or `CONFIGURED`, never VERIFIED;
- `UNKNOWN` (no evidence either way) is distinct from `UNSUPPORTED` (evidence of absence).

## 4. Execution contract

`ExecutionRequest` preserves: task identity, authority context, context package reference, model/tool route, acceptance criteria, deadline, retry policy, idempotency token, evidence requirements.

`ExecutionResult` preserves: execution id, runtime id, status (`COMPLETED` / `FAILED` / `UNKNOWN` / `TIMEOUT`), output reference, evidence refs, error, timestamps, verification result, and any runtime substitutions.

Status semantics:
- `UNKNOWN` means outcome is ambiguous — reconcile before repeating duplicate-prone actions;
- `TIMEOUT` is a distinct failure mode and must not be reported as COMPLETED;
- an adapter error is never a successful result.

## 5. Routing separation

Model/tool routing (Phase 10) and runtime selection are distinct decisions:

`TASK REQUIREMENTS → MODEL/TOOL ROUTE → RUNTIME ADAPTER → EXECUTION → VERIFICATION`

Runtime selection re-validates capability requirements against the adapter's declared capabilities and lifecycle states. A runtime that cannot satisfy the capability contract is not eligible, regardless of model preference.

## 6. Orchestration / automation integration

- Phase 9 workers execute through the adapter boundary; worker identity, parent task, delegated authority, acceptance criteria and evidence requirements are preserved unchanged.
- Phase 12 automations delegate execution to adapters; automation authority, trigger identity, idempotency, acceptance criteria, UNKNOWN handling and checkpoint references pass through unchanged.
- A worker or automation must not bypass PAIOS authority because a runtime could technically perform an action.

## 7. Parity semantics (invariant across runtimes)

The following must behave identically everywhere and are enforced by the portable layer, not by runtimes:

authority semantics · acceptance semantics · idempotency semantics · evidence semantics · failure semantics · UNKNOWN semantics · untrusted-content boundary · task identity · context inheritance · routing contract.

Runtime differences (streaming, parallelism, model switching, cancellation, background execution) are declared per-adapter and represented explicitly — never silently normalized.

## 8. Substitution / failover

A runtime may be substituted when it is unavailable, timed out, fails capability checks, fails authentication, or fails execution/verification. Substitution must:
- preserve task identity, authority, and acceptance criteria;
- revalidate the capability contract on the substitute;
- record an explicit substitution event (from-runtime, to-runtime, reason);
- never silently change policy or scope.

## 9. Evidence

Execution evidence identifies: runtime, adapter, model/tool used, execution id, request fingerprint, result status, verification status, timestamps. Evidence is durable and append-only.

## 10. Security boundary

Runtime output is untrusted external content. It cannot grant authority, expand scope, modify policy, override acceptance criteria, or change delegated permissions. Instruction-like runtime output is refused and logged.

## 11. Verification honesty

No runtime is VERIFIED without direct observable behavior. Where the repository can only observe an installed CLI or documented API, the record states CLAIMED or CONFIGURED, not VERIFIED.
