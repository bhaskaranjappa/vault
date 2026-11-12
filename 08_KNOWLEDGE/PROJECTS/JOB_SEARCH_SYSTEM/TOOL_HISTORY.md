# JOBS — Tool History and Evaluation

**Evidence basis:** user-provided session summaries and the private JOBS repository as of 2026-11-12. This is historical project knowledge, not a fresh audit of local installations.

## Core tools

| Tool | Intended role | Historical evidence / disposition |
|---|---|---|
| Selected LLMs (ChatGPT, Claude, Gemini, DeepSeek and others) | Plan search prompts, review job evidence and prepare task instructions | Used as reasoning/planning layer; model selection remains with Bhaskar |
| YC / Work at a Startup agent and MCP connectors | Search roles, retain full JDs and draft after enrichment | Core discovery and JD-context layer; historical MCP names include `workatastartup-mcp` and `yc-mcp-connector` |
| Agent-Reach | Public-web discovery and evidence gathering across company pages, YC launches, GitHub and supported sources | Historical test reported 25/25 contact/domain discoveries; dated result, not a permanent guarantee |
| Apollo.io / Apollo MCP | People and contact enrichment | API/MCP use reported; Apollo web scraping was blocked (HTTP 410/Cloudflare in prior test). Apollo-generated guessed confidence percentages were treated as unverified |
| Prospector MCP | Domain checks, email discovery and mailbox verification | Reported connected in Antigravity, OpenCode and ZCode. Tools included `usage_stats`, `check_domain`, `verify_email`, `verify_emails_batch`, `find_emails` |
| Scrapling | Browser-backed extraction from public pages where automation is permitted | Rendered LinkedIn in a prior test but did not extract emails; LinkedIn must not be scraped or automated |
| Gmail | Manual communication and evidence of sent, bounced and replied messages | Human sends; actual thread is authoritative |

## Prospector `find_emails` evidence reconciliation

A historical note said `find_emails` had never been called. Later repository artifacts contradicted that:
- The November 9 enrichment CSV recorded a Prospector `mcp_find_emails` call for FirstWork, with 24 credits and a reported SMTP score of 95.
- The November 5 findings CSV recorded a Guac `find_emails` pattern-inference result using 1 credit; that result was explicitly not mailbox verification.

The private JOBS `MEMORY.md` records the current classification as historical output evidence; original MCP logs and live `usage_stats` were not inspected in the ChatGPT session. A repeat test against GetCrux was considered unnecessary because that contact was already present in the sent-outreach tracker.

## Other tools and decisions

- **OpenOutreach:** installed in Freebuff with skills, but `send`/`run` remain disabled. A bounded Apollo comparison was proposed; completion was not established in supplied summaries.
- **Firecrawl:** dropped after Apollo/LinkedIn tests did not solve the problem.
- **Coldreach:** dropped after DNS/time-out failures.
- **mcpman:** installed but did not support the user's coding agents; abandoned.
- **mcpsmgr:** upgrade from 0.3.0 to 0.4.9 failed; abandoned in favor of manual runtime-specific configuration.
- **Freebuff MCP bridge:** abandoned because Freebuff web could not reach localhost MCP servers.
- **Local 14B CPU models:** dropped for multi-step agent loops; historical estimates were roughly 5–15 tokens/sec with long sequential loops.
- **Candidate-side WaaS MCP:** rejected because application-side features did not fit the enrichment workflow and required persisted signed-in browser state.
- **Recruiter-side `yc-software/waas-mcp`:** explicitly excluded as the wrong product side.
- **Agency Agents:** 14 selected specialist agents were installed across coding-agent environments; source summaries distinguish file presence from runtime invocation verification.

## Browser candidates studied later

The user investigated Camoufox, Camofox Browser, CloakBrowser, Wolfbrowser, Stealth Browser MCP and a Ghost Browser name. The private JOBS repository contains the detailed point-in-time comparison. None is approved for bypassing Apollo or LinkedIn access restrictions.

## Runtime matrix (historical)

- Antigravity: Prospector MCP reported connected.
- OpenCode: Prospector MCP reported connected.
- ZCode: Prospector MCP reported connected.
- Freebuff web: could not reach localhost MCP in tested configuration.
- DeepSeek Harness: no compatible MCP server configuration was found in the recorded test.

These statuses are historical and must be rechecked before installs or configuration changes.

## Tool lifecycle rule

Report separately: `SUPPORTED → INSTALLED → ENABLED → CONFIGURED → AUTHENTICATED → VERIFIED`. Installed does not mean working. The private JOBS `integrations/TOOL_REGISTRY.md` is the detailed operational record.
