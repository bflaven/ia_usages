# 07 — Worked Example: A Journalist's Draft, Before/After

This is the "stop showing me theory" version of this POC: a rough draft
with real errors, corrected live through the MCP server — not a lookup
demo with a single clean term, an actual editing pass.

Run it:

```bash
conda activate mcp_architecture_component
cd /path/to/this/repo
python -m src.demo_journalist_workflow
```

---

## Where the draft text comes from — and what it doesn't reproduce

The scenario is inspired by France24's 2026-09-14 report, *"Zelensky says
Ukraine ready to de-escalate if Russia halts strikes"*
(`https://www.france24.com/en/europe/20260914-zelensky-says-ukraine-ready-to-de-escalate-if-russia-halts-strikes`).
The factual core (Zelensky's offer to halt strikes on Russian energy
infrastructure if Russia reciprocates) is paraphrased from that reporting.

**Important**: that article does not actually name any Ukrainian city in
connection with strikes — the real strikes it reports were near the
Polish and Moldovan borders. Every Ukrainian city name in the draft below
(Kiev, Kharkov, Odessa, Dnepropetrovsk, Lvov) is an **original addition**
for this demo, not something misquoted from the source. This is
deliberate: it keeps the demo honest about what came from the article
(one sentence of paraphrased fact) versus what was invented to exercise
the style-guide tool (the place names, on purpose spelled the old,
Russian-derived way).

## The draft (as filed, before house-style check)

> President Volodymyr Zelensky said Ukraine is ready to halt strikes on
> Russian energy infrastructure if Moscow does the same, calling it a
> possible de-escalatory step. He added that Russia has so far shown no
> genuine will to end the war. Away from the frontline diplomacy, wire
> desks noted the toll on Ukraine's rail network: recent weeks have seen
> drone strikes near border crossings, with disruption felt as far as
> **Kiev, Kharkov and Odessa**. Editors compiling the daily brief also
> flagged fresh reporting out of **Dnepropetrovsk and Lvov**, where local
> officials described damage to power substations.

Five intentional errors, bolded above — all pre-2022/pre-2016 Russian- or
Soviet-derived spellings that this newsroom's house style now rejects.

## What the MCP tool call catches

One call, `check_style_rule(text=DRAFT)`, against the live
`newsroom-style-guide` server, returns all five hits with the approved
rendering and the *why*:

| Draft said | House style says | Why |
|---|---|---|
| Kiev | Kyiv | Ukrainian transliteration, house policy since 2022 |
| Kharkov | Kharkiv | Ukrainian transliteration |
| Odessa | Odesa | Single 's' in the Ukrainian spelling |
| Dnepropetrovsk | Dnipro | Post-2016 decommunization rename |
| Lvov | Lviv | Ukrainian transliteration |

## Corrected (ready to file)

> President Volodymyr Zelensky said Ukraine is ready to halt strikes on
> Russian energy infrastructure if Moscow does the same, calling it a
> possible de-escalatory step. He added that Russia has so far shown no
> genuine will to end the war. Away from the frontline diplomacy, wire
> desks noted the toll on Ukraine's rail network: recent weeks have seen
> drone strikes near border crossings, with disruption felt as far as
> **Kyiv, Kharkiv and Odesa**. Editors compiling the daily brief also
> flagged fresh reporting out of **Dnipro and Lviv**, where local
> officials described damage to power substations.

## The point of this file

`src/demo_journalist_workflow.py` calls the exact same `check_style_rule`
MCP tool that Claude Desktop, Claude Code, or any future in-house AI tool
would call — no code specific to this demo script talks to
`style_guide.py` directly. This is `docs/02_user_story.md`'s third
acceptance criterion, applied to an actual editing task instead of a
single-term lookup: a second, independent way of using the same data,
zero new integration code.

Try it live in an actual client, not just the terminal script: open
Claude Desktop (see `docs/05_modop.md` Quick Start / STEP 7) and paste this
exact prompt, draft included, as-is:

```text
Using newsroom-style-guide, check this draft for house-style issues and give me the corrected version:

President Volodymyr Zelensky said Ukraine is ready to halt strikes on Russian energy infrastructure if Moscow does the same, calling it a possible de-escalatory step. He added that Russia has so far shown no genuine will to end the war. Away from the frontline diplomacy, wire desks noted the toll on Ukraine's rail network: recent weeks have seen drone strikes near border crossings, with disruption felt as far as Kiev, Kharkov and Odessa. Editors compiling the daily brief also flagged fresh reporting out of Dnepropetrovsk and Lvov, where local officials described damage to power substations.
```

Expect: a visible `check_style_rule` tool-call step, then all 5 catches
(Kiev→Kyiv, Kharkov→Kharkiv, Odessa→Odesa, Dnepropetrovsk→Dnipro,
Lvov→Lviv) each with its house-style note, plus the corrected paragraph.
