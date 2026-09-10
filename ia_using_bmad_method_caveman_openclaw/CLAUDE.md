# CLAUDE.md — how this post gets written

This file documents the actual workflow used to turn three directories of raw, messy exploration notes into a published blog post with Claude Code. Read it if you want to run the same process again on a different set of tools/directories.

## Starting materials

- One directory per tool explored (e.g. `_ia_using_bmad_method/`, `_ia_using_caveman/`, `_ia_using_openclaw/`), each containing a `_*.diff` file — a running, unedited log of every command, error, half-formed thought, and personal tangent from actually using the tool. Called the "monster file."
- A model post (`_MODEL_*.html`) — an existing published post, used as the style and structure anchor: first-person, self-aware, mixes philosophical digression with concrete how-to, credits sources with real links, no corporate tone.
- A model thumbnail image (`_MODEL_*.jpg`) — the visual style anchor.
- A `_prompts/` directory to keep every prompt used in this project, numbered.

## Step 1 — read everything before writing anything

Read every `_*.diff` file in full, plus the model post and any existing draft. Do not skim. The monster files contain the actual argument the user wants to make, buried in typos, half-French, and dead ends — the job in step 2 is to find that argument, not to invent a new one.

## Step 2 — draft the post as a single narrative, not a tool-by-tool summary

The failure mode is writing three disconnected "how to install X" sections. The fix: find one thesis that threads through all three tools, state it explicitly early in the post, then show how each tool answers a different part of it. In this project the thesis is: *AI makes execution nearly free, so ideation/judgment becomes the scarce resource — and each tool sits at a different point of that triangle.*

Keep the model post's voice: first person, willing to be self-deprecating, real anecdotes kept (not sanitized into corporate case studies), credits and sources as real links, personal opinions clearly flagged as opinions.

Iterate by writing a new numbered file each round (`ia_using_..._2.html`, `_3.html`, ...) rather than overwriting — the user reviews and requests changes, never assume a single pass is final. Put `<!-- TITLE: -->` and `<!-- KWS: -->` HTML comments at the top of the file once a title/keyword list exists, so they travel with the draft.

## Step 3 — fact-check anything time-sensitive before publishing it

If the draft makes a claim about a fast-moving situation (a company policy change, a hire, a platform restriction), do not ship it as a hedge ("my suspicion is...") without checking first. Use WebSearch/WebFetch, get primary sources (TechCrunch, Bloomberg, the vendor's own docs/changelog — not just an AI-generated search summary, which can hallucinate dates), and replace the hedge with dated, sourced, named facts. Keep the inline links in the final HTML.

## Step 4 — privacy pass before anything gets published or pushed

Before treating a draft as postable, or before turning raw notes into a public-facing readme:

- `grep -rniE "realname|/Users/|employer_name|email@"` across every file that will ship.
- Confirm no absolute home-directory paths remain in shareable files (readmes especially) — genericize to `/Users/username/your-directory/`.
- Confirm personal `.diff` monster files and any `.claude/` session config are excluded via `.gitignore`, not just "forgotten to add."
- Personal anecdotes the user chose to include (family, opinions, past jobs) are not a privacy problem by default — the check is for *leaked identifiers*, not for removing voice.

## Step 5 — turn each tool's monster file into a public readme

One `readme.md` per tool directory, English only, structured (install steps, commands, vocabulary, gotchas, sources), stripped of anything from the privacy pass. End each with a short "Visual identity note" quoting the user's own words about how they picture that tool visually — useful later for step 6, and it documents intent for anyone reading the repo.

## Step 6 — thumbnail

1. Check the target site's actual existing style before designing anything (navigate to it, look at real published thumbnails) — do not assume; the user will tell you if a hand-coded guess is "ugly."
2. Prefer AI image generation over hand-coded SVG once the user asks for it — hand-drawn SVG shapes are slow to get right and easy to get wrong (a described "club" can render as something unfortunate; iterate visually, screenshot after every edit, before shipping).
3. When generating via a chat-based image tool (e.g. grok.com through claude-in-chrome):
   - One prompt per subject, no baked-in text/labels (text inside AI-generated images is usually garbled) — composite labels afterward instead.
   - Strip trademarked character names from prompts (e.g. "Alfred E. Neuman," "Fred Flintstone") — describe visual traits instead, to dodge both generation refusals and IP risk.
   - Save every raw generated image locally and separately, unedited, before doing anything else with it — the user may want to inspect or edit them by hand rather than trust a composite.
   - To fetch a generated image, don't rely on a plain `curl` on the asset URL — grok.com's asset URLs are session/cookie-gated and return empty to an unauthenticated request. Instead, navigate a browser tab directly to the asset URL (the tab's existing cookies authenticate it) and screenshot/crop that tab.
   - Watch for silent quota limits: a free/fast tier may generate the first image fine and then silently return no image (no error banner) on subsequent attempts in the same session. If several varied prompts all produce a caption with no attached image, suspect quota exhaustion before suspecting the prompt wording — check whether the tool's dedicated generation surface (e.g. `grok.com/imagine`) throws an explicit paywall; if so, that confirms it.
4. Age-verification or other account-identity dialogs encountered mid-task are not something to fill in by guessing — ask the user for the actual value.

## Step 7 — companion copy (LinkedIn, etc.)

Match the same voice as the post, not generic marketing copy. If the user has a stated allergy to a genre (e.g. clickbait listicles), the teaser's whole job is to be legibly *not* that genre while still hooking a reader — usually by leading with genuinely surprising, real specifics (named people, dated events) rather than a promised verdict. Version this as its own incrementing file, same pattern as the post.

## Step 8 — keep a changelog

Maintain a `readme.md` at the project root logging what changed at each iteration and why (not just "v3" but "v3: reframed X because Y"). This is what makes the process reproducible and lets the user audit editorial decisions later without re-reading every draft in full.

## Things that went wrong once, worth not repeating

- Assuming a colorful flat-icon style would read as "modern/cheerful" — the user's actual site uses monochrome black silhouettes; check before designing.
- Drawing a "club" as a plain tapered capsule shape without contextualizing it as held by a figure — reads as anatomically unfortunate rather than as a weapon. Attach it to a hand, or make the head/handle width ratio obviously tool-like.
- Trying to `curl` an authenticated asset URL directly instead of going through the authenticated browser tab.
- Retrying a failing image prompt many times with wording tweaks before checking whether the actual cause was a quota/paywall rather than the prompt itself — check the tool's own upgrade/paywall surface early once 2+ varied attempts fail identically.
