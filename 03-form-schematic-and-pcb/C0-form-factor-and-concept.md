# C0 — Form Factor and Concept
## Deciding the Product's Shape Before Anyone Opens CAD

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Form Factor, Schematic and PCB
**Time:** ~1 hour · **You will produce:** three annotated concept sketches, a chosen direction with its justification, and a board outline sketch for C2

---

### A Perfect Board Facing the Wrong Way

Imagine a circuit board that is beautifully routed, passes every design rule check and has every footprint verified, and whose heart-rate sensor points at the wearer's face instead of their wrist. Nothing in KiCad can catch that. The board is correct. The *product* is wrong, because nobody decided which way the board sits in the watch before the layout started.

For a wearable, the physical constraints come first. This unit settles them on paper, with quick sketches compared against your spec, before any CAD.

### What You Will Be Able to Do After This Reading

- **Identify** the physical constraints a wearable must meet, and trace each to a requirement in your A0 spec.
- **Calculate** a thickness budget from the parts that stack up inside the product.
- **Sketch** at least three distinct concepts and annotate them with those constraints.
- **Evaluate** the concepts against your spec with a comparison matrix, and **justify** a chosen direction.
- **Decide** the orientation of every part that must face a particular way, such as a sensor against the skin.

---

## The Constraints a Wrist Imposes

List the physical constraints before sketching anything. For a wrist-worn device they come straight from A0's environment and requirements:

| Constraint | Question it answers | Comes from |
|---|---|---|
| Thickness | How far above the wrist may it stand? | A0 size envelope |
| Outline | How wide and long can it be on a small wrist? | A0 size envelope |
| Weight | Will it stay comfortable all day? | A0 size envelope |
| Skin-facing side | Which face touches skin, and what must be on it? | A0 environment; sensing requirement |
| Viewing side | Which face does the wearer look at? | A0 display requirement |
| Strap attachment | Where do the strap forces go into the case? | A0 lifetime and impact |
| Button reach | Can a button be pressed with one hand, without pushing the watch into the wrist? | A0 use scenario |
| Charge access | Where does the charger plug in, and is the opening away from skin and sweat? | A0 charging requirement |
| Sweat and water | What must be sealed, and to what level? | A0 environment (IP target) |

A useful way to think about a wearable is as layers stacked from the wrist upwards. Each layer claims part of the thickness budget, and each face has a job:

```text
          wearer's eyes
               ▲
   ┌───────────────────────┐   lid: window, button openings
   │ display               │
   │ modules and board     │   the electronics stack
   │ battery (beside, or   │
   │ underneath)           │
   │ sensor                │
   └───────────────────────┘   base: sensor window against the skin
               ▼
             wrist
```

## Orientation Is Decided Here

Some parts only work facing one way. Decide their orientation now and write it down, because the board layout in C2 depends on it.

| Part | Must face | Why |
|---|---|---|
| Optical heart-rate sensor | The skin, pressed flat, with outside light blocked | It reads light scattered back from tissue (B0) |
| Display | The wearer's eyes | It must be seen |
| Buttons | Outwards or sideways, reachable by the other hand | They must be pressed without removing the watch |
| Charging port | A side, away from the skin | Sweat and skin contact |
| Antenna | Away from the wrist, the battery and copper | Body tissue, a metal-foil battery and copper all detune it (C2) |

<!-- REFPRODUCT:START -->
esp_watch decides these as follows. The display, motion sensor, XIAO board, both buttons and the slide switch are on the **top** face. The MAX30102 heart-rate module is on the **underside**, so its sensor touches the wrist. The XIAO's USB-C port faces the **left side**. The external antenna is to be routed along the inside of the case, away from the battery. The enclosure's lid has four openings: one for the display, two for the buttons and one for the slide switch.

Putting the sensor on the underside makes the board two-sided, and the case base must present the sensor to the skin through a window. The board outline is 37.8 × 39 mm, with four mounting holes: two at the top left and right, two in the middle.
<!-- REFPRODUCT:END -->

![esp_watch board, underside: the heart-rate sensor module that must face the wrist](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_back.png)

---

## Worked Example: The Thickness Budget

Before sketching shapes, add up what must stack. This is the calculation that most often rules concepts out.

<!-- REFPRODUCT:START -->
**Step 1: The electronics stack.** esp_watch's board with its parts fitted is **14.044 mm** tall. The display sits on a female header above the motion-sensor module (a 4–5 mm air gap between them), and that stack sets the height.

**Step 2: Add the case.** **Example values:** a 3D-printed lid 1.5 mm thick and a base 1.5 mm thick, and 0.5 mm of clearance above and below the electronics so nothing is squeezed.

```text
Electronics stack         14.044 mm
Clearance, top + bottom    1.0   mm   (0.5 + 0.5)
Lid                        1.5   mm
Base                       1.5   mm
──────────────────────────────────
Total                     18.0   mm  (rounded)
```
<!-- REFPRODUCT:END -->

**Step 3: Compare with the requirement.** A0's example size envelope allowed 16 mm including the case. The concept is about 2 mm over.

**Step 4: Check the battery fits the space it was given.**

<!-- REFPRODUCT:START -->
The battery stands vertically in a slot behind the display's header, a face about 38 × 14 mm. The cell is 30 × 12 × 4 mm. Standing on its 30 × 4 face, it is 12 mm tall, which fits under the 14.044 mm stack, and 30 mm long, which fits along the 38 mm board. Its 4 mm thickness is the width it takes from the slot.
<!-- REFPRODUCT:END -->

**Check.** The battery fits within the existing height, so it does not add thickness. That is exactly why it was stood on end. The electronics stack does not fit a 16 mm envelope once walls are added. Either the requirement grows to about 18 mm, with a written reason, or the concept changes. The quickest way to find out which is to sketch alternatives.

---

## Sketching Concepts

A **concept sketch** is a quick drawing, on paper or in any drawing tool, that shows the arrangement of the main parts and the product's outline. It is not CAD. Its job is to let you compare ideas in minutes rather than days.

Draw **at least three concepts that are genuinely different**, not three versions of the same idea. Change the arrangement, not just the corner radius. For each, draw two views, from the top and from the side, and annotate them:

- overall outline and thickness (from a thickness budget like the one above)
- which face touches skin, which the wearer sees
- where the buttons, charge port and strap attachments are
- where the battery goes

Here are three different arrangements of the same parts:

```text
A: Stacked (esp_watch as built)      B: Side by side                 C: Sensor pod on the strap
   side view                            side view                       side view
   ┌──────────────┐                     ┌────────────────────────┐      ┌───────────┐
   │ display      │                     │ display │ board │ batt │      │ display,  │
   │ motion  batt │  ~18 mm             ├─────────┴───────┴──────┤~11mm│ board,    │ ~13 mm
   │ board        │                     │ sensor                 │      │ battery   │
   │ sensor       │                     └────────────────────────┘      └─────┬─────┘
   └──────────────┘                     wider: ~55 mm                   flex cable │ in the strap
   37.8 × 39 mm board                                                      ┌──────▼──────┐
                                                                          │ sensor pod  │ under the wrist
                                                                          └─────────────┘
```

> **Teaching model.** The thicknesses above are rough, for comparing concepts only. They assume the same modules rearranged; real numbers come from CAD in E2.

<!-- MEDIA
type: photo
id: C0-01
caption: An annotated concept sketch: top and side views, with each constraint labelled
brief: A photo or scan of a hand-drawn concept sketch on plain paper, for a wrist device.
  Top view on the left, side view on the right, drawn roughly to scale with a ruler.
  Handwritten annotations with arrows: "skin side: sensor window", "display faces up",
  "USB-C on left, away from skin", "buttons on right edge, reachable with other hand",
  "strap lugs take the load here", "battery stood on end behind display", and a thickness
  dimension "≈ 18 mm total". Pencil or pen, clear and legible, no colour required.
-->

## Choosing a Direction: The Comparison Matrix

Compare the concepts against your spec with a simple matrix. Pick one concept as the **datum**, the reference, and score every other concept against it on each criterion: better (+), same (0) or worse (−). This is often called a **Pugh matrix**. It is quick, and it forces every comparison to name a criterion from the spec.

### Worked Example: Choosing Between A, B and C

<!-- REFPRODUCT:START -->
Concept A, esp_watch as built, is the datum.

| Criterion (A0 spec, plus build effort) | A: Stacked (datum) | B: Side by side | C: Sensor pod on strap |
|---|---|---|---|
| Thickness ≤ 16 mm | 0 | + (about 11 mm) | + (about 13 mm) |
| Outline fits a small wrist | 0 | − (about 55 mm wide) | 0 |
| Sensor pressed to skin, light blocked | 0 | 0 | + (pod sits under the wrist) |
| Buttons reachable with one hand | 0 | 0 | 0 |
| Charge port away from skin | 0 | 0 | 0 |
| Printable with FDM (E3) | 0 | 0 | − (flexible strap section, two parts) |
| Uses the existing board unchanged | 0 | − (new layout) | − (new layout, flex cable) |
| **Total** | 0 | −1 | 0 |
<!-- REFPRODUCT:END -->

**Reading the result.** No concept beats the datum outright. B fixes thickness but becomes too wide and needs a new board. C fixes thickness *and* improves sensor contact, but adds a flexible cable through the strap, a harder-to-print part, and a new board. A remains the most buildable, and its one clear failure, thickness, now has a number.

**The decision, and its justification**, might then read:

> *Direction: Concept A. Accept a total thickness of about 18 mm for version 1 and update NFR-07 accordingly, because A uses the existing board and is printable as two parts. Record Concept C as the version 2 direction, since it solves both thickness and sensor contact.*

**Check.** The decision names the criterion that was traded (thickness), changes the spec in writing rather than ignoring it, and records the better long-term option. That is what a justification looks like: not "A looked best", but which requirement moved and why.

> **Try it: Change the weights.** Suppose your A0 spec says thickness is the single most important requirement, because users in your Part 2 interviews refused to wear anything thick.
> 1. **Predict.** Does the choice change?
> 2. **Do.** Count the thickness row as three times the others, and recalculate the totals.
> 3. **Explain.** Which concept wins now? What would you have to accept to build it?

---

# Putting It All Together

## Applying What You Have Learned

**1. List your constraints.** Build the constraint table for your product, tracing each row to a requirement ID in your A0 spec.

**2. Fix orientations.** For every part that must face a particular way, write the face and the reason.

**3. Calculate a thickness budget.** Use your module heights from B4 and your best estimate of the stack (C2 and E2 will confirm it), plus example wall and clearance values.

**4. Sketch three concepts** that differ in arrangement. Two views each, all constraints annotated, thickness from the budget.

**5. Choose a direction** with a comparison matrix against your spec, and write a justification that names any requirement you changed.

**6. Hand the board its shape.** From the chosen concept, sketch the board outline with its rough dimensions, the mounting-hole positions, and which side (top or bottom) every part goes on. C2 lays out the board to this sketch.

**Deliverable:** three annotated concept sketches (photos or drawings), the comparison matrix, the written direction and the board outline sketch, saved in your design pack as `C0-concept.md`.

## Self-Check

Open `C0-concept.md` and answer each item Y or N.

1. Every constraint in the table traces to a requirement ID in your A0 spec. — Y/N
2. Every part that must face a particular way has its face and reason written. — Y/N
3. A thickness budget is calculated, with every layer listed. — Y/N
4. There are three concepts that differ in arrangement, not just styling. — Y/N
5. Every sketch has a top view and a side view. — Y/N
6. Every sketch shows skin side, viewing side, buttons, charge port, strap attachment and battery. — Y/N
7. The comparison matrix uses criteria from your spec, with one concept as the datum. — Y/N
8. The chosen direction names every requirement it trades, and any spec change is written into A0. — Y/N
9. The board outline sketch gives dimensions, mounting holes and a side for every part. — Y/N

---

## Check Your Understanding

**1.** A student's concept puts the USB-C charging port on the base, next to the sensor window, "so the cable is hidden". Which constraint does this break, and when should it be fixed?

- A. Charge access: the port must open on a side, away from skin and sweat. Fix it now, in the concept, before layout.
- B. None. KiCad DRC will flag a port on the wrong face.
- C. Thickness. Fix it in CAD in E2.
- D. Strap attachment. Fix it in the slicer.

<details>
<summary>Answer</summary>

**A.** The orientation table puts the charge port on a side, away from sweat and skin. **B:** DRC checks copper rules, not which face touches the wrist. **C** and **D** name constraints the port does not affect, at stages too late to move a part.

</details>

**2.** A concept's electronics stack is 14 mm, and the case adds 1.5 mm walls top and bottom plus 0.5 mm clearance on each side. The spec says ≤ 16 mm. What is the right response?

- A. Make the walls 0.5 mm thick.
- B. The total is about 18 mm, so either change the concept to reduce the stack, or change the requirement in writing with a reason.
- C. Ignore it until the CAD model is finished.
- D. Remove the clearances.

<details>
<summary>Answer</summary>

**B.** 14 + 1 + 3 = 18 mm, which fails the requirement. The honest choices are to change the design or change the spec, visibly. **A** and **D** produce parts that are too thin to print reliably or that squeeze the electronics. **C** delays the discovery to a more expensive stage.

</details>

**3.** A student submits three concepts. All are stacked like Concept A: one has rounded corners, one has square corners, one is 2 mm narrower. What is the main problem?

- A. Nothing. Three concepts were drawn.
- B. They differ only in styling, so they share the same thickness and board trade-offs, and nothing real has been compared.
- C. They should have been drawn in CAD.
- D. The narrower one breaks the strap constraint.

<details>
<summary>Answer</summary>

**B.** Same arrangement means the same thickness problem. A real alternative moves parts, as concepts B and C in this unit do. **A** counts sketches, not ideas. **C:** concept sketches are meant to be quick and on paper. **D:** nothing shows the strap is affected.

</details>

**4.** In a Pugh matrix, a concept scores + on thickness but − on "uses the existing board". What does this tell you?

- A. The concept is neutral overall, so it does not matter.
- B. It trades an improvement in a requirement for extra design work; whether that is worth it depends on how much each criterion matters to your product.
- C. The matrix is broken.
- D. Choose it, because pluses outweigh minuses.

<details>
<summary>Answer</summary>

**B.** The matrix makes the trade-off visible; weighting the criteria, or discussing them, decides it. **A** misreads a balanced score as "no difference". **C** is wrong: trade-offs are what the matrix is for. **D** treats all criteria as equally important without checking.

</details>

**5.** Your electronics stack is 12 mm tall over a 35 mm board. Your battery is 25 × 10 × 4 mm. Which placement adds no thickness?

- A. Flat, under the board.
- B. On its long edge beside the modules: 25 mm long, 4 mm wide, 10 mm tall.
- C. On its end: 10 × 4 mm face down, 25 mm tall.
- D. Flat, on top of the display.

<details>
<summary>Answer</summary>

**B.** At 10 mm tall it fits under the 12 mm stack, and at 25 mm long it fits along the 35 mm board. Like esp_watch's cell, it uses height the stack already claims. **A** and **D** add a 4 mm layer. **C** stands 13 mm above the stack.

</details>

---

## What Comes Next

**Next:** [C1 — Schematic Capture](C1-schematic-capture-and-symbols.md) draws the circuit in KiCad. Your concept returns in C2 (board outline) and Module 5 (CAD).

---

## References

1. International Electrotechnical Commission. *Ingress Protection (IP) ratings* (the two-digit code for solids and liquids, for your sweat and water constraint). https://www.iec.ch/ip-ratings

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
