# AIOS CONTEXT PACKAGE SCHEMA V1

Status: CANONICAL V1+ — PHASE 8 IMPLEMENTATION
Purpose: define the minimum portable context package supplied to a task, worker, delegated bot, or runtime.

## 1. Principle

Context is selected, not dumped.

Every runtime receives the smallest sufficient package for the task while retaining enough policy and state to execute correctly.

## 2. Logical schema

```yaml
context_package_id: CTX-<stable-id>
task_id: TASK-<stable-id>
created_at: <ISO-8601>
source_checkpoint: CHK-<id-or-null>
mission:
  objective: <task objective>
  scope: <allowed scope>
  acceptance_criteria: [<criterion>, ...]
policy:
  canonical_rules: [<path-or-rule-ref>, ...]
  authority_scope: <delegated scope>
  prohibited_actions: [<action>, ...]
knowledge:
  selected_records: [MEM-...]
  canonical_files: [<path>, ...]
  workflow_refs: [<path>, ...]
runtime:
  adapter: <adapter path/id>
  executor: <runtime identity>
  model_provider: <provider/model or unknown>
state:
  completed: [<action>, ...]
  pending: [<action>, ...]
  blockers: [<blocker>, ...]
  decisions: [<decision>, ...]
evidence:
  required: [<evidence item>, ...]
  existing_refs: [<evidence-ref>, ...]
inheritance:
  mode: NONE | SELECTED | RECENT_RELEVANT | FULL
  parent_context_refs: [<ref>, ...]
  excluded_refs: [<ref>, ...]
budget:
  max_items: <integer-or-null>
  max_tokens: <integer-or-null>
sensitivity:
  allowed: [PUBLIC | INTERNAL | PERSONAL | SENSITIVE]
```

## 3. Construction algorithm

1. Identify task objective and scope.
2. Load mandatory authority/policy rules.
3. Load only task-relevant canonical files.
4. Retrieve candidate persistent memories.
5. Apply relevance, freshness, provenance, conflict and sensitivity gating.
6. Attach required workflow and runtime adapter references.
7. Attach checkpoint state when resuming.
8. Apply context budget.
9. Explicitly record excluded context when exclusion matters for auditability.
10. Produce the package before delegation/execution.

## 4. Inheritance modes

### NONE
Child receives task contract and mandatory policy only.

### SELECTED
Child receives explicitly selected records/files/state.

### RECENT_RELEVANT
Child receives recent context filtered by relevance and scope.

### FULL
Child receives complete available task context only when explicitly justified by objective complexity.

The default for delegated work is `SELECTED`.

## 5. Leakage control

A child MUST NOT inherit unrelated:
- personal memory;
- credentials/secrets;
- unrelated project state;
- unrelated conversation history;
- hidden assumptions;
- authority beyond its delegated scope.

Runtime ambient instructions may still exist. The adapter must identify such ambient context where the runtime exposes it.

## 6. Context budgeting

Selection priority:

`mandatory policy → task contract → current state/checkpoint → task-relevant canonical knowledge → high-confidence relevant memory → supporting historical context`

Drop lower-priority material before dropping mandatory policy or acceptance criteria.

## 7. Freshness

Prefer current canonical/runtime state over historical context. Historical context may remain in the package when necessary to explain decisions or conflicts.

## 8. Provenance

Every nontrivial imported memory or external fact SHOULD retain a source reference. Context packages should reference canonical paths and memory IDs rather than copying large source documents where possible.

## 9. Resumption

A resumed task should be reconstructable from:
- context package;
- latest checkpoint;
- canonical repository state;
- relevant evidence references.

The full conversation should not be required for normal handoff.

## 10. Phase 8 implementation rule

The context package is a portable logical contract. Runtime adapters may implement it through:
- prompt injection;
- AGENTS.md or equivalent instruction files;
- structured task payloads;
- session state;
- tool calls;
- orchestration metadata.

Do not make any one runtime's native context mechanism canonical.
