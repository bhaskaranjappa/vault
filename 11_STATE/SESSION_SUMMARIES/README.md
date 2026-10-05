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

## Timestamp standard

Every session summary should make the chronology explicit. Use:

`Session date (YYYY-MM-DD)`

`Session timezone: Asia/Kolkata (IST, UTC+05:30)`

`Start time`, `End time`, and `Closeout generated at` in 24-hour IST when available.

When an AI cannot know an exact time, it must write `unknown` or `approximate` rather than inventing a timestamp.

The session date/time describes **when the work happened**. The Git commit timestamp separately records **when VAULT was updated**. Together they provide both activity chronology and repository write-back chronology.
