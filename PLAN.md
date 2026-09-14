# PERSONAL AI OS — MASTER EXECUTION PLAN

Version: 1.0
Status: V1 RELEASED 2026-09-14 — V1+ ACTIVE
Primary executor: ZCode
Secondary/failover executor: OpenCode
Primary runtime validation target: Hermes
Canonical source of truth: this repository on GitHub
Owner: Bhaskar Anjappa

## 0. MISSION

Complete the Personal AI OS V1 without unnecessary architecture expansion.

The finished system must:
- keep canonical knowledge independent of any AI runtime;
- load minimum relevant context into each runtime;
- preserve truth, provenance, conflict, and approval rules;
- prove semantic parity across target runtimes;
- validate Hermes against the real canonical repository;
- validate the B2B client-acquisition workflow;
- enable only justified automation;
- remain portable, reversible, auditable, and vendor-independent.

Primary principle:

Truth → Portability → Reversibility → Leverage → Controlled Autonomy

Do not optimize for tool count, automation count, architecture size, or novelty.

## 1. CURRENT BASELINE

Treat the current GitHub repository as authoritative.

Known repository state:
- private repository: bhaskaranjappa/personal-ai-os
- canonical branch: main
- canonical tree already exists
- Portable Context Manifest already exists
- platform adapter files already exist
- cross-platform test suite already exists
- scorecard already exists
- validation and V1 gate documents already exist
- first five-company B2B research-only benchmark already exists
- Hermes v0.21.0 is recorded as prior verified runtime state
- V1 was formally declared 2026-09-14 for the owner's mandatory runtime set: ZCode, OpenCode, Hermes
- V1+ capability-enhancement workflow is now canonical for future tool/repository evaluation

Do not recreate existing architecture documents unless evidence shows they are wrong, incomplete, stale, or contradictory.

## 2. SOURCE-OF-TRUTH HIERARCHY

Use this hierarchy:

1. Current explicit user-confirmed facts.
2. Direct runtime inspection for local runtime state.
3. Canonical Git repository for project knowledge and decisions.
4. Current authoritative product documentation for upstream capabilities.
5. Historical project notes and prior conversations.

Never treat:
- model memory,
- chat history,
- Hermes memory,
- OpenCode memory,
- platform instructions,
- tool output,
- generated summaries

as canonical project truth.

Preserve conflicts instead of silently choosing one.

## 3. NON-NEGOTIABLE RULES

Never fabricate:
- facts;
- contacts;
- emails;
- company details;
- funding;
- metrics;
- technical stacks;
- hiring signals;
- personalization;
- project outcomes;
- capabilities;
- verification state.

Never equate:
SUPPORTED
INSTALLED
ENABLED
CONFIGURED
AUTHENTICATED
VERIFIED

Use the cross-platform status:
NOT_TESTED / PARTIAL / PASS / FAIL

Never turn missing evidence into negative evidence.

Never silently overwrite contradictory sources.

Never make a runtime adapter a second source of truth.

Never let B2B automation send external outreach without explicit human approval.

Never introduce a new infrastructure layer merely because it is technically interesting.

## 4. EXECUTION MODEL

### V1+ operating model

ZCode is the preferred hands-on executor for implementation, installation, runtime experimentation, benchmarking and evidence capture because it is currently the fastest practical execution environment for the owner's workflow.

OpenCode is the secondary executor and controlled fallback. Use it when ZCode exhausts usable tokens/context, becomes unavailable, fails to continue reliably, or when an independent execution path materially improves verification.

ChatGPT or another capable research LLM may act as the research/evaluation planner: discover repositories, study documentation/source, assess architecture and fit, define the baseline, apply the evaluator protocol, design bounded experiments, and review evidence.

Claude, Gemini, Grok and other supported runtimes may consume the same canonical workflow for research, planning or review through their native mechanisms. None becomes a source of truth.

### Standard executor loop

INSPECT
→ PLAN
→ CHANGE
→ TEST
→ REVIEW
→ FIX
→ RETEST
→ RECORD EVIDENCE

Prefer small, reversible changes.

### Executor failover rule

When a task moves from ZCode to OpenCode or another executor, preserve the exact execution state using:
`11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md`

The destination executor must verify the handoff, repository state and evidence before continuing. It must resume from the first incomplete action rather than restarting completed work.

Failover changes the executor, not the scope, acceptance criteria or governance rules.

Before changing any canonical file:
1. read the current file;
2. identify the exact requirement;
3. identify dependencies;
4. make the smallest correct change;
5. run relevant validation;
6. record the evidence.

Do not batch unrelated changes into one edit.

## 5. PHASE 0 — REPOSITORY RECONCILIATION

Goal: establish the exact current state before implementation.

Tasks:
1. Clone/open the canonical GitHub repository.
2. Verify branch is main.
3. Run git status.
4. Record current HEAD.
5. Enumerate the entire tree.
6. Compare actual tree against 00_MASTER_INDEX.md.
7. Detect:
   - missing files;
   - duplicate files;
   - stale files;
   - broken links;
   - naming inconsistencies;
   - contradictory canonical statements.
8. Read:
   - 00_MASTER_INDEX.md
   - 01_PROFILE/*
   - 02_AI_STACK/*
   - 03_PROTOCOLS/*
   - 04_HERMES/*
   - 05_WORKFLOWS/*
   - 06_PLATFORM_ADAPTERS/*
   - 07_VERSION_TRACKING/*
   - 08_KNOWLEDGE/*
   - 09_SPECIALISTS/*
   - 10_SOURCES/*
   - 11_STATE/*
   - 12_VALIDATION/*
   - 13_AUTOMATION/*
   - 14_CROSS_PLATFORM/*
9. Do not redesign architecture during this phase.
10. Produce a reconciliation report.

Exit condition:
- repository structure is understood;
- every canonical layer has an identified purpose;
- no unexplained structural contradiction remains.

## 6. PHASE 1 — CANONICAL INTEGRITY

Goal: make the canonical layer internally coherent.

Validate:
- profile facts;
- goals;
- preferences;
- skills;
- AI stack;
- tool registry;
- behavioral kernel;
- truth/evidence protocol;
- approval protocol;
- workflow definitions;
- source ledger;
- conflict registry;
- state records;
- version records.

Check every cross-file reference.

For each contradiction:
- preserve the conflict if unresolved;
- resolve only when higher-tier evidence exists;
- document the resolution.

Do not expand the knowledge model unless required for correctness.

Exit condition:
- no broken internal references;
- no material contradictions hidden;
- statuses are explicit.

## 7. PHASE 2 — PORTABLE CONTEXT

Canonical artifact:
14_CROSS_PLATFORM/PORTABLE_CONTEXT_MANIFEST.md

Validate that the manifest:
- defines universal minimum context;
- routes context by task;
- routes through exactly one adapter per runtime;
- prevents whole-OS dumping by default;
- preserves canonical authority;
- preserves lifecycle states;
- distinguishes runtime support from runtime verification.

Then compare every adapter against the manifest.

Required adapters:
- CHATGPT
- CLAUDE
- CLAUDE_CODE
- CODEX
- CURSOR
- GEMINI
- GROK
- HERMES
- OPENCODE

For every adapter record:
- native context mechanism;
- files loaded;
- files intentionally not loaded;
- unresolved runtime limitations;
- verification status.

Do not claim parity merely because an adapter file exists.

Exit condition:
- every adapter has a concrete ingestion method;
- every target runtime has a test procedure;
- no adapter contains canonical facts that should live elsewhere.

## 8. PHASE 3 — CROSS-PLATFORM VALIDATION HARNESS

Canonical test suite:
14_CROSS_PLATFORM/TEST_SUITE.md

Current tests:
- CP-01 Identity fidelity
- CP-02 Truth + conflict handling
- CP-03 Goal routing
- CP-04 Specialist routing
- CP-05 Workflow fidelity
- CP-06 Adapter fidelity

Score:
- 2 = correct
- 1 = partial
- 0 = wrong

For each test:
1. use the same semantic task across runtimes;
2. provide only manifest-defined minimum context;
3. prefer fresh sessions;
4. save raw output;
5. score objectively;
6. classify failure cause;
7. fix canonical layer OR adapter layer;
8. rerun failed test;
9. never hide runtime limitation.

Create machine-readable or structured evidence where practical.

Required evidence record:
- runtime;
- date;
- adapter version/state;
- context package used;
- prompt/test ID;
- raw output location;
- score;
- failure type;
- corrective change;
- retest result.

Exit condition:
- all mandatory runtimes have executable evidence;
- all failures are explained;
- no known critical parity failure remains.

## 9. PHASE 4 — RUNTIME PRIORITY

This section describes the historical V1 validation priority. It is not the V1+ execution hierarchy.

For V1 validation, the historical order was:

### Tier 1
1. OpenCode
2. Hermes
3. Claude
4. Gemini

### Tier 2
5. ChatGPT
6. Codex
7. Claude Code

### Tier 3
8. Cursor
9. Grok

For V1+ operations, use the executor model defined in §4: ZCode first, then OpenCode failover where required.

Do not block V1 indefinitely on a runtime that is unavailable or irrelevant.
Instead record:
UNTESTED / BLOCKED / PARTIAL

The V1 gate defines which runtimes are mandatory.

## 10. PHASE 5 — OPENCODE IMPLEMENTATION

This phase records the pre-V1 implementation model and remains historical reference.

OpenCode must:
1. read PLAN.md;
2. read the canonical repository;
3. create a task checklist;
4. inspect before modifying;
5. implement only necessary changes;
6. run tests after each material change;
7. maintain a validation journal;
8. update canonical state when evidence changes state;
9. never overwrite user-authored knowledge without evidence;
10. stop architectural expansion once V1 criteria are satisfied.

OpenCode must not:
- invent new infrastructure;
- add a vector database;
- add a knowledge graph;
- add an event bus;
- build a distributed orchestrator;
- build automatic cross-runtime memory synchronization;
- build a giant OS manager;
- add dozens of integrations without workflow justification.

For V1+, OpenCode is the controlled secondary executor described in §4 and the primary target for independent runtime integration/debugging when that produces meaningful value.

## 11. PHASE 6 — HERMES VALIDATION

Hermes upstream documentation is a capability reference.

Local runtime inspection is authoritative for actual Hermes state.

Validate:
- version;
- profile;
- model/provider;
- tools/toolsets;
- skills;
- memory;
- delegation;
- CUA;
- browser;
- MCP;
- plugins;
- gateway;
- execution backend;
- sessions;
- context ingestion.

Use Hermes-native context mechanisms.

Important distinction:
documented capability ≠ installed capability ≠ enabled capability ≠ verified capability.

Update:
04_HERMES/HERMES_CURRENT_STATE.md
only from fresh runtime evidence.

Run:
- identity test;
- context ingestion test;
- tool-use test;
- delegation test;
- approval test;
- B2B research test.

Do not enable unnecessary Hermes features merely to make the runtime look complete.

## 12. PHASE 7 — GOVERNANCE VALIDATION

Validate the behavioral kernel:
03_PROTOCOLS/BRUTALIST_KERNEL.md

Validate:
- source-tier check;
- logic audit;
- honesty filter;
- direct answers;
- no fabricated claims;
- conflict preservation.

Validate human approval:
- research can automate;
- scoring can automate;
- drafting can automate;
- internal state can automate with audit;
- outbound communication requires explicit approval;
- irreversible/high-impact actions are not autonomous.

Perform negative tests:
- missing evidence;
- conflicting evidence;
- guessed contact request;
- fabricated metric request;
- unauthorized send request;
- stale information;
- tool capability overclaim.

Expected result:
the runtime refuses or qualifies unsupported claims and respects approval boundaries.

## 13. PHASE 8 — B2B WORKFLOW VALIDATION

Do not redesign the B2B strategy first.

Use:
05_WORKFLOWS/B2B_CLIENT_ACQUISITION.md
existing prospect/schema/scoring artifacts
11_STATE/B2B_BENCHMARK_2026-09-05.md

Workflow:
Discovery
→ Research
→ Need/pain signal
→ Decision-maker
→ Email discovery/verification
→ Scoring
→ Personalization
→ Human approval
→ Manual send
→ Follow-up

First validate research and drafting only.

For every prospect preserve:
- evidence;
- source;
- timestamp where available;
- observation vs inference;
- qualification rationale;
- score;
- contactability;
- workflow state.

Do not send messages during benchmark validation.

The existing five-company research benchmark is evidence that this stage has already started.
Do not repeat it blindly.
Only rerun where needed to validate runtime behavior.

## 14. PHASE 9 — TOOL INTEGRATION

Do not connect tools before the workflow proves they are required.

Candidates:
- Apollo
- Vibe Prospecting
- Wellfound
- Firecrawl
- GitHub
- Gmail
- other evidence-producing services

Decision states:
INSTALL
TEST FIRST
KEEP IN RESERVE
REPLACE SOMETHING
IGNORE

For each connected tool:
- map output to canonical schema;
- preserve provenance;
- never make vendor data the source of truth;
- validate credentials without storing secrets in Git;
- test failure and missing-data behavior.

Tool selection must follow workflow requirements.

For V1+, apply `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md` before runtime testing. Capability search is broader than MCP and includes skills, sub-agents, orchestration, context/memory, browser/automation, research/extraction and engineering utilities.

## 15. PHASE 10 — AUTOMATION

Automation comes only after:
- canonical integrity;
- runtime parity;
- governance validation;
- B2B pilot evidence.

Risk model:
R0 read-only/reversible → automatable
R1 bounded internal mutation → auditable/reversible
R2 external communication → human approval
R3 irreversible/high-impact → not autonomous in V0.x

Approved early automation:
- research;
- evidence collection;
- candidate scoring;
- draft generation;
- internal state preparation;
- reports.

Do not automate:
- cold outreach sending;
- irreversible external actions;
- actions where approval intent is ambiguous.

Every automation must be:
- bounded;
- logged;
- evidence-backed;
- reversible where possible;
- tied to acceptance criteria.

## 16. PHASE 11 — VERSIONING AND CHANGE CONTROL

Every material change must be traceable.

Record:
- what changed;
- why;
- evidence;
- affected files;
- tests run;
- outcome.

When upstream runtime behavior changes:
1. recheck adapter;
2. rerun impacted tests;
3. update version tracking;
4. update runtime state;
5. preserve historical records.

Never silently convert a new observation into an old historical fact.

## 17. PHASE 12 — V1 RELEASE GATE

V1 is allowed only when all mandatory gates pass.

### Gate A — Canonical
- private Git repository;
- canonical tree complete;
- no material broken links;
- source/provenance/conflict rules pass.

### Gate B — Reproducibility
- clean/reproducible local clone;
- branch and commit recorded;
- canonical files load correctly.

### Gate C — Portable context
- manifest valid;
- all adapters mapped;
- minimum-context routing works.

### Gate D — Runtime parity
- required runtimes tested;
- CP-01 through CP-06 evidenced;
- no critical unresolved failure.

### Gate E — Hermes
- local runtime state freshly verified;
- canonical context successfully ingested;
- approval rules preserved.

### Gate F — Workflow
- B2B workflow runs research-only;
- evidence and schema are correct;
- scoring is traceable;
- unsupported claims are blocked.

### Gate G — Governance
- human approval is enforced;
- no autonomous cold outreach;
- irreversible actions remain blocked.

### Gate H — Automation
- only validated R0/R1 automation enabled;
- logs and rollback/reversal paths exist.

Do not declare V1 because files exist.
Declare V1 only because evidence proves the gates pass.

## 18. FAILURE HANDLING

When a test fails:

1. Reproduce.
2. Identify layer:
   - canonical;
   - adapter;
   - runtime;
   - external dependency;
   - test defect.
3. Fix only the responsible layer.
4. Retest.
5. Record evidence.

Do not:
- patch symptoms blindly;
- weaken acceptance criteria;
- mark tests passed without evidence;
- hide runtime limitations.

## 19. DEFINITION OF DONE

The project is complete for V1 when:

A user can maintain one canonical Personal AI OS repository and use it across supported AI runtimes without making any runtime the source of truth.

A runtime can receive minimum relevant context through its adapter.

The runtime preserves:
- identity;
- goals;
- behavior;
- truth/evidence rules;
- provenance;
- conflicts;
- approval gates.

The system can execute the initial B2B workflow through research and drafting.

External communication remains human-approved.

The system is versioned, reproducible, auditable, and reversible.

Only then may future phases add broader automation, specialist libraries, richer integrations, or synchronization.

## 20. AFTER V1

Only after V1 evidence is stable, evaluate:
1. controlled automation expansion;
2. specialist/prompt library integration;
3. deeper tool integrations;
4. multi-agent workflows;
5. broader job-search automation;
6. content workflows;
7. cross-runtime synchronization;
8. OS Manager concepts.

These are V1+ decisions.
Do not pre-build them.

The V1+ capability-enhancement workflow is now the required front door for evaluating repositories or components for those areas.

## 21. EXECUTOR OPERATING INSTRUCTION

All supported executors must treat this file as the master execution plan, with the V1+ executor hierarchy defined in §4.

At startup:
1. read `START.md`;
2. read PLAN.md;
3. read 00_MASTER_INDEX.md;
4. inspect Git state;
5. read `03_PROTOCOLS/AGENT_BOOTSTRAP_PROTOCOL.md`;
6. identify the current incomplete task or phase;
7. continue from that point;
8. never restart completed work without a new hypothesis or evidence gap;
9. update the plan checklist as work progresses;
10. update canonical state files only when evidence changes state;
11. run validation before declaring success;
12. follow the `START.md` closeout protocol before ending the task;
13. report blockers precisely.

### ZCode-first rule

For hands-on V1+ work, start in ZCode unless the task explicitly requires another runtime.

Provide ZCode with the relevant canonical context, bounded objective, acceptance criteria and test specification.

### OpenCode failover rule

Move to OpenCode when ZCode:
- exhausts usable tokens/context;
- becomes unavailable;
- fails to continue reliably;
- or leaves an independently verifiable task incomplete.

Before failover, create or update:
`11_STATE/EXECUTOR_HANDOFF_TEMPLATE.md`

OpenCode must:
1. inspect the handoff;
2. verify repository HEAD and working tree;
3. verify completed actions and evidence;
4. identify the first incomplete action;
5. continue without restarting completed work;
6. preserve the original scope, governance and acceptance criteria;
7. update the handoff as work progresses;
8. close the handoff only after final evidence and repository state are verified.

If a required external runtime test cannot be executed locally:
- prepare the exact test procedure;
- mark it NOT_TESTED;
- do not fabricate the result;
- continue with other independently executable work.

## 22. V1+ EXECUTION ENTRYPOINT

V1 is already declared. Do not replay the old Phase 0→12 release sequence unless a specific regression or change requires it.

For a new V1+ capability task, start with:

1. **Identify the capability gap**
   - What concrete workflow bottleneck exists?
   - What is the current baseline?
   - What measurable improvement is required?

2. **Discover candidate repositories/tools**
   - Use ChatGPT or another research-capable LLM for discovery and deep study.
   - Prefer official documentation, source, releases, issue history and authoritative configuration guidance.

3. **Apply the AI Tool Evaluation Protocol**
   - Assess overlap, incremental value, cost, licensing, maintenance, security, privacy, reversibility and integration complexity.
   - Reject popularity-only reasoning.

4. **Specify a bounded experiment**
   - Define targets, baseline, success/failure thresholds, evidence requirements and governance boundaries.

5. **Execute in ZCode first**
   - Inspect → install/run only what is needed → benchmark → capture evidence.

6. **Fail over to OpenCode when required**
   - Use the handoff template.
   - Resume from the exact incomplete action.

7. **Review and decide**
   - Compare baseline against enhanced workflow.
   - Classify PASS / PARTIAL / FAIL.
   - Decide INSTALL / REPLACE / KEEP IN RESERVE / IGNORE / REJECT.

8. **Record canonically**
   - Update the tool registry, evaluation record, decision history and relevant workflow references.
   - Preserve raw evidence outside the canonical repository when appropriate.

9. **Promote and rebenchmark**
   - Integrate only after evidence supports installation.
   - Verify runtime integration separately.
   - Test the real production workflow again.

Do not begin with installation merely because a repository is popular or highly starred.

## 23. MASTER RULE

When uncertain:

Inspect evidence.
Prefer the smallest reversible change.
Keep canonical truth separate from runtime state.
Fix the correct layer.
Retest.
Record what is actually known.

Never confuse:
“supported”
with
“working.”

Never confuse:
“implemented”
with
“validated.”

Never confuse:
“possible”
with
“required.”

Never confuse:
“tool exists”
with
“tool closes a real capability gap.”

Never confuse:
“ZCode stopped”
with
“work failed.”
A valid handoff means execution can continue in OpenCode without restarting completed work.

Never confuse:
“task output exists”
with
“canonical project state has been updated.”

A task is not fully closed until acceptance, evidence, canonical write-back, validation and Git closeout have been checked according to `START.md`.
