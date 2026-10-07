# E0 — Parametric CAD Fundamentals
## A Fusion Walkthrough: A Case That Follows the Board

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Mechanical and 3D Design
**Time:** ~2 hours · **You will produce:** a parametric practice part and a shelled two-part enclosure

---

### The Board Will Change. Will the Case Follow?

You finish an enclosure model on Friday. On Monday, the board grows by 2 mm because a connector moved in your layout. You open the case model and change the outer width. The lid no longer matches. The screw bosses are now off-centre. The display window is in the wrong place. The fillets fail because the edges they were attached to have gone. By Tuesday you are drawing the case again from scratch.

This is what happens when a model is built from typed-in numbers with no relationships between them. **Parametric CAD** works differently. Each dimension is defined in terms of a few named **parameters**, such as the board's width, the wall thickness and the clearance, and every feature is built on the ones before it. Change the board width in one place, and the case, lid and openings all recalculate.

This unit walks through a simple two-part case for esp_watch's board in **Autodesk Fusion**, step by step. As in the KiCad walkthroughs, it shows only the tools you need to build one enclosure; Fusion's help covers the rest [4]. This course uses only **solid modelling**: the **Solid** tab of Fusion's Design workspace. The Surface, Mesh, Sheet Metal and Form tools are not needed for a printed case.

### What You Will Be Able to Do After This Reading

- **Find** your way round the Fusion window: browser, toolbar, canvas, ViewCube and timeline.
- **Define** named user parameters and formulas, so that one change updates the whole model.
- **Draw** fully constrained sketches using geometric constraints and dimensions.
- **Build** solids with extrude, fillet, shell and split body, in an order that survives change.
- **Read and repair** the timeline when a change breaks a feature, and **export** the model for E2.

---

## Before You Start

| You need | From |
|---|---|
| Autodesk Fusion, installed, with an education licence | Autodesk's education site [1] |
| Your board's width, length and height with parts fitted | C3 (the board file) and your C0 concept |
| The openings your case needs: display, buttons, ports | Your C0 concept |
| esp_watch's board size, to follow along | 37.8 × 39 mm, 14.044 mm tall with parts fitted |

Autodesk offers eligible students and educators free, one-year access to Fusion for educational use, renewable while you remain eligible [1]. **Onshape** is a browser-based alternative with the same core ideas.

<!-- REFPRODUCT:START -->
esp_watch's enclosure was modelled in **Onshape**, not Fusion: a case with a top lid carrying four openings (the display window, two buttons and the slide switch). Onshape calls its parameters **variables**, and keeps them in a **Variable Studio** that several part studios can share [2]. The walkthrough below builds a simpler case for the same board in Fusion. It does not need to match the Onshape one; the steps matter more than the shape.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/enclosure-lid.png -->
![esp_watch enclosure (Onshape), lid with display window, button and switch openings](../reference-files/images/enclosure-lid.png)

### Decide the Design Intent First

Before touching the software, decide the **design intent**: which dimensions *drive* the model and which *follow*. For an enclosure, the board drives everything:

```text
DRIVERS (you set these)           FOLLOWERS (the model calculates these)
────────────────────────          ──────────────────────────────────────
pcb_w, pcb_l   board size   ──►   inner cavity = board + clearance
stack_h        board height ──►   cavity depth
wall           wall thickness ─►  outer size = cavity + 2 × wall
clearance      air gap      ──►   lid position, window positions
```

Write these down before modelling. A model built without a clear intent can still be parametric, but its parameters will control the wrong things.

---

## Step 1: Start a Design

Open Fusion and start a new design (**File → New Design**). Fusion saves designs to its cloud, inside a **project**; make one project for your product and keep every design in it.

Two settings to check once:

- **Units.** In the browser, expand **Document Settings → Units** and make sure it reads **mm**.
- **Timeline.** If there is no timeline along the bottom of the window, right-click the top item in the browser and choose **Capture Design History**. Without it, Fusion does not record the features, and nothing in this unit works.

<!-- MEDIA
type: screenshot
id: E0-W01
caption: The Fusion window, with its main areas labelled
brief: Autodesk Fusion, a new empty design in the Design workspace, Solid tab active.
  Full window, light theme. Claude adds labels for: the application bar (top), the toolbar
  with its CREATE, MODIFY, CONSTRUCT and INSPECT panels, the browser (left), the canvas
  (centre), the ViewCube (top right), the navigation bar (bottom centre) and the timeline
  (bottom left).
-->

| Area | Where | What it is for |
|---|---|---|
| **Toolbar** | Top | Tabs along the top (stay on **Solid**), and the tools grouped into panels: **Create**, **Modify**, **Construct**, **Inspect** |
| **Browser** | Left | Everything in the design: document settings, origin planes, bodies, sketches. Rename bodies here. |
| **Canvas** | Centre | The model |
| **ViewCube** | Top right | Click a face or corner to look from that direction |
| **Timeline** | Bottom | Every feature, in the order it was made. Fusion replays it on every change. |

To move round the model: scroll to zoom, hold the middle button to pan, and hold **Shift** with the middle button to orbit. Press **S** anywhere to open a search box and type a tool's name; it is the quickest way to find a tool you cannot see.

---

## Step 2: Create the Parameters

Parameters come first, so that every dimension you add later can use a name instead of a number.

Open **Modify → Change Parameters**. Click the **+** beside **User Parameters**, and for each row enter a **name**, **unit**, **expression** and **comment** [3]. An expression can be a number, or a formula that uses other parameters. Names are case-sensitive and cannot contain spaces.

Here is the parameter set for a two-part case around a board:

| Name | Unit | Expression | Comment |
|---|---|---|---|
| `pcb_w` | mm | 37.8 | board width |
| `pcb_l` | mm | 39 | board length |
| `stack_h` | mm | 14.044 | height of the parts stack (E2 measures the full stack) |
| `clearance` | mm | 0.5 | air gap between board and inner wall |
| `wall` | mm | 1.5 | side wall thickness |
| `floor_t` | mm | 1.5 | base thickness |
| `lid_t` | mm | 1.5 | lid thickness |
| `corner_r` | mm | 3 | outer corner radius |
| `cavity_w` | mm | `pcb_w + 2 * clearance` | inner width |
| `cavity_l` | mm | `pcb_l + 2 * clearance` | inner length |
| `cavity_h` | mm | `stack_h + 2 * clearance` | inner height |
| `outer_w` | mm | `cavity_w + 2 * wall` | outer width |
| `outer_l` | mm | `cavity_l + 2 * wall` | outer length |
| `outer_h` | mm | `cavity_h + floor_t + lid_t` | total height |

<!-- REFPRODUCT:START -->
The first three values are esp_watch's recorded board: 37.8 × 39 mm, and 14.044 mm from the board to the top of the OLED. E2 measures the full stack, including the board and the MAX30102 underneath, and updates `stack_h`. The wall, floor, lid, corner and clearance values are **example values** for teaching. E3 explains how to choose them for 3D printing.
<!-- REFPRODUCT:END -->

Only the first eight are ever typed in. The other six are formulas. That split is the design intent, written in a form the software can enforce.

<!-- MEDIA
type: screenshot
id: E0-W02
caption: Change Parameters, with the case's drivers and formulas
brief: Autodesk Fusion, Change Parameters dialog open, User Parameters expanded, listing
  pcb_w, pcb_l, stack_h, clearance, wall, floor_t, lid_t, corner_r (typed values) and
  cavity_w, cavity_l, cavity_h, outer_w, outer_l, outer_h (formulas, with evaluated values
  shown). Comment column filled in. Light theme.
-->

### Worked Example: What the Parameters Produce

**Step 1: Cavity.**

```text
cavity_w = 37.8 + 2 × 0.5   = 38.8 mm
cavity_l = 39 + 2 × 0.5     = 40.0 mm
cavity_h = 14.044 + 2 × 0.5 = 15.044 mm
```

**Step 2: Outer size.**

```text
outer_w = 38.8 + 2 × 1.5     = 41.8 mm
outer_l = 40.0 + 2 × 1.5     = 43.0 mm
outer_h = 15.044 + 1.5 + 1.5 = 18.044 mm
```

**Step 3: Change a driver.** The board grows to 40 mm wide. Change `pcb_w` from 37.8 to 40, and nothing else:

```text
cavity_w = 40 + 1   = 41.0 mm
outer_w  = 41 + 3   = 44.0 mm
```

**Check.** The outer height of about 18 mm matches the thickness budget from C0, which is a good sign that the model's structure matches the concept. And a 2.2 mm change to the board produced a 2.2 mm change to the case with one edit. If any feature fails to follow, it is using a typed number somewhere instead of a parameter.

---

## Step 3: Start a Sketch on a Plane

Every 3D feature starts from a **sketch**: a 2D drawing on a plane or a face.

Choose **Create → Create Sketch**, then click the origin plane that lies flat. That is **XY** if Fusion's default modelling orientation (**Preferences → General**) is **Z up**, and **XZ** if it is **Y up**. The view turns to look straight down at the plane, and the toolbar changes to the sketch tools.

<!-- MEDIA
type: screenshot
id: E0-W03
caption: Create Sketch, picking the flat origin plane
brief: Autodesk Fusion, Create Sketch active, the three origin planes shown in the canvas,
  the cursor over the flat (horizontal) plane, which is highlighted. Light theme.
-->

---

## Step 4: Draw and Constrain the Outline

A sketch has two kinds of rules that fix its shape:

- **Geometric constraints**: relationships between lines and points. Horizontal, vertical, parallel, perpendicular, tangent, equal, coincident, concentric, midpoint, symmetric.
- **Dimensions**: sizes and distances, such as "this line is 42 mm".

A sketch is **fully constrained** when every line and point has exactly one possible position. In Fusion, geometry that can still move is shown in **blue**, and fully constrained geometry turns **black**, so you can see at a glance what is still free.

Why does it matter? An under-constrained sketch can change shape unexpectedly when you edit something nearby, and every feature built on it changes too. A fully constrained sketch changes only when you change one of its dimensions.

A common habit is to draw shapes roughly and add dimensions until they look right. That produces sketches held in place by accident. Work the other way round: **constraints first**, so the sketch has the right *shape*, then **dimensions**, so it has the right *size*. Adding a rule that conflicts with an existing one **over-constrains** the sketch, and Fusion refuses to apply it.

**Do it:**

1. **Create → Rectangle → Center Rectangle.** Click the origin, then click anywhere to place a corner. Fusion adds horizontal and vertical constraints to the sides, and the centre sits on the origin, so the case will grow evenly in every direction.
2. **Sketch Dimension (D).** Click the top side, place the dimension, and type `outer_w` instead of a number. Do the same for a vertical side with `outer_l`.
3. **Check the colour.** Every line should now be black. If one is still blue, something can move: find it by dragging it, and add the missing constraint or dimension.
4. Click **Finish Sketch**.

A dimension driven by a parameter shows **fx:** before its value. That is how you spot a typed number later: it has no **fx:**.

<!-- MEDIA
type: screenshot
id: E0-W04
caption: A fully constrained centre rectangle, dimensioned with parameter names
brief: Autodesk Fusion, sketch mode on the flat plane. A centre rectangle around the
  origin, all four lines black (fully constrained). Two dimensions on the sketch showing
  "fx: 41.80" and "fx: 43.00". Constraint glyphs visible (horizontal, vertical, coincident
  at the origin). The Sketch Palette open on the right with Show Constraints ticked.
  Light theme.
-->

> **Try it: Break it and fix it.** Finish Steps 4 and 5 first, so you have a block.
> 1. **Predict.** If you change `wall` from 1.5 to 2.0, what will the block's width become?
> 2. **Do.** Change it, and check the width with **Inspect → Measure (I)**. Then edit the sketch, replace the `outer_w` dimension with the plain number 42, and change `wall` again.
> 3. **Explain.** Which direction followed the change and which did not? How would you find a typed number hiding in a large model? (Hint: the **Model Parameters** section of Change Parameters lists every dimension in the design.)

---

## Step 5: Extrude the Block (E)

**Create → Extrude** (**E**). Click inside the rectangle to select the profile. Set **Distance** to `outer_h`, **Direction** to one side, and **Operation** to **New Body**. Click **OK**.

The result is a solid block the size of the finished case. A body appears in the browser under **Bodies**.

<!-- MEDIA
type: screenshot
id: E0-W05
caption: Extruding the outline into a block, with the distance set to a parameter
brief: Autodesk Fusion, Extrude dialog open, the rectangle profile selected, Distance field
  reading "outer_h", Operation "New Body", the preview block visible in the canvas.
  Light theme.
-->

---

## Step 6: Round the Corners (F)

**Modify → Fillet** (**F**). Select the **four vertical edges** of the block and set the radius to `corner_r`.

Fillet **before** shelling. The shell in Step 7 then follows the rounded outside, so the inner corners are rounded too and the wall stays the same thickness all the way round. Fillet before splitting, too: one fillet on one body gives the base and the lid exactly matching corners.

<!-- MEDIA
type: screenshot
id: E0-W06
caption: Filleting the four vertical edges with one parameter
brief: Autodesk Fusion, Fillet dialog open, the four vertical edges of the block
  selected, radius field reading "corner_r", the rounded preview visible. Light theme.
-->

---

## Step 7: Hollow It Out (Shell)

**Modify → Shell.** Instead of picking a face, select the **body** (click it in the browser), so that no face is removed. Set **Inside Thickness** to `wall` and **Direction** to **Inside**.

The block becomes a closed hollow box with walls all round. Closing it completely now, and splitting it in Step 8, keeps the base and lid walls consistent.

> **Assumption.** Shell uses one thickness everywhere, so `floor_t` and `lid_t` should equal `wall` here. If you want them different, extrude a block and cut a cavity sketch instead of using Shell. The parameter table already has separate values ready.

<!-- MEDIA
type: screenshot
id: E0-W07
caption: Shelling the block into a closed hollow box
brief: Autodesk Fusion, Shell dialog open, the body selected in the browser (no faces
  removed), Inside Thickness "wall", Direction "Inside". The canvas in a section or
  see-through view so the hollow inside is visible. Light theme.
-->

---

## Step 8: Split Into Base and Lid

1. **Construct → Offset Plane.** Select the bottom face of the box and set the distance to `outer_h - lid_t`. A plane appears just below the top.
2. **Modify → Split Body.** **Body to Split**: the box. **Splitting Tool**: the new plane. Click **OK**.
3. In the browser, double-click each new body and rename it: `base` and `lid`.

The lid is now a flat plate sitting on the base's walls. A real case also needs a lip to locate the lid and a way to hold it shut; E3 adds those.

<!-- MEDIA
type: screenshot
id: E0-W08
caption: Split Body along an offset plane, and the two named bodies in the browser
brief: Autodesk Fusion, Split Body dialog open with the box as Body to Split and the
  offset plane as Splitting Tool. The browser on the left shows two bodies named "base"
  and "lid". Light theme.
-->

---

## Step 9: Cut the Openings

1. **Create Sketch** on the lid's top face.
2. Draw the display window (a centre rectangle) and the button holes (**Create → Circle**). Dimension every position **from the origin**, not from the lid's edge: the origin never moves, but edges can.
3. **Finish Sketch**, then **Extrude** each profile downwards with **Operation: Cut**. Under **Objects To Cut**, leave only `lid` ticked, so the cut cannot reach the base.

<!-- REFPRODUCT:START -->
esp_watch's lid has four openings: the display window, two buttons and the slide switch. Its case also needs openings this simple model does not have: the XIAO's USB-C port on the side, and a way for the heart-rate sensor on the underside to reach the wrist. Both belong to E2 and E4, where the real board model is placed inside the case.
<!-- REFPRODUCT:END -->

---

## Step 10: Read the Timeline

Fusion records every feature in the **timeline** at the bottom of the window, in the order you made them. When you change a parameter, Fusion replays the timeline from the start, rebuilding each feature from the ones before it.

That makes order a design decision. Two rules keep the timeline robust:

1. **Big shapes first, details last.** Block, corner fillets, shell, split, then openings. A feature that refers to an edge a later feature removes will fail when the model rebuilds.
2. **Reference stable things.** Sketch on the origin planes or on faces that will always exist, and dimension from the origin rather than from an edge that a fillet might round away.

When a change breaks a feature, Fusion colours it in the timeline, usually because an edge or face it referred to no longer exists. Double-click the feature, see which selection is missing, and re-select the new edge or face. Fixing the **reference**, not the dimension, is almost always the answer.

**Check.** Use **Inspect → Measure (I)** on the base's inside: it should equal `cavity_w` by `cavity_l`.

<!-- MEDIA
type: screenshot
id: E0-W09
caption: The finished two-part case, with its timeline in order
brief: Autodesk Fusion with the finished practice case: base and lid shown slightly
  separated (lid moved up), rounded vertical corners, a rectangular display window and two
  round button holes in the lid. The browser lists bodies "base" and "lid". The timeline
  at the bottom shows, in order: sketch, extrude, fillet, shell, construction plane, split
  body, sketch, extrude (cut). Light theme.
-->

---

## Step 11: Test It by Changing It

A parametric model that has never been changed is only presumed to be parametric. Open **Change Parameters**, set `pcb_w` to 44, and close the dialog. Every step should rebuild: base and lid both widen, the openings stay centred, and the fillets remain. Set it back, then do the same with `wall`.

<!-- MEDIA
type: gif
id: E0-W10
caption: Changing one parameter, and watching the whole case follow
brief: Screen recording, about 12 seconds. Start with the two-part case visible. Open
  Change Parameters, click pcb_w, change 37.8 to 44, press Enter, close the dialog. The
  model rebuilds: base and lid both widen, the lid's window and button holes stay centred,
  fillets remain. Then reopen Change Parameters and set pcb_w back to 37.8. Keep the
  camera still throughout so the change is easy to see.
-->

> **Try it: Order matters.** In your timeline, drag the fillet feature (Step 6) to after the split (Step 8).
> 1. **Predict.** Will the model still rebuild? Will the lid and base corners still match? Will the inner corners still be rounded?
> 2. **Do.** Move it, and change `pcb_w`. Look for warnings in the timeline.
> 3. **Explain.** What does the fillet now refer to? Why did "big shapes first, details last" matter?
>
> **Extra challenge:** Add a `window_w` parameter for the display window, set as a formula from `pcb_w`. When the board grows, should the window grow too? Write down your design intent before deciding.

---

## Step 12: Save and Export

Fusion keeps the design in its cloud project. For your design pack you also need copies on your own disk:

- **File → Export**, type **Fusion Archive (.f3d)**: the full model with its timeline and parameters, which anyone with Fusion can open and edit.
- **File → Export**, type **STEP**: the solid shapes only, readable by any CAD tool, including Onshape.

Commit both to your design pack's Git repository each time the case changes, with a message saying what changed, for example "case: wall 1.5 → 2.0 mm". [Version Control for a Hardware Project](../01-system-architecture/REF-version-control.md) shows how.

---

## Tool Reference

| Tool | Where | Key | Use it to |
|---|---|---|---|
| Search for a tool | Anywhere | S | Find any tool by typing its name |
| Change Parameters | Modify | — | Add user parameters and formulas; list every model dimension |
| Create Sketch | Create | — | Start a 2D sketch on a plane or face |
| Center Rectangle | Sketch: Create → Rectangle | — | Draw a rectangle centred on a point |
| Sketch Dimension | Sketch: Create | D | Size and position sketch geometry |
| Extrude | Create | E | Make a solid from a profile, or cut one away |
| Fillet | Modify | F | Round edges |
| Shell | Modify | — | Hollow a body to a set wall thickness |
| Offset Plane | Construct | — | Make a plane at a set distance from a face or plane |
| Split Body | Modify | — | Cut one body into two |
| Measure | Inspect | I | Check a size or gap |

---

## Parametric Discipline

The tools matter less than the habits. Keep these three:

1. **Every dimension is a parameter or a formula.** A typed number is a future bug.
2. **Drivers are few and named clearly.** `pcb_w`, not `d1`. Add a comment to every parameter saying what it is and where its value comes from.
3. **Test the model by changing it.** Before calling a model finished, change each driver by a meaningful amount and check that everything follows.

---

# Putting It All Together

## Applying What You Have Learned

**1. Practice part.** Model a simple parametric part, such as a bracket or a phone stand, with at least three named driver parameters, one formula parameter and fully constrained sketches. Change each driver and confirm everything follows.

**2. Parameter table.** Write the parameter table for your own enclosure: drivers from your C3 board and C0 concept, followers as formulas, with a comment on each.

**3. Two-part enclosure.** Build it with Steps 1–10: parameters, sketch, block, fillets, shell, split, openings. Add at least the display and button openings from your C0 concept.

**4. Change test.** Change your board width by 2 mm and your wall thickness by 0.5 mm, one at a time. Record which features, if any, failed, and how you fixed them.

**Deliverable:** your practice part and two-part enclosure (`.f3d` and `.step` exports), the parameter table, and your change-test notes, saved in your design pack as `E0-cad/`.

## Self-Check

Open your enclosure model and answer each item Y or N.

1. Every sketch in the model is fully constrained (no blue geometry). — Y/N
2. Every dimension shows **fx:**, using a parameter or formula, not a typed number. — Y/N
3. Every user parameter has a comment. — Y/N
4. The board's width, length and height are drivers, and the outer size is calculated from them. — Y/N
5. The enclosure is split into two named bodies, `base` and `lid`. — Y/N
6. The measured inner cavity equals the calculated cavity size. — Y/N
7. Changing `pcb_w` by 2 mm rebuilds the whole model with no errors. — Y/N
8. Changing `wall` by 0.5 mm rebuilds the whole model with no errors. — Y/N
9. The timeline order is: block, fillets, shell, split, openings. — Y/N
10. The openings stay correctly placed after a size change. — Y/N

---

## Check Your Understanding

**1.** A board is 38 mm wide. Clearance is 0.5 mm per side and walls are 1.5 mm. What is the enclosure's outer width?

- A. 39 mm
- B. 41 mm
- C. 42 mm
- D. 44 mm

<details>
<summary>Answer</summary>

**C.** 38 + 2 × 0.5 + 2 × 1.5 = 42 mm. **A** is the inner cavity only. **B** adds the walls but forgets the clearance. **D** would be the result for a 40 mm board.

</details>

**2.** A sketch's lines are still blue after all dimensions are added. What does that mean, and what should you do?

- A. The sketch is fine; blue is the default colour.
- B. The sketch has too many constraints; delete some.
- C. The model needs to be saved.
- D. Something can still move; add the missing constraint or dimension until every line turns black.

<details>
<summary>Answer</summary>

**D.** In Fusion, blue means under-constrained. **A** is wrong: fully constrained geometry turns black. **B** describes over-constraint, which Fusion refuses to apply rather than showing blue. **C** is unrelated.

</details>

**3.** A fillet fails after a parameter change. What is the most likely cause, and fix?

- A. The edge it referred to no longer exists or has changed; re-select the edge, and consider moving the fillet earlier in the timeline.
- B. The fillet radius is too small; increase it.
- C. Fusion cannot fillet after a change; delete the fillet.
- D. The model needs more parameters.

<details>
<summary>Answer</summary>

**A.** Features refer to the edges and faces made by earlier ones, and a change can remove or replace them. Fixing the reference, and keeping the order "big shapes first, details last", solves most such failures. **B** may occasionally matter, but it is not the usual cause. **C** is false. **D** does not touch the broken reference.

</details>

**4.** Why are the case's corners filleted before it is split into a lid and a base?

- A. Fillets cannot be applied after a split.
- B. One fillet on one body gives the lid and base exactly matching corners.
- C. It makes the file smaller.
- D. Split Body needs rounded corners.

<details>
<summary>Answer</summary>

**B.** One feature on one body guarantees the two parts match. Filleting them separately risks different radii or references. **A**, **C** and **D** are not true.

</details>

**5.** Which parameter should be a formula rather than a typed value?

- A. `pcb_w`, the board width
- B. `wall`, the wall thickness
- C. `clearance`, the air gap
- D. `outer_w`, the enclosure's outer width

<details>
<summary>Answer</summary>

**D.** The outer width follows from the board, clearance and wall, so it should be calculated from them. **A**, **B** and **C** are drivers: values you choose or take from the board, which the rest of the model follows.

</details>

**6.** You want Shell to turn a solid block into a closed hollow box, to split later. What do you select in the Shell dialog?

- A. The top face
- B. The body, with no face selected
- C. All six faces
- D. The sketch the block was made from

<details>
<summary>Answer</summary>

**B.** Selecting the body hollows it without removing a face, leaving a closed box. **A** removes the top, giving an open tray. **C** would remove every face and leave nothing to shell. **D** is not a valid Shell input.

</details>

**7.** You cut the display window into the lid, and the cut also goes through the floor of the base. What setting fixes it?

- A. In the cut's Extrude dialog, leave only `lid` ticked under **Objects To Cut**.
- B. Make the window smaller.
- C. Move the window sketch onto the base.
- D. Delete the base and model it again.

<details>
<summary>Answer</summary>

**A.** Objects To Cut limits which bodies a cut can touch. **B** does not stop the cut going through. **C** makes it worse. **D** throws away work for a one-click fix.

</details>

---

## What Comes Next

In [E1 — Materials, Colour and Rendering](E1-materials-colour-rendering.md) you will choose what the enclosure is printed in and capture its presentation image. Then, in E2, you will bring the board STEP you exported in C3 into this model and fit it inside.

---

## References

1. Autodesk. *Education software overview* (free, one-year access for eligible students and educators, renewable while eligible). https://www.autodesk.com/education/edu-software/overview
2. Onshape. *Variable Studios* (help documentation for defining and sharing variables across part studios). https://cad.onshape.com/help/Content/VariableStudio/variable_studio.htm
3. Autodesk. *How to Create and Edit Parameters in Fusion for Simplified Design Control* (user parameters: name, unit, value, comment). https://www.autodesk.com/products/fusion-360/blog/mastering-fusion-parameters-a-guide-for-simplified-design-control/
4. Autodesk. *Fusion Help*. https://help.autodesk.com/view/fusion360/ENU/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
