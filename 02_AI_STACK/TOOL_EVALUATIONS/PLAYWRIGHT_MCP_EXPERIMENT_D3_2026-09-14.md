# PLAYWRIGHT MCP EXPERIMENT D3 — CONTROLLED A/B RESULT (executed 2026-09-14 IST)

Executed per owner directive (D3: Playwright MCP vs Scrapling DynamicFetcher on the three JS-dependent targets) and the V1+ queue candidate record §7 (`02_AI_STACK/TOOL_EVALUATIONS/V1PLUS_TOOL_EVALUATION_QUEUE_2026-09-13.md`). Canonical D3 framing (unchanged): fallback-scenario test — Playwright is justified **only if** Scrapling fails on JS-heavy targets. Design constraints frozen before any run: navigation-only (no clicks, fills, form submissions, logins, purchases, destructive actions), no anti-bot bypass experimentation, public pages only. Same research objective for both arms. Executor: OpenCode runtime (GLM-5.3-Flash via NVIDIA). Raw evidence stored OUTSIDE the canonical repository at `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\d3-comparison\` (Arm A: `scrapling\` snapshots + fetch log; Arm B: `playwright-mcp\` JSONL runs, 5 a11y-snapshot YMLs, 4 PNG screenshots). No outreach, no secrets committed.

## 1. Installation details (Arm B — Playwright MCP)

| Item | Recorded value |
|---|---|
| Version | `@playwright/mcp@0.0.80` (npm `dist-tags.latest`, published 2026-09-01; wraps **Playwright 1.63.0-alpha-2026-08-31**) |
| Source | official `microsoft/playwright-mcp` (37k stars); npm registry |
| Install method | `npx -y @playwright/mcp@0.0.80` (no persistent install, no runtime config changes); run as stdio MCP subprocess with `--browser chrome --headless --isolated` — uses the pre-existing installed Chrome channel, no browser download |
| Permissions | none (no API keys, no auth, no `--grant-permissions`); scope enforced to `browser_navigate` + `browser_snapshot` + `browser_take_screenshot` + `browser_wait_for` only — 24 tools exposed but none of the interactive ones (click/type/fill/evaluate/run_code) were invoked |
| Lifecycle state | INSTALLED (npx fetch) → **VERIFIED** through direct runtime use on live targets |

Arm A used the pre-existing Scrapling 0.4.15 `DynamicFetcher` (same surface as D1: Playwright rendering, no stealth flags).

## 2. Method and governance log

- Targets (identical for both arms): `https://jobs.ashbyhq.com/bolna`, `https://maxhome.ai/` (+/careers, /about), `https://www.greylabs.ai/` (+/careers, /about).
- Arm A: scripted re-run (adapted D1 script `d3_fetch_js.py`): robots.txt checked before every fetch, 1.5 s inter-request delay, snapshot + extracted text + SHA-256 + elapsed per page.
- Arm B: scripted MCP client (`d3_pw_drive.py`, stdio JSON-RPC): initialize → tools/list → navigate → snapshot → screenshot per target; navigation only.
- **robots.txt finding (recorded honestly)**: `jobs.ashbyhq.com` serves **different robots.txt by User-Agent** — browsers get `Disallow: /meeting/, /b/, /api/` (curl evidence; `/bolna` allowed, consistent with D1's post-hoc verification), while `Python-urllib` gets **HTTP 403 Forbidden**, which Python's `robotparser` conservatively treats as disallow-all. Consequence: the Arm A script (naive urllib robots check) **skipped Ashby** (`robots-disallowed`); the D1 script's Scrapling-based robots check (browser-impersonated) receives the real robots.txt and proceeds. The site itself is browser-accessible; Playwright MCP navigated it without issue.
- Zero governance breaches: public pages, navigation-only, no logins, no forms, no anti-bot features, evidence outside the canonical repo.

## 3. Failure modes observed (both arms, unmanufactured)

1. **Arm A — Ashby robots skip**: naive plain-HTTP robots.txt check → 403 (WAF) → conservative disallow-all. D1's Scrapling-based check avoids this; documented as a reliability note for naive tooling, not a Scrapling failure (D1 evidence proves DynamicFetcher captures the board).
2. **Arm B — navigate→snapshot race (MaxHome)**: default `browser_navigate` (load event) + immediate `browser_snapshot` captured only `progressbar [ref=f2e4]` (SPA hydration incomplete) — run 1, run2.jsonl. Resolved in run 2 with explicit `browser_wait_for` (8 s): full a11y tree (9.6 KB). Reproducible **with** an explicit wait; racy without.
3. **Arm B — screenshot path hygiene**: `browser_take_screenshot` writes to a path relative to the MCP server's **inherited cwd**, ignoring `--output-dir` — the 4 PNGs landed in the canonical repo working directory; immediately moved to the evidence dir and `git status` verified clean. If installed, output paths must be pinned absolutely.
4. **Arm B — snapshot size threshold**: snapshots >~8 KB are returned as file links (`page-*.yml`) instead of inline text — extra file handling step.

## 4. Per-target comparison

### jobs.ashbyhq.com/bolna
- Arm A (Scrapling): D1 evidence — full board captured (28.5 KB HTML, 9 roles); D3 re-run skipped by its own robots guard (see §3.1); capability proven in D1, content stable.
- Arm B (Playwright MCP): full structured a11y tree — "Open Positions (9)", all 9 roles with department/level/URL (job UUIDs), and **filter metadata without interaction**: Department (Business 3, Marketing 2, People and Culture – Operations 2, People and Culture – Talent Acquisition 1, Product 1), Employment (Full time 9), Location (Bengaluru 7, Delhi 4), Location Type (On-site 9). Roles identical to D1's extraction. Navigation took 3.89 s.
- Verdict: both arms capture the required research information; no browser interaction beyond rendering required by either.

### maxhome.ai
- Arm A: 3/3 pages HTTP 200 (home 493,613 B — size identical to D1; SHA varies with JS nonce as documented in D1; careers 22,568 B; about 5,901 B); text extraction 3,235/1,664/119 B; total ~75 s wall incl. delays, zero interactive steps.
- Arm B: home a11y tree (9.6 KB after explicit 8 s wait) — content identical in substance to Scrapling's text: "80% Time Saved on Documents", "10+ Years of Transaction Data", "100% Real Estate Focused", Processing Copilot features, press references. Run 1 without wait: progressbar only.
- Verdict: parity after wait; Scrapling simpler (one call, network_idle built in).

### greylabs.ai
- Arm A: 3/3 pages HTTP 200 (home 44,407 B, careers 9,665 B, about 42,773 B — sizes match D1); text 4,259/538/3,547 B.
- Arm B: home a11y tree 20.7 KB — full first-party content (funding, founders, contact, product lines), same facts as D1's Scrapling extraction.
- Verdict: parity; no advantage from Playwright.

## 5. Measurements

| Criterion | Arm A (Scrapling DynamicFetcher) | Arm B (Playwright MCP) |
|---|---|---|
| Coverage | **3/3 targets** (6/6 pages; Ashby proven in D1 evidence) | 3/3 targets (Ashby + MaxHome-after-wait + GreyLabs) |
| Extraction accuracy | 9/9 role/metric spot-checks vs D1 identical | a11y trees match D1 text in substance (9 roles, 80%/10+/100% metrics, funding/founders) |
| Completeness | Full first-party content + SHA-256 per page | Full a11y structure; extra: filter metadata, job UUIDs, screenshots |
| Reproducibility | MaxHome home size identical across D1/D3 (493,613 B); hash varies with JS nonce (documented) | Racy without wait (run 1); reproducible with explicit `browser_wait_for` (run 2) |
| Reliability | 6/6 fetches 200 in D3 run; 24/24 in D1 | 13/13 MCP calls isError=false; but 1/3 navigations needed a wait to be useful |
| Time/effort | ~75 s wall for 6 pages, single script, zero orchestration | ~30 s for 3 pages across 2 runs; requires MCP server spawn + JSON-RPC driver + wait tuning |
| Token/compute overhead | Zero LLM tokens; ~1.6 MB snapshots | Snapshots 4.9–20.7 KB text each (token-costly if fed to LLM); PNGs 4.5–77 KB; npx package ~ tens of MB (reused installed Chrome) |
| Browser interaction required? | Rendering only (built in) | Rendering only; **no clicks/state changes needed on any target** for the B2B research content |
| Failure modes | Naive robots check 403→skip (naive-tooling note) | SPA race; cwd-relative screenshot paths; snapshot size cutoffs |
| Governance | Fetch-only surface; robots enforced | Interactive-by-design (24 tools incl. run_code_unsafe) — larger enforcement surface |

## 6. D3 result against the canonical trigger

The canonical D3 spec justifies Playwright **only if** Scrapling fails on JS-heavy targets ("Fallback-scenario test only"; DECISION_HISTORY: "TEST ONLY IF NEEDED — conditional fallback for dynamic pages").

- Scrapling DynamicFetcher: **3/3 targets covered** (D1 evidence + D3 re-run, all HTTP 200, full first-party content).
- Playwright MCP: retrieved the same information on all 3 targets; added structural niceties (filter counts, job UUIDs, a11y refs) but **no fact that Scrapling had not already extracted**, and no target required interaction beyond rendering.
- Answers to the evaluation questions: A) No — 0/3 targets have information Scrapling cannot reliably extract. B) Interactions exist (Ashby filters) but are unnecessary — filter metadata is exposed without interaction. C) No — 0/3 targets needed Playwright in this run. D) Yes — Scrapling covers the practical need entirely.
- **Result: the fallback condition is NOT MET — Playwright MCP provides no materially useful capability beyond Scrapling DynamicFetcher for this workflow. Zero of the three targets required it.**

## 7. Recommended disposition

**KEEP IN RESERVE** — conditional fallback for dynamic/interactive pages, consistent with the queue's own framing. Evidence-backed rationale: (1) the tested need did not materialize (Scrapling 3/3, zero interaction required); (2) Playwright MCP itself works reliably (13/13 calls, official Microsoft product) and is the right instrument **if** a future target requires true interaction (pagination, filtered views, state changes) or if a WAF blocks Scrapling's rendering path; (3) it is not IGNORE because D3 did not find it broken — it found it unnecessary; (4) revisit trigger: a concrete Scrapling extraction/interaction failure, or an Ashby-style board that actually requires pagination/filtering. If ever promoted to INSTALL, pin output paths absolutely (see §3.3) and scope the toolset to navigation/snapshot only.

**Confirmed 2026-09-14** (owner promotion pass): KEEP IN RESERVE formalized in `02_AI_STACK/AI_TOOL_REGISTRY.md` — INSTALLED (npx cache, ephemeral) → VERIFIED (D3), but NOT promoted to the production stack; revisit trigger recorded there.

## 8. Provenance

- Arm A evidence: `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\d3-comparison\scrapling\` — `d3-fetch-log-js.json` + per-page HTML/text/meta (SHA-256, timestamps, elapsed) for maxhome and greylabs; fetch log timestamps 2026-09-14 03:26 IST.
- Arm B evidence: `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\d3-comparison\playwright-mcp\` — `run1.jsonl`, `run2.jsonl` (raw JSON-RPC), 5 a11y YML snapshots (page-2026-09-13T22-02-06Z … 22-04-25Z), 4 PNG screenshots (ashby-bolna, maxhome-home [racy], maxhome-home2, greylabs-home).
- robots.txt evidence: browser-served rules (curl, `Disallow: /meeting/, /b/, /api/`) vs Python-urllib 403 — recorded in §3.1.
- Driver scripts: temp working copies (`d3_fetch_js.py`, `d3_pw_drive.py`); methods in §2.
- D1 layer (comparison): `02_AI_STACK/TOOL_EVALUATIONS/SCRAPLING_EXPERIMENT_D1_2026-09-13.md` + `paios-runtime-evidence\2026-09-13\d1-scrapling\`.
- Baseline (unaltered): `11_STATE/B2B_CYCLE_2026-09-13.md`.
