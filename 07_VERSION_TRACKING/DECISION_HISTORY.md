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

## 2026-09-15 — OpenOutreach vs Scrapling comparison test executed (V1+)

- Owner-directed bounded comparison of eracle/OpenOutreach against the installed Scrapling 0.4.15 for B2B client discovery, run entirely in an isolated workspace (`C:\Users\ABhas\projects\paios-eval-20260915\`) outside the canonical repo; no emails sent, no contacts made, no production tooling or runtime configuration modified.
- **Critical question answered at implementation level: OpenOutreach does NOT scrape arbitrary websites.** Full `openoutfind==0.1.12` source inspection: no scraping library present; lead discovery is the BetterContact Lead Finder licensed-DB API (`app.bettercontact.rocks/api/v2/lead_finder/async`); Apollo email enrichment is wired but unexposed; code comments repeatedly disclaim scraping. README's "no scraping" claim is accurate.
- Live research-only `find` run: BLOCKED on a BetterContact account/API key plus an LLM key — account creation is an outward-facing action not performed autonomously; no owner keys consumed. Capability findings rest on source inspection (strong) plus the documented blocked run.
- TEST B (Scrapling, same frozen ICP): discovery via Bing HTML + base64 redirect decode — 26 unique domains in ~4.5 s across 5 ICP queries (DDG HTML endpoint returned 202 anti-bot; unusable with plain fetcher); extraction 11/12 homepages with careers/contact follow-up (up to 3 pages/company), public email capture, JSONL structured output; 1 SSL-chain failure; JS-only sites return empty shells with the plain fetcher. Discovery noise requires the agent/LLM qualification layer.
- **Disposition: OpenOutreach = IGNORE (maintained from owner ruling 2026-09-13, upgraded from analyst analysis to implementation-level evidence).** Recommended B2B lead-finding architecture: agent-driven discovery + Scrapling extraction + agent qualification/reasons (existing PAIOS pattern). Scrapling remains INSTALLED→VERIFIED. No new installs.
- Record: `02_AI_STACK/TOOL_EVALUATIONS/OPENOUTREACH_VS_SCRAPLING_TEST_2026-09-15.md`. Registry updated: `02_AI_STACK/AI_TOOL_REGISTRY.md`. Raw evidence preserved in the isolated workspace (`scrapling_results.jsonl`, `scrapling_test.log`, benchmark script, OpenOutreach clone, venv).


## 2026-10-03 — external agent repository evaluation (V1+)

- Evaluated `HarnessMD/munder-difflin`, `paperclipai/paperclip`, `tahodev/openmuse`, `CopilotKit/OpenDots`, and `diggerhq/opendots` under `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.
- The OpenDots name was resolved as two distinct relevant repositories: Digger's `diggerhq/opendots` and CopilotKit's `CopilotKit/OpenDots`.
- Current fit: **Munder Difflin = TEST FIRST** as an external multi-CLI execution/harness candidate. It most directly overlaps the current PAIOS runtime/orchestration surface and supports Codex/OpenCode and other terminal agents.
- **Paperclip = KEEP IN RESERVE** for a future control-plane integration, especially B2B operations. Its task, org, budget, routine, governance and adapter layers overlap substantially with existing PAIOS engines.
- **OpenMuse = KEEP IN RESERVE** as a security-primitives benchmark. Its exact-action approval model is materially different from PAIOS policy-level delegated autonomy.
- **CopilotKit OpenDots = KEEP IN RESERVE** as a future user-facing agent-workspace/product reference.
- **Digger OpenDots = KEEP IN RESERVE** as a personal-agent UX reference; its OpenComputer dependency is not a current PAIOS runtime-parity solution.
- No candidate was installed, authenticated or runtime-verified. No candidate was promoted to the production runtime stack.
- Full evidence: `02_AI_STACK/TOOL_EVALUATIONS/EXTERNAL_REPOSITORIES_2026-10-03.md`.


## 2026-10-04 — Phase 14 closeout

- V1+ Phase 14 (Real Runtime Integration) CLOSED/COMPLETED. Portable adapter contract plus two live-verified real runtimes through the canonical adapter: Codex CLI (2026-09-17, re-executed 2026-10-04; working model rotated upstream gpt-5.5 → gpt-5.6-terra) and Hermes Agent CLI (2026-10-03/04, Nous Portal auth, free-tier model). Real cross-runtime failover (RT-20) and parity (RT-21) executed live.
- Universal coding-agent parity is NOT a Phase-14 exit requirement. Unavailable/unauthenticated runtimes (OpenCode hang, Grok sign-in, Kimi quota, Cursor) are access limitations, not implementation defects; their states are recorded honestly.
- Owner-confirmed execution pool policy (ZCode, OpenCode, Antigravity, Freebuff; Codex/Cursor restricted) remains authoritative for task planning; live adapter evidence is recorded separately and does not by itself change owner policy.
- Next V1+ objective: bounded agent-memory follow-up evaluation of rohitg00/agentmemory (isolated-scope concurrency + npm package verification). agentmemory retains TEST FIRST; not installed into PAIOS; not verified for PAIOS use.
- Closeout record: `12_VALIDATION/AIOS_PHASE14_CLOSEOUT_2026-10-04.md`.

## 2026-10-04 — agentmemory isolated-scope follow-up

- Isolated-scope follow-up evaluation of rohitg00/agentmemory executed (PARTIAL, leaning PASS FOR NEXT STAGE). Per-call agentId isolation is correct and restart-durable on all tested retrieval surfaces (REST search, smart-search, context) including 20/20 concurrent writes and 10/10 concurrent retrievals.
- Isolation is cooperative client scoping, NOT a security boundary: wildcard `agentId:"*"` and agentId-less reads return all agents' memories by design; the REST bearer secret is the actual access boundary. `project` is confirmed not a security boundary.
- `AGENTMEMORY_AGENT_SCOPE=isolated` silently degrades to shared mode without a server-wide `AGENT_ID`, and the documented hard-refusal branch is unreachable code (upstream finding).
- Abrupt kill within the 3.5 s capture durability window silently loses accepted events (documented window measured, not worked around).
- Disposition remains TEST FIRST; no integration. Smallest next experiment if pursued: a thin PAIOS wrapper that always passes an explicit agentId, refuses wildcard/unscoped reads, and verifies isolated mode is active at startup.
- Evidence: `12_VALIDATION/AIOS_AGENTMEMORY_ISOLATED_SCOPE_EVIDENCE_2026-10-04.md`.

## 2026-10-04 — agentmemory safety-wrapper prototype (owner-initiated next stage)

- Built and tested the smallest disposable prototype demonstrating how PAIOS could safely consume rohitg00/agentmemory despite its cooperative-scope limitations. Prototype and all runtime state remain outside the canonical PAIOS tree (`_eval_tmp\am_wrapper\`); agentmemory is NOT integrated, NOT installed, context injection NOT enabled.
- Wrapper contract verified by 15-test suite (14 PASS / 1 FAIL): every data-path request carries a pinned allowlist agentId (missing/empty/wildcard/broad selectors rejected before I/O); `project` has no read path; startup behaviorally verifies — against the live server — that bearer auth is enforced and isolated scope actually keeps a foreign-agent canary invisible to unscoped reads, failing closed otherwise; any server row owned by another agent raises instead of passing through; all recalled rows are flagged untrusted; PAIOS remains canonical for policy, truth, authority, decisions and durable state.
- Memory capability through the wrapper: relevance (AM-11), no-result (AM-12), injection isolation (AM-13), capture-time redaction (AM-14) and failure/recovery fail-closed behavior (AM-15) all PASS. New upstream findings: hard kill can permanently break the write path (HTTP 500) on a reused data dir; acknowledged writes need settle time before an abrupt kill; `expandIds` cannot resolve `mem_*` memories; only one daemon per lifecycle state unless `--instance N` is used.
- **WR-09 FAIL (upstream defect): under multi-agent concurrent capture, ALL of one agent's acknowledged memories can become permanently unsearchable** (store intact, `verify` finds every record, zero cross-agent leakage — rows lost from the search index, loss survives restart). Single-agent concurrency is safe; the verified mitigation is serialized capture with a per-agent-switch quiesce (>=4 s).
- Decision: PARTIAL. The wrapper safety contract is demonstrated; the upstream recall-completeness defect blocks PASS FOR NEXT STAGE for the multi-runtime continuity use case. Integration may proceed only with the serialized-capture/quiesce adapter discipline (or an upstream fix) plus write-to-read-back durability confirmation; do not integrate in the current state. agentmemory retains TEST FIRST.
- Evidence: `12_VALIDATION/AIOS_AGENTMEMORY_WRAPPER_PROTOTYPE_EVIDENCE_2026-10-04.md`.
