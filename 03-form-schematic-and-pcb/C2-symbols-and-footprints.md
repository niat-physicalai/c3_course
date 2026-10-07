# C2 — Symbols and Footprints the Library Does Not Have
## Drawing, Sourcing and Checking the Parts KiCad Does Not Know

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Form Factor, Schematic and PCB
**Time:** ~1 hour · **You will produce:** at least one symbol and one footprint you drew yourself, and a footprint verification checklist covering every part on your board

---

### The Part You Need Is Not in the Library

You press **A** in KiCad and type "MAX30102 module". Nothing. "MPU-6050 breakout", "SSD1306 OLED 4-pin": nothing useful. KiCad's libraries are full of chips, but the modules you chose in B4 are small boards made by many sellers, and almost nobody has drawn them properly.

esp_watch hit this on every module. None of its three modules had a usable symbol, and the MAX30102 module had no footprint, so the author drew them. This unit shows how, using KiCad 10's **Symbol Editor** and **Footprint Editor**, and how to check the symbols and footprints you download instead. A wrong symbol is caught by ERC only if you typed its pins honestly. A wrong footprint is caught by nothing until the board arrives.

### What You Will Be Able to Do After This Reading

- **Draw** a module symbol with correct pin numbers, names and electrical types, in a project library.
- **Decide**, for each part, whether to draw, source or verify its footprint.
- **Draw** a footprint in the Footprint Editor, on the right layers, from a drawing or a calibrated photo.
- **Verify** any footprint with four measurements, and record it in a checklist.

---

## Symbols

### What a Symbol Contains

A **schematic symbol** is more than a box with pins. Each pin carries four things:

| Property | What it means | Where it comes from |
|---|---|---|
| **Number** | Which physical pad or header pin this is | The datasheet's pin table, or the module's silkscreen |
| **Name** | What the pin does: `SDA`, `VCC`, `INT` | Same source |
| **Electrical type** | How the pin behaves: input, output, power input and so on | The datasheet's pin description |
| **Position** | Where it sits on the symbol outline | Your choice, for readability |

The **number** must match the footprint's pad number exactly: it is the only link between the schematic and the copper. The **name** is for people. The **type** is for ERC.

### Pin Numbers Come From the Part You Will Solder

For a chip, pin numbers come from the datasheet. For a **module**, they come from the module itself: its header or edge pads, numbered in order from the end marked "1" or with a square pad. Two modules built around the same chip can have entirely different pin orders.

<!-- REFPRODUCT:START -->
That is why esp_watch's symbols were drawn for the *modules*, not the chips. The MAX30102 chip has 14 pads underneath it; the black MAX30102 module has 8 edge pads. A symbol copied from the chip's datasheet would have the wrong number of pins in the wrong order.
<!-- REFPRODUCT:END -->

The same applies to microcontrollers. The bare ESP32-C3 chip has pins for a crystal, external flash and an antenna; the XIAO module has none of these on its edge, because they are inside. Use the module's symbol, not the chip's.

### Electrical Types, and Why ERC Needs Them

ERC cannot see voltages. It only knows each pin's **electrical type**, and checks that connected pins make sense together [1]:

| Type | Use for | Example |
|---|---|---|
| Power input | A pin that receives power | Module `VCC`, `GND` |
| Power output | A pin that supplies power | A regulator's output |
| Input | A signal the part only receives | `AD0` address select |
| Output | A push-pull output, driving high and low | A typical interrupt output |
| Bidirectional | A signal driven either way | I²C `SDA` |
| Open collector | An output that can only pull low | MAX30102 `INT`, which is open-drain [2] |
| Passive | Resistors, connectors, pins with no active electronics | A plain header pin |

Two rules matter most. A **power input** with no power output on its net is an ERC error; C1 showed the PWR_FLAG fix. And **open-collector** outputs may share a net, while ordinary outputs may not.

<!-- REFPRODUCT:START -->
esp_watch's three module symbols type **every pin as input**, including `VCC`, `GND` and `SDA`. The board works, because copper does not care about types. But ERC can no longer tell a supply pin from a signal: it cannot warn that a module's `VCC` is unpowered, or that two outputs share a net. For your own symbols, type each pin by what it does.
<!-- REFPRODUCT:END -->

The opposite shortcut, setting every pin to *passive* "to make the errors go away", does the same damage. The errors go, and so does every check ERC could have made.

### Worked Example: The MPU-6050 Module Symbol

<!-- REFPRODUCT:START -->
esp_watch's MPU-6050 (GY-521 style) module symbol numbers its 8 pins in this order, matching its footprint pad for pad. The *Type* column is what this unit recommends, not what esp_watch's symbol uses.

| Pin | Name | Type | Reason |
|---|---|---|---|
| 1 | INT | Output | Interrupt output; unused on esp_watch (no-connect flag) |
| 2 | AD0 | Input | Address select; tied to GND for 0x68 |
| 3 | XCL | Output | Auxiliary bus clock; unused |
| 4 | XDA | Bidirectional | Auxiliary bus data; unused |
| 5 | SDA | Bidirectional | Data flows both ways |
| 6 | SCL | Input | Clock driven by the microcontroller |
| 7 | GND | Power input | Ground return |
| 8 | VCC | Power input | Receives 3.3 V |
<!-- REFPRODUCT:END -->

**Teaching model:** I²C lets a peripheral hold SCL low to pause the controller, so some libraries type SCL as bidirectional. Either is defensible; write down which you chose.

Many GY-521 modules print their pins the other way round (`VCC` first). Neither order is wrong. What matters is that the symbol, the footprint and the module you will solder all count from the same end. Check yours against its silkscreen.

**Check.** Place the symbol, connect `VCC` to `+3V3`, `GND` to ground, `SDA` and `SCL` to the bus and `AD0` to ground, and put no-connect flags on `INT`, `XCL` and `XDA`. Run ERC. The symbol's pins produce no errors of their own.

### How To: Draw a Symbol in the Symbol Editor

**Step 1: Open the Symbol Editor** from the Project Manager or the schematic's top toolbar.

<!-- MEDIA
type: screenshot
id: C2-W01
caption: KiCad's Symbol Editor, with esp_watch's project library in the tree
brief: KiCad 10 Symbol Editor, full window, esp_watch's project open. The library tree on
  the left shows the project library containing the MAX30102, MPU-6050 and SSD1306 module
  symbols. The MPU-6050 module symbol is open on the canvas.
-->

**Step 2: Create a project library.** Choose **File → New Library**, pick **Project** (not Global), and save it in your project folder. A project library travels with the project, so anyone who opens it, including you on another laptop, gets the same symbols.

**Step 3: Create the symbol.** Right-click the library and choose **New Symbol**. Give it a name that says exactly what it is (`MPU6050_Module_GY521`, not `MPU`), and set the reference designator to `U`.

<!-- MEDIA
type: screenshot
id: C2-W02
caption: The New Symbol dialog
brief: KiCad 10 Symbol Editor, New Symbol dialog, with a name such as
  "MPU6050_Module_GY521" and the default reference designator "U" filled in. Crop to
  the dialog.
-->

**Step 4: Add the pins** (**P**). For each pin, set its number, name and electrical type, then click to place it. Keep the default 2.54 mm (100 mil) grid, so wires in the schematic snap onto the pins.

<!-- MEDIA
type: screenshot
id: C2-W03
caption: The Pin Properties dialog, with the electrical type list open
brief: KiCad 10 Symbol Editor, Pin Properties dialog for one pin of the MPU-6050 module
  symbol (e.g. pin 8, VCC). Name, Number and the Electrical type dropdown open, showing
  the full list of types. Crop to the dialog.
-->

**Step 5: Draw the body** with the rectangle tool, and lay the pins out for reading: power at the top and bottom, signals that go to the microcontroller on the left, the rest on the right.

```text
                  VCC (8)
                    │
              ┌─────┴─────┐
    SCL (6) ──┤           ├── XDA (4)
    SDA (5) ──┤  MPU-6050 ├── XCL (3)
    INT (1) ──┤  module   │
    AD0 (2) ──┤           │
              └─────┬─────┘
                    │
                  GND (7)
```

**Step 6: Fill in the fields.** Value (the part name) and, once its footprint exists, the Footprint field. Linking it now saves a mistake later.

**Step 7: Check every pin against your source, then save.** Tick number, name and type for each pin before you place the symbol anywhere.

<!-- MEDIA
type: screenshot
id: C2-W04
caption: A finished module symbol
brief: KiCad 10 Symbol Editor, the finished MPU-6050 (or MAX30102) module symbol: body
  rectangle, all 8 pins with names and numbers visible, power top and bottom. Crop to
  the canvas.
-->

<!-- REFPRODUCT:START -->
esp_watch keeps its hand-drawn symbols in a project library, [`pcb/esp_Watch/symbol.kicad_sym`](https://github.com/niat-physicalai/esp_watch/blob/main/pcb/esp_Watch/symbol.kicad_sym).
<!-- REFPRODUCT:END -->

### Downloaded Symbols Need Checking Too

<!-- REFPRODUCT:START -->
esp_watch's XIAO symbol and footprint were downloaded from an open-source repository [3]: useful, GPL-3.0, battery pads included. Its last commit message reads *"the symbol didn't have the right reference to the footprint. Not sure if this fixes it or not"*. That is honest, and a warning. The symbol also types the XIAO's `VCC_3V3` pin as a power *input*, which is why C1's ERC needed a PWR_FLAG on `+3V3`.
<!-- REFPRODUCT:END -->

Before using a downloaded symbol, open it in the Symbol Editor and check every pin number against the module's documentation, every type, and the footprint field. Check the licence too, if you will share or sell your design files.

---

## Footprints

### What a Footprint Is

A **footprint** is the set of copper pads, holes and outlines that stands for one part on the board. Each pad has a number, and it must match the symbol's pin number. A footprint also carries non-copper layers:

| Layer | What it holds | Who uses it |
|---|---|---|
| Copper (F.Cu, B.Cu) | Pads | The fab house |
| Silkscreen (F.Silkscreen) | Outline and pin-1 mark printed on the board | The person soldering |
| Fabrication (F.Fab) | The part's true body outline | Assembly drawings |
| Courtyard (F.Courtyard) | The area no other part may enter | DRC |
| User.Drawings | Your own notes and markers | You, and the enclosure designer |

### Draw, Source or Verify

Every footprint on your board falls into one of three cases:

```text
                   Does a footprint already exist?
                         │
             ┌───────────┴───────────┐
            no                       yes
             │                        │
     ┌───────▼───────┐        ┌───────▼────────────────┐
     │  DRAW it from │        │ From KiCad's own        │
     │  a mechanical │        │ library, for a standard │
     │  drawing or a │        │ part (e.g. a pushbutton)│
     │  calibrated   │        └───────┬────────┬───────┘
     │  photo        │               yes       no (downloaded
     └───────┬───────┘                │         from elsewhere)
             │              spot-check│   ┌──────▼──────┐
             │              pin 1 and │   │ VERIFY all  │
             │              pitch     │   │ four        │
             │                        │   │ measurements│
             └──────────┬─────────────┘   └──────┬──────┘
                        ▼                        │
              Record it in the footprint ◄───────┘
              verification checklist
```

**A downloaded footprint is unverified until you have checked it yourself.** DRC checks that pads keep their distance from each other; it has no idea whether they are where the real part's pins are.

<!-- REFPRODUCT:START -->
esp_watch used all three routes:

| Part | Route | Source |
|---|---|---|
| XIAO ESP32-C3 | Sourced | Downloaded from an open-source repository [3] |
| MAX30102 module | Drawn | By the author, from a calibrated photo |
| MPU-6050 and OLED modules | Sourced | Downloaded |
| SW1, SW2, SW3 | Sourced | KiCad's standard library: `SW_PUSH_6mm` and the Würth slide switch |
<!-- REFPRODUCT:END -->

### The Four Measurements

| # | Measurement | What goes wrong if it is off |
|---|---|---|
| 1 | **Pad pitch**: centre to centre, along a row and between rows | Pins miss their pads; the error grows along the row |
| 2 | **Pad and hole size** | Pins do not fit, or pads are too small to solder |
| 3 | **Courtyard and body outline** | Parts overlap, or the enclosure does not fit |
| 4 | **Pin 1 position and numbering** | The part fits but is wired backwards |

The pitch error grows along the row. A footprint drawn at 2.50 mm instead of 2.54 mm has pin 2 0.04 mm out, and pin 8 7 × 0.04 = 0.28 mm out. A 0.64 mm square pin is about 0.9 mm across its corners, so a 1.0 mm hole leaves only about 0.05 mm of slack.

### Worked Example: The MAX30102 Module Footprint

<!-- REFPRODUCT:START -->
The author drew esp_watch's black MAX30102 module footprint from a **calibrated photo**: a photo taken straight down, using the module's own edge pads as the ruler.

**Step 1: Calibrate the photo.** The edge pads are on a standard 2.54 mm grid, so their spacing is a known length. In the photo, the pitch measured **62.2 pixels**.

```text
Scale = 62.2 px ÷ 2.54 mm = 24.5 px/mm
```

**Step 2: Measure the body.** At that scale the body measured **20.2 × 15.6 mm**. The seller's nominal size is 21 × 16 mm; the footprint outlines it as **20 × 15 mm**.

**Step 3: Notice how the module is mounted.** esp_watch's module is not on header pins. It is soldered **flat**, sensor-side out, through the pads along its edges, so the footprint needs **surface-mount (SMD) pads**, not holes.

**Step 4: Place the pads.** Two rows of four at **2.54 mm** pitch. The rows are **18 mm** apart, centre to centre, so each sits under one edge of the module.

**Step 5: Size the pads for hand soldering.** Each pad is a **2 × 3 mm** rectangle that starts at the module's edge and runs 3 mm outward, so the iron can reach copper the module does not cover.

**Step 6: Outline the body** on a drawing layer, so the enclosure designer can see where the module sits. Use `F.Fab` or `User.Drawings`, never **Margin**: graphics on Margin inside esp_watch's footprint stopped KiCad's router reaching the pads.

**Step 7: Mark what the enclosure needs.** The footprint outlines the module, not the 5.6 × 3.3 mm sensor on it. The case window must line up with the sensor, so add that rectangle yourself, measured from the photo.

The result: [`assets/kicad/MAX30102_module.kicad_mod`](../assets/kicad/MAX30102_module.kicad_mod).
<!-- REFPRODUCT:END -->

**Check.** Pad 1 to pad 4 along a row should measure 3 × 2.54 = 7.62 mm; row to row, 18 mm. Measure both in the Footprint Editor before saving.

<!-- MEDIA
type: photo
id: C2-W06
caption: Calibrating a module photo, with the edge-pad pitch as the ruler
brief: Top-down photo of the black MAX30102 module, taken square-on. Overlay: a line across
  two adjacent edge pads labelled "62.2 px = 2.54 mm"; lines across the body labelled
  "20.2 mm" and "15.6 mm"; the 5.6 × 3.3 mm sensor package outlined; "24.5 px/mm" in a
  corner; pin 1 circled. (Was C2-01.)
-->

### How To: Draw a Footprint in the Footprint Editor

**Step 1: Open the Footprint Editor** and create a project footprint library (**File → New Library**, **Project**), as for symbols [4].

<!-- MEDIA
type: screenshot
id: C2-W07
caption: The Footprint Editor with the MAX30102 module footprint open
brief: KiCad 10 Footprint Editor, full window, esp_watch's MAX30102 module footprint
  open: two rows of four SMD pads, the body outline, the silkscreen outline. Layers panel
  visible on the right.
-->

**Step 2: Create the footprint** (right-click the library → **New Footprint**). Name it after the part, as for symbols.

**Step 3: Set the grid** to 2.54 mm, or 1.27 mm, so pads land on the module's pitch.

**Step 4: Place pad 1** with the **Add Pad** tool, then edit it (**E**). Choose **SMD** for a module soldered flat, or **Through-hole** for one on header pins, and set the size and number.

<!-- MEDIA
type: screenshot
id: C2-W08
caption: Pad Properties for one MAX30102 module pad
brief: KiCad 10 Footprint Editor, Pad Properties dialog for pad 1 of the MAX30102 module
  footprint: pad type SMD, shape rectangle, size 2 × 3 mm, layers F.Cu / F.Paste / F.Mask.
  Crop to the dialog.
-->

**Step 5: Place the other pads** on the grid, numbered in the same order as the module and your symbol.

**Step 6: Draw the outlines on the right layers.** Body on `F.Fab`; a silkscreen outline just outside it with a pin-1 mark; a courtyard on `F.Courtyard` about 0.25 mm outside everything. Pick the layer in the Layers panel *before* drawing.

<!-- MEDIA
type: screenshot
id: C2-W09
caption: Choosing the drawing layer: F.Fab and User.Drawings, not Margin
brief: KiCad 10 Footprint Editor, Layers panel crop showing F.Fab, F.Courtyard,
  F.Silkscreen, User.Drawings and Margin, with F.Fab selected as the active layer.
-->

**Step 7: Measure.** Use the measure tool from pad 1 to the last pad of the row, and row to row. Record both in your checklist.

**Step 8: Attach a 3D model.** Open the footprint's properties, **3D Models** tab, and add the part's STEP file. Without it, the part is missing from the board's 3D view and from the STEP you will export to Fusion in Module 5.

<!-- MEDIA
type: screenshot
id: C2-W11
caption: Attaching a STEP model to a footprint
brief: KiCad 10 Footprint Properties, 3D Models tab, for the MAX30102 module footprint:
  the STEP file from esp_watch's "3d models" folder listed, with the offset and rotation
  fields and the 3D preview showing the module sitting on its pads.
-->

<!-- REFPRODUCT:START -->
esp_watch's repository has STEP models for the XIAO, the MAX30102, MPU-6050 and OLED modules, the female header and the Würth switch, in [`pcb/esp_Watch/3d models/`](https://github.com/niat-physicalai/esp_watch/tree/main/pcb/esp_Watch/3d%20models). For your own parts, look on the manufacturer's or seller's page, or on a model-sharing site such as GrabCAD; if there is none, a box of the right size is enough.
<!-- REFPRODUCT:END -->

**Step 9: Save, and assign it** to the symbol: the Footprint field in the symbol, or Assign Footprints (C1, Step 11).

### Verifying a Downloaded Footprint

Five steps before you trust it:

1. **Open it in the Footprint Editor** and look at every layer, not just copper.
2. **Measure the pitch** between the first two pins and across the full row, against the part's drawing or your calibrated photo.
3. **Check pad and hole sizes** against the part's pins.
4. **Check pin 1**: which pad is marked, and does the numbering match your symbol?
5. **Check for stray graphics** on copper, courtyard, edge or Margin layers.

<!-- REFPRODUCT:START -->
Step 5 comes from esp_watch: graphics on the **Margin** layer inside a footprint stopped the router reaching its pads. Moving them to `F.Fab` or `User.Drawings` fixed it. The footprint was electrically correct; a drawing on the wrong layer was enough to block routing.
<!-- REFPRODUCT:END -->

### The Footprint Verification Checklist

One row per footprint on your board. This table is part of your deliverable.

| Part | Route | Source | Pitch ✓ | Pad/hole ✓ | Courtyard ✓ | Pin 1 ✓ | Checked against | Date |
|---|---|---|---|---|---|---|---|---|
| e.g. MAX30102 module | Drawn | Calibrated photo | 2.54 / rows 18 | SMD 2 × 3 | body 20 × 15 | Matches symbol | Photo, 24.5 px/mm | |

---

## Applying What You Have Learned

1. **List every part** on your C1 schematic and decide, for each, whether its symbol and footprint are drawn, sourced or need verifying.
2. **Draw at least one symbol** in a project library. Number the pins from the part you will solder, and type each one by what it does.
3. **Draw at least one footprint** in a project library, from a mechanical drawing or a calibrated photo. Record the four measurements, and attach a 3D model (or a box).
4. **Verify every downloaded symbol and footprint** with the steps above.
5. **Assign every footprint** in your schematic and re-run ERC to zero errors.

**Deliverable:** your project symbol and footprint libraries, and the completed footprint verification checklist, saved in your design pack as `C2-symbols-and-footprints/`.

## Self-Check

Open your libraries and checklist and answer each item Y or N.

1. At least one symbol and one footprint were drawn by you, in project libraries. — Y/N
2. Every drawn symbol's pin numbers were checked against the part you will solder. — Y/N
3. No pin is "unspecified", and no active pin is marked passive to hide an error. — Y/N
4. Every footprint's pad numbers match its symbol's pin numbers. — Y/N
5. Every footprint is in the checklist, with all four measurements ticked. — Y/N
6. Every body outline is on F.Fab or User.Drawings, and nothing is drawn on Margin. — Y/N
7. Every footprint has a 3D model or a stand-in box attached. — Y/N
8. ERC still reports zero errors with every footprint assigned. — Y/N

---

## Check Your Understanding

**1.** A student uses the MAX30102 *chip* symbol from a library for a MAX30102 *module* with 8 edge pads. What goes wrong?

- A. Nothing; the chip is the same.
- B. ERC fails on every pin, because chip symbols cannot be used for modules.
- C. The pin numbers match the chip, not the module's pads.
- D. The I²C address changes.

<details>
<summary>Answer</summary>

**C.** Pin numbers must match the part you solder, and the module's 8 pads are not the chip's 14. **A** ignores that the module is a different physical part. **B** is unlikely: ERC checks types and connections, not which physical part you chose. **D** is a property of the chip, unaffected by the symbol.

</details>

**2.** A light sensor's interrupt pin is open-drain, active-low, and shares its net with a pull-up resistor. Which electrical type is correct?

- A. Output
- B. Power output
- C. Passive
- D. Open collector

<details>
<summary>Answer</summary>

**D.** Open collector describes a pin that can only pull low, and lets it share a net with a pull-up. **A** describes a push-pull output that also drives high, which this pin cannot. **B** is for supply pins. **C** hides the pin's behaviour from ERC.

</details>

**3.** A classmate sets every pin on their new symbol to *passive*, and ERC goes quiet. What have they lost?

- A. Nothing; ERC checks passive pins exactly as it checks every other type.
- B. ERC's ability to catch an unpowered part or two outputs on one net.
- C. The ability to assign a footprint.
- D. The pin numbers.

<details>
<summary>Answer</summary>

**B.** ERC's checks depend on pin types; passive tells it nothing. **A** is false for the same reason. **C** and **D** are unaffected by pin types.

</details>

**4.** A downloaded footprint for a 10-pin header uses a 2.50 mm pitch. If pin 1 is lined up, how far out is pin 10?

- A. 0.04 mm
- B. 0.40 mm
- C. 0.36 mm
- D. 2.54 mm

<details>
<summary>Answer</summary>

**C.** Pin 10 is nine pitches from pin 1: 9 × 0.04 = 0.36 mm. **A** is the error at pin 2 only. **B** counts ten pins instead of nine gaps. **D** confuses the pitch with the error.

</details>

**5.** A module photo shows edge pads 50.8 pixels apart, and the body is 406 pixels wide. How wide is the body?

- A. 20.3 mm
- B. 8.0 mm
- C. 16.0 mm
- D. 203 mm

<details>
<summary>Answer</summary>

**A.** The scale is 50.8 ÷ 2.54 = 20 px/mm, so 406 ÷ 20 = 20.3 mm. **B** divides by the pixel pitch, counting pitches, not millimetres. **C** uses 25.4 px/mm, mixing up the pitch with an inch. **D** is a factor-of-ten slip.

</details>

**6.** A calibrated photo of a 2 × 3 header module gives a row spacing of 7.51 mm, at 20 px/mm. What should the footprint use?

- A. 7.51 mm, because it was measured.
- B. 7.80 mm, to leave some clearance.
- C. 7.50 mm, rounded to the nearest 0.5 mm.
- D. 7.62 mm (3 × 2.54).

<details>
<summary>Answer</summary>

**D.** Header pins sit on the 2.54 mm grid by construction, and 0.11 mm is about 2 pixels of measuring error. **A** trusts the less reliable source. **B** and **C** match neither the grid nor the measurement.

</details>

**7.** In the PCB editor, the router will not reach the pads of one footprint, though DRC shows no clearance problem in the footprint itself. What should you check first?

- A. The track width set in the board's default net class.
- B. Graphics on the Margin layer inside the footprint.
- C. The board thickness.
- D. The silkscreen font size.

<details>
<summary>Answer</summary>

**B.** Graphics on Margin inside a footprint can block the router, exactly as on esp_watch; move them to F.Fab or User.Drawings. **A** would affect every footprint, not one. **C** and **D** do not affect routing.

</details>

**8.** Your symbol numbers a module's pins 1 to 8 starting from `VCC`; your footprint numbers its pads 1 to 8 starting from `INT`, at the other end. Both look correct on their own. What happens on the board?

- A. Every pin connects to the wrong pad, mirrored end to end.
- B. ERC reports the mismatch.
- C. KiCad renumbers the pads to match.
- D. Only pin 1 is wrong; the other seven pads still line up with their pins.

<details>
<summary>Answer</summary>

**A.** Pads join nets by number, so counting from opposite ends reverses every connection. **B** and **C** do not happen: neither tool knows which end is the real pin 1. **D** underestimates it: all eight move.

</details>

---

## What Comes Next

Every part now has a symbol, a checked footprint and a 3D model. In [C3 — KiCad Walkthrough: PCB Layout](C3-kicad-pcb-walkthrough.md) you lay out the board itself.

---

## References

1. KiCad. *Schematic Editor reference manual, version 10.0* (pin electrical types, PWR_FLAG, Symbol Editor, symbol library tables). https://docs.kicad.org/10.0/en/eeschema/eeschema.html
2. Analog Devices. *MAX30102 datasheet* (interrupt pin: active-low, open-drain). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
3. VectorSpaceHQ. *XIAO_ESP32C3: KiCad footprint and symbol for XIAO ESP32C3* (KiCad v7 files; battery pads; GPL-3.0; commit history). https://github.com/VectorSpaceHQ/XIAO_ESP32C3
4. KiCad. *PCB Editor reference manual, version 10.0* (Footprint Editor, pad properties, layers, 3D models). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html
