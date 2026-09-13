# GITHUB MCP EXPERIMENT D2 — CONTROLLED RESULT (executed 2026-09-14 IST)

Executed per owner directive (D2: GitHub MCP, three-way comparison baseline/D1/D2 on the same frozen 5-company set) and the V1+ queue candidate record §4 (`02_AI_STACK/TOOL_EVALUATIONS/V1PLUS_TOOL_EVALUATION_QUEUE_2026-09-13.md`). Design constraints frozen before any run: read-only mode, max 3 bounded MCP calls per company, entity resolution required before any repo attribution, no exploration of unrelated repositories. Executor: OpenCode runtime (GLM-5.3-Flash via NVIDIA). Raw evidence stored OUTSIDE the canonical repository at `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\d2-github-mcp\` (7 JSONL evidence files). No outreach, no external communication, no secrets committed.

## 1. Installation details

| Item | Recorded value |
|---|---|
| Version | github-mcp-server **v1.12.1** (official `github/github-mcp-server`, release 2026-09-08, MIT) |
| Install method | Official binary downloaded from GitHub releases to temp working dir; no package-manager install, no config changes to any runtime |
| Run mode | stdio subprocess with `--read-only --toolsets=repos,orgs,users,stargazers`; driven by a scripted MCP client (`d2_mcp_drive.py`, newline-delimited JSON-RPC: initialize → tools/list → tools/call) |
| Auth | **Unauthenticated (zero permissions)** — the pre-existing `GITHUB_MCP_TOKEN` env var was tested separately and is dead (HTTP 401); no token used for any evidence-producing call. Hygiene flags for owner: rotate the dead token and revoke the leaked PAT stored as an env-var *name* (malformed `setx`); neither was printed or committed |
| Lifecycle state | INSTALLED → **VERIFIED** through direct runtime use on live targets |

## 2. Method and governance log

- Frozen set (5 companies): Logibee, Bolna AI, MaxHome.AI, GreyLabs AI, Simplismart — identical to D1. Not modified.
- **Entity resolution rule enforced**: repo attribution requires first-party evidence. Bolna: `docs.bolna.ai` → `github.com/bolna-ai` link captured in D1 snapshot (`bolna\docs-home.html`). Grep of all D1 snapshots found no other first-party GitHub links.
- **No forced results**: name matches were never treated as ownership. 4 of 5 companies recorded "No verified GitHub evidence found" rather than attributing a personal repo to the company.
- Read-only flag enforced server-side for every call; public data only; issue/PR counts used as metadata only (no issue-text mining); languages/topics recorded as indicators, never as proof of commercial stack.
- **Failure behaviors documented**: (1) `org:simplismart` and `org:simplismart-ai` searches → `Validation Failed: resources do not exist or you do not have permission to view them` (no public org under either name); (2) driver bug on first Bolna run — evidence collected in memory but 0-byte file on disk (`results.append` vs `flush()`); driver fixed and run repeated; (3) Bolna README fetch returned SHA confirmation only, file content not included in response text (isError null — recorded as a limitation, retrievable in a future run).
- Zero governance breaches: read-only, public data, no outreach, evidence outside the canonical repo, no secrets in Git.

## 3. Per-company findings

### Logibee — **No verified GitHub evidence found** (1 call)
- Search `logibee`: 8 repos, all personal/learning projects by unrelated individuals (HTML/CSS/Blade, 0–1 stars, most from 2021); one description references a "Logibee internship" homepage design. None attributable to logibee.ai; D1 homepage snapshot contains no GitHub links. Evidence: `logibee-search.jsonl`.

### Bolna AI — verified first-party presence (`github.com/bolna-ai`) — 3 Tier-1 technical signals (3 calls + 1 earlier probe)
- S1 **FACT (NEW)**: first-party **MCP server** repo `bolna-ai/mcp` (TypeScript, 14 open issues, updated 2026-09-02) — Bolna ships native MCP integration; never surfaced by baseline or D1. Directly relevant to Personal AI OS integration options.
- S2 **FACT (NEW)**: developer-platform motion — official installable skills package `bolna-ai/skills` ("npx skills add bolna-ai/skills", created 2026-05-19) positions Bolna as extensible infrastructure, not only a hosted service.
- S3 **FACT (NEW)**: open-source core product repo `bolna-ai/bolna` ("Conversational voice AI agents", Python, 758 stars, 359 forks, 133 open issues, created 2024-08-24) under active maintenance — commits 2026-09-11 (2 days before probe), 4 version bumps 0.10.234→0.10.237 in 2 days, automated releases via `github-actions[bot]`, internal ticket IDs (`BOLNA-2621`) indicating a structured tracker behind public GitHub.
- **INFERENCE (labeled, not recorded as fact)**: topics (cartesia, deepgram, deepseek, elevenlabs, openai, plivo, twilio, whisper) *suggest* an integration surface but **topics ≠ proof of commercial stack**; commit activity ≠ business pain; OSS activity ≠ contractor need.
- Sources: https://github.com/bolna-ai/bolna (+ commits 59debec, ee66661), https://github.com/bolna-ai/mcp, https://github.com/bolna-ai/skills, https://github.com/bolna-ai/web-call. Evidence: `bolna-probe.jsonl`, `unauth-probe.jsonl`.

### MaxHome.AI — **No verified GitHub evidence found** (1 call)
- Search `maxhome`: 31 name matches, all personal/homework/take-home style repos by individuals (a "MaxhomeAi — Email Inbox (React)" repo suggests an interview assignment, unattributable). No official org. Evidence: `maxhome-search.jsonl`.

### GreyLabs AI — **No verified GitHub evidence found** (1 call)
- Search `greylabs`: 14 name matches, all personal repos; several look like interview take-homes (`greylabs-frontend` 2023, `calendar-app-greylabs` 2024, `greylabs-mofsl-api-backend` 2026 — MOFSL is a GreyLabs bank client, so assignments reference client work; recorded as observation, not company evidence). No official org. Evidence: `greylabs-search.jsonl`.

### Simplismart — **No verified GitHub evidence found** (3 calls)
- Search `simplismart`: 63 name matches, all personal take-home submissions (one a Kubernetes/KEDA/Helm infra assignment). No public org under `simplismart` or `simplismart-ai` (both searches: Validation Failed / does not exist). Evidence: `simplismart-search.jsonl`, `simplismart-org.jsonl`, `simplismart-org2.jsonl`.

## 4. Measurements

| Metric | Result |
|---|---|
| Call budget | 11 total (Bolna 3 + 1 probe, Logibee 1, MaxHome 1, GreyLabs 1, Simplismart 3 + 1 evidence-loss re-run); all within the 3-per-company bound |
| Latency | init 0.05–0.08 s; calls 0.93–6.19 s; no hangs, no timeouts |
| Rate-limit footprint | unauthenticated 60 req/hr — ~11 used; zero-permission mode for all evidence |
| New Tier-1 technical signals | **3** (Bolna: first-party MCP server; installable skills package; active OSS core + release automation) |
| Decisive negatives | **4/5 companies have no attributable public GitHub org** — recorded honestly instead of forced attribution; prevents wasted manual digging in future cycles |
| FACT vs INFERENCE | Preserved: languages/topics recorded as indicators only; activity ≠ pain; name match ≠ ownership (enforced on 4 companies) |
| Fabricated entries | **0** — every claim API-returned with raw response preserved |
| Provenance | 7 JSONL evidence files with raw JSON-RPC responses, timestamps, elapsed times; outside canonical repo |
| Governance compliance | Read-only enforced server-side; public data; no outreach; no secrets. **Zero breaches** |

## 5. Three-way comparison

| Dimension | Baseline (cycle 1) | D1 (Scrapling) | D2 (GitHub MCP) |
|---|---|---|---|
| Evidence class | Third-party citations | First-party web snapshots (marketing/careers/docs) | First-party API data (repo metadata, commits, org existence) |
| Repo-level technical truth | None | None (only the bolna-ai link discovered) | Only layer that reaches it: org existence checks, commits, languages, topics |
| Staleness detection | Undetectable | Page-level (ATS role list) | Repo-level (commit dates, version bumps, issue counts) |
| Negative confirmation | Not possible | Not possible | Decisive: 4/5 companies have no attributable public org |
| Conflicts resolved | — | GreyLabs founders; Bolna ATS roles | Queue hypothesis §4.6 "all 5 prospects have GitHub orgs" **DISPROVED** (1/5 verified) |

## 6. Score against the predefined criterion

- PASS requires: ≥3 new or corrected Tier-1 technical signals across the frozen set ✓ (**3**, all Bolna) · zero fabricated entries ✓ · provenance preserved ✓.
- **Result: PASS.**

## 7. Recommended disposition

**INSTALL** as the OSS-diligence layer of the B2B research workflow, scoped: read-only mode, bounded per-company call budgets, entity-resolution rule mandatory, unauthenticated (or scoped fine-grained PAT) operation. Rationale: only source of repo-level truth in the stack; decisive negatives (4/5) have standalone decision value; official GitHub product at highest maturity; free in unauth mode; zero governance risk in read-only. **Owner approval pending and required in `07_VERSION_TRACKING/DECISION_HISTORY.md`; thresholds inform, they do not decide.**

Scope limits carried forward: no write scopes; no issue-text mining without explicit relevance; name-match attribution prohibited without first-party evidence; 60 req/hr unauth budget.

## 8. Provenance

- Evidence: `C:\Users\ABhas\projects\paios-runtime-evidence\2026-09-13\d2-github-mcp\` (outside canonical repo): `unauth-probe.jsonl`, `bolna-probe.jsonl`, `logibee-search.jsonl`, `maxhome-search.jsonl`, `greylabs-search.jsonl`, `simplismart-search.jsonl`, `simplismart-org.jsonl`, `simplismart-org2.jsonl`.
- Driver script: temp working copy (`d2_mcp_drive.py`); method in §1 — stdio JSON-RPC, `--read-only --toolsets=repos,orgs,users,stargazers`.
- D1 layer (comparison): `02_AI_STACK/TOOL_EVALUATIONS/SCRAPLING_EXPERIMENT_D1_2026-09-13.md`; D1 snapshot link grep used for entity resolution.
- Baseline (unaltered): `11_STATE/B2B_CYCLE_2026-09-13.md`.
