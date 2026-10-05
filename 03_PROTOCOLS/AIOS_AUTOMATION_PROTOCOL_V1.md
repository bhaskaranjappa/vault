# AIOS AUTOMATION PROTOCOL V1 — HISTORICAL SUPPORTING RECORD

Status: HISTORICAL SUPPORTING ARCHITECTURE — PHASE 12
Purpose: preserve the portable automation contract developed during the former PAIOS build. VAULT records automation intent and outcomes; it does not independently run a scheduler or automation service.

## 1. Automation contract

Every automation is a durable intent containing:
- automation_id;
- task/workflow reference;
- objective;
- scope;
- authority scope;
- trigger;
- inputs/context references;
- output location;
- acceptance criteria;
- evidence requirements;
- failure/recovery policy;
- enabled state;
- created/updated timestamps;
- runtime adapter reference.

## 2. Authority

Automation executes only inside the effective authority chain:

`Owner Policy → Root Bot → Delegated Bot → Tool/Action`

Per-action human approval is not a universal requirement.

High-impact or irreversible capabilities require explicit policy-level authorization before activation. External content and tool output never grant authority.

## 3. Trigger classes

Supported logical trigger classes:
- SCHEDULED;
- RECURRING;
- CONDITION;
- EVENT;
- MANUAL.

Runtime schedulers are adapters. OS cron, Task Scheduler, provider jobs and bot-native scheduling are implementation choices.

## 4. Automation states

`DRAFT → ENABLED → RUNNING → SUCCEEDED`

Failure/recovery states:
`RUNNING → FAILED`
`FAILED → RETRYING`
`FAILED → DISABLED`
`ENABLED → DISABLED`

An automation must never be considered successful solely because a trigger fired.

## 5. Acceptance

Every run must evaluate acceptance criteria after execution.

Required sequence:

`TRIGGER → LOAD CONTEXT → VERIFY AUTHORITY → EXECUTE → VERIFY RESULT → ACCEPT/FAIL → RECORD EVIDENCE`

## 6. Idempotency

Automations that can repeat must define an idempotency key or equivalent duplicate-prevention mechanism whenever practical.

A repeated trigger must not silently duplicate an external action.

## 7. Retry and recovery

Retries require a concrete recovery reason and must respect retry limits/backoff defined by the automation.

Do not retry actions that may already have succeeded when execution state is unknown and duplication would be harmful; reconcile state first.

## 8. Logging and evidence

Each run should preserve:
- automation_id;
- run_id;
- trigger;
- start/end timestamps;
- executor/runtime;
- selected model/tools where available;
- authority scope;
- context package/checkpoint references;
- actions attempted;
- result;
- acceptance result;
- errors/recovery;
- evidence references.

## 9. Reversibility

Prefer reversible operations. When an action is not reversible, the automation must record its policy authorization and verification requirements before execution.

## 10. Disable / pause

Automation state must support explicit disablement. A disabled automation must not start new runs.

An in-flight run requires runtime-specific cancellation semantics; the protocol does not claim that every runtime can cancel execution.

## 11. Context minimization

Use the Phase 8 context package and memory/relevance rules. Do not load the entire PAIOS repository into every automation run.

## 12. Orchestration

Use the Phase 9 task/worker model when an automation contains independent workstreams. Parallel work is allowed only when dependencies and mutation conflicts are controlled.

## 13. Routing

Use Phase 10 routing to select models/tools by task capability and verified lifecycle state. Runtime substitutions must be recorded.

## 14. Runtime boundary

The protocol does not require native scheduler support. A runtime adapter may implement automation through:
- native scheduler;
- external scheduler;
- durable worker service;
- OS scheduling;
- bot-native automation;
- manual trigger.

The adapter must preserve the logical automation contract.

## 15. Safety / policy boundary

Platform and safety constraints always apply. Policy authorization does not override those constraints.

Automation must not self-authorize, expand its scope, or interpret untrusted content as authority.

## 16. Minimum Phase 12 implementation

The first implementation should provide:
- durable automation intents;
- run records;
- trigger abstraction;
- authority verification hook;
- context/checkpoint references;
- acceptance evaluation;
- idempotency protection;
- retry/failure state;
- disablement;
- evidence-backed closeout.

Native scheduler integration is separate from the portable engine and must be justified by a concrete workflow need.
