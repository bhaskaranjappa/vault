# JOBS — System Architecture

## Design intent

A human-in-the-loop, multi-agent workflow for finding relevant YC/startup roles and preparing personalized founder/hiring-lead outreach. The architecture separates job discovery, contact enrichment, drafting and communication evidence.

## End-to-end flow

1. **Profile and search planning:** a selected LLM uses Bhaskar's current resume, profile, preferences and exclusion list to write a precise prompt for the YC agent.
2. **YC job discovery:** the YC agent searches for approximately 25 relevant openings. Historical testing found that `remote=true` and `visa=true` needed separate queries; current connector behavior must be rechecked before combining them.
3. **Job-context capture:** preserve job ID, company ID, title, official URLs, full JD text, location, remote/work-authorisation details, salary only when published, role requirements, fit evidence and skill gaps. Keep the original YC agent context for later drafting.
4. **Contact enrichment:** use approved public-web research and permitted API/MCP sources to identify founders, CTOs or hiring leads and obtain source-backed contact details.
5. **Return to original YC context:** feed normalized contacts back into the same YC agent session. Map each contact to the exact company and JD.
6. **JD-aware drafting:** the YC agent writes the email using the actual JD and the locked project-to-JD mapping. Exactly one proof project is used per message.
7. **Human review and Gmail send:** Bhaskar reviews and manually sends. No autonomous sending or application submission.
8. **Evidence-backed tracking:** reconcile actual Gmail sent/reply/bounce events into the private JOBS tracker. Drafts do not count as sent records.

## Data handoff

Each discovery run is stored in `runs/<run_id>/` in private JOBS:
- `manifest.json` — run ID, status, artifacts and non-secret YC session reference.
- `search_run.json` — search requests, job records, complete JD text and discovery-stage founder/contact identities.
- `enriched_contacts.json` — stable contact IDs, job mappings, email evidence, confidence, routing, source URLs and verification results.
- `drafts/email/<contact_id>.md` — email drafts.
- `drafts/linkedin/<contact_id>.md` — manual-review LinkedIn-message variants only after a public profile is confirmed.
- `draft_review.json` — PASS/FIX/HOLD and evidence per draft.

The schemas and run validator live in JOBS. The current tracker is separate and contains only actual Gmail-confirmed outreach.

## Main components

- LLM prompt planner
- YC job-discovery and JD-context agent
- Public-web/contact researcher (Agent-Reach and other approved sources)
- Apollo official API/MCP where permitted
- Prospector MCP for contact/domain/mailbox discovery/verification
- Scrapling for allowed public pages only
- Email reviewer
- Tracker steward
- Gmail as communication evidence source

## Runtime portability

The work has used Antigravity, OpenCode and ZCode, with tests/limitations recorded for Freebuff web and DeepSeek Harness. Runtime-specific MCP JSON and credentials remain local. JOBS documents runtime state but does not store secrets or claim uniform compatibility.

## Control boundaries

- Human approval required before external email or application.
- No automatic Gmail send, LinkedIn DM or application submission.
- No Apollo website scraping; use permitted official API functionality.
- No LinkedIn scraping or automation.
- No stealth-browser bypass of login walls, bot challenges, rate limits or access controls.
- A catch-all SMTP result does not verify an individual mailbox.
- `LOW_GUESSED` is not eligible for automatic email drafting.
- `NOT_FOUND` does not imply a LinkedIn profile exists; profile identity must be confirmed separately.

## Architectural lesson

The hard problem is not adding more agents. It is preserving job context and evidence across agent boundaries, maintaining stable IDs, validating handoffs and preventing false status transitions.
