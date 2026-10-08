---
description: One-time setup — learn the reference style and map the template (run again only if the template changes)
allowed-tools: Bash(python3 tools/*), Bash(python tools/*), Read, Edit, Write, Glob
---
Set up deck-kit for this repo. Follow CLAUDE.md → "Slide decks".

1. Check `deck.config.yaml`: the `template` and every `reference_pairs[].pptx` exist (Glob). If a reference pptx is
   missing, tell me which path to put it at and stop.
2. Run `python3 tools/analyze_reference.py`. Read `deck/style-profile.md`.
3. Run `python3 tools/extract_template.py --sample` (add `--force` only if I asked to redo the map).
   Read `deck/template-inventory.md`.
4. Render the reference deck: `python3 tools/render_preview.py <template path>` and look at
   `…/preview/contact-sheet.png` plus 3–4 individual slides. Learn the design: where titles sit, image vs text
   balance, how sections are introduced, colour accents, fonts.
5. Improve `deck/template.map.yaml` so each kind (title, agenda, section, image-text, image-full, two-images,
   bullets, key-idea, recap) looks like the reference:
   - If the reference's look lives in its **layouts**, map kinds to `layout:` + placeholder idx.
   - If the look lives on the **slides themselves** (common for decks made in Google Slides/Canva — decorations sit
     on each slide), use `prototype: <slide no>` with shape **names** from the inventory for title/body/visual.
   - Set `fonts:` sizes to the reference's sizes (style-profile font_sizes_pt). Set `force_sizes: true` if the
     reference uses explicit run sizes.
6. Rebuild the sample (`python3 tools/extract_template.py --sample`), render `deck/build/_layout-sample.pptx`,
   compare with the reference contact sheet, iterate on the map until each kind matches.
7. Report to me in ≤ 8 lines: kinds mapped (layout vs prototype), font sizes, the learned targets
   (slides/module, md-words per slide, visual ratio) and anything I must decide.
