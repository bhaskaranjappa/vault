# AIOS ORCHESTRATION PROTOCOL

Status: CANONICAL V1+
Purpose: define portable multi-agent dispatch, delegation, supervision and per-agent routing derived from Astra and Grok Bot.

## 1. Dispatcher model

The root orchestrator receives the user's objective, resolves the required scope and decides whether to execute directly or delegate.

Default rule:
- simple bounded work → execute directly;
- substantial independent work → delegate;
- independent workstreams → parallelize;
- long-running work → supervise workers and preserve state.

`Grok Bot` is the initial root orchestrator pattern, but the protocol is runtime-independent.

## 2. Task contract

Every delegated task contains:
- task_id;
- parent_task_id;
- objective;
- scope;
- inputs/context;
- allowed tools;
- authority scope;
- constraints;
- acceptance criteria;
- expected output;
- evidence requirements.

## 3. Delegation contract

A parent delegates only the authority required for the task.

The child must:
- inspect its assigned context;
- execute within scope;
- report evidence and status;
- preserve provenance;
- return a structured result;
- surface blockers instead of silently changing scope.

## 4. Hierarchy

Agents may form a hierarchy:

`root → coordinator → specialist → worker`

Nested delegation is allowed only when the parent scope explicitly permits it.

A child cannot grant itself new scope.

## 5. Parallel execution

Independent tasks should run concurrently when the runtime supports it.

Parallelization must not be used when tasks have unresolved dependencies or competing mutations.

## 6. Model routing

Select a model per task/agent using:
- task capability requirements;
- reasoning demand;
- context requirements;
- latency requirements;
- cost constraints;
- reliability evidence.

A model override is an execution choice, not canonical truth.

## 7. Reasoning routing

Where supported, assign reasoning intensity by task complexity:
- low: routine transformation/lookup;
- medium: standard engineering/research;
- high: complex diagnosis/design;
- maximum available: unusually difficult or high-uncertainty work.

Do not spend maximum reasoning on work that does not benefit from it.

## 8. Worker supervision

The dispatcher tracks:
- pending;
- running;
- blocked;
- completed;
- failed;
- cancelled.

For stalled work, the dispatcher may:
- inspect;
- provide corrective context;
- redirect within scope;
- resume;
- stop.

## 9. Context inheritance

Child agents receive the minimum context needed for the task.

Supported inheritance modes:
- none;
- selected task context;
- recent relevant context;
- full context only when justified.

Never dump the entire PAIOS repository into every child by default.

## 10. Completion

A parent accepts child output only after checking:
- acceptance criteria;
- evidence;
- scope compliance;
- authority compliance;
- contradictions;
- result completeness.

Completed child output does not automatically mean completed parent task.

## 11. Recovery

When a worker fails, preserve its evidence and state. Retry when a concrete recovery path exists. Otherwise redirect or replace the worker without losing the parent objective.

## 12. Runtime adapter boundary

Runtime-specific APIs such as `spawn_agent`, `fork_turns`, `SendMessage`, task IDs or provider-specific model names belong in adapters. This protocol defines the behavior they implement.
