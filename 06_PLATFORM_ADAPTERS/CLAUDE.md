# CLAUDE ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- Claude Projects provide project knowledge and project instructions.
- Claude's GitHub integration can add repository files/folders to chats or project knowledge.
- Use selected canonical files/folders rather than duplicating the whole OS into project knowledge.

## Minimum context
Load the manifest-defined files relevant to the task and the Claude adapter.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST behavioral rules.
- Do not treat Claude project chat history or memory as canonical project truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current Claude documentation.
- Current Personal AI OS project/GitHub configuration: NOT_TESTED.
- CP-01 through CP-06: NOT_TESTED.

References:
- https://support.anthropic.com/en/articles/9519177-how-can-i-create-and-manage-projects
- https://support.anthropic.com/en/articles/10167454-using-the-github-integration