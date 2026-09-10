## PROMPT_SET — Grok thumbnail generation

Context: replacing the hand-coded SVG thumbnail for the blog post with AI-generated icons via grok.com. Trademarked character names dropped deliberately (Alfred E. Neuman, Fred Flintstone, Captain Caveman are copyrighted) — described by visual traits instead, so generation doesn't refuse or lean on IP. Text labels left out of the generated images on purpose; labels get added afterward in compositing, since AI image generators reliably mangle small text.

Style anchor used in all four prompts, lifted from flaven.fr's existing post thumbnails: flat, bold, minimal graphic illustration, mostly monochrome black on a clean white background, confident thick outlines, no gradients, no clutter, editorial-blog quality rather than photorealistic.

---

### PROMPT_1 — BMAD METHOD icon

```
Flat minimalist icon illustration, bold black shape on a pure white background, editorial blog style, no gradients, no shadows, no text or letters anywhere in the image. A single round cartoon face with a big mischievous gap-toothed grin, wide simple eyes, one eyebrow raised, ears sticking out slightly, freckles optional — playful and impish rather than angry, evoking a classic satirical-magazine mascot vibe without copying any specific character. Solid black silhouette style with a couple of white cutout details (eyes, teeth gap), high contrast, clean vector look, centered composition, plenty of white margin around the subject, square-ish crop.
```

### PROMPT_2 — CAVEMAN icon

```
Flat minimalist icon illustration, bold black silhouette on a pure white background, editorial blog style, no gradients, no shadows, no text or letters anywhere in the image. A stocky, cartoonish prehistoric caveman figure, standing, wearing a single-shoulder-strap fur tunic, spiky messy hair, one arm raised overhead swinging a wooden club with a heavy round head — energetic, mid-swing pose, confident and a bit goofy, like a classic Stone-Age cartoon character (but an original generic design, not a copy of any specific existing character). Solid black silhouette, clean vector look, centered composition, plenty of white margin around the subject, square-ish crop.
```

### PROMPT_3 — OPENCLAW icon

```
Flat minimalist icon illustration, bold black silhouette on a pure white background, editorial blog style, no gradients, no shadows, no text or letters anywhere in the image. A single open lobster claw / pincer, viewed from the side, clearly showing two pincer tips slightly apart as if open and ready to snap, thick and chunky proportions, cartoon-graphic rather than realistic. Solid black silhouette, clean vector look, centered composition, plenty of white margin around the subject, square-ish crop.
```

### PROMPT_4 — Combined thumbnail (fallback attempt, one shot)

```
Flat minimalist blog-header illustration, bold black silhouettes on a pure white background, editorial style, no gradients, no shadows, no text or letters or words anywhere in the image. Three separate simple icons evenly spaced left to right on one wide horizontal canvas (16:9): (1) a round cartoon face with a big mischievous gap-toothed grin and one raised eyebrow; (2) a stocky cartoon prehistoric caveman in a fur tunic, mid-swing with a club raised overhead; (3) a single open lobster claw / pincer shown from the side. Each icon is a clean solid black silhouette, same visual weight and style, generous white space between and around them, nothing overlapping, nothing photorealistic, no background scenery, no color.
```

---

Recommended path: run PROMPT_1 through PROMPT_3 separately (small, single-subject prompts generate more reliably), pick the cleanest result for each, then composite the three side by side with typed labels (BMAD METHOD / CAVEMAN / OPENCLAW) added afterward rather than baked into the generation. PROMPT_4 is there in case a one-shot combined image works well enough on the first or second try — worth one attempt before falling back to compositing.
