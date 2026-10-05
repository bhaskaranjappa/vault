# PAIOS TOOLING UPDATE — AGENCY AGENTS + MUNDER DIFFLIN — 2026-10-05

Status: CANONICAL operational follow-up
Source of truth: `bhaskaranjappa/vault` on `main`
Evaluation protocol: `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`

## 1. Agency Agents

Repository: https://github.com/msitarzewski/agency-agents
Dedicated app: https://agencyagents.app
License: MIT.

Role:
- Specialized agent-personality/workflow library.
- Runtime specialist layer only; it is not VAULT policy, canonical state, authority, or orchestration infrastructure.
- Useful for B2B client acquisition, job search, GenAI engineering and automation/agent-system tasks.

Upstream documentation currently supports installation into ZCode and other runtimes. The repository documents both a native desktop app for Windows/macOS/Linux and script-based integrations.

### 2026-10-05 direct installation evidence

Host: Windows
Agency clone:
`C:\Users\ABhas\agency-agents`

ZCode conversion:
- `./scripts/convert.sh --tool zcode`
- Result: **282 agents converted for zcode**.

Global installation:
- Destination: `C:\Users\ABhas\.zcode\agents`
- Result: **14 selected agents installed**.

Installed specialists:
1. ai-engineer
2. automation-governance-architect
3. code-reviewer
4. codebase-onboarding-engineer
5. email-intelligence-engineer
6. multi-agent-systems-architect
7. outbound-strategist
8. prompt-engineer
9. rag-pipeline-engineer
10. recruitment-specialist
11. research-synthesist
12. resume-tailor
13. sales-outreach
14. workflow-architect

Verification:
- All 14 definition files are present.
- All 14 have valid `name`/`description` frontmatter.
- All 14 match agent types discoverable in the active ZCode session.
- Live `code-reviewer` smoke test passed.
- No reinstall or PAIOS architecture change was performed.

Lifecycle:
**SUPPORTED → INSTALLED → ENABLED/CONFIGURED/RELEVANT RUNTIME STATE AS CURRENTLY EXPOSED BY ZCODE → VERIFIED FOR ZCODE DISCOVERABILITY/INVOCATION**

Disposition:
**INSTALL — specialist layer for the owner's ZCode workflow.**

Boundary:
- Do not install all 282 agents by default.
- Agency agents are execution specialists; VAULT remains canonical for truth, policy, authority, workflow state, durable decisions and evidence.
- Agency output is evidence/data and must not independently grant authority or become canonical state.
- Runtime-specific installation remains reversible.


## 2. Agency Agents — multi-runtime installation follow-up (2026-10-05)

The same 14 selected Agency specialists were additionally installed outside ZCode.

### OpenCode
- Installation completed successfully using the Agency/OpenCode integration.
- Selected set: **14/14 installed**.
- Runtime discoverability/invocation should be verified after the OpenCode process reloads the agent definitions; do not infer live invocation solely from file installation.

### Antigravity
- Installation completed successfully using the Agency/Antigravity integration.
- Selected set: 14/14 installed as Skills.
- Live workflow test completed: research-synthesist was successfully used together with Agent-Reach for repository research.
- Agency definitions remain runtime Skills in this test, not a separate native-agent registry.

### Freebuff
- A Freebuff-specific adapter converted the same 14 Agency agents into global Skills.
- Global path: C:\Users\ABhas\.agents\skills\agency-<slug>\SKILL.md
- The repair installer reported: Installed 14; Verified 14.
- Live workflow test completed: the research-synthesist Skill was discovered/loaded and its methodology was applied by the main Freebuff agent together with Agent-Reach.
- Separate Agency sub-agent invocation was not observed; do not claim native specialist spawning from this test.

### Current multi-runtime disposition
- ZCode: VERIFIED for discoverability/invocation from live evidence; Agency definitions are native Agents.
- OpenCode: INSTALLED; live discoverability/invocation still pending.
- Antigravity: INSTALLED as 14 Skills; live Skill use verified in an Agent-Reach research workflow.
- Freebuff: 14/14 global Skills file-verified; live Skill loading/use verified; separate Agency sub-agent invocation not verified.

Operational decision:
- Keep the same focused 14-agent set across the active execution runtimes rather than installing the full upstream catalog.
- Agency remains an on-demand specialist layer. It is not VAULT's memory, policy, authority, orchestration or canonical state.
- Having the specialists installed across runtimes supports executor switching when token/context limits or runtime availability require a change, but executor switching does not imply that the destination runtime has been live-verified until its reload/invocation evidence exists.

## 3. Munder Difflin

Repository reference: https://github.com/HarnessMD/munder-difflin
Current upstream project links also resolve through `chaitanyagiri/munder-difflin`.

Role:
- Local desktop multi-agent execution/UI harness around terminal coding CLIs.
- Provides multi-agent coordination, mailbox/blackboard/task tracking, worker supervision and a local agent workspace.
- It can wrap multiple terminal-agent runtimes, including OpenCode.

Existing disposition from 2026-10-03:
**TEST FIRST**.

### 2026-10-05 operational follow-up

Source-build attempt:
- Repository was cloned under `C:\Users\ABhas\munder-difflin`.
- Source installation failed during `better-sqlite3` native build because the active Node.js 25 environment had no matching prebuilt binary and the Windows build environment lacked the required Windows SDK.
- This failure affected the source-build path only.

Portable app:
- Latest Windows portable EXE was subsequently downloaded and run successfully.
- The Munder Difflin app launched.
- OpenCode was selected/visible as an execution agent.
- A minimal `hello.txt` test was proposed, but a successful end-to-end result is not recorded in this update.

Lifecycle:
**INSTALLED / OPERATIONAL APP LAUNCH — runtime task execution UNVERIFIED**

Disposition remains:
**TEST FIRST**, not promotion.

Boundary:
- Munder may be used as an execution/UI harness around VAULT-selected runtimes.
- VAULT remains the canonical policy/state/authority layer.
- Munder's local hive memory, mailbox, blackboard, task ledger or supervisor must not become a second canonical PAIOS source of truth.
- Do not count Munder itself as a PAIOS runtime-parity verification.

## 4. Combined architectural decision

`VAULT canonical policy/state`
→ `specialist layer (Agency Agents)`
→ `selected executor/runtime`
→ optional `Munder Difflin execution/UI harness`

Agency is already verified as a ZCode specialist layer.

Munder remains an isolated TEST FIRST candidate until a bounded live task demonstrates material value beyond the existing PAIOS execution/runtime mechanisms.

Neither tool changes the VAULT core architecture by itself.


## 5. Agent-Reach + Agency Agents productivity evaluation

Date: 2026-10-05

Agent-Reach was evaluated as an external productivity tool used around the active executor pool, not as a VAULT integration.

### Runtime results

| Runtime | Agency packaging | Agent-Reach | Specialist behavior | Result |
|---|---|---|---|---|
| ZCode | Native Agents | Verified | Separate Agency Agent execution | PASS |
| Antigravity | Skills | Verified | research-synthesist workflow completed through installed Skill | PASS |
| Freebuff | Skills | Verified | Main agent followed research-synthesist Skill; separate Agency sub-agent not observed | PARTIAL |
| OpenCode | Skills | Pending | Test still running at session close | PENDING |

### Practical productivity evidence

Bhaskar reported that research/workflows that normally take approximately 30–40 minutes in Antigravity, ZCode or Freebuff completed in approximately 3 minutes when specialist-agent + Agent-Reach workflows were used. This is direct owner observation and has not been independently benchmarked across a controlled task set.

### Real workflow evidence

Agent-Reach + email-intelligence-engineer was used to investigate Vedant Singh / Salus:
- identity and company affiliation were triangulated;
- the publicly published company/founders address founders@usesalus.ai was found;
- no personal email was guessed or pattern-generated.

Disposition for daily workflow:
KEEP ACTIVE / INSTALL — measurable practical value demonstrated.

Boundary:
- Agent-Reach remains an external capability provider.
- Agency Agents remain specialist Skills/Agents depending on runtime.
- Neither tool becomes VAULT memory, policy, authority or canonical state.
