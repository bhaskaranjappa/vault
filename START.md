# PERSONAL AI OS — START HERE

Purpose: use this file as the compact boot instruction for any new LLM, coding agent, runtime, bot, or human operator entering the Personal AI OS.

This is a navigation and operating instruction, not a second source of truth. The canonical source of truth is:

`GitHub → bhaskaranjappa/personal-ai-os → main`

## 1. BOOT

Start every new session by reading, in this order:

1. `PLAN.md`
2. `00_MASTER_INDEX.md`
3. `03_PROTOCOLS/AGENT_BOOTSTRAP_PROTOCOL.md`
4. `03_PROTOCOLS/AIOS_SPEC_V1.md`
5. `03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`
6. The task-specific protocol, workflow, state and runtime files identified by the bootstrap procedure.

Do not rely on previous chat history, model memory, generated summaries, or assumptions for canonical project state.

## 2. DETERMINE CURRENT STATE

Before doing work, establish:

- current V1/V1+ status;
- current active objective;
- completed work that must not be repeated;
- current tool/runtime lifecycle states;
- unresolved blockers, conflicts and owner decisions;
- exact next incomplete task;
- applicable bot authority and execution constraints.

Load only the minimum relevant canonical context required for the task.

## 3. TASK EXECUTION

Use the repository's applicable protocol before acting.

For V1+ capability or repository evaluation, use:
`03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`

Execution selection, token-limit switching and runtime-specific prompt/test rules in that protocol override older generic executor-order assumptions.

For coding-agent work, use the owner-selected active executor from the current pool: ZCode, OpenCode, Antigravity or Freebuff.

The owner may switch executors when token/context limits, availability, task fit or workflow preference require it. Preserve the exact execution state through the handoff procedure when switching.

Do not require universal coding-agent testing. For any repository/tool test, write the test specification and prompt specifically for the executor the owner is currently using.

Codex and Cursor are currently unavailable to the owner and must not be selected unless the owner explicitly reports access again.

For autonomous multi-bot work, use:
`Grok Bot → delegated bots`

Use `11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md` whenever execution moves between agents/runtimes. The destination executor must resume from the first incomplete action rather than restart completed work.

Preserve scope, acceptance criteria, provenance, conflicts, least privilege, reversibility and the canonical bot authority policy.

## 4. EXTERNAL REPOSITORY / TOOL RESEARCH

When evaluating a candidate repository or product:

`Personal AI OS PLAN → relevant protocol/workflow → candidate README/orientation → full official documentation → source/config/releases/issues as needed → bounded experiment → evidence → decision`

Do not stop at a README when the task requires understanding the full capability set.

Do not install merely because a repository is popular, highly starred, novel, or interesting.

Evaluate against a concrete capability gap and the current Personal AI OS stack.

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

## 9. MASTER RULE

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
