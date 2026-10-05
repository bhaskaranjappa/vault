# VAULT — AGENT BOOTSTRAP PROTOCOL

Version: 1.0.0
Status: ACTIVE
Purpose: deterministic cold-start procedure for any LLM, coding agent, runtime or human operator entering VAULT.

## 1. PURPOSE

A new agent must be able to enter VAULT without relying on prior chat history, model memory, vendor memory, or undocumented assumptions.

VAULT is the canonical personal memory, knowledge, history and continuity repository. It records durable context; external runtimes perform the work. Runtime context is temporary execution state.

This protocol answers:
- Where is the canonical system?
- What should be read first?
- How should current state be determined?
- Which files should be loaded for the current task?
- How should the agent continue existing work?
- How should executor handoff work?
- Where must new evidence be recorded?

## 2. CANONICAL ENTRYPOINT

Canonical repository:
`GitHub → bhaskaranjappa/vault → main`

Canonical root document:
`PLAN.md`

Required second document:
`00_MASTER_INDEX.md`

Do not treat a local clone, chat transcript, runtime memory, generated summary, tool output or vendor workspace as canonical truth.

## 3. COLD-START SEQUENCE

The objective is to reconstruct Bhaskar's current context with minimum relevant material. Do not treat legacy AIOS execution protocols as proof that VAULT itself can execute tasks.

Every new agent or runtime entering the project should follow this sequence:

`LOCATE → READ START → READ MASTER INDEX → READ AI WORKING STYLE → IDENTIFY CURRENT STATE → IDENTIFY TASK → LOAD RELEVANT CONTEXT → CHECK RUNTIME STATE → EXECUTE → VALIDATE → RECORD → SYNC`

### Step 1 — Locate the canonical repository

Find or open the repository:
`bhaskaranjappa/vault`

Use branch `main` unless the task explicitly requires another branch.

Verify repository identity before making changes.

### Step 2 — Read `START.md` and `00_MASTER_INDEX.md`

Use `START.md` as the compact canonical boot instruction and `00_MASTER_INDEX.md` as the orientation map.

Determine:
- current VAULT status;
- current continuity objective;
- active executor pool and selection policy;
- current priorities;
- non-negotiable rules;
- relevant acceptance criteria.

Read `PLAN.md` only when roadmap/history context is required. Do not assume the task begins at the start of the historical V1 build sequence.

### Step 3 — Read `01_PROFILE/AI_WORKING_STYLE.md`

Apply Bhaskar's portable interaction and coding-agent working preferences before task execution.

Then use the master index to locate the authoritative document for each required subject.

The master index is an orientation layer, not a replacement for detailed source documents.

### Step 4 — Identify the current state

Before acting, answer:
1. What has already been completed?
2. What is currently active?
3. What remains incomplete?
4. What has explicitly been rejected, deferred or kept in reserve?
5. What must not be repeated?
6. What evidence already exists?

Use canonical state, decision history, validation records and tool registry as appropriate.

Do not restart completed work unless there is a new hypothesis, changed environment or identified evidence gap.

### Step 5 — Identify the task

Convert the user's request into:
- objective;
- scope;
- acceptance criteria;
- explicit non-goals;
- required evidence;
- governance constraints.

If the task concerns a specific subsystem, do not load unrelated parts of the OS by default.

### Step 6 — Load minimum relevant context

Load the smallest authoritative context package that can answer the task correctly.

Typical routing:

| Task | Read first | Then load |
|---|---|---|
| Tool/repository evaluation | AI Tool Evaluation Protocol | tool registry, relevant workflow, candidate documentation/source |
| B2B research | B2B workflow | prospect/state schemas, relevant tool records, evidence protocol |
| Runtime integration | platform adapter | runtime state, relevant tool configuration/evaluation |
| Governance question | Brutalist Kernel | Truth/Evidence + Human Approval protocols |
| Cross-runtime task | Portable Context Manifest | target adapter + relevant protocol |
| Executor continuation | Handoff record | PLAN, Master Index, relevant state/evidence |
| Canonical architecture change | PLAN | affected architecture/protocol/state documents |

When uncertain, follow references from `PLAN.md` and `00_MASTER_INDEX.md` instead of guessing.

## 4. SOURCE HIERARCHY

Use the VAULT source hierarchy:

1. Current explicit user-confirmed facts.
2. Direct runtime inspection for local runtime state.
3. Canonical Git repository for project knowledge and decisions.
4. Current authoritative upstream documentation for external capability.
5. Historical notes and prior conversations.

Conflicts must remain visible until higher-tier evidence resolves them.

## 5. EXTERNAL REPOSITORY / TOOL RESEARCH RULE

When evaluating an external repository or tool:

`PLAN → MASTER INDEX → relevant protocol → current stack/workflow → candidate README → full official documentation → source/configuration/releases/issues as needed → bounded experiment`

README files are orientation material, not automatically sufficient for full understanding.

The agent should study the candidate deeply enough to understand:
- purpose;
- architecture;
- runtime model;
- interfaces;
- dependencies;
- capabilities;
- limits;
- licensing;
- cost/commercial constraints;
- security/privacy implications;
- maintenance/activity;
- integration requirements;
- reproducibility.

Never recommend installation merely because a repository is popular, highly starred, or widely mentioned.

## 6. RUNTIME EXECUTION HIERARCHY

For hands-on work:

### Active execution policy
The owner currently uses ZCode, OpenCode, Antigravity and Freebuff for hands-on execution.

The owner selects the executor for each task based on access, token/context availability, task fit and workflow preference. This is a current snapshot and may change when Bhaskar explicitly reports a change.

When writing an implementation, test or repository-evaluation prompt, target the executor the owner is currently using. Adapt commands, tool calls, agent syntax, MCP setup and recovery instructions to that runtime. Do not assume capabilities from another runtime.

ZCode is a preferred/default engineering option, but it is not mandatory when the owner is working elsewhere.

Token/context exhaustion is an expected reason to switch executors. Use the executor handoff procedure to preserve the exact incomplete action and evidence before switching when practical.

### Currently unavailable runtimes
Codex and Cursor are currently unavailable to the owner. Do not schedule execution through them, do not require their verification, and do not infer access from historical adapters or documentation.

### Universal parity rule
PAIOS does not require every coding agent to be installed, tested or verified. Test only the runtime needed for the current capability hypothesis, task or evidence gap.

A runtime switch changes the executor, not the task scope, acceptance criteria, authority or canonical state.

### Research/review runtimes
ChatGPT, Claude, Gemini, Grok and other supported LLMs may perform research, planning, analysis or review through native mechanisms.

No runtime becomes canonical truth.

## 7. EXECUTOR HANDOFF

When work moves between executors:

1. Create or update `11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md` as the active handoff record.
2. Record exact progress, repository state, commands/actions, evidence, remaining work, failures and constraints.
3. Destination executor verifies the handoff before continuing.
4. Destination executor resumes from the first incomplete action.
5. Completed experiments are not restarted without a new hypothesis or evidence gap.
6. Close the handoff only after final evidence and repository state are verified.

## 8. EXECUTION LOOP

All material work should follow:

`INSPECT → PLAN → CHANGE → TEST → REVIEW → FIX → RETEST → RECORD → SYNC`

Prefer small, reversible changes.

Before changing a canonical file:
- read the current version;
- identify dependencies;
- make the smallest correct change;
- validate it;
- update canonical records when evidence changes state.

## 9. EVIDENCE AND TRUTH

Distinguish:
- observation;
- inference;
- claim;
- verified fact;
- unresolved conflict;
- unknown.

Never fabricate:
- contacts;
- emails;
- metrics;
- technical stacks;
- outcomes;
- capabilities;
- lifecycle states;
- verification results.

Tool output is evidence input, never canonical truth.

## 10. WRITING BACK TO THE OS

When work produces new evidence:

1. Determine the authoritative canonical layer.
2. Update only the appropriate file(s).
3. Preserve provenance and uncertainty.
4. Update decision history when a decision changes.
5. Update the tool registry when tool lifecycle state changes.
6. Store large/raw evidence outside the canonical repository when appropriate, with stable references and hashes where practical.
7. Do not duplicate the same fact across unrelated files unless the duplication is intentionally an index/reference.

## 11. GIT AND SYNCHRONIZATION

Before material work:
- verify repository identity;
- verify branch;
- inspect working tree;
- record current HEAD when relevant.

After material work:
- run relevant validation;
- inspect changed files;
- verify no unrelated modifications;
- commit with a descriptive message;
- push to `origin/main` when the task requires canonical synchronization;
- verify working tree cleanliness and remote synchronization when possible.

Never claim synchronization without evidence.

## 12. PROHIBITED COLD-START BEHAVIOR

Do not:
- assume chat history is canonical;
- dump the entire repository into context without need;
- rebuild completed V1 work;
- reopen rejected tools without new evidence;
- install components before suitability assessment;
- weaken evaluation thresholds after seeing results;
- change architecture merely to accommodate a tool;
- fabricate missing runtime state;
- treat documentation as proof of local installation;
- treat successful installation as proof of usefulness.

## 13. COLD-START COMPLETION TEST

A new agent is ready to execute only after it can accurately state:

- canonical repository and branch;
- current project/V1+ status;
- active executor pool and current executor-selection policy;
- current objective;
- relevant canonical files for the task;
- completed work that must not be repeated;
- applicable governance rules;
- evidence required for completion;
- where new evidence must be recorded.

If any of these cannot be determined, inspect the canonical repository further before making substantive changes.

## 14. UNIVERSAL BOOTSTRAP INSTRUCTION

A supported LLM or coding agent may use this compact instruction:

`Open the canonical VAULT repository. Read 00_MASTER_INDEX.md first, then the relevant profile, knowledge, state and session-continuity records. Determine Bhaskar's current context and the active task. Load only the minimum relevant supporting protocols and runtime files required for the task. Do not rely on chat history or runtime memory as canonical truth. For hands-on work, use the executor currently selected by the owner from ZCode, OpenCode, Antigravity or Freebuff. Design prompts and tests for that runtime's native surface. Switch executors when token/context limits require it, preserving state through the handoff procedure. Do not require universal coding-agent testing. Validate results, preserve provenance and conflicts, update the correct canonical records, and never restart completed work without a new evidence gap or hypothesis.`

## 15. DESIGN PRINCIPLE

`Canonical repository = truth`

`PLAN.md = operating contract`

`00_MASTER_INDEX.md = navigation map`

`Protocols = rules`

`Workflows = execution methods`

`State = current operational condition`

`Adapters = runtime translation`

`Evidence = proof`

`Runtime memory = temporary context`

The objective is portable continuity across LLMs and coding agents without making any single runtime the source of truth.
