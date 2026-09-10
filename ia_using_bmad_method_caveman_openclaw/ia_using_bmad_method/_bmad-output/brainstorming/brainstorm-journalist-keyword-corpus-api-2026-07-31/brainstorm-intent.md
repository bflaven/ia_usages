# Brainstorm Intent: Journalist Keyword Corpus API

## Context
Web app for journalists to enrich a keyword list for a local corpus. Corpus exports to JSON feeding an API. Goal: share a consolidated corpus across French media outlets via that API endpoint.

## Core Direction
Build a **trust/reputation system** as the core unifying primitive of the product — not a bolt-on feature. It is simultaneously:
- The moat vs. free/open-source clones (uncloneable asset = editorial reputation + trusted journalist network, not the software itself).
- The auto-approve/auto-flag engine for keyword submissions when no human editor is available.
- The basis for tiered moderation once the network scales (algorithm handles the bulk; humans review only edge cases). This is required because per-keyword editor-consensus review breaks down at scale (~100 outlets) — it does not survive past small-network size.
- Scored at two levels with the same mechanism: keyword-level (trust score per keyword/submission) and outlet-level (a minimum monthly contribution quota per outlet, to measure involvement and deter free-riders).

## Signal Plumbing (feeds the reputation engine)
Bidirectional, real-time entanglement between local corpus and API export:
- A local flag on a keyword instantly blocks/removes it from the API export.
- Outlet-side usage/click data on exported keywords feeds back as a review/trust signal on the local corpus.

## Governance Model: Two-Speed
Resolves the tension between wanting fast automated trust/moderation action and wanting governance stability:
- **Fast layer (continuous/automated):** keyword-level trust scoring, auto-approve/flag, day-to-day moderation.
- **Slow layer (annual):** a governance board sets policy and quota rules (e.g., outlet contribution quotas) once a year; not touched mid-cycle.

## Adoption Hook (why journalists will actually use it)
Root cause of predicted adoption failure: enrichment work has no visible payoff for the journalist doing it. Fix: surface instant value immediately after enrichment — related-story keyword suggestions generated right after a journalist enriches an entry. This is the feature that earns initial usage; the reputation engine is the retention/scale mechanism underneath it.

## Editorial Governance Layer (dispute handling)
- Disputes resolved by a neutral third party with final say, grounded in published editorial standards.
- Full version history retained for keyword edits (audit trail / accountability), independent of the automated trust score.

## Build Sequence (priority order)
1. Reputation/trust engine as core primitive — keyword-level scoring + outlet-level scoring.
2. Instant-payoff feature (related-story suggestions) as the adoption hook.
3. Neutral-third-party dispute resolution + version history as the editorial governance layer on top.
