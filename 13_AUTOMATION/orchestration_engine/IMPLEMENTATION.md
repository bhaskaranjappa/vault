# PAIOS ORCHESTRATION ENGINE — IMPLEMENTATION

Phase: V1+ Phase 9 — Multi-Agent Orchestration Hardening
Location: `13_AUTOMATION/orchestration_engine/`
Language: Python 3, standard library only.
Nature: portable orchestration engine. Runtime-independent; no ZCode, OpenCode,
Hermes, Grok, LangChain/LangGraph or other vendor framework dependency.

## 1. Architecture position

```
Canonical Knowledge
  ↓
AIOS Orchestration Protocol + Worker State Schema V1   (03_PROTOCOLS/)
  ↓
Portable Orchestration Engine (this package, paios_orch)
  ↓
Runtime Adapter (paios_orch.executor.Executor + runtime adapters)
  ↓
Runtime-native agents/tools
```

The engine implements contracts; adapters implement execution. Vendor behavior
never leaks into the portable layer, and this file does not duplicate the
canonical protocol text.

## 2. Modules

| Module | Responsibility |
| --- | --- |
| `tasks.py` | Frozen `TaskContract` (stable task identity), validation |
| `states.py` | 8-state lifecycle machine, explicit transitions, `InvalidTransition` |
| `ledger.py` | Durable worker ledger (`WRK-*.json` + `index.yaml`), hierarchy, stale reconciliation |
| `events.py` | Append-only JSONL evidence log for every material transition |
| `delegation.py` | Bounded delegation; scope/authority containment checks; escalation rejection |
| `deps.py` | Dependency graph: readiness, blocked state, failure propagation, cycle rejection |
| `parallel.py` | `ThreadPoolExecutor` parallel branches; per-branch failure visibility; deterministic aggregation |
| `supervision.py` | inspect / redirect / resume / stop / cancel / replace + bounded recovery |
| `acceptance.py` | Parent acceptance checks; aggregate parent completion |
| `dispatcher.py` | Dispatch policy (EXECUTE / DELEGATE / PARALLELIZE / WAIT_DEPENDENCY / RETRY / REDIRECT / REPLACE / STOP) separated from execution |
| `executor.py` | Adapter boundary + capability discovery (`SUPPORTED` vs `RUNTIME_SUPPORTED` vs `RUNTIME_UNSUPPORTED`) |
| `orchestrator.py` | Facade wiring ledger + dispatcher + supervisor + acceptor + Phase 8 integration |

## 3. Task model

`TaskContract` is a frozen dataclass with stable `TASK-<uuid>` identity that
survives serialization and resume. Required fields: objective, scope,
authority_scope, acceptance_criteria, expected_output (validated at
registration). Inputs, allowed tools, constraints, evidence requirements and a
`context_package` reference (CTX-*) are carried on the contract.

## 4. Worker lifecycle

States: `PENDING → RUNNING → COMPLETE | FAILED | BLOCKED | CANCELLED | STOPPED`
plus `UNKNOWN` (reconciliation entry). Transitions are explicit in
`states.TRANSITIONS`; illegal moves raise `InvalidTransition`. `COMPLETE` is
reachable only from `RUNNING` and only through an explicit caller decision —
stopping execution can never produce `COMPLETE`.

Ledger layout (operational state, not canonical knowledge):

```
<state_root>/workers/
  index.yaml            # one-line summary per worker
  records/WRK-*.json    # full worker record per schema
  events.jsonl          # evidence event log
```

## 5. Delegation and authority

`delegation.scope_contains()` performs conservative scope containment: a child
may never claim a term the parent prohibits, and where the parent uses an
explicit allow-list the child must stay inside it. Escalation attempts raise
`PermissionError(SCOPE_ESCALATION_REJECTED | AUTHORITY_ESCALATION_REJECTED)`.
`Supervisor.redirect` refuses to modify scope/authority/tools. `replace()`
clones the original bounded contract — never a wider one.

## 6. Dependencies

`DependencyGraph.declare(a, [b, c])` with cycle detection. Readiness:
`READY` (all deps COMPLETE), `BLOCKED` (deps pending), `POISONED` (a dep
FAILED/CANCELLED/STOPPED → failure propagates; task never runs).

## 7. Parallel execution

`ParallelRunner.run({branch: (worker_id, fn)})` executes branches on a thread
pool, captures per-branch exceptions as `BranchResult(error=...)`, and
aggregates deterministically (`succeeded` / `failed` sorted lists). It does not
lock shared files: conflicting mutations must be coordinated explicitly before
submission.

## 8. Supervision and recovery

All supervisor operations are portable desired actions; actual execution is the
adapter's job. Recovery (`retry | resume | redirect | replace | stop`)
increments `recovery.attempts`, preserves the original error list untouched,
and never widens scope or authority. `replace()` preserves the old record
(including evidence and a replacement pointer) rather than deleting it.

## 9. Parent acceptance

`ParentAcceptor.accept` verifies: child truly COMPLETE; each acceptance
criterion evidenced (explicit `criterion_evidence` mapping or recorded
evidence/output refs — free-text claims alone are not proof); evidence
present; authority unchanged; no unresolved blockers. `aggregate_parent`
requires ALL required children accepted: one child's success cannot hide
another's failure. A child may be COMPLETE while the parent stays unaccepted.

## 10. Context integration (Phase 8)

Delegated tasks default to `SELECTED` context mode. The orchestrator references
`context_package` IDs built by the Phase 8 `ContextBuilder`; no context logic
is duplicated. Note: a minimal change was made to
`13_AUTOMATION/memory_engine/paios_memory/context.py` to allow direct
`store=` lookup in `SELECTED` mode (previously required a `Retriever`); the
Phase 8 suite still passes 17/17.

## 11. Checkpoint integration

`Orchestrator.write_checkpoint(task_id)` builds a Phase 8 `Checkpoint`
containing task identity, worker states, completed work, blockers, next
actions (reconciliation steps for incomplete workers), context package and
authority scope. Logical state only — no process/filesystem snapshotting.

## 12. Runtime adapter boundary

`Executor` defines optional operations; the base class raises
NotImplementedError for all of them. `ExecutorCapabilities.classify(op)`
distinguishes `UNSUPPORTED` (not in the portable contract),
`RUNTIME_UNSUPPORTED` (contract exists, runtime lacks it) and
`RUNTIME_SUPPORTED`. `InlineExecutor` is the reference in-process adapter for
tests. No claim is made that any real runtime supports nested delegation,
model routing, or background execution.

## 13. Stale workers

`Orchestrator.reconcile_after_restart()` marks every `RUNNING` worker found at
process restart as `stale` + `requires_reconciliation`; they are never treated
as complete, prior evidence is preserved, and the dispatcher routes them to
`REDIRECT`.

## 14. Tests

`tests/test_phase9.py` — 30 tests: OR-01..OR-20 plus the 8 adversarial cases
(scope escalation, authority escalation, failed sibling, stale worker, invalid
transition, dependency violation, context leakage, evidence loss).
Run: `cd 13_AUTOMATION/orchestration_engine && python -m unittest tests.test_phase9 -v`
