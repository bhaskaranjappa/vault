# JOBS — Current Project Handoff

**Reconciled:** 2026-11-12 (Asia/Kolkata; exact time not recorded)  
**Operational repository:** https://github.com/bhaskaranjappa/jobs (private)  
**Current JOBS main HEAD observed:** `c7041774bc0a123f1606af971293cea98961c556`  
**Current tracker:** private JOBS `00-tracking.csv`

## Current pipeline design

The private JOBS repository contains the YC-led discovery/enrichment/drafting handoff:
- run schemas for search, enriched contacts and manifests;
- prompts for YC job search, contact enrichment and JD-aware drafting;
- commands for run creation, enrichment, drafting and Gmail reconciliation;
- specialist agent/skill contracts;
- a run-level validator;
- synthetic end-to-end fixtures;
- GitHub Actions validation.

The synthetic fixture and data-contract workflow passed on 2026-11-12. This validates the schemas/validator path; it does not mean a live YC search has run.

## Outreach snapshot

The private tracker contains 45 records from the November 11 reconciliation:
- 22 older outreach records with follow-ups sent.
- 23 newer first-email records.
- Last recorded no-reply check was 2026-11-11 20:55 IST. This is historical only.
- Do not infer current inbox status from that old check.

Full row-level data stays in the private tracker. This public VAULT handoff does not reproduce founder contact details or email addresses.

## Important current contact note

GetCrux/Atharva Padhye is already represented in the current tracker with an email recorded as sent on 2026-11-11 and confidence `FOUND_UNVERIFIED`. It is not a fresh `NOT_FOUND` prospect. Do not repeat the proposed Prospector test against this already-contacted record without a specific owner-approved reason.

## Prospector finding

Historical enrichment artifacts record Prospector `find_emails` invocations for FirstWork and Guac. The exact original MCP logs/live usage_stats were not inspected in the ChatGPT session. The next audit is local Prospector usage/log inspection, not an assumption that the tool was never called.

## Next incomplete engineering action

Start a real dated YC search run in private JOBS:
1. read current MEMORY.md, 00-tracking.csv, 01-notes.md and tool registry;
2. build exclusions from previously contacted/closed companies;
3. create a run manifest;
4. run separate remote/visa searches unless current YC connector behavior has been re-verified;
5. preserve full JDs and founder/contact identifiers;
6. validate the search artifact;
7. enrich and return contacts to the same YC session;
8. draft and review; send only after Bhaskar manually approves and sends;
9. reconcile Gmail evidence.

No new real search run was created as part of this VAULT documentation update.

## Source of truth

This file is a VAULT project handoff. The private JOBS repository, its current tracker, dated run artifacts and Gmail evidence remain authoritative for operational state.
