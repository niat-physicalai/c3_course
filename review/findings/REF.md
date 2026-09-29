# Findings — REF The Verification Stack

**Words now:** 1185 · **After accepted cuts (est.):** 860 (−27 %)
**Verdict:** The page gives the same check list twice (the "at a glance" block and the full table) and retells the green-MAX story, which B3 owns.

Note on assessment: `CURRICULUM.md` §8 and `PROGRESS.md` define this as an untimed reference page with no deliverable, so the 5-MCQ / 8-item self-check rule is not applied. Leave it that way unless the author decides otherwise.

## Section-level calls
| Section | Keep / Shrink / Cut / Merge into … | Reason (≤ 15 words) | ~Words saved |
|---|---|---|---|
| Header + subtitle | Keep | Needed to find the page | 0 |
| Why This Page Exists | Shrink | Two paragraphs for one point; rhetorical question padding | 60 |
| The Stack at a Glance | Merge into The Full Table | Same rows twice; move only the Specification row across | 150 |
| The Full Table | Keep (+1 row, 1 paragraph tightened) | Core of the page | 30 |
| What a Pass Does Not Tell You | Shrink | Cut moral, cut the "professional teams" aside, cut the weak I²C example | 45 |
| REFPRODUCT block | Shrink to pointer | Story owned by B3 (clamp) and D5 (OLED) | 40 |
| How to Use This Page | Keep | Short, actionable | 0 |
| References | Keep | Needed | 0 |

## Findings

### F1 · P2 · REPEAT · L72 · "What a Pass Does Not Tell You"
> The reference watch shows why both warnings matter. On its breadboard prototype, one version of the heart-rate module pulled the shared I²C bus down to 1.82 V, and the motion sensor then failed 80% of its reads. … That is exactly the kind of problem the funded build exists to find, and the reason this page never says "verified" when it means "simulated".

**Proposed:** The reference watch shows why both warnings matter. On the breadboard, one heart-rate module broke the shared I²C bus. No DRC or simulator would have caught it (full story in B3; why the display hid it in D5). That is why this page never says "verified" when it means "simulated".
**Why:** B3 owns the 1.82 V clamp and D5 owns the OLED story. Keep the lesson here and point to them.
- [x] applied

### F2 · P2 · CUT · L17 · "The Stack at a Glance"
> ## The Stack at a Glance

**Delete section through:** `Every choice           Are my choices sound?              Comparison with the reference watch` and the closing ```` ``` ```` fence (L39).
**Why:** It repeats every row of the full table below. Its one extra row moves across in F3.
- [x] applied

### F3 · P2 · STRUCTURE · L43 · "The Full Table"
> | Question | Tool that answers it | What "pass" looks like |
> |---|---|---|
> | Is my architecture coherent? |

**Proposed:**
```
| Question | Tool that answers it | What "pass" looks like |
|---|---|---|
| Is every requirement checkable? | Your specification | Every requirement has an ID, a number and a test method |
| Is my architecture coherent? |
```
**Why:** Keeps the Specification row, which only the deleted glance block had. Needed only if F2 is accepted.
- [x] applied

### F4 · P2 · TIGHTEN · L13 · "Why This Page Exists"
> In Part 1, you knew a circuit worked because the LED lit up or the sensor printed a sensible number. In this course you will not build anything. … This page lists them in one place, so that whenever you finish something you know exactly what to run before calling it done.

**Proposed:** In Part 1, you knew a circuit worked because the LED lit up or the sensor printed a sensible number. In this course nothing is built until the funded build. So for each stage of the design, this page names the check that gives a clear pass or fail. Run it before you call the work done.
**Why:** The rhetorical question and "hoping is not an answer" add nothing. Two paragraphs become one.
- [x] applied

### F5 · P2 · CLARITY · L67 · "What a Pass Does Not Tell You"
> The fix is a habit that professional firmware teams use anyway: write a **mock sensor**, a small piece of code that stands in for the real sensor and returns made-up but realistic readings. Your application code cannot tell the difference, so you can still test everything around the sensor. You will do this in the firmware module.

**Proposed:** The fix is a **mock sensor**: a small piece of code that stands in for the real sensor and returns made-up but realistic readings. Your application code cannot tell the difference, so you can still test everything around the sensor. You write one in B5 and reuse it in the firmware module.
**Why:** The mock sensor is first written in B5 (its story owner), not the firmware module. "Professional teams" aside is padding.
- [x] applied

### F6 · P3 · CUT · L69 · "What a Pass Does Not Tell You"
> Simulators also idealise. Wokwi's I²C bus, for example, runs the ESP32 only as the controller on the bus [1], and no simulator reproduces a badly soldered joint, a weak battery or a noisy wrist.

**Proposed:** Simulators also idealise: none reproduces a badly soldered joint, a weak battery or a noisy wrist.
**Why:** "Controller only" is a missing feature, not idealisation, and the student cannot use it here. If accepted, reference [1]'s note about "Master only" can go too.
- [ ] accept

### F7 · P3 · TIGHTEN · L59 · "The Full Table"
> The last row matters most in a course with no instructor. Whenever your design differs from the reference watch, you must be able to say why. Sometimes your reason will be better than the reference's. The reference watch is the course author's own work, not a polished commercial product, and it has known flaws that you are encouraged to criticise.

**Proposed:** The last row matters most. Whenever your design differs from the reference watch, write down why; your reason may be the better one. The watch is the author's own work, not a commercial product, and you are encouraged to criticise its known flaws.
**Why:** Same content, fewer words.
- [ ] accept

### F8 · P3 · CUT · L63 · "What a Pass Does Not Tell You"
> Every tool on this page has limits. Two catch students out more than any others.

**Proposed:** Two limits catch students out more than any others.
**Why:** The first sentence is implied by the heading.
- [ ] accept

### F9 · P3 · CUT · L65 · "What a Pass Does Not Tell You"
> A board can pass DRC perfectly and still be useless.

**Delete.**
**Why:** It repeats the bold opening sentence of the same paragraph.
- [ ] accept

### F10 · P3 · CUT · L83 · "How to Use This Page"
> By the end of the course, that record shows a reviewer that every part of your design has been checked by something other than your own confidence.

**Delete.**
**Why:** It is a closing moral. The three steps are enough on their own.
- [ ] accept
