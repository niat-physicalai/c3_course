# Slide decks (deck-kit) — rules for Claude

> Append this section to the repo's CLAUDE.md. It applies to every /deck-* command.

## What a deck is
One summary deck per **module** (one folder like `02-sensing-and-hardware-architecture/`), covering
every unit in it, **max 30 slides**. It shows the crux; the reading material holds the detail, so every
content slide's speaker notes end with `Read more: <unit id> — <unit title>`.

## Source of truth — hard rules
1. **Content comes only from the module being built** (`deck/build/<key>/digest.json`, i.e. its unit .md files).
   The Applied IoT reference (`reference/applied-iot/`, `deck/style-profile.*`) teaches *style, density and layout only* —
   never copy facts, examples or wording from it into this course's slides.
2. Every content slide lists `sources:` as `UNIT#anchor` taken from `outline.md`. Never invent an anchor.
3. **Shorten, don't add.** Bullets are compressions of sentences that exist in the cited sections. No new
   facts, numbers, part names, claims or examples. If something is missing from the source, it is missing from the slide.
4. Keep the source's technical terms and figures exactly (units, part numbers, values). Don't "round" or "update" them.
5. The curriculum (`curriculum.md` slice) decides **what must be covered** (outcomes → `covers:`); the units decide **what is said**.
6. `python tools/validate_spec.py <key>` must PASS before any build. Never use `--force` for a deck you hand over.

## Updating — no drastic changes
- On `/deck-update`, edit **only** slides listed in `changes.md` and only the parts tied to the changed sections.
  All other slides stay byte-identical. Slides with `locked: true` are never touched (the validator enforces it).
- Prefer editing an existing slide over adding one; never reorder or renumber slide ids. New slides get new ids (`s31`, `s32`…)
  and are inserted in position; ids are labels, not positions.

## Visual-first
- Target ≥ 60 % of content slides with a visual (`limits.min_visual_ratio`). Text is for elaboration only:
  ≤ 4 bullets, ≤ 14 words each, ≤ 45 body words per slide.
- Keep the slides that introduce and explain (what a thing is, why it matters, how it works), but write them
  direct and minimal: one point per bullet, no lead-ins, no filler. No decorative subtitles ("Module 2 · Summary").
- Body text is 18 pt; the builder drops to 15 pt only when a slide's text wouldn't fit. Aim for text that fits at 18.
- Every deck gets the template's WELCOME and THANK YOU slides automatically (`bookends:` in the map) — don't add
  them to `slides.yaml`; they are not counted in the 30-slide cap (≤ 32 slides in the .pptx).
- Visual priority: **(1)** reuse an existing course asset (images referenced in the cited sections, or `asset_dirs`)
  → **(2)** Claude-made: `claude-svg` diagram, `claude-gif` animation, `claude-chart` plot → **(3)** `user-capture`
  (KiCad/PlatformIO screenshots, screen-recording GIFs, product photos) → **(4)** `user-ai` with a ready prompt.
- Diagrams: an arrow meets a box at the centre of the side it touches (a pair of arrows sits symmetric about
  it); move or resize the box rather than offsetting the arrow.
- A visual must depict something stated in its slide's sources. AI-image prompts must ask for **no text / labels**
  (image AIs misspell) — labels go in the caption.

## Visual spec fields
`{id: V-<slide>-<n>, status: existing|generated|todo, route: course|claude-svg|claude-gif|claude-chart|user-capture|user-ai,
type: image|diagram|gif|screenshot|photo|chart, path: <file if ready>, save_to: assets/slides/<key>/<id> (no extension),
brief: <what it shows>, prompt: <for user-ai>, aspect: 16:9|4:3|1:1, caption: <≤12 words>, source_ref: UNIT#anchor}`

## Google Slides compatibility (the deck is uploaded there, then embedded)
Never add: SmartArt, charts objects, SVG/EMF, WordArt/3D/shadows/glow, embedded fonts, video/audio, text that relies on
shrink-to-fit, grouped shapes, slide transitions/animations (Slides drops most). Use only fonts that exist in Google Slides.
`build_deck.py` already rasterises SVG, fixes text sizes and fits images — don't post-edit the .pptx by hand; change
`slides.yaml` or `template.map.yaml` and rebuild.

## Files per module (`deck/build/<key>/`)
`outline.md` (read first) · `digest.json` · `curriculum.md` · `slides.yaml` (the editable spec — the ONLY thing you write)
· `<key>-<title>.pptx` · `manifest.json` · `ASSETS-TODO.md` · `changes.md` · `preview/`
