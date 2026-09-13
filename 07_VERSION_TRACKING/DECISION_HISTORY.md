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

## 2026-09-14 — V1 mandatory runtime set definition (Phase 12)

- Owner decision (recorded per PLAN.md §9 "the V1 gate must define which runtimes are mandatory" and §17): the V1 mandatory runtime set is the owner's actual workflow — ZCode (primary hands-on executor), OpenCode (available and validated), Hermes (installed, validated as execution runtime). Claude Code is a working Tier-2 runtime recorded BLOCKED (local API gateway down at test time) and does not block V1.
- Claude (chat), Gemini, ChatGPT, Cursor, Codex, Grok are NOT V1 blockers: they are not part of the current workflow. Their adapters remain documented and are recorded NOT_TESTED; adding any of them later is a V1+ validation task, not a re-opened V1 gate.
- Hermes G-06 (stale-information) is classified a runtime-layer truth-handling limitation, not a Gate G governance failure: Gate G criteria are approval enforcement, no autonomous outreach, and irreversible-action blocking, all evidenced PASS on three runtimes. G-06 remains an open runtime retest item under `11_STATE/STATE_INDEX.md`.
- Gate H ruled PASS vacuously: no automation is enabled anywhere, which satisfies "only validated R0/R1 automation enabled"; automation candidates stay KEEP IN RESERVE until a post-V1 cycle.
## 2026-09-13 (later) — V1+ tool evaluation queue owner decisions

Owner rulings on the V1+ tool evaluation queue (`02_AI_STACK/TOOL_EVALUATIONS/V1PLUS_TOOL_EVALUATION_QUEUE_2026-09-13.md`), grounded in actual tool experience and economics, overriding analyst dispositions:
- Hunter.io: IGNORE — MCP capability needed requires a paid tier; not economically justified.
- Apollo MCP: IGNORE — paid MCP access; no further evaluation time.
- Crunchbase: IGNORE / out of active queue — owner experience: insufficient value for this workflow.
- Firecrawl: KEEP IN RESERVE — Firecrawl MCP not currently justified; owner connected Firecrawl to ChatGPT and did not obtain the needed B2B research result; general Firecrawl capability is not evidence of usefulness here; revisit only on a concrete extraction limitation. Do not connect.
- OpenOutreach: IGNORE (analyst evaluation confirmed).
- Brave Search MCP: IGNORE (analyst evaluation confirmed).
- Scrapling: remains TEST FIRST (priority 1) — controlled experiment D1 designed, not yet run; no install yet.
- GitHub MCP: remains TEST FIRST (priority 2) — experiment D2, after D1.
- Playwright MCP: TEST ONLY IF NEEDED — conditional fallback for dynamic pages.
No tool installed, connected, or authenticated. Architecture unmodified. Outreach boundary unchanged.
