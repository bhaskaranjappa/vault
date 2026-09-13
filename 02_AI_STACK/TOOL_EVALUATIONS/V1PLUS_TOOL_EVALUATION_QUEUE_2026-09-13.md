# V1+ TOOL EVALUATION QUEUE — 2026-09-13

Evaluated per `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`. Question asked per candidate: "Does this materially improve the Personal AI OS B2B workflow enough to justify adding it?" — not "is it a good tool?" Nothing installed, authenticated, or connected during this evaluation. All data below is public evidence gathered 2026-09-13; sources cited per claim. No scores invented; dispositions are judgments with stated reasons.

Baseline being improved: B2B workflow `05_WORKFLOWS/B2B_CLIENT_ACQUISITION.md` as executed in `11_STATE/B2B_CYCLE_2026-09-13.md` (manual research via general web search; evidence captured as cited URLs; contacts verified only via public LinkedIn/company channels).

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
15. **Disposition:** TEST FIRST (consistent with PLAN.md Phase 9 candidate "GitHub").
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

## A. EVALUATION QUEUE (expected value order)

1. Scrapling (+MCP) — TEST FIRST
2. GitHub MCP (official) — TEST FIRST
3. Firecrawl MCP — TEST FIRST (head-to-head vs #1; install at most one)
4. Hunter verifier — TEST FIRST (verifier mode only)
5. Playwright MCP — TEST FIRST (conditional, fallback only)
6. Apollo MCP — KEEP IN RESERVE
7. Crunchbase MCP — KEEP IN RESERVE
8. OpenOutreach — IGNORE
9. Brave Search MCP — IGNORE

## B. TOP 5 TEST-FIRST RATIONALE
Covered in records 1, 4, 5, 6, 7 above. Shared thread: each attacks a measured cycle-1 gap (evidence reproducibility, signal freshness, contact verification, JS-page fallback) without duplicating working capabilities or breaching governance.

## C. DO-NOT-INSTALL-YET LIST
- **Apollo MCP** — paid, inferred data, R2-adjacent sequences; revisit at higher volume.
- **Crunchbase MCP** — redundant with news search now; paid; community server stale.
- **OpenOutreach** — competing architecture; autonomous send violates R2; IGNORE.
- **Brave Search MCP** — duplicates built-in search; IGNORE.

## D. TEST DESIGNS (BASELINE = current OS workflow; ENHANCED = OS + candidate; same prospect universe unless stated)

**D1. Scrapling vs Firecrawl (one experiment, two arms + baseline).**
- Universe: the 5 cycle-1 prospects + 5 new prospects (fixed list, frozen before test).
- Task per tool: for each company, produce (a) careers/jobs evidence, (b) tech-stack evidence, (c) one raw evidence snapshot per claim (HTML/screenshot/markdown) with URL + timestamp.
- Measure: discovery coverage (signals found vs baseline's 12 cycle-1 signals), false positives (claims not supportable by snapshot), false negatives (baseline-known signals missed), evidence/provenance completeness (snapshot per claim %), extraction accuracy (spot-check 10 claims), time to complete batch, token/compute usage (metered), operational complexity (setup + failures), governance compliance (public pages only, robots respected).
- Pass bar: ≥ baseline signal coverage with ≥90% snapshot-backed claims, at acceptable time cost.

**D2. GitHub MCP.**
- Universe: same 10 companies' GitHub orgs.
- Task: enumerate hiring/tech-stack signals (careers README, jobs repos, languages, activity) for stage 3.
- Measure: new Tier-1 signals not in baseline record; conflicts resolved/created vs third-party job boards (e.g., Simplismart Series B claim); false positives; time; token usage.
- Pass bar: ≥3 new or corrected Tier-1 signals across the batch with zero fabricated entries.

**D3. Hunter verifier.**
- Task: take 10 already-publicly-identified contact addresses/domains (from cycle 1 + new batch; no finder mode), verify deliverability.
- Measure: verification success rate, agreement with manual/public-listing check, false positives (marked deliverable but bounced — cannot fully measure pre-send, so treat as unverifiable and record as such), time, cost in credits.
- Pass bar: verifier-only usage demonstrably compliant; ≥80% of public addresses resolved with a deliverability verdict; no guessed addresses generated.

**D4. Playwright MCP (conditional on D1).**
- Trigger: only if D1 shows both Scrapling and Firecrawl failing on ≥2 JS-heavy target pages.
- Task: capture evidence from the failed pages; measure success rate, screenshot evidence quality, time.
- Pass bar: recovers ≥1 of the failed pages with reproducible screenshot evidence.

## E. INSTALLATION GATE (evidence required before entering AI_TOOL_REGISTRY)
1. Controlled-test pass at/above the stated bar, recorded in `02_AI_STACK/TOOL_EVALUATIONS/` with raw evidence.
2. Lifecycle honesty: INSTALLED/CONFIGURED/AUTHENTICATED/VERIFIED states recorded separately, VERIFIED only from direct runtime inspection.
3. Output mapping: tool output maps to canonical record schema (source, date, status, confidence, conflict notes); vendor data NEVER becomes source of truth.
4. Secrets: no keys/tokens in Git; local env only.
5. Governance: written scope limits (public pages, verifier-only, read-only PAT, etc.); R2 boundary unchanged — no tool may send outreach.
6. Failure behavior tested: missing-data, rate-limit, offline behavior documented.
7. Owner approval for INSTALL recorded in DECISION_HISTORY.md.

## F. RECOMMENDED ORDER
**Test Scrapling first.** Rationale: evidence collection is the highest-leverage, cross-cutting stage (feeds stages 2, 3, and 7); it is free, self-hosted, and runtime-agnostic; and D1 doubles as the Firecrawl evaluation, resolving the only either/or in one experiment. GitHub MCP second (simplest, free, official). Hunter third (small, gated to verifier mode). Playwright only if triggered.

## Boundary statement
No tool installed, authenticated, or connected. No outreach sent. No contacts guessed. Canonical architecture unmodified except this evaluation record.
