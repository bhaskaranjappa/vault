# OPENOUTREACH vs SCRAPLING — B2B LEAD-FINDING COMPARISON TEST

Date: 2026-09-15. Executor: ZCode (primary). Protocol: `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.
Isolated workspace: `C:\Users\ABhas\projects\paios-eval-20260915\` (outside canonical repo; untouched by PAIOS tooling).
Rules honored: no emails sent, no contacts made, no production tooling modified, public pages only, plain fetch (no anti-bot modes per D1 governance).

ICP (frozen): "Find 10 B2B software/technology companies that could plausibly need AI/software engineering services."

## TEST A — OpenOutreach (github.com/eracle/OpenOutreach)

### Installation & contract
- Cloned repo (depth 1) into isolated workspace. Architecture: Django host package over two child packages — `openoutfind==0.1.12` (discovery/qualification) and `openoutsend==0.1.36` (mail sending).
- Installed `openoutreach` CLI into isolated venv (`ooenv`). `openoutreach status` runs; reports `not_initialized` until `init`. CLI contract verified: `init`, `find N [emails]`, `send`, `run`, `status`. `find` is free (no credits); `find N emails` = 1 credit/address; `send`/`run` = R2 territory (not executed).

### CRITICAL QUESTION — does OpenOutreach scrape arbitrary websites?
**NO — verified from implementation, not marketing.**
- README itself: "zero platform-ToS surface: browserless, no social-network account, **no scraping**."
- Full `openoutfind` source grep: no scraping library (no BeautifulSoup/Playwright/Selenium/Scraply/crawler). Only `requests` for API calls.
- `discovery.py` L14: "Lead discovery via BetterContact Lead Finder" — `https://app.bettercontact.rocks/api/v2/lead_finder/async`. All leads come from BetterContact's licensed database.
- `enrichment/apollo.py`: Apollo `people/match` email lookup present but "wired, not exposed, never run against a live key."
- Its own code comments repeatedly disclaim scraping ("no extra scrape", "Neither is scraped from any network", "synthesized (not scraped)").

### Live research-only run: BLOCKED
`find` requires (a) a BetterContact account/API key — account creation is an outward-facing action not performed autonomously — and (b) an LLM provider key. No PAIOS keys were consumed. Capability findings below therefore rest on implementation inspection (strong) plus blocked-run documentation, not a live lead pull.

### What it does well (from code inspection)
- ICP → LLM-generated query tree → BetterContact search → embedding-based qualification → per-lead verdict with written reason → CSV/JSON output. Structured output and reasoning are first-class.
- Agent-controlled use is a design goal (`skills/find-leads/SKILL.md` defines flags that cost credits vs free; `--agent-qualify`, `--verdict`, `--reason` for agent-driven qualification).
- Quality of engineering is high (typed seniority vocabulary, retry transports, error taxonomy).

### What it does not do
- Does NOT scrape/crawl arbitrary company websites. Cannot extract from a prospect's own site, careers page, or tech stack. Discovery breadth is bounded by BetterContact's database and its query vocabulary.

## TEST B — Scrapling 0.4.15 (INSTALLED→VERIFIED)

Script: `paios-eval-20260915/scrapling_b2b_test.py`; raw evidence: `scrapling_results.jsonl`, `scrapling_test.log` (preserved in workspace).

- **Discovery**: no built-in search; achieved via Bing HTML fetch (plain Fetcher, HTTP 200) + base64 decode of `bing.com/ck/a` redirects → **26 unique domains in ~4.5s across 5 ICP queries**. DuckDuckGo HTML endpoint returned 202 (anti-bot) — DDG not usable with plain fetcher. Discovery noise is significant (directories, ChatGPT, non-ICP sites) — needs an LLM/agent filter.
- **Crawl/extract**: 12 company sites fetched; 11/12 homepage success; automatic follow-up into careers/contact subpages (up to 3 pages/company); 1 failure (SSL chain, startupindia.gov.in). Per-company latency 0.4–6.1s (one 33s outlier, JS-heavy site).
- **Decision-maker/contact info**: emails extracted from homepage/contact/careers where publicly present (e.g. proptechlabs.com: 5 emails; proptechconnect.com: info@ + networking@). No name/seniority extraction (needs targeted parsing per site).
- **Heterogeneous structures**: handled plain HTML, React/Next shells, event sites; JS-only sites return empty shells with plain fetcher (documented limitation; StealthyFetcher exists but is out of governance scope).
- **Structured output**: JSONL with title, meta description, H1s, emails, careers URL, hiring signals, tech keywords, page count, errors, latency — directly LLM/agent-consumable.

## COMMON BENCHMARK SCORECARD

| Dimension | OpenOutreach | Scrapling |
|---|---|---|
| Discovery capability | BetterContact DB via ICP query tree (not scraping) | Search-engine HTML + agent queries; noisy but working |
| Source coverage | Licensed DB only | Arbitrary public web |
| Data richness | Person/company rows from DB | Full page content, structure, emails, keywords |
| Decision-maker discovery | Yes (DB roles/seniority) — unverified live | Partial (emails; names need per-site parsing) |
| Qualification quality | High (LLM + embeddings + written reasons) | None built-in — agent/LLM layer does it |
| Reasoning quality | High (per-lead verdict prose) | External (PAIOS agent) |
| Extraction reliability | N/A (no extraction) | 11/12 homepages; 1 SSL fail; JS shells empty |
| Structured output | CSV (schema-owned) | JSONL (schema-free, agent-defined) |
| Cost/credits | Free discovery; 1 credit/email; BetterContact account needed | Free; no accounts |
| Speed/friction | Blocked on credentials (account signup) | 26 domains/4.5s; ~2s/company |
| Reproducibility | Good (pinned children, deterministic CLI) | Good (script is deterministic; engine SERPs vary) |
| Failure modes | Missing key, silent empty query pages (seniority vocab), credit burn on emails | 202 anti-bot, SSL chains, JS-only shells, SERP noise |
| External dependencies | BetterContact API (mandatory), LLM key, SMTP for send | None (pure local fetch) |

## FINAL DECISION

**Critical answer: OpenOutreach does NOT scrape arbitrary websites — verified at source level.** Its discovery is a licensed third-party database (BetterContact), the same category of dependency the owner already ruled IGNORE for (Apollo/Crunchbase/Hunter: paid data APIs, external account + credit dependency).

Recommended architecture: **Scrapling + agent (existing PAIOS pattern)** — discovery via agent search queries, Scrapling for arbitrary-site extraction, PAIOS agent for ICP qualification and written reasons (the reasoning quality OpenOutreach advertises is exactly what the B2B workflow's FACT/INFERENCE/CLAIM discipline already produces, with better provenance).

- A. OpenOutreach alone: REJECT as discovery engine for PAIOS — depends on external DB + account + credits; no arbitrary-web extraction.
- B. Scrapling alone: insufficient for discovery (no search, noisy SERPs) but excellent extraction.
- C. Scrapling + OpenOutreach: adds a second external dependency without closing any gap Scrapling+agent has; OpenOutreach's qualifications duplicate what the agent layer already does.

**Disposition: OpenOutreach = IGNORE (maintained from owner ruling 2026-09-13, now upgraded from opinion-adjacent analysis to implementation-level evidence). Scrapling remains INSTALLED→VERIFIED as the extraction layer. No new installs.**

## Unknowns
- Live OpenOutreach `find` quality (blocked on BetterContact account — only owner can create one).
- Scrapling StealthyFetcher on JS-only sites (out of D1 governance scope for this test).
- Decision-maker *name/title* extraction rate on arbitrary sites (needs a second bounded experiment with per-site parsing).
