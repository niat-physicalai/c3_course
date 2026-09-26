# F — Capstone: The Design Pack and the Reference Review
## Turning Thirty Deliverables into One Proposal Someone Can Fund

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 6 — Capstone
**Time:** ~2 hours, plus your own pace · **You will produce:** a complete Design Pack, a self-review against the rubric, a comparison with the reference watch, and a one-page "what I would change in version 2"

---

### This Pack Is Your Proposal

Over this course you have written a specification, drawn an architecture, designed a circuit and a board, planned firmware, modelled a case and costed a build. Each piece lives in a different file, made at a different time.

**This Design Pack is exactly what you submit when you apply for the funded build.** A reviewer deciding whether to fund your product will not read thirty separate files in random order. They will open one folder, read one README, and ask three questions: *Is this a real problem? Is the design complete enough to build? Does this person know where the risks are?* This unit turns your work into a pack that answers all three quickly, checks it against a rubric, and ends with the most honest section of all: a comparison with the reference watch, including where your design is better.

### What You Will Be Able to Do After This Reading

- **Assemble** every deliverable from the course into a single, navigable Design Pack.
- **Review** your pack against a binary rubric, and **fix** what fails.
- **Compare** your design with the reference watch, and **justify** every divergence.
- **Write** a one-page version 2 plan that names your design's real risks.

### What Parts 1 and 2 Already Covered

Part 1 ended with a final project that you demonstrated and explained. Part 2 gave you the problem statement this course began from. **What is new here** is presenting a complete design, not a demonstration, in a form that someone who has never met you can review and fund.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Assembling the Pack

## What Goes In

The Design Pack has nine sections. Every one is something you have already made:

| # | Section | Contents | From |
|---|---|---|---|
| 1 | Specification and system architecture | Spec, context diagram, subsystem breakdown, allocation table, state diagram, failure table, ADRs | A0, A1, A2 |
| 2 | Hardware architecture | Block diagram, interface table, power tree, current budget, pin map | B0, B1 |
| 3 | Part selection | Sensor selection matrix, module-versus-IC table, costed BOM with lifecycle | C3, B2, E0 |
| 4 | Schematic and PCB | KiCad project (ERC and DRC clean), your own symbols and footprints, footprint checklist | B4, B5 |
| 5 | Firmware design | Architecture diagram, module table, flowchart, state diagram, sequence diagram | C0, C1 |
| 6 | Firmware and simulation | Firmware repository with README, serial protocol doc, payload contract, working simulation link | C2–C6, B3 |
| 7 | Mechanical | CAD assembly, board STEP, sliced enclosure file, DFM audit, functional design notes | D0–D5 |
| 8 | Manufacturing | Fabrication zip with annotation, DFM reports, three-tier cost model | E1, E2 |
| 9 | Version 2 | One page: what you would change and why | This unit |

## A Structure a Reviewer Can Navigate

Use numbered folders matching the sections, so the order is obvious:

```text
design-pack/
├── README.md                  ← start here
├── 01-spec-and-architecture/
├── 02-hardware-architecture/
├── 03-part-selection/
├── 04-schematic-and-pcb/
├── 05-firmware-design/
├── 06-firmware-and-simulation/
├── 07-mechanical/
├── 08-manufacturing/
├── 09-version-2.md
└── verification-log.md        ← every check you ran, its date and result
```

Keep every file in a format a reviewer can open without your tools: diagrams as images or Mermaid text, spreadsheets as `.xlsx` or `.csv`, KiCad and CAD files alongside PDF or image exports of the key views.

## The README: One Page That Explains the Rest

The README is the first thing a reviewer reads, and often the only thing they read carefully. Keep it to one page:

```markdown
# <Product name> — Design Pack v1.0

## The problem
Two sentences, from your Part 2 problem statement.

## The product
Three sentences: what it is, who wears or uses it, what it does.
One image: the CAD render with the board inside.

## Key numbers
| Battery life (usage pattern UP-1) | Size (W × L × H) | Unit cost at 10 / 100 / 1,000 |
|---|---|---|

## Status of every check
| Check | Result | Where |
|---|---|---|
| ERC | 0 errors | 04-schematic-and-pcb/ |
| DRC | 0 errors, N accepted warnings | 04-schematic-and-pcb/ |
| Interference | 0 overlaps | 07-mechanical/ |
| Fab DFM | resolved | 08-manufacturing/ |
| Simulation | link | 06-firmware-and-simulation/ |

## Top three risks
1. ...
2. ...
3. ...

## How to read this pack
One line per folder.
```

The "top three risks" section matters more than it looks. A reviewer who sees you have named your own risks trusts the rest of the pack more, not less.

## The Verification Log

In the verification stack page at the start of the course, you were asked to record every check: what, when and the result. Gather those records into one `verification-log.md`. For each row, include what the check did **not** cover, as B3 taught for simulations. It is the evidence that your design has been checked by something other than your own confidence.

<!-- MEDIA
type: screenshot
id: F-01
caption: A well-organised Design Pack: numbered folders and a one-page README
brief: A file browser (or GitHub repository view) showing a design-pack folder with the
  numbered subfolders 01 to 08, README.md, 09-version-2.md and verification-log.md. Beside
  it, the README rendered: a title, a two-sentence problem, a CAD render thumbnail of a
  small wrist device, a key-numbers table and a status-of-checks table with green ticks.
  Clean, readable, no personal details.
-->

---

# Part 2 — Reviewing It Yourself

## The Rubric

There is no instructor to mark your pack, so you review it yourself, with a rubric of yes-or-no items that can each be checked by opening a file. Work through it honestly. Every "no" is either fixed or written down as a known gap in the README.

| Section | Rubric item | Y/N |
|---|---|---|
| **Spec** | Every requirement has an ID, a number, a condition and a check method | |
| | The battery requirement names a usage pattern | |
| | An out-of-scope list exists, with reasons | |
| **Architecture** | Every requirement has exactly one owner in the allocation table | |
| | The state diagram has no traps, and every event is handled in every state | |
| | At least three ADRs exist, with context, options and consequences | |
| **Hardware** | Every connection in the block diagram has a row in the interface table | |
| | The current budget gives a runtime that meets the spec, with sources | |
| | No strapping pin is held at the wrong level at reset | |
| **Parts** | Every active part has an MPN, a second source and a lifecycle status | |
| | Every sensor choice names a rejected alternative | |
| **Schematic and PCB** | ERC: zero errors | |
| | DRC: zero errors, and every accepted warning has a reason | |
| | Every footprint has its four measurements recorded | |
| **Firmware** | No blocking calls in the main loop | |
| | Code transitions match the state diagram, arrow for arrow | |
| | Every external dependency has a timeout and a failure path | |
| | A simulation link runs without errors | |
| **Mechanical** | Interference check: zero overlaps | |
| | The sensor, if any, reaches the skin in a section view | |
| | The enclosure is sliced, with a time and material estimate | |
| **Manufacturing** | The fabrication zip is annotated file by file | |
| | Unit cost is given at 10, 100 and 1,000, with sources | |
| **Pack** | The README fits on one page and names three risks | |
| | Every check in the README links to its evidence | |

> **Teaching model.** A rubric of binary items cannot tell you whether a design is *good*. It tells you whether it is *complete* and *checked*. Good judgement shows up in the comparison and the version 2 page, which is where the next two parts come in.

---

# Part 3 — The Reference Review

## Comparing With the Reference Watch

Throughout the course, the reference watch, esp_watch, has been used as a worked example, including the places where it got things wrong. Now compare your design with it deliberately, section by section.

For every section, answer three questions:

1. **Where did you converge?** You made the same choice. Was it for the same reason?
2. **Where did you diverge?** You made a different choice.
3. **Can you justify each divergence?** Either your product's requirements are different, or your choice is better, or you have learned something.

The third question is the heart of it. A divergence you can justify shows judgement. A divergence you cannot justify shows you something to learn, and writing that down is just as valuable.

### Worked Example: Two Rows of a Reference Review

<!-- REFPRODUCT:START -->
A student's product is a hostel activity tracker with semester history. Their reference review includes:

| Topic | esp_watch | My design | Converge / diverge | Justification |
|---|---|---|---|---|
| Connectivity | WiFi once at first boot, then off (ADR-002) | BLE to a phone app | Diverge | My spec requires semester history (FR-05), which A1 showed esp_watch cannot deliver; BLE sends small daily summaries at low radio power, and the phone stores the history |
| Motion sensor | MPU-6050, obsolete, clone on the module | MPU-6050 module for the prototype, behind a `MotionSensor` interface | Converge, with a plan | Same reason as esp_watch: cheap and available now. Unlike esp_watch, my BOM records it as obsolete, and my firmware isolates it in one driver, so the v2 swap is a driver change |

And one row where the student found they could *not* justify a divergence:

| Topic | esp_watch | My design | Converge / diverge | Justification |
|---|---|---|---|---|
| I²C pull-ups | One 4.7 kΩ pair on the carrier; module pull-ups removed | Left every module's pull-ups in place | Diverge | **Cannot justify.** Recalculated: three pairs in parallel is about 1.57 kΩ, as esp_watch found. Added a fab note to remove them, as B4 recommends. |
<!-- REFPRODUCT:END -->

**Check.** The first row justifies a divergence from a requirement. The second converges but improves on how the risk is handled. The third found a mistake and fixed it. All three are good outcomes. The only bad outcome is a divergence left unexamined.

## Where the Reference Is Weak, Say So

The reference watch is the course author's own design, not a polished commercial product. It has known issues, and the course has pointed them out as it went. Your review is expected to criticise it where your design does better.

<!-- REFPRODUCT:START -->
These are the reference watch's recorded weak points, all of which appeared in earlier units:

- **Thickness.** The board with its parts is 14.044 mm tall, because the display sits on standoffs above the motion sensor, and no thickness limit was written first (A0, D0, D2).
- **An obsolete motion sensor**, a clone on its module, kept for version 1 (E0).
- **A lid held by an interference fit**, sensitive to print accuracy and loosening with use (D3).
- **Measured on a breadboard, modelled on paper.** Its bus measurements come from the breadboard prototype, and every current figure is modelled; none was measured (B1).
- **Several design decisions not yet recorded**, such as the sensor window and sweat protection (D4).
- **Its specification was written after the build**, so it could only describe the design, not steer it (A0).
<!-- REFPRODUCT:END -->

If your design avoids any of these, say how. If it repeats one, say why that was acceptable for your product.

> **Try it: Find your best divergence.** Look through your reference review.
> 1. **Predict.** Which of your divergences will a reviewer find most convincing?
> 2. **Do.** Rewrite it in two sentences: the requirement that caused it, and the evidence it works (a calculation, a check, a simulation).
> 3. **Explain.** Does your strongest divergence rest on a requirement, a calculation or a preference? Only the first two will persuade a funding panel.

---

# Part 4 — Version 2, on One Page

The last page of the pack looks forward. It is short, and it is where a reviewer sees whether you understand your own design.

Use this structure:

```markdown
# What I would change in version 2

## Changes forced by risk
Things that must change for the product to survive: an obsolete part, a failure mode
with no detection, a requirement the design only just meets.

## Changes that improve the product
Things that would make it better: thinner, longer battery life, cheaper at volume.

## Things I would test first in the funded build
The gaps your simulations and CAD could not close: what you would measure first
on real hardware, and what result would change the design.
```

For every item, give the reason in one line and trace it to a requirement, a check or a cost.

<!-- REFPRODUCT:START -->
For comparison, esp_watch's own version 2 direction, from its recorded known issues and the units of this course, would include: replacing the obsolete MPU-6050 (TDK names the ICM-42670-P as its recommended alternate), which is a new driver behind the existing interface; rethinking the module stack to reduce thickness, perhaps towards D0's concept C; a repeatable lid fastening in place of the interference fit; and, first on the list for the build, measuring real current in every mode, because every figure so far is modelled.
<!-- REFPRODUCT:END -->

The "test first" section matters most for the funded build. Nothing in this course was built. Your pack is a design that has been checked in every way that does not need hardware. The build exists to check the rest, and a pack that says exactly what to check first is a pack that can be funded with confidence.

<!-- MEDIA
type: diagram
id: F-02
caption: From design pack to funded build: what was checked on a laptop, and what the build must check
brief: A two-column graphic. Left column "Checked in this course" with icons and short
  labels: spec traced, ERC 0, DRC 0, footprints verified, simulation runs, interference 0,
  slicer preview, DFM resolved, cost model. Right column "Checked in the funded build":
  real current in every mode, sensor accuracy on a wrist, bus signals with the real
  modules, fit of the printed case, battery life, drop and sweat. An arrow from left to
  right labelled "design pack". Flat, clean style.
-->

---

# Putting It All Together

## Applying What You Have Learned

**1. Build the folder structure** and move every deliverable into its section.

**2. Write the README**, including key numbers, the status of every check and your top three risks.

**3. Compile the verification log** from every check you have run.

**4. Review against the rubric.** Fix every "no" you can; list the rest as known gaps in the README.

**5. Write the reference review**: converge, diverge and justify, for every section.

**6. Write the version 2 page**, with changes forced by risk, improvements, and what to test first.

**Deliverable:** the complete Design Pack folder.

## Self-Check

1. The pack has all nine sections, in numbered folders. — Y/N
2. The README fits on one page. — Y/N
3. The README names three risks. — Y/N
4. Every check in the README links to its evidence. — Y/N
5. The verification log lists every check with its date, result and what it did not cover. — Y/N
6. Every rubric item is answered, and every "no" is fixed or listed as a known gap. — Y/N
7. The reference review covers every section. — Y/N
8. Every divergence has a justification, or is marked "cannot justify" with what you learned. — Y/N
9. The version 2 page has all three parts, each item traced to a requirement, check or cost. — Y/N
10. Every file opens without the tool that made it, or has an exported view beside it. — Y/N

---

## Check Your Understanding

**1.** A reviewer has ten minutes for your Design Pack. What should they read first, and what must it contain?

- A. The KiCad project, because it is the most technical.
- B. The one-page README: the problem, the product, key numbers, the status of every check, and the top three risks.
- C. The firmware source code.
- D. The BOM.

<details>
<summary>Answer</summary>

**B.** The README is the map of the pack, and it tells a reviewer whether the rest is worth their time. **A**, **C** and **D** are important evidence, but each covers only one part of the design.

</details>

**2.** Your design uses a different connectivity route from the reference watch. What makes that divergence convincing?

- A. Saying your choice is more modern.
- B. Tracing it to a requirement the reference does not have, and showing evidence, such as a power calculation, that it works.
- C. Choosing the same route to avoid questions.
- D. Not mentioning it.

<details>
<summary>Answer</summary>

**B.** A requirement plus evidence is a justification. **A** is a preference. **C** avoids the question rather than answering it. **D** leaves a reviewer to wonder.

</details>

**3.** Your rubric review finds that DRC has three unexplained warnings. What should you do?

- A. Delete the rubric item.
- B. Examine each warning; fix it or write the reason it is acceptable, then update the README's check status.
- C. Mark the item "Y" because there are no errors.
- D. Re-run DRC until they disappear.

<details>
<summary>Answer</summary>

**B.** An accepted warning needs a written reason, as B5 taught. **A** and **C** hide the gap. **D** does not change the design, so the warnings will not disappear.

</details>

**4.** Why should the version 2 page include "things I would test first in the funded build"?

- A. To make the page longer.
- B. Because nothing was built in this course, so the first real measurements are where the design's remaining risks are resolved; naming them shows you know where the gaps are.
- C. Because reviewers require a test plan in every proposal.
- D. Because the design will certainly fail.

<details>
<summary>Answer</summary>

**B.** A design checked only on a laptop still has things only hardware can confirm, such as real current and real sensor accuracy. Naming them is a sign of understanding. **A** is not a reason. **C** may be true of some reviewers, but it is not why. **D** is too pessimistic; the point is to find out quickly.

</details>

**5.** In your reference review you find a divergence you cannot justify. What is the best response?

- A. Remove the row.
- B. Mark it "cannot justify", work out what the reference got right, fix your design if needed, and record what you learned.
- C. Change the reference's description to match yours.
- D. Leave it as it is and hope the reviewer does not notice.

<details>
<summary>Answer</summary>

**B.** An honest "cannot justify" followed by a fix is a strong result. **A** and **D** hide it. **C** misrepresents the reference.

</details>

---

## What You Can Now Do

- Present a complete design as one navigable pack, with a README that answers a reviewer's questions in a page.
- Review your own work against a rubric, and turn every gap into a fix or a stated risk.
- Compare your design with a reference openly, including where the reference is weaker.
- Plan version 2 and the first tests of a real build.

The idea to carry forward from the whole course: **a design is not finished when it looks right, but when every requirement is traced, every check is recorded, and every remaining risk is named.** That is what this Design Pack shows, and it is what makes it ready to build.

---

## References

This unit draws only on the earlier units of this course and on the reference product's recorded facts. For the sources behind each check, see the reference lists of the units named in the tables above.

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
