# Review rubric — C3 units

The reviewer reads one unit against this rubric and returns **proposed edits**, not opinions.
Every finding must quote the text it touches and give the replacement (or "delete").

The reader is a BTech student in India, working alone, with Part 1 (Applied IoT) behind them.
Every sentence is measured against one question: **would this student notice if it were gone?**
If not, it goes.

---

## Categories (use these codes)

| Code | What it catches | Default action |
|---|---|---|
| **CUT** | A sentence, paragraph or section the student would not miss: restating the previous paragraph, previewing the next one, "why this matters" padding, a second analogy for something already clear, recap of another unit, a history lesson nobody asked for. | Delete |
| **TIGHTEN** | Right idea, too many words. Three sentences that could be one; a paragraph that could be a 4-row table; a worked example with steps that show nothing new. | Rewrite shorter, give the rewrite |
| **JARGON** | A term a 3rd-year BTech student would not know and the text does not need: consultant words (load-bearing, first-class, provenance, traceability, specimen, invariant), industry acronyms used once (PCN, NRND, NRE, LTB), formal notation where plain words work. | Plain word, or define in ≤1 line, or cut |
| **EXTRAPOLATE** | Content that goes beyond `CURRICULUM.md`'s unit row or beyond what a student can act on in this course: production-scale concerns (certification, 10k-unit tooling, IP ratings in depth), enterprise practice (ADR governance, team process), speculative "in a real company…" asides. | Cut, or shrink to one sentence |
| **REPEAT** | The same explanation or reference-product story told in full in another unit. (See lint report's "stories" table.) One unit owns each story; others point to it in one line. | Replace with a one-line pointer |
| **FACT** | A reference-product claim not in `REFERENCE-PRODUCT.md`, a modelled figure presented as measured, a cost presented as the author's real spend, a number with no source and no `FACT:VERIFY`. | Correct or flag |
| **SCOPE** | Activity needs hardware, soldering, printing or measuring. Re-teaches Part 1 (Ohm's law, GPIO, basic I²C/MQTT use). | Rewrite as laptop-only, or cut |
| **STRUCTURE** | Missing deliverable, activities that do not produce it, self-check items that are not binary, MCQs that test recall only, broken code, broken relative links. | Fix |
| **CLARITY** | A sentence a student would have to read twice. Nested clauses, passive chains, a claim whose "so what" is missing. | Rewrite |

## Severity

- **P1 — wrong or blocking:** incorrect fact, invented reference-product detail, broken code, activity impossible on a laptop, deliverable missing.
- **P2 — costs the student time:** CUT / TIGHTEN / JARGON / EXTRAPOLATE / REPEAT worth ≥ 40 words, or anything that confuses.
- **P3 — polish:** small wording, spelling, formatting.

## Length stance

The build prompt's word target is a ceiling, not a goal. There is **no fixed percentage to cut.**
Cut only what a CUT/TIGHTEN/JARGON/EXTRAPOLATE/REPEAT finding actually justifies — restated points,
retold reference-watch stories, jargon, and content beyond the unit's `CURRICULUM.md` row. A unit
with none of that stays as it is, even at full target length. A unit with a lot of it may end up
much shorter — report the estimated saving either way, but never treat a percentage as the goal.

Template sections are **not sacred**. The reviewer may propose deleting or merging:
- "How to read the labels" box (keep once, in A0 or the course intro — cut from every other unit)
- "What Part 1 Already Covered" when it says nothing specific (shrink to one line)
- Opening bridge longer than two short paragraphs
- "What You Can Now Do, and What Comes Next" when it restates the outcomes list
- Try-it boxes that are the same exercise as an activity at the end

## Tells of padding (look for these first)

- Sentence pairs of the form "This is not X. It is Y." / "Not just X, but Y."
- "Here is the thing / the honest answer / the lesson is / that is the whole point"
- A paragraph that ends by restating its first sentence
- Rhetorical question immediately answered in the next sentence, more than once per section
- Three-item lists where the third item is vaguer than the first two
- Em-dash asides stacked two or more per sentence
- Every section ending with a moral
- Reference-product story retold with full numbers when a pointer would do
- Words: genuinely, deliberately, precisely, quietly, crucially, fundamentally, discipline

## What to leave alone

- Correct, concrete, short explanations — even if you would phrase them differently.
- Worked examples that show a step the student will actually repeat.
- `REFPRODUCT`, `MEDIA`, `ASSET:PLACEHOLDER`, `FACT:VERIFY`, `LINK:VERIFY` comments (check them, do not strip them).
- British spelling.
