# GEMINI ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- Gemini CLI loads hierarchical `GEMINI.md` context files from global, workspace, parent, and relevant subdirectory locations.
- `GEMINI.md` can import additional Markdown files with `@file.md` references.
- Use a concise project-level `GEMINI.md` to route Gemini to task-relevant canonical files.

## Minimum context
Load only task-relevant canonical files plus this adapter.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST rules.
- Gemini memory/context files are runtime context, not canonical project truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current Gemini CLI documentation.
- Current Personal AI OS Gemini configuration: NOT_TESTED.
- CP-01 through CP-06: NOT_TESTED.

References:
- https://geminicli.com/docs/cli/gemini-md/
- https://geminicli.com/docs/cli/tutorials/memory-management/