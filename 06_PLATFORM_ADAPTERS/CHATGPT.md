# CHATGPT ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- ChatGPT Projects can hold project files and project instructions.
- ChatGPT GitHub integration can read the live connected repository.
- Use the GitHub-connected repository for current canonical project knowledge where available.
- Use project files/instructions for minimum portable context when a task requires a bounded context package.

## Minimum context
Load only the manifest-defined files relevant to the task: profile, AI stack, protocols, one workflow, this adapter, and relevant knowledge.

## Rules
- Canonical OS is the source of truth.
- Preserve CURRENT / HISTORICAL / UNVERIFIED / CONFLICTING states.
- Do not silently overwrite canonical knowledge.
- Preserve BRUTALIST behavioral rules.
- Do not treat ChatGPT memory or project chat history as canonical truth.

## Verification status
- Ingestion mechanism: SUPPORTED by current ChatGPT documentation.
- Current Personal AI OS runtime configuration: NOT_TESTED.
- CP-01 through CP-06: NOT_TESTED.

References:
- https://help.openai.com/en/articles/10169521-chatgpt-projects
- https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt