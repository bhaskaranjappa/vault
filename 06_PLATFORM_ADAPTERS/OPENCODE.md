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
- PAIOS authority remains an external policy layer unless runtime enforcement is directly verified.

## Runtime role
Secondary/failover engineering executor.

Use OpenCode when ZCode is unavailable, exhausted, unreliable, or when an independent execution path materially improves verification.

## Verification status — 2026-09-15
- Runtime: VERIFIED for bounded V1+ validation.
- OpenCode v1.18.30 tested.
- Execution discipline: VERIFIED.
- Parallel execution: VERIFIED.
- Explicit-contract delegation + task resume: VERIFIED.
- Selective context packaging: VERIFIED.
- Untrusted-content behavioral boundary: VERIFIED.
- Native persistent/semantic memory: NOT_SUPPORTED.
- In-runtime per-agent model/reasoning routing: NOT_SUPPORTED.
- Nested delegation beyond depth 1: NOT_SUPPORTED.
- Native automation: NOT_SUPPORTED.
- True snapshot/rollback checkpoint restore: NOT_SUPPORTED.
- Machine-enforced authority scope/identity/revocation: NOT_SUPPORTED.
- GitHub MCP: CONFIGURED but not verified because authentication/configuration was invalid during validation.
- Overall role status: **READY WITH GAPS**.

Evidence: `12_VALIDATION/AIOS_V1PLUS_OPENCODE_EVIDENCE_2026-09-15.md`
