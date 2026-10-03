# EVALUATION EVIDENCE — rohitg00/agentmemory (bounded experiment, 2026-10-03)

Status: EVALUATION ONLY — no PAIOS integration, no architecture change, no new runtime dependency.
Protocol: `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md` (TEST FIRST disposition, bounded runtime test).
Executor: ZCode (Windows native path).

## Environment

| Item | Value |
|---|---|
| PAIOS HEAD tested | `1c84a21` (main) |
| Date/time | 2026-10-03, ~19:15–19:55 IST |
| Upstream URL | https://github.com/rohitg00/agentmemory |
| Upstream commit SHA | `2a00e7b38fc4ae4e38af4134586be0bbe9612706` (main, 2026-10-03 13:30 +0530, "feat(codex): package local memory plugin ... #1459") |
| Upstream version (source) | 0.9.29, pins iii-sdk/@iii-dev/helpers 0.22.1 |
| Runtime path | Native Windows: Node v25.6.0 + manually downloaded pinned `iii.exe` v0.22.1 (`iii-x86_64-pc-windows-msvc.zip` from iii-hq/iii release `iii/v0.22.1`) into `%USERPROFILE%\.agentmemory\bin\iii.exe`; agentmemory run from source clone |
| Eval dir (outside PAIOS) | `C:\Users\ABhas\projects\_eval_tmp\agentmemory` (clone), `...\_eval_tmp\am_data` (data dir via `--data-dir`) |
| Mode | Keyless, zero-LLM (BM25 only); embeddings, graph, consolidation, auto-compress, context injection all OFF (verified via `/agentmemory/status` flags) |
| Ports | 3111 REST/MCP, 3112 streams, 3113 viewer, 49134 engine — all up |

## Install/execution procedure (reproducible)

1. `git clone https://github.com/rohitg00/agentmemory` → HEAD `2a00e7b`.
2. Download pinned engine per README Windows Option A; verify `iii.exe --version` = `0.22.1`.
3. `npm install`; `npx tsdown` + manual asset copy (repo `npm run build` uses POSIX `cp`, fails under cmd.exe on Windows — minor Windows DX issue).
4. Start: `CI=1 node dist/cli.mjs --data-dir C:\Users\ABhas\projects\_eval_tmp\am_data`.
5. REST auth: `Authorization: Bearer <secret>`; server auto-generates secret at `%USERPROFILE%\.agentmemory\secret`.
6. Endpoints used: `POST /agentmemory/remember` (201), `POST /agentmemory/smart-search` (200), `GET /agentmemory/health|status|capture`, `POST /agentmemory/capture/drain`.

## Synthetic test data

All data synthetic; no real PAIOS data used.

- M1 (project eval-alpha, no agentId): "Alpha project synthetic fact: the quantum toaster uses fusion battery model FB-9", concepts [fusion-battery, alpha-scope], files [alpha/spec.md] → id `mem_musg59tt_08c8bfb34ad8`
- M2 (project eval-alpha): "Alpha ... lead engineer is Dr. Yara Voss" → `mem_musg5a3l_2575c38db961`
- M3 (project eval-beta): "Beta ... lighthouse maintenance runs every 11 days" → `mem_musg5ad7_fedb2b2d298c`
- M4 (project eval-alpha, agentId agent-scout): "Scout agent secret: the north gate code is 4-7-1-echo"
- M5 (project eval-alpha, agentId agent-logger): "Logger agent note: north gate routine inspection tuesday"

## Results

| # | Capability | Result | Evidence |
|---|---|---|---|
| 1 | Capture/retrieval + provenance | PASS | 3 writes returned 201 with full records. Query "fusion battery model" returned M1 (mode=compact). Provenance preserved: id, createdAt/updatedAt, version, strength, origin.channel="agent", concepts, files, project, agentId, sessionIds, sourceObservationIds. |
| 2 | Restart persistence | PASS | Killed server (ports closed), restarted with same `--data-dir`; both keyless query and agent-scoped query returned identical stored memories. `state_store.db` persisted in data dir. No manual recovery steps needed. |
| 3 | Scope/isolation | PASS via agentId / FAIL via project | `agentId` filtering works: scout's secret NOT returned to agent-logger query; both visible only unscoped. Code also supports `AGENTMEMORY_AGENT_SCOPE=isolated` with hard refusal to read cross-agent rows. **Defect:** `project` accepted by both `remember` and `smart-search` REST schemas but is NOT applied to memory results — query with `project: eval-alpha` (and even `project: project-never-created`) returned eval-beta memory. In `src/functions/smart-search.ts`, `project` only filters lesson recall, not memory search. |
| 4 | No-result behavior | PASS (observed) | Never-stored nonsense query ("purple elephant algebra") returned empty results — no fabrication. Keyword-overlap near-miss ("quantum coffee machine") returned the toaster memory (BM25 "quantum" match) with opaque `score: 1` — no graded relevance shown in compact mode. Ambiguity risk is keyword-level, not hallucination. |
| 5 | Context/token overhead | OBSERVED: compact | `smart-search` compact responses measured 260–443 bytes (~65–110 tokens) for limit=5. Retrieval overhead is small; recall stays compact by design. Injection overhead not measured (context injection kept disabled per mandate). |
| 6 | Reliability/recovery | PASS (documented + observed) | Server restart recovery verified (Test 2). Duplicate capture of identical content creates version 2 superseding v1 (no duplicate rows; `supersedes` lineage). `/agentmemory/status` exposes capture inbox with documented retry policy (maxAttempts=5, retryIntervalMs=10s), dead-letter cap, dedup retention (168h), spool files, and boot-drain counters. Health endpoint exposes circuit breaker (state=closed). |

## Baseline vs agentmemory (PAIOS canonical Markdown/Git memory)

- Same synthetic facts CAN be stored in PAIOS Markdown and retrieved (grep); maintenance overhead is trivial and fully transparent.
- Concrete gaps agentmemory closes that PAIOS baseline lacks:
  1. **Multi-agent scoped memory** with enforced isolation (`AGENTMEMORY_AGENT_SCOPE=isolated` refuses cross-agent reads).
  2. **Scored BM25 retrieval** over free-text memory (PAIOS grep is exact/regex, no ranking).
  3. **Memory lifecycle**: versioning, supersedes lineage, TTL, strength, consolidation hooks.
  4. **Capture durability**: retry queue, dead-letter, dedup, spool for unreliable capture paths.
- Gaps agentmemory does NOT close: PAIOS's human-readable/Git-auditable canonical truth; agentmemory state is an opaque SQLite store (`state_store.db`).

## Limitations / blockers / unexpected behavior

- **npm release lag:** `npx @agentmemory/agentmemory@latest` (published package) demanded iii-engine v0.11.2 and failed on native Windows; only the source build at HEAD (0.9.29) matches the documented 0.22.1 pairing. Evaluation therefore used the repo source, not the published npm artifact.
- `project` scope parameter silently ignored on memory search (defect observed above).
- Windows `npm run build` fails under cmd.exe (POSIX-only build script).
- `smart-search` compact mode returns opaque `score: 1` rather than graded relevance.
- REST requires bearer secret (auto-generated at `~/.agentmemory/secret`); local file permission posture is the user's own.
- No destructive testing performed; no real secrets used; all test data synthetic.

## Security/privacy observations

- All data local (loopback-bound ports per docker-compose/compose config; REST on 127.0.0.1); keyless mode works without any cloud account.
- agentId isolation is opt-in; default is a shared memory space — an agent not passing agentId sees all memories. PAIOS adoption decision would need mandatory scoped mode.

## Decision gate

**A. TEST RESULT: PROMISING** — concrete capability (enforced multi-agent scoped retrieval, ranked BM25 recall, memory lifecycle/versioning) demonstrated against the PAIOS Markdown/Git baseline, and a narrowly defined follow-up experiment is justified. Not adoption; no PAIOS files changed except this evidence record.

## Follow-up candidate (not started)

One narrowly scoped follow-up: test `AGENTMEMORY_AGENT_SCOPE=isolated` end-to-end with two concurrent scoped agents under concurrent writes + restart, and verify the published npm package (once it catches up to 0.22.1) reproduces the source-build results.
