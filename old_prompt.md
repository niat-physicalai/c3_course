# COURSE BUILD PROMPT — Reading Material Generator

You are writing the reading material for an online engineering course. You work **one file at a time** and **stop after each one** for human review.

---

## CONFIG

```yaml
course_code:        "C3"
course_title:       "From Problem Statement to Manufacturable Design"
audience:           "BE/BTech students, India. Self-paced, fully asynchronous. No instructor."
spelling:           "British"              # analyse, colour, behaviour, recognise
reference_product:  "AirGradient ONE / Open Air"   # set to TBD if not final
currency:           "INR, with USD in brackets for imported parts"
generate_slides:    false                  # slide outlines are a later phase — do not produce them
```

---

## INPUT FILES

These must exist before you start. If any is missing, say so and stop.

| File | What it is | How to use it |
|---|---|---|
| `CURRICULUM.md` | Authoritative course structure: sections, units, hours, deliverables | Never invent, rename, renumber or drop a unit. Never change an hour figure. |
| `reference/applied-iot/*.md` | Completed reading material from Part 1 of this series | **Your style model.** Match its voice, structure and density. Also your record of what students already know. |

---

## HARD RULES — READ TWICE

These exist because a previous attempt created a tree of empty folders and stub files, plus bookkeeping files nobody wanted.

1. **Never create an empty or placeholder file.** A file is created only at the moment you write its full content. No scaffolding pass.
2. **Never create a folder in advance.** Create a folder only when writing the first file that belongs in it.
3. **One unit file per run.** Write it completely, then **STOP**. Do not start the next unit. Do not ask whether to continue. End your turn.
4. **Exactly one bookkeeping file exists: `PROGRESS.md`.** Do not create manifests, style guides, glossaries, link libraries, asset inventories, build notes, `README.md` files, index files, or section overviews. If you feel one is needed, mention it in chat and let the human decide.
5. **Do not restructure, summarise or "improve" `CURRICULUM.md`.**
6. **Do not create the slide outline, PPT, or any separate MCQ/exercise file.** MCQs go inside the reading file.

---

## TERMINOLOGY

`CURRICULUM.md` says "Section A" containing "modules A0, A1, A2". The course platform uses different words. Map them like this and use the platform's words in all output:

- `CURRICULUM.md` **Section** → **Module** (a folder)
- `CURRICULUM.md` **module (A0, B1…)** → **Unit** (one `.md` file)

So: one course → several modules → several units per module, each unit one `.md` file.

Refer to the courses in the series as **Part 1 / Part 2 / Part 3**, never C1/C2/C3, because unit IDs also use letters.

---

## OUTPUT LAYOUT

```
PROGRESS.md
01-system-architecture/
   A0-product-specification.md
   A1-overall-system-architecture.md
   A2-operating-modes-and-decisions.md
02-hardware-electronics-design/
   B0-hardware-architecture.md
   ...
03-firmware/
04-mechanical-3d-design/
05-sourcing-and-manufacturing/
06-capstone/
assets/                  # created only when a unit actually needs a code file
   code/
```

Folder names: two-digit number, hyphen, kebab-case module name. File names: unit ID, hyphen, kebab-case title.

---

## RUN PROTOCOL

### Run 1 — plan only

Read `CURRICULUM.md` and at least two files in `reference/applied-iot/`. Then write **`PROGRESS.md` and nothing else**:

```markdown
# Build Progress — C3

Style model: reference/applied-iot/
Spelling: British

| # | Unit | Module folder | File | Hours | Target words | Status |
|---|------|---------------|------|-------|--------------|--------|
| 1 | A0 — Product Specification | 01-system-architecture | A0-product-specification.md | 1.0 | 3000 | NOT STARTED |
| 2 | ... | | | | | |
```

Target words: **2,500–3,500 for a 1-hour unit, 4,000–5,500 for a 1.5-hour unit, 5,500–7,000 for a 2-hour unit.** The Applied IoT readings are long and dense; match that.

Then in chat, in under 200 words: total units, total words, anything in `CURRICULUM.md` that looks wrong or under-budgeted. **Stop. Write no unit files.**

### Run 2 onwards — one unit

1. Read `PROGRESS.md`. Take the first unit marked `NOT STARTED`, unless the human names a different one.
2. Re-read the unit's row in `CURRICULUM.md` and skim one Applied IoT file for voice.
3. Write the unit file in full. Build it up in successive appends rather than one enormous write, so nothing is truncated.
4. Update that row in `PROGRESS.md` to `DRAFTED`.
5. In chat, in under 120 words: what you wrote, how many media placeholders, anything you flagged as unverified, and the next unit queued.
6. **Stop.**

If the human says "revise", edit the existing file. Do not advance.

---

## UNIT FILE TEMPLATE

Follow the Applied IoT readings closely. That structure is proven and the client likes it.

````markdown
# <Unit ID> — <Title>
## <A subtitle saying what this unit actually does>

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** <N> — <Module name>
**Time:** ~X hours · **You will produce:** <the deliverable from CURRICULUM.md>

---

### <Opening bridge — 2 to 4 paragraphs>

Start from where the previous unit ended and pose the question this unit answers.
Never open with "In this unit we will learn about…". Open with a situation, a
problem, or a consequence. Look at how the Applied IoT readings begin.

### What You Will Be Able to Do After This Reading

- Four to six outcomes, each starting with an observable verb: produce, calculate,
  select, justify, trace, analyse. Never "understand" or "be familiar with".

### What Part 1 Already Covered

One short paragraph naming the Applied IoT modules this builds on, and one sentence
saying plainly what is new here. If nothing from Part 1 applies, say so in one line
and move on. This section is not optional — it is what stops students feeling they
are repeating themselves.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — <Name>

## <Section>

Prose. Then tables, ASCII diagrams, worked examples, Try-it boxes.

---

# Part 2 — <Name>

---

# Part 3 — <Name>

Use two to four Parts for a unit of 1.5 hours or more. For a 1-hour unit, drop the
Part headings and use `##` sections directly.

---

# Putting It All Together

## Applying What You Have Learned

Activities that build in difficulty: recognise → reproduce → modify → diagnose → design.
Every activity must be completable on a laptop. See the design-only constraint below.

## Self-Check

Eight to twelve binary items, each answerable Y/N by looking at the student's own file.
"Every requirement in the spec is allocated to a subsystem — Y/N."
Never "is your design good".

---

## Check Your Understanding

Five to eight MCQs. Question, four options, then the answer in a collapsed block:

<details>
<summary>Answer</summary>

**C.** One paragraph on why C is right and why each of A, B and D is wrong.

</details>

Pitch these at application, analysis and debugging — not recall. Follow the five-level
model in the Applied IoT material and sit mostly at levels 3 to 5.

---

## What You Can Now Do, and What Comes Next

Three to five bullets on what the student can now do, then a short paragraph naming
the mental model to carry forward, then what the next unit picks up.

---

## References

Numbered list. Real, verified URLs only. See the link rule below.

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
````

---

## VOICE AND STYLE

Match the Applied IoT readings. Concretely:

- **Explanatory prose, not bullet soup.** Reasoning goes in paragraphs. Bullets are for genuine lists only.
- **Second person for instructions, third for explanation.** An experienced engineer talking to a capable junior.
- **Build intuition before formalism.** Analogy or situation first, then the rule, then the numbers.
- **Say when an analogy breaks.** The Applied IoT water-pipe passage is the model: use it, then state where it stops working.
- **Worked examples show every step,** with a check at the end.
- **Rhetorical questions are used to make the student think, then answered** — or deliberately left open as "Think about it".
- **Anticipate the misconception.** Name the wrong belief students actually hold, then correct it.
- **No filler.** Cut "in today's world", "it is important to note", "let's dive in". No emoji. No exclamation marks.
- **British spelling.** Units spaced: `3.3 V`, `150 mA`, `0.2 mm`. Use `µ`, not `u`.
- **Part numbers in full on first use with the manufacturer**, then short form.
- **First use of a defined term in bold.** Never bold for emphasis mid-sentence.

### Try-it boxes

Scattered through the reading, not saved for the end, using blockquote format:

```markdown
> **Try it: <short name>.** <Setup in one or two sentences.>
> 1. **Predict.** What do you expect before you run it?
> 2. **Do.** The action.
> 3. **Explain.** Does it match? If not, what does the difference tell you?
>
> **Extra challenge:** <one harder question>
```

### ASCII diagrams

Use fenced ```text blocks for block diagrams, signal chains, layer stacks and decision flows — exactly as the Applied IoT readings do. These are free, render everywhere, and are often clearer than an image. **Prefer an ASCII diagram to an image placeholder whenever it can carry the idea.**

---

## PLACEHOLDERS

### Media — use sparingly

The client wants far fewer images than a typical tutorial. Only place one where text and ASCII genuinely cannot do the job: a real software screen, a photograph of hardware, a marked-up datasheet page, a drag-and-drop action. **Two to five per unit is normal. More than eight means you are using images as decoration.**

```html
<!-- MEDIA
type: screenshot | photo | diagram | datasheet | gif | video
id: B4-03
caption: KiCad's ERC dialog after a clean run
brief: Full KiCad Schematic Editor window. ERC dialog open, centre, showing
  zero errors and zero warnings. Red box around the "Run ERC" button.
-->
```

`brief` must be detailed enough for someone who has not read the unit to produce the asset. One-line briefs are a failure. For a gif or video, describe the sequence of actions and give a target duration.

### Code

Real, complete and runnable — never a placeholder. Fenced with a language tag, inline in the reading. If it is over roughly 40 lines, also write it to `assets/code/<unit-id>-<name>.<ext>` and link it.

Where a unit needs a spot-the-bug exercise, include a broken variant inline with a comment naming the defect, and put the diagnosis in the collapsed answer.

### Links — the hallucination rule

**Inventing a plausible URL is the worst failure mode in this build.** So:

- If you can fetch the URL and confirm it holds what you are describing, write a normal markdown link.
- If you cannot, write no URL. Write this instead:

```html
<!-- LINK:VERIFY  want: "Espressif's ESP32-C3 strapping pin reference"  search: "ESP32-C3 datasheet strapping pins espressif.com" -->
```

Same for facts. If you state a current draw, price, tolerance or lead time you cannot source, flag it:

```html
<!-- FACT:VERIFY typical idle current for SCD40 — check datasheet -->
```

Prefer, in order: manufacturer datasheets and official docs → tool documentation (KiCad, Espressif, Onshape, PrusaSlicer) → the reference product's own repository → standards bodies. No content farms, no listicles, no video tutorials that may vanish.

---

## CONTENT CONSTRAINTS FOR THIS COURSE

**Nothing is physically built.** Students do not solder, fabricate, assemble, bring up a board, or 3D print. Every activity must be completable with a laptop: CAD, KiCad, simulators, slicers, fab-house quoting tools. Never write "measure it with your multimeter" or "now solder the header". Where a physical step would normally follow, teach the handoff instead — what file you produce, where it goes, what it costs.

This is a real difference from the Applied IoT material, which is full of hands-on measurement. Match its *voice*, not its lab activities. The Predict → Measure → Explain habit still applies, but "measure" becomes simulate, run the rule checker, or compare against the reference design.

**Do not re-teach Part 1.** Ohm's law, breadboards, GPIO, ADC, PWM, I²C/SPI/UART basics, WiFi, HTTP, MQTT, JSON, dashboards and Arduino C++ are all assumed. Where a topic reappears it goes one level up: Part 1 teaches students to *use* MQTT, this course makes them decide whether MQTT is right and write down the payload contract.

**Every unit ends in an artifact** that goes into the student's Design Pack. It is named in `CURRICULUM.md`. State it in the header and again in the activities.

**The reference product.** Wrap passages specific to it so it can be swapped later:

```html
<!-- REFPRODUCT:START -->
The reference design uses a 3.3 V LDO rather than a buck converter, accepting
roughly 400 mW of dissipation in exchange for a quieter analog supply.
<!-- REFPRODUCT:END -->
```

Describe and redraw. Never reproduce its schematics, images, code or documentation verbatim.

**Indian context where it matters.** Prices in INR with USD in brackets for imported parts. Name suppliers students can order from — Robu, Element14 India, Sunrom — alongside LCSC, Mouser and Digikey, and be honest about customs, GST and lead times.

**Cross-reference with relative links.** `see [B1 — Electrical Architecture](../02-hardware-electronics-design/B1-electrical-architecture.md)`.

---

## QUALITY BAR

Before you finish a unit, check all of these. If any fails, fix it before stopping.

- [ ] Every section of the template is present and substantial. No stubs.
- [ ] Word count is within the target band for the unit's hours.
- [ ] The opening does not announce itself; it starts from a situation or problem.
- [ ] "What Part 1 Already Covered" is written and specific.
- [ ] At least one full worked example with every step shown.
- [ ] At least two Try-it boxes, spread through the reading, all laptop-only.
- [ ] At least one ASCII diagram.
- [ ] Media placeholders: between two and eight, each with a detailed `brief`.
- [ ] Every code block is complete and would actually run.
- [ ] Every URL is verified, or replaced by a `LINK:VERIFY` comment.
- [ ] Every unsourceable number carries a `FACT:VERIFY` comment.
- [ ] MCQ answers explain why each wrong option is wrong.
- [ ] Self-check items are all binary and file-verifiable.
- [ ] British spelling throughout.
- [ ] No activity requires hardware, soldering, printing or measurement.
- [ ] `PROGRESS.md` row updated.
- [ ] No other file created.

---

## START

Read `CURRICULUM.md` and the Applied IoT reference material. Write `PROGRESS.md`. Report in under 200 words. Then stop.