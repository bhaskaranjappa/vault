# AIOS MEMORY + CONTEXT PROTOCOL — SUPPORTING CONTEXT

Status: CANONICAL SUPPORTING PROTOCOL
Purpose: record portable memory/context rules used by external runtimes to consume and preserve VAULT context. VAULT remains the canonical record; this document does not turn VAULT into an autonomous runtime.

## 1. Memory layers

AIOS recognizes four memory classes:

1. Canonical knowledge — versioned VAULT files; highest project authority.
2. Runtime/session state — temporary operational state for the current task.
3. Persistent memory — durable user/project memories stored outside the model weights.
4. Conversation history — historical context that may inform retrieval but never silently overrides current canonical truth.

## 2. Memory provenance

Each durable memory should preserve, where available:
- source;
- date/time;
- memory type;
- confidence/status;
- stated vs inferred classification;
- related project/task;
- conflict references.

## 3. Retrieval

Use semantic or structured retrieval when available. Retrieve only memory relevant to the current task.

Direct questions about the user's known context may use relevant persistent memory. Generic technical work should not receive unrelated personal memory.

## 4. Relevance gating

Before memory enters active context, evaluate:
- task relevance;
- freshness;
- source quality;
- conflict state;
- sensitivity;
- whether the memory is actually needed.

Irrelevant memory must be excluded.

## 5. Current-state precedence

When persistent memory conflicts with current canonical information:

`current explicit fact / direct runtime evidence / canonical repository > historical memory`

Do not silently replace the historical record. Preserve the conflict when it matters.

## 6. Explicit memory operations

The system may support:
- remember;
- update;
- forget;
- retrieve;
- invalidate.

Explicit user requests to store or forget information take precedence over inferred memory operations, subject to applicable system/runtime constraints.

## 7. Background memory extraction

A runtime may extract durable memories after completed work. Automatic extraction must be conservative and must never convert inference into a canonical fact without evidence.

## 8. Context package

Every task should receive a context package containing only:
- mission/task;
- required canonical rules;
- task-relevant knowledge;
- relevant workflow;
- runtime adapter;
- necessary prior state.

## 9. Selective inheritance

Delegated agents inherit only the context required by their bounded objective. The parent may explicitly widen the inheritance scope when necessary.

Inheritance modes:
- none;
- selected context;
- recent relevant context;
- full context when justified.

## 10. Context checkpointing

Long tasks maintain a compact checkpoint containing:
- objective;
- completed actions;
- current state;
- decisions;
- evidence;
- blockers;
- next incomplete action.

The checkpoint is sufficient for handoff without replaying the entire conversation.

## 11. Compaction and restoration

When context becomes constrained, preserve durable checkpoint state before compaction. After compaction, restore the task from the checkpoint and verify repository/runtime state before continuing.

## 12. Runtime boundary

A runtime may implement memory with files, databases, vector stores, semantic indexes, conversation retrieval or provider services. Those are implementation choices. None replaces canonical PAIOS knowledge.

## 13. Privacy

Sensitive or unnecessary personal information should not be copied into task context. Store and retrieve only what the task actually requires.
