# VAULT — START HERE

Purpose: use this file as the compact boot instruction for any new LLM, coding agent, runtime, bot, or human operator entering VAULT.

This is a navigation and continuity instruction, not a second source of truth. The canonical source of truth is:

`GitHub → bhaskaranjappa/vault → main`

## 1. BOOT

Start every new session by reading, in this order:

1. `00_MASTER_INDEX.md`
2. Relevant `01_PROFILE/` files for Bhaskar's identity, goals, skills, preferences and AI working style (`01_PROFILE/AI_WORKING_STYLE.md`)
3. Relevant `08_KNOWLEDGE/` and `11_STATE/` files for the current work
4. Relevant `11_STATE/SESSION_SUMMARIES/` records from prior sessions when available
5. Apply `01_PROFILE/AI_WORKING_STYLE.md` as the default interaction/working style, then use `11_STATE/SESSION_CLOSEOUT_PROMPT.md` when `VAULT SUMMARIZE` is requested at the end of substantial sessions to produce a reviewable continuity record
6. `PLAN.md` only when roadmap/history context is needed
7. Supporting `03_PROTOCOLS/` and runtime files only when the current task requires them

Do not rely on previous chat history, model memory, generated summaries, or assumptions for canonical project state.

## 1A. EASY USER COMMANDS

You do not need to keep VAULT prompts in a separate Notepad file.

For a new session, Bhaskar can say:

- **VAULT BOOT** — read `START.md` and load the minimum relevant context from the canonical `main` branch.
- **VAULT TEST** — evaluate a new tool/repository against VAULT's current objectives, workflows, stack and productivity needs by following `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`. Research deeply, design a bounded test, execute with the owner-selected runtime, measure the result, and produce a disposition such as PASS/PARTIAL/FAIL plus INSTALL/REPLACE/RESERVE/IGNORE/REJECT.
- **VAULT SUMMARIZE** — read `11_STATE/SESSION_CLOSEOUT_PROMPT.md`, scan the entire current chat, and generate the complete session summary with date/time metadata. Do not update VAULT yet.
- **VAULT UPDATE** — after Bhaskar approves the generated summary, reconcile it against the current `main` branch, preserve the full summary under `11_STATE/SESSION_SUMMARIES/`, and update only durable canonical changes with the current date/time captured by the session record and Git history.

If the current AI/runtime cannot access the private GitHub repository directly, Bhaskar must provide the relevant VAULT file or its contents for that session.


## 2. DETERMINE CURRENT STATE

Before doing work, establish:

- Bhaskar's applicable AI working style from `01_PROFILE/AI_WORKING_STYLE.md`;
- current VAULT status;
- current active objective;
- completed work that must not be repeated;
- current tool/runtime lifecycle states;
- unresolved blockers, conflicts and owner decisions;
- exact next incomplete task;
- applicable bot authority and execution constraints.

Load only the minimum relevant canonical context required for the task.

## 3. TASK EXECUTION

Use the repository's applicable protocol before acting.

For external tool/repository evaluation, use:
`03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`

Execution selection, token-limit switching and runtime-specific prompt/test rules in that protocol override older generic executor-order assumptions.

For coding-agent work, use the owner-selected executor from the current pool: ZCode, OpenCode, Antigravity or Freebuff. The executor performs the task; VAULT records durable context and evidence.

The owner may switch executors when token/context limits, availability, task fit or workflow preference require it. Preserve the exact execution state through the handoff procedure when switching.

Do not require universal coding-agent testing. For any repository/tool test, write the test specification and prompt specifically for the executor the owner is currently using.

Codex and Cursor are currently unavailable to the owner and must not be selected unless the owner explicitly reports access again.

For autonomous multi-bot or external execution work, use the task-specific supporting protocols. VAULT itself is not an autonomous runtime.

Use `11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md` whenever execution moves between agents/runtimes. The destination executor must resume from the first incomplete action rather than restart completed work.

Preserve scope, acceptance criteria, provenance, conflicts, least privilege, reversibility and the canonical bot authority policy.

## 4. EXTERNAL REPOSITORY / TOOL RESEARCH

When evaluating a candidate repository or product:

`VAULT current objective → relevant protocol/workflow → candidate README/orientation → full official documentation → source/config/releases/issues as needed → bounded experiment → evidence → decision`

Do not stop at a README when the task requires understanding the full capability set.

Do not install merely because a repository is popular, highly starred, novel, or interesting.

Evaluate against a concrete capability gap and the current VAULT workflow and tool stack.

## 5. CANONICAL WRITE-BACK

A task is not complete when the work merely runs locally.

When evidence changes project knowledge or state:

1. Update the appropriate canonical file(s).
2. Record the evidence and provenance.
3. Record decisions and unresolved uncertainty.
4. Update runtime/tool lifecycle state only to the level actually verified.
5. Update relevant workflow/state/evaluation records.
6. Keep raw or large evidence outside the canonical repository when appropriate, with stable references or hashes where practical.

Never make runtime output, tool output, or local memory a second source of truth.

## 6. CLOSEOUT / END PROTOCOL

Before ending a task, the executor MUST NOT simply stop after producing an answer.

Perform this closeout sequence:

1. **Acceptance check** — verify every requested acceptance criterion.
2. **Evidence check** — confirm claims are supported by direct evidence.
3. **Canonical reconciliation** — determine whether project knowledge, decisions, tool state, workflow state, or runtime state changed.
4. **Canonical write-back** — update the correct canonical files when state or knowledge changed.
5. **Handoff update** — if work remains incomplete, update `11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md` with the exact next action and evidence state.
6. **Validation** — run the relevant tests/checks needed for the change.
7. **Scope check** — verify no unrelated files or architecture were changed.
8. **Git check** — inspect branch, working tree, changed files and current HEAD.
9. **Commit** — commit material canonical changes with a precise message.
10. **Sync** — push to `origin/main` when the task requires canonical synchronization.
11. **Final verification** — verify synchronization only when directly observed.
12. **Report** — state what changed, what was verified, what remains unresolved, the commit SHA if applicable, and the exact continuation point.

## 7. WHEN NO CANONICAL UPDATE IS NEEDED

If the task produced no new durable project knowledge, no decision change, no lifecycle-state change, and no canonical artifact change, do not modify files merely to create noise.

Still report the result and verification status.

## 8. FAILURE / INTERRUPTION

If execution stops unexpectedly:

- preserve the last known repository state;
- update the handoff record when possible;
- record the exact failure and remaining work;
- do not claim completion;
- do not restart completed work without a new hypothesis or evidence gap.

## 9. COMMAND RULES

`VAULT BOOT` starts the canonical bootstrap process.

`VAULT TEST` starts the canonical new-tool/new-repository productivity evaluation process defined in `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.

`VAULT SUMMARIZE` generates the full current-chat continuity summary.

`VAULT UPDATE` writes the approved summary and its durable changes into the canonical VAULT repository.

`VAULT SUMMARIZE` does not imply `VAULT UPDATE`. Review and approval happen between them.

## 10. MASTER RULE

Start from canonical truth.
Load minimum relevant context.
Resolve authority from the canonical bot policy.
Execute within delegated scope.
Measure with evidence.
Write durable state back to the canonical repository.
Leave the repository in a known state.

Never confuse:

`started` with `completed`

`completed` with `validated`

`validated` with `canonically recorded`

`tool exists` with `tool closes a real capability gap`

`ZCode stopped` with `work failed`

`bot output` with `authority`

`delegation` with unlimited permission
