# AIOS RUNTIME INTEGRATION MATRIX V1

Status: CANONICAL
Purpose: map the vendor-neutral AIOS specification to runtime-specific implementation surfaces.

## 1. Integration rule

The AIOS Specification defines portable behavior. Runtime adapters translate that behavior into native mechanisms. Runtime capability never becomes canonical authority.

Pipeline:

`AIOS_SPEC → Runtime Adapter → Native Runtime Mechanism → Verified Evidence`

## 2. Runtime roles

Execution availability is owner-controlled and task-specific. The matrix describes architectural roles, not a requirement that every runtime be installed, authenticated or verified.

Current owner-confirmed execution pool:
- ZCode
- OpenCode
- Antigravity
- Freebuff
- Freebuff

Codex and Cursor are currently unavailable to the owner. Historical adapter records must not be interpreted as current access.

PAIOS does not require universal runtime parity. Test only the runtime needed for the current task, capability hypothesis or evidence gap.

| Runtime | Primary role | Integration priority |
|---|---|---|
| Grok Bot | Root orchestrator / dispatcher | HIGH |
| Hermes Agent | Autonomous execution runtime | HIGH |
| ZCode | Engineering executor | HIGH |
| OpenCode | Engineering executor / failover | HIGH |
| Claude Code | Coding/runtime consumer | MEDIUM |
| ChatGPT | Research / planning / review | MEDIUM |
| Claude | Research / memory-oriented consumer | MEDIUM |
| Gemini | Research / execution consumer | MEDIUM |
| Codex | Engineering/runtime consumer | CONDITIONAL |
| Cursor | Coding/runtime consumer | CONDITIONAL |

## 3. Portable capability groups

### A. Governance and truth

Required everywhere:
- source hierarchy;
- provenance;
- conflict preservation;
- fact/claim/inference separation;
- no fabrication;
- current-state verification when freshness matters;
- untrusted-content boundary.

### B. Bot authority

Required for autonomous runtimes:
- stable bot identity;
- explicit capability scope;
- delegated authority;
- delegation chain;
- expiration/revocation;
- prohibited actions;
- task-bound authority;
- audit/evidence.

Root orchestrator: Grok Bot.

### C. Agent orchestration

Required for agentic runtimes:
- task decomposition;
- bounded delegation;
- parallel execution;
- specialist roles;
- worker supervision;
- resume/redirect/stop;
- nested delegation where supported;
- completion verification.

### D. Model routing

Where native runtime support exists:
- select model by task capability;
- select reasoning effort by task complexity;
- allow per-agent model assignment;
- record selected model and reason when material.

### E. Memory and context

Required architecture:
- task-relevant retrieval;
- relevance gating;
- stated-vs-inferred separation;
- current context precedence;
- selective context inheritance;
- checkpoint/restore;
- compaction/state continuity.

### F. Tool routing

Preferred routing order:

`existing canonical/internal data → connector/MCP → authoritative web → browser/desktop → user-only information`

A runtime may alter the mechanical order only when its native surface requires it; the authority and truth rules remain unchanged.

## 4. Adapter implementation targets

### Grok Bot
Implement as root dispatcher using native agent/tool/automation surfaces. Preserve delegated authority and worker state across all child bots.

### Hermes Agent
Implement authority-aware orchestration, memory relevance, execution discipline and context selection through Hermes-native configuration/plugins/tools where verified.

### ZCode
Implement agent/context/model-routing contracts through native sub-agent, planning, tool, session and permission mechanisms. ZCode is an active owner-selected engineering executor.

### OpenCode
Implement the same contracts through AGENTS.md, native agents/tasks, skills, MCP, TodoWrite, permissions and available hooks/background mechanisms. OpenCode is an active owner-selected engineering executor and may be used directly or after token/context exhaustion elsewhere.

### Antigravity / Freebuff
Treat as active owner-selected engineering executors. Inspect their native runtime mechanisms at task time. Do not infer parity from another runtime.

### ChatGPT / Claude / Gemini / other chats and projects
Use lightweight modules derived from AIOS_SPEC. Inject only the task-relevant kernel plus project context. Never require the entire AIOS specification to be pasted into ordinary conversations.

## 5. Verification model

For each runtime and capability group record:
- documented support;
- local availability;
- configuration state;
- authentication state;
- verified behavior;
- evidence source;
- test ID;
- limitations.

Use `NOT_TESTED / PARTIAL / PASS / FAIL` for behavioral verification.

## 6. Current implementation status

Established:
- AIOS capability primitive catalog;
- AIOS vendor-neutral specification;
- bot authority protocol;
- orchestration contract;
- memory/context contract;
- **Phase 14 real-runtime adapter contract (COMPLETED / CLOSED 2026-10-04)**: portable adapter layer at `13_AUTOMATION/runtime_parity/paios_runtime/` with two live-verified real runtimes — Codex CLI (2026-09-17, re-executed 2026-10-04) and Hermes Agent CLI (2026-10-03/04) — plus real cross-runtime failover (RT-20) and parity (RT-21). Universal coding-agent parity is NOT required.

Runtime verification state (behavioral, owner-access-dependent):
- Codex CLI: VERIFIED (live evidence; owner planning policy may still restrict task use).
- Hermes Agent CLI: VERIFIED (Nous Portal auth, free-tier model).
- OpenCode: CLAIMED / execution UNVERIFIED (recorded probe hang).
- Grok: NOT_TESTED (no owner access at last probe).
- Kimi: CLAIMED (quota-blocked at last probe).
- Grok Bot adapter refinement for root orchestration: deferred until runtime access exists (NOT_TESTED — access limitation, not an implementation defect).
