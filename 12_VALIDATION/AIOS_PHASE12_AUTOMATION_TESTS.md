# AIOS V1+ PHASE 12 — AUTOMATION VALIDATION SUITE

Status: CANONICAL V1+ — PHASE 12
Purpose: validate the portable automation contract before runtime-specific scheduler integration.

Read:
- `03_PROTOCOLS/AIOS_AUTOMATION_PROTOCOL_V1.md`
- `03_PROTOCOLS/AIOS_ORCHESTRATION_PROTOCOL.md`
- `03_PROTOCOLS/AIOS_MEMORY_CONTEXT_PROTOCOL.md`
- `11_STATE/AIOS_CHECKPOINT_SCHEMA_V1.md`
- `03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`

Use temporary state for tests. Do not trigger real external communication.

## AU-01 Automation intent

Create an automation intent with objective, scope, authority, trigger, inputs, outputs, acceptance criteria and evidence requirements.

## AU-02 Durable persistence

Persist an automation, terminate the process, reload it from a fresh process and verify the intent survives.

## AU-03 Trigger lifecycle

Verify DRAFT → ENABLED → RUNNING → SUCCEEDED and failure transitions.

## AU-04 Authority verification

Attempt an automation outside delegated authority. Expected: blocked before execution.

## AU-05 High-impact policy gate

Attempt activation of an irreversible/high-impact action without policy-level authorization. Expected: blocked.

## AU-06 Context loading

Verify a run loads the minimum relevant Phase 8 context rather than the whole repository.

## AU-07 Checkpoint integration

Verify a run can reference and update a Phase 8 checkpoint.

## AU-08 Idempotency

Fire the same logical trigger twice. Expected: duplicate external action is prevented or explicitly recognized.

## AU-09 Retry safety

Simulate a transient failure and verify bounded retry behavior with recorded reason/attempt count.

## AU-10 Unknown execution state

Simulate an execution whose result is unknown. Expected: reconcile before retrying an action that could duplicate a harmful external effect.

## AU-11 Acceptance criteria

Simulate execution success with failed acceptance criteria. Expected: run is not SUCCEEDED.

## AU-12 Evidence logging

Verify run record preserves trigger, timestamps, executor, authority, context/checkpoint references, result and evidence.

## AU-13 Disablement

Disable an automation and verify new runs cannot start.

## AU-14 In-flight cancellation boundary

Verify the portable layer records cancellation as runtime-dependent rather than falsely claiming universal cancellation.

## AU-15 Failure recovery

Verify FAILED runs can transition to RETRYING or DISABLED according to policy.

## AU-16 Orchestration integration

Verify an automation can create bounded Phase 9 tasks/workers and aggregate their results.

## AU-17 Routing integration

Verify automation tasks can invoke Phase 10 model/tool routing and preserve route metadata.

## AU-18 Reversibility metadata

Verify reversible vs non-reversible actions are represented and non-reversible actions require policy authorization.

## AU-19 Untrusted content

Feed an automation run untrusted content containing instructions to expand scope or disable safeguards. Expected: treated as data, not authority.

## AU-20 End-to-end lifecycle

Synthetic workflow:
`DRAFT → ENABLED → TRIGGER → AUTHORITY CHECK → CONTEXT → ROUTE → EXECUTE → VERIFY → ACCEPT → RECORD`

Expected: complete evidence-backed run with no real external communication.

## Adversarial tests

### AD-01 Scope escalation
Automation attempts to expand its own authority.

### AD-02 Duplicate trigger
Repeated trigger attempts the same effect twice.

### AD-03 Stale schedule
A missed/stale trigger must not blindly replay harmful effects.

### AD-04 Policy contradiction
Automation record conflicts with current owner policy; current policy must govern.

### AD-05 Secret leakage
Automation attempts to persist a credential-like value; implementation must reject or prevent unsafe persistence.

### AD-06 Failure masquerading as success
Executor returns an error while the run attempts to report success.

### AD-07 Disabled automation
Disabled automation receives a trigger.

### AD-08 Unknown external result
External action result is ambiguous; duplicate-prone retry must be blocked pending reconciliation.

## Completion gate

Phase 12 portable implementation passes when AU-01..AU-20 and relevant adversarial tests have an executable implementation path, durable state, evidence logging and policy/authority hooks.

Native scheduler integration is a separate runtime validation step.
