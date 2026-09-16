# AIOS PHASE 8 ZCODE PARITY VALIDATION — 2026-09-16

Executor: ZCode (independent validation pass; OpenCode NOT used for this validation).
Commit tested: `382f3fc` (`feat(paios): implement phase 8 memory and context engine`) — HEAD of `main`, synced to `origin/main` before validation.
Implementation evidence compared against: `12_VALIDATION/AIOS_PHASE8_IMPLEMENTATION_EVIDENCE_2026-09-16.md`.

## 1. Repository state at validation

- Branch: `main`; HEAD: `382f3fcf17a64427c371b0d613e7a3001f6605a0`; local == `origin/main` (verified after push in the prior session).
- Working tree: clean except two untracked empty files `13_AUTOMATION/memory_engine/oc_out.txt` / `oc_err.txt` (0 bytes, timestamped 2026-09-16 19:45, after the implementation session; consistent with an OpenCode probe) and untracked `.freebuff/project-id` (tool artifact). Neither committed.
- Python: 3.14.0 (Windows). Engine dependencies: standard library only (verified by inspection; pytest/PyYAML exist in the environment but are not imported by the engine).

## 2. Commands executed

- `python -m pytest 13_AUTOMATION/memory_engine/tests/test_phase8.py -q` → **17 passed in 0.82s**. Confirms the reported 17/17 under a different runner than the original unittest run.
- Independent adversarial/probe script (12 checks, temp directories only, imports the committed engine): 11/12 PASS; 1 genuine finding (§5).
- Cross-process persistence probe: memory written in one OS process, recovered by a **separate** process creating a fresh `MemoryStore` on the same state root → RECOVERED: True. (Stronger than the in-suite MC-02, which resets the store instance within one process.)

## 3. MC/CT results (independent re-verification)

| Test | Result | Independent verification |
| --- | --- | --- |
| MC-01 | PASS | Write/read-back with full provenance; empty content and `api_key = sk-...` rejected (see §5 for a heuristic bypass). |
| MC-02 | PASS | Proven across a real OS process boundary, not just a new in-process instance. |
| MC-03 | PASS | Engineering memory retrieved; irrelevant personal memory excluded by threshold + token scoring. |
| MC-04 | PASS | `PERSONAL` hard-filtered at `max_sensitivity=INTERNAL`; adversarial check also confirms `SENSITIVE` never leaks (A2). |
| MC-05 | PASS | `source.kind/ref` and timestamps survive write→load→retrieve. |
| MC-06 | PASS | STATED/INFERRED preserved; INFERRED stored with LOW confidence + AGENT source, never promoted. |
| MC-07 | PASS | Adversarial A1: contradictory memories both remain discoverable, cross-linked via `conflict_refs`, `CONFLICT-*.json` written. |
| MC-08 | PASS | Adversarial A3: newer CANONICAL_FILE record outranks stale one; old content preserved verbatim as `SUPERSEDED`. |
| MC-09 | PASS | Adversarial A4: invalidated record absent from retrieval, file retained on disk with `INVALIDATED` status. |
| CT-01 | PASS | All schema §2 keys present in produced package. |
| CT-02 | PASS | `NONE` mode: zero records, policy/mission retained. |
| CT-03 | PASS | Adversarial A5: `SELECTED` package contains exactly the selected memory; unrelated memory absent from the entire knowledge blob. |
| CT-04 | PASS | Adversarial A6: under `max_chars` pressure, filler records dropped first; policy, objective, acceptance criteria survive. Priority order confirmed. |
| CT-05 | PASS | Checkpoint persisted and reloaded with objective/completed/next-actions/repository state. |
| CT-06 | PASS | Fresh `CheckpointStore` reconstructs task state from disk alone. |
| CT-07 | PASS | Adversarial A7: `resume()` detects HEAD/working-tree drift, reports discrepancies, `safe_to_continue=False`, still identifies next action. |
| CT-08 | PASS | Checkpoint references context package; both reconstructable without conversation replay. |

## 4. Adversarial results

| Check | Result | Detail |
| --- | --- | --- |
| A1 conflict-preservation | PASS | Both contradictory DB-engine memories discoverable; cross-linked. |
| A2 sensitivity-leak | PASS | `SENSITIVE` record absent from `INTERNAL`-authorized retrieval. |
| A3 historical supersession | PASS | New authoritative record wins retrieval; history retained verbatim. |
| A4 invalidation | PASS | Invalidated memory absent from ordinary retrieval; audit record retained. |
| A5 context leakage | PASS | `SELECTED` child receives only selected memory; no unrelated memory anywhere in the knowledge section. |
| A6 budget pressure | PASS | Low-priority context discarded before objective/policy/acceptance criteria. |
| A7 state drift | PASS | Resume detects repository changes rather than blindly continuing. |
| L1 `max_tokens` | CONFIRMED LIMITATION | `budget.max_tokens` is always `null`; only `max_items`/`max_chars` implemented. As reported. |
| L2 no locking | CONFIRMED LIMITATION | No file-locking mechanism exists. As reported. |
| L3 no vector infra | CONFIRMED LIMITATION | No embedding/vector dependencies or code paths. As reported. |
| B1 architecture boundary | PASS | Docs/code make no claims of native semantic retrieval, native runtime memory, process snapshotting, or canonical authority; hierarchy `Canonical → Protocol → Engine → Adapter → Runtime` preserved. |
| S1 secret heuristic | **FINDING** | See §5. |

## 5. Discrepancies and findings

1. **Secret heuristic bypass (new finding, reproduced).** The write-time secret detector (`records.py:SECRET_PATTERNS`) misses credential names embedded with underscores, e.g. `aws_secret_access_key = wJalr...`, because `\b` word boundaries do not fire between `_` and alphanumerics. Reproduced: write succeeds where the implementation evidence implies rejection of secret-shaped content.
   - Classification: minor hygiene gap, not a data-loss or correctness defect. The detector is a best-effort heuristic, not a security boundary; OWNER-disciplined writes remain the primary control per `AIOS_MEMORY_ARCHITECTURE_V1.md` §4.
   - Disposition: preserved here as a finding; **not silently patched mid-validation and the implementation evidence was not rewritten**. Recommend a small follow-up fix (e.g. also match `(?i)[a-z0-9_]*(key|secret|token|password)[a-z0-9_]*\s*[:=]`).
2. **MC-02 evidence scope.** Implementation evidence proved persistence via a new in-process instance. This validation proves the stronger cross-process case. Not a contradiction; the original claim stands and is now extended.
3. **Stray files.** `oc_out.txt`/`oc_err.txt` (empty) appeared in the engine directory post-implementation. Not produced by this validation; left uncommitted and flagged for the owner.

## 6. Security / hygiene findings

- No secrets, credentials, or sensitive personal data in test fixtures or committed examples (inspected all fixture content).
- Secret-write heuristic has the underscore bypass described in §5.
- All test/adversarial state used temporary directories; canonical `11_STATE/memory/` was not written by this validation.

## 7. Limitations acknowledged (as reported, confirmed — not defects)

- Lexical (structured + token) retrieval only; no semantic retrieval until a `SemanticAdapter` is supplied.
- `max_tokens` budgeting unimplemented (`null`); only chars/items.
- No multi-process locking; concurrent writers could interleave `index.yaml` regeneration.
- Resume verification limited to branch/HEAD/working-tree; file-level content drift undetected.
- Logical checkpoint/restore only; no filesystem/process snapshot rollback.

## 8. Final classification

**PARITY PASS WITH GAPS**

All 17 MC/CT tests pass independently (pytest runner), all 7 adversarial scenarios pass, cross-process persistence proven, architecture boundaries intact. Gap: one minor secret-heuristic bypass (§5.1) plus the acknowledged limitations above, which match the implementation evidence.

Model/runtime note: ZCode validation session (model identity not exposed to the session; agent powered by GLM via ZCode, 2026-09-16).
