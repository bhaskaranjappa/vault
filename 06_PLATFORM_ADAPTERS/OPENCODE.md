# OPENCODE ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- OpenCode uses `AGENTS.md` as its persistent instruction mechanism.
- Global instructions can live under the OpenCode global configuration directory.
- Project instructions belong in a repository-level `AGENTS.md` and can reference task-relevant canonical files for lazy loading.
- Use one concise project instruction entry to route OpenCode to the canonical manifest and relevant files.

## Minimum context
Load only task-relevant canonical files plus this adapter.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST behavioral rules.
- OpenCode instruction/configuration files are runtime context, not canonical project truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current OpenCode documentation.
- Installed OpenCode v1.18.29 configuration: NOT_TESTED in this current validation cycle.
- CP-01 through CP-06: NOT_TESTED.

References:
- https://opencode.ai/v2/docs/instructions
- https://opencode.ai/v2/docs/agents