# JOBS — Operating Decisions and Constraints

## Human control

- AI may discover jobs, research contacts, enrich data, rank opportunities, draft and quality-check emails.
- Bhaskar manually reviews and sends every external email/application.
- No autonomous email sending, LinkedIn messaging or application submission.
- A draft is not a sent email. Gmail thread evidence establishes actual dispatch, bounce and reply.
- A follow-up due date triggers a Gmail review, not automatic sending.

## Contact evidence

Keep these classifications distinct:
- `VERIFIED` — SMTP or approved direct/API mailbox verification.
- `VERIFIED_PUBLIC_COMPANY` — published on an official company source, but not necessarily SMTP-confirmed.
- `VERIFIED_DATABASE` — found in a business directory; preserve source and caveat.
- `FOUND_UNVERIFIED` — found on a public personal/academic/GitHub source, mailbox not verified.
- `LOW_GUESSED` — pattern inference only; hold and do not draft by default.
- `NOT_FOUND` — no sufficiently supported email. Do not assume a LinkedIn profile exists.

A catch-all SMTP result does not prove an individual mailbox exists. A generic company inbox is not necessarily a founder's personal email. Never invent an address or upgrade confidence without evidence.

## Source and platform boundaries

- Apollo: official API/MCP functionality only, within current terms and limits; no browser scraping.
- LinkedIn: no scraping or automated messaging.
- Agent-Reach and Scrapling: public pages only where automated access is permitted.
- Stealth/anti-detection browsers must not be used to defeat login walls, bot challenges, rate limits or access controls.
- Never give agents passwords, cookies, OAuth files or authenticated browser sessions.
- Keep API credentials and runtime-specific MCP configuration local and out of Git.

## Locked email format

The exact template is maintained in private JOBS `01-notes.md`. Durable constraints:
- fixed signature and links;
- subject 6–10 words and specific to product/role;
- middle paragraph 2–3 lines only;
- one project mapped to the actual JD;
- no "I recently applied for..." line;
- honest gap clause where relevant;
- no placeholders, invented metrics, fabricated JD details, generic project lists or tool inventories.

## Project-to-JD proof mapping

Use exactly one:
- RAG/retrieval/document search → Enterprise RAG & Knowledge Base.
- Agents/orchestration → Deep Research Multi-Agent System.
- Research/model fundamentals → Transformer-Based LLM from Scratch.
- Serving/APIs/deployment → FastAPI services with auth, rate limiting, tracing and LangSmith.
- Automation/internal tools → 10+ n8n/Make LLM-integrated workflows.
- Summarization/classification → Gemini pipelines on Vertex AI.

## Historical decisions, not automatic current tasks

Source summaries mention an OpenOutreach-vs-Apollo comparison, old follow-up schedules, stale listing checks and an earlier FirstWork draft. These are historical work items. Check current JOBS files and Gmail before resuming any.
