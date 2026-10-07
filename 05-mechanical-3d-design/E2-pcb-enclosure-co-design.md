# E2 — PCB and Enclosure Co-Design
## Putting the Real Board Inside the Real Case, and Checking Nothing Collides

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Mechanical and 3D Design
**Time:** ~1.5 hours · **You will produce:** a CAD assembly with the real board model inside the enclosure, and a clean interference check

---

### Two Correct Designs That Do Not Fit Together

By now you have a board that passes DRC and an enclosure that updates when its parameters change. Each is correct on its own. Put them together for the first time and problems appear that neither could show alone: a connector sits 1 mm lower than the case opening; a mounting hole lands on a rib; the tallest module pushes into the lid; the antenna cable has nowhere to go.

To find these problems, put the real board model inside the real case model and check. Some fixes belong on the board, so this unit also covers sending changes back to KiCad. As in E0, everything here uses Fusion's Design workspace and its Solid tools.

### What You Will Be Able to Do After This Reading

- **Make sure** every part on the board has a 3D model, and **find** one, or make a stand-in, when it does not.
- **Insert** the board STEP from C3 into your E0 case, and **fix** it in place.
- **Design** mounting bosses and connector openings from the board's real geometry.
- **Measure** the component stack in CAD and **decide** whether it meets your thickness requirement.
- **Run** an interference check and a section analysis, **resolve** what they find, and **send** board changes back to KiCad.

---

## Before You Start

| You need | From |
|---|---|
| Your board exported as STEP, with every part's 3D model attached | C3 Step 13 |
| Your parametric two-part case (`base` and `lid`) | E0 |
| The thickness requirement and openings list | A0 and your C0 concept |
| esp_watch's board STEP, to follow along | [`pcb/esp_Watch/esp_Watch.step`](https://github.com/niat-physicalai/esp_watch/blob/main/pcb/esp_Watch/esp_Watch.step) |

---

# Part 1 — From KiCad to Fusion

## The Trap: Parts With No 3D Model

The board STEP you exported in C3 contains only the components whose footprints have a **3D model** attached (C2 Step 8). A part with no model exports as nothing: just its pads on a flat board. The CAD model looks tidy, the interference check passes, and the real module, sitting on its header, crashes into the lid.

So before importing, open KiCad's 3D viewer (**View → 3D Viewer**) and check that every part is there. For each one that is missing, find a model in this order:

| Where | Good for |
|---|---|
| KiCad's own library | Standard parts: headers, sockets, buttons, passives. Library footprints usually have one attached already. |
| The manufacturer's or seller's product page | Branded parts and modules, such as Würth switches or Seeed boards |
| A model-sharing site, such as GrabCAD | Common hobby modules, uploaded by other users. Check the size against your part before trusting it. |
| A box you model yourself in Fusion | Anything with no model. Measure the outline and height, extrude a box, export it as STEP, and attach it to the footprint. |

A box is a stand-in, like the mock sensors in the firmware module: it has the size that matters for this check and nothing else. A beautiful model is not required.

Some parts are not on the board at all: the battery, a strap, a cable. They will not be in the board STEP, so model them as boxes directly in your Fusion case.

<!-- REFPRODUCT:START -->
esp_watch's repository has STEP models for every part on its board: the XIAO, the MAX30102, MPU-6050 and OLED modules, the female header and the Würth slide switch, in `pcb/esp_Watch/3d models/`; the push buttons use KiCad's library model. Its exported `esp_Watch.step` therefore shows the full stack. The battery is not on the board and has no model, so it is a box: **30 × 12 × 4 mm**, standing on end in the slot behind the OLED's header.
<!-- REFPRODUCT:END -->

![esp_watch board, KiCad 3D render from the side: the module stack that the enclosure must fit around](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_side.png)

## Step 1: Insert the Board Into the Case

1. **Upload the STEP.** Open the **Data Panel** (the grid icon at the top left), go to your product's project, click **Upload**, and choose the board's `.step` file. Fusion converts it into a design [2].
2. **Insert it.** With your E0 case open, right-click the uploaded board in the Data Panel and choose **Insert into Current Design**. It arrives as its own **component**.
3. **Position it.** Use **Modify → Move/Copy (M)** to drop the board into the base, centred on the origin, resting at the height its standoffs or bosses will give it.
4. **Fix it.** Right-click the board component in the browser and choose **Ground**. A grounded component cannot be moved by accident. You place case features around it; you never edit it.
5. **Name it** with its revision, for example `pcb_v1`. When C3 changes the board, you insert `pcb_v2` beside it and see what moves.

<!-- MEDIA
type: screenshot
id: E2-W01
caption: esp_watch's board STEP inserted into the case and grounded
brief: Autodesk Fusion, Design workspace. The enclosure base visible, the lid hidden or
  translucent. The imported esp_watch board sits in the base cavity: 37.8 × 39 mm board,
  the OLED raised on its female header above the MPU-6050 (a 4–5 mm air gap between them),
  the XIAO with its USB-C connector at the left edge, and the MAX30102 module on the
  underside. A 30 × 12 × 4 mm battery box standing on end behind the OLED header, in a
  contrasting colour. Browser shows bodies "base", "lid" and the grounded component
  "pcb_v1" (pin icon). Light theme.
-->

---

# Part 2 — Designing Around the Board

## Step 2: Mounting Bosses From the Real Holes

A **boss** is a raised post in the case that the board sits on or screws to. A **standoff** is a separate spacer between two boards or between a board and a module. Place them from the board's actual mounting holes, not from a guess.

1. **Create Sketch** on the inside face of the base's floor.
2. **Create → Project / Include → Project (P)**, and click the edge of each mounting hole on the board. Fusion copies their circles into your sketch, linked to the board.
3. Draw a circle around each projected hole for the boss's outside, dimensioned with a parameter such as `boss_d`.
4. **Extrude (E)** the ring up to the underside of the board, with **Operation: Join** onto the `base` body.

Because the circles are projected, the bosses follow the board if the holes move in the next revision. E3 sizes the boss and the screw hole for printing.

<!-- REFPRODUCT:START -->
esp_watch has **four mounting holes**: two at the top corners and two in the middle. They hold the MPU-6050 and OLED modules on standoffs; the OLED also sits on a female header, which raises it above the MPU-6050 with a 4–5 mm air gap. Take the hole positions by projecting them from the board model, not by measuring a render.
<!-- REFPRODUCT:END -->

## Step 3: Openings for Connectors and Controls

Every part the user touches or plugs into needs an opening, sized from the part and positioned from the board model. Sketch each one on the case wall or lid, **project** the part's outline from the board as a guide, and cut it with **Extrude → Cut**, with only the right body ticked under **Objects To Cut** (E0 Step 9).

| Opening | Size it from | Check |
|---|---|---|
| USB-C port | The plug's overmould, not the socket, because the cable must fit | The plug fully seats with the case in place |
| Button caps or plungers | The button's actuator, plus clearance for movement | The button can travel fully without binding |
| Slide switch | The slider's full travel | Both end positions are reachable |
| Display window | The display's active area, not the whole module | No border visible, no pixels hidden |

<!-- REFPRODUCT:START -->
esp_watch's openings: the XIAO's **USB-C port on the left side** of the case, and four in the lid for the **display window, two buttons and the slide switch**.
<!-- REFPRODUCT:END -->

### Worked Example: Sizing the USB-C Opening

**Step 1: Find the socket's position** in the imported board: its centre height above the case floor and its position along the wall. Use **Inspect → Measure (I)** on the board model.

**Step 2: Size the opening for the plug**, not the socket. **Example values:** a USB-C cable's plug overmould about 12 × 6.5 mm, with 0.5 mm clearance each side.

```text
Opening width  = 12.0 + 2 × 0.5 = 13.0 mm
Opening height =  6.5 + 2 × 0.5 =  7.5 mm
```

**Step 3: Check the wall.** The plug must reach the socket through the wall. If the wall is 1.5 mm thick and the socket's face sits 0.5 mm inside the board edge, which itself sits 0.5 mm (the clearance) inside the wall, the plug must travel 2.5 mm before it meets the socket face.

```text
Wall thickness                  1.5 mm
Board-to-wall clearance         0.5 mm
Socket face set back from edge  0.5 mm   (example value; measure yours)
─────────────────────────────────────
Distance plug travels in        2.5 mm
```

**Check.** An opening sized for the overmould lets the overmould enter the wall, so the plug seats. If the opening is smaller, the overmould stops at the outside of the wall. The metal shell must then cross these 2.5 mm *and* still go fully into the socket, which many cables cannot. Fixes: enlarge the opening, thin the wall locally, or move the socket closer to the board edge in C3.

## Clearance to Tall Parts, and Keep-Outs

Leave a gap between every part and the case, as you did with the `clearance` parameter in E0. The gap matters most above the tallest part and beside anything that moves, bends or gets warm.

Also mark areas the case must stay clear of:

- **The antenna.** No case features, screws or metal close to it, and a path along the inside of the case for its cable.
- **The battery.** A bay that holds it without pressing on it (E4 covers this).
- **Cables**, such as a display's flexible ribbon, which need room to bend gently.

<!-- REFPRODUCT:START -->
esp_watch's external antenna is to be routed along the inside of the case, away from the battery, which stands on end behind the OLED's header. In CAD, sketch the intended antenna path as a line along the inner wall and keep features off it.
<!-- REFPRODUCT:END -->

---

# Part 3 — Measuring the Stack

## The Number That Sets the Thickness

On a module-based board, the tallest stack of parts decides the product's thickness.

<!-- REFPRODUCT:START -->
On esp_watch, the OLED sits on a female header above the MPU-6050, with a 4–5 mm air gap between them. The recorded height is **14.044 mm**, measured from the board to the top of the OLED. The board itself and the MAX30102 module on the underside add to that, so the case must hold more than 14.044 mm. In C0, the thickness budget added walls and clearance and reached about 18 mm, against an example requirement of 16 mm.
<!-- REFPRODUCT:END -->

### Worked Example: Measure, Then Decide

**Step 1: Measure in CAD.** With the board inserted, use **Measure** from the underside of the lowest part to the top of the highest part. Compare it with the number you used in C0 and E0's `stack_h`. If they differ, update `stack_h` in **Change Parameters**, and the case follows.

**Step 2: Find what sets it.** Section the assembly through the tallest point (Step 4). Identify each layer in the stack and its height. **Example breakdown** for a stacked module design:

```text
Display module thickness           ~ 3 mm
Header gap above the IMU           ~ 5 mm
IMU module on its header           ~ 4 mm
Board thickness                    ~ 1.6 mm
Parts below the board              ~ rest
```

> **Teaching model.** These layer heights are illustrative, to show how a stack is broken down. Measure yours in CAD.

**Step 3: Decide.** For each layer, ask whether it could be smaller: a lower header, a shorter standoff, a module moved from *above* another to *beside* it, as in C0's concept B.

**Check.** The decision is either "accept the thickness and update the requirement in writing" or "change the board". Either is fine. Leaving the two out of step is not.

---

# Part 4 — Checking and Closing the Loop

## Step 4: Interference Check and Section Analysis

Two tools in the **Inspect** panel answer the question "does it fit?":

- **Inspect → Interference** [2] compares what you select and reports every place where two solids overlap. Select the board component, the battery box, `base` and `lid`, and click **Compute**. Each overlap is listed and shown in red.
- **Inspect → Section Analysis** cuts the model along a plane so you can see inside it: gaps, wall thickness, how parts stack. Pick a plane, drag the arrow to move the cut, and measure across it.

A clean interference check means **no overlaps** between the board, every part on it, and the case. But "no overlap" is not "enough clearance". Section through the tallest part and the connectors, and measure the gaps. A 0.05 mm gap passes the interference check and will fail in a real print.

<!-- MEDIA
type: screenshot
id: E2-W02
caption: Fusion's interference check between the board and the case, with one collision found
brief: Autodesk Fusion, Inspect > Interference dialog open, with pcb_v1, the battery box,
  base and lid selected. The results list shows one interference between the OLED module
  and the lid, and the overlapping volume is highlighted in red in the model. The lid is
  semi-transparent so the collision is visible. Light theme.
-->

<!-- MEDIA
type: screenshot
id: E2-W03
caption: A section view through the tallest stack, with each gap measured
brief: Autodesk Fusion, Section Analysis cutting the assembly vertically through the OLED,
  the MPU-6050 and the board. The cut faces are hatched. Measurement annotations show: gap
  between the OLED top and the lid underside, lid thickness, base thickness, and the total
  height. The MAX30102 module on the underside visible, with the base below it.
-->

## Step 5: Send Changes Back to the Board

Some fixes belong on the board: moving a connector closer to the edge, shifting a mounting hole off a rib, changing the outline to fit a rounded case. Make those changes in KiCad, not by forcing the case to fit a board that is wrong.

For the **board outline**, the case is often the better place to design it, because the outline must match the inside of the case. Sketch it in Fusion, right-click the sketch in the browser and choose **Save As DXF**. In KiCad's PCB Editor, use **File → Import → Graphics** to place the DXF on the **Edge.Cuts** layer [1]. Then re-export the board as STEP, insert it as the next revision, and repeat the checks.

```text
Fusion: board outline sketch ──(DXF)──► KiCad: Edge.Cuts
                                           │
          KiCad: layout, DRC               │
                                           ▼
Fusion: interference check ◄──(STEP)── KiCad: export board with 3D models
```

Expect to run this loop several times. Commit the board and the case to your design pack's repository together each time, so a case version always has the board version it was checked against ([Version Control](../01-system-architecture/REF-version-control.md), Step 3).

---

## Tool Reference

| Tool | Where | Key | Use it to |
|---|---|---|---|
| Upload | Data Panel | — | Bring the board STEP into your Fusion project |
| Insert into Current Design | Data Panel, right-click | — | Place the board in the case design as a component |
| Move/Copy | Modify | M | Position the board |
| Ground | Browser, right-click a component | — | Fix the board in place |
| Project | Sketch: Create → Project / Include | P | Copy board geometry, such as hole circles, into a sketch |
| Interference | Inspect | — | Find solids that overlap |
| Section Analysis | Inspect | — | Cut the view open to see and measure gaps |
| Measure | Inspect | I | Measure heights and gaps |
| Save As DXF | Browser, right-click a sketch | — | Send an outline to KiCad |

---

# Putting It All Together

## Applying What You Have Learned

**1. Give every part a 3D model.** Check your board in KiCad's 3D viewer. For each part without a model, find one or make a box of its measured outline and height, and attach it. Model off-board parts, such as the battery, as boxes in Fusion.

**2. Insert and ground.** Insert your board STEP into your E0 case, position it, ground it and name it with its revision.

**3. Build the mounting and openings** from the board's real geometry: bosses from projected hole centres, and every opening sized from the part. Check that the charging plug seats, as in the USB-C worked example.

**4. Measure the stack.** Update `stack_h` to the measured value, and write your thickness decision.

**5. Check.** Run the interference check to zero overlaps, then section through the tallest part and every connector, and record the gaps.

**Deliverable:** the Fusion assembly with the real board inside (`.f3d` export), a screenshot of a clean interference check, and your section measurements and thickness decision, saved in your design pack as `E2-fit/`.

## Self-Check

Open your assembly and answer each item Y or N.

1. Every component on the board appears in the CAD model, with at least a box of the right size. — Y/N
2. Off-board parts, such as the battery, are modelled as boxes. — Y/N
3. The board is a separate, named, grounded component. — Y/N
4. Mounting bosses are built from projected hole positions. — Y/N
5. Every connector and control has an opening sized from the part. — Y/N
6. The charging plug's travel through the wall has been checked. — Y/N
7. `stack_h` equals the height measured in CAD. — Y/N
8. The interference check reports zero overlaps. — Y/N
9. Section measurements show at least your chosen clearance above the tallest part. — Y/N
10. Any board change is recorded as a change to make in KiCad, not only in the case. — Y/N

---

## Check Your Understanding

**1.** An interference check between a board and its case reports no overlaps, but the real board will not fit. What is the most likely cause?

- A. The interference check is broken.
- B. The case is too big.
- C. One or more footprints have no 3D model, so a tall module was missing from the exported STEP.
- D. The board is too thin.

<details>
<summary>Answer</summary>

**C.** Parts without 3D models export as nothing, so the check cannot see them. **A** blames the tool for data it was never given. **B** would not stop a board fitting. **D** is not the usual cause.

</details>

**2.** Why build mounting bosses from projected hole circles rather than typed coordinates?

- A. Projected geometry follows the board, so if the holes move in a board revision, the bosses move with them.
- B. It is faster to draw.
- C. Fusion cannot use typed coordinates.
- D. It makes the bosses stronger.

<details>
<summary>Answer</summary>

**A.** It links the case to the board's real geometry. **B** may or may not be true, and is not the point. **C** is false. **D** is unrelated.

</details>

**3.** A USB-C opening is sized exactly to the socket on the board. What is likely to go wrong?

- A. Nothing.
- B. The socket will fall out.
- C. The board will overheat.
- D. The cable's plug overmould is larger than the socket, so the plug cannot enter the opening far enough to seat.

<details>
<summary>Answer</summary>

**D.** The plug is what passes through the wall, so the opening must fit the plug. **A** ignores the plug. **B** and **C** have no connection to the opening size.

</details>

**4.** The interference check is clean, but a section shows 0.05 mm between the display and the lid. What should you do?

- A. Nothing; no overlap means it fits.
- B. Increase the gap to your chosen clearance, because a 3D-printed part will not hold 0.05 mm, and the display could be pressed or the lid may not close.
- C. Remove the lid.
- D. Make the display thinner.

<details>
<summary>Answer</summary>

**B.** "No overlap" and "enough clearance" are different tests; printing tolerances need a real gap (E3). **A** confuses the two. **C** and **D** are not sensible fixes.

</details>

**5.** A connector needs to be 1 mm closer to the board edge for the plug to seat. Where should the change be made?

- A. In the CAD case, by carving the wall away.
- B. In the slicer.
- C. In KiCad, by moving the connector footprint, then re-exporting the STEP and re-checking.
- D. Nowhere; users can push harder.

<details>
<summary>Answer</summary>

**C.** The root cause is the connector's position on the board, so fix it there and re-check. **A** can be a valid local fix if the wall allows it, but it weakens the wall and hides the real cause. **B** cannot change geometry. **D** is not engineering.

</details>

**6.** Your board STEP looks complete, but the case still needs to hold a 30 × 12 × 4 mm battery. Why is the battery not in the STEP, and what do you do?

- A. KiCad left it out by mistake; re-export.
- B. It is not a part on the board, so it has no footprint; model it as a box in Fusion and include it in the checks.
- C. Batteries never need clearance.
- D. Add a battery footprint to the board just to get the model.

<details>
<summary>Answer</summary>

**B.** The STEP holds only what has a footprint on the board. Off-board parts are modelled in the case design. **A** is not a fault. **C** is false: E4 needs a bay that does not press on the cell. **D** adds a fake part to the board and its BOM.

</details>

---

## What Comes Next

In [E3 — Design for Manufacturing](E3-design-for-manufacturing.md) you will make sure the case you have designed can actually be 3D printed, and see what would change if it were moulded instead.

---

## References

1. KiCad. *PCB Editor documentation, version 10.0* (importing graphics onto board layers; board outline on Edge.Cuts; 3D models in footprint properties). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html
2. Autodesk. *Fusion Help* (Data Panel upload, Insert into Current Design, Interference, Section Analysis). https://help.autodesk.com/view/fusion360/ENU/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
