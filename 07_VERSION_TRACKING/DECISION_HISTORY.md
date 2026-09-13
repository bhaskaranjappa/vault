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

## 2026-09-14 — Scrapling experiment D1 executed (V1+)

- D1 run per the frozen design in `02_AI_STACK/TOOL_EVALUATIONS/V1PLUS_TOOL_EVALUATION_QUEUE_2026-09-13.md` §D (design and thresholds unmodified). Result: **PASS** on all five frozen criteria — coverage 6/6 taxonomy classes (~30 snapshot-backed items) ≥ baseline 12; 100% of enhanced-arm claims snapshot-backed; 6 materially new decision-relevant signals (Bolna current ATS role list correcting a stale baseline pain signal, GreyLabs 6-founder leadership team resolving a recorded CONFLICT, GreyLabs direct public contact, GreyLabs seed-round history with Z47, Logibee AI Operations Planning capability, Simplismart cost/GPU case metrics); zero governance breaches (robots enforced in code, public pages only, no stealth features, no outreach); extraction spot-check 12/12.
- Record: `02_AI_STACK/TOOL_EVALUATIONS/SCRAPLING_EXPERIMENT_D1_2026-09-13.md`. Raw snapshots + fetch logs + scripts archived OUTSIDE the canonical repo (`paios-runtime-evidence\2026-09-13\d1-scrapling\`, 78+ files). Snapshots are evidence inputs, never canonical truth.
- Scrapling lifecycle: INSTALLED (pre-existing 0.4.15, pip) → VERIFIED through direct runtime use in D1.
- **Recommended disposition: INSTALL** as the B2B evidence-capture layer — recorded as a recommendation; final INSTALL decision rests with the owner per the installation gate. Scope limits carried forward: no StealthyFetcher/anti-bot bypass, public pages + robots.txt only, no LinkedIn automation. Playwright MCP not triggered (Scrapling DynamicFetcher handled all JS-rendered targets).
- Next experiment (D2 — GitHub MCP) is queued but NOT started, per directive.

## 2026-09-14 — GitHub MCP experiment D2 executed (V1+)

- D2 run on the same frozen 5-company set (Logibee, Bolna AI, MaxHome.AI, GreyLabs AI, Simplismart), read-only github-mcp-server v1.12.1 (official binary, stdio subprocess, no runtime config changes), max 3 bounded calls per company. Result: **PASS** on the predefined criterion — 3 new or corrected Tier-1 technical signals across the set, zero fabricated entries, provenance preserved (7 JSONL evidence files outside the canonical repo).
- Evidence-backed findings: (1) **Bolna AI is the only prospect with a verified first-party GitHub presence** (`github.com/bolna-ai`, attributed via the docs.bolna.ai link captured in D1 snapshots) — 3 new Tier-1 signals: first-party MCP server repo, installable skills package ("npx skills add bolna-ai/skills"), actively maintained open-source core (commits 2 days before probe, 4 version bumps in 2 days, automated releases, internal ticket IDs). (2) **Queue hypothesis §4.6 ("all 5 cycle-1 prospects have GitHub orgs") is DISPROVED** — Logibee, MaxHome.AI, GreyLabs AI, and Simplismart have no attributable public GitHub org; name matches were all personal/learning/take-home repos and were recorded as "No verified GitHub evidence found" rather than forced attribution. (3) Decisive negatives have standalone value: future cycles should not spend manual search effort looking for GitHub orgs on closed-source SaaS prospects.
- Record: `02_AI_STACK/TOOL_EVALUATIONS/GITHUB_MCP_EXPERIMENT_D2_2026-09-14.md`. FACT vs INFERENCE preserved throughout (languages/topics are indicators, not proof of commercial stack; commit activity ≠ business pain; OSS activity ≠ contractor need).
- Auth note (hygiene flags for owner, recorded from testing): the pre-existing `GITHUB_MCP_TOKEN` env var is dead (HTTP 401 — rotate it) and a leaked PAT is stored as an env-var *name* (malformed `setx` — revoke it); all D2 evidence was produced in unauthenticated zero-permission mode.
- **Recommended disposition: INSTALL** as the read-only OSS-diligence layer (bounded call budgets, entity-resolution rule mandatory, no write scopes) — recorded as a recommendation; final decision rests with the owner per the installation gate.
- Next experiment (D3 — Playwright MCP, Scrapling DynamicFetcher vs Playwright MCP on JS-dependent targets) is queued but NOT started, per directive.

## 2026-09-14 — Playwright MCP experiment D3 executed (V1+)

- D3 controlled comparison on the three JS-dependent targets (jobs.ashbyhq.com/bolna, maxhome.ai, greylabs.ai): Arm A = pre-existing Scrapling 0.4.15 DynamicFetcher (same surface as D1), Arm B = official `@playwright/mcp@0.0.80` (wraps Playwright 1.63.0-alpha-2026-08-31, npx run, stdio subprocess with `--browser chrome --headless --isolated`, no runtime config changes, navigation-only scope). Result: **the canonical fallback condition is NOT MET** — Scrapling DynamicFetcher covered 3/3 targets (D1 evidence + D3 re-run, all HTTP 200, full first-party content, MaxHome home size byte-identical to D1); Playwright MCP retrieved the same information on all 3 targets but added no fact Scrapling had not already extracted (extra structure only: Ashby filter metadata, job UUIDs, a11y refs); **no target required browser interaction beyond rendering, which Scrapling already performs**.
- Evidence-backed findings: (1) jobs.ashbyhq.com serves different robots.txt by User-Agent — browsers get permissive rules (`/bolna` allowed, consistent with D1), Python-urllib gets HTTP 403 which robotparser conservatively treats as disallow-all; naive plain-HTTP robots checks therefore skip Ashby while browser-context tooling handles it. (2) Playwright MCP's default navigate→snapshot flow races SPA hydration (MaxHome captured progressbar-only without an explicit `browser_wait_for`; full a11y tree after an 8 s wait) — reproducible with the wait, racy without. (3) `browser_take_screenshot` writes relative to the MCP server's inherited cwd rather than `--output-dir` — PNGs landed in the canonical repo working directory, were immediately moved to the external evidence dir, and `git status` verified clean; any future install must pin output paths absolutely.
- Record: `02_AI_STACK/TOOL_EVALUATIONS/PLAYWRIGHT_MCP_EXPERIMENT_D3_2026-09-14.md`. Raw evidence (Arm A snapshots + fetch log; Arm B JSONL runs, 5 a11y YMLs, 4 PNGs) archived OUTSIDE the canonical repo (`paios-runtime-evidence\2026-09-13\d3-comparison\`). FACT vs INFERENCE preserved throughout.
- **Recommended disposition: KEEP IN RESERVE** — conditional fallback for dynamic/interactive pages; revisit only on a concrete Scrapling extraction/interaction failure or an Ashby-style board that actually requires pagination/filtering. Not IGNORE: D3 found it unnecessary, not broken.
- With D3 complete, the V1+ tool-evaluation experiments (D1 Scrapling, D2 GitHub MCP, D3 Playwright MCP) are all executed. No further tool evaluations started, per directive.

## 2026-09-14 — production tool-stack promotion pass (V1+)

- Owner promotion directive executed after D1/D2/D3: **Scrapling and github-mcp-server promoted to the production B2B stack**; no other tools promoted, installed, or evaluated; no runtime MCP configuration or Personal AI OS architecture modified.
- Lifecycle states assigned (only those supported by direct runtime evidence — distinction between INSTALLED, ENABLED, CONFIGURED, AUTHENTICATED, VERIFIED preserved; registry: `02_AI_STACK/AI_TOOL_REGISTRY.md`):
  - **Scrapling 0.4.15**: INSTALLED (pip, pre-existing) → VERIFIED (D1 PASS + D3 re-run) — CURRENT as the B2B evidence-capture layer. ENABLED/CONFIGURED/AUTHENTICATED not applicable (Python library, no auth). Production scope: static Fetcher + DynamicFetcher (no stealth), robots.txt enforced in code, public pages only, snapshots as evidence inputs outside the canonical repo.
  - **github-mcp-server v1.12.1**: INSTALLED (official binary, relocated from temp to `C:\Users\ABhas\tools\github-mcp-server\`, SHA-256 recorded) → VERIFIED (D2 PASS) — CURRENT as the read-only OSS-diligence layer. **ENABLED: no** (not wired into any runtime MCP config — by design); **CONFIGURED: no**; **AUTHENTICATED: no** (unauthenticated zero-permission mode used for all evidence; any future token must be a read-only fine-grained PAT with no repo-write scopes). Production scope: `--read-only` mandatory, max 3 read/search calls per company, entity-resolution rule mandatory.
  - **@playwright/mcp 0.0.80**: KEEP IN RESERVE — VERIFIED (D3) but not promoted; fallback only (D3: fallback condition not met). Revisit on a concrete Scrapling extraction/interaction failure; if promoted, pin output paths absolutely and scope toolset to navigation/snapshot only.
  - **Firecrawl**: KEEP IN RESERVE (unchanged, owner decision 2026-09-13). **Hunter.io, Apollo MCP, Crunchbase, OpenOutreach, Brave Search MCP**: IGNORE (unchanged).
- Hygiene flags carried forward (owner actions required, no secrets committed): rotate the dead `GITHUB_MCP_TOKEN` env var (401) and revoke the leaked PAT stored as an env-var *name* (malformed `setx`).
- Files updated in this pass: `02_AI_STACK/AI_TOOL_REGISTRY.md`, `07_VERSION_TRACKING/DECISION_HISTORY.md`, D1/D2/D3 evaluation records (promotion confirmations appended). `05_WORKFLOWS/B2B_CLIENT_ACQUISITION.md` has no tool references (tool-agnostic by design — left untouched). PLAN.md Phase 9 framework unchanged.
