# PAIOS TOOLING UPDATE — AGENCY AGENTS + MUNDER DIFFLIN — 2026-10-05

Status: CANONICAL operational follow-up
Source of truth: `bhaskaranjappa/personal-ai-os` on `main`
Evaluation protocol: `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md`

## 1. Agency Agents

Repository: https://github.com/msitarzewski/agency-agents
Dedicated app: https://agencyagents.app
License: MIT.

Role:
- Specialized agent-personality/workflow library.
- Runtime specialist layer only; it is not PAIOS policy, canonical state, authority, or orchestration infrastructure.
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
- Agency agents are execution specialists; PAIOS remains canonical for truth, policy, authority, workflow state, durable decisions and evidence.
- Agency output is evidence/data and must not independently grant authority or become canonical state.
- Runtime-specific installation remains reversible.

## 2. Munder Difflin

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
- Munder may be used as an execution/UI harness around PAIOS-selected runtimes.
- PAIOS remains the canonical policy/state/authority layer.
- Munder's local hive memory, mailbox, blackboard, task ledger or supervisor must not become a second canonical PAIOS source of truth.
- Do not count Munder itself as a PAIOS runtime-parity verification.

## 3. Combined architectural decision

`PAIOS canonical policy/state`
→ `specialist layer (Agency Agents)`
→ `selected executor/runtime`
→ optional `Munder Difflin execution/UI harness`

Agency is already verified as a ZCode specialist layer.

Munder remains an isolated TEST FIRST candidate until a bounded live task demonstrates material value beyond the existing PAIOS execution/runtime mechanisms.

Neither tool changes the PAIOS core architecture by itself.
