# C3 — KiCad Walkthrough: PCB Layout
## From a Checked Schematic to a Board You Could Order

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Form Factor, Schematic and PCB
**Time:** ~2 hours · **You will produce:** a routed two-layer PCB of your own product that passes DRC, a 3D render, and a STEP file of the board

---

### A Board Can Pass Every Check and Still Not Work

Your schematic passes ERC and every footprint is checked. Now the parts need places on a real board, and copper between them. The **PCB Editor** is where the product gets its size, where the sensor ends up facing the skin or not, and where the antenna is helped or blocked. Its **Design Rules Check** (DRC) will tell you whether the board can be made. It will not tell you whether the board is any good: that depends on decisions you make in the order this unit follows.

This unit walks through esp_watch's real board in KiCad 10, step by step, then asks you to lay out your own. As in C1, it shows only what you need to make one board; the PCB Editor manual covers the rest [2].

### What You Will Be Able to Do After This Reading

- **Set** a board's design rules from your fab house's published capabilities.
- **Draw** the board outline and mounting holes from your C0 concept, and **place** parts outside-in.
- **Route** tracks and vias, and **pour** a ground plane on both layers.
- **Keep** an antenna clear of copper, and **reach** zero DRC errors with every warning explained.
- **Export** a 3D render and a STEP file for the enclosure work in Module 5.

---

## Before You Start

| You need | From |
|---|---|
| A schematic with zero ERC errors, every symbol annotated | C1 |
| A footprint, checked and with a 3D model, for every symbol | C2 |
| The board outline, mounting-hole positions and the side for every part | Your C0 concept |
| Your fab house's current capabilities page | e.g. JLCPCB [3] |
| esp_watch's KiCad project, to compare against | `pcb/esp_Watch/` [4] |

<!-- REFPRODUCT:START -->
### What esp_watch's board contains

| Item | On esp_watch |
|---|---|
| Layers | 2 |
| Outline | 37.8 × 39 mm |
| Top side | XIAO ESP32-C3, MPU-6050, OLED (on a female header above the MPU), SW1, SW2, SW3 |
| Bottom side | MAX30102 module, against the wrist |
| Tracks | 0.4 mm for signals, 0.6 mm for the 3.3 V and battery lines |
| Vias | 4 |
| Ground | A GND pour on both layers |
| Silkscreen | Pin names beside each module's pads, and `version 0.1.0` |
| DRC | Zero errors |
<!-- REFPRODUCT:END -->

![esp_watch PCB render, top face](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_top.png)

![esp_watch PCB render, bottom face, with the MAX30102 module](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_back.png)

---

## Step 1: Open the PCB Editor

From the schematic, click **Switch to PCB Editor** in the top toolbar, or open the `.kicad_pcb` file from the Project Manager.

<!-- MEDIA
type: screenshot
id: C3-W01
caption: KiCad's PCB Editor, with the Appearance panel and Selection Filter
brief: KiCad 10 PCB Editor, full window, esp_watch's board open. The right-hand Appearance
  panel (Layers tab) and Selection Filter visible, F.Cu active. Claude adds numbered
  callouts: 1 top toolbar, 2 left toolbar (display), 3 right toolbar (tools), 4 Layers
  tab, 5 Selection Filter, 6 status bar with the unrouted count.
-->

Navigation is the same as in the schematic: drag with the middle or right button to pan, scroll to zoom [1]. On the right, the **Layers** tab of the Appearance panel shows each layer's colour, and clicking a layer's name makes it the **active layer**, the one you draw on. By default front copper (F.Cu) is red and back copper (B.Cu) is blue. Everything is viewed from the front, so parts on the bottom appear mirrored.

## Step 2: Set the Design Rules

Click **File → Board Setup**. Three pages matter.

**Board Stackup → Physical Stackup.** Leave it at **2** copper layers. Two layers are enough for a module-based board, and cost the least.

**Design Rules → Constraints.** These are the smallest track, gap, via and hole the design may use. Take them from your fab house's capabilities page, then stay comfortably above them. JLCPCB currently allows 0.10 mm tracks and gaps on two-layer boards, and copper at least 0.2 mm from a routed edge [3]; numbers like these change, so check the page on the day.

<!-- MEDIA
type: screenshot
id: C3-W02
caption: Board Setup, Design Rules → Constraints
brief: KiCad 10 Board Setup dialog on esp_watch's project, Design Rules → Constraints page:
  minimum track width, clearance, via diameter, through-hole diameter, annular width and
  copper-to-edge clearance visible. Crop to the dialog.
-->

<!-- REFPRODUCT:START -->
esp_watch's board file sets: minimum track 0.2 mm, minimum via 0.5 mm, minimum hole 0.3 mm, minimum annular ring 0.1 mm, and copper at least 0.5 mm from the edge. All sit well above JLCPCB's limits, so the board never depends on the fab's best day.

<!-- FACT:VERIFY esp_watch — REFERENCE-PRODUCT.md §5 records constraints of 0.127 mm track/clearance and 0.3 mm copper-to-edge, and Default 0.25 mm / Power 0.5 mm net classes; the public board file has 0.2 mm minimum track, 0.5 mm copper-to-edge, a single Default class (0.2 mm), and tracks drawn at 0.4 / 0.6 mm. This unit quotes the board file. -->
<!-- REFPRODUCT:END -->

**Design Rules → Net Classes.** A **net class** gives a group of nets its own track width and clearance, so the router uses the right width automatically and DRC checks it. Make two: **Default** for signals, and **Power** (wider) for the supply and battery nets. Assign nets to Power with a pattern such as `+3V3`.

<!-- MEDIA
type: screenshot
id: C3-W03
caption: Board Setup, Net Classes, with a wider class for power
brief: KiCad 10 Board Setup → Design Rules → Net Classes. Default and a Power class with a
  wider track width, and the assignment table below with +3V3 and the battery net matched
  to Power. Crop to the dialog. (esp_watch's file has only Default; set up the Power class
  for the screenshot, or capture another project.)
-->

<!-- REFPRODUCT:START -->
esp_watch uses one net class and picks the width by hand while routing: 0.4 mm for signals, 0.6 mm for the 3.3 V and battery lines, from the track-width list in **Pre-defined Sizes**. That works on a board this small. A Power class does the same job without relying on you to pick the right width every time.
<!-- REFPRODUCT:END -->

## Step 3: Bring the Parts In (F8)

Click **Tools → Update PCB from Schematic** (**F8**). Read the list of changes, click **Update PCB**, close it, and click to drop the footprints on the canvas [1].

<!-- MEDIA
type: screenshot
id: C3-W04
caption: Update PCB from Schematic, then the parts in a heap with their ratsnest
brief: Two shots. (a) KiCad 10 Update PCB from Schematic dialog listing the footprints to
  be added. (b) esp_watch's footprints just after placement, in a heap beside the board
  outline, thin ratsnest lines between their pads. Use a copy of the project with the
  footprints removed first.
-->

The thin lines between pads are the **ratsnest**: connections the schematic wants that are not yet copper. The count of unrouted connections is in the status bar.

**The schematic and board do not sync themselves.** After any schematic change, press **F8** again, or the board will be built from an old schematic.

## Step 4: Draw the Board Outline

Set the grid to **1 mm**, click **Edge.Cuts** in the Layers tab, and draw the outline with the **rectangle** tool [1]. The outline must be one closed shape. Add a **dimension** on each side, so the size is on every drawing of the board.

<!-- MEDIA
type: screenshot
id: C3-W05
caption: esp_watch's 37.8 × 39 mm outline on Edge.Cuts, dimensioned
brief: KiCad 10 PCB Editor, esp_watch's board with only Edge.Cuts and a User.Drawings (or
  Dwgs) layer visible: the rectangular outline with a dimension on each side reading 37.8
  and 39 mm.
-->

The size comes from your C0 concept, not from where the parts happen to land. If the parts do not fit, that is a C0 decision to revisit, not a reason to let the board grow quietly.

## Step 5: Place the Mounting Holes

Mounting holes come next, because the case's bosses and screws (Module 5) line up with them. Place them as footprints from KiCad's `MountingHole` library: `MountingHole_3.2mm_M3` for an M3 screw, for example. Position them exactly, using the footprint's properties (**E**) to type in coordinates.

<!-- REFPRODUCT:START -->
esp_watch has **four mounting holes**: two at the top corners and two in the middle. They hold the MPU-6050 and OLED modules on standoffs.
<!-- REFPRODUCT:END -->

<!-- MEDIA
type: screenshot
id: C3-W06
caption: esp_watch's mounting holes, placed before any part
brief: KiCad 10 PCB Editor, esp_watch's outline with its four mounting holes visible and
  nothing else placed (hide footprints other than the holes, or use a copy). If the holes
  are part of the module footprints rather than separate footprints, say so in the
  reference column of ASSETS-TODO.
-->

## Step 6: Place the Parts, Outside In

Select a footprint and use these keys:

| Key | Does |
|---|---|
| **M** | Move |
| **D** | Drag, keeping attached tracks |
| **R** | Rotate |
| **F** | Flip to the other side of the board |
| **E** | Properties, to type an exact position |

Place in this order, because each step constrains the next:

1. **Parts fixed by the outside world**: connectors at the edge where the case opening will be, buttons where a finger reaches them, sensors on the face where they must look.
2. **Parts that must be near another part**: decoupling capacitors beside their chip, a crystal beside its pins.
3. **Everything else**, arranged so the ratsnest lines do not cross much. Untangled ratsnest means easy routing [1].

Keep courtyards from overlapping, unless two parts really do stack.

<!-- REFPRODUCT:START -->
On esp_watch, step 1 decided almost everything:

- **Board sides** come from C0: everything on top except the MAX30102, which is flipped (**F**) to the bottom, against the wrist.
- **The XIAO's USB-C** faces the left edge, where the case will have its charging opening.
- **The OLED** sits on a female header above the MPU-6050, with a 4–5 mm air gap between them.
- **The battery** is not on the board. It stands in a slot behind the OLED's header, wired to the XIAO's BAT pads through SW3.

Breakout modules carry their own decoupling capacitors, so step 2 had nothing to place: esp_watch's carrier board has none of its own.
<!-- REFPRODUCT:END -->

<!-- MEDIA
type: screenshot
id: C3-W07
caption: esp_watch's parts placed, before routing
brief: KiCad 10 PCB Editor, esp_watch's board with every footprint in its final place and
  the ratsnest visible, no tracks yet (use a copy with tracks deleted). USB-C edge on the
  left visible.
-->

<!-- MEDIA
type: screenshot
id: C3-W08
caption: The MAX30102 module flipped to the bottom layer
brief: KiCad 10 PCB Editor, esp_watch's board viewed with View → Flip Board (bottom view),
  showing the MAX30102 module footprint on B.Cu with its 8 SMD pads, readable.
-->

## Step 7: Route the Tracks (X)

Click the layer to route on (F.Cu or B.Cu), press **X**, click a pad, then click the pad its ratsnest line leads to. The track follows, and the ratsnest line disappears once the connection is copper [1].

<!-- MEDIA
type: gif
id: C3-W09
caption: Routing SDA from the XIAO to a module
brief: KiCad 10 PCB Editor, esp_watch's board with the SDA track deleted. Press X on the
  XIAO's D4 pad and route to the nearest module's SDA pad, with the track-width dropdown
  in the top toolbar visible at 0.4 mm. 5–10 s, about 1000 px wide.
-->

While routing:

- **Change layer with a via:** press **V** mid-track, click to drop the via, and carry on on the other layer [1].
- **Through-hole pads join both layers** already; a track can arrive on one layer and leave on the other.
- **Pick the width** from the track-width dropdown, or let the net class set it.
- **Keep it short and direct.** Route power first, at its wider width; then the bus lines, kept side by side; then the rest.
- Watch the **unrouted count** in the status bar. Routing is finished at 0.

<!-- MEDIA
type: screenshot
id: C3-W10
caption: A via changing a track from the top layer to the bottom
brief: KiCad 10 PCB Editor, zoomed on one of esp_watch's four vias, with the red F.Cu track
  arriving and the blue B.Cu track leaving.
-->

<!-- REFPRODUCT:START -->
esp_watch routes 76 track segments, split almost evenly between the two layers, with only four vias: one each on SDA, SCL, the "previous" button line and 3.3 V. The through-hole pins of the modules and switches do most of the layer changes for free.
<!-- REFPRODUCT:END -->

## Step 8: Pour Ground on Both Layers (B)

Click **Add a filled zone**, click the first corner, and in **Copper Zone Properties** choose the **GND** net and tick **both** F.Cu and B.Cu. Click round the board edge and double-click to finish. Press **B** to fill. Zones are not refilled automatically, so press **B** again after any change, and always before DRC and fabrication [1].

<!-- MEDIA
type: screenshot
id: C3-W11
caption: The GND zone's properties, then the filled board
brief: Two shots. (a) KiCad 10 Copper Zone Properties for esp_watch's GND zone: net GND,
  layers F.Cu and B.Cu both ticked, clearance 0.3 mm. (b) esp_watch's board after B, both
  pours filled, with thermal-relief spokes visible on the GND pads.
-->

A **ground pour** fills the empty copper on a layer and connects it to GND. Every signal needs a path back to its source, and a solid ground under it gives the return current the shortest path. GND pads connect to the pour through thin **thermal-relief** spokes, which make them easier to solder [1]. **Stitching vias**, GND vias dropped every 5–10 mm, join the two pours so neither is left as a separate island.

<!-- REFPRODUCT:START -->
esp_watch has a GND zone on both F.Cu and B.Cu and **no stitching vias**. The two pours join through the GND pins of the through-hole modules and switches, which pass through both layers. On a small board crowded with through-hole parts that is enough; on a board of mostly surface-mount parts, add stitching vias.
<!-- REFPRODUCT:END -->

<!-- REFPRODUCT:START -->
esp_watch routes its 3.3 V rail as a **track**, not as a second copper plane. On two layers, a power plane would be cut into pieces by every signal crossing it, and those cuts would break up the ground under the signals too. A wide track carries a watch's current just as well and leaves the ground pour whole.
<!-- REFPRODUCT:END -->

A common belief is that more copper is always better, so students pour power on one side and ground on the other. On a two-layer board that usually makes things worse, for the reason above.

## Step 9: Keep the Antenna Clear

An antenna radiates into the space around it. Copper nearby, especially a ground pour underneath, changes how it behaves. For a board with an antenna **on** it, such as a module with a printed antenna, draw a **rule area** (**Ctrl+Shift+K**) over the antenna on both layers, set to allow no copper, and refill the zones: the pour flows round it [2].

<!-- MEDIA
type: screenshot
id: C3-W12
caption: A rule area keeping copper away from an antenna
brief: KiCad 10 Rule Area Properties dialog with "Keep out copper fills", "tracks" and
  "vias" ticked on F.Cu and B.Cu, and the hatched rule area on a board under a module's
  antenna end. esp_watch has no rule area (its antenna is on a cable), so capture this on
  any board with an on-board antenna, or a copy of esp_watch's board.
-->

<!-- REFPRODUCT:START -->
esp_watch's board has no rule area, because its antenna is not on the board. The XIAO ESP32-C3 uses an **external antenna** on a U.FL cable, and its rules move into the case: no copper under the antenna on either layer, away from the battery's metal-foil pouch, and routed along the inside of the case wall. Mark the intended antenna position on `User.Drawings` now, so Module 5 can check it.
<!-- REFPRODUCT:END -->

## Step 10: Label the Board

Use the text tool on **F.Silkscreen** for anything someone holding the bare board needs: what each connector or pad is, `+` beside a battery pad, and the board's **revision**.

<!-- REFPRODUCT:START -->
esp_watch prints the pin names beside each module's pads and `version 0.1.0` on the board, matching the schematic's revision. When a board comes back from the fab, the revision on the copper is the only reliable way to tell which files made it.
<!-- REFPRODUCT:END -->

## Step 11: Run DRC

Click **Inspect → Design Rules Checker**, keep **Refill all zones before performing DRC** ticked, and click **Run DRC**. Each violation is listed, and an arrow marks it on the board; click a line to jump to it [1].

<!-- MEDIA
type: screenshot
id: C3-W13
caption: DRC finding violations, with their markers
brief: KiCad 10 DRC dialog on a copy of esp_watch's board with one track dragged (D) too
  close to a pad: a clearance violation listed and selected, its marker visible on the
  board behind.
-->

| DRC message (paraphrased) | Usual cause | Fix |
|---|---|---|
| Clearance violation | A track or pad too close to another net | Move or reroute; refill zones (**B**) |
| Unconnected items | A ratsnest line still open | Route it; check the unrouted count |
| Courtyards overlap | Two parts placed in the same space | Move one, unless they really stack |
| Copper too close to board edge | A pad, track or pour near Edge.Cuts | Move it, or let the pour clearance handle it |
| Schematic parity | The board and schematic disagree | Press **F8** and update the board |

Aim for **zero errors**. A warning may stay, but only with a written reason: right-click it, choose **Exclude**, and add a comment.

<!-- REFPRODUCT:START -->
esp_watch finished with **zero DRC errors**. Some warnings remained; the author judged them acceptable and did not record which. That is the one thing worth doing differently: an accepted warning should be a written decision, so the next person does not have to rediscover whether it matters.
<!-- REFPRODUCT:END -->

<!-- MEDIA
type: screenshot
id: C3-W14
caption: A clean DRC run
brief: KiCad 10 DRC dialog on esp_watch's board: 0 errors, 0 unconnected items, any
  remaining warnings excluded with a comment visible. Crop to the dialog. (Was C2-03.)
-->

**Remember what a clean DRC means.** It says the board **can be made**: every rule you set is met. It does not say the footprints match the parts (C2), that the sensor faces the skin (C0), or that the antenna works (Step 9).

## Step 12: Look at It in 3D

Click **View → 3D Viewer**. Drag to orbit, middle-drag to pan. Check that every part has a model (a missing one shows as bare pads), that the sensor is on the face you meant, and that nothing tall sits where the case will be thinnest. **Preferences → Raytracing** gives a slower, better-looking render; save one for your design pack [1].

<!-- MEDIA
type: screenshot
id: C3-W15
caption: esp_watch in the 3D viewer, top and bottom
brief: KiCad 10 3D Viewer, esp_watch's board, two views: top (XIAO, MPU-6050, OLED on its
  header) and bottom (MAX30102). The repository's pcb_front.png and pcb_back.png may serve
  if they come from the current board.
-->

## Step 13: Export the Board as STEP

Click **File → Export → STEP / GLB / BREP / XAO / PLY / STL**, choose **STEP**, and save [2]. The STEP file holds the board and every 3D model attached to its footprints. Module 5 imports it into Fusion to build the case around it. Gerbers and drill files, for the fab house, are F1's job.

<!-- MEDIA
type: screenshot
id: C3-W16
caption: Exporting the board as a STEP file
brief: KiCad 10 Export 3D Model dialog with STEP selected, the output path and the default
  options visible. Crop to the dialog.
-->

<!-- REFPRODUCT:START -->
esp_watch's exported board is in its repository as [`pcb/esp_Watch/esp_Watch.step`](https://github.com/niat-physicalai/esp_watch/blob/main/pcb/esp_Watch/esp_Watch.step).
<!-- REFPRODUCT:END -->

## Tool Reference

| Tool | Key | Use it to |
|---|---|---|
| Update PCB from Schematic | F8 | Bring schematic changes onto the board |
| Route Tracks | X | Draw copper between pads |
| Via (while routing) | V | Change layer mid-track |
| Add a Filled Zone | — | Pour copper on a net |
| Fill All Zones | B | Refill every pour |
| Add Rule Area | Ctrl+Shift+K | Keep copper out of an area |
| Flip | F | Move a footprint to the other side |
| Design Rules Checker | — | Check the board against its rules |
| 3D Viewer | — | Inspect and render the board |

<!-- PLACEHOLDER:ASSET C3-T — icon crops for this table, same style as assets/kicad/schematic_view/tools/ (see review/ASSETS-TODO.md §6c) -->

---

## Applying What You Have Learned

Lay out your own product's board.

1. **Set the rules.** Two layers; constraints from your fab's capabilities page, with margin; a Power net class for supply and battery nets.
2. **Update from the schematic** (F8).
3. **Draw the outline** from your C0 concept, dimensioned, and **place the mounting holes**.
4. **Place outside in**: fixed parts first, then neighbours, then the rest. Flip any part that belongs on the bottom.
5. **Route** to an unrouted count of 0, power first.
6. **Pour GND on both layers**, stitch the pours if few through-hole GND pins join them, and add a rule area over any on-board antenna. Mark a cable antenna's intended position on User.Drawings.
7. **Label** the board with pin names and its revision.
8. **Run DRC to zero errors**, with a written reason for every excluded warning.
9. **Save a 3D render and export a STEP file.**

**Deliverable:** your KiCad board (`.kicad_pcb`), a screenshot of the clean DRC result, a 3D render, and the board's STEP file, saved in your design pack as `C3-pcb/`.

## Self-Check

Open your board and answer each item Y or N.

1. The board outline matches your C0 concept, and is dimensioned. — Y/N
2. Your constraints are at or above your fab's current published minimums. — Y/N
3. Supply and battery nets use a wider track than signals. — Y/N
4. The status bar shows 0 unrouted connections. — Y/N
5. GND is poured on both layers, and the pours are joined. — Y/N
6. No copper lies under any on-board antenna. — Y/N
7. DRC reports zero errors, and every excluded warning has a comment. — Y/N
8. The board carries its revision on the silkscreen, and a STEP file has been exported. — Y/N

---

## Check Your Understanding

**1.** You add a test point to the schematic, then run DRC on the board. DRC reports the board and schematic disagree. What did you forget?

- A. To refill the zones.
- B. To press F8 and update the board.
- C. To re-run ERC.
- D. To flip the test point to the bottom.

<details>
<summary>Answer</summary>

**B.** The board does not follow the schematic by itself; F8 brings the change across. **A** fixes stale copper pours, not missing parts. **C** checks the schematic, not the board. **D** changes nothing about the mismatch.

</details>

**2.** You move a part after pouring ground, and DRC reports clearance violations between its pads and the GND pour. What is the quickest correct fix?

- A. Delete the zone and route ground as tracks.
- B. Reduce the clearance rule until the errors go.
- C. Refill the zones with B, then re-run DRC.
- D. Exclude the violations.

<details>
<summary>Answer</summary>

**C.** Zones are not refilled automatically; the old fill still covers where the part now sits. **A** throws away the pour's benefits. **B** weakens the rule for the whole board. **D** hides a short circuit the fab would really make.

</details>

**3.** A board passes DRC with zero errors. Which problem could it still have?

- A. A track narrower than the minimum set in the design rules
- B. Two courtyards overlapping
- C. Copper too close to the board edge
- D. A heart-rate sensor on the face away from the skin

<details>
<summary>Answer</summary>

**D.** DRC checks the board against its rules; it cannot know which face should touch the wrist. **A**, **B** and **C** are all things DRC reports.

</details>

**4.** A two-layer board has the 3.3 V rail as a copper pour on the bottom layer and GND on the top. After routing, the bottom pour is in six separate pieces. What is the main problem?

- A. The board costs more to make, because six separate pours need extra processing.
- B. Signals crossing the cuts lose their ground return path below them, and the supply is fragmented.
- C. The fab house will reject six pours.
- D. Nothing; more copper is always better.

<details>
<summary>Answer</summary>

**B.** Every track cuts the plane, so the supply becomes islands and the return paths under the signals are broken. Route the supply as a track and pour GND on both layers instead. **A** and **C** are not true. **D** is the belief this example disproves.

</details>

**5.** Your board uses a module with a printed antenna at one end. What should the layout include?

- A. A ground pour under the antenna, to shield it from the other parts.
- B. A wider track width near the antenna.
- C. Stitching vias around the antenna.
- D. A rule area with no copper under the antenna on both layers.

<details>
<summary>Answer</summary>

**D.** Copper under an antenna changes its behaviour; a rule area keeps the pour out. **A** is the mistake the rule area prevents. **B** has nothing to do with the antenna. **C** puts more grounded copper beside it.

</details>

**6.** Your fab's capabilities page lists a 0.10 mm minimum track. What should your design-rule minimum be?

- A. 0.10 mm, to use the full capability.
- B. 0.08 mm, since fabs have some margin.
- C. Comfortably above it, such as 0.2 mm, unless the board really needs finer tracks.
- D. Whatever KiCad's default happens to be, since KiCad ships with safe values.

<details>
<summary>Answer</summary>

**C.** Staying above the limit means the board never depends on the fab's best day. **A** works but leaves no margin. **B** is below what the fab promises. **D** may be fine or not; it was never checked against the fab.

</details>

**7.** You export your board as STEP for the enclosure, and the OLED module is missing from the file. Why?

- A. The OLED's footprint has no 3D model attached.
- B. STEP files only include the bare board.
- C. The OLED is on the top layer.
- D. The zones were not refilled.

<details>
<summary>Answer</summary>

**A.** The STEP export includes the models attached to footprints (C2, Step 8); a footprint without one adds nothing. **B** is false: the other parts appear. **C** and **D** do not affect the 3D export.

</details>

**8.** You place a button footprint, then realise it belongs on the bottom of the board. Which key moves it there?

- A. F
- B. R
- C. M
- D. X

<details>
<summary>Answer</summary>

**A.** F flips a footprint to the other side; its pads change layer and it appears mirrored. **B** rotates, **C** moves on the same side, and **D** starts routing a track.

</details>

**9.** A route on the top layer is blocked, and the track must cross under another to reach its pad. What do you do?

- A. Route straight through the other track; DRC will flag nothing.
- B. Make the track narrower so it squeezes past the other one.
- C. Press V to drop a via and continue on the bottom layer.
- D. Delete the other track and route it again later, after this one.

<details>
<summary>Answer</summary>

**C.** A via takes the track to the other layer, under the obstacle. **A** would short two nets, which DRC reports. **B** does not help it cross. **D** just moves the problem.

</details>

---

## What Comes Next

The hardware design is complete. Module 4 writes the firmware that runs on it, starting with [D0 — Firmware Architecture](../04-firmware/D0-firmware-architecture.md). Module 5 imports this board's STEP file into Fusion and builds the case around it, and F1 turns the board into the files a fab house needs.

---

## References

1. KiCad. *Getting Started in KiCad, version 10.0* (PCB editor basics, board setup, update from schematic, outline, placement, routing, zones, DRC, 3D viewer). https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html
2. KiCad. *PCB Editor reference manual, version 10.0* (rule areas, 3D model export). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html
3. JLCPCB. *PCB Manufacturing and Assembly Capabilities* (1–2 layer minimum track and spacing 0.10 / 0.10 mm; copper clearance from routed edges ≥ 0.2 mm). https://jlcpcb.com/capabilities/pcb-capabilities
4. niat-physicalai. *esp_watch* (KiCad project and board STEP in `pcb/esp_Watch/`). https://github.com/niat-physicalai/esp_watch
