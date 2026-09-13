# PERSONAL AI OS — MASTER INDEX

Version: 1.0.0
Status: V1 RELEASED 2026-09-14 — V1+ ACTIVE
Owner: Bhaskar Anjappa
Last Updated: 2026-09-14

This repository is the canonical, portable personal AI knowledge and operating layer. It is designed to work across AI runtimes without making any single model, chat history, vendor memory system, or agent framework the source of truth.

Primary runtimes: ChatGPT, Claude, Gemini, Grok, Hermes Agent, OpenCode, Cursor, Codex, Claude Code.

Architecture: profile, AI stack, protocols, Hermes runtime, workflows, platform adapters, version tracking, knowledge, specialists, sources, state, validation, automation, cross-platform tests.

Kernel = behavior. Knowledge = known facts. Workflow = execution method. Runtime state = software state. Adapter = platform translation. Provenance = source.

Source hierarchy is fact-type dependent. Current user-confirmed facts outrank older memory; direct runtime inspection outranks documentation for local software state; current explicit Custom Instructions outrank inferred behavior. Conflicts must remain visible.

Status vocabulary: CURRENT, VERIFIED, CLAIMED, UNVERIFIED, CONFLICTING, OUTDATED, HISTORICAL, PROPOSED, REJECTED, UNKNOWN.

Capability lifecycle: SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED.

Never fabricate facts, metrics, outcomes, contacts, email addresses, company details, client history, project results, tool capabilities, or installation/configuration state.

Current goals: B2B GenAI client acquisition and Personal AI OS. Job search is secondary. Content creation, YouTube, Instagram, entrepreneurship, research and broader automation are future/possible.

Hermes v0.21.0 is verified from a fresh runtime audit (2026-09-13); the default profile model is `gemini-2.5-flash-lite` via OpenRouter transport. The earlier Solar/Nemotron model-selection issue is resolved by user confirmation; Nemotron remains historical provenance.

The first five-company B2B research-only benchmark is recorded. Connectsys and MaxHome.ai are the strongest research candidates; no outreach was sent.

## Deployment state

The private GitHub repository `bhaskaranjappa/personal-ai-os` exists and contains the canonical rebuild. Windows clone verification is COMPLETE. The 2026-09-13 validation cycle is complete and canonical: cross-platform tests CP-01..CP-06 executed on OpenCode, Hermes, and the ZCode executor (all scored 2×6); governance battery executed on all three; fresh Hermes runtime state captured; B2B research-only re-validation recorded.

V1 DECLARED 2026-09-14: all release gates PASS with evidence (`12_VALIDATION/V1_RELEASE_GATES.md`). The V1 mandatory runtime set is the owner's actual workflow — ZCode, OpenCode, Hermes — defined by owner decision 2026-09-14 (`07_VERSION_TRACKING/DECISION_HISTORY.md`) per PLAN.md §9/§17. Claude chat and Gemini are NOT_TESTED and non-blocking (not in current workflow); Claude Code is recorded BLOCKED (local API gateway down at test time). Hermes G-06 stale-information failure is recorded as a general model-layer limitation (reproduced on an alternate model 2026-09-13) and classified as a runtime-layer truth-handling limitation, not a Gate G governance failure.

## Cold-start / agent bootstrap

For any new LLM, coding agent, runtime or human operator entering the project, use:
`AGENTS.md` as the thin coding-agent entrypoint and `03_PROTOCOLS/AGENT_BOOTSTRAP_PROTOCOL.md` as the authoritative cold-start procedure.

Bootstrap order:
`Canonical GitHub repository → PLAN.md → 00_MASTER_INDEX.md → AGENTS.md / Agent Bootstrap Protocol → current state → task-specific protocols/workflows/state → runtime state → execute → validate → record → sync`

The bootstrap protocol defines cold-start behavior, minimum relevant context loading, source hierarchy, external repository research order, ZCode-first execution, OpenCode failover, executor handoff, evidence handling and canonical write-back.

## V1+ execution model

The canonical AI Tool / Repository Discovery and Capability-Enhancement Workflow is defined in `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.

Execution roles:
- ChatGPT or another capable research LLM: repository discovery, deep documentation/source study, architecture and suitability analysis, baseline definition, evaluator application, experiment specification and result review.
- ZCode: preferred hands-on executor for installation, runtime experimentation, benchmarking and evidence capture.
- OpenCode: secondary executor and failover runtime when ZCode exhausts usable tokens/context, becomes unavailable, or cannot continue reliably.
- Claude, Gemini, Grok and other supported LLMs: consumers of the portable canonical workflow and evidence; they may perform research, planning or review using their native mechanisms.

Standard pipeline:
`Capability gap → Discover repository/tool → Deep research → Protocol assessment → Bounded test specification → ZCode execution → OpenCode failover if required → Measure → Independent review → PASS/PARTIAL/FAIL → INSTALL/REPLACE/RESERVE/IGNORE/REJECT → Canonical evidence → Runtime integration → Production rebenchmark`

Executor continuity is standardized by `11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md`. A handoff preserves completed work, evidence, repository state, remaining work, failures and constraints so the destination executor resumes from the exact incomplete action rather than restarting.

Capability search is not restricted to MCP. Candidate classes include tools/MCP, skills, sub-agents, orchestration, context/memory, browser/automation, research/extraction and engineering utilities. Candidates are evaluated against a concrete capability gap rather than popularity or tool count.

## Required next steps

1. Maintain GitHub tree and manifest integrity.
2. Verify local reproducibility and Git state.
3. Retest Claude Code when its local API gateway is running; validate other adapters only if they enter the actual workflow (V1+ tasks).
4. Fix failures at the canonical layer or adapter layer; retest Hermes G-06 when a stronger model is available.
5. Use the V1+ capability-enhancement workflow for future repository/tool discovery and evaluation.
6. Promote only evidence-backed components and rebenchmark the enhanced production workflow.
7. Preserve ZCode-first execution with OpenCode failover and standardized handoff state.
8. Treat `AGENTS.md` and `03_PROTOCOLS/AGENT_BOOTSTRAP_PROTOCOL.md` as the standard cold-start entry path for new coding agents and LLM runtimes.
9. V1+ backlog (PLAN.md §20): controlled automation expansion, specialist/prompt library, deeper tool integrations, multi-agent workflows, job-search/content automation, cross-runtime synchronization.

Build principle: Truth → Portability → Reversibility → Leverage → Controlled Autonomy