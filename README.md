<div align="center">

# 🔐 VAULT

### Your personal AI memory agent

**One evolving memory. Multiple AI models. More continuity, less repetition.**

A personal memory layer designed to carry your profile, goals, working style, preferences, tools, and project context across the AI systems you use every day.

![Project](https://img.shields.io/badge/PROJECT-Personal_AI_Memory-6558D3?style=for-the-badge)
![Workflow](https://img.shields.io/badge/CURRENT_WORKFLOW-Manual-DAA520?style=for-the-badge)
![Focus](https://img.shields.io/badge/FOCUS-Cross--Platform_Continuity-218C74?style=for-the-badge)

</div>

---

## 💡 Why VAULT exists

Every time you switch an AI model, open a new chat, or move to another coding agent, you risk starting from zero. You repeat your background, re-explain your goals, list your tools, and reconstruct decisions or unfinished work.

**VAULT is being built to solve that continuity gap.**

It is your personal AI memory agent: a durable record of who you are, how you work, what you are trying to achieve, which tools you use, and where your work currently stands. The goal is to make that context reusable across providers rather than trapped inside one chatbot or coding environment.

> **The idea:** explain yourself once, preserve what matters, and carry useful context into the next session.

## 🧠 What VAULT is designed to remember

| Memory area | What it preserves |
|---|---|
| **Profile and goals** | Background, skills, priorities, and long-term objectives |
| **Working style** | How an AI should explain, research, plan, code, review, and communicate |
| **Preferences** | Response style, constraints, recurring choices, and collaboration expectations |
| **Tools and integrations** | Models, coding agents, skills, plugins, MCP servers, hooks, and relevant setup state |
| **Projects and decisions** | Current objective, architecture, completed work, trade-offs, blockers, and next steps |
| **Conversation continuity** | Session summaries, important discoveries, decisions, and unresolved threads |
| **Execution handoffs** | What has already been done, evidence collected, files changed, and where the next session should resume |
| **Knowledge and evidence** | Reusable findings, source references, verification status, and the difference between facts and assumptions |

## 🌐 One memory layer across your AI workflow

VAULT is intended to support the AI services and coding agents you regularly use—not to lock your memory to one vendor.

<div align="center">

| LLM chat environments | Coding-agent environments |
|:---:|:---:|
| ChatGPT · Claude | Claude Code · OpenCode |
| Gemini · Grok | GrokBuild · Hermes |
| DeepSeek · Z.ai | Antigravity · Freebuff · ZCode |
| Other LLM chatbots | Other coding agents |

</div>

**Integration status matters:** these are target environments for cross-platform continuity, not a claim that every listed platform is already connected or automatically synchronized.

## 🔄 How the workflow works today

The current VAULT workflow is repository-backed and **requires manual commands and a review step**. Automatic session capture and updating across LLMs and coding agents are still in development.

<div align="center">

**START SESSION**  
↓  
**Load relevant VAULT context**  
↓  
**Work in your chosen AI model or coding agent**  
↓  
**Summarize important outcomes**  
↓  
**Review and approve the changes**  
↓  
**Update canonical memory for the next session**

</div>

### The commands

| Command | Purpose |
|---|---|
| `VAULT BOOT` | Start from the canonical repository, establish the current state, and load only the context needed |
| `VAULT SUMMARIZE` | Generate a dated summary of the current conversation, including decisions, results, blockers, and continuation details |
| `VAULT UPDATE` | After review and approval, reconcile the summary with canonical files and record durable changes |
| `VAULT TEST` | Evaluate a tool or repository against a real capability gap using research, bounded testing, evidence, and a clear decision |

These are conversational instructions for an AI or operator following VAULT's protocols; they are not shell commands.

<details>
<summary><strong>⚠️ Current limitation — read before relying on VAULT</strong></summary>

VAULT does **not yet automatically collect and synchronize every conversation** across the listed LLMs and coding agents. Today, the user must invoke the appropriate boot, summarize, and update workflow, and review changes before write-back.

The automatic feature and broader integrations are planned work. Until they are implemented and verified, do not assume a conversation has been saved just because it happened in an AI application.

</details>

## 🧭 Operating principles

- **Continuity over chat history:** preserve durable context that remains useful after a conversation ends.
- **One canonical record:** use the repository as the source of truth, not the model's recollection or an unreviewed generated summary.
- **Relevant context, not everything:** load the smallest useful subset for the task at hand.
- **Evidence over assumptions:** mark uncertainty, preserve provenance, and do not turn claims into verified facts without evidence.
- **Reviewed write-back:** separate generating a summary from approving and recording durable changes.
- **Clear handoffs:** resume from the first incomplete action rather than repeating completed work.
- **Portable by design:** keep the memory structure understandable and useful across different AI tools and providers.

## 🗂️ Repository map

The repository is organized so a new session can navigate from the entrypoint to the relevant context without loading everything.

| File or directory | Role |
|---|---|
| `START.md` | Bootstrap, execution, write-back, and closeout instructions |
| `00_MASTER_INDEX.md` | Canonical overview, status, source hierarchy, and navigation |
| `PLAN.md` | Roadmap and historical plan |
| `01_PROFILE/` | Profile and portable AI working style |
| `02_AI_STACK/` | AI stack and architecture research |
| `03_PROTOCOLS/` | Operating contracts and evaluation procedures |
| `08_KNOWLEDGE/` | Durable knowledge and reusable findings |
| `10_SOURCES/` | Source ledger and provenance |
| `11_STATE/` | Current state, handoffs, and session continuity |
| `12_VALIDATION/` | Tests, validation evidence, and closeout records |

Use `START.md` as the entrypoint. The master index is the navigation guide; individual canonical files hold the relevant details.

## 🚧 What's next

The intended evolution of VAULT includes:

- [ ] **Automatic session capture** across supported LLM and coding-agent environments
- [ ] **Start/end-of-session automation** to collect relevant context and propose durable updates
- [ ] **Provider and agent integrations** using the appropriate supported extension points
- [ ] **Smarter context retrieval** so each session receives relevant memory instead of an entire history dump
- [ ] **Reliable synchronization and conflict handling** across multiple runtimes
- [ ] **Clear provenance and review controls** for what is remembered, changed, or left unsaved
- [ ] **Verification and recovery workflows** for failed, partial, or interrupted updates

These are roadmap goals, not claims of shipped functionality. Capabilities should be marked complete only after implementation and verification.

## 🚀 Start here

For an AI model, coding agent, or human operator beginning a session:

1. Read `START.md`.
2. Follow its boot sequence and inspect `00_MASTER_INDEX.md`.
3. Load only the profile, state, knowledge, and protocols relevant to the current objective.
4. Confirm what is complete, what remains, and what evidence supports the current state.
5. At closeout, follow the summarize → review → update → validate workflow.

If the current environment cannot access the private repository, provide the specific authorized files or excerpts needed for that session. Repository access and automatic synchronization must never be assumed.

---

<div align="center">

**VAULT — Your context should travel with you.**

*Built around a simple goal: spend less time re-explaining, and more time moving work forward.*

</div>
