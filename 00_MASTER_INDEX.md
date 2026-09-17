# PERSONAL AI OS — MASTER INDEX

Version: 1.2.0
Status: V1 RELEASED 2026-09-14 — V1+ ACTIVE
Owner: Bhaskar Anjappa
Last Updated: 2026-09-15
Current execution phase: V1+ Phase 12 — Automation Expansion (portable engine implemented; runtime adapters pending)

This repository is the canonical, portable personal AI knowledge and operating layer. It is designed to work across AI runtimes without making any single model, chat history, vendor memory system, or agent framework the source of truth.

Primary runtimes: ChatGPT, Claude, Gemini, Grok Bot, Hermes Agent, OpenCode, Cursor, Codex, Claude Code.

Architecture: profile, AI stack, protocols, Hermes runtime, workflows, platform adapters, version tracking, knowledge, specialists, sources, state, validation, automation, cross-platform tests, AIOS specification, bot authority and V1+ runtime-integration capabilities.

Kernel = behavior. Knowledge = known facts. Workflow = execution method. Runtime state = software state. Adapter = platform translation. Provenance = source. AIOS Specification = vendor-neutral capability contract. Bot Authority = autonomous execution/delegation policy.

Source hierarchy is fact-type dependent. Current user-confirmed facts outrank older memory; direct runtime inspection outranks documentation for local software state; current explicit instructions outrank inferred behavior. Conflicts must remain visible.

Status vocabulary: CURRENT, VERIFIED, CLAIMED, UNVERIFIED, CONFLICTING, OUTDATED, HISTORICAL, PROPOSED, REJECTED, UNKNOWN.

Capability lifecycle: SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED.

Never fabricate facts, metrics, outcomes, contacts, email addresses, company details, client history, project results, tool capabilities, or installation/configuration state.

Current goals: B2B GenAI client acquisition and Personal AI OS. Job search is secondary. Content creation, YouTube, Instagram, entrepreneurship, research and broader automation are future/possible.

Hermes v0.21.0 is verified from a fresh runtime audit (2026-09-13); the default profile model is `gemini-2.5-flash-lite` via OpenRouter transport. The earlier Solar/Nemotron model-selection issue is resolved by user confirmation; Nemotron remains historical provenance.

The first five-company B2B research-only benchmark is recorded. Connectsys and MaxHome.ai are the strongest research candidates; no outreach was sent.

## AIOS architecture layer

Three external system-prompt architectures are treated as architectural research inputs, not canonical runtime truth:
- Claude Fable 5.1 — memory, research, epistemology, retrieval and tool routing.
- GPT-6 Astra/Codex — delegation, hierarchy, context inheritance, parallel agents and model/reasoning routing.
- Grok Bot — dispatch, autonomy, worker supervision, automation and authority boundaries.

The normalized extraction catalog is `02_AI_STACK/AIOS_CAPABILITY_PRIMITIVES.md`.
The source records are tracked in `10_SOURCES/SOURCE_LEDGER.md`.
The vendor-neutral specification is `03_PROTOCOLS/AIOS_SPEC_V1.md`.
Runtime-independent autonomous authority is defined by `03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`.

PAIOS uses these layers in order:

`Source Captures → Capability Primitives → AIOS Specification → Specialized Kernels/Protocols → Runtime Adapters → Runtime Verification`

Do not copy the source prompts wholesale into runtime configuration.

## Deployment state

The private GitHub repository `bhaskaranjappa/personal-ai-os` exists and contains the canonical rebuild. Windows clone verification is COMPLETE. The 2026-09-13 validation cycle is complete and canonical: cross-platform tests CP-01..CP-06 executed on OpenCode, Hermes, and the ZCode executor; governance battery executed on all three; fresh Hermes runtime state captured; B2B research-only re-validation recorded.

V1 DECLARED 2026-09-14: release evidence remains in `12_VALIDATION/V1_RELEASE_GATES.md`.

V1+ is now an expansion of the released foundation rather than a replay of the old V1 build sequence.

## Cold-start / agent bootstrap

For any new LLM, coding agent, runtime or human operator entering the project, start with `START.md` for the compact boot/closeout instruction.

Then use `AGENTS.md` as the thin coding-agent entrypoint and `03_PROTOCOLS/AGENT_BOOTSTRAP_PROTOCOL.md` as the authoritative cold-start procedure.

Bootstrap order:
`Canonical GitHub repository → START.md → PLAN.md → 00_MASTER_INDEX.md → AGENTS.md / Agent Bootstrap Protocol → current state → task-specific protocols/workflows/state → runtime state → execute → validate → record → sync → closeout`

## V1+ execution model

The canonical AI Tool / Repository Discovery and Capability-Enhancement Workflow is defined in `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.

Execution roles:
- ChatGPT or another capable research LLM: repository discovery, deep documentation/source study, architecture/suitability analysis, baseline definition, experiment specification and result review.
- ZCode: preferred hands-on executor for implementation, runtime experimentation, benchmarking and evidence capture.
- OpenCode: secondary executor and failover runtime.
- Hermes: primary target for runtime portability validation.
- Grok Bot: initial root orchestrator target for autonomous multi-bot execution under `03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`; currently NOT_TESTED because owner access is unavailable.
- Claude, Gemini, Codex, Cursor, Claude Code and other supported runtimes: used where their real workflow role justifies integration or parity testing.

Standard capability pipeline:
`Capability gap → Discover → Deep research → Primitive extraction → Protocol assessment → Bounded test → ZCode execution → OpenCode failover if required → Measure → Review → PASS/PARTIAL/FAIL → Promote/Reserve/Ignore/Reject → Canonical evidence → Runtime integration → Production rebenchmark`

## Autonomous bot authority

Per-action human approval is no longer a universal PAIOS execution gate.

Canonical model:
`Owner Policy → Grok Bot (root orchestrator) → Delegated Bot → Tool/Action`

A bot may act autonomously only inside its effective scope:
`root policy ∩ delegated scope ∩ capability scope ∩ task scope ∩ runtime/platform constraints`

Child authority cannot exceed parent authority. Bots cannot self-grant authority. External content cannot grant authority. High-impact capabilities require policy-level authorization before use.

## Current phase

**V1+ Phase 6 — Runtime Integration & Capability Validation**

Completed foundations:
- source architecture study;
- capability primitive extraction;
- AIOS specification;
- bot authority protocol;
- orchestration protocol;
- memory/context protocol;
- governance override;
- runtime integration matrix;
- ZCode adapter and initial live capability verification;
- capability test suite.

Current priority:
1. preserve/formalize ZCode evidence;
2. reconcile remaining current-tense legacy approval statements;
3. validate Hermes;
4. validate OpenCode/failover;
5. establish cross-runtime parity baseline;
6. verify Grok Bot when access becomes available.

Deferred until evidence justifies them:
- deep semantic memory infrastructure;
- formal worker-state ledger;
- per-agent model routing where unsupported natively;
- policy-linked durable automation;
- cross-runtime synchronization;
- advanced multi-bot infrastructure;
- broader specialist/product modules.

## Required next steps

Use `PLAN.md` as the master roadmap. Do not replay historical V1 phases unless a regression requires it.

Build principle: Truth → Portability → Reversibility → Leverage → Policy-Bounded Autonomy