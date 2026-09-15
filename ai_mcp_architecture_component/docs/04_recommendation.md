# 04 — Recommendation: build vs. buy vs. protocol

Method step: **Scrum-ready decision** — same discipline as the build-vs-buy
9-point grid used on the Procurement RAG POC: options laid out, scored,
decided, before a single sprint is planned.

---

## Options considered

| Option | Description | Verdict |
|---|---|---|
| **A. Do nothing** | Keep the spreadsheet, keep asking colleagues | Fails the user story outright — see `docs/02_user_story.md` acceptance criteria. Rejected. |
| **B. One bespoke REST endpoint per AI client** | `src/legacy_api.py` — clean, simple, works for exactly one client | Solves the *first* client's problem. Recreates the integration cost identically for every *next* client (N×M). Deployment-speed KPI (`docs/03_kpis.md`) stays bad by construction. Rejected as the long-term answer, **kept in the repo as the control group**, not deleted. |
| **C. Model Context Protocol server** | `src/mcp_server.py` — one server, standard tool/resource contract, any MCP-compatible client connects without new integration code | Directly satisfies the third acceptance criterion in the user story (a second, independent client reaching the data with zero new integration code) and fixes the deployment-speed KPI. **Chosen.** |

## Why MCP, specifically (not "AI for its own sake")

This is the point worth being explicit about, including in an interview:
**MCP was not chosen because it's a trending acronym.** It was chosen
because option B fails a measured KPI (deployment speed) that option C
fixes, for a real, qualified, measured pain point (`docs/01_discovery.md`).
If the numbers in `docs/03_kpis.md` had come out the other way — if there
was only ever going to be one client, forever — option B would have been
the right call, and building an MCP server would have been technical debt
dressed up as innovation.

The product reasoning comes first. The protocol is the conclusion, not the
premise.

## Governance note (carried over from DENIA practice)

MCP's tool/resource contract also gives a structural place to enforce
"who is allowed to call what" — the same instinct behind DENIA's
multi-department validation gate before production release. This POC
doesn't implement auth (explicitly out of scope, see `docs/02_user_story.md`),
but the `MCPServer` constructor's `auth`/`token_verifier` parameters are
exactly where that governance would attach in a real deployment — noted
here so the architecture story is honest about what's demonstrated vs.
what's a known next step.

## Bottom line

> We didn't pick MCP because it's new. We picked it because it's the only
> option of the three that keeps the deployment-speed KPI from getting
> worse every time a new AI client shows up — and we could name that KPI,
> and measure it, before writing a line of server code.
