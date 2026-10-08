# deck-kit — module summary decks from your reading material (Claude Code)

One command turns a module folder of unit `.md` files into a ≤ 30-slide summary deck in your Applied IoT template,
visual-first, grounded line-by-line in the reading material, plus a numbered asset to-do list (with AI-image prompts)
for anything Claude can't draw itself. Content edits later get **targeted** slide updates, not a regenerated deck.

```
 unit .md files ──► digest (sections + hashes) ──► crux.md ──► slides.yaml ──► validate ──► fidelity agent
      ▲                                              (Claude)   (the editable spec)  (script)    (fresh context)
      │                                                                                          │
  you edit content ──► /deck-update: changes.py finds changed sections → only those slides edited │
                                                                                                 ▼
 ASSETS-TODO.md ◄── assets_todo.py ◄── build_deck.py (template, Slides-safe) ◄── render_preview (LibreOffice)
   you drop files → --sync → rebuild                         │
                                                             ▼
                                  .pptx → Google Slides → Publish to web → embed iframe in course
```

The LLM writes exactly one file per module (`slides.yaml`). Everything else — parsing, checking, layout, image fitting,
change detection — is deterministic Python, so a rebuild never "reinterprets" anything.

---

## 1 · Install (once, ~10 min)

**Needs:** Claude Code, Python ≥ 3.10, LibreOffice + poppler (only for previews; `sudo apt install libreoffice poppler-utils`
· macOS `brew install --cask libreoffice && brew install poppler` · Windows: install LibreOffice, use WSL for poppler).

1. Copy the kit into the **course repo root** (next to `CURRICULUM.md`):
   ```
   .claude/commands/deck-setup.md  deck-build.md  deck-update.md  deck-assets.md
   .claude/agents/deck-fidelity-checker.md
   tools/*.py  tools/requirements.txt
   deck/examples/slides.example.yaml
   deck.config.yaml
   ```
2. Append `CLAUDE.deck.md` to the repo's `CLAUDE.md` (create it if missing): `cat CLAUDE.deck.md >> CLAUDE.md`
3. `pip install -r tools/requirements.txt` (use a venv, or `--break-system-packages` on Debian/Ubuntu)
4. Put the Applied IoT decks in the repo — your tree has the Applied IoT *markdown* but no `.pptx` yet:
   `reference/applied-iot/slides/Module-1.pptx … Module-5.pptx`. Download from Google Slides as **.pptx**
   (File → Download → Microsoft PowerPoint).
5. Edit `deck.config.yaml`: `template` (the reference deck whose look you want), `reference_pairs` (2–3 md-folder ↔
   pptx pairs are plenty), module list (already filled from your tree), limits.
6. `.gitignore`: `deck/build/*/preview/` and `deck/build/*/_media/`. Commit everything else — `slides.yaml` and
   `manifest.json` are what make updates incremental.

## 2 · One-time calibration

```
claude
> /deck-setup
```
Claude measures the reference decks (words/slide, visual ratio, layouts, fonts, md→slide compression and which
section each slide came from → `deck/style-profile.md`), inventories the template, and tunes
`deck/template.map.yaml` until a sample deck with every slide kind matches the reference look.

**Do the Google Slides smoke test now, before the first real module:** upload `deck/build/_layout-sample.pptx`
to Drive → open with Google Slides → compare each slide with the PowerPoint/LibreOffice render. If something
shifts, fix the map (usually a font size or a box), rebuild the sample, repeat. Do this once and every module
inherits it. Also confirm a GIF plays after import (it should; if not, see Troubleshooting).

## 3 · Build a module

```
> /deck-build 02            # or "/deck-build 02 auto" to skip the outline checkpoint
```
What happens: digest → Claude reads every unit, writes `crux.md` → proposes a slide outline table (**you approve/edit**)
→ writes `slides.yaml` → validator must PASS → independent fidelity agent checks each slide against its sources → Claude
draws the diagrams/GIFs it can → build → render → Claude checks the PNGs for overflow → `ASSETS-TODO.md`.

Output in `deck/build/02/`: the `.pptx`, `preview/contact-sheet.png`, `ASSETS-TODO.md`, `crux.md`.

Unmade visuals appear in the deck as **orange dashed "ASSET TODO · V-s06-1" boxes**, so a draft is always
reviewable and nothing goes missing silently.

## 4 · Fill the asset to-do list

`ASSETS-TODO.md` groups items by who makes them, each with **slide no · pic no · asset id · save-to path · what it shows
· prompt**:

| route | who | how |
|---|---|---|
| `course` | — | existing course image reused automatically |
| `claude-svg` / `claude-gif` / `claude-chart` | Claude | `/deck-assets 02` (scripts kept in `deck/asset-src/` → re-runnable) |
| `user-ai` | you | paste the prompt into a free generator: **Gemini / ImageFX**, **Microsoft Designer (Bing)**, **Ideogram**, **Leonardo** free tier, **Canva** free Magic Media |
| `user-capture` | you | KiCad/PlatformIO/Onshape screenshots; screen-recording GIFs with ScreenToGif (Win) / Kap (mac) / Peek (Linux); shrink at ezgif.com |

Save each file at its **Save to** path (any of png/jpg/gif/svg — the extension doesn't matter), then:
```
python3 tools/assets_todo.py 02 --sync      # validates, rebuilds the .pptx, renders preview/ + deck.pdf
```
(or just ask Claude: "sync assets and rebuild 02"). Prompts always ask for *no text in the image* — image AIs misspell
labels; labels live in captions instead.

Optional: you have a Canva connector in claude.ai with `generate-image`. The commands tell Claude to **ask first**
before using any image connector, and results still land at `save_to`.

## 5 · When the reading material changes

```
> /deck-update 02
```
`changes.py` hashes every section and compares with the last build. Claude may edit **only** slides citing a changed
section, and only what the change requires; it then shows you a one-line-per-slide diff
(`s08: 4.7 kΩ → 10 kΩ (B1#pull-up-resistors)`). Mark any slide `locked: true` in `slides.yaml` to freeze it — the
validator fails if a locked slide changes. A copy of the previous spec is kept as `slides.prev.yaml`.

Changing the **template** only? Edit `template.map.yaml` and run `python3 tools/build_deck.py 02` — no LLM involved,
content is untouched.

## 6 · Google Slides → course

1. **First time:** Drive → New → File upload → the `.pptx` → right-click → Open with → Google Slides.
2. Embed: File → Share → **Publish to web** → Embed → copy the iframe into the production course.
3. **Updating without breaking the embed link:** open the *same* Google Slides file → select all slides in the filmstrip
   → delete → Insert → **Import slides** → upload the new `.pptx` → Select all → tick *Keep original theme* → Import.
   The file ID (and so the published embed URL) stays the same. Re-uploading a new file would give a new URL.

## Why it stays faithful (and where you still look)

| guard | catches |
|---|---|
| sources must be real `UNIT#anchor`s from the digest | invented references |
| every number on a slide must exist in its cited sections | invented / stale specs (tested: a source edit 4.7→10 kΩ fails the old slide) |
| key-word grounding score per bullet (warning) | wording drifting away from the source |
| every unit cited, every curriculum outcome covered | gaps vs units and CURRICULUM.md |
| fidelity agent in a fresh context (claim-by-claim) | meaning changes the scripts can't see |
| change hashes + `locked:` | drastic rewrites on update |
| reference decks used for style metrics only (rule in CLAUDE.md) | Applied IoT content leaking in |

The number/word checks are heuristics and the agent is a model, so skim `crux.md` and the outline checkpoint — those two
are where your judgement is worth the most and take ~5 minutes per module.

## Google Slides compatibility — what the builder enforces

SVG is rasterised to PNG (Slides can't import SVG); images > 1920 px downscaled; text autofit turned **off** with fixed
sizes (Slides ignores PowerPoint's shrink-to-fit — the #1 cause of text spilling after import); bullets are plain `•`;
images fitted by aspect ratio, never cropped; no SmartArt/charts/groups/effects/transitions created; empty
placeholders removed (no "Click to add text"). Text overflow is checked twice: an estimate at build time and Claude
looking at the LibreOffice render, which is closer to Slides than PowerPoint is. Keep template fonts to ones Google
Slides offers (check the font list in `deck/style-profile.md`).

## Config knobs (`deck.config.yaml`)

`limits.max_slides` (30) · `min_slides` · `max_bullets_per_slide` · `max_words_per_bullet` · `max_words_per_slide` ·
`min_visual_ratio` · `exclude_units` (e.g. `["REF-*.md"]` if REF files shouldn't get slides) · `asset_dirs` ·
`compat.*`. In `template.map.yaml`: per slide kind `layout:` or `prototype:` (clone a designed reference slide),
placeholder idx / shape names, `*_box` overrides in inches, `fonts`.

## Troubleshooting

- **"Layout 'X' not in template"** → names differ in your deck; see `deck/template-inventory.md`, fix the map.
- **Reference look is lost on built slides** → its decorations live on the slides, not the layouts. Switch those kinds
  to `prototype: <slide no>` (Claude does this in `/deck-setup`).
- **GIF static in Google Slides** → re-export it ≤ 8 MB, or insert that one GIF in Slides via Insert → Image after import.
- **Text spills in Slides only** → shorten the bullet in `slides.yaml` (don't shrink fonts) and rebuild.
- **Curriculum slice wrong** → `curriculum.md` match is best-effort by module title/number; edit
  `deck/build/<key>/curriculum.md` by hand before building.

## Command reference

| | |
|---|---|
| `/deck-setup` | calibrate style + template map (once, or when the template changes) |
| `/deck-build <key> [auto]` | first build of a module |
| `/deck-update <key>` | targeted update after content edits |
| `/deck-assets <key>` | make Claude-drawable visuals, refresh todo |
| `python3 tools/digest_module.py <key>` | sections + anchors → `outline.md` |
| `python3 tools/validate_spec.py <key>` | guard-rails (exit 1 on error) |
| `python3 tools/build_deck.py <key>` | spec → .pptx (`--force` = draft despite errors) |
| `python3 tools/render_preview.py <key or file.pptx>` | PNGs + contact sheet + 1 |
| `python3 tools/assets_todo.py <key> [--sync]` | to-do list / pick up dropped files |
| `python3 tools/changes.py <key>` | what changed since last build |
