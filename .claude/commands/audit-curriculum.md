---
description: Check CURRICULUM.md against the original requirements and the reference product; propose cuts and gaps
---

You are auditing the course plan, not the reading files. Read `review/REQUIREMENTS.md`,
`CURRICULUM.md`, `REFERENCE-PRODUCT.md`, `PROGRESS.md` and `COURSE-BUILD-PROMPT*.md`.
Read `review/SUMMARY.md` if it exists.

Write `review/CURRICULUM-AUDIT.md` with these sections, each as a table, no prose padding:

1. **Coverage** — one row per item in REQUIREMENTS.md: requirement · unit(s) covering it ·
   Covered / Partly / Missing / Out of scope by design · one-line note.
2. **Beyond the brief** — curriculum content that no requirement asks for and a BTech student
   building their first product does not need (e.g. enterprise practice, 1000-unit costing,
   certification, IP ratings). Proposed action: cut / shrink to a paragraph / move to C7-style
   "going further". Estimated hours saved.
3. **Contradictions** — places where CURRICULUM.md says something REFERENCE-PRODUCT.md or
   PROGRESS.md contradicts (tool used, what dominates the power budget, whether a real invoice
   exists, etc.). Quote both sides.
4. **Build-prompt causes** — rules in the build prompt that push length or padding (word targets,
   mandatory sections, "match the long dense readings", etc.), with a replacement rule for each.
5. **Proposed revised hours table** — Section · current hrs · proposed hrs · why.

Do not edit CURRICULUM.md. Report the top five recommendations in chat, ≤ 10 lines.
