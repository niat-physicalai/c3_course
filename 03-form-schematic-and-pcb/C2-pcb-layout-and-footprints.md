# B5 — PCB Layout, and the Footprint Problem
## From a Correct Schematic to a Board That Fits, Routes and Can Be Made

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 2 — Hardware and Electronics Design
**Time:** ~1.5 hours · **You will produce:** a routed PCB that passes DRC, a 3D render, and a footprint verification checklist

---

### A Board Can Pass Every Check and Still Not Fit

Your schematic passes ERC. You import it into the PCB editor, place the parts, route the tracks, and the Design Rules Check reports zero errors. The board is ordered. Two weeks later it arrives, and the sensor module's header pins do not line up with the holes. Every pin is off by a fraction of a millimetre, and the error grows along the row until the last pin misses completely.

Nothing in KiCad warned you, because nothing in KiCad knew. DRC checks that tracks and pads keep their distance. It has no idea whether the holes are where the real part's pins are. That depends on the **footprint**, the pattern of pads that stands for the part on the board, and a footprint is only as correct as the measurements it was drawn from.

This unit covers both halves of turning a schematic into a board. First the footprints: whether to draw, download or verify each one, and how to check it with four measurements. Then the layout itself: placing parts from the outside in, pouring ground, routing power, keeping the antenna clear, and reaching a clean DRC.

### What You Will Be Able to Do After This Reading

- **Decide**, per part, whether to draw, source or verify a footprint.
- **Verify** a footprint with four measurements against a mechanical drawing or a calibrated photo.
- **Draw** a footprint for a through-hole module, by hand or with a script.
- **Place and route** a two-layer board, starting from connectors and mechanical constraints.
- **Keep** an external antenna clear of copper and the battery, and **reach** zero DRC errors.

### What Part 1 Already Covered

Part 1 had you build circuits on breadboards and solder modules to headers, so you know what a module's pins look like. **What is new here** is designing the board those pins go into: footprints that match real parts, and a layout that works electrically, fits mechanically and can be made by a fab house.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Footprints: Draw, Source or Verify

## What a Footprint Is

A **footprint** is the set of copper pads, holes and outlines that represents one part on the board. Each pad has a number, and the number must match the pin number in the part's schematic symbol, which is how KiCad knows which pad joins which net.

A footprint also carries several non-copper layers:

| Layer | What it holds | Who uses it |
|---|---|---|
| Copper (F.Cu, B.Cu) | Pads | The fab house |
| Silkscreen (F.SilkS) | The outline and pin-1 mark printed on the board | The person soldering |
| Fabrication (F.Fab) | The part's true body outline | Assembly drawings |
| Courtyard (F.CrtYd) | The area no other part may enter | DRC |
| User.Drawings | Your own notes and markers | You, and the enclosure designer |

## The Decision

Every footprint in your design falls into one of three cases:

```text
                   Does a footprint already exist?
                         │
             ┌───────────┴───────────┐
            no                       yes
             │                        │
     ┌───────▼───────┐        ┌───────▼────────────────┐
     │  DRAW it from │        │ From KiCad's own        │
     │  a mechanical │        │ library, for a standard │
     │  drawing or a │        │ part (e.g. a pin header)│
     │  calibrated   │        └───────┬────────┬───────┘
     │  photo        │               yes       no (downloaded
     └───────┬───────┘                │         from elsewhere)
             │                        │          │
             │              spot-check│   ┌──────▼──────┐
             │              pin 1 and │   │ VERIFY all  │
             │              pitch     │   │ four        │
             │                        │   │ measurements│
             └──────────┬─────────────┘   └──────┬──────┘
                        ▼                        │
              Record it in the footprint ◄───────┘
              verification checklist
```

The rule behind the diagram: **a downloaded footprint is unverified until you have checked it yourself.** A wrong footprint is found when the board arrives, not by DRC.

<!-- REFPRODUCT:START -->
esp_watch used all three routes:

| Part | Route | Source |
|---|---|---|
| XIAO ESP32-C3 | Sourced | Downloaded from an open-source repository [1] |
| MAX30102 module | Drawn | Generated by the author from measurements of the module |
| Module headers | Sourced | KiCad's standard library: `PinSocket_1x08_P2.54mm_Vertical` |
<!-- REFPRODUCT:END -->

## The Four Measurements

Check every footprint against the real part with these four measurements. They catch almost every footprint error that matters.

| # | Measurement | What goes wrong if it is off |
|---|---|---|
| 1 | **Pad pitch**: centre-to-centre distance between pins, and between rows | Pins do not reach their holes; the error grows along the row |
| 2 | **Pad and hole size** | Pins do not fit the holes, or pads are too small to solder |
| 3 | **Courtyard and body outline** | Parts overlap on the board, or the enclosure does not fit |
| 4 | **Pin 1 position and numbering** | The part fits but is wired backwards |

Why does the pitch error grow? Suppose a downloaded footprint uses 2.50 mm instead of 2.54 mm. The first pin is right, the second is 0.04 mm off, and the eighth is 7 × 0.04 = 0.28 mm off. A 1.0 mm hole with a 0.64 mm square pin has some slack, but not that much, and the error in the *other direction* at the far end of the row doubles the misfit.

## Worked Example: Drawing the MAX30102 Module Footprint

<!-- REFPRODUCT:START -->
No trustworthy footprint existed for esp_watch's black MAX30102 module, and no mechanical drawing came with it. The author measured the module from a **calibrated photo**: a photograph taken straight down, with the module's own header pins as the ruler.

**Step 1: Calibrate the photo.** Header pins are on a standard 2.54 mm grid, so their spacing is a known length. In the photo, the pitch measured **62.2 pixels**.

```text
Scale = 62.2 px ÷ 2.54 mm = 24.5 px/mm
```

**Step 2: Measure the body.** Using that scale, the module body measured **20.2 × 15.6 mm**. The seller's nominal size is **21 × 16 mm**.

**Step 3: Choose which body size to use.** The footprint uses the **nominal 21 × 16 mm**. It is slightly larger than the measurement, so the courtyard and enclosure clearances err on the safe side, and it covers the variation between batches of a marketplace module.

**Step 4: Measure the pads.** Two rows of four pins at 2.54 mm pitch. The spacing between the rows measured **10.3 mm**.

**Step 5: Snap to the grid.** Header pins sit on a 2.54 mm grid, and 4 × 2.54 = **10.16 mm**. The measured 10.3 mm is 0.14 mm away, which is within the photo's measuring error (about 3 pixels). The footprint uses **10.16 mm**, because a real header is built on the grid and a photo is not perfectly accurate.

**Step 6: Choose drill and pad sizes.** Holes of **1.0 mm** and round pads of **1.7 mm**, with pin 1 square.

**Step 7: Mark what the enclosure needs.** The sensor package itself, **5.6 × 3.3 mm**, is drawn on the `User.Drawings` layer, so that the enclosure designer can line up the window in the case base with the sensor, which faces the wrist.

The result is `MAX30102_Module_21x16mm_2x4_P2.54mm.kicad_mod`, produced by the author's own generator script so the dimensions can be edited and regenerated.
<!-- REFPRODUCT:END -->

**Check.** Compare the footprint with the measurements: pitch 2.54 mm on the grid; row spacing 10.16 mm against 10.3 mm measured, explained; body at nominal size, larger than measured; pin 1 marked square. Every number has a stated source, which is the point of the exercise.

<!-- ASSET:PLACEHOLDER reference-files/kicad/MAX30102_Module_21x16mm_2x4_P2.54mm.kicad_mod -->
<!-- ASSET:PLACEHOLDER reference-files/kicad/make_max30102_footprint.py -->

<!-- MEDIA
type: photo
id: B5-01
caption: Calibrating a module photo: the header pitch used as the ruler
brief: A top-down photo of the black MAX30102 module (one of the author's uploaded module
  photos), taken square-on. Overlay in a contrasting colour: a measurement line across
  two adjacent header pins labelled "62.2 px = 2.54 mm"; a line across the body width
  and height labelled "20.2 mm" and "15.6 mm"; a line between the two header rows
  labelled "10.3 mm measured → 10.16 mm used". A small scale note "24.5 px/mm" in a
  corner. Pin 1 circled.
-->

<!-- MEDIA
type: screenshot
id: B5-02
caption: The MAX30102 module footprint in KiCad's Footprint Editor
brief: KiCad Footprint Editor, full window, with MAX30102_Module_21x16mm_2x4_P2.54mm open.
  Two rows of four through-hole pads, pad 1 square and the rest round. Body outline on
  F.Fab and F.SilkS, courtyard on F.CrtYd, and the 5.6 × 3.3 mm sensor rectangle on
  User.Drawings, visible in its own colour. The Pad Properties dialog open for pad 1,
  showing size 1.7 mm, hole 1.0 mm, shape rectangle. The measurement tool drawn between
  pad 1 and pad 2 showing 2.54 mm.
-->

## Drawing Your Own: Two Ways

You can draw a module footprint by hand in KiCad's **Footprint Editor**, or generate it with a script. For simple, regular parts like header modules, a script has a big advantage: when a measurement changes, you edit one number and regenerate, instead of redrawing.

**By hand, in eight steps:**

1. Create a footprint library for your project and a new footprint in it.
2. Set the grid to 2.54 mm (or 1.27 mm) for header pins.
3. Place pad 1 as a rectangular through-hole pad with your chosen drill and pad size.
4. Place the remaining pads on the grid, numbered in the same order as the module's pins and your symbol.
5. Draw the body outline on `F.Fab` at the size you decided.
6. Draw the silkscreen outline just outside the body, and mark pin 1.
7. Draw the courtyard on `F.CrtYd`, about 0.25 mm outside the body.
8. Measure pad 1 to pad 2, and row to row, with the measuring tool. Record the results in your checklist.

**With a script:** the course provides [`B5-header-module-footprint.py`](../assets/code/B5-header-module-footprint.py), a short Python program that writes a KiCad footprint file for any module with rows of through-hole pins. Edit the parameters at the top, run it, and add the resulting `MyModules.pretty` folder to KiCad as a footprint library. Its output opens in KiCad 10. These are the parameters, set here to the MAX30102 module's figures:

```python
NAME = "Module_21x16mm_2x4_P2.54mm"   # footprint name
BODY_W, BODY_H = 21.0, 16.0           # module body width and height
ROWS, COLS = 2, 4                     # header rows and pins per row
PITCH = 2.54                          # distance between pins in a row
ROW_SPACING = 10.16                   # distance between the two rows
DRILL, PAD = 1.0, 1.7                 # hole diameter, pad diameter
PADS_OFFSET_X, PADS_OFFSET_Y = 0.0, 0.0   # shift of pad array from body centre
COURTYARD_MARGIN = 0.25               # courtyard clearance around the body
MARKER = (5.6, 3.3, 0.0, 0.0)         # (w, h, x, y) on User.Drawings, or None
```

Two parameters need your own measurements. The script centres the pads and the marker on the body by default. On a real module they are rarely centred, so measure the offsets from your photo or drawing. The script also numbers pads along the first row and then along the second. Check this against your module's pin order and your symbol, because modules differ.

<!-- FACT:VERIFY esp_watch — the pad-array and sensor offsets from the module body centre are not recorded in REFERENCE-PRODUCT.md; the script's centred defaults are not esp_watch's real values -->

## Verifying a Downloaded Footprint

**Five steps before you trust it:**

1. **Open it in the Footprint Editor**, not just the PCB, and look at every layer.
2. **Measure the pitch** between the first two pins and across the full row, against the part's drawing or your own calibrated photo.
3. **Check pad and hole sizes** against the part's pin size.
4. **Check pin 1**: which pad is square, and does the numbering match your symbol?
5. **Check for stray graphics** on copper, courtyard and edge layers that could interfere with routing or manufacture.

<!-- REFPRODUCT:START -->
Step 5 comes from esp_watch. Its layout hit a footprint with graphics on the **Margin** layer inside the footprint, and the router refused to reach the pads. Moving those graphics to `F.Fab` or `User.Drawings` fixed it. The footprint looked fine and was electrically correct. A drawing on the wrong layer was enough to block routing.

The XIAO footprint came from an open-source repository whose own history says the symbol's link to the footprint may not have been right [1]. Treat any downloaded symbol and footprint pair as a claim to be checked, however useful it is.
<!-- REFPRODUCT:END -->

## The Footprint Verification Checklist

Keep one row per footprint in your design. This table is part of your deliverable.

| Part | Route | Source | Pitch ✓ | Pad/hole ✓ | Courtyard ✓ | Pin 1 ✓ | Checked against | Date |
|---|---|---|---|---|---|---|---|---|
| e.g. MAX30102 module | Drawn | Calibrated photo | 2.54 / 10.16 | 1.0 / 1.7 | 21 × 16 + 0.25 | Square, matches symbol | Photo, 24.5 px/mm | |

> **Try it: Spot the wrong pitch.** A downloaded footprint for a 1 × 8 header module has pads at x = 0, 2.50, 5.00, 7.50, 10.00, 12.50, 15.00 and 17.50 mm.
> 1. **Predict.** Will a real 2.54 mm header fit?
> 2. **Do.** Work out where each pin of a real header sits, and the error at each pad.
> 3. **Explain.** At which pin does the error first exceed 0.15 mm? If you centred the footprint on the header instead of lining up pin 1, how big would the worst error be?

---

# Part 2 — Layout

## Stackup and Design Rules

<!-- REFPRODUCT:START -->
esp_watch is a **two-layer** board, 38 × 38 mm. It uses two classes of design rule:

| Class | Track | Clearance | Via (pad / hole) |
|---|---|---|---|
| Default (signals) | 0.25 mm | 0.2 mm | 0.6 / 0.3 mm |
| Power (3V3, GND, BAT+, BAT−) | 0.5 mm | 0.2 mm | 0.8 / 0.4 mm |

Its minimum constraints were set to 0.127 mm track and clearance, 0.5 mm via, 0.3 mm drill, 0.13 mm annular ring and 0.3 mm copper-to-edge.
<!-- REFPRODUCT:END -->

Compare those minimums with JLCPCB's currently published two-layer capabilities: 0.10 mm minimum track and spacing, and 0.2 mm copper clearance from a routed board edge [2]. esp_watch's settings are more conservative than the fab's limits, which is a good habit. Fab capabilities change, and designing right at the limit leaves no room for the fab's own variation. Set your constraints from your fab's current published capabilities, then design comfortably above them.

The design rules themselves are wider still. Signal tracks of 0.25 mm are easy to make and easy to repair, and power tracks of 0.5 mm carry the few hundred milliamps a watch needs with plenty of margin.

## Placement: Outside In

Place parts in this order, because each step constrains the next:

1. **Board outline and mounting holes.** These come from the enclosure, so they are fixed first. In Module 4 you will export the board to CAD, and any changes to the outline come back here.
2. **Parts that must be at a particular place**: connectors at the edge where the case opening is, buttons and switches where a finger reaches them, sensors where they must face.
3. **Parts that must be near another part**: decoupling capacitors next to their chip, pull-ups near the bus.
4. **Everything else.**

<!-- REFPRODUCT:START -->
On esp_watch, most of the board was decided by step 2:

- The **XIAO's USB-C port** faces the left side of the watch, where the case has its charging opening.
- The **display, motion sensor, XIAO, both buttons and the slide switch** are on the top face, where the wearer can see and reach them.
- The **MAX30102 module** is on the **bottom** face, so its sensor touches the wrist.
- **Four mounting holes**, two at the top corners and two in the middle, hold the motion-sensor and display modules on standoffs.
- The **battery** stands vertically in a slot behind the display's header.

With modules, the decoupling in step 3 is mostly done already, because each module carries its own capacitors, so the carrier board's layout is dominated by mechanical placement.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/render-top.png -->
![esp_watch PCB render, top face](../reference-files/images/render-top.png)

<!-- ASSET:PLACEHOLDER reference-files/images/render-bottom.png -->
![esp_watch PCB render, bottom face, with the MAX30102 module](../reference-files/images/render-bottom.png)

## Ground and Power on Two Layers

On a two-layer board, the most effective single step is a **ground pour**: filling the empty space on both layers with copper connected to ground, then **stitching** the two layers together with vias. Every signal needs a path back to its source, and a solid ground under it gives the return current the shortest possible path.

<!-- REFPRODUCT:START -->
esp_watch pours ground on both layers and stitches them with vias every 5 to 10 mm. Its 3.3 V rail is routed as a **track**, not as a second copper plane. On a four-layer board, a whole layer can be given to power. On two layers, a power plane would be cut into pieces by every signal crossing it, and those cuts would also break up the ground return paths beneath the signals. A 0.5 mm track carries the current just as well, and leaves the ground pour intact.
<!-- REFPRODUCT:END -->

A common belief is that "more copper is always better", so students pour power on one side and ground on the other. On a two-layer board that usually makes things worse, for exactly the reason above.

## The Antenna Keep-Out

An antenna radiates into the space around it. Copper nearby, especially a ground pour directly underneath, changes its behaviour and can stop it working well.

<!-- REFPRODUCT:START -->
The XIAO ESP32-C3 uses an **external antenna** on a U.FL cable. esp_watch's layout rules for it:

- **No copper under the antenna** on either layer: draw a keep-out zone and let the ground pour flow around it.
- **Keep it away from the battery**, because a metal-foil LiPo pouch near the antenna affects it just as copper does.
- **Route it along the inside of the case**, away from the board.
<!-- REFPRODUCT:END -->

Because the antenna is on a cable, its final position is decided with the enclosure. Mark its intended position on `User.Drawings` now, add the keep-out, and check it again once the case exists.

## DRC, and What It Does Not Mean

The **Design Rules Check** checks the board against your rules: track widths, clearances, drill sizes, unconnected pads, courtyard overlaps and copper too close to the edge [3]. Run it often, not just at the end.

<!-- REFPRODUCT:START -->
esp_watch finished with **zero DRC errors**. Some warnings remained; the author judged them acceptable for a hobbyist board and did not fix them. Which warnings they were is not recorded, and that is the one thing worth changing. An accepted warning should be a written decision, with a reason, so that the next person does not have to rediscover whether it matters.
<!-- REFPRODUCT:END -->

Remember what a clean DRC means. It says the board **can be made**: every rule you set is met. It does not say the footprints match the parts, that the sensor faces the skin, or that the antenna works. That is why this unit has a footprint checklist as well as a DRC report.

<!-- MEDIA
type: screenshot
id: B5-03
caption: KiCad's DRC dialog after a clean run
brief: KiCad 10 PCB Editor with the Design Rules Checker dialog open after a run on a
  small two-layer module-carrier board. Summary shows "0 Errors" and a small number of
  warnings, with one warning selected and marked as excluded, and its exclusion comment
  visible (for example "Silkscreen clipped by pad on module header, acceptable").
  The board behind the dialog shows both ground pours. Light theme.
-->

> **Try it: Find the plane problem.** Open any two-layer example board in KiCad, or your own.
> 1. **Predict.** If you replace the 3.3 V track with a copper pour on the bottom layer, what will happen to the bottom-layer ground pour?
> 2. **Do.** Add the 3.3 V pour, refill all zones, and look at the bottom layer. Then undo it.
> 3. **Explain.** How many separate islands did the 3.3 V pour form? What happened to the ground under the signal tracks?

---

# Putting It All Together

## Applying What You Have Learned

**1. Classify every footprint.** For each part, decide draw, source or verify, and record the source.

**2. Draw at least one footprint.** Use the Footprint Editor or the provided script, working from a mechanical drawing or a calibrated photo. Record the four measurements.

**3. Verify every downloaded footprint** with the five steps, and fill the checklist.

**4. Lay out the board.** Outline and mounting holes first, then fixed-position parts, then the rest. Pour ground on both layers and stitch it. Route power as tracks at the power class width. Add the antenna keep-out.

**5. Run DRC to zero errors.** Write a reason next to every accepted warning. Open the 3D viewer and export a render.

**Deliverable:** your routed KiCad board with zero DRC errors, a 3D render, and the completed footprint verification checklist, saved in your design pack.

## Self-Check

Open your KiCad board and checklist and answer each item Y or N.

1. DRC reports zero errors. — Y/N
2. Every accepted DRC warning has a written reason. — Y/N
3. Every footprint appears in the checklist with its route and source. — Y/N
4. Every footprint has all four measurements recorded and ticked. — Y/N
5. At least one footprint was drawn by you. — Y/N
6. Every footprint's pad numbering matches its schematic symbol. — Y/N
7. Your design-rule minimums are at or above your fab's current published capabilities. — Y/N
8. Ground is poured on both layers and stitched with vias. — Y/N
9. Any antenna area has a copper keep-out on both layers. — Y/N
10. A 3D render of the finished board is saved. — Y/N

---

## Check Your Understanding

**1.** A downloaded footprint for a 10-pin header uses a 2.50 mm pitch. If pin 1 is lined up, how far out is pin 10?

- A. 0.04 mm
- B. 0.36 mm
- C. 0.40 mm
- D. 2.54 mm

<details>
<summary>Answer</summary>

**B.** Pin 10 is nine pitches from pin 1, so the error is 9 × 0.04 = 0.36 mm. **A** is the error at pin 2 only. **C** multiplies by ten pins instead of nine gaps. **D** confuses the pitch with the error.

</details>

**2.** A module photo shows header pins 50.8 pixels apart, and the module body is 406 pixels wide. How wide is the body?

- A. 8.0 mm
- B. 20.3 mm
- C. 16.0 mm
- D. 203 mm

<details>
<summary>Answer</summary>

**B.** The scale is 50.8 ÷ 2.54 = 20 px/mm, so 406 ÷ 20 = 20.3 mm. **A** divides by the pixel pitch (406 ÷ 50.8 ≈ 8), which counts pitches, not millimetres. **C** divides by 25.4, treating the scale as 25.4 px/mm, a mix-up between the pitch and the millimetres in an inch. **D** divides by 2 instead of 20, a factor-of-ten slip.

</details>

**3.** A board passes DRC with zero errors. Which problem could it still have?

- A. A track narrower than the design rule
- B. Two courtyards overlapping
- C. A footprint whose pin 1 is on the wrong corner compared with the real module
- D. Copper too close to the board edge

<details>
<summary>Answer</summary>

**C.** DRC compares the board with its own rules and netlist. It cannot know where the real module's pin 1 is. **A**, **B** and **D** are all exactly what DRC checks.

</details>

**4.** Why did esp_watch route 3.3 V as a track rather than as a copper plane?

- A. Tracks carry more current than planes.
- B. On two layers, a power plane would be cut into pieces by signal routing, breaking up the ground return paths too, while a 0.5 mm track carries the current easily.
- C. JLCPCB does not allow planes.
- D. Planes are only for ground.

<details>
<summary>Answer</summary>

**B.** With only two layers, every signal crossing a plane cuts it, and the ground pour loses its continuity as well. **A** is backwards: a plane can carry more, but a watch does not need more. **C** is false. **D** is false; power planes are common on boards with more layers.

</details>

**5.** A calibrated photo gives a header row spacing of 10.3 mm. The pins are on a 2.54 mm grid. What should the footprint use, and why?

- A. 10.3 mm, because it was measured.
- B. 10.16 mm (4 × 2.54), because headers are built on the grid and 0.14 mm is within the photo's measuring error.
- C. 10.5 mm, to leave clearance.
- D. 10.0 mm, to round down.

<details>
<summary>Answer</summary>

**B.** A header's pins are on the 2.54 mm grid by construction, and a small difference in a photo measurement is more likely error than reality. **A** trusts the less reliable source. **C** and **D** invent numbers that match neither the grid nor the measurement.

</details>

**6.** An external antenna on a cable ends up lying directly over the ground pour, next to the LiPo pouch. What is the best fix?

- A. Remove the ground pour from the whole board.
- B. Add a copper keep-out under the antenna's position on both layers, and route the antenna along the case wall away from the battery.
- C. Nothing; external antennas are not affected by nearby copper.
- D. Move the battery onto the other side of the board.

<details>
<summary>Answer</summary>

**B.** It follows both esp_watch rules: no copper under the antenna, and distance from the battery. **A** throws away the ground pour's benefits for the whole board to fix a local problem. **C** is false; nearby copper and a foil pouch both affect an antenna. **D** may help with the battery, but it leaves the copper under the antenna.

</details>

---

## What You Can Now Do, and What Comes Next

- Decide whether to draw, source or verify each footprint, and verify with four measurements.
- Draw a module footprint from a calibrated photo, by hand or with a script.
- Lay out a two-layer board from the outside in, with a solid ground and power on tracks.
- Keep an antenna clear, and reach a clean DRC while recording what it cannot tell you.

The idea to carry forward: **DRC checks the board against your rules, and the checklist checks your rules against reality.** You need both.

This completes the hardware design. Module 3 turns to the firmware that runs on it, starting with [C0 — Firmware Architecture](../03-firmware/C0-firmware-architecture.md), and Module 4 brings this board into the enclosure, where its outline, holes and height will be tested against a real case.

---

## References

1. VectorSpaceHQ. *XIAO_ESP32C3: KiCad footprint and symbol for XIAO ESP32C3* (commit history includes "the symbol didn't have the right reference to the footprint. Not sure if this fixes it or not"). https://github.com/VectorSpaceHQ/XIAO_ESP32C3
2. JLCPCB. *PCB Manufacturing and Assembly Capabilities* (1–2 layer minimum track and spacing 0.10 / 0.10 mm; copper clearance from routed edges ≥ 0.2 mm). https://jlcpcb.com/capabilities/pcb-capabilities
3. KiCad. *PCB Editor documentation, version 10.0* (Design Rules Checker, courtyards, zones). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
