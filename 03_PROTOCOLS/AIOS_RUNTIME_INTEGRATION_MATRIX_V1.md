# AIOS RUNTIME INTEGRATION MATRIX V1

Status: CANONICAL
Purpose: map the vendor-neutral AIOS specification to runtime-specific implementation surfaces.

## 1. Integration rule

The AIOS Specification defines portable behavior. Runtime adapters translate that behavior into native mechanisms. Runtime capability never becomes canonical authority.

Pipeline:

`AIOS_SPEC → Runtime Adapter → Native Runtime Mechanism → Verified Evidence`

## 2. Runtime roles

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
| Codex | Engineering/runtime consumer | MEDIUM |
| Cursor | Coding/runtime consumer | MEDIUM |

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
Implement agent/context/model-routing contracts through native sub-agent, planning, tool, session and permission mechanisms. ZCode remains the preferred hands-on executor.

### OpenCode
Implement the same contracts through AGENTS.md, native agents/tasks, skills, MCP, TodoWrite, permissions and available hooks/background mechanisms. OpenCode remains controlled failover.

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
- memory/context contract.

Next runtime work:
1. Grok Bot adapter refinement for root orchestration.
2. ZCode implementation specification and bounded test.
3. Hermes implementation specification and bounded test.
4. OpenCode failover implementation specification and bounded test.
5. Lightweight ChatGPT/Claude/Gemini modules.
6. Cross-runtime parity tests for the new capabilities.
