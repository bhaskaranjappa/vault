# AI TOOL EVALUATION PROTOCOL

Before installing a newly discovered repository/tool: identify the exact product/repo; read official documentation and repository material; compare against current goals and stack; identify overlap/gaps; check free/paid options, cost, licensing, security, maintenance and integration; then choose INSTALL, TEST FIRST, KEEP IN RESERVE, REPLACE, IGNORE or REJECT.

Never install merely because a tool is popular or appears useful. Prefer small focused stacks. Record evidence and verification status.

## V1+ AI TOOL / REPOSITORY DISCOVERY AND CAPABILITY-ENHANCEMENT WORKFLOW

### Purpose

Use this protocol to discover external repositories, tools, MCP servers, plugins, skills, sub-agent systems, orchestration components, browser systems, research tools and other capability providers that may materially improve the Personal AI OS workflow or a specific runtime.

The goal is not maximum tool count. The goal is measurable incremental capability.

### Operating model

**ChatGPT or another capable research LLM** is the research and evaluation planner.

**ZCode** is the preferred hands-on executor for implementation, installation, runtime testing and evidence capture because it is currently the fastest practical execution environment for the owner's workflow.

**OpenCode** is the secondary executor and controlled fallback when ZCode reaches token/context limits, becomes unavailable, or cannot complete the current task cleanly.

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

5. **Preferred execution: ZCode first**
   - Give ZCode the complete test specification and relevant canonical context.
   - ZCode inspects the repository/runtime first, then installs or runs only what is required.
   - ZCode captures raw evidence, measurements, failure modes and reproducibility information.
   - Keep tool-call, reasoning and execution budgets bounded.

6. **Controlled failover to OpenCode**
   - If ZCode exhausts its available tokens/context before completing the task, cannot continue reliably, or becomes operationally unavailable, create or update a handoff record containing:
     - current task and objective;
     - exact progress completed;
     - files changed;
     - commands/actions already performed;
     - evidence locations;
     - remaining work;
     - known failures and hypotheses;
     - repository commit/branch/state;
     - constraints that must not be violated.
   - Resume in OpenCode from that handoff state instead of restarting the experiment.
   - OpenCode must first inspect the inherited state and verify the handoff before continuing.
   - The failover is execution continuity, not permission to expand scope.

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

### Cross-LLM portability

The canonical workflow must be understandable and executable by ChatGPT, Claude, Gemini, Grok and other supported LLM runtimes.

Each runtime may use its native tools, plugins, MCP clients, sub-agents or skills, but those mechanisms are adapters and execution aids. They must not become a second source of truth.

The portable instruction is:

`Discover → Research deeply → Assess gap/fit → Specify bounded experiment → Execute in ZCode → Fail over to OpenCode if needed → Measure → Review → Decide → Record canonically → Promote → Rebenchmark`

### Governance boundaries

- No autonomous external outreach.
- No fabricated evidence, contacts, metrics, capabilities or lifecycle states.
- No secret material committed to the repository.
- No unnecessary write permissions.
- No architecture expansion merely to accommodate a candidate tool.
- No installation solely for popularity, novelty or completeness.
- No restart from zero after executor failover when a valid handoff exists.
- No final promotion without evidence.
