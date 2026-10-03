# PAIOS V1+ EXTERNAL REPOSITORY EVALUATION — 2026-10-03

Status: CANONICAL V1+ evaluation
Task: Evaluate OpenDots/OpenMuse/Munder Difflin/Paperclip for fit with Personal AI OS.
Source of truth: `bhaskaranjappa/personal-ai-os` on `main`.
Evaluation protocol: `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`.

## 1. Current PAIOS gap

Phase 14 is the latest implemented canonical phase. Codex CLI is the first directly verified real runtime through the canonical adapter.

The next real integration step is a second authenticated/usable runtime followed by real cross-runtime parity measurement.

Therefore, a candidate is valuable only if it closes a concrete gap around:
- runtime execution and multi-runtime operation;
- orchestration/supervision;
- memory/context;
- automation;
- governance/evidence;
- user-facing agent workspace.

No candidate was installed or promoted during this evaluation.

## 2. Repository identity

The name `OpenDots` is ambiguous. Two materially relevant repositories were evaluated:

1. `diggerhq/opendots` — model-agnostic personal agent on OpenComputer.
2. `CopilotKit/OpenDots` — self-hosted persistent AI coworkers with computers, web/mobile UI, calls and Slack.

The current Munder Difflin repository is `HarnessMD/munder-difflin`; older references under `chaitanyagiri/munder-difflin` resolve to this project.

The relevant Paperclip repository is `paperclipai/paperclip`.

The relevant OpenMuse repository is `tahodev/openmuse`.

## 3. Candidate evaluation

| Candidate | Primary layer | PAIOS overlap | Main incremental value | Main conflict/cost | Disposition |
|---|---|---|---|---|---|
| HarnessMD/munder-difflin | Local multi-agent execution harness | Very high | Wraps many existing terminal-agent CLIs, multi-agent hive, mailbox, memory, supervision and local operation | Duplicates PAIOS orchestration/memory/state; its own god-agent/HITL semantics need an explicit adapter boundary | TEST FIRST |
| paperclipai/paperclip | Agent-team control plane | Very high | Mature task/org/budget/routine/governance control plane with Codex/OpenCode/Claude/etc. adapters and plugins | Large overlap with PAIOS orchestration, automation and governance; risks becoming a second control plane/source of state | KEEP IN RESERVE |
| tahodev/openmuse | Security-primitives personal-agent runtime | Medium | Exact-action approvals, host policy boundary, tamper-evident audit, secret isolation, bounded workers | Exact-action approval model differs from PAIOS policy-level autonomous authority; alpha; native Windows unsupported | KEEP IN RESERVE |
| CopilotKit/OpenDots | Agent workspace/product UI | Medium | Persistent specialist Dots, per-Dot computers, pages, Slack/calls, background work, automatic learning | Heavy CopilotKit/AG-UI/Intelligence/OpenBot stack; alpha; much of this is product/UI rather than PAIOS core capability | KEEP IN RESERVE |
| diggerhq/opendots | Personal-agent UX/runtime | Low-Medium | Topics, persistent notes, cloud computers, model-agnostic agents | Strong OpenComputer dependency; young/early-preview app; not a second verified PAIOS runtime | KEEP IN RESERVE |

## 4. Munder Difflin assessment

Munder Difflin is the closest architectural fit to the current PAIOS execution surface.

Its HIVE model provides per-agent identity/memory, a shared blackboard, mailbox routing, a durable task ledger, worker supervision, bounded hops and a privileged orchestrator. Its README also wraps multiple terminal-agent runtimes, including Codex and OpenCode.

This maps closely to PAIOS Phase 9 and Phase 14 concerns:
`dispatcher → workers → runtime CLIs → evidence`.

The critical integration rule is separation of authority:
- PAIOS remains canonical knowledge and policy.
- PAIOS remains the authority model.
- Munder Difflin may act as an execution/UI harness.
- Munder state must not become canonical PAIOS state.
- Any Munder god-agent must not silently replace the PAIOS root authority model.

The project is active and currently publishes support for multiple CLI agents. Source evidence was reviewed from `README.md`, `HIVE.md`, `SPEC.md`, package metadata and current commit activity.

## 5. Paperclip assessment

Paperclip is a broader control plane than Munder Difflin.

It provides agent org charts, task ownership, atomic checkout, heartbeat execution, budgets, governance, routines, plugins, secrets, activity logs, company portability and adapters for Codex, OpenCode, Claude, Gemini and other runtimes.

It is therefore highly relevant to future B2B operating workflows. However, those same features overlap heavily with existing PAIOS Phase 9, Phase 10 and Phase 12 engines.

The correct architectural relationship would be:
`PAIOS canonical policy/state → Paperclip adapter/execution surface`.

Do not import Paperclip as a second canonical orchestration database without a demonstrated capability gap and explicit authority mapping.

Paperclip's own documentation describes it as a control plane rather than the execution plane. Its current roadmap still marks Memory / Knowledge as partial, so it does not replace the PAIOS memory/context layer.

## 6. OpenMuse assessment

OpenMuse is valuable as a security/reference implementation.

Its strongest ideas are host-enforced policy, one-time exact-action approvals, redacted HMAC hash-chain auditing, process-separated secret handling and bounded workers.

However, its security model intentionally pauses every sensitive action for exact-action user approval. PAIOS instead uses policy-level delegated authority and permits autonomous execution inside that scope.

That difference is architectural, not cosmetic.

OpenMuse is therefore best used as a security benchmark and threat-model reference rather than as the core runtime.

## 7. OpenDots assessment

### CopilotKit/OpenDots

This project is strong at the user-facing agent workspace layer.

It combines persistent specialists, individual agent computers, page/document workspaces, browser tooling, calls, Slack and background work. Its latest activity also includes parallel research/extraction and automatic-learning work.

It can inspire a future PAIOS product surface, but it adds a substantial external stack and does not solve the immediate second-runtime parity gap.

### diggerhq/opendots

This project is simpler and strongly aligned with personal-agent UX.

It delegates long-running topics to OpenComputer agents, stores owner/topic notes, and supports model selection per agent. Its architecture relies on an external OpenComputer service and HTTPS callback setup.

That dependency makes it less attractive as a portable PAIOS execution substrate.

## 8. Decision

For the current PAIOS architecture, the candidates are not interchangeable.

**Best current fit for an external execution harness: Munder Difflin.**

**Best future control-plane reference: Paperclip.**

**Best security-primitives reference: OpenMuse.**

**Best future end-user workspace reference: CopilotKit OpenDots.**

**Digger OpenDots:** useful personal-agent UX reference, but not a current PAIOS priority.

The result is a disposition, not a promotion. No candidate should be installed until a bounded experiment demonstrates incremental value against the live PAIOS baseline.

## 9. Recommended bounded experiment

Test Munder Difflin first, in isolation, against a narrow PAIOS scenario:

1. Register two existing runtimes: Codex and OpenCode.
2. Give the harness one bounded read-only task with explicit acceptance criteria.
3. Confirm whether Munder can dispatch and track both runtimes without owning PAIOS policy/state.
4. Capture runtime identity, task identity, authority propagation, failure handling and evidence.
5. Verify whether Munder's local state can be treated purely as an adapter/runtime cache.
6. Do not promote unless the experiment demonstrates material value not already provided by the PAIOS runtime adapter/orchestration layers.

A real cross-runtime parity test remains blocked until a second runtime is authenticated and usable. Munder cannot be counted as that verification by itself.

## 10. Primary source evidence

- PAIOS canonical state: `PLAN.md`, `00_MASTER_INDEX.md`, `12_VALIDATION/AIOS_PHASE14_STATUS_2026-09-17.md`, `12_VALIDATION/AIOS_PHASE14_REAL_RUNTIME_TESTS.md`.
- Munder Difflin: https://github.com/HarnessMD/munder-difflin
- Digger OpenDots: https://github.com/diggerhq/opendots
- CopilotKit OpenDots: https://github.com/CopilotKit/OpenDots
- OpenMuse: https://github.com/tahodev/openmuse
- Paperclip: https://github.com/paperclipai/paperclip
- Paperclip docs: https://docs.paperclip.ing/

## 11. Evidence limitations

This was a source/documentation/repository evaluation. No candidate was installed, authenticated, or runtime-tested.

Therefore no candidate receives VERIFIED runtime status from this evaluation.
