# CODEX ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- Codex supports repository-level `AGENTS.md` instructions.
- Codex project initialization can generate an `AGENTS.md` scaffold.
- Use a concise root `AGENTS.md` to route Codex to the manifest-defined canonical files as needed.

## Minimum context
Load only task-relevant canonical files plus this adapter.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST behavioral rules.
- Codex instruction files are runtime context, not canonical project truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current OpenAI Codex documentation.
- Current Personal AI OS Codex configuration: NOT_TESTED.
- CP-01 through CP-06: NOT_TESTED.

References:
- https://openai.com/index/introducing-codex/
- https://github.com/openai/codex