# AIOS PHASE 8 IMPLEMENTATION EVIDENCE — 2026-09-16

Executor: ZCode (primary implementation executor).
Scope: file-backed memory/context engine per the Phase 8 contracts.
Nature of this record: **implementation evidence only**. It does NOT verify
runtime capabilities in ZCode/OpenCode/Hermes sessions, and it does NOT claim
semantic/vector retrieval — retrieval is structured + lexical.

Implementation: `13_AUTOMATION/memory_engine/paios_memory/` (Python stdlib only)
Tests: `13_AUTOMATION/memory_engine/tests/test_phase8.py` — 17 tests, all in
temporary directories; canonical `11_STATE/memory/` untouched.
Run: `cd 13_AUTOMATION/memory_engine && python -m unittest tests.test_phase8 -v`
Result: **17/17 OK** (Python 3.14.0, Windows).

## Memory tests

| Test | Result | Evidence |
| --- | --- | --- |
| MC-01 | PASS | `test_MC01_explicit_memory_write` — write+read-back with provenance; empty content rejected (`ValueError`); secret-shaped content rejected. Path: `store.remember`. |
| MC-02 | PASS | `test_MC02_persistence_across_sessions` — record written, store object discarded, a **new** `MemoryStore` instance on the same root recovers the record from disk JSON. Proves persistence, not in-process caching. |
| MC-03 | PASS | `test_MC03_relevance_gating` — lexical query returns the engineering memory; personal coffee-order memory excluded. Threshold `min_relevance=3.0` + token-overlap scoring. |
| MC-04 | PASS | `test_MC04_sensitivity_gating` — `max_sensitivity=INTERNAL` hard-filters a `PERSONAL` record while a `PUBLIC` record passes. |
| MC-05 | PASS | `test_MC05_provenance_preservation` — `source.kind/ref` and created/updated timestamps survive write→load round-trip. |
| MC-06 | PASS | `test_MC06_stated_vs_inferred` — STATED vs INFERRED classification preserved; INFERRED record stored with LOW confidence and AGENT source, never promoted. |
| MC-07 | PASS | `test_MC07_conflict_preservation` — `update(conflict=True)` preserves old content/status=CONFLICTING, writes `CONFLICT-*.json`, cross-links `conflict_refs`; both records individually retrievable. |
| MC-08 | PASS | `test_MC08_current_state_precedence` — newer CANONICAL_FILE record outranks stale OWNER record (freshness + source-quality weighting); old record preserved as SUPERSEDED with content intact. |
| MC-09 | PASS | `test_MC09_invalidation` — invalidated record excluded from retrieval, remains on disk with status `INVALIDATED` (auditable transition, not deletion). |

## Context tests

| Test | Result | Evidence |
| --- | --- | --- |
| CT-01 | PASS | `test_CT01_context_package_construction` — package contains all schema §2 keys; persisted as `CTX-*.json`. |
| CT-02 | PASS | `test_CT02_minimal_context` — `inheritance_mode="NONE"` yields zero selected records while policy + mission remain present. |
| CT-03 | PASS | `test_CT03_selective_inheritance` — `SELECTED` mode package contains exactly the selected memory ID and nothing else. |
| CT-04 | PASS | `test_CT04_context_budgeting` — `max_items` truncates records; `max_chars` drops lowest-priority records first while mission/acceptance criteria/policy survive. Excluded IDs recorded in `inheritance.excluded_refs`. |
| CT-05 | PASS | `test_CT05_checkpoint_creation` — checkpoint persisted with objective, completed actions, next actions, repository state; reloaded from disk. |
| CT-06 | PASS | `test_CT06_checkpoint_reconstruction` — a fresh `CheckpointStore` instance reconstructs task state (task id, next actions) from disk alone. |
| CT-07 | PASS | `test_CT07_state_verification_on_resume` — `resume()` detects HEAD drift vs the checkpointed commit, reports discrepancies, and sets `safe_to_continue=False`; next action still identified. |
| CT-08 | PASS | `test_CT08_compaction_readiness` — checkpoint references a context package ID; checkpoint + stored package together reconstruct the task without conversation history. |

## Per-test detail (expected / observed / limitations)

- **MC-02**: expected — new store instance recovers memory; observed — exact. Limitation — single-process test; no multi-process file-locking. Concurrent writers could interleave `index.yaml` regeneration.
- **MC-03/MC-08**: expected — deterministic lexical ranking; observed — exact. Limitation — lexical matching is exact-token based; paraphrases without shared tokens will score low until a semantic adapter is added (extension point: `SemanticAdapter`).
- **MC-04**: expected — hard sensitivity ceiling; observed — exact. Limitation — no per-record redaction; filtering is all-or-nothing.
- **CT-04**: expected — protected material survives truncation; observed — exact. Limitation — `max_tokens` is defined in the schema but not implemented (only `max_chars`/`max_items`); no tokenizer dependency was justified.
- **CT-07**: expected — discrepancy reported, not blindly continued; observed — exact. Limitation — verification compares only branch/HEAD/working-tree; file-level content drift is not detected.

## Explicitly NOT claimed

- Semantic/vector retrieval (structured + lexical only; adapter boundary exists).
- Runtime verification in ZCode/OpenCode/Hermes live sessions.
- Filesystem snapshot / process rollback (logical checkpoint only).
- Multi-process concurrent-write safety.
