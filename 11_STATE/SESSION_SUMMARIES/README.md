# SESSION SUMMARIES

Purpose: durable, chronological records of substantial AI sessions used for cross-runtime continuity.

Each summary should preserve:
- date/time;
- AI runtime and coding executor;
- project/task;
- objective;
- completed work;
- files changed;
- commands/actions;
- tests and evidence;
- failures/blockers;
- decisions;
- tool/specialist usage;
- remaining work;
- exact continuation point;
- provenance/confidence.

Suggested filename:

`YYYY-MM-DD_<runtime>_<project-or-task>.md`

A session summary is a provenance record, not a second source of truth. Current canonical profile, project state, decisions, and tool state must be reconciled against the repository before being changed.

Do not store secrets or unnecessary raw transcripts in this directory. Keep large/raw artifacts outside the repository and reference them from the summary when appropriate.
