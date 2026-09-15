# HUMAN APPROVAL PROTOCOL — DEPRECATED

Status: SUPERSEDED 2026-09-15

Per-action human approval is no longer the required execution gate for PAIOS.

Use the canonical autonomous authority model in:

`03_PROTOCOLS/BOT_AUTHORITY_PROTOCOL.md`

The current model is:

`Owner Policy → Grok Bot → delegated bot → tool/action`

Authority is granted at policy/delegation level. A bot may execute autonomously within its effective scope without requesting approval for every individual action.

The following controls remain mandatory:
- explicit policy authorization for capabilities;
- bounded delegation;
- least-privilege scope;
- truth/evidence/provenance rules;
- untrusted-content boundary;
- verification of material actions;
- auditability;
- platform and system safety restrictions.

This file is retained only as historical provenance so old references do not become an unnoticed second policy.
