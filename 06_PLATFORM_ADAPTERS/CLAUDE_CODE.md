# CLAUDE CODE ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- Claude Code loads project `CLAUDE.md` instructions into context.
- `CLAUDE.md` can import additional files with `@path/to/file`.
- Use a small project-level `CLAUDE.md` that points Claude Code to the manifest-defined canonical files as needed.

## Minimum context
Load only task-relevant canonical files plus this adapter.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST behavioral rules.
- Runtime memory files are instruction/context mechanisms, not canonical project truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current Claude Code documentation.
- Current Personal AI OS runtime configuration: NOT_TESTED.
- CP-01 through CP-06: NOT_TESTED.

Reference:
- https://docs.anthropic.com/en/docs/claude-code/memory