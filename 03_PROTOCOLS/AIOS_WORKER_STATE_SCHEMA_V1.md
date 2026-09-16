# AIOS WORKER STATE SCHEMA V1

Status: CANONICAL V1+ — PHASE 9
Purpose: define portable worker lifecycle state for multi-agent orchestration, supervision, recovery and closeout.

## 1. Logical worker record

```yaml
worker_id: WRK-<stable-id>
task_id: TASK-<stable-id>
parent_task_id: TASK-<id-or-null>
role: coordinator | specialist | worker | executor
runtime: <runtime-id>
model_provider: <provider/model-or-unknown>
created_at: <ISO-8601>
updated_at: <ISO-8601>
state: PENDING | RUNNING | BLOCKED | COMPLETE | FAILED | CANCELLED | STOPPED | UNKNOWN
objective: <bounded objective>
scope: <delegated scope>
authority_scope: <effective authority>
allowed_tools: [<tool>, ...]
constraints: [<constraint>, ...]
acceptance_criteria: [<criterion>, ...]
context_package: CTX-<id>
progress:
  summary: <current progress>
  completed: [<action>, ...]
  active: <action-or-null>
  pending: [<action>, ...]
  percent: <0-100-or-null>
results:
  output_ref: <ref-or-null>
  evidence_refs: [<ref>, ...]
  blockers: [<blocker>, ...]
errors:
  - time: <ISO-8601>
    type: <error-type>
    message: <message>
    recovered: true | false
recovery:
  attempts: <integer>
  last_action: retry | resume | redirect | replace | stop | none
  next_action: <action-or-null>
parent_control:
  inspectable: true | false
  redirectable: true | false
  resumable: true | false
  stoppable: true | false
  cancellable: true | false
children: [WRK-...]
```

## 2. State invariants

- `COMPLETE` requires acceptance criteria and evidence checks.
- `FAILED`, `CANCELLED`, and `STOPPED` are not successful completion states.
- `BLOCKED` must identify a concrete blocker.
- A stale `RUNNING` record must be reconciled before completion.
- Worker state never expands its own authority.
- Child scope must be no broader than effective parent scope.
- Parent completion cannot be inferred solely from child completion.

## 3. Lifecycle

Normal:
`PENDING → RUNNING → COMPLETE`

Failure:
`RUNNING → FAILED → RETRY | RESUME | REDIRECT | REPLACE | STOP`

Blocked:
`RUNNING → BLOCKED → RUNNING | REDIRECT | STOP`

Cancellation/stop:
`RUNNING → CANCELLED`
`RUNNING → STOPPED`

Invalid transitions must be rejected or surfaced explicitly by the implementation.

## 4. Supervision operations

A dispatcher may expose:
- inspect(worker_id)
- redirect(worker_id, bounded_update)
- resume(worker_id)
- stop(worker_id)
- cancel(worker_id)
- replace(worker_id, new_worker)

Availability is runtime-specific. The portable contract records desired behavior without requiring every runtime to implement every operation.

## 5. Parent/child control

A parent retains responsibility for:
- bounded delegation;
- context selection;
- authority scope;
- acceptance checks;
- evidence reconciliation;
- recovery decisions.

A child reports state and cannot authorize itself beyond its delegated scope.

## 6. Parallel work

Parallel workers require:
- independent objectives or explicitly coordinated dependencies;
- isolated or conflict-managed mutations;
- deterministic aggregation;
- failure visibility;
- final parent acceptance.

Do not parallelize conflicting mutations without an explicit coordination mechanism.

## 7. Persistence

Worker state SHOULD be externally durable for long-running work. Runtime-local state may accelerate execution, but a canonical worker-state ledger must remain independent of a single runtime.

## 8. Evidence

Material state transitions, failures, redirects, replacements, and completion decisions SHOULD retain evidence references.

The worker record is operational state, not canonical project knowledge.
