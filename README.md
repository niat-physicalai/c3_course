# C3 review kit

Drop the contents of this folder into the root of your course repo (next to `CURRICULUM.md`,
`PROGRESS.md`, `REFERENCE-PRODUCT.md`) and commit. Everything runs inside Claude Code.

```
.claude/agents/unit-reviewer.md      the reviewer (one unit → one findings file)
.claude/commands/review-unit.md      /review-unit B1 [C3 …]
.claude/commands/review-all.md       /review-all [02]
.claude/commands/apply-review.md     /apply-review B1 [all]
.claude/commands/audit-curriculum.md /audit-curriculum
review/RUBRIC.md                     what counts as padding, jargon, extrapolation — edit freely
review/REQUIREMENTS.md               your original requirements sheet, transcribed
review/lint_units.py                 mechanical counts, no dependencies
```

## The loop

1. **`/audit-curriculum`** (once). Checks the plan against your original requirements, flags
   contradictions and over-reach, and proposes an hours table. Decide the curriculum cuts
   *before* polishing units you may delete.
2. **`/review-all`** — lints every unit, runs the reviewer on each one, and writes
   `review/SUMMARY.md`. Or run **`/review-unit A0`** to try one unit first.
3. Open `review/findings/A0.md`. Each finding quotes the text and gives the replacement.
   Tick `- [x] accept` on the ones you agree with. You're reading a list of proposed edits,
   not the whole unit.
4. **`/apply-review A0`** applies only the findings you ticked, reports the words saved, and stops
   before committing. Use `/apply-review A0 all` once you trust the reviewer.
5. Review the git diff and commit.

## Tuning

- If the reviewer flags too much or too little, edit `review/RUBRIC.md`. That file sets how
  strict the review is.
- Add phrases you keep deleting to `FILLER` / `JARGON` in `lint_units.py`, and add retold
  anecdotes to `STORIES`.
- The findings files go in git, so you have a record of what was cut and why.

## Stop the padding at the source

Paste `BUILD-PROMPT-PATCH.md` into `COURSE-BUILD-PROMPT-v2.md` before you regenerate or write
any new unit.
