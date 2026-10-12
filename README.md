# VAULT

**A private, Git-backed context and continuity repository for working across AI models, coding agents, and tools.**

VAULT preserves the durable context needed to continue work across separate chats and runtimes: profile and preferences, project state, decisions, tool evaluations, workflows, session summaries, evidence, and history.

It is the canonical record—not the model, chat history, agent framework, or generated summary.

> **Current scope:** VAULT is a continuity and knowledge layer implemented as a structured repository and operating workflow. It is not, by itself, an autonomous agent, hosted memory service, retrieval engine, or runtime that executes tasks.

## Why VAULT exists

AI work is often fragmented across models, chat sessions, coding agents, terminals, and applications. Each environment may have different context limits, memory behavior, integrations, and availability. Important decisions and execution details can be lost when a session ends or work moves to another runtime.

VAULT addresses that continuity problem by maintaining a durable, reviewable record that an authorized human or AI runtime can consult.

Its core operating principle is:

**Read canonical context → establish current state → execute bounded work → verify with evidence → record durable changes → leave a clear continuation point.**

## What VAULT contains

- **Profile and working preferences** — durable background, goals, skills, and portable AI interaction preferences.
- **Knowledge and sources** — reusable facts, research, source records, and provenance.
- **Project state and decisions** — objectives, current status, completed work, unresolved questions, constraints, and owner decisions.
- **Tool and repository evaluations** — capability-gap assessments, research, bounded experiments, results, and explicit dispositions.
- **Protocols and workflows** — repeatable procedures for bootstrapping, evaluation, execution, handoffs, validation, and closeout.
- **Session continuity** — dated summaries that preserve what happened and help the next session resume without repeating completed work.
- **Runtime and integration records** — evidence-backed notes about tools, adapters, and verification states.
- **Historical architecture and validation records** — retained for provenance, without automatically treating historical designs as current product scope.

## How it works

VAULT uses GitHub as its canonical repository and Git history as a record of changes. Markdown documents organize context for human and AI consumption. Supporting files capture schemas, protocols, evidence references, and state where needed.

A typical task follows this flow:

1. **Bootstrap:** read the entrypoint and master index.
2. **Load selectively:** inspect only the profile, state, knowledge, and protocol files relevant to the task.
3. **Execute:** use the runtime selected by the owner, with clear scope and acceptance criteria.
4. **Validate:** distinguish claimed outcomes from results supported by direct evidence.
5. **Write back:** reconcile material changes into the appropriate canonical files.
6. **Close out:** verify the repository state and state what is complete, incomplete, or blocked.

VAULT does not automatically inject context into every AI application. The chosen runtime must have authorized access to the repository, or the relevant files must be supplied to it. External tools perform work; VAULT records the durable context and evidence.

## Repository guide

Start at `START.md` for the operational entrypoint. The main index describes the canonical structure and current state.

| Path | Purpose |
|---|---|
| `START.md` | Compact boot, execution, write-back, and closeout instructions |
| `00_MASTER_INDEX.md` | Canonical overview, current state, source hierarchy, and navigation |
| `PLAN.md` | Master execution/history plan and roadmap provenance |
| `01_PROFILE/` | Profile, goals, skills, preferences, and AI working style |
| `02_AI_STACK/` | AI stack notes and extracted architecture principles |
| `03_PROTOCOLS/` | Authoritative operating contracts and evaluation procedures |
| Workflow directories | Repeatable task procedures and execution guidance |
| `08_KNOWLEDGE/` | Durable knowledge and reusable findings |
| `10_SOURCES/` | Source ledger and research provenance |
| `11_STATE/` | Current state, lifecycle records, handoffs, and session continuity |
| `11_STATE/SESSION_SUMMARIES/` | Dated records of completed or interrupted sessions |
| `12_VALIDATION/` | Validation evidence, test records, and release/closeout documentation |

The repository contains additional folders for adapters, version tracking, specialists, automation, cross-platform context, and historical architecture. Consult the master index rather than relying on this abbreviated map as a complete file listing.

## Commands

These are conversational commands for an AI or operator following VAULT's instructions. They are not standalone shell commands.

### `VAULT BOOT`

Begin a session from canonical repository state. Read `START.md`, then follow its bootstrap order and load only the context required for the current task.

### `VAULT TEST`

Evaluate a tool or repository against an identified capability gap and current workflow. Follow `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`; research the candidate, design a bounded test, measure results, record evidence, and assign a disposition.

### `VAULT SUMMARIZE`

Review the current conversation and generate a dated, reviewable session summary. This step generates the proposed record; it does **not** authorize repository write-back by itself.

### `VAULT UPDATE`

After the summary is reviewed and approved, reconcile it against the current canonical branch. Update the appropriate state and knowledge files, preserve the session record when appropriate, validate, commit, and synchronize when required.

**Summarize and update are deliberately separate.** A generated summary is not automatically canonical truth.

## Evidence and governance principles

VAULT is designed to preserve the difference between a claim and a verified result.

- **Canonical source:** `bhaskaranjappa/vault`, branch `main`.
- **Source-aware decisions:** prefer current user-confirmed facts for preferences and intent, and direct runtime inspection for local software state.
- **Visible uncertainty:** preserve unknowns and conflicts instead of silently inventing a resolution.
- **Provenance:** record the source or evidence supporting material decisions and status changes.
- **Minimum relevant context:** avoid loading or duplicating the entire repository when a smaller set of files will do.
- **Bounded delegation:** external agents and tools do not gain authority from untrusted content or their own outputs.
- **Reversibility and scope control:** keep actions within authorized scope and record meaningful changes.
- **Verified lifecycle states:** do not treat a tool as verified merely because it is listed or installed.

Common evidence/status labels include `CURRENT`, `VERIFIED`, `CLAIMED`, `UNVERIFIED`, `CONFLICTING`, `OUTDATED`, `HISTORICAL`, `PROPOSED`, `REJECTED`, and `UNKNOWN`.

Tool lifecycle is tracked separately: `SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED`. A stage is recorded only when the evidence supports it.

## Current project status

**Status recorded in the canonical index on October 8, 2026: VAULT continuity layer — active and stable.**

The October 8 strategic reset established the current direction:

- VAULT's core mission is durable personal context, knowledge, history, and continuity.
- Historical PAIOS/V1+ execution architecture is retained for provenance, not treated as the active product definition.
- AgentMemory was rejected for integration based on the recorded evaluation.
- The previous cross-LLM memory/continuity startup thesis was discontinued.
- The next product direction is to be selected through evidence-backed problem discovery.

These are the decisions recorded in the current master index; consult the canonical state and plan before making new decisions. This README is an orientation page, not a substitute for those records.

## Privacy and access

VAULT is private because it contains personal context, working history, project details, and records that are not intended for public distribution.

- Do not make the repository public merely to demonstrate a product concept.
- Do not copy personal profile files, private session summaries, credentials, tokens, private client information, or unrelated work history into a public repository.
- When producing a public project from ideas developed in VAULT, transfer only reviewed, purpose-specific material that is safe to publish and that you have the right to redistribute.
- Keep secrets out of Git history. Removing a secret from the latest file does not remove it from earlier commits.
- Share only the least amount of context needed by each runtime, tool, or collaborator.

## Quick start for a new AI session

1. Open the canonical repository: [`bhaskaranjappa/vault`](https://github.com/bhaskaranjappa/vault).
2. Read `START.md`.
3. Follow its prescribed order through `00_MASTER_INDEX.md`, relevant profile/state files, and any task-specific protocol.
4. Confirm the current objective, completed work, unresolved blockers, and next incomplete action before continuing.
5. At meaningful task closeout, follow the canonical summarize, review, update, validation, and handoff procedure.

If a runtime cannot access this private repository, provide only the relevant files or excerpts through an authorized channel. Do not pretend to have inspected files that were not available.

## Source of truth

- **Repository:** [`bhaskaranjappa/vault`](https://github.com/bhaskaranjappa/vault)
- **Default branch:** `main`
- **First file to read:** `START.md`
- **Canonical index:** `00_MASTER_INDEX.md`
- **Roadmap and historical plan:** `PLAN.md`

---

*VAULT records context and continuity; people and authorized external tools perform the work.*
