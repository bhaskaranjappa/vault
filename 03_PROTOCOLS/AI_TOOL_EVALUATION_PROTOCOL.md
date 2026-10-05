# VAULT — AI TOOL / REPOSITORY EVALUATION PROTOCOL

Before installing a newly discovered repository/tool used in Bhaskar's workflow: identify the exact product/repo; read official documentation and repository material; compare against current goals and stack; identify overlap/gaps; check free/paid options, cost, licensing, security, maintenance and integration; then choose INSTALL, TEST FIRST, KEEP IN RESERVE, REPLACE, IGNORE or REJECT.

Never install merely because a tool is popular or appears useful. Prefer small focused stacks. Record evidence and verification status.

## V1+ AI TOOL / REPOSITORY DISCOVERY AND CAPABILITY-ENHANCEMENT WORKFLOW

### Purpose

Use this protocol to discover external repositories, tools, MCP servers, plugins, skills, sub-agent systems, orchestration components, browser systems, research tools and other capability providers that may materially improve the Personal AI OS workflow or a specific runtime.

The goal is not maximum tool count. The goal is measurable productivity improvement without turning an external tool into VAULT's source of truth.

### Operating model

**ChatGPT or another capable research LLM** is the research and evaluation planner.

**Active executor pool:** the owner currently uses ZCode, OpenCode, Antigravity and Freebuff. The owner selects the runtime for each hands-on task according to access, token/context limits, task fit and workflow preference.

**Prompt/test design rule:** every implementation, installation, repository-evaluation or benchmark prompt must be written for the executor the owner is currently using. Use that runtime's native commands, agent model, MCP/configuration surface and recovery mechanisms. Do not assume another runtime's interface.

**Executor switching:** token/context exhaustion is an expected operating condition. When switching executors, preserve the exact execution state with the handoff procedure and continue from the first incomplete action.

**Universal parity is not required:** do not test every coding agent merely to establish that all agents work. Test only the executor and runtime capability required by the current task or hypothesis.

Codex and Cursor are currently unavailable to the owner and should not be selected for execution until the owner explicitly reports access again.

**Other LLM runtimes** such as Claude, Gemini and Grok may consume the canonical protocol and evidence to perform equivalent research, analysis, review or planning. No runtime becomes the source of truth.

### Standard pipeline

1. **Capability-gap identification**
   - Start with an observed workflow problem, bottleneck or missing capability.
   - Define the baseline behavior before searching for a solution.
   - Prefer capability gaps over tool-name searches.

2. **Repository/tool discovery**
   - Identify candidate repositories or products.
   - Prefer first-party documentation, repository source, releases, issue history and official configuration guidance.
   - Use connected research capabilities where available.
   - Do not treat a catalogue, star count, model claim or marketing page as proof of suitability.

3. **Deep research and architecture assessment**
   - Read the candidate's relevant documentation and repository material deeply enough to understand its purpose, architecture, dependencies, runtime model, supported interfaces and operational constraints.
   - Determine whether the candidate provides a tool, MCP server, plugin, skill, sub-agent, orchestration layer, context mechanism, browser capability, research capability or another concrete improvement.
   - Record known limits and unknowns.

4. **Protocol-based suitability decision**
   - Compare the candidate with the current Personal AI OS stack and the identified capability gap.
   - Assess overlap, incremental value, maintenance burden, cost, licensing, security, privacy, reversibility and integration complexity.
   - Produce a bounded test specification only when the candidate has a credible path to measurable value.
   - Candidate disposition before runtime testing: `IGNORE`, `KEEP IN RESERVE`, `TEST FIRST`, or another approved decision state.

5. **Preferred execution: owner-selected active executor**
   - Give the currently selected executor the complete test specification and relevant canonical context.
   - The executor inspects the repository/runtime first, then installs or runs only what is required.
   - The executor captures raw evidence, measurements, failure modes and reproducibility information.
   - Design the prompt specifically for that executor rather than copying a runtime-generic command sequence.
   - Keep tool-call, reasoning and execution budgets bounded.

6. **Controlled executor switch**
   - If the active executor exhausts usable tokens/context, becomes unavailable, or cannot continue reliably, create or update a handoff record containing:
     - current task and objective;
     - exact progress completed;
     - files changed;
     - commands/actions already performed;
     - evidence locations;
     - remaining work;
     - known failures and hypotheses;
     - repository commit/branch/state;
     - constraints that must not be violated.
   - Resume in the newly selected executor from that handoff state instead of restarting the experiment.
   - The destination executor must first inspect the inherited state and verify the handoff before continuing.
   - The executor switch is execution continuity, not permission to expand scope.

7. **Runtime evaluation**
   - Compare baseline versus tool-enhanced workflow using the same decision-relevant task set.
   - Measure, where relevant: evidence quality, coverage, false positives/negatives, speed, cost, provenance completeness, reliability, operational complexity, governance compliance and unique decision value.
   - Test failure and missing-data behavior, not only the happy path.
   - Do not weaken thresholds after observing poor results.

8. **Independent analysis**
   - A research LLM or reviewer analyzes the captured evidence.
   - Classify the result as `PASS`, `PARTIAL`, or `FAIL`.
   - Identify whether value is real, redundant, conditional, or unproven.
   - Preserve unresolved conflicts and unknowns.

9. **Disposition**
   - `INSTALL` only when evidence demonstrates material incremental value and operational fit.
   - `REPLACE` only when the new component clearly supersedes an existing component.
   - `KEEP IN RESERVE` when the component works but its trigger condition has not been met.
   - `IGNORE` when value is insufficient, redundant, commercially unsuitable, unsafe, or outside the workflow.
   - `REJECT` for governance, security, legal or other disqualifying reasons.

10. **Canonical recording**
    - Record the candidate, evaluation date, source evidence, test design, runtime used, result, measurements, provenance, lifecycle state and final disposition.
    - Update the AI tool registry and decision history when the evidence changes canonical state.
    - Store raw or large runtime evidence outside the canonical repository when appropriate, with stable references and hashes where practical.
    - Tool output is evidence input, never canonical truth.

11. **Promotion and integration**
    - Only after an `INSTALL` decision, integrate the component into the smallest appropriate runtime/tool layer.
    - Preserve least privilege and read-only operation when write capability is unnecessary.
    - Distinguish `SUPPORTED`, `INSTALLED`, `ENABLED`, `CONFIGURED`, `AUTHENTICATED`, and `VERIFIED`.
    - Runtime integration must be separately verified from standalone tool evaluation.

12. **Operational benchmark**
    - After promotion, test the complete workflow with the enhanced stack.
    - Compare against the pre-tool baseline.
    - Confirm that the component improves the actual workflow rather than only passing synthetic tests.
    - Do not repeat completed experiments without a concrete new hypothesis or changed environment.

### Capability-layer guidance

Evaluate candidates by the capability they add, not by their branding or repository category.

Possible layers include:

- **Tools/MCP:** external system access and evidence retrieval.
- **Skills:** reusable procedural behavior and domain-specific instructions.
- **Sub-agents:** specialization, delegation and parallel task execution.
- **Orchestration:** task decomposition, sequencing and bounded delegation.
- **Context/memory:** controlled retrieval and context management.
- **Browser/automation:** rendering, interaction and stateful web workflows.
- **Research/extraction:** web discovery, crawling, scraping and evidence capture.
- **Engineering utilities:** repository analysis, debugging, testing and code intelligence.

Do not assume an MCP server will solve a sub-agent, orchestration or context-management problem. Evaluate each capability layer separately.

### Tool trust and evaluation depth

Evaluation depth is proportional to **trust, privilege, risk, and integration depth**. Do not automatically treat a first-party vendor tool and an unknown third-party repository as equivalent diligence cases, and do not reject a tool merely because it is open-source, community-built, solo-developed or small.

#### First-party / major-vendor tools

For a tool built and maintained by a major vendor or first-party ecosystem:
- verify the relevant official documentation and supported capability claims;
- verify availability, configuration and actual runtime behavior where the capability matters;
- check material cost, permissions, privacy/security constraints and integration fit;
- deep source-code inspection is normally unnecessary unless the privilege/risk or the workflow requires it.

#### Established open-source / community projects

For an established open-source or community project:
- perform documentation and source/release review appropriate to the capability;
- inspect maintenance/activity, dependencies, licensing, security posture and operational constraints;
- run a bounded runtime test before production promotion when practical.

#### Unknown / small / solo-developer projects

For unknown or lightly established projects:
- perform deeper source/code and dependency review;
- inspect permissions, network access, credential handling, install/build behavior and data handling;
- check maintenance/release history and licensing;
- use an isolated or least-privilege bounded experiment before promotion when practical.

#### Privilege overrides brand

Any tool that receives sensitive credentials, filesystem write access, browser control, email/external communication, code execution, autonomous agent authority or other high-impact privileges requires appropriately strong verification regardless of who built it.

The objective is not to prefer Big Tech over open source. The objective is to spend diligence where failure or misuse would matter, while still verifying that every promoted component closes a real capability gap.

### Cross-LLM portability

The canonical workflow must be understandable and executable by ChatGPT, Claude, Gemini, Grok and other supported LLM runtimes.

Each runtime may use its native tools, plugins, MCP clients, sub-agents or skills, but those mechanisms are adapters and execution aids. They must not become a second source of truth.

The portable instruction is:

`Discover → Research deeply → Assess gap/fit → Specify bounded experiment → Execute in ZCode → Fail over to OpenCode if needed → Measure → Review → Decide → Record canonically → Promote → Rebenchmark`

### Governance boundaries

- No fabricated evidence, contacts, metrics, capabilities or lifecycle states.
- No secret material committed to the repository.
- No unnecessary write permissions.
- No architecture expansion merely to accommodate a candidate tool.
- No installation solely for popularity, novelty or completeness.
- No restart from zero after executor failover when a valid handoff exists.
- No final promotion without evidence.
- External communication follows the effective owner/bot authority policy; per-action human approval is not a universal V1+ requirement.
