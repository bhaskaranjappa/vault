# AIOS MEMORY ARCHITECTURE V1

Status: CANONICAL V1+ — PHASE 8 IMPLEMENTATION
Purpose: define a vendor-neutral durable memory model that can be implemented with files, databases, vector stores, provider APIs, or hybrid storage without making any runtime memory canonical.

## 1. Design goals

The memory layer must:
- preserve evidence and provenance;
- distinguish stated, inferred, observed and historical information;
- preserve conflicts instead of silently overwriting them;
- retrieve only task-relevant memory;
- respect freshness, source quality and sensitivity;
- support explicit remember/update/forget/retrieve/invalidate operations;
- remain portable across runtimes;
- keep canonical repository knowledge above runtime memory;
- permit simple file-backed implementation before specialized infrastructure is justified.

## 2. Authority hierarchy

Memory is never the highest authority.

`Current explicit owner fact / direct runtime evidence / canonical repository > persistent memory > conversation history > model inference`

A memory record may be useful context without becoming project truth.

## 3. Memory record

Every durable memory SHOULD use this logical schema:

```yaml
memory_id: MEM-<stable-id>
content: <fact, preference, decision, observation, or useful context>
type: FACT | PREFERENCE | DECISION | OBSERVATION | PROCEDURE | PROJECT_STATE | CONTACT | OTHER
status: ACTIVE | SUPERSEDED | INVALIDATED | CONFLICTING | HISTORICAL
classification: STATED | INFERRED | RUNTIME_OBSERVED
source:
  kind: OWNER | CANONICAL_FILE | RUNTIME | CONVERSATION | EXTERNAL_SOURCE | AGENT
  ref: <path/url/task/message/evidence-id>
  captured_at: <ISO-8601>
confidence: HIGH | MEDIUM | LOW | UNKNOWN
project: <project-id>
task: <task-id-or-null>
tags: [<topic>, ...]
sensitivity: PUBLIC | INTERNAL | PERSONAL | SENSITIVE
valid_from: <ISO-8601-or-null>
valid_until: <ISO-8601-or-null>
related_memories: [MEM-...]
conflict_refs: [MEM-...]
created_at: <ISO-8601>
updated_at: <ISO-8601>
```

Required fields for canonicalized durable memory: `memory_id`, `content`, `type`, `status`, `classification`, `source`, `confidence`, `created_at`, `updated_at`.

## 4. Write policy

Store a memory only when at least one is true:
- the owner explicitly asks to remember it;
- it is a durable project decision or state needed for future work;
- it materially reduces repeated work;
- it is verified runtime/project state with an identifiable source.

Do not store:
- transient conversational filler;
- unsupported guesses;
- secrets or credentials unless a dedicated secure system explicitly authorizes storage;
- unrelated personal information;
- generated claims without provenance.

When uncertain, do not write durable memory.

## 5. Update policy

Never silently mutate historical meaning.

For a changed fact:
1. preserve the previous record;
2. mark it `SUPERSEDED` or `CONFLICTING` as appropriate;
3. create/update the current record with new provenance;
4. retain a relationship through `related_memories` or `conflict_refs`.

## 6. Retrieval pipeline

Use this sequence:

`Task query → candidate retrieval → relevance scoring → freshness/source/conflict checks → sensitivity filtering → context budget → selected memory`

Candidate retrieval may be:
- exact/structured lookup;
- lexical search;
- semantic/vector retrieval;
- metadata filtering;
- hybrid retrieval.

The implementation MAY start with structured/lexical retrieval. A vector database is not required by the protocol.

## 7. Relevance score

A runtime implementation SHOULD calculate a deterministic ranking signal using:

`relevance = task_match + project_match + semantic_match + freshness + source_quality + confidence - sensitivity_penalty - conflict_penalty - redundancy_penalty`

The protocol does not mandate specific numeric weights.

A memory should enter active context only when it passes the configured relevance threshold and is permitted by task scope.

## 8. Gating rules

Reject a candidate from active context when:
- it is outside the task/project scope;
- sensitivity is not authorized;
- it is invalidated;
- it is clearly stale and a newer authoritative record exists;
- it is unresolved low-confidence speculation with no task need;
- it exceeds the context budget after higher-value candidates have been selected.

Conflicting records may both be surfaced when the conflict affects the task.

## 9. Current-state reconciliation

When memory conflicts with current evidence:
- use the current authoritative source for action;
- preserve the historical memory;
- record the conflict when material;
- do not rewrite history to make sources appear consistent.

## 10. Explicit memory operations

### remember
Create a durable record with provenance and classification.

### retrieve
Return only task-relevant records permitted by scope and sensitivity.

### update
Create a new current record or transition status while preserving provenance.

### forget
Invalidate/remove a memory when policy permits; preserve an audit record where required.

### invalidate
Mark a record unusable without pretending it never existed.

## 11. Background extraction

Automatic memory extraction is optional. When enabled it MUST:
- be conservative;
- require identifiable source context;
- preserve `INFERRED` versus `STATED`;
- never promote an inference into a canonical fact automatically;
- allow review or later invalidation.

## 12. Storage adapters

Supported implementation patterns:

`File-backed | SQLite | SQL/Document DB | Vector DB | Provider memory | Hybrid`

All adapters MUST expose the same logical operations and preserve the same provenance semantics.

Runtime memory is an acceleration layer. The Git repository remains canonical project truth.

## 13. Minimal Phase 8 implementation

The first implementation should be file-backed unless a measured workload justifies a database/vector service.

Recommended structure:

```text
11_STATE/
  memory/
    index.yaml
    records/
      MEM-*.yaml
    conflicts/
      CONFLICT-*.yaml
    retrieval/
      <task-id>.yaml
```

The `index.yaml` is a retrieval index, not a second canonical knowledge base.

## 14. Validation targets

Phase 8 implementation is considered structurally complete when it can demonstrate:
- explicit memory write;
- persistence across sessions;
- relevant retrieval;
- irrelevant-memory exclusion;
- provenance preservation;
- stated/inferred distinction;
- conflict preservation;
- current-state precedence;
- sensitivity gating;
- explicit invalidation/forgetting;
- compact context-package generation.

Runtime-specific verification remains separate from this protocol.
