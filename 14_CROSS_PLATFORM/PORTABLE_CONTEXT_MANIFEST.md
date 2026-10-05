# PORTABLE CONTEXT MANIFEST

Purpose: define the minimum canonical context a runtime should receive without duplicating the Personal AI OS or turning runtime memory into a second source of truth.

## Universal minimum

Every runtime receives, directly or through its native adapter:

- `01_PROFILE/` — identity, goals, preferences, skills
- `02_AI_STACK/` — current AI stack and tool registry
- `03_PROTOCOLS/` — behavioral, truth/evidence, tool-evaluation, and approval rules
- relevant `05_WORKFLOWS/` — only the workflow needed for the current task
- relevant `06_PLATFORM_ADAPTERS/` — runtime-specific translation rules
- relevant `08_KNOWLEDGE/` — only the durable knowledge needed for the task

Do not dump the entire VAULT into every runtime by default.

## Routing rule

`canonical knowledge → runtime adapter → native runtime context`

Adapters translate. They do not become independent sources of truth.

## Task routing

### Identity / personal context
Load:
- `01_PROFILE/MY_PROFILE.md`
- `01_PROFILE/MY_GOALS.md`
- `01_PROFILE/MY_PREFERENCES.md`
- `01_PROFILE/MY_SKILLS.md`

### AI/tool decisions
Load:
- `02_AI_STACK/MY_AI_STACK.md`
- `02_AI_STACK/AI_TOOL_REGISTRY.md`
- relevant files under `02_AI_STACK/TOOL_EVALUATIONS/`

### Behavioral / truth / governance
Load:
- `03_PROTOCOLS/BRUTALIST_KERNEL.md`
- `03_PROTOCOLS/TRUTH_AND_EVIDENCE_PROTOCOL.md`
- `03_PROTOCOLS/HUMAN_APPROVAL_PROTOCOL.md`
- `03_PROTOCOLS/AI_TOOL_EVALUATION_PROTOCOL.md` when evaluating tools

### B2B client acquisition
Load:
- `05_WORKFLOWS/B2B_CLIENT_ACQUISITION.md`
- relevant prospect/company knowledge under `08_KNOWLEDGE/`
- approval protocol before any external communication

### Job search
Load:
- `05_WORKFLOWS/JOB_SEARCH.md`
- relevant profile and job-search knowledge

### GenAI engineering / coding
Load:
- `05_WORKFLOWS/GENAI_ENGINEERING.md`
- relevant project knowledge
- Python preference from profile

### Research
Load:
- `05_WORKFLOWS/RESEARCH.md`
- relevant project/decision knowledge
- truth/evidence protocol

### Content creation
Load:
- `05_WORKFLOWS/CONTENT_CREATION.md`
- relevant profile/goals/knowledge

## Runtime adapter rule

Use exactly one runtime adapter for each target runtime. Current adapter files:

- `06_PLATFORM_ADAPTERS/CHATGPT.md`
- `06_PLATFORM_ADAPTERS/CLAUDE.md`
- `06_PLATFORM_ADAPTERS/CLAUDE_CODE.md`
- `06_PLATFORM_ADAPTERS/CODEX.md`
- `06_PLATFORM_ADAPTERS/CURSOR.md`
- `06_PLATFORM_ADAPTERS/GEMINI.md`
- `06_PLATFORM_ADAPTERS/GROK.md`
- `06_PLATFORM_ADAPTERS/HERMES.md`
- `06_PLATFORM_ADAPTERS/OPENCODE.md`

A runtime adapter is not considered operational merely because the file exists. Native ingestion and behavioral parity must be tested.

## Verification states

Use:

`SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED`

For cross-platform portability, also record:

`NOT_TESTED | PARTIAL | PASS | FAIL`

Never convert documentation support into local runtime verification.
