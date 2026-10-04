# AIOS AGENTMEMORY CAPTURE SERIALIZER — FINAL MITIGATION + SOAK EVIDENCE (2026-10-04)

Status: EVALUATION EVIDENCE — bounded disposable experiment, NOT an
integration record, NOT a production implementation claim.
Predecessor records (preserved, not modified):
`AIOS_AGENTMEMORY_EVAL_EVIDENCE_2026-10-03.md`,
`AIOS_AGENTMEMORY_ISOLATED_SCOPE_EVIDENCE_2026-10-04.md`,
`AIOS_AGENTMEMORY_WRAPPER_PROTOTYPE_EVIDENCE_2026-10-04.md` (source of the
WR-09 blocker this experiment targets).
This is the final agentmemory experiment for 2026-10-04 per owner directive.

## 1. Environment

| Item | Value |
|---|---|
| Repository under test | rohitg00/agentmemory, source clone at upstream commit **2a00e7b** (unchanged; no upstream code modified) |
| iii-engine | v0.22.1 native (pinned `iii.exe`, `%USERPROFILE%\.agentmemory\bin`) |
| OS / runtime | Windows 10.0.26200 x64, Git Bash host, Python 3.14.0 (stdlib only), Node daemon `node dist/cli.mjs --instance 1 --data-dir <fresh dir>` |
| Server mode | instance 1 (REST 3211), `AGENT_ID=paios-primary`, `AGENTMEMORY_AGENT_SCOPE=isolated`, `AGENTMEMORY_INJECT_CONTEXT` removed from env |
| Data dirs | `_eval_tmp\am_data_wrap` — fresh-wiped per run (except Test C restart and Test E restart, which reuse the prior dir deliberately) |
| Prototype | `_eval_tmp\am_wrapper\capture_serializer_test.py` (disposable, outside the PAIOS tree) |
| Auth | host-generated bearer secret at `%USERPROFILE%\.agentmemory\secret`; never committed |
| Test data | synthetic only: 64 distinct subject+predicate sentences (no near-duplicates — near-identical contents collapse into supersede chains, finding U6), run prefix `serializer-eval-2026-10-04` |

## 2. Exact serializer behavior

`CaptureSerializer`: (1) one global write lock — a single `/remember` in
flight at a time; (2) tracks the last writing agentId and the completion
time of its last write; (3) when the next write comes from a DIFFERENT
agent and less than QUIESCE=4.0 s has elapsed since that completion, it
sleeps the remainder BEFORE issuing the write; (4) same-agent writes incur
zero added delay; (5) every quiesce and every write is timed.

## 3. Test A — serialized burst with quiesce (3 runs, fresh dirs)

alpha → 10 unique writes → ≥4 s quiesce → beta → 10 unique writes → ≥4 s.

| Run | Stored | Searchable | Wrong-owner rows | Duplicate ids | Version corruption | Wall |
|---|---|---|---|---|---|---|
| 1 | 10+10 | 10+10 | 0 | none | none (all v1, isLatest) | 4.5 s |
| 2 | 10+10 | 10+10 | 0 | none | none | 4.6 s |
| 3 | 10+10 | 10+10 | 0 | none | none | 4.6 s |

**Test A: PASS 3/3** (20/20 stored and searchable, correct agentId on every
record and every ack, alpha saw only alpha, beta only beta, zero leakage).

## 4. Test B — alternating-burst soak (3 runs, fresh dirs, verify per phase)

4 phases per run: alpha×5 → quiesce → beta×5 → quiesce → alpha×5 → quiesce
→ beta×5. Each agent 20 records total; storage (`/verify` per id),
searchable count, ownership and isolation checked after every phase.

| Run | Phases (stored/searchable/wrong-owner) | Final | Wall |
|---|---|---|---|
| 1 | 5/5/0, 10/0+0/0, 15/5+0/0, 20/5+5/0 | 20 stored, alpha 10/10, beta 10/10, 0 wrong-owner | 13.4 s |
| 2 | identical pattern | 20 stored, 10+10, 0 wrong-owner | 13.4 s |
| 3 | identical pattern | 20 stored, 10+10, 0 wrong-owner | 13.3 s |

**Test B: PASS 3/3** at final state, zero cross-agent leakage throughout.

OBSERVATION (transient mid-run recall): after each phase only that phase's
fresh burst was reliably searchable; the PREVIOUS phase's rows were
transiently unsearchable (e.g. after phase 2 both agents' first bursts read
0) and reappeared by the final check in all 3 runs. Under active multi-agent
capture, recall is temporarily incomplete even when the mitigated final
state is complete. A PAIOS consumer must not assume read-your-writes across
agent switches during capture.

## 5. Test C — restart after mitigated capture

Same data directory as Test B run 3, clean stop (taskkill /F of the daemon
tree), restart without recreating any memory:

- alpha searchable 10/10, beta searchable 10/10, total 20/20
- isolation intact (0 wrong-owner rows)

**Test C: PASS** — no searchable records lost after restart.

## 6. Test D — no-quiesce control (one run)

Identical burst pattern (alpha×10 then beta×10, immediate switch, no
serializer): **both agents 10/10 stored and searchable.** The defect did
NOT reproduce in this control run.

## 7. Test E — durability boundary (one bounded abrupt-stop)

6 writes acknowledged in 0.01–0.04 s each; daemon terminated 1.0 s after
the last ack; restart on the same dir:

- stored after restart: **0/6** (`/verify` finds none)
- searchable after restart: **0/6**

The 201 acknowledgement is purely in-memory at +1 s — the record is not
even at storage level, let alone searchable. Consistent with the earlier
wrapper-stage observation (5 s settle → survived). **Confirmed: the
durability window for `/remember`-acknowledged writes exceeds 1 s; an
abrupt stop inside it loses acknowledged writes entirely.** Not "fixed" in
this experiment per directive.

## 8. Test F — serialization limitation (2 runs)

Interleaved threaded callers through the serializer (2 threads, 10 writes
each, alternating alpha/beta per write; global lock held; per-switch
quiesce honored — every switch actually slept ~3.9 s):

| Run | Wall | alpha searchable | beta searchable | Wrong-owner |
|---|---|---|---|---|
| 1 | 76.6 s | **0/10** | 10/10 | 0 |
| 2 (repeat) | 76.6 s | **0/10** | 10/10 | 0 |

**Deterministic failure (2/2): under tightly alternating per-write agent
switching, the serializer with per-switch quiesce does NOT prevent total
searchable-memory loss for one agent.** All writes acked 201 with correct
agentIds; no leakage (alpha never saw beta's rows and vice versa); the
store-level check was not reached in the failing pattern, but the loss
matches the established index-loss signature (ack + store survive, search
loses one agent).

## 9. Test F overhead measurements (operational cost)

Across 140 serializer-mediated writes (Tests A, B, F run 1):

- 31 writes incurred a switch quiesce; total added delay 121.7 s; average
  quiesce actually slept 3.93 s per switch.
- Average write latency 0.028 s (max 0.068 s) — the REST call itself is
  negligible; the quiesce dominates.
- Effective throughput under the mitigated alternating pattern:
  ~66.8 writes/min (vs ~2100+ writes/min burst rate unmitigated) — a
  ~30× throughput penalty on agent switching.
- The mechanism requires GLOBAL serialization at minimum; per-agent-switch
  serialization with quiesce proved INSUFFICIENT (Test F).

## 10. Reproducibility count

- Test A: 3/3 PASS (fresh dirs). Test B: 3/3 PASS (fresh dirs).
  Test C: 1/1 PASS. Test D (control): 1 run, defect did NOT reproduce.
  Test E: 1 run, confirmed durability window. Test F: 2/2 FAIL (identical).
- Across all of 2026-10-04's multi-agent capture experiments (wrapper stage
  + this stage), the index-loss defect appeared in 4 of 11 multi-agent
  close-write scenarios — it is stochastic and pattern-sensitive: it did
  NOT reproduce in the unmitigated control, yet DID reproduce
  deterministically under the mitigated tightly-alternating pattern.

## 11. Classification

- FACT (live-observed, reproducible): all Test A/B/C/E/F result tables;
  the 201-ack-not-durable-at-1s boundary; the per-switch quiesce actually
  sleeping ~3.9 s; Test F's deterministic loss 2/2; zero cross-agent
  leakage in every run of the entire evaluation to date.
- OBSERVATION: transient mid-run recall incompleteness in Test B;
  Test D's non-reproduction (single run per directive).
- INFERENCE: the defect's trigger is engine-internal index state
  (agent-switch and/or burst structure and timing), not simply "elapsed
  time between agents" — the quiesce reduces but does not remove the risk,
  and cannot be relied on as a causal control (D passed without it; F
  failed with it).
- UNKNOWN: the precise engine-internal flush/replacement mechanism behind
  the index loss; behavior under Docker deployment; MCP-surface behavior.

## 12. FINAL DECISION: B — NOT VIABLE

Acceptance criteria check:
1. Test A 3/3 — MET.
2. Test B 3/3 — MET.
3. Test C — MET.
4. Isolation intact — MET (zero leakage in every run of the whole evaluation).
5. **No acknowledged write permanently unsearchable under the mitigated
   workload — NOT MET** (Test F: 2/2 deterministic total loss of one
   agent's mitigated writes).
6. Operational delay measured — MET (~3.9 s per agent switch, ~30×
   throughput penalty, global serialization required yet insufficient).
7. Control and limitations documented honestly — MET (this record).

Criterion 5 fails, therefore RESULT = FAIL and the decision is
**B. NOT VIABLE**: the CaptureSerializer mitigation does not reliably
prevent searchable-memory loss. It works for burst-then-switch workloads
(A 3/3, B 3/3) but fails deterministically under interleaved per-write
switching, and the no-quiesce control passing shows the quiesce is not a
reliable causal control.

## 13. PAIOS disposition and recommendation

- agentmemory disposition changes from **TEST FIRST** to
  **RESERVE — WAIT FOR UPSTREAM FIX** (per owner directive: mitigation
  failed → no additional workarounds to be built).
- Do NOT integrate agentmemory into PAIOS. The blocker is no longer only
  isolation design (cooperative scoping) but an unreliability defect in
  multi-agent recall completeness that client-side mitigation cannot
  reliably close.
- If upstream later ships a fix for the concurrent multi-agent index loss
  (and the abrupt-stop durability window), a fresh bounded evaluation
  could re-open the TEST FIRST path. Nothing further to be built on the
  PAIOS side for now.
- PAIOS runtime-memory continuity remains served by the canonical
  file-backed memory/context engine (Phase 8, `13_AUTOMATION/memory_engine`).

## 14. Hygiene

- All agentmemory daemons stopped at closeout; ports 3211/3311/3411 free.
- All runtime state and test data remain outside the canonical PAIOS tree
  (`C:\Users\ABhas\projects\_eval_tmp\`).
- No real secrets or personal data anywhere in this record or the logs;
  all markers/tokens synthetic.
- PAIOS tree changes limited to: this file,
  `02_AI_STACK/AI_TOOL_REGISTRY.md`, `07_VERSION_TRACKING/DECISION_HISTORY.md`.
- Canonical experiment log: `_eval_tmp/am_wrapper/serializer_run.log`.
