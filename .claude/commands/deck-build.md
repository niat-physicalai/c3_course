---
description: Build the summary deck for one module, e.g. /deck-build 02   (add "auto" to skip the outline checkpoint)
argument-hint: <module key> [auto]
allowed-tools: Bash(python3 tools/*), Bash(python tools/*), Read, Write, Edit, Glob, Grep, Agent
---
Build the summary deck for module **$ARGUMENTS**. Obey CLAUDE.md → "Slide decks" at every step.
If `deck/build/<key>/manifest.json` already exists, stop and tell me to use `/deck-update <key>` instead.

## 1 · Digest (deterministic)
`python3 tools/digest_module.py <key>` → read `deck/build/<key>/outline.md`, `curriculum.md`, and the
"aggregate" table at the top of `deck/style-profile.md`.

## 2 · Crux extraction (read everything, keep only the crux)
Read **every unit file in full**. Write `deck/build/<key>/crux.md`: per unit, 3–6 crux points, each one line,
each ending with its anchor `(B0#selection-matrix)`. A crux point is a decision, rule, mental model, key
number, or process a student must leave with. Skip: anecdotes, repeated explanations, tool trivia, tangents.
Also note per unit which existing images/GIFs (from the outline `imgs:`) best show each point.

## 3 · Slide budget and outline
- Target count ≈ module words ÷ `avg_md_words_per_slide`, clamped to `limits.min_slides`…`limits.max_slides` (30).
- Fixed frame: `title` → `agenda` → [per unit: optional `section` slide + content slides] → `recap` (one bullet per unit).
  With > 6 units, skip per-unit section slides and let agenda do the job.
- Split the remaining budget across units in proportion to their word count, minimum 1 content slide per unit.
- Map every curriculum outcome in `curriculum.md` to ≥ 1 slide (`outcomes:` + `covers:`). If an outcome has **no**
  supporting content in the units, don't invent it — list it under "Curriculum gaps" in your report.
- Pick a kind per slide; prefer `image-text`, `image-full`, `two-images`; use `bullets` only when there's genuinely
  nothing to show; `key-idea` for one rule or number that must stick (max ~3 per deck).

**Checkpoint** (skip if "auto" was given or I'm not around): show me a compact table —
`# | kind | title | sources | visual idea (route)` — and wait for OK / edits.

## 4 · Write `deck/build/<key>/slides.yaml`
Schema: see an example in `deck/examples/slides.example.yaml` (fields: id, kind, title, subtitle, bullets, key_idea,
visual, visual2, sources, covers, notes, locked). Rules:
- ids `s01`, `s02`… in order. Titles are short claims ("I2C needs pull-ups"), not topics ("Pull-ups").
- Bullets: compress source sentences; reuse source terms and figures verbatim.
- `notes`: 2–4 sentences the presenter can say, drawn from the same sources, ending `Read more: <unit> — <title>`.
- Visuals in priority order (CLAUDE.md "Visual-first"). Every visual gets `id: V-<slide id>-<n>`, a `route`,
  a `brief`, and `save_to: assets/slides/<key>/<id>` unless it reuses an existing file (`status: existing`, `path:`).
  `user-ai` visuals get a full prompt: subject, composition, style (match the reference deck's look — flat vector,
  palette from the template), aspect ratio, "white background, no text, no labels".

## 5 · Validate → fix → validate
`python3 tools/validate_spec.py <key>` until **PASS**. Treat "low grounding" warnings as real: re-read the source
and reword the bullet closer to it.

## 6 · Independent fidelity review
Spawn the `deck-fidelity-checker` agent with: the module key. It compares every slide against its cited sections
in a fresh context. Apply its fixes (only the ones that remove drift/inaccuracy), re-validate.

## 7 · Make what Claude can make
For visuals with route `claude-svg`, `claude-gif`, `claude-chart`, follow `/deck-assets` steps 2–4, then
`python3 tools/assets_todo.py <key> --sync`.

## 8 · Build and look at it
`python3 tools/build_deck.py <key>` then `python3 tools/render_preview.py <key>`. Read `preview/contact-sheet.png`
and every slide that has text near a box edge. Fix overflow by shortening text in `slides.yaml` (never by shrinking fonts),
fix bad image fits by changing kind. Rebuild until clean. Then `python3 tools/assets_todo.py <key>`.

## 9 · Report (≤ 10 lines)
Slide count, visual ratio, outcomes covered, curriculum gaps, fidelity fixes made, and
"N assets left for you → deck/build/<key>/ASSETS-TODO.md". Point to the .pptx path.
