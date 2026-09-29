# E2 — PCB and Enclosure Co-Design
## Putting the Real Board Inside the Real Case, and Checking Nothing Collides

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Mechanical and 3D Design
**Time:** ~1.5 hours · **You will produce:** a CAD assembly with the real board model inside the enclosure, and a clean interference check

---

### Two Correct Designs That Do Not Fit Together

By now you have a board that passes DRC and an enclosure that updates when its parameters change. Each is correct on its own. Put them together for the first time and problems appear that neither could show alone: a connector sits 1 mm lower than the case opening; a mounting hole lands on a rib; the tallest module pushes into the lid; the antenna cable has nowhere to go.

To find these problems, put the real board model inside the real case model and check. Some fixes belong on the board, so this unit also covers sending changes back to KiCad.

### What You Will Be Able to Do After This Reading

- **Export** a board with its components from KiCad as a STEP model, and **import** it into CAD.
- **Design** mounting bosses, standoffs and connector openings from the board's real geometry.
- **Measure** the board's component stack in CAD and **decide** whether it meets your thickness requirement.
- **Run** an interference check and a section analysis, and **resolve** what they find.
- **Send** changes back to the board, such as a revised outline, in a form KiCad can import.

---

# Part 1 — From KiCad to CAD

## Exporting the Board as STEP

**STEP** is a standard 3D file format that almost every CAD tool can open. KiCad exports the board as a STEP file, including the 3D model of every component that has one. In the PCB editor it is under the File menu's export options. 

## The Trap: Parts With No 3D Model

A STEP export only contains components whose footprints have a **3D model** attached. KiCad's standard library footprints, such as pin headers and sockets, usually have one. A footprint you drew yourself in C2, or one you downloaded, often has none.

A part with no 3D model exports as nothing: just its pads on a flat board. The CAD model looks tidy, the interference check passes, and the real module, sitting on its header, crashes into the lid.

<!-- REFPRODUCT:START -->
esp_watch is exposed to this: its MAX30102 footprint was generated and its XIAO footprint downloaded (C2). Every active part is a module. Without 3D models, the export shows a bare board, not a 14 mm stack.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — whether the MAX30102, XIAO, MPU-6050 and SSD1306 footprints have 3D models attached in the KiCad project is not recorded in REFERENCE-PRODUCT.md -->

The fix is simple, and worth doing even with a rough model. In Fusion, model each module as a box of its measured size (body outline and height), export it as STEP, and attach it to the footprint in KiCad's footprint properties, under 3D Models. A box with the right outline and height is enough to catch collisions. A beautiful model is not required.

> **Teaching model.** A box is a stand-in, like the mock sensors in the firmware module: it has the size that matters for this check and nothing else. Replace it with a better model if one becomes available.

## Importing Into Fusion

Open or upload the STEP file in Fusion, then insert it into your enclosure design as its own component. Keep it as a separate, **fixed** component: you will place case features around it, not edit it. Name it clearly, for example `pcb_v1`, so that when C2 changes the board you can replace it with `pcb_v2` and see what moves.

<!-- MEDIA
type: screenshot
id: E2-01
caption: The esp_watch board STEP, with module stand-in boxes, placed inside the enclosure in Fusion
brief: Autodesk Fusion, design with the enclosure base visible and the lid hidden or made
  translucent. The imported board sits in the base cavity: 38 × 38 mm board, with the
  display module raised on a female header above the motion-sensor module (a 4–5 mm air gap between them), the XIAO module with
  its USB-C connector at the left edge, and the heart-rate module on the underside. Module
  stand-ins shown as simple boxes in a contrasting colour. Browser panel shows components
  "enclosure_base", "enclosure_lid", "pcb_v1". Light theme.
-->

<!-- ASSET:PLACEHOLDER reference-files/images/render-iso.png -->
![esp_watch board, KiCad 3D render, showing the module stack that the enclosure must fit around](../reference-files/images/render-iso.png)

---

# Part 2 — Designing Around the Board

## Mounting: Bosses and Standoffs

A **boss** is a raised post in the case that the board sits on or screws to. A **standoff** is a separate spacer between two boards or between a board and a module. Place them from the board's actual mounting holes, not from a guess.

In Fusion, project the mounting hole centres from the imported board onto a sketch in the case, and build the bosses from those projected points. Then the bosses follow the board if the board moves.

<!-- REFPRODUCT:START -->
esp_watch has **four mounting holes**: two at the top corners and two in the middle. They hold the motion-sensor and display modules on standoffs; the display also sits on a female header, which raises it above the motion sensor with a 4–5 mm air gap. The hole diameter and positions are not recorded, so take them from the board file, not from a render.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — mounting hole diameter and exact positions are not recorded in REFERENCE-PRODUCT.md -->

## Openings for Connectors and Controls

Every part the user touches or plugs into needs an opening, sized from the part and positioned from the board model:

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

**Step 1: Find the socket's position** in the imported board: its centre height above the case floor and its position along the wall. Use Fusion's Measure tool on the board model.

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

**Check.** An opening sized for the overmould lets the overmould enter the wall, so the plug seats. If the opening is smaller, the overmould stops at the outside of the wall. The metal shell must then cross these 2.5 mm *and* still go fully into the socket, which many cables cannot. Fixes: enlarge the opening, thin the wall locally, or move the socket closer to the board edge in C2.

## Clearance to Tall Parts, and Keep-Outs

Leave a gap between every part and the case, as you did with the `clearance` parameter in E0. The gap matters most above the tallest part and beside anything that moves, bends or gets warm.

Also mark areas the case must stay clear of:

- **The antenna.** No case features, screws or metal close to it, and a path along the inside of the case for its cable.
- **The battery.** A bay that holds it without pressing on it (E4 covers this).
- **Cables**, such as a display's flexible ribbon, which need room to bend gently.

<!-- REFPRODUCT:START -->
esp_watch's external antenna is to be routed along the inside of the case, away from the battery, which stands on end behind the display's header. In CAD, sketch the intended antenna path as a line along the inner wall and keep features off it.
<!-- REFPRODUCT:END -->

---

# Part 3 — Measuring the Stack

## The Number That Sets the Thickness

On a module-based board, the tallest stack of parts decides the product's thickness.

<!-- REFPRODUCT:START -->
On esp_watch, the display sits on a female header above the motion-sensor module, with a 4–5 mm air gap between them, and the board with parts fitted is recorded as **14.044 mm** tall. That stack sets the watch's thickness. In C0, the thickness budget added walls and clearance and reached about 18 mm, against an example requirement of 16 mm.
<!-- REFPRODUCT:END -->

### Worked Example: Measure, Then Decide

**Step 1: Measure in CAD.** With the board imported, use Measure between the underside of the lowest part and the top of the highest part. Compare it with the number you used in C0 and E0's `stack_h`. If they differ, update `stack_h`, and the case follows.

**Step 2: Find what sets it.** Section the assembly through the tallest point (Part 4). Identify each layer in the stack and its height. **Example breakdown** for a stacked module design:

```text
Display module thickness           ~ 3 mm
Standoff gap above the IMU         ~ 5 mm
IMU module on its header           ~ 4 mm
Board thickness                    ~ 1.6 mm
Parts below the board              ~ rest
```

> **Teaching model.** These layer heights are illustrative, to show how a stack is broken down. Measure yours in CAD.

**Step 3: Decide.** For each layer, ask whether it could be smaller: a lower header, a shorter standoff, a module moved from *above* another to *beside* it, as in C0's concept B.

**Check.** The decision is either "accept the thickness and update the requirement in writing" or "change the board". Either is fine. Leaving the two out of step is not.

---

# Part 4 — Checking and Closing the Loop

## Interference Check and Section Analysis

Two Fusion tools answer the question "does it fit?":

- **Interference** (in the Inspect menu) compares selected components and reports every place where two solids overlap. Select the board and both halves of the case, and run it.
- **Section analysis** (also under Inspect) cuts the model along a plane so you can see inside it: gaps, wall thickness, how parts stack.

A clean interference check means **no overlaps** between the board, including every module stand-in, and the case. But "no overlap" is not "enough clearance". Section through the tallest part and the connectors, and measure the gaps. A 0.05 mm gap passes the interference check and will fail in a real print.

<!-- MEDIA
type: screenshot
id: E2-02
caption: Fusion's interference check between the board and the case, with one collision found
brief: Autodesk Fusion, Inspect > Interference dialog open, with pcb_v1, enclosure_base and
  enclosure_lid selected. The results list shows one interference between a module
  stand-in box and the lid, and the overlapping volume is highlighted in red in the model.
  The lid is semi-transparent so the collision is visible. Light theme.
-->

<!-- MEDIA
type: screenshot
id: E2-03
caption: A section view through the tallest stack, with each gap measured
brief: Autodesk Fusion, section analysis cutting the assembly vertically through the
  display, the motion-sensor module and the board. The cut faces are hatched. Measurement
  annotations show: gap between the display top and the lid underside, lid thickness,
  base thickness, and the total height. The heart-rate module on the underside visible,
  with the base below it.
-->

## Sending Changes Back to the Board

Some fixes belong on the board: moving a connector closer to the edge, shifting a mounting hole off a rib, changing the outline to fit a rounded case. Make those changes in KiCad, not by forcing the case to fit a board that is wrong.

For the **board outline**, the case is often the better place to design it, because the outline must match the inside of the case. Sketch it in Fusion, save the sketch as a DXF file, and import that DXF onto KiCad's board-outline layer (Edge.Cuts) using the PCB editor's graphics import [2]. Then re-export the board as STEP and repeat the checks.

```text
Fusion: board outline sketch ──(DXF)──► KiCad: Edge.Cuts
                                           │
          KiCad: layout, DRC               │
                                           ▼
Fusion: interference check ◄──(STEP)── KiCad: export board with 3D models
```

Expect to run this loop several times.

---

# Putting It All Together

## Applying What You Have Learned

**1. Give every part a 3D model.** For each footprint without one, make a box of the part's measured outline and height and attach it.

**2. Export and import.** Export your board as STEP and insert it into your E0 enclosure as a fixed component.

**3. Build the mounting and openings** from the board's real geometry: bosses from projected hole centres, and every opening sized from the part. Check that the charging plug seats, as in the USB-C worked example.

**4. Measure the stack.** Update `stack_h` to the measured value, and write your thickness decision.

**5. Check.** Run the interference check to zero overlaps, then section through the tallest part and every connector, and record the gaps.

**Deliverable:** the CAD assembly with the real board inside, a screenshot of a clean interference check, and your section measurements and thickness decision, saved in your design pack.

## Self-Check

Open your assembly and answer each item Y or N.

1. Every component on the board appears in the CAD model with at least a box of the right size. — Y/N
2. The board is a separate, named, fixed component. — Y/N
3. Mounting bosses are built from the board's actual hole positions. — Y/N
4. Every connector and control has an opening sized from the part. — Y/N
5. The charging plug's travel through the wall has been checked. — Y/N
6. `stack_h` equals the height measured in CAD. — Y/N
7. The interference check reports zero overlaps. — Y/N
8. Section measurements show at least your chosen clearance above the tallest part. — Y/N
9. Keep-outs for the antenna, battery and any cable are marked. — Y/N
10. Any board change is recorded as a change to make in KiCad, not only in the case. — Y/N

---

## Check Your Understanding

**1.** An interference check between a board and its case reports no overlaps, but the real board will not fit. What is the most likely cause?

- A. The interference check is broken.
- B. One or more footprints have no 3D model, so the tall module was not in the exported STEP at all.
- C. The case is too big.
- D. The board is too thin.

<details>
<summary>Answer</summary>

**B.** Parts without 3D models export as nothing, so the check cannot see them. **A** blames the tool for data it was never given. **C** would not stop a board fitting. **D** is not the usual cause.

</details>

**2.** Why build mounting bosses from projected hole centres rather than typed coordinates?

- A. It is faster to draw.
- B. Projected points follow the board, so if the holes move in a board revision, the bosses move with them.
- C. Fusion cannot use typed coordinates.
- D. It makes the bosses stronger.

<details>
<summary>Answer</summary>

**B.** It links the case to the board's real geometry. **A** may or may not be true, and is not the point. **C** is false. **D** is unrelated.

</details>

**3.** A USB-C opening is sized exactly to the socket on the board. What is likely to go wrong?

- A. Nothing.
- B. The cable's plug overmould is larger than the socket, so the plug cannot enter the opening far enough to seat.
- C. The socket will fall out.
- D. The board will overheat.

<details>
<summary>Answer</summary>

**B.** The plug is what passes through the wall, so the opening must fit the plug. **A** ignores the plug. **C** and **D** have no connection to the opening size.

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
- B. In KiCad, by moving the connector footprint, then re-exporting the STEP and re-checking.
- C. In the slicer.
- D. Nowhere; users can push harder.

<details>
<summary>Answer</summary>

**B.** The root cause is the connector's position on the board, so fix it there and re-check. **A** can be a valid local fix if the wall allows it, but it weakens the wall and hides the real cause. **C** cannot change geometry. **D** is not engineering.

</details>

---

## What Comes Next

In [E3 — Design for Manufacturing](E3-design-for-manufacturing.md) you will make sure the case you have designed can actually be 3D printed, and see what would change if it were moulded instead.

---

## References

1. KiCad. `kicad-cli pcb export step` (command-line STEP export; options include `--board-only`, `--no-components` and `--subst-models`), as shown by `kicad-cli pcb export step --help` in KiCad 10.0.
2. KiCad. *PCB Editor documentation, version 10.0* (importing graphics onto board layers; board outline on Edge.Cuts; 3D models in footprint properties). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
