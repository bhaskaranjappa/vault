# AI TOOL REGISTRY

Lifecycle: SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED.

Status usage: `CURRENT` records whether the tool is in active use in the stack; it does not assert a lifecycle stage. Installation/configuration/verification state must be stated separately using the lifecycle.

ZCode — active owner-selected hands-on executor — CURRENT by owner confirmation; use for implementation, runtime experimentation, benchmarking and evidence capture when selected.
OpenCode — active owner-selected hands-on executor — CURRENT by owner confirmation; use directly or after token/context exhaustion when selected.
Antigravity — active owner-selected hands-on executor — CURRENT by owner confirmation; runtime lifecycle/verification state remains unspecified unless directly tested.
Freebuff — active owner-selected hands-on executor — CURRENT by owner confirmation; runtime lifecycle/verification state remains unspecified unless directly tested.
Hermes Agent — orchestration/automation — VERIFIED by prior audit/user confirmation.
ChatGPT — general reasoning/research/architecture — CURRENT.
Claude — general/specialist runtime — CURRENT/UNVERIFIED for canonical-repo integration.
Gemini — model/research/Vertex work — CURRENT.
Grok — target runtime — UNVERIFIED.
Cursor — development/IDE — UNAVAILABLE_TO_OWNER; do not use for current execution or testing until access is explicitly restored.
Codex — development/agent runtime — UNAVAILABLE_TO_OWNER; do not use for current execution or testing until access is explicitly restored.
Claude Code — coding runtime — UNVERIFIED.

Tool evaluations follow `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.

## B2B evidence-collection tools — V1+ promotion pass (2026-09-14)

Promoted per owner directive after controlled experiments D1/D2/D3 (`02_AI_STACK/TOOL_EVALUATIONS/`). Lifecycle states below are only those supported by direct runtime evidence; no runtime MCP configuration was modified (no architecture changes).

| Tool | Lifecycle | CURRENT | Production scope and governance constraints |
|---|---|---|---|
| **Scrapling 0.4.15** (pip user site-packages, Python 3.14.0, BSD-3-Clause) | INSTALLED → VERIFIED | yes — B2B evidence-capture layer | Static `Fetcher` + `DynamicFetcher` (Playwright rendering, no stealth/anti-bot flags); robots.txt compliance enforced in code with per-URL verdicts logged; public pages only, no logins, no LinkedIn automation; raw snapshots stored OUTSIDE the canonical repo and used as evidence inputs, never canonical truth. Evidence: D1 (PASS), D3 re-run (6/6 pages, sizes match D1). |
| **github-mcp-server v1.12.1** (official binary, MIT; `C:\Users\ABhas\tools\github-mcp-server\github-mcp-server.exe`, 26,080,768 B, SHA-256 `19a2a274472f535bef3080e7b2a79becb767a18ce8bb8ca4add6a708498b55e2`) | INSTALLED → VERIFIED | yes — read-only OSS-diligence layer | stdio subprocess with `--read-only` MANDATORY; unauthenticated zero-permission mode is the operating mode (no PAT configured — the pre-existing `GITHUB_MCP_TOKEN` env var is dead/401; rotate it); bounded usage: max 3 read/search calls per company; entity-resolution rule mandatory (repo attribution requires first-party evidence; name match ≠ ownership); languages/topics are indicators, not proof of commercial stack. Evidence: D2 (PASS). |

Lifecycle precision (distinction preserved — no state asserted without evidence):
- **Scrapling**: INSTALLED (pip, pre-existing 0.4.15) → VERIFIED (direct runtime use in D1 + D3). ENABLED / CONFIGURED / AUTHENTICATED: not applicable — Python library imported directly by scripts; no auth, no service.
- **github-mcp-server**: INSTALLED (official release binary, relocated from temp to `C:\Users\ABhas\tools\`) → VERIFIED (direct runtime use in D2). **ENABLED: no** (not wired into any runtime MCP config — by design, per no-architecture-changes rule). **CONFIGURED: no**. **AUTHENTICATED: no** (unauthenticated zero-permission mode used for all D2 evidence; if a token is ever configured it must be a read-only fine-grained PAT with no repo-write scopes).
- **@playwright/mcp 0.0.80** (wraps Playwright 1.63.0-alpha-2026-08-31): INSTALLED (npx cache, ephemeral) → VERIFIED (D3) — **lifecycle decision: KEEP IN RESERVE**, not promoted; fallback only (D3: fallback condition not met — Scrapling covered 3/3 JS-dependent targets; no target required interaction beyond rendering). Revisit trigger: a concrete Scrapling extraction/interaction failure or a board requiring true pagination/filtering. If ever promoted: pin output paths absolutely (screenshot cwd leak, D3 §3.3) and scope toolset to navigation/snapshot only.
- **Firecrawl**: NOT INSTALLED in the runtime stack — **KEEP IN RESERVE** (owner decision 2026-09-13; revisit only on a concrete extraction limitation).
- **Hunter.io, Apollo MCP, Crunchbase, OpenOutreach, Brave Search MCP**: **IGNORE** (owner decisions 2026-09-13). OpenOutreach IGNORE independently re-confirmed 2026-09-15 by implementation-level comparison test vs Scrapling: verified NO arbitrary-website scraping (discovery = BetterContact licensed DB API; no scraping library in `openoutfind` source); live `find` blocked on external account/credits; adds no capability over Scrapling+agent. Evidence: `02_AI_STACK/TOOL_EVALUATIONS/OPENOUTREACH_VS_SCRAPLING_TEST_2026-09-15.md`.
- **Scrapling B2B benchmark (2026-09-15)**: extraction-layer role confirmed for B2B lead finding — 26 domains discovered via Bing HTML (plain Fetcher), 11/12 company-site extractions with careers/contact follow-up and email capture, JSONL agent-consumable output; DDG HTML 202 anti-bot and JS-only shells are documented failure modes. Discovery alone is noisy — agent/LLM qualification layer remains required.

## External repository evaluations — 2026-10-03

| Repository | Disposition | Intended role | Boundary |
|---|---|---|---|
| **HarnessMD/munder-difflin** | TEST FIRST | external local multi-agent execution/UI harness | PAIOS remains canonical policy, state and authority |
| **paperclipai/paperclip** | KEEP IN RESERVE | future agent-team/control-plane integration | must not become a second canonical control plane |
| **tahodev/openmuse** | KEEP IN RESERVE | security/threat-model reference | exact-action approval model differs from PAIOS delegated autonomy |
| **CopilotKit/OpenDots** | KEEP IN RESERVE | future agent-workspace/product surface | heavy CopilotKit/AG-UI/Intelligence/OpenBot edge stack |
| **diggerhq/opendots** | KEEP IN RESERVE | personal-agent UX reference | OpenComputer dependency; not current runtime-parity solution |

Full evidence: `02_AI_STACK/TOOL_EVALUATIONS/EXTERNAL_REPOSITORIES_2026-10-03.md`.
No candidate was installed, authenticated or runtime-verified during this evaluation.

### Memory repository evaluations — 2026-10-03

| Repository | Disposition | Intended role | Boundary |
|---|---|---|---|
| **kkonstvol-lab/obsidian-memory** | KEEP IN RESERVE | human-readable Obsidian/Markdown memory and source-backed wiki reference | PAIOS remains the sole canonical source of truth; use only as a sidecar/view or after a concrete knowledge-workspace gap |
| **rohitg00/agentmemory** | RESERVE — WAIT FOR UPSTREAM FIX | external persistent-memory capability provider behind a PAIOS adapter | runtime memory remains non-canonical; PAIOS authority, policy and durable project state remain authoritative. Bounded evaluation 2026-10-03 — PROMISING. Isolated-scope follow-up 2026-10-04 — PARTIAL: per-call agentId isolation correct; NOT a security boundary; `AGENTMEMORY_AGENT_SCOPE=isolated` silently degrades without server `AGENT_ID`; pre-durability capture loss on abrupt kill. Wrapper prototype 2026-10-04 — PARTIAL: fail-closed wrapper contract passed 14/15; WR-09 upstream defect silently drops one agent's acknowledged writes from the search index under multi-agent concurrent capture. CaptureSerializer mitigation experiment 2026-10-04 (`AIOS_AGENTMEMORY_CAPTURE_SERIALIZER_EVIDENCE_2026-10-04.md`) — **FAIL, decision NOT VIABLE**: mitigation passed burst-then-switch workloads (A 3/3, B 3/3, restart clean) but failed deterministically 2/2 under interleaved per-write switching even with per-switch quiesce; unmitigated control did not reproduce (defect stochastic); ~3.9 s per agent switch (~30× throughput penalty); abrupt stop ≤1 s after ack loses acknowledged writes at storage level. Zero cross-agent leakage in every run to date. Requires upstream fix of concurrent multi-agent index loss (and durability window) before any re-evaluation. NOT INSTALLED into PAIOS, NOT VERIFIED for PAIOS use |
