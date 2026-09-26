# D1 — Parametric CAD Fundamentals
## Models That Update Themselves When the Board Changes

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Mechanical and 3D Design
**Time:** ~2 hours · **You will produce:** a parametric practice part and a shelled two-part enclosure

---

### The Board Will Change. Will the Case Follow?

You finish an enclosure model on Friday. On Monday, the board grows by 2 mm because a connector moved in B5. You open the case model and change the outer width. The lid no longer matches. The screw bosses are now off-centre. The display window is in the wrong place. The fillets fail because the edges they were attached to have gone. By Tuesday you are drawing the case again from scratch.

This is what happens when a model is built from typed-in numbers with no relationships between them. **Parametric CAD** works differently. Each dimension is defined in terms of a few named **parameters**, such as the board's width, the wall thickness and the clearance, and every feature is built on the ones before it. Change the board width in one place, and the case, lid, bosses and window all recalculate.

This unit teaches the tools of parametric modelling in Fusion 360: constrained sketches, the core features, the feature history, and above all named parameters. It then builds a two-part enclosure whose size follows the board. The same ideas work in Onshape, which the reference watch's enclosure was built in.

### What You Will Be Able to Do After This Reading

- **Draw** fully constrained sketches using geometric constraints and dimensions.
- **Build** solids with extrude, revolve, shell and fillet, in an order that survives change.
- **Define** named user parameters and formulas, so that one change updates the whole model.
- **Read and repair** the feature history (the timeline) when a change breaks a feature.
- **Produce** a shelled two-part enclosure sized from the board's dimensions.

### What Part 1 Already Covered

Part 1 did not include CAD. **Everything here is new**: sketching, constraints, 3D features and parametric thinking, taught from zero.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Getting Set Up

## Which Tool

This course teaches **Autodesk Fusion** (Fusion 360). Autodesk offers eligible students and educators free, one-year access to its software for educational use, renewable while you remain eligible [1]. **Onshape** is a browser-based alternative with the same core ideas, and it is what the reference watch's enclosure was built in.

<!-- REFPRODUCT:START -->
esp_watch's enclosure was modelled in Onshape and is almost complete: a case with a top lid carrying four openings (the display window, two buttons and the slide switch), with an interference-fit lid. The course teaches Fusion because it is widely used and has a free education licence. The concepts transfer directly: Onshape calls its parameters **variables**, and keeps them in a **Variable Studio** that several part studios can share [2].
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/enclosure-lid.png -->
![esp_watch enclosure (Onshape), lid with display window, button and switch openings](../reference-files/images/enclosure-lid.png)

## Design Intent

Before touching the software, decide the **design intent**: which dimensions *drive* the model and which *follow*. For an enclosure, the board drives everything:

```text
DRIVERS (you set these)           FOLLOWERS (the model calculates these)
────────────────────────          ──────────────────────────────────────
pcb_w, pcb_l   board size   ──►   inner cavity = board + clearance
stack_h        board height ──►   cavity depth
wall           wall thickness ─►  outer size = cavity + 2 × wall
clearance      air gap      ──►   lid position, lip, window positions
```

Write these down before modelling. A model built without a clear intent can still be parametric, but its parameters will control the wrong things.

---

# Part 2 — Sketches That Stay in Shape

## Constraints and Dimensions

Every 3D feature starts from a **sketch**: a 2D drawing on a plane or a face. A sketch has two kinds of rules that fix its shape:

- **Geometric constraints**: relationships between lines and points. Horizontal, vertical, parallel, perpendicular, tangent, equal, coincident, concentric, midpoint, symmetric.
- **Dimensions**: sizes and distances, such as "this line is 42 mm".

A sketch is **fully constrained** when every line and point has exactly one possible position. In Fusion, under-constrained geometry is shown in blue and fully constrained geometry turns black, so you can see at a glance what is still free to move.

Why does it matter? An under-constrained sketch can change shape unexpectedly when you edit something nearby, and every feature built on it changes too. A fully constrained sketch changes only when you change one of its dimensions.

A common habit is to draw shapes roughly and add dimensions until they look right. That produces sketches held in place by accident. Work the other way round: add the **geometric constraints first**, so the sketch has the right *shape*, and then the **dimensions**, so it has the right *size*.

> **Teaching model.** Think of a sketch as a frame of rods joined at pins. Constraints are the joints that fix angles and alignments; dimensions are the rods' lengths. A frame with a missing joint wobbles. The analogy stops working with over-constraint: in a real frame an extra rod just adds strength, but in a sketch an extra rule that conflicts with an existing one is an error Fusion will refuse to apply.

## Worked Example: A Fully Constrained Board Outline

We will sketch a rectangle representing the board, centred on the origin, so that the enclosure can grow evenly around it.

**Step 1: Create a sketch** on the XY plane (Design workspace, Create Sketch).

**Step 2: Draw a centre rectangle** from the origin. Fusion adds horizontal and vertical constraints to its sides automatically, and its centre is coincident with the origin.

**Step 3: Check what is free.** The rectangle's width and height can still change, so its lines are blue.

**Step 4: Dimension both sides.** Do not type numbers yet. In the next part you will create parameters and type their names instead.

**Check.** After Step 4, every line is black: shape fixed by constraints, size fixed by dimensions, position fixed by the origin. One sketch, three kinds of rules, nothing left to chance.

<!-- MEDIA
type: screenshot
id: D1-01
caption: A fully constrained centre rectangle in Fusion, dimensioned with parameter names
brief: Autodesk Fusion, Design workspace, sketch mode on the XY plane. A centre rectangle
  around the origin, all four lines black (fully constrained). Two dimensions shown on the
  sketch reading "pcb_w" and "pcb_l" with their evaluated values (38.00) in brackets.
  Constraint glyphs visible (horizontal, vertical, coincident at the origin). The Sketch
  Palette open on the right with "Show Constraints" ticked. Light theme.
-->

---

# Part 3 — Parameters

## Named User Parameters

A **user parameter** is a named value you define once and use everywhere. In Fusion, open the Change Parameters dialog (Design workspace, Modify menu) and add user parameters with a name, unit, value and comment [3]. Parameters can be **formulas** that use other parameters.

Here is the parameter set for a two-part enclosure around a board:

| Name | Unit | Expression | Comment |
|---|---|---|---|
| `pcb_w` | mm | 38 | board width |
| `pcb_l` | mm | 38 | board length |
| `stack_h` | mm | 14.044 | board height with parts fitted |
| `clearance` | mm | 0.5 | air gap between board and inner wall |
| `wall` | mm | 1.5 | side wall thickness |
| `floor_t` | mm | 1.5 | base thickness |
| `lid_t` | mm | 1.5 | lid thickness |
| `cavity_w` | mm | `pcb_w + 2 * clearance` | inner width |
| `cavity_l` | mm | `pcb_l + 2 * clearance` | inner length |
| `cavity_h` | mm | `stack_h + 2 * clearance` | inner height |
| `outer_w` | mm | `cavity_w + 2 * wall` | outer width |
| `outer_l` | mm | `cavity_l + 2 * wall` | outer length |
| `outer_h` | mm | `cavity_h + floor_t + lid_t` | total height |

<!-- REFPRODUCT:START -->
The first three values are esp_watch's recorded board: 38 × 38 mm, 14.044 mm tall with its parts fitted. The wall, floor, lid and clearance values are **example values** for teaching. D3 explains how to choose them for 3D printing.
<!-- REFPRODUCT:END -->

Only the first seven are ever typed in. The other six are formulas. That split is the design intent from Part 1, written in a form the software can enforce.

### Worked Example: What the Parameters Produce

**Step 1: Cavity.**

```text
cavity_w = 38 + 2 × 0.5    = 39.0 mm
cavity_l = 38 + 2 × 0.5    = 39.0 mm
cavity_h = 14.044 + 2 × 0.5 = 15.044 mm
```

**Step 2: Outer size.**

```text
outer_w = 39.0 + 2 × 1.5          = 42.0 mm
outer_l = 39.0 + 2 × 1.5          = 42.0 mm
outer_h = 15.044 + 1.5 + 1.5      = 18.044 mm
```

**Step 3: Change a driver.** B5 moves a connector, and the board grows to 40 mm wide. Change `pcb_w` from 38 to 40, and nothing else:

```text
cavity_w = 40 + 1   = 41.0 mm
outer_w  = 41 + 3   = 44.0 mm
```

**Check.** The outer height of about 18 mm matches the thickness budget from D0, which is a good sign that the model's structure matches the concept. And a 2 mm change to the board produced a 2 mm change to the case with one edit. If any feature fails to follow, it is using a typed number somewhere instead of a parameter.

<!-- MEDIA
type: screenshot
id: D1-02
caption: Fusion's Parameters dialog with the enclosure's user parameters, drivers and formulas
brief: Autodesk Fusion, Change Parameters dialog open, "User Parameters" section expanded,
  listing pcb_w, pcb_l, stack_h, clearance, wall, floor_t, lid_t (typed values) and
  cavity_w, cavity_l, cavity_h, outer_w, outer_l, outer_h (formulas, with evaluated values
  shown). Comments column filled in. The row for pcb_w selected, with its expression field
  being edited from 38 to 40. The model behind the dialog visible.
-->

> **Try it: Break it and fix it.** Build a simple box: a sketch rectangle dimensioned `outer_w` by `outer_l`, extruded by `outer_h`.
> 1. **Predict.** If you change `wall` from 1.5 to 2.0, what will the box's width become?
> 2. **Do.** Change it, and check the new width with the Inspect, Measure tool. Then edit the sketch, replace one dimension's parameter name with the plain number 42, and change `wall` again.
> 3. **Explain.** Which direction followed the change and which did not? How would you find a typed number hiding in a large model?

---

# Part 4 — Building Solids

## The Core Features

Most enclosures need only a handful of features:

| Feature | What it does | Enclosure use |
|---|---|---|
| **Extrude** | Pushes a sketch profile into a solid, or cuts it out | The main block; window and button openings |
| **Revolve** | Spins a profile around an axis | Round buttons, knobs, round bosses |
| **Shell** | Hollows a solid, leaving walls of a set thickness, with chosen faces removed | Turning a block into a box |
| **Fillet** | Rounds an edge | Comfort against the wrist; stronger corners |
| **Split body** | Cuts one solid into two along a plane or face | Separating the lid from the base |

## Order Matters: The Timeline

Fusion records every feature in the **timeline** at the bottom of the window, in the order you made them. When you change a parameter, Fusion replays the timeline from the start. Each feature is rebuilt using the ones before it.

That makes order a design decision. Two rules keep the timeline robust:

1. **Big shapes first, details last.** Block, then shell, then openings, then fillets. A fillet on an edge that a later cut removes will fail when the model rebuilds.
2. **Reference stable things.** Sketch on the origin planes or on faces that will always exist, and dimension from the origin rather than from an edge that a fillet might round away.

When a change breaks a feature, Fusion marks it in the timeline, usually because an edge or face it referred to no longer exists. Open the feature, see what is missing, and re-select the new edge or face. Fixing the *reference*, not the dimension, is almost always the answer.

> **Teaching model.** CAD tools identify edges and faces by how they were created. When a change adds or removes one, later features can lose track of "the edge they meant". Different tools handle this differently, and none handles it perfectly. Referencing origin planes and sketches, rather than generated edges, keeps you out of most of the trouble.

## Worked Example: A Shelled Two-Part Enclosure

With the parameters defined, the enclosure takes six features.

**Step 1: Outer block.** Sketch a centre rectangle on the XY plane, dimensioned `outer_w` by `outer_l`. Extrude it upwards by `outer_h`.

**Step 2: Shell.** Use Shell on the block with **no faces removed**, thickness `wall`. The block becomes a closed hollow box with walls all round. Closing it completely now, and splitting it in Step 4, keeps the lid and base walls consistent.

> **Assumption.** This uses the same thickness for side walls, floor and lid. If you want them different, extrude a block and cut a cavity sketch instead of using Shell. The parameter table already has separate values ready.

**Step 3: Corner fillets.** Fillet the four vertical outer edges, for example with a `corner_r` parameter. Doing this before splitting means both parts get matching corners.

**Step 4: Split into lid and base.** Create an offset plane at height `outer_h - lid_t`, and use Split Body to cut the box into two solids along it. Name them `base` and `lid` in the browser.

**Step 5: Openings.** On the lid's top face, sketch the display window and button holes, dimensioned from the origin, and cut them through the lid only.

**Step 6: Check.** Measure the base's inner cavity: it should equal `cavity_w` by `cavity_l`. Then change `pcb_w` to 40 and watch every step rebuild.

<!-- REFPRODUCT:START -->
esp_watch's enclosure also needs openings in places this simple model does not have: the XIAO's USB-C port on the left side, and a way for the heart-rate sensor on the underside to reach the wrist. Both belong to D2 and D4, where the real board model is placed inside the case.
<!-- REFPRODUCT:END -->

<!-- MEDIA
type: screenshot
id: D1-03
caption: The two-part enclosure in Fusion, with its timeline showing the six features in order
brief: Autodesk Fusion with the finished practice enclosure: base and lid shown slightly
  separated (exploded or with the lid moved up), filleted vertical corners, a rectangular
  display window and two round button holes in the lid. The browser on the left lists
  bodies "base" and "lid". The timeline at the bottom shows, in order: sketch, extrude,
  shell, fillet, construction plane, split body, sketch, extrude (cut). Light theme.
-->

<!-- MEDIA
type: gif
id: D1-04
caption: Changing one parameter, and watching the whole enclosure follow
brief: Screen recording, about 12 seconds. Start with the two-part enclosure visible.
  Open Change Parameters, click pcb_w, change 38 to 44, press Enter, close the dialog.
  The model rebuilds: base and lid both widen, the lid's window and button holes stay
  centred, fillets remain. Then reopen Change Parameters and set pcb_w back to 38.
  Keep the camera still throughout so the change is easy to see.
-->

> **Try it: Order matters.** In your enclosure's timeline, drag the corner fillet feature (Step 3) to after the split (Step 4).
> 1. **Predict.** Will the model still rebuild? Will the lid and base corners still match?
> 2. **Do.** Move it, and change `pcb_w`. Look for warnings in the timeline.
> 3. **Explain.** What does the fillet now refer to? Why did "big shapes first, details last" matter?
>
> **Extra challenge:** Add a `window_w` parameter for the display window, set as a formula from `pcb_w`. When the board grows, should the window grow too? Write down your design intent before deciding.

---

# Part 5 — Parametric Discipline

The tools matter less than the habits. Keep these five:

1. **Every dimension is a parameter or a formula.** A typed number is a future bug. The only exceptions are values that genuinely never change, and even they deserve a name.
2. **Drivers are few and named clearly.** `pcb_w`, not `d1`. Add a comment to every parameter saying what it is and where its value comes from.
3. **Sketches are fully constrained.** Nothing blue before you leave a sketch.
4. **Big shapes first, details last**, and reference origin planes wherever possible.
5. **Test the model by changing it.** Before calling a model finished, change each driver by a meaningful amount and check that everything follows. A parametric model that has never been changed is only presumed to be parametric.

<!-- REFPRODUCT:START -->
Rule 1 matters especially for a design like esp_watch, where the board's stack height of 14.044 mm drives the case's thickness. If a v2 changes the module stack, as D0's concept comparison suggests it might, a model driven by `stack_h` recalculates every height-dependent feature in one edit.
<!-- REFPRODUCT:END -->

---

# Putting It All Together

## Applying What You Have Learned

**1. Practice part.** Model a simple parametric part, such as a bracket or a phone stand, with at least three named driver parameters, one formula parameter and fully constrained sketches. Change each driver and confirm everything follows.

**2. Parameter table.** Write the parameter table for your own enclosure: drivers from your B5 board and D0 concept, followers as formulas, with a comment on each.

**3. Two-part enclosure.** Build it with the six-step method: block, shell, fillets, split, openings, check. Add at least the display and button openings from your D0 concept.

**4. Change test.** Change your board width by 2 mm and your wall thickness by 0.5 mm, one at a time. Record which features, if any, failed, and fix them.

**5. Diagnose.** A classmate's lid window stays in the same place when `pcb_w` changes, while the case grows around it. Name two possible causes.

<details>
<summary>Answer</summary>

Most likely, the window's sketch is dimensioned from an **edge of the lid** with a typed number, rather than from the origin or with a parameter. Or the window sketch is **not fully constrained**, so it stayed where it was drawn. Fix: dimension the window from the origin, centred with a symmetric or midpoint constraint, and use parameters for its size.

</details>

**Deliverable:** your practice part and two-part enclosure files (Fusion archives or links), the parameter table, and your change-test notes, saved in your design pack.

## Self-Check

Open your enclosure model and answer each item Y or N.

1. Every sketch in the model is fully constrained (no blue geometry). — Y/N
2. Every dimension uses a parameter or formula, not a typed number. — Y/N
3. Every user parameter has a comment. — Y/N
4. The board's width, length and height are drivers, and the outer size is calculated from them. — Y/N
5. The enclosure is split into two named bodies, a base and a lid. — Y/N
6. The measured inner cavity equals the calculated cavity size. — Y/N
7. Changing `pcb_w` by 2 mm rebuilds the whole model with no errors. — Y/N
8. Changing `wall` by 0.5 mm rebuilds the whole model with no errors. — Y/N
9. The timeline order is: big shapes, shell, fillets, split, openings. — Y/N
10. The openings stay correctly placed after a size change. — Y/N

---

## Check Your Understanding

**1.** A board is 38 mm wide. Clearance is 0.5 mm per side and walls are 1.5 mm. What is the enclosure's outer width?

- A. 39 mm
- B. 40 mm
- C. 42 mm
- D. 44 mm

<details>
<summary>Answer</summary>

**C.** 38 + 2 × 0.5 + 2 × 1.5 = 42 mm. **A** is the inner cavity only. **B** adds the clearance and one wall. **D** would be the result for a 40 mm board.

</details>

**2.** A sketch's lines are still blue after all dimensions are added. What does that mean, and what should you do?

- A. The sketch is fine; blue is the default colour.
- B. Something can still move; add the missing geometric constraint or dimension until everything turns black.
- C. The sketch has too many constraints; delete some.
- D. The model needs to be saved.

<details>
<summary>Answer</summary>

**B.** In Fusion, blue means under-constrained. **A** is wrong: fully constrained geometry turns black. **C** describes over-constraint, which Fusion reports as an error rather than showing blue. **D** is unrelated.

</details>

**3.** A fillet fails after a parameter change. What is the most likely cause, and fix?

- A. The fillet radius is too small; increase it.
- B. The edge it referred to no longer exists or has changed; re-select the edge, and consider moving the fillet later in the timeline.
- C. Fusion cannot fillet after a change; delete the fillet.
- D. The model needs more parameters.

<details>
<summary>Answer</summary>

**B.** Features refer to the edges and faces created by earlier ones; a change can remove or replace them. Fixing the reference, and putting details last, solves most such failures. **A** may occasionally matter, but it is not the usual cause. **C** is false. **D** does not address the broken reference.

</details>

**4.** Why should the fillets on the enclosure's vertical corners be applied before splitting it into a lid and a base?

- A. Fillets cannot be applied after a split.
- B. Filleting the single body first gives the lid and base exactly matching corners from one feature.
- C. It makes the file smaller.
- D. The split tool needs rounded corners.

<details>
<summary>Answer</summary>

**B.** One fillet on one body guarantees the two parts match. Filleting them separately risks different radii or references. **A**, **C** and **D** are not true.

</details>

**5.** Which parameter should be a formula rather than a typed value?

- A. `pcb_w`, the board width
- B. `wall`, the wall thickness
- C. `outer_w`, the enclosure's outer width
- D. `clearance`, the air gap

<details>
<summary>Answer</summary>

**C.** The outer width follows from the board, clearance and wall, so it should be calculated from them. **A**, **B** and **D** are drivers: values you choose or take from the board, which the rest of the model follows.

</details>

**6.** A student says their model is parametric because every dimension is named. They have never changed a parameter. What is the best advice?

- A. Nothing more is needed.
- B. Test it: change each driver by a meaningful amount and check that every feature follows without errors. Until then it is only presumed parametric.
- C. Add more parameters.
- D. Rename the parameters.

<details>
<summary>Answer</summary>

**B.** Names do not prove relationships; only a change does. **A** skips the verification. **C** and **D** add work without testing anything.

</details>

---

## What You Can Now Do, and What Comes Next

- Draw sketches whose shape and size are fixed by constraints and dimensions.
- Define driver and formula parameters that capture your design intent.
- Build a shelled two-part enclosure in an order that survives change.
- Test a model by changing it, and repair broken references.

The idea to carry forward: **the board drives the case.** Make that relationship explicit in parameters, and every future board change becomes an edit rather than a redraw.

In [D2 — PCB and Enclosure Co-Design](D2-pcb-enclosure-co-design.md) you will bring the real board model from KiCad into CAD, fit it inside this enclosure, and check for collisions.

---

## References

1. Autodesk. *Education software overview* (free, one-year access for eligible students and educators, renewable while eligible). https://www.autodesk.com/education/edu-software/overview
2. Onshape. *Variable Studios* (help documentation for defining and sharing variables across part studios). https://cad.onshape.com/help/Content/VariableStudio/variable_studio.htm
3. Autodesk. *How to Create and Edit Parameters in Fusion for Simplified Design Control* (user parameters: name, unit, value, comment). https://www.autodesk.com/products/fusion-360/blog/mastering-fusion-parameters-a-guide-for-simplified-design-control/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
