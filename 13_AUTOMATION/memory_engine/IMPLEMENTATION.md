# PAIOS Memory/Context Engine — Implementation Notes

Status: IMPLEMENTATION (Phase 8) — subordinate to the canonical protocols.
Canonical sources: `03_PROTOCOLS/AIOS_MEMORY_ARCHITECTURE_V1.md`,
`03_PROTOCOLS/AIOS_CONTEXT_PACKAGE_SCHEMA_V1.md`,
`11_STATE/AIOS_CHECKPOINT_SCHEMA_V1.md`. This document describes one
implementation of those contracts; it does not override them.

## Architecture

```text
Canonical Knowledge → AIOS Protocols → paios_memory (this engine) → Runtime Adapter → Runtime
```

- Package: `13_AUTOMATION/memory_engine/paios_memory/` (Python 3, standard library only).
- Operational state: any state root; production default `11_STATE/memory/`.
- The engine is operational state, never canonical project truth.

Modules:

| Module | Role |
| --- | --- |
| `records.py` | `MemoryRecord` schema, validation, secret heuristic, enum vocabularies |
| `store.py` | `MemoryStore`: remember / get / update / invalidate / record_conflict; JSON persistence; `index.yaml` regeneration |
| `retrieval.py` | `Retriever`: candidate filtering, deterministic scoring, sensitivity ceiling, top-k |
| `context.py` | `ContextBuilder`: context packages, inheritance modes, budgeting |
| `checkpoint.py` | `CheckpointStore` (create/load/update), `repo_state`, safe `resume()` |

## Storage format

```text
<root>/
  index.yaml                    # retrieval index (ids only; regenerated on write)
  records/MEM-*.json            # one JSON record per memory
  conflicts/CONFLICT-*.json     # explicit conflict pairs
  checkpoints/CHK-*.json        # logical checkpoints
  context_packages/CTX-*.json   # context packages
```

Records are JSON; the logical field schema matches the YAML schema in
`AIOS_MEMORY_ARCHITECTURE_V1.md` §3 (with `source.kind/ref/captured_at` nested).

## API

```python
from paios_memory import (MemoryRecord, MemoryStore, Retriever, RetrievalQuery,
                          ContextBuilder, ContextRequest, TaskSpec,
                          Checkpoint, CheckpointStore, resume)

store = MemoryStore("11_STATE/memory")
rec = store.remember(MemoryRecord(content=..., type="FACT",
                                  source_kind="OWNER", source_ref="task://...",
                                  project="personal-ai-os"))
old, new = store.update(rec.memory_id, "new content",
                        source_kind="OWNER", source_ref="...")
store.invalidate(rec.memory_id, reason="contradicted")
results = Retriever(store).retrieve(RetrievalQuery(text="...", task=..., project=...,
                                                   max_sensitivity="INTERNAL"))
```

## Retrieval algorithm (structured + lexical)

Pipeline: `query → candidate retrieval → relevance scoring → freshness/source/conflict checks → sensitivity filter → threshold → ranking`.

Hard filters (drop before scoring): `INVALIDATED` and `SUPERSEDED` records,
sensitivity above the request ceiling, project/task scope mismatch (when both
sides specify one), and expired validity intervals. `CONFLICTING` records stay
retrievable (penalized, not hidden) unless `include_conflicting=False`.

Deterministic score (weights are implementation-defined, in `retrieval.py:WEIGHTS`):

```
relevance = 3·task_match + 2·project_match + 3·lexical_match(+semantic) +
            1·freshness + 2·source_quality + 1·confidence
            − 1.5·conflict − 0.5·sensitivity_boundary − 1·redundancy
```

- `lexical_match`: token-overlap (shared content/tag tokens vs query, capped) ∈ [0,1].
- `freshness`: exponential decay, half-life ≈ 90 days — old history never silently outranks newer authoritative records.
- `source_quality`: OWNER/CANONICAL_FILE 1.0, RUNTIME 0.8, EXTERNAL_SOURCE 0.6, CONVERSATION/AGENT 0.5.
- redundancy: ≥80% token overlap with an already-accepted record.
- Default threshold `min_relevance=3.0`, default `top_k=8`. This is what keeps an irrelevant personal memory out of a generic engineering task.

## Sensitivity model

`PUBLIC < INTERNAL < PERSONAL < SENSITIVE`. A retrieval/package request carries
`max_sensitivity`; any record above the ceiling is hard-filtered. Boundary-level
records get a small penalty.

## Conflict handling

`update(..., conflict=True)` preserves the old record as `CONFLICTING`, writes
a `CONFLICT-*.json` pair record, and cross-links both via `conflict_refs`.
Neither record is deleted; both remain individually discoverable.

## Context builder

Implements the package schema §2 verbatim. Inheritance modes `NONE`,
`SELECTED` (default for delegated work; only `selected_memory_ids` enter),
`RECENT_RELEVANT` / `FULL` (retrieve via `Retriever`). Records exceeding the
sensitivity ceiling are recorded in `inheritance.excluded_refs` — exclusion is
explicit, not left to the model's memory.

Budgeting: `max_items` truncates; `max_chars` keeps policy/mission/state
(everything except selected records) intact and drops lowest-priority selected
records first. Never drops objective, mandatory policy, or acceptance criteria.

## Checkpoints and resume

`CheckpointStore` persists the full `AIOS_CHECKPOINT_SCHEMA_V1.md` logical
schema as JSON. `repo_state()` captures branch/HEAD/working-tree. `resume()`
implements: load → verify repository state (flags HEAD/working-tree drift as
discrepancies rather than continuing) → verify authority scope → verify
completed claims carry evidence → report `next_action`. This is logical
checkpoint/restore only — no filesystem/process snapshotting.

## Extension point for semantic retrieval

`retrieval.SemanticAdapter` is a Protocol with `score(query, record) -> [0,1]`.
Pass an adapter to `Retriever(store, semantic_adapter=...)` and its
contribution enters the same deterministic formula as `semantic_match`. No
vector infrastructure exists or is claimed in this implementation.

## Tests

`tests/test_phase8.py` — 17 tests covering MC-01..MC-09 and CT-01..CT-08, all
in temporary directories (canonical memory untouched). Run:

```bash
cd 13_AUTOMATION/memory_engine && python -m unittest tests.test_phase8 -v
```
