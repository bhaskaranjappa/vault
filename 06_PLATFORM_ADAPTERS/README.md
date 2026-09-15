# PLATFORM ADAPTERS

These files translate the canonical AIOS specification into runtime-specific ingestion and execution mechanisms.

Canonical layers:

`AIOS_SPEC → adapter → native runtime`

Available adapters:
- CHATGPT.md
- CLAUDE.md
- CLAUDE_CODE.md
- CODEX.md
- CURSOR.md
- GEMINI.md
- GROK.md
- GROK_BOT.md
- HERMES.md
- OPENCODE.md
- ZCODE.md

`GROK_BOT.md` is the authoritative adapter for Grok Bot's autonomous root-orchestrator role. `GROK.md` is retained only for generic Grok chat/runtime consumption.

Adapters must not contain canonical project facts that belong in the core repository.