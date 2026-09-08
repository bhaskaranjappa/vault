# GROK ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- Grok supports a GitHub connector for repositories and code.
- Use the connected repository as the source for current canonical project knowledge when available.
- For bounded portable context, provide only the manifest-defined files required by the task.

## Minimum context
Load only task-relevant canonical files and this adapter.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST rules.
- Grok connectors and conversation memory are runtime context, not canonical project truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current xAI documentation.
- Current Personal AI OS Grok configuration: NOT_TESTED.
- CP-01 through CP-06: NOT_TESTED.

Reference:
- https://docs.x.ai/grok/connectors