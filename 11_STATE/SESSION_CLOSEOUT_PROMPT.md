# VAULT SESSION CLOSEOUT PROMPT

Purpose: reusable end-of-session prompt for ChatGPT, Claude, Gemini, ZCode, OpenCode, or another AI runtime.

Use this prompt at the end of a substantial chat or coding session to produce a reviewable continuity record. The generated summary is not automatically canonical. After Bhaskar reviews and explicitly approves the summary, reconcile it against the current VAULT repository and update only the durable canonical records that actually changed.

```text
[UNIVERSAL CONTEXT TRANSFER PROTOCOL]

You are a Context Extraction Engine. Read the ENTIRE current conversation from the first message to the last.

Your job is to produce a portable handoff summary that lets a DIFFERENT AI model, coding agent, or new chat continue the work with minimal repeated explanation.

The summary must preserve concrete facts, decisions, execution state, evidence, failures, tools used, and the exact continuation point.

Do not treat chat history, model memory, generated summaries, or assumptions as canonical project truth. The summary is a proposed continuity record that must later be reconciled against VAULT.

OUTPUT ONLY the structured summary below.

---
## CONTEXT
One-line description of the work in this conversation.

## STACK / ENVIRONMENT
Only tools, runtimes, languages, frameworks, versions, repositories, APIs, paths, models, and configuration details that materially affect continuation.

## WHAT'S BEEN DONE
Chronological, concrete record of completed work.
Include exact file/repo names, commands, versions, decisions, important outputs, and finalized code/config when central.
Include failed approaches only when they matter to continuation or must not be repeated.

## CURRENT STATE / PROBLEM
Exactly where the work stands.
Separate:
- VERIFIED
- CLAIMED
- UNKNOWN
- CONFLICTING
- BLOCKED
- INTERRUPTED

Include exact errors, failures, incomplete actions, and current repository/workspace state where known.

## KEY DECISIONS + WHY
Only decisions that constrain future work.
For rejected alternatives, state only the chosen approach and the reason it won.

## TOOL / RUNTIME USAGE
Record the AI runtimes, coding agents, specialist agents, repositories, connectors, and other tools actually used.
State what each tool contributed and whether it was useful, failed, or remains unverified.

## BHASKAR CONTEXT RELEVANT TO THIS SESSION
Record only durable personal context newly established or materially updated in this conversation:
profile, goals, preferences, skills, projects, working style, tool usage, or current priorities.
Do not duplicate unchanged profile information without a reason.

## OPEN THREADS / NEXT STEPS
List the exact remaining tasks in execution order.
Identify the first incomplete action.
Do not restart completed work without a new hypothesis or evidence gap.

## DO NOT
Record anything explicitly ruled out, unsafe, redundant, rejected, or prohibited from future attempts.

## CANONICAL WRITE-BACK CANDIDATES
Identify which VAULT files may need updating after review.
For each candidate file, state the durable fact/state/decision that changed.
Do not rewrite the file.
Do not claim that a file was updated.

## PROVENANCE / CONFIDENCE
For important claims, state where they came from:
conversation observation, user statement, runtime output, repository evidence, external source, or inference.
Mark uncertainty explicitly.

## SESSION METADATA
Session date (YYYY-MM-DD):
Session timezone: Asia/Kolkata (IST, UTC+05:30)
Approximate/exact start time (24-hour, IST):
Approximate/exact end time (24-hour, IST):
Closeout summary generated at (YYYY-MM-DD HH:MM:SS IST):
AI runtime(s):
Coding executor(s):
Project/repository:
Primary task:
Status at close:

---

STRICT RULES:
1. Scan the full conversation, not just recent messages.
2. Never fabricate facts, metrics, files, contacts, outcomes, tool capabilities, or completion state.
3. Preserve exact terminology and important numbers/versions.
4. Distinguish completed from tested, tested from verified, and verified from canonically recorded.
5. Preserve contradictions instead of silently resolving them.
6. Do not assume a generated summary is canonical truth.
7. Capture interruptions caused by token limits, stopped execution, runtime failure, unavailable tools, or deferred work.
8. Identify the exact first incomplete action for continuation.
9. Keep the summary complete enough for a new AI runtime to understand Bhaskar's current context without reading the whole conversation.
10. Record the session date and available start/end/closeout times explicitly so the chronology is clear. Use IST (UTC+05:30) for VAULT timestamps. If an exact time is unavailable, write "unknown" or "approximate" rather than inventing one.
11. Do not add commentary before or after the summary.
```

## Approval and write-back procedure

1. Generate the summary in the current AI conversation.
2. Bhaskar reviews it and explicitly says to update VAULT.
3. The updating AI reads the current VAULT main state and reconciles the approved summary against canonical files.
4. Update only durable profile, project, decision, history, tool-state, session-summary, or current-state records that actually changed.
5. Preserve the approved raw session summary as a provenance record when appropriate.
6. Never overwrite a higher-confidence canonical fact with a lower-confidence conversation inference.
7. Validate the changes, inspect Git state, commit, synchronize to main when required, and report the exact result.

The session summary is a bridge between an AI conversation and VAULT, not a replacement for canonical reconciliation.


## Quick access

In any new AI session, ask the AI to read the canonical repository `bhaskaranjappa/vault` on `main`, then open:

`11_STATE/SESSION_CLOSEOUT_PROMPT.md`

At the end of a substantial session, the practical command is simply: "Use VAULT's session closeout prompt and generate the full session summary." You do not need to keep a separate Notepad copy.