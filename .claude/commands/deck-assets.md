---
description: Make the Claude-generatable visuals for a module (SVG diagrams, GIF animations, charts) and refresh the todo list
argument-hint: <module key>
allowed-tools: Bash(python3 *), Bash(python *), Read, Write, Edit, Glob
---
Produce visuals for module **$ARGUMENTS**.

1. `python3 tools/assets_todo.py <key> --sync` (picks up anything I dropped in). Read `slides.yaml` and the todo list.
2. **claude-svg** (diagrams: block diagrams, flows, state machines, comparisons, matrices):
   write `assets/slides/<key>/<id>.svg` directly. 16:9 viewBox `0 0 1600 900` unless `aspect` says otherwise,
   white background, palette and font family taken from the template (see `deck/style-profile.md` fonts), labels
   ≥ 28 px, ≤ 12 words of text total, only terms that appear in the slide's `sources`. No `<foreignObject>`,
   no external fonts/images (they don't rasterise).
3. **claude-gif** (processes over time: signal on a bus, state transitions, a loop running, sleep/wake timeline):
   write `deck/asset-src/<key>/<id>.py` using `tools/gif_kit.py` (Canvas, save_gif), run it, output to
   `assets/slides/<key>/<id>.gif`. ≤ 40 frames, ≤ 960 px wide, ≤ 4 s loop, < 2 MB.
4. **claude-chart** (numbers that appear in the sources only): `deck/asset-src/<key>/<id>.py` with matplotlib → PNG,
   1600×900, template colours, no chart junk. Never plot numbers that aren't in the cited sections.
5. Look at every file you made (Read the PNG/SVG render; for GIFs check first and last frame by saving them as PNG).
   Fix anything unreadable or off-source.
6. `python3 tools/assets_todo.py <key> --sync` (it validates, rebuilds the .pptx and renders preview + PDF), and tell me how many `user-ai` /
   `user-capture` items remain, pointing at `deck/build/<key>/ASSETS-TODO.md`.

Never route a `user-ai` or `user-capture` item to yourself. If a free image-generation connector is available
in this session (e.g. Canva `generate-image`), ask me before using it — and still save the result to `save_to`.
