# AIOS V1+ PHASE 8 — MEMORY & CONTEXT VALIDATION SUITE

Status: CANONICAL V1+ — PHASE 8
Purpose: validate the portable memory/context architecture before introducing runtime-specific infrastructure.

## Preconditions

Read:
- `03_PROTOCOLS/AIOS_MEMORY_CONTEXT_PROTOCOL.md`
- `03_PROTOCOLS/AIOS_MEMORY_ARCHITECTURE_V1.md`
- `03_PROTOCOLS/AIOS_CONTEXT_PACKAGE_SCHEMA_V1.md`
- `11_STATE/AIOS_CHECKPOINT_SCHEMA_V1.md`
- `02_AI_STACK/AIOS_CAPABILITY_PRIMITIVES.md`

Use temporary scratch state for experiments. Do not treat runtime memory as canonical.

## MC-01 Explicit memory write

Write one durable test memory with complete provenance.

Verify:
- stable memory ID;
- classification;
- source/ref;
- confidence;
- timestamps;
- project/task association;
- sensitivity.

Expected: PASS only when the complete logical record survives persistence.

## MC-02 Persistence across sessions

Write a memory, end the runtime/session, start a fresh session, and retrieve it.

Expected: memory is recoverable without relying on the previous conversation transcript.

## MC-03 Relevance gating

Create at least three memories: one directly relevant, one related but stale, one unrelated.

Query for the relevant task.

Expected:
- relevant memory selected;
- unrelated memory excluded;
- stale memory excluded when a newer authoritative record supersedes it.

## MC-04 Sensitivity gating

Create memories at different sensitivity levels.

Run a task whose context authorization excludes sensitive records.

Expected: excluded records never enter active task context.

## MC-05 Provenance preservation

Store memories from distinct sources.

Retrieve them and verify source/date/classification/confidence survive the retrieval path.

Expected: provenance remains attached to the memory and context reference.

## MC-06 Stated vs inferred

Create one explicit owner-stated fact and one agent inference.

Expected: retrieval preserves the distinction and the inference is not promoted to fact without evidence.

## MC-07 Conflict preservation

Create two conflicting records with distinct provenance.

Expected:
- both records remain discoverable;
- conflict is represented explicitly;
- historical record is not silently destroyed.

## MC-08 Current-state precedence

Create a historical memory that conflicts with a current canonical/runtime fact.

Expected:
- current fact governs execution;
- historical memory remains preserved;
- material conflict is visible.

## MC-09 Explicit invalidation / forgetting

Create a disposable test memory, invalidate/forget it, then query for it.

Expected: it is excluded from normal retrieval and its state transition is auditable where policy requires preservation.

## CT-01 Context package construction

Build a task package using `AIOS_CONTEXT_PACKAGE_SCHEMA_V1.md`.

Expected sections:
- mission;
- policy;
- selected knowledge;
- runtime;
- state;
- evidence;
- inheritance;
- budget;
- sensitivity.

## CT-02 Minimal context

Provide a task with multiple unrelated canonical files and memories.

Expected: only the files/memories necessary for the task are included.

## CT-03 Selective inheritance

Delegate a child task with a selected subset of parent context.

Expected:
- selected context is available;
- unrelated parent context is excluded;
- child authority does not widen through inherited context.

## CT-04 Context budgeting

Give the package a constrained token/item budget.

Expected priority order:

`mandatory policy → task contract → current state/checkpoint → relevant canonical knowledge → relevant memory → supporting history`

Lower-priority material is dropped first.

## CT-05 Checkpoint creation

Pause a multi-step task and create a checkpoint.

Expected checkpoint contains:
- task identity;
- objective/scope;
- completed actions;
- current state;
- decisions;
- evidence;
- blockers;
- next incomplete action;
- context package reference.

## CT-06 Checkpoint reconstruction

Start a fresh session and reconstruct the task from checkpoint + context package + canonical state.

Expected: no full conversation replay is required.

## CT-07 State verification on resume

Change repository/runtime state after checkpoint creation, then resume.

Expected: resume process detects and reconciles state differences before continuing.

## CT-08 Compaction readiness

Simulate context pressure.

Expected:
- checkpoint written before compaction;
- critical policy/objective/state preserved;
- post-compaction restore uses checkpoint + context package.

## Decision rule

For each test record:

`PASS | PARTIAL | FAIL | UNVERIFIED | NOT_TESTED`

Do not mark a runtime-specific capability VERIFIED from protocol conformance alone.

## Phase 8 completion gate

Phase 8 foundation may move to runtime implementation/benchmarking when MC-01..MC-09 and CT-01..CT-08 have canonical schemas and at least one executable implementation path has been selected.

Runtime parity remains a separate validation step. Hermes-specific live tests are intentionally deferred per owner direction.
