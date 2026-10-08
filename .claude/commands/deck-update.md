---
description: Update a module's deck after the reading material changed — minimal, targeted edits only
argument-hint: <module key>
allowed-tools: Bash(python3 tools/*), Bash(python tools/*), Bash(git diff*), Bash(cp *), Read, Write, Edit, Glob, Grep, Agent
---
Update the deck for module **$ARGUMENTS** after content changes. Obey CLAUDE.md → "Slide decks", especially
"Updating — no drastic changes".

1. Snapshot: `cp deck/build/<key>/slides.yaml deck/build/<key>/slides.prev.yaml`.
2. `python3 tools/changes.py <key>` → read `deck/build/<key>/changes.md`. If it says nothing changed, stop and say so.
3. For each **affected slide**: read its cited sections (old wording is in `git diff` of the unit file if available)
   and change only what the source change requires — a figure, a term, a bullet. Keep title, kind, visual and order
   unless the change makes them wrong.
4. **New sections**: fold into an existing slide of that unit if it fits the limits; add a new slide (next free id,
   inserted after its unit's last slide) only if it's a new crux point and the deck stays ≤ 30 slides.
   **Removed sections**: re-point `sources:` or drop the bullet; remove a slide only if nothing is left.
   **New/removed units**: add/remove slides and agenda/recap lines accordingly.
5. If a changed source invalidates a visual, set it back to `status: todo` with an updated brief/prompt.
6. `python3 tools/validate_spec.py <key>` until PASS (locked slides and figures are enforced here).
7. Spawn `deck-fidelity-checker` with the module key **and the list of edited slide ids** (review only those).
8. Build + render (`build_deck.py`, `render_preview.py`), check the edited slides' PNGs, then `assets_todo.py <key>`.
9. Report a diff summary: for each edited slide one line "s07: 4.7 kΩ → 10 kΩ (B1#pull-up-resistors)",
   plus any new/removed slides and new asset todos. Show `diff slides.prev.yaml slides.yaml` stats.
