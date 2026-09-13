# EXECUTOR HANDOFF TEMPLATE

Purpose: preserve execution continuity when a task moves from ZCode to OpenCode or another supported executor.

This is runtime state, not canonical project truth. Update it during an active handoff and preserve the final evidence in the appropriate canonical record.

## Handoff metadata

- Handoff ID:
- Date/time:
- Source executor:
- Destination executor:
- Reason: `TOKEN_EXHAUSTED / CONTEXT_LIMIT / UNAVAILABLE / FAILURE / OTHER`
- Repository:
- Branch:
- HEAD commit:
- Working tree state:

## Task

- Objective:
- Scope:
- Acceptance criteria:
- Explicit non-goals:

## Completed work

- Steps completed:
- Files created/modified:
- Commands/actions already performed:
- Tests already run:
- Results obtained:

## Evidence

- Raw evidence locations:
- Canonical evidence locations:
- Logs:
- Hashes/checksums where applicable:

## Remaining work

- Exact next action:
- Remaining files/tasks:
- Remaining tests:
- Expected completion condition:

## Known issues

- Failures:
- Error messages:
- Known hypotheses:
- Unresolved conflicts:
- Security/hygiene concerns:

## Constraints

- Canonical source of truth remains the GitHub repository.
- Do not restart completed experiments without a new hypothesis.
- Do not expand scope merely because executor changes.
- Preserve read-only and least-privilege requirements.
- Do not commit secrets.
- Do not fabricate missing evidence.
- Preserve human-approval boundaries.

## Destination executor instructions

1. Inspect repository state and this handoff first.
2. Verify the reported HEAD, working tree and completed changes.
3. Reconcile evidence before continuing.
4. Continue from the first incomplete action.
5. Keep the original scope and acceptance criteria.
6. Record any discrepancy between this handoff and observed state.
7. Update the handoff as work progresses.
8. Close the handoff only after final evidence is recorded and repository state is verified.
