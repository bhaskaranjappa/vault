# DECISION HISTORY

- Personal AI OS knowledge must be portable.
- Canonical knowledge must not live only in model memory.
- Hermes is orchestration runtime for current B2B work.
- OpenCode is development/debugging runtime.
- B2B and job search are separate workflows.
- Prospect quality over volume.
- Human approval before outbound communication.
- No fabricated evidence.
- Small focused tool stack.
- Public upstream repos remain separate from private personal OS.
- Rejected approaches remain recorded.
- Canonical knowledge is versioned with Git.

## 2026-09-13 — tool integration and automation decisions (Phase 9/10 evidence)

- No new tool integration is justified at V1: the B2B research-and-drafting stages were validated with public web research alone (2026-09-05 benchmark, 2026-09-13 Connectsys re-validation). Decision states — Apollo: KEEP IN RESERVE (enrichment only becomes relevant at outreach-ready stage). Vibe Prospecting / Wellfound: IGNORE for V1 (no workflow evidence). Firecrawl: KEEP IN RESERVE (only if scraping volume exceeds plain web search). GitHub: TEST FIRST via Hermes MCP/GitHub key (currently unset) — not required for research stages. Gmail: IGNORE until an approved-send stage exists, and even then sending stays manual.
- No automation is built in this cycle: Gate H prerequisites (Gates D and G fully passing) are not met. R0/R1 automation candidates remain the existing research/scoring/drafting steps, to be revisited after V1.