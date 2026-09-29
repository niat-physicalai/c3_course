# Findings — G Capstone: The Design Pack and the Reference Review

**Words now:** 3042 · **After accepted cuts (est.):** 2560 (−16 %)
**Verdict:** The pack list leaves out three deliverables the curriculum requires, and the reference review states esp_watch "facts" and v2 plans that are not in REFERENCE-PRODUCT.md.

## Section-level calls
| Section | Keep / Shrink / Cut / Merge into … | Reason (≤ 15 words) | ~Words saved |
|---|---|---|---|
| This Pack Is Your Proposal | Shrink | First paragraph recaps the course; keep the funded-build sentence and three questions | 70 |
| What You Will Be Able to Do | Keep | — | 0 |
| What Parts 1 and 2 Already Covered | Cut | Says nothing the student needs | 55 |
| How to read the labels box | Cut | Rubric: keep once in A0 only | 45 |
| Part 1 — Assembling the Pack | Keep, fix table and tree | Missing curriculum items; review files have no folder | −30 (added) |
| Part 2 — Reviewing It Yourself | Keep | Rubric is the core tool; trim closing box slightly | 15 |
| Part 3 — Reference Review | Shrink | Restated moral, retold weak points, Try-it duplicates activity and MCQ 2 | 160 |
| Part 4 — Version 2 | Shrink | Fix invented v2 plan; tighten closing paragraph | 65 |
| Putting It All Together / Self-Check | Keep | Produces the deliverable | 0 |
| Check Your Understanding | Keep, fix Q4 | Q4 tests recall with joke distractors | 0 |
| What You Can Now Do | Shrink to one sentence | Restates the outcomes list | 55 |
| References + Note on numbers | Shrink | The unit has no component values or prices | 50 |

## Findings

### F1 · P1 · STRUCTURE · L44 · "What Goes In"
> | 3 | Part selection | Sensor selection matrix, module-versus-IC table, costed BOM with lifecycle | B0, B4, F0 |

**Proposed:** | 3 | Part selection | Sensor selection matrix, interface choice table, module-versus-IC table, costed BOM with lifecycle | B0, B1, B4, F0 |
**Why:** CURRICULUM pack item 2 requires interface choices (B1); the pack omits them.
- [x] applied

### F2 · P1 · STRUCTURE · L48 · "What Goes In"
> | 7 | Mechanical | CAD assembly, board STEP, sliced enclosure file, DFM audit, functional design notes | C0, E0–E5 |

**Proposed:** | 7 | Mechanical | Concept sketches, CAD assembly, board STEP, material choice, rendered image, hardware list, sliced enclosure file, DFM audit, functional design notes | C0, E0–E5 |
**Why:** CURRICULUM pack items 5 and 8 need form-factor concept, material choice, render and hardware list.
- [x] applied

### F3 · P1 · FACT · L206 · "Where the Reference Is Weak, Say So"
> - **Thickness.** The board with its parts is 14.044 mm tall, because the display sits on standoffs above the motion sensor, and no thickness limit was written first (A0, C0, E2).

**Proposed:** - **Thickness.** The board with its parts is 14.044 mm tall, set by the modules standing on standoffs and header sockets (E2).
**Why:** "Display above the motion sensor" and "no limit written first" are not in REFERENCE-PRODUCT.md; E2 owns this story.
- [x] applied (adapted to author facts 2026-09-29)

### F4 · P1 · FACT · L211 · "Where the Reference Is Weak, Say So"
> - **Its specification was written after the build**, so it could only describe the design, not steer it (A0).

**Proposed:** **Delete.** (Or keep and add `<!-- FACT:VERIFY spec written after build — not in REFERENCE-PRODUCT.md, which says the design ran "from problem statement through schematic" -->`.)
**Why:** Not in REFERENCE-PRODUCT.md; its §1 implies the opposite order.
- [x] applied

### F5 · P1 · FACT · L247 · "Part 4 — Version 2, on One Page"
> For comparison, esp_watch's own version 2 direction, from its recorded known issues and the units of this course, would include: replacing the obsolete MPU-6050 (TDK names the ICM-42670-P as its recommended alternate), which is a new driver behind the existing interface;

**Proposed:** For comparison, a version 2 page for esp_watch, written from its open issues, might include: replacing the obsolete MPU-6050 (TDK names the ICM-42670-P as its recommended alternate), which is a new driver behind the existing interface;
**Why:** REFERENCE-PRODUCT §8 says esp_watch keeps the MPU-6050; the author has no recorded v2 plan.
- [x] applied

### F6 · P2 · CUT · L12 · "This Pack Is Your Proposal"
> Over this course you have written a specification, drawn an architecture, designed a circuit and a board, planned firmware, modelled a case and costed a build. Each piece lives in a different file, made at a different time.

**Proposed:** **Delete.**
**Why:** Recap the student already knows; the next paragraph carries the point.
- [x] applied

### F7 · P2 · TIGHTEN · L14 · "This Pack Is Your Proposal"
> **This Design Pack is exactly what you submit when you apply for the funded build.** A reviewer deciding whether to fund your product will not read thirty separate files in random order. They will open one folder, read one README, and ask three questions:

**Proposed:** **This Design Pack is exactly what you submit when you apply for the funded build.** A reviewer will open one folder, read one README, and ask three questions: *Is this a real problem? Is the design complete enough to build? Does this person know where the risks are?* This unit turns your work into a pack that answers all three, checks it against a rubric, and compares it with the reference watch.
**Why:** Same message in about 60 words instead of 95.
- [x] applied

### F8 · P2 · CUT · L23 · "What Parts 1 and 2 Already Covered"
> ### What Parts 1 and 2 Already Covered

**Delete section through:** "…in a form that someone who has never met you can review and fund."
**Why:** Nothing specific; the opening already says the pack is a funding proposal.
- [x] applied

### F9 · P2 · CUT · L27 · labels box
> > **How to read the labels in this material.**

**Delete section through:** "> - **Assumption** — something this reading assumes because your tools or kit will define it precisely."
**Why:** Rubric: labels box lives in A0 only. The unit barely uses the labels.
- [x] applied

### F10 · P2 · STRUCTURE · L67 · "A Structure a Reviewer Can Navigate"
> ├── 09-version-2.md

**Proposed:**
```text
├── 09-version-2.md
├── rubric-review.md           ← the rubric, answered Y/N
├── reference-review.md        ← converge / diverge / justify
```
**Why:** Header promises a self-review and reference comparison; the tree gives them no home.
- [x] applied

### F11 · P2 · CUT · L178 · "Comparing With the Reference Watch"
> The third question is the heart of it. A divergence you can justify shows judgement. A divergence you cannot justify shows you something to learn, and writing that down is just as valuable.

**Proposed:** **Delete.**
**Why:** Said again in the "Check" paragraph after the worked example.
- [x] applied

### F12 · P2 · CLARITY · L180 · "Worked Example"
> ### Worked Example: Two Rows of a Reference Review

**Proposed:** ### Worked Example: Three Rows of a Reference Review
**Why:** Three rows are shown and the "Check" paragraph refers to "the third".
- [x] applied

### F13 · P2 · TIGHTEN · L197 · "Worked Example"
> **Check.** The first row justifies a divergence from a requirement. The second converges but improves on how the risk is handled. The third found a mistake and fixed it. All three are good outcomes. The only bad outcome is a divergence left unexamined.

**Proposed:** **Check.** Row 1 justifies a divergence with a requirement. Row 2 converges but handles the risk better. Row 3 found a mistake and fixed it. The only bad outcome is a divergence left unexamined.
**Why:** Drops a sentence that adds nothing.
- [x] applied

### F14 · P2 · TIGHTEN · L201 · "Where the Reference Is Weak, Say So"
> The reference watch is the course author's own design, not a polished commercial product. It has known issues, and the course has pointed them out as it went. Your review is expected to criticise it where your design does better.

**Proposed:** esp_watch is the course author's own design, with known issues. Criticise it wherever your design does better.
**Why:** Three sentences into two; the list below shows the issues.
- [x] applied

### F15 · P2 · CUT · L216 · "Where the Reference Is Weak, Say So"
> > **Try it: Find your best divergence.** Look through your reference review.

**Delete section through:** "> 3. **Explain.** Does your strongest divergence rest on a requirement, a calculation or a preference? Only the first two will persuade a funding panel."
**Why:** Same point as the Justification column, activity step 5 and MCQ 2. Try-its are optional.
- [x] applied

### F16 · P2 · TIGHTEN · L250 · "Part 4 — Version 2, on One Page"
> The "test first" section matters most for the funded build. Nothing in this course was built. Your pack is a design that has been checked in every way that does not need hardware. The build exists to check the rest, and a pack that says exactly what to check first is a pack that can be funded with confidence.

**Proposed:** The "test first" section matters most. Your pack has been checked in every way that needs no hardware; the build checks the rest, so say exactly what to measure first.
**Why:** Four sentences restating one idea; MCQ 4 repeats it too.
- [x] applied

### F17 · P2 · STRUCTURE · L343 · "Check Your Understanding"
> **4.** Why should the version 2 page include "things I would test first in the funded build"?

**Replace question, options and answer through:** "**D** is too pessimistic; the point is to find out quickly."
**Proposed:**
**4.** Your current budget is modelled, and your battery-life requirement is met with only 10 % margin. Where does this belong in your version 2 page?

- A. Nowhere; the requirement is met.
- B. Under "things I would test first": measure real current in every mode, and state what result would force a bigger cell or lower sleep current.
- C. Under "changes that improve the product", as longer battery life.
- D. Only in the README's key numbers.

Answer: **B.** A modelled figure with thin margin is a risk only hardware can close, so it is tested first. **A** treats a model as a measurement. **C** calls a risk an improvement. **D** reports the number but hides the risk.
**Why:** Current Q4 is recall, with joke distractors ("to make the page longer").
- [x] applied

### F18 · P2 · CUT · L373 · "What You Can Now Do"
> ## What You Can Now Do

**Delete section through:** "That is what this Design Pack shows, and it is what makes it ready to build."
**Proposed replacement for the whole section:** **A design is finished not when it looks right, but when every requirement is traced, every check is recorded, and every remaining risk is named.**
**Why:** The bullets restate the outcomes list; keep only the closing idea.
- [x] applied

### F19 · P2 · CUT · L388 · "References"
> > **Note on numbers.** Component values, prices and specifications in this reading are

**Delete section through:** "> supplier listing for the part you are actually using."
**Why:** This unit has no component values or prices.
- [x] applied

### F20 · P3 · CUT · L113 · "The Verification Log"
> It is the evidence that your design has been checked by something other than your own confidence.

**Proposed:** **Delete.**
**Why:** Repeats the verification stack page nearly word for word.
- [x] accept

### F21 · P3 · TIGHTEN · L162 · "The Rubric"
> > **Teaching model.** A rubric of binary items cannot tell you whether a design is *good*. It tells you whether it is *complete* and *checked*. Good judgement shows up in the comparison and the version 2 page, which is where the next two parts come in.

**Proposed:** A yes/no rubric tells you whether a design is *complete* and *checked*, not whether it is *good*. Judgement shows in the reference review and the version 2 page.
**Why:** A rubric is not a simplified model; drop the label and a sentence.
- [x] accept

### F22 · P3 · CUT · L170 · "Comparing With the Reference Watch"
> Throughout the course, the reference watch, esp_watch, has been used as a worked example, including the places where it got things wrong. Now compare your design with it deliberately, section by section.

**Proposed:** Now compare your design with esp_watch, section by section.
**Why:** The student knows what esp_watch is; "deliberately" is a flagged filler word.
- [x] accept

### F23 · P3 · CUT · L225 · "Part 4 — Version 2, on One Page"
> The last page of the pack looks forward. It is short, and it is where a reviewer sees whether you understand your own design.

**Proposed:** **Delete.**
**Why:** The heading and template already say this.
- [x] accept
