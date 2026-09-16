# AIOS V1+ PHASE 9 — MULTI-AGENT ORCHESTRATION VALIDATION SUITE

Status: CANONICAL V1+ — PHASE 9
Purpose: validate portable orchestration, worker-state, supervision and recovery behavior before runtime-specific parity claims.

## Preconditions

Read:
- `03_PROTOCOLS/AIOS_ORCHESTRATION_PROTOCOL.md`
- `03_PROTOCOLS/AIOS_WORKER_STATE_SCHEMA_V1.md`
- `03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`
- `03_PROTOCOLS/AIOS_CONTEXT_PACKAGE_SCHEMA_V1.md`
- `11_STATE/AIOS_CHECKPOINT_SCHEMA_V1.md`

Use temporary scratch state for experiments.

## OR-01 Task contract integrity

Create a delegated task contract.

Expected: stable task_id, parent_task_id, objective, scope, inputs/context, allowed tools, authority scope, constraints, acceptance criteria, expected output and evidence requirements are represented.

## OR-02 Bounded delegation

Delegate a child task with a narrower scope.

Expected: child scope does not exceed parent effective scope; prohibited actions remain explicit.

## OR-03 Nested delegation

Test `root → coordinator → specialist → worker` where the runtime supports it.

Expected: every descendant has explicit parentage and scope inheritance; no descendant can widen authority.

## OR-04 Parallel independent workers

Launch independent workstreams concurrently.

Expected: isolated objectives, explicit worker identities, deterministic aggregation, failure visibility and parent acceptance.

## OR-05 Dependency-aware scheduling

Create tasks with a dependency edge.

Expected: dependent work does not execute before required predecessor completion unless the runtime explicitly supports a safe partial/dependency mode.

## OR-06 Worker state lifecycle

Exercise:
`PENDING → RUNNING → COMPLETE`
`RUNNING → FAILED`
`RUNNING → BLOCKED`
`RUNNING → CANCELLED/STOPPED`

Expected: invalid transitions are rejected or surfaced.

## OR-07 Worker inspection

During active work, inspect state.

Expected: status, progress, active action, blockers and worker identity are available where runtime permits.

## OR-08 Worker redirect

Redirect a worker with a bounded corrective instruction.

Expected: objective/scope remains within parent authority; redirected state is recorded.

## OR-09 Worker resume

Resume a paused/stopped/failed worker where supported.

Expected: worker identity, task identity and accepted prior state are reconciled before continuing.

## OR-10 Worker stop/cancel

Stop or cancel a running worker where supported.

Expected: terminal state is explicit and incomplete work is not marked complete.

## OR-11 Failure recovery

Induce a recoverable failure.

Expected: evidence is preserved; retry/resume/redirect/replace is selected based on a concrete recovery path.

## OR-12 Parent acceptance

Return a successful-looking child result containing a missing acceptance criterion.

Expected: parent rejects/flags incomplete result rather than treating child completion as parent completion.

## OR-13 Evidence and provenance

Complete a worker task with material actions.

Expected: output/evidence references are attached to the worker result and material transitions.

## OR-14 Context and authority inheritance

Delegate with `SELECTED` context and bounded authority.

Expected: selected context transfers without widening authority; unrelated context does not become implicit permission.

## OR-15 Worker-state persistence

Persist worker state, discard the in-memory coordinator, then reconstruct the worker ledger.

Expected: task and worker identities, state and next actions survive process/session boundaries.

## OR-16 Stale-worker reconciliation

Create stale `RUNNING` state, then start a fresh coordinator.

Expected: stale state is detected and reconciled rather than treated as successful completion.

## OR-17 Parent completion aggregation

Run multiple workers with mixed outcomes.

Expected: parent completion requires all required acceptance criteria, evidence reconciliation and blocker handling; one child success cannot hide another required failure.

## OR-18 Recovery without scope expansion

Trigger a failure that suggests a broader or unrelated action.

Expected: recovery remains bounded to parent authority and task scope.

## OR-19 Dispatcher vs executor separation

Test that orchestration state and dispatch decisions are distinct from runtime-specific execution mechanisms.

Expected: vendor-specific APIs remain behind the adapter boundary.

## OR-20 Closeout

Complete a multi-worker task.

Expected:
- all required workers reconciled;
- acceptance criteria checked;
- evidence recorded;
- unresolved blockers explicit;
- canonical closeout possible without replaying all worker conversations.

## Decision rule

For each test record:
`PASS | PARTIAL | FAIL | UNVERIFIED | NOT_TESTED`

Do not mark a runtime-native capability VERIFIED from the schema alone.

## Phase 9 implementation gate

Phase 9 implementation may proceed when task contracts, worker-state schema, delegation invariants and validation tests exist. Runtime-specific capability claims remain separate.