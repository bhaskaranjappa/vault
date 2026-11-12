# JOBS — Project Knowledge Record

**Owner:** Bhaskar Anjappa  
**Priority:** Secondary in VAULT's overall goals; detailed operational workstream  
**Last reconciled:** 2026-11-12  
**Operational repository:** https://github.com/bhaskaranjappa/jobs (private)

## Purpose

Preserve the architecture, history, tools, decisions and lessons behind Bhaskar's YC/startup job-search workflow. This VAULT folder is the cross-project knowledge record, not a duplicate operational database.

## Source-of-truth boundary

| System | Owns |
|---|---|
| VAULT public repository | Durable project context, architecture, historical decisions, tool evaluations, session history and cross-project lessons |
| JOBS private repository | Current job records, founder/contact data, enrichment evidence, per-run artifacts, drafts, review results and the live outreach tracker |
| YC agent / Work at a Startup | Job discovery and retained job-description context used later for tailored drafting |
| Gmail | Actual sent, bounced and replied message evidence |
| Local coding-agent runtimes | Installed tools, credentials and runtime-specific MCP configuration; secrets stay local |

Do not copy the live `00-tracking.csv`, founder contact exports, email drafts, credentials, cookies or MCP configuration into this public VAULT repository. There must be one operational tracker: the private JOBS repository.

## Actual pipeline

`Selected LLM → prompt planning → YC agent searches about 25 matching jobs → full JDs and job context are saved → contact enrichment → enriched contacts return to the same YC context → YC agent drafts JD-specific outreach → Bhaskar manually reviews/sends in Gmail → Gmail evidence updates JOBS tracker`

The key design is preserving the YC agent's original full JD context through contact enrichment and returning contacts to that same session for drafting. The run archive also persists full JD text so the process can recover after context loss.

## Documentation

- [System architecture](SYSTEM_ARCHITECTURE.md)
- [Tool history and evaluation](TOOL_HISTORY.md)
- [Operating decisions and constraints](DECISIONS_AND_CONSTRAINTS.md)
- [Current project handoff](CURRENT_HANDOFF.md)
- [Historical source summaries](HISTORY/README.md)

## Canonical operational entrypoints

- [Private JOBS repository](https://github.com/bhaskaranjappa/jobs)
- [JOBS README](https://github.com/bhaskaranjappa/jobs/blob/main/README.md)
- [JOBS MEMORY.md](https://github.com/bhaskaranjappa/jobs/blob/main/MEMORY.md)
- [JOBS WORKFLOW.md](https://github.com/bhaskaranjappa/jobs/blob/main/WORKFLOW.md)
- [JOBS tool registry](https://github.com/bhaskaranjappa/jobs/blob/main/integrations/TOOL_REGISTRY.md)
- [JOBS current tracker](https://github.com/bhaskaranjappa/jobs/blob/main/00-tracking.csv) — private; repository permission required

## Historical record and privacy

Full-length user-provided summaries are preserved under `HISTORY/` with direct email addresses redacted because VAULT is public. The original unredacted summary text remains in private JOBS `MEMORY.md`. A duplicate summary attachment was deduplicated. A PowerShell/GitHub upload transcript was not classified as a session summary.

## Operating rules

1. VAULT records durable context; JOBS owns mutable operational records.
2. Current user instructions and direct evidence outrank historical summaries.
3. Installed does not mean enabled, configured, authenticated or verified.
4. Drafting is not sending. Gmail evidence confirms communication events.
5. Human review remains required before every external email or application.
6. Do not bypass Apollo or LinkedIn access restrictions with stealth browsers.
7. Preserve source provenance and uncertainty.
8. Promote reusable lessons into VAULT; keep contact-level operational data in JOBS.
