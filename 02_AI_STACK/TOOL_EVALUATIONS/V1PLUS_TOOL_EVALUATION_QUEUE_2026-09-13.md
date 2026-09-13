# V1+ TOOL EVALUATION QUEUE — 2026-09-13

Evaluated per `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`. Question asked per candidate: "Does this materially improve the Personal AI OS B2B workflow enough to justify adding it?" — not "is it a good tool?" Nothing installed, authenticated, or connected during this evaluation. All data below is public evidence gathered 2026-09-13; sources cited per claim. No scores invented; dispositions are judgments with stated reasons.

Baseline being improved: B2B workflow `05_WORKFLOWS/B2B_CLIENT_ACQUISITION.md` as executed in `11_STATE/B2B_CYCLE_2026-09-13.md` (manual research via general web search; evidence captured as cited URLs; contacts verified only via public LinkedIn/company channels).

---

## OWNER DECISION REVISION — 2026-09-13

The dispositions below in records/queue sections were the analyst recommendation. The owner has since ruled on dispositions based on actual tool experience and economics. Owner decisions OVERRIDE analyst dispositions and are marked OWNER-DECISION. The original analyst text is preserved for provenance. Decision recorded in `07_VERSION_TRACKING/DECISION_HISTORY.md`.

| Candidate | Owner disposition | Owner reason |
|---|---|---|
| Hunter.io | IGNORE (was TEST FIRST) | MCP usage requires a paid tier for the capability needed — not economically justified for current workflow. |
| Apollo MCP | IGNORE (was KEEP IN RESERVE) | Paid MCP access unsuitable; no further evaluation time. |
| Crunchbase MCP | IGNORE / OUT OF ACTIVE QUEUE (was KEEP IN RESERVE) | Owner experience: insufficient value for this workflow. |
| Firecrawl | KEEP IN RESERVE (demoted from TEST FIRST) | IMPORTANT DISTINCTION: Firecrawl capability itself may be useful, but Firecrawl MCP is not currently justified. Owner already connected Firecrawl to ChatGPT and did not obtain the needed B2B research result. General Firecrawl capability is NOT evidence of usefulness here. Revisit only if a concrete research/extraction limitation appears that Firecrawl is likely to solve. Do not connect. |
| OpenOutreach | IGNORE (confirmed) | Architectural duplication + autonomous outreach conflict with governance. |
| Brave Search MCP | IGNORE (confirmed) | Substantial overlap with working web-search capability. |
| Scrapling | TEST FIRST (confirmed, priority 1) | Highest-priority actual tool experiment. |
| GitHub MCP | TEST FIRST (confirmed, priority 2) | Specifically for technical-company research: repo activity, engineering activity, tech signals, issues/projects, evidence-backed technical pain signals; does it add info the web-research baseline misses? |
| Playwright MCP | TEST ONLY IF NEEDED (conditional fallback) | For dynamic/browser-only research ordinary HTTP extraction cannot handle. |

---

## CANDIDATE RECORDS

### 1. Scrapling (+ official MCP)
1. **Name:** Scrapling (D4Vinci/Scrapling; MCP via `pip install "scrapling[ai]"`)
2. **Source:** https://github.com/D4Vinci/Scrapling (README inspected 2026-09-13)
3. **Category:** Web extraction/crawling framework with official MCP server
4. **Does:** Fetcher with TLS impersonation; Playwright-based DynamicFetcher; self-healing adaptive element relocation; Scrapy-like spider; `page.markdown()` LLM output; MCP server with one-shot/session scraping, prompt-injection stripping, screenshots (per README).
5. **B2B stage:** Company research (stages 2) and evidence collection; crawling careers/tech/pricing pages at scale (stage 3 signal discovery).
6. **Hypothesis:** Current cycle captured evidence as citations only, with no raw-HTML/screenshot snapshot; Scrapling can make evidence reproducible (stored snapshot per claim) and crawl job/tech pages systematically, reducing false negatives on pain signals.
7. **Duplication:** Partial — ZCode has Browser Use; Scrapling is runtime-agnostic (usable from Hermes/OpenCode via MCP or Python) and adds crawling + persistence Browser Use lacks.
8. **Complements:** Yes — evidence feed INTO canonical records; canonical repo stays source of truth.
9. **Provenance:** Raw HTML, markdown, screenshots capture = strong provenance; MCP strips prompt injection (README claim, unverified).
10. **Governance/safety:** README self-describes as "educational and research purposes only"; stealth/anti-bot features carry ToS/legal responsibility on us. Restrict to public pages, robots.txt compliance (Spider supports it), no login-walled scraping.
11. **Complexity:** Medium — Python ≥3.10, `[fetchers]` extra + browser download; MCP via `[ai]` extra.
12. **Cost/license:** BSD-3-Clause; free, self-hosted; no vendor API (proxy sponsors are third-party ads).
13. **Maturity:** ~80.7k stars, 1,620 commits, 92% test coverage, typed, Docker images per release (README, 2026-09-13). Strong for a single-maintainer project; bus factor is a residual risk.
14. **Evaluation type:** Controlled A/B against baseline on same prospect batch.
15. **Disposition:** TEST FIRST.
16. **Reason:** Directly attacks the weakest measured part of cycle 1 (evidence reproducibility, systematic signal crawling), free, no vendor lock-in, governance-compatible if scoped to public pages.

### 2. OpenOutreach (eracle/OpenOutreach)
1. **Name:** OpenOutreach (OpenOutFind + OpenOutSend)
2. **Source:** https://github.com/eracle/OpenOutreach, https://openoutreach.app (README inspected 2026-09-13)
3. **Category:** Self-hosted end-to-end B2B lead-gen/outreach agent
4. **Does:** discover → qualify → gate → resolve (buy verified emails via BetterContact) → write → SEND from your mailbox, autonomously via `run` (README).
5. **B2B stage:** Would cover nearly all stages — which is the problem.
6. **Hypothesis:** None survives scrutiny — see 15/16.
7. **Duplication:** High — discovery, qualification, scoring, drafting duplicate our canonical pipeline; replaces rather than feeds it.
8. **Complements:** No — it is a competing architecture whose pipeline overlaps ours almost 1:1.
9. **Provenance:** Output is CSV + LLM judgment; no evidence/provenance model comparable to TRUTH_AND_EVIDENCE_PROTOCOL; email data is purchased (BetterContact credits), affiliate-linked.
10. **Governance/safety:** Autonomous sending from `run` directly violates our R2 boundary (HUMAN_APPROVAL_PROTOCOL). Affiliate-funded monetization biases provider choice. GPLv3. "Use at your own risk" disclaimer; Gaussian-process candidate selection self-described as unproven experiment.
11. **Complexity:** Medium-high (LLM key + BetterContact account + SMTP app password).
12. **Cost:** BetterContact credits (1/verified email), LLM tokens; free tier 40 credits.
13. **Maturity:** ~3k stars, 1,043 commits, single maintainer, 1 open issue; active but solo and sponsor-funded.
14. **Evaluation type:** Read-only architectural comparison only (done). No install test justified.
15. **Disposition:** IGNORE.
16. **Reason:** Answer to the A/B/C question is B-leaning-C: it is a competing system that duplicates our architecture, and its core differentiator (autonomous send) is exactly the behavior our governance forbids. Its discovery/qualification ideas are already implemented in our workflow with stronger provenance. Revisit only if our manual pipeline proves too slow at scale.

### 3. Awesome MCP Servers (as discovery catalogue — NOT evaluated as an installable)
1. **Name:** punkpeye/awesome-mcp-servers (canonical, active; wong2 list dormant)
2. **Source:** https://github.com/punkpeye/awesome-mcp-servers (94.9k stars, pushed 2026-09-13)
3. **Category:** Discovery catalogue only.
4. **Does:** Curated MCP server index; used to shortlist individual servers below and in records 4–9.
5–16. Disposition for the catalogue itself: **IGNORE as an installable** (per directive). Individual findings evaluated as separate candidates.

### 4. GitHub MCP Server (official)
1. **Name:** github/github-mcp-server
2. **Source:** https://github.com/github/github-mcp-server (32.9k stars, pushed 2026-09-10); docs.github.com MCP setup guide; Jan 2026 changelog (Projects tools, OAuth scope filtering)
3. **Category:** MCP server — GitHub API
4. **Does:** Repos, org details, issues/PRs, code search, Projects (official docs).
5. **B2B stage:** Pain/need signal detection — org tech stack, engineering activity, careers READMEs/jobs repos; decision-maker identification via public maintainer/org-role data.
6. **Hypothesis:** Cycle 1 relied on third-party job boards with stale/conflicting listings; primary GitHub data gives fresher, Tier-1 hiring/tech evidence for AI-product companies (all 5 cycle-1 prospects have GitHub orgs).
7. **Duplication:** Low — we currently use generic web search for this.
8. **Complements:** Yes — Tier-1 evidence feed.
9. **Provenance:** First-party API data; strong.
10. **Governance/safety:** PAT scope control (use read-only fine-grained token; no repo-write scopes); secrets never in Git.
11. **Complexity:** Low — PAT + MCP config; Docker or hosted remote.
12. **Cost/license:** MIT; free with existing GitHub account.
13. **Maturity:** Official GitHub product, actively developed — highest possible maturity class here.
14. **Evaluation type:** Controlled A/B on same prospect batch (signal discovery completeness).
  15. **Disposition:** TEST FIRST (consistent with PLAN.md Phase 9 candidate "GitHub") → **EXECUTED as D2 (2026-09-14): PASS — 3 new Tier-1 signals (Bolna only: first-party MCP server, skills package, active OSS core); 4/5 companies have no attributable public GitHub org (hypothesis §4.6 DISPROVED); zero fabricated; provenance preserved. Record: `GITHUB_MCP_EXPERIMENT_D2_2026-09-14.md`. Recommended disposition: INSTALL (read-only OSS-diligence layer) — owner approval pending.**
16. **Reason:** Free, official, Tier-1 provenance, low complexity, direct fit to stage 3.

### 5. Firecrawl MCP Server
1. **Name:** firecrawl/firecrawl-mcp-server
2. **Source:** https://github.com/firecrawl-mcp-server (7.4k stars, pushed 2026-09-12); https://docs.firecrawl.dev/mcp-server
3. **Category:** MCP web scraping/crawling/search (vendor API)
4. **Does:** Search, scrape, crawl, GitHub-repo research via Firecrawl API (official docs).
5. **B2B stage:** Evidence collection; company research.
6. **Hypothesis:** Managed extraction may beat Scrapling on JS-heavy pages with zero local setup; direct comparison against Scrapling decides which one enters the stack (avoid carrying both).
7. **Duplication:** High vs Scrapling (same stages); this is an either/or.
8. **Complements:** Yes if it wins; vendor output feeds canonical records.
9. **Provenance:** Good (clean markdown + source URLs) but vendor-processed — weaker than raw-HTML snapshots from Scrapling.
10. **Governance/safety:** External API sees queried URLs (minor privacy consideration); vendor data never source of truth.
11. **Complexity:** Very low (API key + MCP URL).
12. **Cost/license:** MCP wrapper MIT; engine AGPL-3.0 if self-hosted; cloud free tier small, paid ~$16–20/mo.
13. **Maturity:** Official vendor repo, very active.
14. **Evaluation type:** Head-to-head vs Scrapling in same experiment.
15. **Disposition:** TEST FIRST (was KEEP IN RESERVE; promoted because workflow need is now evidenced by cycle 1).
16. **Reason:** Only credible challenger to Scrapling; test both, install at most one.

### 6. Hunter.io MCP plugin (verifier)
1. **Name:** hunter-io/claude-plugin (domain search / finder / verifier)
2. **Source:** https://github.com/hunter-io/claude-plugin (9 stars, pushed 2026-09-01)
3. **Category:** Contact discovery/verification MCP
4. **Does:** Domain email search, finder, and email VERIFIER (deliverability check).
5. **B2B stage:** Stage 5 — professional contact verification.
6. **Hypothesis:** Cycle 1 verified contacts only via public LinkedIn/pages; a verifier lets us check a decision-maker's publicly-listed address before outreach without guessing (we verify, never generate).
7. **Duplication:** None — no verification capability exists in the stack.
8. **Complements:** Yes — strictly post-identification verification.
9. **Provenance:** Deliverability verdicts with confidence; vendor-claimed.
10. **Governance/safety:** MUST be used in verifier-only mode on already-identified contacts; the FINDER mode conflicts with "never guess an email" and is out of policy. GDPR sensitivity in EU outreach.
11. **Complexity:** Low — API key.
12. **Cost/license:** MIT plugin; Hunter free tier ~25 searches + 50 verifications/mo, paid ~$34–49/mo.
13. **Maturity:** Official vendor repo but very low usage signal (9 stars); the underlying API is a mature commercial product.
14. **Evaluation type:** Small controlled test: verify N known-public addresses vs manual check.
15. **Disposition:** TEST FIRST (verifier mode only).
16. **Reason:** Fills a real gap at the approval boundary; free tier sufficient for quality-first volumes.

### 7. Playwright MCP (Microsoft)
1. **Name:** microsoft/playwright-mcp
2. **Source:** https://github.com/microsoft/playwright-mcp (37k stars, pushed 2026-09-11); playwright.dev/mcp
3. **Category:** Browser automation MCP
4. **Does:** Accessibility-snapshot browser control: navigate, click, fill, screenshot.
5. **B2B stage:** Evidence collection fallback for JS-heavy/login-free interactive pages.
6. **Hypothesis:** Cross-runtime interactive evidence capture where scraping fails.
7. **Duplication:** High in ZCode (Browser Use plugin already present and working); unique for Hermes/OpenCode runtimes.
8. **Complements:** Yes.
9. **Provenance:** Screenshots = good evidence.
10. **Governance/safety:** Interactive browsing must respect site ToS (esp. LinkedIn — do not automate LinkedIn).
11. **Complexity:** Low (npx, local browser, no keys).
12. **Cost/license:** Apache-2.0; free.
13. **Maturity:** Official Microsoft, very active.
14. **Evaluation type:** Fallback-scenario test only.
15. **Disposition:** TEST FIRST (lowest priority of the five) — only if Scrapling/Firecrawl fail on JS-heavy targets in the head-to-head.
16. **Reason:** Free and official but largely duplicates working ZCode capability; condition on the scraping test outcome.

### 8. Apollo.io MCP plugin
1. **Name:** apolloio/apollo-mcp-plugin (official; community alt thevgergroup/apollo-io-mcp)
2. **Source:** https://github.com/apolloio/apollo-mcp-plugin (20 stars, pushed 2026-09-11); docs.apollo.io/docs/apollo-mcp
3. **Category:** B2B contact/firmographic database MCP
4. **Does:** Org/people search (240M+ contacts claimed), enrichment, sequences.
5. **B2B stage:** Prospect discovery, decision-maker ID, enrichment.
6. **Hypothesis:** Would expand discovery coverage beyond web-visible companies.
7. **Duplication:** Moderate — overlaps discovery stages but with different (database) coverage.
8. **Complements:** Possible, but risk of becoming a second source of truth is high.
9. **Provenance:** WEAK — data is model-inferred/vendor-aggregated; conflicts with our Tier discipline and "never guess contacts" (Apollo emails are confidence-scored, not verified).
10. **Governance/safety:** GDPR/ToS exposure of database outreach; sequences feature = outreach automation (R2).
11. **Complexity:** Low technically.
12. **Cost:** Paid product; free tier API credits negligible; ~$49+/user/mo.
13. **Maturity:** Official but brand-new plugin (20 stars); commercial API mature.
14. **Evaluation type:** None now.
15. **Disposition:** KEEP IN RESERVE (unchanged from V1 decision).
16. **Reason:** Cost + weak provenance + governance friction; quality-over-volume workflow doesn't need database scale yet.

### 9. Brave Search MCP
1. **Name:** brave/brave-search-mcp-server
2. **Source:** https://github.com/brave/brave-search-mcp-server (1.4k stars, pushed 2026-09-10)
3. **Category:** Web search MCP
4. **Does:** Web + local-business search via Brave API.
5. **B2B stage:** Prospect discovery.
6. **Hypothesis:** —
7. **Duplication:** Near-total — ZCode/OpenCode/Hermes sessions already have capable web search built in (cycle 1 executed entirely on it).
8. **Complements:** Marginal.
9–13. Provenance same as any search engine; free tier 2k queries/mo then metered; MIT; official Brave repo, active.
14. **Evaluation type:** None.
15. **Disposition:** IGNORE.
16. **Reason:** Duplicates an existing, working capability; adds an API-key dependency for no measured gap.

### 10. Crunchbase MCP (official; community server stale)
1. **Name:** Crunchbase official MCP (data.crunchbase.com/docs/mcp-overview); community Cyreslab-AI/crunchbase-mcp-server (16 stars, last push 2025-05-05 — stale)
2. **Category:** Funding-data MCP
3. **Does:** Company/funding/people data.
4. **B2B stage:** Funding-signal detection.
5. **Hypothesis:** Funding is a top pain-signal class in cycle 1 (3 of 5 prospects cited rounds) — but news search already surfaced each round.
7. **Duplication:** Moderate vs news/web search.
8. **Complements:** Yes.
9. **Provenance:** Vendor database; Tier 2-ish.
10. **Governance:** Paid/enterprise API; acceptable use constraints.
11–13. Complexity low; cost nontrivial; community server stale → avoid.
14. **Evaluation type:** None now.
15. **Disposition:** KEEP IN RESERVE.
16. **Reason:** Real but redundant coverage at current volume; revisit if funding-signal false negatives appear.

---

## A. EVALUATION QUEUE — REVISED PER OWNER DECISIONS (operative)

1. Scrapling (+MCP) — TEST FIRST (experiment D1 below)
2. GitHub MCP (official) — TEST FIRST (experiment D2, run after D1)
3. Playwright MCP — CONDITIONAL (only on D1 trigger: dynamic pages HTTP extraction cannot handle)
4. Firecrawl — KEEP IN RESERVE (owner experience; revisit only on a concrete extraction limitation)
5. Hunter.io — IGNORE (owner: paid tier required)
6. Apollo MCP — IGNORE (owner: paid, no further evaluation)
7. Crunchbase MCP — IGNORE / out of active queue (owner experience)
8. OpenOutreach — IGNORE
9. Brave Search MCP — IGNORE

(Superseded analyst-only queue: Firecrawl was originally TEST FIRST #3, Hunter #4, Playwright #5 — overridden above.)

## B. TOP 5 TEST-FIRST RATIONALE
Superseded: only 2 active TEST-FIRST candidates remain (Scrapling, GitHub MCP). Rationale in records 1 and 4 stands.

## C. DO-NOT-INSTALL-YET LIST
Per owner decisions: Firecrawl (RESERVE; do not connect), Hunter.io, Apollo, Crunchbase, OpenOutreach, Brave Search — all IGNORE/RESERVE. No installs of any kind until the installation gate (section E) is passed.

## D. EXPERIMENT D1 — SCRAPLING CONTROLLED EXPERIMENT PROTOCOL (designed 2026-09-13; EXECUTED 2026-09-13 UTC — result: PASS)

> **D1 outcome (recorded):** PASS on all five frozen thresholds (coverage 6/6 classes ~30 items ≥ baseline 12; 100% claims snapshot-backed; 6 materially new decision-relevant signals incl. corrected Bolna role list and GreyLabs co-founder conflict resolution; zero governance breaches; 12/12 spot-check accuracy). Recommended disposition: INSTALL as the B2B evidence-capture layer — owner approval pending. Full result: `02_AI_STACK/TOOL_EVALUATIONS/SCRAPLING_EXPERIMENT_D1_2026-09-13.md`. Raw evidence: `paios-runtime-evidence\2026-09-13\d1-scrapling\` (outside repo). Design below is preserved unmodified.

### Frozen company set (fixed before any run; identical for both arms)
The 5 cycle-1 prospects (`11_STATE/B2B_CYCLE_2026-09-13.md`), chosen because a complete baseline evidence record already exists for them:
1. Logibee (connectsys/logibee.ai)
2. Bolna AI (bolna.ai)
3. MaxHome.AI (maxhome.ai)
4. GreyLabs AI (greylabs.ai)
5. Simplismart (simplismart.ai)

### Frozen signal taxonomy (what counts as a signal; fixed before run)
For each company, evidence-backed items in these classes:
- S1 open roles / hiring (careers pages, boards)
- S2 funding/financial events
- S3 product/technology positioning
- S4 decision-maker identity
- S5 contact channel (public, verified)
- S6 tech-stack evidence (repos, docs, engineering blogs)

### Baseline arm
Existing cycle-1 record (documented methodology: runtime web search + WebFetch; evidence = cited URLs; 12 recorded signals). No new baseline run — the baseline is the frozen cycle-1 record, applied identically via its recorded methodology if a gap requires re-checking.

### Enhanced arm (only after owner authorizes install for this test)
Personal AI OS + Scrapling (base + `[fetchers]`; MCP optional and separately recorded if used). Scope limits: public pages only; respect robots.txt; no login-walled or LinkedIn automation; no StealthyFetcher anti-bot features in this test (plain Fetcher/DynamicFetcher only — governance constraint, recorded as deviation from full capability set).

### Task (identical target list per company)
For each company: (a) find S1 signals on the company's own careers/jobs pages; (b) extract S3/S6 evidence from product/docs pages; (c) store one raw evidence snapshot per claim (HTML/markdown/screenshot) with URL + retrieval timestamp into a local evidence folder OUTSIDE the canonical repo; (d) log elapsed time and any failures.

### Measurements
| Metric | Method |
|---|---|
| Relevant signal coverage | count of taxonomy signals found, vs baseline per company |
| Evidence quality | each claim classified FACT/INFERENCE/CLAIM with source tier |
| Provenance completeness | % of claims with stored snapshot + URL + timestamp |
| Extraction accuracy | spot-check 10 extracted facts against live page content |
| False positives | claims not supportable by their snapshot |
| False negatives | baseline-known signals missed by Scrapling arm |
| Time/effort | wall-clock + operator steps per company |
| Token/compute overhead | metered where the MCP/LLM path is used; else dependency-install footprint and runtime notes |
| Reproducibility | re-run 3 extrctions on 3 targets; snapshot hash stability / adaptive relocation success |
| Governance compliance | public-page scope held, robots respected, no ToS-risky fetch modes |
| Material usefulness | any NEW decision-relevant signal the baseline missed |

### C. SUCCESS / FAILURE THRESHOLDS
- **PASS (authorize INSTALL consideration):** signal coverage ≥ baseline (≥12 total across set) AND ≥90% of enhanced-arm claims snapshot-backed AND ≥2 materially new decision-relevant signals found AND zero governance breaches AND extraction spot-check ≥9/10 accurate.
- **PARTIAL:** coverage ≥ baseline but <2 new signals, or snapshots ≥75% — keep as documented capability, RESERVE disposition, revisit at higher volume.
- **FAIL:** coverage < baseline, or any false positive reaching the record, or governance breach, or reproducibility broken (snapshots not regenerable).
- Owner makes the final INSTALL call; thresholds inform, they do not decide.

### E. INSTALLATION GATE (unchanged from original, restated for this test)
1. D1 pass at/above bar with raw evidence recorded here.
2. Lifecycle recorded separately: INSTALLED/CONFIGURED/VERIFIED (VERIFIED only via direct runtime inspection).
3. Output maps to canonical schema; Scrapling snapshots are evidence inputs, never source of truth.
4. No secrets in Git (none expected — no API keys required).
5. Written scope limits (above) enforced; R2 boundary unchanged.
6. Failure behavior tested and documented (404, JS-heavy failure, robots disallow).
7. Owner approval recorded in DECISION_HISTORY.md.

### Next recommended experiment after D1
**D2 — GitHub MCP (official):** same frozen 5-company set; enumerate org repos, languages, activity, careers README/jobs repos, issues/projects for S6/S1 signals; measure new Tier-1 signals vs both baseline AND D1 results (three-way comparison), false positives, time, PAT read-only scope. Pass bar: ≥3 new or corrected Tier-1 technical signals across the set with zero fabricated entries.

## F. RECOMMENDED ORDER (revised)
D1 Scrapling first (highest leverage, free, self-hosted; resolves evidence-collection quality directly). D2 GitHub MCP second. Playwright MCP only if D1 logs show HTTP-extraction failures on dynamic pages within the frozen set.
