# PAIOS Automation Engine — Implementation Notes

Portable, runtime-independent automation control layer (`paios_automation`,
stdlib-only) implementing `03_PROTOCOLS/AIOS_AUTOMATION_PROTOCOL_V1.md`.
It is the durable control plane for automation; scheduling and execution
are adapter concerns. It does not duplicate the canonical protocol.

## Architecture

```
Automation Intent (durable, AUT-*.json)
  → Trigger (logical: MANUAL/SCHEDULED/RECURRING/CONDITION/EVENT)
  → Context Loader (Phase 8 SELECTED context package)
  → Authority Check (hook: AuthorityVerifier → AUTHORIZED/UNAUTHORIZED/UNKNOWN)
  → Phase 10 Route (TaskCapabilityProfile → route decision ref on the run)
  → Phase 9 Task/Worker (bounded scopes; parent acceptance validates)
  → Executor Adapter (execute/verify/cancel boundary)
  → Result Verification (COMPLETED/FAILED/UNKNOWN)
  → Acceptance Check (per-criterion, evidence-backed)
  → Run Record (RUN-*.json, append-only history)
  → Checkpoint / Recovery (Phase 8 checkpoint refs; restart reconciliation)
```

## Modules

| Module | Responsibility |
|--------|----------------|
| `automation.py` | `AutomationIntent` (all contract fields + secrets rejection), `AutomationState` machine, `Trigger`/`TriggerType`, `ConditionRegistry` (TRUE/FALSE/UNKNOWN), `AuthorityVerifier` hook, `ExecutorAdapter` boundary, `RunRecord`, `AutomationLedger` (records/ + runs/ persistence) |
| `events.py` | Append-only JSONL event log with the 15 canonical event types |
| `engine.py` | `AutomationEngine` facade: lifecycle, trigger matching, idempotency, run pipeline, acceptance, retry/recovery, untrusted-content boundary |

## Key invariants

- **A trigger firing is not success.** SUCCEEDED requires execution
  completion AND acceptance criteria met with explicit evidence.
- **Authority is a hook, not an assumption.** The engine never invents an
  authorization backend; empty/unverifiable policy yields UNAUTHORIZED or
  UNKNOWN, never silent authorization. External content cannot grant authority.
- **Irreversible actions require policy-level authorization** recorded on
  the automation (`high_impact_policy_authorized`) before `enable()` (AU-05/AU-18).
- **Idempotency:** `automation_id + logical input + execution window`.
  A repeated trigger of a COMPLETED/UNKNOWN/PENDING run with the same token
  raises `DuplicateRunBlocked` — duplicate external actions are prevented
  and explicitly recognized, never silently repeated (AU-08/AD-02/AD-03).
- **UNKNOWN is never retried blindly.** Unknown results require explicit
  `reconcile_unknown()` with preserved evidence before any retry (AU-10/AD-08).
- **Retries are bounded and scope-preserving:** concrete reason required,
  retry limit enforced, same run and same idempotency token — no authority
  or scope expansion (AU-09).
- **In-flight disable is runtime-dependent.** The portable layer refuses
  `disable()` while RUNNING (Protocol §10); disabled automations reject new runs.
- **Untrusted content is data.** Instruction-like retrieved content raises
  `UntrustedContent` and is logged; scope and authority remain unchanged (AU-19).
- **Secrets never persist.** Credential-like values are rejected at intent
  creation and run-record save (`SecretRejected`, AD-05).
- **Stale recovery:** `recover_after_restart()` flags stale RUNNING runs for
  reconciliation instead of resuming them (AU-07/prompt §22).

## Durable state layout

```
<state_root>/
  records/AUT-*.json     automation intents
  runs/RUN-*.json        current run records
  runs/RUN-*.history.jsonl  prior versions (append-only history)
  events.jsonl           evidence event log
```

## Integration

- **Phase 8:** context packages use SELECTED inheritance; minimum relevant
  context only (AU-06). Checkpoints referenced via `run.checkpoint_id` (AU-07).
- **Phase 9:** automations create bounded tasks/workers; parent aggregation
  requires per-worker evidence (AU-16).
- **Phase 10:** per-task routing with the decision reference stored on the
  run record (`record_route`) (AU-17). Runtime substitutions must be recorded.

## Runtime adapter boundary

`ExecutorAdapter` exposes `execute`/`verify`/`cancel`; `cancel` raises by
default — cancellation, scheduling, background work and model switching are
adapter capabilities, never engine assumptions. `InlineNoOpAdapter` is the
reference adapter: it performs no external action and is used by tests so
no real side effect can occur.
