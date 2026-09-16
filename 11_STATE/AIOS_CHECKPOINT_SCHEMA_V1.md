# AIOS CHECKPOINT SCHEMA V1

Status: CANONICAL V1+ — PHASE 8 IMPLEMENTATION
Purpose: define a compact, runtime-independent checkpoint sufficient to resume or hand off an active task without replaying the full conversation.

## 1. Logical schema

```yaml
checkpoint_id: CHK-<stable-id>
task_id: TASK-<stable-id>
version: 1
created_at: <ISO-8601>
updated_at: <ISO-8601>
repository:
  ref: <repo>
  branch: <branch>
  head: <commit-or-unknown>
  working_tree: CLEAN | DIRTY | UNKNOWN
objective: <task objective>
scope: <task scope>
acceptance_criteria: [<criterion>, ...]
completed:
  - action: <action>
    status: COMPLETE
    evidence: [<ref>, ...]
current_state:
  phase: <current phase>
  active_action: <current action>
  observations: [<fact>, ...]
decisions:
  - decision: <decision>
    rationale: <brief rationale>
    evidence: [<ref>, ...]
blockers:
  - <blocker>
next_actions:
  - <next incomplete action>
context_package: CTX-<id>
authority_scope: <effective delegated scope>
workers:
  - worker_id: <id>
    role: <role>
    state: RUNNING | COMPLETE | FAILED | STOPPED | UNKNOWN
    result_ref: <ref-or-null>
evidence_refs: [<ref>, ...]
conflicts: [<conflict-ref>, ...]
risks: [<risk>, ...]
```

## 2. Checkpoint invariants

A checkpoint MUST be:
- compact;
- externally durable;
- timestamped;
- tied to a task identity;
- sufficient to identify the next incomplete action;
- backed by evidence references where claims matter;
- consistent with current repository/runtime state at checkpoint creation.

## 3. Safe resume

Resume sequence:

`Load checkpoint → verify repository/runtime state → verify authority scope → load referenced context package → verify completed claims → execute next incomplete action → update checkpoint`

Never blindly resume based only on the textual checkpoint.

## 4. State transitions

Valid worker states:

`RUNNING → COMPLETE`
`RUNNING → FAILED`
`RUNNING → STOPPED`

A `FAILED`, `STOPPED`, or stale `RUNNING` worker must be reconciled before being treated as complete.

## 5. Compaction

Before context compaction, write/update the checkpoint with:
- objective;
- completed work;
- current state;
- decisions;
- evidence;
- blockers;
- next action;
- context-package ID.

After compaction, restore only what is required by the checkpoint and task context package.

## 6. Handoff

The checkpoint is compatible with `11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md`.

A handoff may reference the checkpoint rather than duplicating every state detail. The canonical repository and evidence records remain authoritative.

## 7. Snapshot limitation

This schema describes logical task state. It does not imply filesystem snapshot, database transaction rollback, model-state restoration, or runtime process restoration.

Those are runtime-specific capabilities and must be separately verified.
