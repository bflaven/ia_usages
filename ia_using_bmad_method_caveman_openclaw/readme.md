# ia_using_bmad_method_caveman_openclaw

Blog post project: one post covering three AI tools (BMad Method, Caveman, OpenClaw), built from raw exploration notes per tool. See `CLAUDE.md` in this same directory for the full reproducible workflow.

## Layout

```
_ia_using_bmad_method/                 raw notes + readme.md for BMad Method
_ia_using_caveman/                     raw notes + readme.md for Caveman
_ia_using_openclaw/                    raw notes + readme.md for OpenClaw
_prompts/                              prompt history for this project (chat prompts, image prompts)
grok_thumbnail_assets/                 raw images generated via grok.com, one per prompt, unedited
_MODEL_ia_augmented_journalist_wp_toolkit_10.html   model/reference post (style + structure anchor)
_MODEL_ia_managing_prompts_b.jpg       model/reference thumbnail image
ia_using_bmad_method_caveman_openclaw_N.html        post draft, incremented per editorial iteration
ia_using_bmad_method_caveman_openclaw_thumbnail.jpg current thumbnail candidate
linkedin_ia_using_bmad_method_caveman_openclaw_N.md LinkedIn teaser copy, incremented per iteration
.gitignore                             excludes *.diff (raw personal notes) and .claude/ (session config)
```

`*.diff` files inside each tool directory are personal working notes ("monster files") — excluded from git via `.gitignore`, never published. Each tool directory's `readme.md` is the cleaned-up, English, shareable version of the same material, meant to ship alongside the post's GitHub repo (`github.com/bflaven/ia_usages`).

## Thumbnail prompts (Grok / grok.com)

Trademarked characters (Alfred E. Neuman, Fred Flintstone, Captain Caveman) are deliberately described by visual traits rather than named, to avoid IP issues and generation refusals. Full history in `_prompts/002_grok_thumbnail_prompts.md`.

**1 — BMAD METHOD (grin icon)** — succeeded first try, saved as `grok_thumbnail_assets/01_bmad_grin.png`.
```
Flat minimalist icon illustration, bold black shape on a pure white background, editorial blog style, no gradients, no shadows, no text or letters anywhere in the image. A single round cartoon face with a big mischievous gap-toothed grin, wide simple eyes, one eyebrow raised, ears sticking out slightly, freckles optional — playful and impish rather than angry, evoking a classic satirical-magazine mascot vibe without copying any specific character. Solid black silhouette style with a couple of white cutout details (eyes, teeth gap), high contrast, clean vector look, centered composition, plenty of white margin around the subject, square-ish crop.
```

**2 — CAVEMAN (club icon)** — 4 attempts, all silently returned no image (see changelog). Not yet obtained from Grok.
```
Flat minimalist icon illustration, bold black silhouette on a pure white background, editorial blog style, no gradients, no shadows, no text or letters anywhere in the image. A stocky, cartoonish prehistoric caveman figure, standing, wearing a single-shoulder-strap fur tunic, spiky messy hair, one arm raised overhead swinging a wooden club with a heavy round head — energetic, mid-swing pose, confident and a bit goofy, like a classic Stone-Age cartoon character (but an original generic design, not a copy of any specific existing character). Solid black silhouette, clean vector look, centered composition, plenty of white margin around the subject, square-ish crop.
```

**3 — OPENCLAW (claw icon)** — 1 attempt, silently returned no image (see changelog). Not yet obtained from Grok.
```
Flat minimalist icon illustration, bold black silhouette on a pure white background, editorial blog style, no gradients, no shadows, no text or letters anywhere in the image. A single open lobster claw / pincer, viewed from the side, clearly showing two pincer tips slightly apart as if open and ready to snap, thick and chunky proportions, cartoon-graphic rather than realistic. Solid black silhouette, clean vector look, centered composition, plenty of white margin around the subject, square-ish crop.
```

**4 — Combined, one-shot fallback** — not attempted yet.
```
Flat minimalist blog-header illustration, bold black silhouettes on a pure white background, editorial style, no gradients, no shadows, no text or letters or words anywhere in the image. Three separate simple icons evenly spaced left to right on one wide horizontal canvas (16:9): (1) a round cartoon face with a big mischievous gap-toothed grin and one raised eyebrow; (2) a stocky cartoon prehistoric caveman in a fur tunic, mid-swing with a club raised overhead; (3) a single open lobster claw / pincer shown from the side. Each icon is a clean solid black silhouette, same visual weight and style, generous white space between and around them, nothing overlapping, nothing photorealistic, no background scenery, no color.
```

## Thumbnail prompts (Mistral / chat.mistral.ai — Robert Crumb style, v1)

Switched to Mistral's Le Chat after Grok's free quota ran out. Tool used: Chat tab → `+` → Outils → "Génération d'images" enabled. Raw outputs saved unedited in `mistral_thumbnail_assets/`.

**1 — BMAD METHOD** — succeeded first try, `mistral_thumbnail_assets/01_bmad_grin_crumb.png`.
```
Robert Crumb-inspired underground comix ink illustration: dense scratchy cross-hatching, imperfect wobbly hand-drawn linework, high-contrast black ink, rough textured pen strokes, no digital-smooth vector look, no modern flat illustration, no futuristic or sci-fi style. Transparent background, isolated illustration only, no text, no lettering, no watermark, no color, black ink linework only. Subject: a single grinning, gap-toothed, mischievous cartoon face, wide bulging eyes, one eyebrow cocked, big jug ears, exaggerated grotesque Crumb-style proportions, rendered as a standalone mask-like object, not a full body.
```

**2 — CAVEMAN** — succeeded first try, `mistral_thumbnail_assets/02_caveman_club_crumb.png`.
```
Robert Crumb-inspired underground comix ink illustration: dense scratchy cross-hatching, imperfect wobbly hand-drawn linework, high-contrast black ink, rough textured pen strokes, no digital-smooth vector look, no modern flat illustration, no futuristic or sci-fi style. Transparent background, isolated illustration only, no text, no lettering, no watermark, no color, black ink linework only. Subject: a grotesque stocky prehistoric caveman character, wild scruffy hair, ragged fur pelt draped over one shoulder, exaggerated Crumb-style bulbous nose and grinning expression, gripping a heavy knobby wooden club resting on his shoulder, thick hairy limbs, standing pose, full figure.
```

**3 — OPENCLAW** — succeeded first try but weak result (reads as a curled shrimp/worm, not a clear two-fingered pincer), `mistral_thumbnail_assets/03_openclaw_pincer_crumb.png`.
```
Robert Crumb-inspired underground comix ink illustration: dense scratchy cross-hatching, imperfect wobbly hand-drawn linework, high-contrast black ink, rough textured pen strokes, no digital-smooth vector look, no modern flat illustration, no futuristic or sci-fi style. Transparent background, isolated illustration only, no text, no lettering, no watermark, no color, black ink linework only. Subject: a single large open lobster claw / pincer, isolated object viewed from the side, jagged rough shell texture with cross-hatched shading, two pincer tips slightly apart as if snapping, grotesque exaggerated Crumb-style linework, no body, no other body parts, just the claw.
```

## Thumbnail prompts (Mistral — Keith Haring blend, v2, friendlier/less scary)

Requested revision: same three subjects, but blended toward Keith Haring's bold, cheerful, thick-outline pop-art style instead of full Crumb grotesquerie — especially for BMAD METHOD and OPENCLAW. Target output: `mistral_thumbnail_assets/v2/01_bmad_grin_crumb.png`, `02_caveman_club_crumb.png`, `03_openclaw_pincer_crumb.png`. **Not yet generated — Mistral's free image-generation quota was already exhausted (`Quota de génération d'images dépassé`) on the first attempt of this batch.**

**1 — BMAD METHOD** — generated via ChatGPT (chatgpt.com), succeeded first try. Saved: `mistral_thumbnail_assets/v2/01_bmad_grin_crumb.png`.
```
Bold pop-art illustration mixing Keith Haring's style (thick uniform black outlines, simple flat shapes, energetic playful pose, minimal cheerful facial features, no shading, no cross-hatching) with a touch of loose hand-drawn underground-comix confidence, but friendly and NOT scary or grotesque. Transparent background, isolated illustration only, no text, no lettering, no watermark, no color, black outline only. Subject: a simple round friendly cartoon face, big warm closed-eye smile or gentle open eyes, no menacing expression, no bulging eyes, no sharp teeth, rendered as a cheerful standalone mask-like icon.
```

**2 — CAVEMAN** — generated via ChatGPT, succeeded first try, strongest result of the three. Saved: `mistral_thumbnail_assets/v2/02_caveman_club_crumb.png`.
```
Bold pop-art illustration mixing Keith Haring's style (thick uniform black outlines, simple flat shapes, energetic dynamic dancing-like pose, no shading, no cross-hatching) with a touch of loose hand-drawn underground-comix looseness, but friendly and NOT scary or grotesque. Transparent background, isolated illustration only, no text, no lettering, no watermark, no color, black outline only. Subject: a stocky cheerful prehistoric caveman character in a bouncy triumphant Haring-style pose, simple minimal fur texture (a few short lines, not dense hatching), simple round friendly face with a big open smile, holding a simple round-headed club raised playfully overhead, full figure, dynamic and joyful, not menacing.
```

**3 — OPENCLAW** — generated via ChatGPT, succeeded first try, clear improvement over the v1 Crumb attempt (now reads as a real jagged-tooth pincer). Saved: `mistral_thumbnail_assets/v2/03_openclaw_pincer_crumb.png`.
```
Bold pop-art illustration mixing Keith Haring's style (thick uniform black outlines, simple flat rounded shapes, no shading, no cross-hatching) with a touch of loose hand-drawn underground-comix looseness, but friendly and NOT scary or grotesque. Transparent background, isolated illustration only, no text, no lettering, no watermark, no color, black outline only. Subject: a single, simple, rounded lobster claw/pincer shape, clearly showing two open pincer fingers, smooth bold clean outline, cute and friendly rather than jagged or menacing, isolated object, no body.
```

## Changelog

- **v1** (`ia_using_bmad_method_caveman_openclaw_1.html`) — empty WordPress template, no content yet.
- **v2** — first full draft. Opening philosophical frame (liquid modernity / Bauman, Arthur Mensch "compressed intelligence," Terminator T-800 vs T-1000), one section per tool, closing synthesis tying back to the son's question.
- **v3** — restructured around an explicit thesis (AI makes execution cheap, ideation becomes the scarce resource) stated up front; BMad reframed as feeding Anthropic's engagement/token consumption rather than competing with it; OpenClaw reframed around claude-in-chrome as the lived alternative, plus a hedge about platform lock-in; Caveman reframed with a callback to the opening liquidation fear (compressing human expression for a machine's convenience). TITLE/KWS HTML comments added.
- **v4** — replaced the OpenClaw hedge with confirmed, dated, sourced facts: Feb 15 2026 OpenAI hires Peter Steinberger (OpenClaw creator), Feb 20 Anthropic bans OAuth token use in third-party tools, Feb 22 Google restricts Gemini access via OpenClaw, Apr 4 Anthropic technical cutoff + Apr 10 brief account suspension. Sources inline-linked (TechCrunch, Bloomberg, Forbes, Implicator.ai, Winbuzzer).
- **Privacy pass** — grepped v3/v4 and all three tool readmes for real names, absolute home-directory paths, employer name: none found; personal `.diff` notes and employer name (present only in raw notes, never in the post) excluded via `.gitignore`.
- **Per-tool readmes** — turned each tool's raw `.diff` monster file into a structured, English-only `readme.md` (install steps, commands, vocabulary, sources), each ending with a "Visual identity note" quoting the author's own icon concept.
- **Thumbnail, attempt 1** — hand-coded SVG, colorful flat icons (lightbulb / club / lobster). Rejected: "too childish," decorative dots/lines, wrong club shape.
- **Thumbnail, attempt 2** — hand-coded SVG, monochrome black silhouettes matching flaven.fr's existing style (verified live via browser). Rejected: still "ugly" by hand-drawn standard — moved to AI generation instead.
- **Thumbnail, attempt 3** — generating icons via grok.com (Grok Imagine), one prompt per tool, composited manually afterward. BMAD grin succeeded on the first try; CAVEMAN (4 phrasing variants) and OPENCLAW (1 attempt) each returned an empty result with no error message. Root cause found: Grok's free/"Rapide" chat tier appears to allow roughly one image generation before silently dropping further ones — the dedicated Grok Imagine tool refused outright with a SuperGrok subscription paywall.
- **Thumbnail, attempt 4** — switched to Mistral's Le Chat (`chat.mistral.ai`), Robert Crumb underground-comix style per the author's own reference (scratchy ink, grotesque, transparent background, no text). All three prompts succeeded on the first try this time: BMAD grin and CAVEMAN-with-club both genuinely strong; OPENCLAW pincer weak (reads as a curled shrimp, not a clear two-fingered claw). Saved raw and unedited in `mistral_thumbnail_assets/`.
- **Thumbnail, attempt 5** — feedback: too scary, especially BMAD and OPENCLAW. Requested blend toward Keith Haring's bold cheerful pop-art style instead of full Crumb grotesquerie. Rewrote all three prompts accordingly. Blocked on Mistral: free image-generation quota was already exhausted on the very first attempt of this batch (`Quota de génération d'images dépassé`).
- **Thumbnail, attempt 6** — switched to ChatGPT (chatgpt.com), same three Haring-blend prompts. All three succeeded on the first try. Saved unedited (aside from patching out the hover-UI "Modifier"/share pill overlays picked up in the screenshot capture) to `mistral_thumbnail_assets/v2/`. CAVEMAN is the standout; BMAD and OPENCLAW both land as cheerful and non-scary as requested.
- **Thumbnail, `b_v2` composite (local, no AI calls)** — user supplied `images/001_image_prompt.md`, a detailed prompt for a single AI-generated three-strip vertical comic-collage wallpaper (BMAD METHOD / CAVEMAN / OPENCLAW), plus a folder of reference images to guide it: `bemad_*`, `caveman_*`, `openclaw_*`. The `caveman_*` files are actual Hanna-Barbera stills (Fred Flintstone, Captain Caveman) and `openclaw_3_*` is OpenClaw's real logo asset — copyrighted/trademarked material, not ours to publish. A first pass fed the full prompt plus 5 of those reference images into ChatGPT (uploads capped mid-batch by ChatGPT's free-tier file-import quota) and produced a genuinely strong colored 3-strip result — but it was never saved because the user asked to stop and redo the whole thing locally, with no further calls to Grok/Mistral/ChatGPT. Rebuilt entirely with local Python/Pillow instead: composited the three already-generated, original v2 Haring-blend icons (`mistral_thumbnail_assets/v2/*.png`, from attempt 6 above) onto a 3-strip 1080×1200 canvas (yellow/orange/blue fields, black dividers and border), luminance-keyed each icon to pure black ink on transparent so it drops cleanly onto the color fields, and rendered the "BMAD METHOD / CAVEMAN / OPENCLAW" labels as real typed text (crisp, not AI-rendered) rather than reproducing any of the copyrighted reference art. Output: `images/ia_using_bmad_method_caveman_openclaw_b_v2.jpg`. Rejected: "ugly." User taking the thumbnail over manually from here — no further AI/automated thumbnail attempts.
