# AIOS AGENTMEMORY WRAPPER PROTOTYPE — EVIDENCE RECORD (2026-10-04)

Status: EVALUATION EVIDENCE — NOT an integration record. agentmemory is NOT
installed into PAIOS and remains non-canonical runtime memory.
Predecessor records: `AIOS_AGENTMEMORY_EVAL_EVIDENCE_2026-10-03.md`,
`AIOS_AGENTMEMORY_ISOLATED_SCOPE_EVIDENCE_2026-10-04.md` (preserved, not modified).
Objective: build and test the smallest disposable prototype demonstrating how
PAIOS could safely consume agentmemory despite its cooperative-scope
limitations — the "smallest next experiment" defined by the 2026-10-04 record.

## 1. Test environment

| Item | Value |
|---|---|
| Repository under test | rohitg00/agentmemory (source clone, upstream commit 2a00e7b, v0.9.29) |
| Prototype location | `C:\Users\ABhas\projects\_eval_tmp\am_wrapper\` — OUTSIDE the canonical PAIOS tree |
| Wrapper | `paios_memory_wrapper.py` (sha256 5d1cdd01ceaf96ac8cdf7e3b6cbfc6f5a8b65b760e65b770df8980f00eb2de6e) |
| Test suite | `test_wrapper.py` (sha256 ebbc37fb02b32f33ee7457f7f64b64acaab0a9e82bdce7afd67d91493354fe14), stdlib unittest |
| Server instances | native iii.exe v0.22.1 via `node dist/cli.mjs --instance N --data-dir <dir>`; instance 1 = main (isolated, `AGENT_ID=paios-primary`), instance 2 = misconfigured (WR-06), instance 3 = persistence (WR-08) |
| Data dirs | `_eval_tmp\am_data_wrap{,_shared,_persist}` — fresh-wiped per suite run |
| Auth | host bearer secret at `%USERPROFILE%\.agentmemory\secret` (host-generated; not committed anywhere) |
| Test data | synthetic only; markers `WRxx/AMxx wrap-eval-2026-10-04 …`; synthetic secrets `SYNTH_TOKEN_DEADB33F4242`, `SYNTH_TOKEN_CAFEBAD9876`; injection text with `SYNTH_INJECT_PAYLOAD_77`; no real credentials or personal data |
| Injection | `AGENTMEMORY_INJECT_CONTEXT` explicitly removed from server env; asserted OFF at runtime (AM-13) |
| Canonical run | `test_run_9_final.log` — 15 tests, 14 PASS, 1 FAIL (WR-09) in 105.9 s |

## 2. Wrapper design (protection requirements → mechanism)

| Requirement | Mechanism |
|---|---|
| R1. Every read carries explicit agentId | Single outbound choke point `_post_scoped()` injects the pinned agentId into every data-path body and re-asserts it on the serialized payload before network I/O |
| R2. Reject missing/null/empty agentId | `validate_agent_id()` — rejects None, non-strings, empty/whitespace before any I/O; constructor cannot exist without an id |
| R3. Reject wildcard/broad selectors | Allowlist charset `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$` (excludes `*`, whitespace) + reserved-word denylist (`*`, `all`, `any`, `root`, `admin`) |
| R4. project is not a boundary | `project` accepted for metadata on writes only; NO project-based read selector exists in the wrapper API (`search_by_project_is_forbidden()`) |
| R5. Startup verifies actual enforcement | `verify_isolation()` behavioral gate: V1 health; V2 bearer auth actually enforced (unauthenticated probe must get 401/403); V3 foreign-agent canary must be invisible to an unscoped diagnostic read AND to the pinned agent; V4 own-scoped write/read round trip |
| R6. Fail closed | Any V1–V4 failure raises `IsolationVerificationError`; server unreachable → error, never cached/fallback data; any server row owned by another agent (or ownerless) raises instead of passing through; retrieval rows normalized and flagged `untrusted: True` |
| R7. Data outside PAIOS | All runtime state under `_eval_tmp\`; nothing added to the PAIOS tree except this evidence + registry/decision entries |
| R8. No auto context injection | Wrapper performs no injection; server env explicitly excludes `AGENTMEMORY_INJECT_CONTEXT` (asserted in AM-13) |
| R9. PAIOS canonical | Wrapper docstring + returned rows marked untrusted; memory never treated as policy/truth/authority/durable state |

Retrieval endpoint choice (FACT): the wrapper uses `POST /agentmemory/search`
(BM25) because it returns full observation rows including `agentId`.
`smart-search` compact mode returns titles/ids only (no content, no agentId),
and its `expandIds` path cannot resolve `mem_*` memories at all — expand
requests return `results: []` even unscoped with the correct `sessionId`
(observed live; upstream gap). `/context` requires additional params and is
not needed by the thin wrapper.

## 3. WR test results (wrapper safety contract)

| # | Test | Result | Evidence (observed behavior) |
|---|---|---|---|
| WR-01 | Own-agent read works | PASS | alpha wrote `WR01 …` (201, response `memory.agentId=paios-alpha`); scoped search returned it; every row flagged untrusted |
| WR-02 | Missing agentId rejected | PASS | None / `""` / `"   "` / 42 / list all raise `WrapperPolicyError` before I/O; wrapper with null id cannot be constructed |
| WR-03 | Wildcard agentId rejected | PASS | `*`, `**`, `" *"`, `all`, `any`, `root`, `a*b`, `"agent *"` all rejected by the allowlist/denylist |
| WR-04 | Cross-agent read rejected | PASS | beta searched alpha's unique marker → 0 rows; simulated rogue server returning a foreign row → wrapper raises `WrapperPolicyError` (defense-in-depth) |
| WR-05 | Project-only query rejected | PASS | same project string, different agent → 0 rows; no project-read API exists |
| WR-06 | Startup fails on misconfigured isolation | PASS | Case A (shared mode, no env): V3 caught the foreign canary in an unscoped read → `IsolationVerificationError("V3 ISOLATION NOT ENFORCED…")`. Case B (`AGENTMEMORY_AGENT_SCOPE=isolated` but no `AGENT_ID`): silently degraded to shared (re-confirms finding F2) → also caught. Correctly-configured server passes and serves |
| WR-07 | Valid scoped write/read passes | PASS | full verify-on-init + write/search round trip with project metadata |
| WR-08 | Restart preserves scoped behavior | PASS (with settle time) | dedicated instance: marker written, 5 s settle, hard kill, restart → own marker retrievable, foreign agent still excluded. Without the settle delay the acknowledged write was lost (finding U5) |
| WR-09 | Concurrent scoped access remains isolated | **FAIL** | Isolation held on every probe (zero cross-agent rows under concurrency, 2 runs + 4 targeted reproductions). Recall completeness did NOT: with two agents writing interleaved bursts, ALL of one agent's acknowledged writes became unsearchable — permanently (finding U1). This is an upstream defect, not a wrapper leak |
| WR-10 | Never forwards unsafe unscoped request | PASS | logging reverse proxy captured every outbound body: exactly one unscoped request exists (the V3 startup diagnostic, canary-marked); every data-path body carried the pinned agentId; zero wildcard bodies; zero foreign-agent bodies |

## 4. AM test results (memory capability through the wrapper)

| # | Test | Result | Evidence |
|---|---|---|---|
| AM-11 | Relevance | PASS | 4 distinct-topic memories; paraphrased queries ("why did the CI pipeline break disk", "tomato frost plants") returned the correct memories as top hits |
| AM-12 | No-result / near-miss | PASS with relevance finding | Never-written tokens (`QUANTUM_FLUMPTION_8817 zephyrboondoggle`) → `[]`, no fabrication. Near-miss query ("bathroom shower leak plumber burst pipe") returned 1 row: an unrelated own-agent AM-11 memory (relevance looseness; query expansion suspected). Wrapper guarantees held: only real, own-agent, untrusted-flagged rows |
| AM-13 | Memory prompt-injection | PASS | Attacker-scoped memory containing "IGNORE ALL PREVIOUS INSTRUCTIONS … SYNTH_INJECT_PAYLOAD_77" unreachable by victim (0 rows on attacker-only tokens). Victim's own memory containing instruction-like text returns as DATA flagged untrusted. Global auto-injection asserted OFF |
| AM-14 | Secret redaction / data boundary | PASS | Upstream stores captures verbatim (raw `SYNTH_TOKEN_DEADB33F4242` retrievable in full — no server-side redaction). Wrapper capture-time redactor kept `SYNTH_TOKEN_CAFEBAD9876` out of the store entirely (`SYNTH_TOKEN_[REDACTED]` stored instead) |
| AM-15 | Failure / recovery | PASS | (a) server down → constructor and `verify_isolation()` raise (fail closed, nothing served); (b) hard kill with recent write → wrapper re-verified cleanly this run (`RECOVERY_REPORT: clean re-verify`) and pre-kill memory survived (5 s settle); (c) fresh-store rebuild restored full function |

## 5. Upstream findings (new, this stage)

- **U1 (FACT — WR-09 FAIL root cause): silent permanent search-index loss under
  multi-agent concurrent capture.** Two agents writing interleaved bursts of 10
  `/remember` calls: ALL 20 calls acknowledged 201 with correct `agentId` in
  responses; `verify` endpoint finds all 20 records in the store; the search
  index contains ONLY one agent's 10 rows. Reproduced 2/2 interleaved runs
  (loser varied: alpha once, beta once) and 1/1 locked-sequential
  burst-then-burst run. The loss persists across restart (the persisted index
  is reloaded, not rebuilt from the store). No cross-agent leakage ever
  occurred — rows are lost, never mis-attributed.
- **U2 (FACT): single-agent concurrency is safe.** Two wrappers on the SAME
  agent writing a 20-item concurrent burst → 20/20 searchable. The trigger is
  agent-switch during an unflushed index buffer, not concurrency per se.
- **U3 (FACT): quiesce mitigation verified.** With a ≥4 s settle between
  agent bursts, both agents' bursts were 10/10 + 10/10 searchable, and a
  subsequent immediate burst did not drop the settled agent. A PAIOS adapter
  would need serialized capture with a per-agent-switch quiesce (or an
  upstream fix); plain serialization without quiesce did NOT help.
- **U4 (FACT): hard kill can permanently break the write path.** `taskkill /F`
  on an instance with accumulated writes → subsequent `/remember` calls return
  HTTP 500 `invocation_failed: Cannot read properties of undefined (reading
  'isLatest')` for agents whose dedup candidates hit stale index entries;
  persists across restart; fresh agentIds unaffected; only a fresh data dir
  reliably recovers. Search stays 200 (read path intact).
- **U5 (FACT): acknowledged writes need settle time before a hard kill.**
  A `/remember` acknowledged 201 and killed 0 s later was lost (WR-08 run 4);
  the same write killed after 5 s survived. Consistent with the ~3.5 s
  durability window previously measured for `/observe` — it extends to
  `/remember`-acknowledged writes becoming searchable/durable.
- **U6 (FACT): near-identical contents collapse into a supersede chain.**
  Digit-only-different items (`item 0`…`item 9`) dedup to one version chain;
  only the latest version stays searchable (consistent with T8 of the
  2026-10-04 record). Test data must be genuinely distinct sentences.
- **U7 (FACT): `expandIds` cannot resolve `mem_*` memories** (returns
  `results: []` even unscoped with correct `sessionId`), and smart-search
  compact rows carry no content/agentId — so `/search` is the only usable
  full-row retrieval surface for a scoped consumer.
- **U8 (FACT): only one daemon per lifecycle state.** A second
  `--port`-based daemon is refused while one runs ("The canonical lifecycle
  state is owned by a live agentmemory engine…"); `--instance N` is required
  for concurrent isolated daemons (ports 3111+N*100).
- **U9 (OBSERVATION): relevance looseness.** A near-miss query returned a
  topically unrelated own-agent memory (AM-12). Query expansion suspected
  (`src/functions/query-expansion.ts` exists) but mechanism not verified.

## 6. Classification

All results above are FACT (live-observed, reproducible within this stage)
except U9 (OBSERVATION — mechanism unverified) and the following UNKNOWNs:
exact internal trigger/flush timing of the index buffer (U1/U3), MCP-surface
behavior (untested — no MCP client wired, unchanged from prior record), and
behavior under Docker deployment (not exercised).

## 7. Decision: PARTIAL

The wrapper prototype achieved its purpose: it demonstrates a complete,
verified fail-closed consumption contract (WR-01–08, WR-10 PASS; AM-11–15
PASS) around agentmemory's cooperative isolation. What blocks PASS FOR NEXT
STAGE is U1: agentmemory can silently and permanently make one agent's
acknowledged memories unsearchable under multi-agent capture — precisely the
multi-runtime memory-continuity scenario PAIOS would use it for. Isolation
(secrecy) held everywhere; availability/completeness of recall did not.

Suitability for the next PAIOS integration stage: **conditionally suitable,
not yet qualified.** If the owner pursues integration, the wrapper must add:
(a) serialized capture with a per-agent-switch quiesce (verified mitigation,
U3) or a single-capture-writer per store; (b) post-capture recall
verification (write→read-back) before acknowledging durability; (c) the
startup isolation gate as built. Alternatively, wait for an upstream fix of
the index race. Do not integrate in the current state.

## 8. Smallest next experiment, if pursued

Extend the prototype with a `CaptureSerializer` (global write lock + ≥4 s
quiesce on agent switch + write→read-back confirmation) and re-run WR-01–10
plus a soak test of alternating agent bursts. No broader testing.

## 9. Provenance & hygiene

- Evidence recorded 2026-10-04 by ZCode; server source inspected at
  `src/functions/remember.ts` (dedup/supersede), `src/functions/smart-search.ts`
  (compact/expandIds), `src/functions/search.ts` (hybrid filter),
  `src/config.ts` (scope loader), `src/cli-data-dir.ts`/`src/cli.ts`
  (instance lifecycle).
- Canonical suite log: `_eval_tmp/am_wrapper/test_run_9_final.log`
  (outside PAIOS; summarized fully above).
- No real secrets appear in this record; all tokens/markers are synthetic.
- PAIOS canonical tree changes limited to: this file,
  `02_AI_STACK/AI_TOOL_REGISTRY.md`, `07_VERSION_TRACKING/DECISION_HISTORY.md`.
- agentmemory runtime/data remains in `C:\Users\ABhas\projects\_eval_tmp\`,
  outside the canonical repository.
