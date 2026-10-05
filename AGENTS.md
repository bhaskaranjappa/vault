# VAULT — CODING AGENT ENTRYPOINT

This file is a thin runtime entrypoint. It is not a second source of truth.

VAULT is a personal memory, knowledge and continuity repository. It is not an autonomous runtime or control plane. Coding agents and external tools do the work; VAULT records durable context and evidence.

## Start here

1. Read `PLAN.md`.
2. Read `00_MASTER_INDEX.md`.
3. Read `03_PROTOCOLS/AGENT_BOOTSTRAP_PROTOCOL.md`.
4. Determine the current V1+ objective and active task.
5. Load only the relevant canonical protocols, workflows, state and runtime documents.
6. Inspect Git state before making changes.

## Execution hierarchy

For V1+ hands-on work:
- **ZCode** is the preferred executor.
- **OpenCode** is the secondary/failover executor.
- When ZCode exhausts usable tokens/context, becomes unavailable, or cannot continue reliably, preserve state with `11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md` and resume in OpenCode from the first incomplete action.

## Canonical truth

The canonical project source is:
`GitHub → bhaskaranjappa/vault → main`

Do not treat chat history, runtime memory, generated summaries, tool output or local working state as canonical project truth.

## Non-negotiable rules

- Do not restart completed work without a new hypothesis or evidence gap.
- Do not fabricate facts, evidence, capabilities, contacts, metrics or verification state.
- Do not install tools merely because they are popular or highly starred.
- Apply the relevant protocol before installation or integration.
- Prefer the smallest reversible change.
- Preserve provenance, conflicts and human-approval boundaries.
- Do not commit secrets.
- Validate before declaring success.
- Record material evidence in the appropriate canonical location.

## Tool/repository capability evaluation

For repositories, tools, MCP servers, plugins, skills, sub-agents, orchestration components, browser systems, research systems or engineering utilities used around Bhaskar's workflows, use:
`03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`

The standard path is:
`Capability gap → Discover → Research deeply → Assess → Bounded experiment → ZCode → OpenCode failover if needed → Measure → Review → Decide → Record → Promote → Rebenchmark`

## Completion

Before finishing, verify:
- the requested acceptance criteria are met;
- the correct canonical files were updated;
- relevant tests/evidence exist;
- no unrelated changes were introduced;
- Git state is understood;
- synchronization is reported only when actually verified.
