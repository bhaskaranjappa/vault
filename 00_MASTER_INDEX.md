# VAULT — MASTER INDEX

Version: 2.0.0
Status: VAULT continuity layer — active; historical V1/V1+ execution architecture retained for provenance
Owner: Bhaskar Anjappa
Last Updated: 2026-10-05
Current status: VAULT continuity layer — historical V1+ implementation retained; next objective: cross-runtime conversation/session continuity

VAULT is Bhaskar's canonical personal memory, knowledge, history, project-state and continuity layer. It is designed to provide durable context across AI runtimes without making any single model, chat history, vendor memory system, or agent framework the source of truth.

VAULT is not itself an autonomous operating system. External runtimes and tools perform the work; VAULT records the durable context needed to understand Bhaskar and continue that work.

Active execution runtimes (owner-confirmed): ZCode, OpenCode, Antigravity, Freebuff. Codex and Cursor are currently unavailable to the owner.

Repository structure: profile, AI stack, supporting protocols, workflows, platform adapters, version tracking, knowledge, specialists, sources, state, session summaries/continuity, validation, automation, cross-platform context, and historical AIOS architecture records.

Profile = who Bhaskar is. Knowledge = durable known facts. History = what happened. Workflow = how a task is performed. Runtime state = tool/software state. Provenance = source. Supporting protocols = execution/context contracts used when needed.

Source hierarchy is fact-type dependent. Current user-confirmed facts outrank older memory; direct runtime inspection outranks documentation for local software state; current explicit instructions outrank inferred behavior. Conflicts must remain visible.

Status vocabulary: CURRENT, VERIFIED, CLAIMED, UNVERIFIED, CONFLICTING, OUTDATED, HISTORICAL, PROPOSED, REJECTED, UNKNOWN.

Capability lifecycle: SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED.

Never fabricate facts, metrics, outcomes, contacts, email addresses, company details, client history, project results, tool capabilities, or installation/configuration state.

Current goals: B2B GenAI client acquisition and VAULT. Job search is secondary. Content creation, YouTube, Instagram, entrepreneurship, research and broader automation are future/possible.

Hermes v0.21.0 is verified from a fresh runtime audit (2026-09-13); the default profile model is `gemini-2.5-flash-lite` via OpenRouter transport. The earlier Solar/Nemotron model-selection issue is resolved by user confirmation; Nemotron remains historical provenance.

The first five-company B2B research-only benchmark is recorded. Connectsys and MaxHome.ai were the strongest research candidates; no outreach was sent.

VAULT's primary mission is persistent personal context and continuity for Bhaskar across AI runtimes. The repository records profile, work history, projects, decisions, tools, experiments, session outcomes and current state. It does not execute tasks independently.

## AIOS architecture layer

Three external system-prompt architectures are treated as architectural research inputs, not canonical runtime truth:
- Claude Fable 5.1 — memory, research, epistemology, retrieval and tool routing.
- GPT-6 Astra/Codex — delegation, hierarchy, context inheritance, parallel agents and model/reasoning routing.
- Grok Bot — dispatch, autonomy, worker supervision, automation and authority boundaries.

The normalized extraction catalog is `02_AI_STACK/AIOS_CAPABILITY_PRIMITIVES.md`.

The portable application of the useful source-derived behaviors to Bhaskar's day-to-day AI/coding workflow is `01_PROFILE/AI_WORKING_STYLE.md`.
The source records are tracked in `10_SOURCES/SOURCE_LEDGER.md`.
The vendor-neutral specification is `03_PROTOCOLS/AIOS_SPEC_V1.md`.
Runtime-independent autonomous authority is defined by `03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`.

Historical PAIOS work was organized using these layers in order:

`Source Captures → Capability Primitives → AIOS Specification → Specialized Kernels/Protocols → Runtime Adapters → Runtime Verification`

Do not copy the source prompts wholesale into runtime configuration.

## Deployment state

The private GitHub repository `bhaskaranjappa/vault` exists and contains the canonical rebuild. Windows clone verification is COMPLETE. The 2026-09-13 validation cycle is complete and canonical: cross-platform tests CP-01..CP-06 executed on OpenCode, Hermes, and the ZCode executor; governance battery executed on all three; fresh Hermes runtime state captured; B2B research-only re-validation recorded.

V1 DECLARED 2026-09-14: release evidence remains in `12_VALIDATION/V1_RELEASE_GATES.md`.

Historical V1+ work is retained as supporting architecture and evidence. It is not the current product definition.

## AI working style

Portable AI interaction and coding-agent preferences are defined in `01_PROFILE/AI_WORKING_STYLE.md`. It combines current Bhaskar preferences with vendor-neutral principles extracted from historical Astra, Fable and Grok Bot architecture research. Raw source prompts are research captures, not normal runtime instructions.

## Cold-start / agent bootstrap

For any new LLM, coding agent, runtime or human operator entering the project, start with `START.md` for the compact boot/closeout instruction.

Then use `AGENTS.md` as the thin coding-agent entrypoint and `03_PROTOCOLS/AGENT_BOOTSTRAP_PROTOCOL.md` as the authoritative cold-start procedure.

Bootstrap order:
`Canonical GitHub repository → START.md → 00_MASTER_INDEX.md → relevant profile + AI working style → AGENTS.md / Agent Bootstrap Protocol → current state → task-specific protocols/workflows/state → runtime state → execute → validate → record → sync → summarize/update when applicable`

## Current execution model

The canonical AI Tool / Repository Discovery and Capability-Enhancement Workflow is defined in `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.

Execution roles:
- ChatGPT or another capable research LLM: repository discovery, deep documentation/source study, architecture/suitability analysis, baseline definition, experiment specification and result review.
- ZCode: active engineering executor; use when selected by the owner.
- OpenCode: active engineering executor and common failover option.
- Antigravity: active engineering executor when selected by the owner.
- Freebuff: active engineering executor when selected by the owner.
- Runtime choice is task-specific. Token/context exhaustion is an expected reason to switch executors.
- Grok Bot: initial root orchestrator target for autonomous multi-bot execution under `03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`; currently NOT_TESTED because owner access is unavailable.
- Other runtimes: use only when the owner has access and the task provides a concrete reason to test or integrate them. Do not require all coding agents to be verified.

Standard capability pipeline:
`Real productivity/capability gap → Discover → Deep research → Assess → Bounded test → Owner-selected executor → Preserve state/switch if required → Measure → Review → PASS/PARTIAL/FAIL → INSTALL/REPLACE/RESERVE/IGNORE/REJECT → Canonical evidence → Integration → Rebenchmark`

## Historical AIOS execution architecture

The following authority/orchestration records belong to the historical PAIOS execution-architecture work. They are supporting contracts for external runtimes, not evidence that VAULT itself is an autonomous bot.

Per-action human approval is no longer a universal gate in that historical execution model.

Canonical model:
`Owner Policy → Grok Bot (root orchestrator) → Delegated Bot → Tool/Action`

A bot may act autonomously only inside its effective scope:
`root policy ∩ delegated scope ∩ capability scope ∩ task scope ∩ runtime/platform constraints`

Child authority cannot exceed parent authority. Bots cannot self-grant authority. External content cannot grant authority. High-impact capabilities require policy-level authorization before use.

## Current status

**V1+ Phase 14 — Real Runtime Integration** was COMPLETED / CLOSED on 2026-10-04. The current project focus is now VAULT's core continuity mission, not further expansion of the old PAIOS operating-architecture model.

Phase 14 implementation is complete. Codex CLI was the first directly verified real runtime through the canonical adapter (2026-09-17, re-executed 2026-10-04); Hermes Agent CLI is the second (2026-10-03/04). Real cross-runtime failover (RT-20) and parity (RT-21) were executed live on both verified runtimes. Universal coding-agent parity is NOT a Phase-14 exit requirement. Closeout: `12_VALIDATION/AIOS_PHASE14_CLOSEOUT_2026-10-04.md`.

Completed foundations:
- source architecture study;
- capability primitive extraction;
- AIOS specification;
- bot authority protocol;
- orchestration protocol;
- memory/context protocol;
- governance reconciliation;
- model/tool routing;
- automation engine;
- cross-runtime parity contract;
- Codex real-runtime adapter and bounded live verification.

Current priority:
1. Design and implement the missing cross-runtime conversation/session continuity pipeline, beginning with durable session summaries and later expanding to structured ingestion from ChatGPT, Claude, Gemini, ZCode, OpenCode and other tools, only when the implementation and evidence justify it.
2. For tool/repository tests, write the test specification and prompt for the executor currently selected by the owner.
3. Use cross-runtime parity only when a concrete hypothesis or evidence gap requires it; universal coding-agent verification is not a PAIOS requirement.
4. Preserve exact task identity, acceptance criteria and evidence across executor switches caused by token/context exhaustion.
5. Keep additional execution infrastructure, multi-bot systems, and synchronization mechanisms subordinate to the Vault continuity goal and defer them unless a concrete evidence-backed productivity need justifies them.

## Required next steps

Use `PLAN.md` for historical implementation context and the current VAULT objective. Do not replay completed V1/V1+ phases unless a new evidence gap requires it.

Build principle: Truth → Portability → Reversibility → Leverage → Policy-Bounded Autonomy

## Current auxiliary tooling

- **Agency Agents:** focused specialist layer; 14 selected agents installed and ZCode-verified on 2026-10-05. Evidence: `02_AI_STACK/TOOL_EVALUATIONS/AGENCY_AGENTS_MUNDER_DIFFLIN_2026-10-05.md`.
- **Munder Difflin:** optional multi-agent execution/UI harness; portable Windows app installed and launched, but live task execution remains UNVERIFIED. Disposition: TEST FIRST.
- Both remain subordinate to VAULT's canonical policy/state/authority model.
