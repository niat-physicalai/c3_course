> **Superseded by `COURSE-BUILD-PROMPT-v3.md` (2026-10-01).** Kept as a record of the v2 patch.

# Patch for COURSE-BUILD-PROMPT-v2.md

**Status: applied.** These changes were made directly to the `COURSE-BUILD-PROMPT-v2.md` sent back
to you on 2026-09-28 (config fixed to `esp_watch`, word targets reframed as a ceiling, voice/quality
bar rules added against filler, jargon and extrapolation — with no fixed cut percentage, per your
note that cuts should target actual repetition, not a quota). Kept here as a record of what changed
and why, and as the list to re-apply if you regenerate the build prompt from scratch.

These rules replace the parts of the build prompt that produce long, padded units.

**1. Applied version of the target-words line in Run 1:**

> Target words: 2,500–3,500 / 4,000–5,500 / 5,500–7,000 per hour band, unchanged — but now stated
> as a **ceiling, not a goal**: write the shortest version that covers the unit's `CURRICULUM.md`
> row and nothing else. Match the Applied IoT readings' voice, not their length. Do not pad to
> reach the target, and do not retell a reference-watch story another unit already owns.

**2. In the template, make these sections optional or once-only:**

- "How to read the labels" box: **A0 only**. Delete it from every other unit.
- "What Part 1 Already Covered": **one or two sentences**, or leave it out when nothing applies.
- Opening bridge: **at most two short paragraphs**.
- "What You Can Now Do, and What Comes Next": **one short paragraph**. Do not repeat the outcomes.
- MCQ answer explanations: **≤ 60 words**. Explain why the wrong options are wrong only when the
  reason isn't obvious.
- Try-it boxes: **one or two**. Never duplicate an end-of-unit activity.

**3. In QUALITY BAR, replace "Every section of the template is present and substantial" with:**

> - [ ] Every paragraph passes the test "would the student notice if it were gone?"
> - [ ] Nothing goes beyond this unit's row in `CURRICULUM.md`: no production-scale, certification or team-process asides.
> - [ ] Every reference-product story is either owned by this unit or is a one-line pointer to the unit that owns it.
> - [ ] No term a 3rd-year BTech student wouldn't know is left undefined, and none is used when a plain word works.

**4. Add to VOICE AND STYLE:**

> - Plain words. Sentences under 25 words where possible.
> - Banned: "This is not X. It is Y.", "Here is the thing", "the lesson is", "genuinely",
>   "deliberately", "quietly", "discipline", "load-bearing", "first-class", "specimen".
> - Explain one idea in one way. No second analogy, no closing moral at the end of each section.

**5. Fix the stale config line:** `reference_product` still says "AirGradient ONE / Open Air". It
should say "esp_watch — see REFERENCE-PRODUCT.md".

**6. Superseded 2026-09-29 (author):** word targets are **removed**, not just made a ceiling. Replace
the Run 1 target-words line and the quality-bar item "Word count is within the target band" with:

> Write what a student needs to understand this unit's `CURRICULUM.md` row and produce its
> deliverable, then stop. There is no word target. The only size limit is the 50,000-character file cap.

Also change in the template and quality bar:

- **Required in every unit:** outcomes, the content, one worked example, the activity that produces the
  deliverable, a binary self-check of about 8 items, and 5 MCQs.
- **Optional:** Try-it boxes (no minimum of two), Part headings (no "two to four Parts"), and the
  recognise → reproduce → modify → diagnose → design activity ladder.
- **Unit IDs and folders** follow the 2026-09-29 restructure in `CURRICULUM.md` and `PROGRESS.md`
  (A · B sensing & hardware architecture · C form factor, schematic & PCB · D firmware · E mechanical ·
  F sourcing · G capstone).
