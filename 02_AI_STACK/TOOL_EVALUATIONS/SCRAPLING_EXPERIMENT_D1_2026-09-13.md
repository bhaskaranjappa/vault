# SCRAPLING EXPERIMENT D1 — CONTROLLED A/B RESULT (executed 2026-09-13 UTC / 2026-09-14 IST)

Executed per `02_AI_STACK/TOOL_EVALUATIONS/V1PLUS_TOOL_EVALUATION_QUEUE_2026-09-13.md` §D (design frozen before any run — not modified). Executor: OpenCode runtime (GLM-5.3-Flash via NVIDIA), continuing after ZCode quota exhaustion. Raw snapshots and fetch logs are stored OUTSIDE the canonical repository at `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\d1-scrapling\` (78 files: 25 HTML + 26 text + 25 metadata JSON + 2 fetch logs; 3.34 MB). Scrapling output is evidence input, never canonical truth. No outreach, no external communication. No secrets involved (no API keys used anywhere).

## 1. Installation details

| Item | Recorded value |
|---|---|
| Version | Scrapling **0.4.15** (pre-existing install; not installed during D1) |
| Source | PyPI distribution of D4Vinci/Scrapling; BSD-3-Clause; author Karim Shoair |
| Install method | pip, user site-packages (Python 3.14.0, pip 26.2.1) — installed prior to D1; verified importable (`from scrapling.fetchers import Fetcher, DynamicFetcher` OK) |
| Environment | Windows 11, Python 3.14.0; Playwright Chromium pre-existing (used by DynamicFetcher) |
| Secrets | none used, none committed |
| Lifecycle state | INSTALLED (pre-existing) → **VERIFIED** through this experiment via direct runtime use on live targets |

Tool surface actually exercised: Python `scrapling.fetchers.Fetcher` (plain static, TLS-impersonated, no stealth) for 19 static targets, and `scrapling.fetchers.DynamicFetcher` (Playwright rendering, no stealth/anti-bot flags) for 4 JS-rendered targets + 1 ATS board. The Scrapling MCP server (connected to this runtime) was used only for initial robots.txt checks and one page-recon batch; all experiment fetches were scripted for reproducibility.

## 2. Method and governance log

- Frozen set (5 companies, both arms): Logibee, Bolna AI, MaxHome.AI, GreyLabs AI, Simplismart — identical to cycle-1 baseline set. Not modified.
- Frozen taxonomy S1–S6. Not modified. Thresholds fixed per §D before results were seen.
- **robots.txt compliance enforced in code** (`urllib.robotparser` checked before every fetch; skip-on-disallow; fetch-log records the verdict per URL). All 5 domains' robots.txt fetched and archived. Result: every target URL allowed. Logibee disallows only `/book-demo/thank-you` and `/industries/framework` (not fetched); Bolna/GreyLabs disallow only static-asset paths; MaxHome and Simplismart have no disallow rules.
- Redirect note (recorded honestly): `bolna.ai/careers` redirects to `jobs.ashbyhq.com/bolna`; the script's robots check ran against the origin URL. The redirect target's robots.txt was verified post-hoc: only `/meeting/`, `/b/`, `/api/` disallowed — `/bolna` allowed. Also `docs.bolna.ai` → `www.bolna.ai/docs` and `docs.simplismart.ai` → `/overview`: both robots-allowed.
- Public pages only. No login-walled content. No LinkedIn automation. No StealthyFetcher, no anti-bot bypass, no proxies. Plain Fetcher + DynamicFetcher only (the design-permitted surface).
- **Failure behaviors documented** (installation-gate item E.6): 404 (`simplismart.ai/careers` does not exist); JS-heavy shell failure (maxhome.ai and greylabs.ai serve `You need to enable JavaScript to run this app.` shells to plain HTTP — 1.9 KB / 1.7 KB; identical hash across all their pages); recovery via DynamicFetcher (allowed surface) captured full rendered content (MaxHome home 493 KB; GreyLabs home 44 KB). Ashby ATS board also JS-rendered → DynamicFetcher used.

## 3. Per-company findings (enhanced arm; every claim below is snapshot-backed)

Classification: Tier 1 = company's own domain/docs; Tier 2 = company-controlled ATS board; Tier 3 = third-party press reproduced on company site.

### Logibee (Tier 1, logibee.ai) — 6 pages snapshotted
- S1 **FACT**: 5 open roles: AI Engineer (3+ yrs), Fullstack Engineer (3+ yrs, Remote/India), Android Engineer (3+ yrs), BDR (0–3 yrs), B2B SaaS Marketing (2+ yrs). NEW vs baseline: Android Engineer, BDR, B2B SaaS Marketing named. Snapshot: `logibee\careers.html`.
- S1 **FACT**: AI Engineer role page confirms route intelligence, demand signals, control-tower decision support. Snapshot: `logibee\careers-ai-engineer.html`.
- S3 **FACT**: positioning — real-time logistics command, AI Operations Planning launched as a new capability (zone-level demand forecast, driver-capacity calculation, scenario simulation). NEW vs baseline. Snapshot: `logibee\home.html`.
- S4 **FACT**: Founder & CEO Burhan Surti, 25+ yrs enterprise software — Tesco, Alibaba, RedMart, **Future Group, Wipro** (last two NEW). Snapshot: `logibee\company-founder.html`.
- S5 **FACT**: public careers email `hr@logibee.ai` via careers-page mailto; contact page present. Snapshot: `logibee\careers.html`, `logibee\company-contact.html`.
- S6 **FACT**: API-first architecture, 50+ integration points, REST/webhooks/token auth; integration ecosystem (ZID, Salla, Unicommerce, NearPay, Mada, MSG91, Twilio). NEW vs baseline. Snapshot: `logibee\home.html`.

### Bolna AI (Tier 1 + Tier 2) — 5 pages snapshotted
- S1 **FACT (corrects baseline)**: current own-ATS board (jobs.ashbyhq.com/bolna) shows **9 open positions, all full-time on-site (Bengaluru 7 / Delhi 4)**: AI Solutions Engineer, Conversation Quality Analyst, Enterprise Lead, 2× Marketing, 3× People/Culture, Product Designer. The baseline's cited **Founding Engineer – AI/ML and Python Backend roles are no longer listed** — hiring has shifted to GTM/ops; only AI Solutions Engineer is technical. MATERIAL new signal; changes the cycle-1 pain-signal read. Snapshot: `bolna\careers-ashby-js.html`.
- S2 **FACT**: $6.3M seed led by General Catalyst (own newsroom, confirming baseline's third-party citation); **Y Combinator funding** and **YourStory Tech30 2025 recognition**; **500K+ voice conversations monthly across 10+ Indian languages** (scale metric NEW). Snapshot: `bolna\newsroom.html`.
- S3 **FACT**: Voice AI platform for Indian languages confirmed. Snapshot: `bolna\home.html`.
- S6 **FACT**: docs.bolna.ai live (voice-agent platform docs). Snapshot: `bolna\docs-home.html`.
- Not found on fetched pages: decision-maker page (baseline S4 via YC page stands, unverified by D1 — recorded as scope miss, not extraction miss); no public email on site.

### MaxHome.AI (Tier 1) — 3 pages snapshotted (DynamicFetcher required)
- S2 **FACT**: own Press section: "MaxHome.AI raises $5 million to streamline real estate transactions" — HousingWire, **September 25, 2025** (exact date NEW vs baseline); second piece: "Divya Aathresh on using AI to solve brokerage back office problems" (Dec 5, 2024). Snapshot: `maxhome\home-js.html`.
- S3 **FACT**: Processing Copilot positioning; 80% document-time reduction claim; 10+ years of transaction data; 100% real-estate focused. Confirms + extends baseline. Snapshot: `maxhome\home-js.html`.
- S4 **FACT**: founder Divya Aathresh named in press headline. Snapshot: `maxhome\home-js.html`.
- S1 **FACT**: careers page states active hiring ("WE'RE HIRING", "See open positions" → external board). No specific roles on own site. Snapshot: `maxhome\careers-js.html`.
- S5: no public email (demo form only) — recorded absence.

### GreyLabs AI (Tier 1) — 3 pages snapshotted (DynamicFetcher required)
- S2 **FACT (NEW funding history)**: own About page — 2024 seed **₹12 Crores led by Z47 (formerly Matrix Partners India)** with angels; 2025 Series A **₹85 Crores led by Elevation Capital and Z47**. Baseline had only "₹85 crore led by Elevation Capital"; Z47 co-lead + seed round are materially new. Snapshot: `greylabs\about-js.html` (banner: "raises Rs 85 crores from Elevation Capital & Z47", `greylabs\home-js.html`).
- S4 **FACT (resolves baseline CONFLICT)**: full leadership team on own About page — **Aman Goel (Co-Founder & CEO), Harshita Srivastava (Co-Founder & CPO), Shreyas Patel (Co-Founder & CTO), Raj Sanghavi (Co-Founder & COO), Debabrata Basak (Co-Founder & CCO), Shivam Gupta (Co-Founder & CGO)** — all IIT alumni. Baseline recorded "co-founder list varies by source — CONFLICT"; the first-party page resolves it. Snapshot: `greylabs\about-js.html`.
- S5 **FACT (NEW)**: public direct contact **hello@greylabs.ai**, phone +91 9818841545, Mumbai address, CIN U62013MH2023PTC410388. Baseline had no direct contact (LinkedIn/Wellfound only). Snapshot: `greylabs\home-js.html`.
- S3 **FACT**: agentic AI product lines — Voice AI Agents, Speech Analytics, **Email Analytics (NEW)**; use cases telesales/collections/service/renewals. Snapshot: `greylabs\home-js.html`.
- S6 **FACT**: ISO certified, SOC 2, DPDP compliance claims; CIN registered 2023. Snapshot: `greylabs\home-js.html`.
- S1 note: own careers page contains no listed roles (genuinely empty) — baseline's Wellfound "Research Engineer" listing is third-party and unverifiable on the company's own site (possibly stale; not re-checked here — D1 scope is own pages). Snapshot: `greylabs\careers-js.html`.
- Correction note: About page says **40+ enterprise clients** (baseline said "50+ financial institutions" from third-party sources) — first-party figure recorded.

### Simplismart (Tier 1) — 3 pages snapshotted
- S3 **FACT**: "Tailor-made inference for any model at scale"; MLOps platform for deploying/serving/optimizing models; custom inference engine. Confirms baseline. Snapshot: `simplismart\home.html`.
- S6 **FACT (NEW pain-fit evidence)**: customer case metrics on own site — image-generation costs cut **$30,000 → under $1,000** while halving inference time; peak GPU usage **15 → 6** at equal latency; vision model for medical prescriptions at **95% accuracy**; **150+ pre-deployed models** marketplace (Llama, Mistral). Snapshot: `simplismart\home.html`, `simplismart\docs-home.html`.
- S1/S2 note: own careers page does not exist (404) and funding not stated on fetched pages — baseline's Wellfound roles and Accel $7M Series A citations stand unverified by D1 (scope boundary, recorded honestly).

## 4. Measurements

| Metric | Result |
|---|---|
| Signal coverage | 6/6 taxonomy classes covered across set (baseline covered S1–S5 via third parties; D1 adds first-party S6). ~30 distinct snapshot-backed signal items vs baseline's 12 recorded signals. Coverage ≥ baseline on every company where own-site content exists. |
| Evidence quality | Every claim classified FACT with source tier (Tier 1 company domain; Tier 2 ATS; Tier 3 press-reproduced). No INFERENCE entered the record unlabeled. |
| Provenance completeness | **100% of enhanced-arm claims are snapshot-backed** (raw HTML + extracted text + metadata with URL, final URL, HTTP status, retrieval timestamp, SHA-256). |
| Extraction accuracy | Spot-check **12/12 accurate** against snapshot/live content (roles count, role details, founder names/backgrounds, email, ATS role list, funding amounts/dates/leads, product metrics, case-study numbers). |
| False positives | **0** — no claim entered without snapshot support. |
| False negatives | 2 scope misses recorded honestly (Bolna S4 on YC page; Simplismart S1/S2 on external boards) — these are out-of-scope pages, not extraction failures. Baseline-known signals that own-site pages contradict (Bolna founding-engineer roles; GreyLabs 50+ clients) are treated as baseline staleness, not Scrapling misses. |
| Reproducibility | Re-run on 3 targets: static pages **hash-identical** across runs (logibee home `c865e090…` 694,280 B; bolna newsroom `e91b8c1f…` 177,358 B); dynamic page hash differs (JS nonces — expected) with content stable (493,612 vs 493,613 B) and text extraction identical in substance. Snapshots regenerable. |
| Time/effort | ~15 minutes end-to-end for 24 fetches across 5 companies + 3 re-runs, via one reusable script; operationally far below the manual cycle-1 research time. |
| Token/compute overhead | Zero LLM tokens for extraction (local scripted fetch); Scrapling 0.4.15 + Playwright Chromium pre-existing (no new install footprint); ~3.34 MB snapshots. |
| Governance compliance | Public pages only; robots enforced in code with per-URL verdicts logged; no stealth/anti-bot features; no outreach; no external communication; snapshots outside the canonical repo; no secrets. **Zero breaches.** |
| Materially new decision-relevant signals | **6** — (1) Bolna current ATS role list corrects a stale baseline pain signal (founding-engineer roles closed; GTM-heavy hiring); (2) GreyLabs full 6-founder leadership team resolves the baseline CONFLICT; (3) GreyLabs direct public email + phone + CIN; (4) GreyLabs 2024 ₹12cr seed led by Z47 + Z47 co-lead on Series A; (5) Logibee AI Operations Planning capability + integration-stack evidence; (6) Simplismart concrete cost/GPU optimization case metrics. |

## 5. Baseline vs enhanced comparison

| Dimension | Baseline (cycle 1) | Enhanced (D1, Scrapling) |
|---|---|---|
| Evidence capture | Cited URLs only — not reproducible | Raw HTML snapshot per claim, URL + timestamp + SHA-256 |
| Coverage | 12 recorded signals, S1–S5 | ~30 snapshot-backed items, S1–S6 |
| JS-rendered companies (MaxHome, GreyLabs, Ashby) | Handled via third-party summaries | First-party content recovered via allowed DynamicFetcher |
| Conflicts | GreyLabs co-founder roles CONFLICTING | Resolved from first-party page (6 co-founders with roles) |
| Stale signals | Undetectable at citation level | Detectable: Bolna founding-engineer roles no longer listed; GreyLabs 40+ vs "50+" |
| Contact discovery | LinkedIn/board channels only | Direct public email found for GreyLabs; Logibee mailto re-confirmed from primary source |
| False-positive risk | Search-engine summaries could drift | Every claim verifiable against stored snapshot |
| Cost | Manual search + fetch time | Free, self-hosted; zero LLM tokens; ~15 min for the set |

## 6. Score against frozen thresholds

- PASS requires: coverage ≥ baseline (≥12) ✓ (6/6 classes, ~30 items) · ≥90% claims snapshot-backed ✓ (100%) · ≥2 materially new decision-relevant signals ✓ (6) · zero governance breaches ✓ · spot-check ≥9/10 ✓ (12/12).
- **Result: PASS** (all five criteria met; nothing qualifies PARTIAL or FAIL; no snapshot-unsupportable claim entered the record; snapshots regenerable).

## 7. Recommended disposition

**INSTALL** (as the evidence-capture layer of the B2B research workflow — company research and signal collection), with lifecycle recorded separately: INSTALLED (pre-existing 0.4.15) → VERIFIED (direct runtime use in this experiment). Install-gate items from §E: raw evidence recorded (this file + external archive) ✓; output maps to canonical schema — snapshots are evidence inputs, never source of truth ✓; no secrets ✓; written scope limits enforced ✓; failure behavior tested and documented (404 / JS-shell / robots) ✓; R2 boundary unchanged ✓. **Owner approval for formalizing the disposition is pending and required in `07_VERSION_TRACKING/DECISION_HISTORY.md`; thresholds inform, they do not decide.**

**Promoted 2026-09-14** (owner promotion pass): disposition formalized as INSTALL — registered in `02_AI_STACK/AI_TOOL_REGISTRY.md` as INSTALLED → VERIFIED, CURRENT (B2B evidence-capture layer), with production scope and governance constraints recorded there.

Scope limit carried forward (recorded as deviation from full capability set): no StealthyFetcher/anti-bot bypass; public pages + robots.txt compliance only; no LinkedIn automation. Playwright MCP remains conditional and NOT triggered — Scrapling's own DynamicFetcher handled all JS-rendered targets in the frozen set.

## 8. Provenance

- Snapshots + fetch logs: `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\d1-scrapling\` (outside canonical repo), 78 files, fetch timestamps 2026-09-13T19:55–20:03 UTC.
- Fetch scripts (reproducible): temp working copy; method documented in §2 — scrapling.Fetcher (static) + DynamicFetcher (Playwright), robots-checked, 1.5 s inter-request delay.
- Baseline (unaltered): `11_STATE/B2B_CYCLE_2026-09-13.md`.
- Experiment design (unaltered): `02_AI_STACK/TOOL_EVALUATIONS/V1PLUS_TOOL_EVALUATION_QUEUE_2026-09-13.md` §D.
