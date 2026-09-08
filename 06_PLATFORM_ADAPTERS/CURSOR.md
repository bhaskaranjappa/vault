# CURSOR ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- Cursor project rules live under `.cursor/rules` and are version-controlled.
- Cursor also supports project `AGENTS.md`; use the simplest mechanism that preserves the canonical routing model.
- Rules can reference additional files and can be scoped to relevant paths.

## Minimum context
Load only task-relevant canonical files and one Cursor adapter.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST behavioral rules.
- Cursor rules and memories are runtime context, not canonical project truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current Cursor documentation.
- Current Personal AI OS Cursor configuration: NOT_TESTED.
- CP-01 through CP-06: NOT_TESTED.

Reference:
- https://docs.cursor.com/context/rules