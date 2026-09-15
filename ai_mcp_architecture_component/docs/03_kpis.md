# 03 — KPIs

Method step: **Lean** — value/effort scoring before committing to a build.
KPI framework kept identical to the four blocks used across this author's
other product work, for consistency across everything he publishes:

- Adoption/usage
- Operational efficiency
- Quality/reliability
- Deployment speed

No new taxonomy invented for this POC — the point is that the same KPI
discipline applies whether the deliverable is a newsroom product (DENIA) or
a technical-architecture choice (this POC).

---

## Adoption / usage

| Metric | Target for this POC |
|---|---|
| Number of distinct AI clients able to query the style guide **without new integration code** | ≥ 2, proven by `src/client_demo.py` acting as an independent second client alongside the FastAPI/legacy caller |
| Lookup calls served | Every call logged with term + result (found/not found) for later adoption analysis |

## Operational efficiency

| Metric | Before (manual) | After (this POC) |
|---|---|---|
| Time to check one term's house style | ~2-4 min (search spreadsheet / ask a colleague, per discovery interview) | Sub-second tool call |
| Time to resolve a "not found" case | Same 2-4 min, often with no resolution | Instant structured "not found" + closest-match suggestion |

## Quality / reliability

| Metric | Target |
|---|---|
| Automated test coverage on lookup logic | Covered by `tests/test_mcp_server.py` (found / not-found / fuzzy-suggestion paths) |
| Consistent behavior across clients | Same underlying data source (`newsroom_style_guide.json`) served to both the legacy REST endpoint and the MCP tool — no drift between "what REST says" and "what MCP says" by construction |

## Deployment speed

This is the sharpest number in the whole POC, and the actual argument for
choosing MCP over a bespoke integration — see `docs/04_recommendation.md`
for the full reasoning:

| Metric | Legacy REST pattern | MCP pattern |
|---|---|---|
| Effort to onboard a **new** AI client onto this data source | A new bespoke integration per client (custom auth, custom response parsing, custom error handling) — realistically days of dev work per client, the same shape of cost as any N×M integration problem | Point the new client at one config entry (server address/command); the tool/resource contract is already standard | 

**This table is the whole point of the POC.** Everything else
(discovery, user story, code) exists to make this row defensible instead of
asserted.
