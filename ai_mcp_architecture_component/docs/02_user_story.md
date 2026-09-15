# 02 — User Story

Method step: Design Thinking discovery → **formalized requirement**, before
any technology is named. No "MCP" appears anywhere on this page on purpose.

---

## In plain words, first — what is a "persona" and a "User Story"?

Skip this box if these terms are already familiar.

**Persona** = a stand-in for "the person this is actually for," given a
name so every decision can be checked against a real situation instead of
an abstract "the user." It is not a real, named individual (see the note
in `docs/01_discovery.md`) — it's a compact, realistic sketch: role, daily
task, one recurring frustration.

Toy example to make the mechanism click, nothing to do with this repo:

> **Tom** is a customer support agent. He answers 40 emails a day. His
> one recurring frustration: he has to look up the current refund policy
> wording every time, because it changes and he can't trust his memory.
> **Maureen** is his team lead. Her frustration: when Tom misquotes the
> policy, the ticket escalates to her.
>
> A **User Story** turns one persona's frustration into one sentence with
> three parts — who, what, why:
> **As** Tom, support agent, **I want** the current refund wording pulled
> up automatically when I open a ticket, **so that** I never misquote it
> and Maureen never sees that ticket again.

That's the whole mechanism. Everything below does the same thing for this
POC's real persona (Amira, `docs/01_discovery.md`) instead of the toy Tom
example. This POC deliberately uses **one** persona, not two like the Tom/
Maureen example — Amira's frustration is enough to justify the whole
build; a second persona would be padding, not rigor.

---

## User Story

> **As** a multilingual newsroom editor,
> **I want** any AI assistant I'm using to instantly check a term or
> phrase against our house style guide,
> **So that** I don't publish inconsistent terminology across languages,
> and I don't have to interrupt my work to search a spreadsheet or ask a
> colleague.

## Acceptance criteria (Gherkin)

```gherkin
Feature: Terminology and style lookup from any AI assistant

  Scenario: Editor checks a known term
    Given the house style guide contains an entry for "Sud-Liban"
    When an AI assistant looks up "Sud-Liban" for the French->English pair
    Then it returns the approved English rendering and any usage note
    And the response includes the source entry's last-updated date

  Scenario: Editor checks an unknown term
    Given the house style guide has no entry for the requested term
    When an AI assistant looks up that term
    Then it returns a clear "not found" result, not a guess
    And it suggests the closest known entries if any exist

  Scenario: A second, unrelated AI client reaches the same data
    Given the style guide is already exposed to one AI client
    When a second, independently-built AI client requests the same lookup
    Then it succeeds without any new integration code being written
    And this is the acceptance criterion that actually separates a REST-only
    solution from an MCP-based one — see docs/04_recommendation.md
```

## Out of scope for this POC

- Authentication/authorization beyond a placeholder (a real deployment
  would need it — noted, not built, to keep the POC focused on the
  integration-cost argument).
- Multi-language *generation* (translation itself) — this POC is about
  *lookup/consistency*, not machine translation, which DENIA already
  covers via NLLB in production.
- A production-grade style-guide editing UI — the dataset is a static
  JSON file for this demonstration (`src/data/newsroom_style_guide.json`).

