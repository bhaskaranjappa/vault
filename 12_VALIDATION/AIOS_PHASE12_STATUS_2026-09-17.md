# AIOS V1+ PHASE 12 STATUS — 2026-09-17

Status: ACTIVE
Phase: Automation Expansion

## Completed before Phase 12

- Phase 8 memory/context implementation + ZCode parity complete.
- Phase 9 orchestration implementation + ZCode validation complete.
- Phase 10 model/tool routing implementation + ZCode validation complete.
- Phase 11 B2B workflow implementation + ZCode validation complete for synthetic data.

## Phase 12 objective

Extend PAIOS automation only where bounded authority, verification, recovery, auditability and acceptance criteria are present.

Primary executor: ZCode.
Failover executor: OpenCode only when ZCode cannot continue reliably.
Hermes live validation: deferred until the end of the broader roadmap.
Grok Bot: NOT_TESTED because runtime access is unavailable.

## Foundation added

- `03_PROTOCOLS/AIOS_AUTOMATION_PROTOCOL_V1.md`
- `12_VALIDATION/AIOS_PHASE12_AUTOMATION_TESTS.md`

## Policy reconciliation

Current-tense automation documents that still encode the obsolete universal approval matrix are being reconciled to the active V1+ governance model.

Active authority model:

`Owner Policy → Root Bot → Delegated Bot → Tool/Action`

Per-action human approval is not universally required. External communication may be autonomous only when owner policy explicitly delegates that capability and scope. Irreversible/high-impact actions require policy-level authorization and remain subject to safety/platform constraints.

## Next execution

Implement the portable automation engine with durable automation intents, run records, trigger abstraction, authority checks, context/checkpoint references, acceptance evaluation, idempotency, failure/retry handling, disablement and evidence-backed closeout.

Native scheduler/runtime integration remains separate.

## Completion gate

AU-01..AU-20 and relevant adversarial tests must have an executable implementation path before Phase 12 can close at the portable layer.
