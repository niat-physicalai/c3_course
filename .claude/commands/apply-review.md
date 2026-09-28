---
description: Apply the findings you ticked in review/findings/<ID>.md to the unit file
argument-hint: <UNIT-ID> [all]   — "all" applies every P1/P2 finding without needing ticks
---

Apply review findings for: $ARGUMENTS

1. Read `review/findings/<ID>.md`. Select findings marked `- [x] accept`.
   If the second argument is `all`, select every P1 and P2 finding instead.
   If nothing is selected, say so and stop.
2. Open the unit file. For each selected finding, in order from the **bottom of the file up**
   (so earlier line numbers stay valid):
   - Locate the quoted text by exact match (the `…` in a quote means "any text between").
   - Apply the replacement, or delete. For "Delete section through", remove from the heading to the
     quoted last line inclusive.
   - If the quote is not found exactly once, skip it and record it as SKIPPED.
3. After all edits: fix numbering that broke (MCQ numbers, Part numbers, activity numbers),
   make sure no heading is left empty, and that `---` separators are not doubled.
4. Do not touch `REFPRODUCT`, `MEDIA`, `ASSET`, `FACT:VERIFY` or `LINK:VERIFY` comments unless a
   finding explicitly targets them.
5. Run `python review/lint_units.py <ID>` and report: words before → after, findings applied,
   findings skipped (with IDs).
6. In the findings file, change each applied `- [x] accept` to `- [x] applied`, and each skipped
   one to `- [ ] SKIPPED — quote not found`.
7. Do not commit. Show me `git diff --stat` and stop.
