# AIOS CAPABILITY PRIMITIVES

Status: CANONICAL EXTRACTION CATALOG
Sources: Claude Fable 5.1, GPT-6 Astra/Codex, Grok Bot.

This catalog converts source-prompt behaviors into reusable, vendor-neutral architectural primitives. Source prompts remain immutable research captures; this file is the normalized layer.

## Classification

- PORTABLE — policy/behavior that can survive runtime changes.
- RUNTIME-ADAPTER — runtime-specific mechanism implementing a portable capability.
- VENDOR-SPECIFIC — product/UI/API behavior intentionally kept outside core AIOS.
- REJECTED — behavior incompatible with AIOS truth, authority, safety, portability or reversibility.

## Source mapping

### Claude Fable 5.1
Memory, semantic retrieval, conversation retrieval, relevance gating, stated-vs-inferred separation, current-state verification, uncertainty/no-guess behavior, internal-data-first routing, structured MCP parsing, artifact/visual reasoning.

### GPT-6 Astra/Codex
Bounded and nested delegation, agent hierarchy, parallel execution, per-agent model selection, reasoning-effort routing, selective context inheritance, task identity, checkpoints/compaction, plan/execution modes, plugin/tool provenance, task-completion bias.

### Grok Bot
Dispatcher/worker architecture, act-by-default execution, worker supervision, resume/redirect/stop, connector-first routing, durable automation, explicit authority boundary, untrusted-content boundary, persistent execution, progress and evidence behavior.

## Primitive catalog

| ID | Primitive | Source | Class | PAIOS status |
|---|---|---|---|---|
| P-001 | mission_contract | Astra | PORTABLE | COVERED |
| P-002 | objective_scope | Astra | PORTABLE | COVERED |
| P-003 | acceptance_criteria | Astra/Grok | PORTABLE | COVERED |
| P-004 | source_hierarchy | Claude/PAIOS | PORTABLE | COVERED |
| P-005 | evidence_requirement | Claude | PORTABLE | COVERED |
| P-006 | current_state_verification | Claude | PORTABLE | PARTIAL |
| P-007 | uncertainty_no_guess | Claude | PORTABLE | COVERED |
| P-008 | fact_claim_inference_separation | Claude | PORTABLE | COVERED |
| P-009 | provenance_tracking | Claude/Astra | PORTABLE | COVERED |
| P-010 | conflict_preservation | PAIOS/Claude | PORTABLE | COVERED |
| P-011 | persistent_memory | Claude | PORTABLE | PARTIAL |
| P-012 | semantic_memory_retrieval | Claude | PORTABLE | PARTIAL |
| P-013 | explicit_memory_write | Claude | PORTABLE | PARTIAL |
| P-014 | background_memory_extraction | Claude | PORTABLE | MISSING |
| P-015 | conversation_retrieval | Claude | PORTABLE | PARTIAL |
| P-016 | memory_relevance_gating | Claude | PORTABLE | MISSING |
| P-017 | stated_vs_inferred_memory | Claude | PORTABLE | PARTIAL |
| P-018 | memory_conflict_resolution | Claude | PORTABLE | PARTIAL |
| P-019 | memory_privacy_policy | Claude | PORTABLE | PARTIAL |
| P-020 | context_selection | Claude/Astra | PORTABLE | PARTIAL |
| P-021 | context_budgeting | Claude/Astra | PORTABLE | PARTIAL |
| P-022 | selective_context_inheritance | Astra | PORTABLE | MISSING |
| P-023 | project_continuity | Claude/Astra | PORTABLE | COVERED |
| P-024 | checkpointing | Astra | PORTABLE | PARTIAL |
| P-025 | compaction_state_restore | Astra | PORTABLE | PARTIAL |
| P-026 | task_identity | Astra | PORTABLE | PARTIAL |
| P-027 | task_decomposition | Astra | PORTABLE | COVERED |
| P-028 | bounded_delegation | Astra | PORTABLE | PARTIAL |
| P-029 | nested_delegation | Astra | PORTABLE | MISSING |
| P-030 | agent_hierarchy | Astra | PORTABLE | PARTIAL |
| P-031 | dispatcher_architecture | Grok Bot | PORTABLE | MISSING |
| P-032 | parallel_workers | Astra/Grok Bot | PORTABLE | PARTIAL |
| P-033 | specialist_agents | Astra/Grok Bot | PORTABLE | PARTIAL |
| P-034 | worker_health_supervision | Grok Bot | PORTABLE | MISSING |
| P-035 | worker_resume | Grok Bot | PORTABLE | PARTIAL |
| P-036 | worker_redirect | Grok Bot | PORTABLE | PARTIAL |
| P-037 | worker_stop | Grok Bot | PORTABLE | PARTIAL |
| P-038 | model_routing | Astra | PORTABLE | PARTIAL |
| P-039 | per_agent_model_routing | Astra | PORTABLE | MISSING |
| P-040 | reasoning_effort_routing | Astra | PORTABLE | MISSING |
| P-041 | capability_based_model_selection | Astra | PORTABLE | MISSING |
| P-042 | tool_routing | Claude/Grok Bot | PORTABLE | PARTIAL |
| P-043 | internal_data_first | Claude | PORTABLE | PARTIAL |
| P-044 | connector_first | Grok Bot | PORTABLE | PARTIAL |
| P-045 | web_current_data_routing | Claude/Grok Bot | PORTABLE | PARTIAL |
| P-046 | structured_mcp_parsing | Claude | PORTABLE | PARTIAL |
| P-047 | tool_provenance | Astra | PORTABLE | PARTIAL |
| P-048 | act_by_default | Grok Bot | PORTABLE | PARTIAL |
| P-049 | continue_until_complete | Astra/Grok Bot | PORTABLE | PARTIAL |
| P-050 | retry_and_recovery | Grok Bot/Astra | PORTABLE | PARTIAL |
| P-051 | verify_after_action | Grok Bot | PORTABLE | COVERED |
| P-052 | authority_scope | Grok Bot | PORTABLE | NEW |
| P-053 | authority_delegation_chain | Grok Bot/Astra | PORTABLE | NEW |
| P-054 | authority_expiration_revocation | Grok Bot | PORTABLE | NEW |
| P-055 | untrusted_content_boundary | Grok Bot | PORTABLE | NEW |
| P-056 | prompt_injection_resistance | Grok Bot/Claude | PORTABLE | PARTIAL |
| P-057 | durable_automation_intent | Grok Bot | PORTABLE | PARTIAL |
| P-058 | scheduled_automation | Grok Bot | PORTABLE | PARTIAL |
| P-059 | condition_automation | Grok Bot | PORTABLE | PARTIAL |
| P-060 | progress_visibility | Grok Bot | PORTABLE | COVERED |
| P-061 | evidence_backed_reporting | Claude/Grok Bot | PORTABLE | COVERED |
| P-062 | completeness_check | Astra/Grok Bot | PORTABLE | PARTIAL |
| P-063 | canonical_closeout | PAIOS | PORTABLE | COVERED |
| P-064 | runtime_adapter_boundary | PAIOS | PORTABLE | COVERED |

## Highest-priority implementation gaps

1. authority_scope + authority_delegation_chain + untrusted_content_boundary;
2. dispatcher architecture + worker supervision;
3. per-agent model/reasoning routing;
4. semantic memory + relevance gating;
5. selective context inheritance;
6. nested delegation;
7. stronger checkpoint/compaction/state restoration.

## Design constraint

Do not implement every primitive as prompt text. Primitives are architecture-level capabilities. They may be implemented through policy, runtime configuration, tools, state files, orchestration code or small reusable prompt modules depending on the runtime.
