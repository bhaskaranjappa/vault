# JOB SEARCH WORKFLOW

**Priority:** Secondary in VAULT's overall goals.  
**Operational system:** Private repository `bhaskaranjappa/jobs`.

## Actual stages

1. **Search planning:** a selected LLM writes the YC agent prompt from Bhaskar's current profile/resume and exclusion list.
2. **YC discovery:** the YC agent returns approximately 25 matching roles. Preserve exact job/company IDs, source URLs and complete JDs.
3. **Context retention:** keep full JD context in the same YC agent session for subsequent drafting. Also persist JD text in private JOBS run artifacts so context can be restored.
4. **Contact enrichment:** approved public research and permitted APIs identify founders/CTOs/hiring contacts and source-backed contact information.
5. **Return handoff:** normalized contacts are returned to the same YC agent context and mapped to the exact job/company.
6. **JD-aware drafting:** the YC agent drafts using the actual JD and exactly one relevant proof project from the locked mapping.
7. **Human review/send:** Bhaskar manually reviews and sends emails. No autonomous send, LinkedIn automation or application submission.
8. **Reconciliation:** Gmail establishes sent/bounced/replied state; only then is the private JOBS tracker updated.

## Evidence and controls

- Remote and visa filters were historically tested as separate YC searches; reconfirm current connector behavior before combining.
- Keep contact confidence and source provenance explicit. A catch-all mailbox is not verified.
- Never guess an email or invent job facts/metrics.
- Apollo web scraping and LinkedIn scraping/automation are not approved. Use official APIs or permitted public sources.
- Drafts are separate run artifacts; they are not `NOT_SENT` rows in the live tracker.
- A follow-up date triggers an inbox review, not an automatic send.

## System boundary

VAULT stores durable project context and reusable lessons. The private JOBS repo stores mutable records, search-run artifacts, contact evidence, drafts and the live outreach tracker. Gmail is the source of truth for actual communication events.

Detailed project files: `08_KNOWLEDGE/PROJECTS/JOB_SEARCH_SYSTEM/`.
