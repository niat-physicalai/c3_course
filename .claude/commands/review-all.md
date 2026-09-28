---
description: Lint every unit, review all of them in parallel batches, and write a course-level summary
argument-hint: (optional) module folder prefix, e.g. 02
---

1. Run `python review/lint_units.py` (all units) and read `review/lint-report.md`.
2. List unit files under `0*-*/` (filter by "$ARGUMENTS" prefix if given), in course order.
3. Launch the `unit-reviewer` agent on each file, **5 at a time**, waiting for each batch to finish.
   Skip any unit that already has `review/findings/<ID>.md` newer than the unit file.
4. Read every findings file and write `review/SUMMARY.md`:

   ```markdown
   # Review summary — <date>
   | Unit | Words now | After cuts | P1 | P2 | Verdict |
   ## P1 issues across the course (fix first)
   <one line each: unit · finding id · what is wrong>
   ## Repeated stories — who should own each
   <story → owner unit → units that should replace it with a pointer>
   ## Patterns the build prompt keeps producing
   <3–6 bullets, each a rule to add to COURSE-BUILD-PROMPT so the next unit does not repeat it>
   ## Units to consider cutting or merging
   <only if the findings support it>
   ```
5. Report in chat: total words now vs after cuts, P1 count, and the three units in worst shape.

Do not edit any unit file in this command.
