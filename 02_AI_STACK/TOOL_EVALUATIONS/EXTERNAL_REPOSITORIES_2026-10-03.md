# PAIOS V1+ EXTERNAL REPOSITORY EVALUATION — 2026-10-03

Status: CANONICAL V1+ evaluation
Task: Evaluate OpenDots/OpenMuse/Munder Difflin/Paperclip for fit with Personal AI OS.
Source of truth: `bhaskaranjappa/personal-ai-os` on `main`.
Evaluation protocol: `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.

## 1. Current PAIOS gap

Phase 14 is the latest implemented canonical phase. Codex CLI is the first directly verified real runtime through the canonical adapter.

The next real integration step is a second authenticated/usable runtime followed by real cross-runtime parity measurement.

Therefore, a candidate is valuable only if it closes a concrete gap around:
- runtime execution and multi-runtime operation;
- orchestration/supervision;
- memory/context;
- automation;
- governance/evidence;
- user-facing agent workspace.

No candidate was installed or promoted during this evaluation.

## 2. Repository identity

The name `OpenDots` is ambiguous. Two materially relevant repositories were evaluated:

1. `diggerhq/opendots` — model-agnostic personal agent on OpenComputer.
2. `CopilotKit/OpenDots` — self-hosted persistent AI coworkers with computers, web/mobile UI, calls and Slack.

The current Munder Difflin repository is `HarnessMD/munder-difflin`; older references under `chaitanyagiri/munder-difflin` resolve to this project.

The relevant Paperclip repository is `paperclipai/paperclip`.

The relevant OpenMuse repository is `tahodev/openmuse`.

## 3. Candidate evaluation

| Candidate | Primary layer | PAIOS overlap | Main incremental value | Main conflict/cost | Disposition |
|---|---|---|---|---|---|
| HarnessMD/munder-difflin | Local multi-agent execution harness | Very high | Wraps many existing terminal-agent CLIs, multi-agent hive, mailbox, memory, supervision and local operation | Duplicates PAIOS orchestration/memory/state; its own god-agent/HITL semantics need an explicit adapter boundary | TEST FIRST |
| paperclipai/paperclip | Agent-team control plane | Very high | Mature task/org/budget/routine/governance control plane with Codex/OpenCode/Claude/etc. adapters and plugins | Large overlap with PAIOS orchestration, automation and governance; risks becoming a second control plane/source of state | KEEP IN RESERVE |
| tahodev/openmuse | Security-primitives personal-agent runtime | Medium | Exact-action approvals, host policy boundary, tamper-evident audit, secret isolation, bounded workers | Exact-action approval model differs from PAIOS policy-level autonomous authority; alpha; native Windows unsupported | KEEP IN RESERVE |
| CopilotKit/OpenDots | Agent workspace/product UI | Medium | Persistent specialist Dots, per-Dot computers, pages, Slack/calls, background work, automatic learning | Heavy CopilotKit/AG-UI/Intelligence/OpenBot stack; alpha; much of this is product/UI rather than PAIOS core capability | KEEP IN RESERVE |
| diggerhq/opendots | Personal-agent UX/runtime | Low-Medium | Topics, persistent notes, cloud computers, model-agnostic agents | Strong OpenComputer dependency; young/early-preview app; not a second verified PAIOS runtime | KEEP IN RESERVE |

## 4. Munder Difflin assessment

Munder Difflin is the closest architectural fit to the current PAIOS execution surface.

Its HIVE model provides per-agent identity/memory, a shared blackboard, mailbox routing, a durable task ledger, worker supervision, bounded hops and a privileged orchestrator. Its README also wraps multiple terminal-agent runtimes, including Codex and OpenCode.

This maps closely to PAIOS Phase 9 and Phase 14 concerns:
`dispatcher → workers → runtime CLIs → evidence`.

The critical integration rule is separation of authority:
- PAIOS remains canonical knowledge and policy.
- PAIOS remains the authority model.
- Munder Difflin may act as an execution/UI harness.
- Munder state must not become canonical PAIOS state.
- Any Munder god-agent must not silently replace the PAIOS root authority model.

The project is active and currently publishes support for multiple CLI agents. Source evidence was reviewed from `README.md`, `HIVE.md`, `SPEC.md`, package metadata and current commit activity.

## 5. Paperclip assessment

Paperclip is a broader control plane than Munder Difflin.

It provides agent org charts, task ownership, atomic checkout, heartbeat execution, budgets, governance, routines, plugins, secrets, activity logs, company portability and adapters for Codex, OpenCode, Claude, Gemini and other runtimes.

It is therefore highly relevant to future B2B operating workflows. However, those same features overlap heavily with existing PAIOS Phase 9, Phase 10 and Phase 12 engines.

The correct architectural relationship would be:
`PAIOS canonical policy/state → Paperclip adapter/execution surface`.

Do not import Paperclip as a second canonical orchestration database without a demonstrated capability gap and explicit authority mapping.

Paperclip's own documentation describes it as a control plane rather than the execution plane. Its current roadmap still marks Memory / Knowledge as partial, so it does not replace the PAIOS memory/context layer.

## 6. OpenMuse assessment

OpenMuse is valuable as a security/reference implementation.

Its strongest ideas are host-enforced policy, one-time exact-action approvals, redacted HMAC hash-chain auditing, process-separated secret handling and bounded workers.

However, its security model intentionally pauses every sensitive action for exact-action user approval. PAIOS instead uses policy-level delegated authority and permits autonomous execution inside that scope.

That difference is architectural, not cosmetic.

OpenMuse is therefore best used as a security benchmark and threat-model reference rather than as the core runtime.

## 7. OpenDots assessment

### CopilotKit/OpenDots

This project is strong at the user-facing agent workspace layer.

It combines persistent specialists, individual agent computers, page/document workspaces, browser tooling, calls, Slack and background work. Its latest activity also includes parallel research/extraction and automatic-learning work.

It can inspire a future PAIOS product surface, but it adds a substantial external stack and does not solve the immediate second-runtime parity gap.

### diggerhq/opendots

This project is simpler and strongly aligned with personal-agent UX.

It delegates long-running topics to OpenComputer agents, stores owner/topic notes, and supports model selection per agent. Its architecture relies on an external OpenComputer service and HTTPS callback setup.

That dependency makes it less attractive as a portable PAIOS execution substrate.

## 8. Decision

For the current PAIOS architecture, the candidates are not interchangeable.

**Best current fit for an external execution harness: Munder Difflin.**

**Best future control-plane reference: Paperclip.**

**Best security-primitives reference: OpenMuse.**

**Best future end-user workspace reference: CopilotKit OpenDots.**

**Digger OpenDots:** useful personal-agent UX reference, but not a current PAIOS priority.

The result is a disposition, not a promotion. No candidate should be installed until a bounded experiment demonstrates incremental value against the live PAIOS baseline.

## 9. Recommended bounded experiment

Test Munder Difflin first, in isolation, against a narrow PAIOS scenario:

1. Register two existing runtimes: Codex and OpenCode.
2. Give the harness one bounded read-only task with explicit acceptance criteria.
3. Confirm whether Munder can dispatch and track both runtimes without owning PAIOS policy/state.
4. Capture runtime identity, task identity, authority propagation, failure handling and evidence.
5. Verify whether Munder's local state can be treated purely as an adapter/runtime cache.
6. Do not promote unless the experiment demonstrates material value not already provided by the PAIOS runtime adapter/orchestration layers.

A real cross-runtime parity test remains blocked until a second runtime is authenticated and usable. Munder cannot be counted as that verification by itself.

## 10. Primary source evidence

- PAIOS canonical state: `PLAN.md`, `00_MASTER_INDEX.md`, `12_VALIDATION/AIOS_PHASE14_STATUS_2026-09-17.md`, `12_VALIDATION/AIOS_PHASE14_REAL_RUNTIME_TESTS.md`.
- Munder Difflin: https://github.com/HarnessMD/munder-difflin
- Digger OpenDots: https://github.com/diggerhq/opendots
- CopilotKit OpenDots: https://github.com/CopilotKit/OpenDots
- OpenMuse: https://github.com/tahodev/openmuse
- Paperclip: https://github.com/paperclipai/paperclip
- Paperclip docs: https://docs.paperclip.ing/

## 11. Evidence limitations

This was a source/documentation/repository evaluation. No candidate was installed, authenticated, or runtime-tested.

Therefore no candidate receives VERIFIED runtime status from this evaluation.


## 11. Follow-up evaluation — Obsidian Memory and agentmemory

This follow-up evaluates two agent-memory repositories identified during the 2026-10-03 research pass.

### 11.1 kkonstvol-lab/obsidian-memory

Repository: https://github.com/kkonstvol-lab/obsidian-memory
Branch reviewed: master
License: MIT
Evaluation depth: README, SKILL.md, AGENTS.md, setup/schema/memory/hooks/graph/operator/qualification/workflow/routing/release references, and supplied assets.

Architecture:
- Markdown + Git are the source of truth.
- wiki/ stores source-backed summaries, entities, concepts, synthesis and domains.
- 12-shared/ and 12-{agent}/ store shared and agent-private operational memory.
- Provenance is explicit through source hashes/manifests and source frontmatter.
- Codex lifecycle hooks provide bounded SessionStart, PostToolUse and PreCompact support.
- Graph, bridge-health and Control Tower outputs are derived/advisory rather than canonical.
- Retrieval/context changes use a qualification-first workflow: baseline → golden set → gap report → minimal read-only trial → shadow result.
- The public repository intentionally does not ship a DB, required vector layer, MCP memory server, job runtime, automatic canonical promotion, or always-on dynamic context.

PAIOS mapping:
- Strong alignment with PAIOS memory/context, provenance, selective context, checkpointing, evidence, canonical-vs-runtime separation and qualification-first governance.
- Useful as an architectural reference and possible human-readable memory/view layer.
- Main risk is duplication: PAIOS already uses Git/Markdown as canonical project knowledge. An Obsidian vault must therefore remain an adapter/view or auxiliary workspace, not a second source of truth.
- Obsidian also adds operational dependencies such as the Obsidian application and recommended plugins.

Disposition: KEEP IN RESERVE
Reason: high architectural relevance, but no demonstrated incremental runtime capability for the current Phase 14 objective. Revisit only for a concrete need for a human-operated knowledge workspace or a measured memory/context gap that its vault workflow uniquely addresses.
Runtime state: NOT_INSTALLED / NOT_TESTED.

### 11.2 rohitg00/agentmemory

Repository: https://github.com/rohitg00/agentmemory
Branch reviewed: main
Current package version reviewed: 0.9.29
License: Apache-2.0
Evaluation depth: README, AGENTS.md, INSTALL_FOR_AGENTS.md, GOVERNANCE.md, ROADMAP.md, SECURITY.md, Codex local/submission docs, pairing recipes, reliability recovery docs, benchmark/eval documentation.

Architecture:
- Local persistent memory server built on iii-engine.
- REST + MCP surfaces, hooks, native skills and a real-time viewer.
- Keyless operation provides BM25 search; local MiniLM embeddings are an explicit opt-in for semantic retrieval.
- Automatic observation capture, event-id deduplication, retry/spool recovery, source redaction, provenance and audit logging are implemented.
- Supports Codex, Claude Code, Cursor, Gemini CLI, OpenCode, Hermes and other agents through adapters.
- Offers graph memory, consolidation, lessons, cross-agent facilities and session/history operations.
- Context injection is optional and disabled by default.
- Native Windows requires the pinned iii-engine v0.22.1 through manual installation, WSL2, or Docker.
- The repository publishes retrieval and scale benchmarks, but those are project-owned measurements and require independent PAIOS reproduction before being treated as validation evidence.

PAIOS mapping:
- Directly targets several current PAIOS PARTIAL/MISSING primitives: persistent memory, semantic retrieval, explicit memory writes, background observation capture, conversation/session retrieval, relevance-oriented search, graph retrieval, provenance and memory lifecycle.
- Its Codex/OpenCode/Hermes integrations make it relevant to the Phase 14 runtime-adapter boundary.
- It can serve as a memory capability provider behind an AIOS adapter, while PAIOS remains canonical policy, authority, project knowledge and durable decision state.
- Its agentId/project scoping is not equivalent to the PAIOS authorization model. PAIOS authority must remain external and canonical.
- Always-on context injection should not be enabled initially. It must pass PAIOS relevance, leakage, evidence and safety qualification first.

Evidence notes:
- The project reports 95.2% R@5 retrieval on LongMemEval-S using BM25 + local MiniLM, versus 86.2% BM25-only; this is retrieval-only evaluation, not end-to-end QA accuracy.
- Its own smaller quality benchmark shows mixed results across retrieval variants, reinforcing the need for a PAIOS-specific baseline contest.
- Release history shows recent hardening. v0.9.28 fixed a cross-agent memory leak under isolated scope, and v0.9.29 added hybrid ranking to recall and additional connector coverage.
- An open issue (#1219) reports 400 errors in the v0.9.29 default OpenAI compression/summarization path when using the configured reasoning model. This affects optional provider-backed compression, not the keyless BM25 path.

Disposition: TEST FIRST
Reason: this is the stronger candidate for closing a real current PAIOS capability gap. The next experiment should be read-only and bounded, compare the existing PAIOS baseline against agentmemory retrieval/capture, and test provenance, private-scope isolation, restart recovery and no-result behavior before any persistent integration.
Runtime state: NOT_INSTALLED / NOT_TESTED.

### 11.3 Combined decision

Do not install either repository as a default PAIOS dependency from documentation alone.

For the current Phase 14 objective:
1. Keep Obsidian Memory as a reference/sidecar architecture unless a concrete knowledge-workspace gap appears.
2. Run a bounded agentmemory experiment first when a memory-specific capability gap is selected for testing.
3. Keep PAIOS canonical truth in GitHub regardless of the experiment result.
4. Do not count agentmemory as a second runtime; it is a memory capability provider and adapter surface.

No runtime installation, authentication, or benchmark execution was performed in this research pass.