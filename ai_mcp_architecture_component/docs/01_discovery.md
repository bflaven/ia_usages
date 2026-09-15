# 01 — Discovery: stakeholder interview & use case capture

Method step: **Design Thinking (discovery)** → feeds the use case capture
loop **qualify → measure → adjudicate → adopt**.

> **Note on the persona**: "Amira" below is an explicitly-labeled composite
> persona, built from patterns common to multilingual newsroom work (the
> kind of pain point observed across newsroom/production teams handling
> content in 15+ languages), not a real named individual. This keeps the
> discovery step honest as a method demonstration without pretending to
> quote someone who doesn't exist.

---

## Stakeholder interview (composite persona)

**Persona**: Amira, senior editor/translator at a multilingual news outlet.
Works daily across 4-5 language pairs, handling place names, institution
names, and house-style phrasing that must stay consistent across every
language version of a story.

**Interview notes (synthesized)**

- *"Every outlet has a style guide. Nobody reads it under deadline."*
- *"I know Claude / [AI assistant] can help me draft or translate faster,
  but every time I ask it to check our house terminology, it doesn't know
  it — I have to paste the relevant spreadsheet row myself, every time."*
- *"If a new AI tool gets rolled out next quarter, IT will need weeks to
  wire it into our terminology database. That's the pattern every time —
  new tool, new bespoke integration, same data."*
- *"What I actually want: whatever AI tool I'm using that day, ask it a
  term, get the house-style answer. I don't want to think about which
  system holds the data."*

**Pain point, qualified**: terminology/style consistency work is manual,
repeated, and re-integrated from scratch for every new AI tool — not a
data problem (the style guide exists), an **integration** problem.

---

## Use case capture: qualify → measure → adjudicate → adopt

| Step | What it means here | Outcome |
|---|---|---|
| **Qualify** | Is this a real, recurring pain point, not a one-off request? | Yes — confirmed across every language pair, every new AI tool rollout (see interview notes). Not a stage/alternance-level triviality; a structural integration cost. |
| **Measure** | Size the pain in time/cost before proposing a fix | See `docs/03_kpis.md` — manual lookup time, integration lead time per new client. |
| **Adjudicate** | Is this worth solving now, and how (build vs buy vs protocol)? | See `docs/04_recommendation.md` — three options compared on a decision grid, same discipline as the POC RAG Procurement build-vs-buy grid this method is drawn from. |
| **Adopt** | Ship it, make it usable by real clients, prove adoption is trivial for the *next* client too | `src/client_demo.py` proves a second, independent client (not just the original REST caller) can reach the same data with zero new integration code — the actual test of "adopt" for this use case. |

This is the same four-step discipline used elsewhere in this author's
product work (cf. `fiche_memo_condensee.md`): *qualify, measure, adjudicate,
adopt* — applied here to a technical-architecture decision instead of a
business use case, on purpose, to demonstrate that the method doesn't
change depending on where in the pipeline you're standing.
