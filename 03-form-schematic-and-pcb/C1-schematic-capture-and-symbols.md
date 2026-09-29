# C1 — Schematic Capture, and Drawing Your Own Symbols
## Turning the Pin Map into a Schematic That Checks Itself

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Form Factor, Schematic and PCB
**Time:** ~1.5 hours · **You will produce:** a KiCad schematic that passes ERC with zero errors, including at least one symbol you drew yourself

---

### The Part You Need Is Not in the Library

You open KiCad, press the key to add a symbol, and type "MAX30102 module". Nothing. You try "MPU-6050 breakout" and "SSD1306 OLED 4-pin". Nothing useful. KiCad's libraries are full of chips, but the modules you actually chose in B4 are small boards made by many different sellers, and almost nobody has drawn them properly.

This happened on the reference watch. None of its three peripheral modules had a usable symbol, so all three were drawn by hand. The microcontroller's symbol was downloaded, and even that came with a warning in its own history.

So this unit covers two skills. The first is **schematic capture**: drawing the circuit in KiCad so that its connections, names and notes are clear, and so that KiCad's **Electrical Rules Check** (ERC) can catch mistakes. The second is the one most courses skip: **drawing a schematic symbol from a datasheet or a module**, correctly enough that ERC can trust it and reusable enough that you never draw it twice.

### What You Will Be Able to Do After This Reading

- **Draw** a schematic in KiCad from your B2 interface table and B3 pin map, using clear net names.
- **Create** a schematic symbol from a pin table, with correct pin numbers, names and electrical types.
- **Explain** how pin electrical types drive ERC, and **resolve** the common ERC errors.
- **Add** test points and fabrication notes where the build will need them.
- **Organise** your symbols in a project library so they can be reused.

### What Part 1 Already Covered

Part 1 taught you to read simple schematics and wire circuits from them. **What is new here** is drawing a schematic yourself in KiCad, making symbols for parts that have none, and using ERC to check the drawing, so that the schematic becomes a document a manufacturer, and a reviewer, can rely on.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Schematic Capture

## Transcribe, Do Not Invent

By now every connection has been decided. B2 listed them, B3 assigned the pins, and B4 chose the parts. The schematic is where you **transcribe** those decisions into KiCad, not where you make new ones.

That changes how you work. Keep the B3 pin map open beside KiCad. Draw one connection at a time and tick it off in the interface table. If you find yourself deciding something new, such as moving a signal to a different pin, stop. Update B3 first, with a reason, then draw it. A schematic that silently disagrees with the pin map is how a board ends up with an interrupt on a boot pin.

## Net Names

A **net** is a set of pins that are electrically connected. KiCad names every net automatically, with names like `Net-(U2-Pad3)`. Replace those with meaningful names by adding **labels**, taking the names from your B2 interface table.

<!-- REFPRODUCT:START -->
For esp_watch, the interface table's signal column gives the names directly: `SDA`, `SCL`, `MAX_INT`, `IMU_INT`, `BTN_NEXT`, `BTN_PREV`, `VBAT_SENSE`, plus the power nets `+3V3`, `VBAT` and `GND`.
<!-- REFPRODUCT:END -->

Good names pay off three times: in the schematic, where a reader sees `IMU_INT` rather than a wire to trace; in the PCB editor, where the same names appear on every pad; and in the firmware, where the same names become constants. Use the same spelling in all three.

KiCad offers three kinds of label [1]:

| Label | Connects | Use it for |
|---|---|---|
| Local label | Nets with the same name on the **same sheet** | Most signals in a small design |
| Global label | Nets with the same name on **any sheet** | Signals used across many sheets |

Power nets use **power symbols** (such as `+3V3` and `GND`) instead of labels. They connect everywhere in the project automatically.

**One sheet is enough.** Large designs split the schematic into linked sheets (a *hierarchical schematic*); a small carrier board like a watch's is clearer on one page.

## Test Points and Fabrication Notes

Two additions turn a schematic from a drawing into a build document.

**Test points** are small pads, each with its own symbol, where someone can touch a probe during bring-up. Nobody will probe your board in this course, but the funded build will, and adding test points now costs almost nothing. Put them on every power rail, on ground, and on every bus line.

**Fabrication notes** are text on the schematic telling the builder something the connections cannot say.

<!-- REFPRODUCT:START -->
esp_watch has two notes that every builder of this board must read, both learned on the breadboard:

- *"Remove the I²C pull-up resistors from U2, U3 and U4 before fitting. The only pull-ups are the 4.7 kΩ pair on this board."* Three modules' pull-ups in parallel made 400 kHz unreliable.
- *"U2 must be the MAX30102 module whose I²C lines are referenced to 3.3 V (the black module), not 1.8 V."* The green module clamped the bus to 1.82 V.

Neither fact is visible in the wiring. Without the notes, a builder following the schematic exactly would rebuild the bug.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/schematic.png -->
![The esp_watch schematic in KiCad](../reference-files/images/schematic.png)

---

# Part 2 — Drawing Your Own Symbol

## What a Symbol Actually Contains

A **schematic symbol** is more than a drawing of a box with pins. Each pin carries four pieces of information:

| Property | What it means | Where it comes from |
|---|---|---|
| **Number** | Which physical pad or header pin this is | The datasheet's pin table, or the module's silkscreen |
| **Name** | What the pin does: `SDA`, `VCC`, `INT` | Same source |
| **Electrical type** | How the pin behaves: input, output, power input and so on | The datasheet's pin description |
| **Position** | Where it sits on the symbol outline | Your choice, for readability |

The **number** must match the footprint's pad number exactly, because that number is the only link between the schematic and the copper. The **name** is for humans. The **electrical type** is for ERC.

## Pin Numbers Come From the Part You Will Solder

For a chip, pin numbers come from the datasheet's pin table. For a **module**, they come from the module itself: the header pins, numbered in order, usually starting at the end marked "1" or with a square pad. Two modules built around the same chip can have entirely different header orders.

<!-- REFPRODUCT:START -->
This is why esp_watch's symbols were drawn for the *modules*, not the chips. The MAX30102 chip has 14 pads underneath it. The black MAX30102 module that esp_watch uses has two rows of four header pins, 8 in total. A symbol copied from the chip's datasheet would have the wrong number of pins, in the wrong order.
<!-- REFPRODUCT:END -->

The same idea applies to microcontrollers. The bare ESP32-C3 chip has pins for an external crystal, external flash and an antenna input. The XIAO module has none of these on its edge, because they are inside. Using the chip's symbol for the module would be wrong in exactly the same way.

## Electrical Types, and Why ERC Needs Them

ERC cannot see your circuit's voltages. It only knows each pin's **electrical type**, and it checks that connected pins make sense together. If the types are wrong, ERC either misses real mistakes or reports false ones. KiCad's types [1] include:

| Type | Use for | Example |
|---|---|---|
| Power input | A pin that receives power | Module `VCC`, `GND` |
| Power output | A pin that supplies power | Regulator output, XIAO `3V3` |
| Input | A signal the part only receives | `AD0` address-select pin |
| Output | A push-pull output that drives high and low | A typical interrupt output |
| Bidirectional | A signal that can be driven either way | I²C `SDA` |
| Open collector | An output that can only pull low | MAX30102 `INT`, which is open-drain [2] |
| Passive | Resistors, connectors, pins with no active electronics | Header pins on a connector |
| Unconnected | A pin that must never be connected | A pad with no internal connection |

Two rules from KiCad's documentation matter most [1]:

- A **power input** pin that is not connected to any **power output** pin produces an ERC error. If your power arrives through a connector or battery (passive pins), add a **PWR_FLAG** symbol to that net to tell ERC it is driven.
- **Open collector** outputs may connect to each other and to inputs; ordinary outputs may not connect to other outputs. Mark the MAX30102's interrupt as open collector, and ERC will accept it sharing a net with a pull-up resistor.

A common mistake is to set every pin to *passive* "to make the errors go away". The errors do go away, and so does every check ERC could have made. A symbol full of passive pins is a symbol ERC cannot help you with.

## Worked Example: A Symbol for a Motion-Sensor Module

We will draw a symbol for a GY-521-style MPU-6050 module, the kind of motion-sensor module esp_watch uses.

**Step 1: Get the pin order from the module, not a website.** A common order printed on these modules is `VCC, GND, SCL, SDA, XDA, XCL, AD0, INT`, pins 1 to 8. Your module may differ. Check its silkscreen and write down what *your* board says.

**Step 2: Decide each pin's electrical type** from what the pin does:

| Pin | Name | Type | Reason |
|---|---|---|---|
| 1 | VCC | Power input | Receives the supply |
| 2 | GND | Power input | Ground return |
| 3 | SCL | Input | Clock driven by the controller |
| 4 | SDA | Bidirectional | Data flows both ways |
| 5 | XDA | Bidirectional | Auxiliary bus data; unused on esp_watch |
| 6 | XCL | Output | Auxiliary bus clock; unused on esp_watch |
| 7 | AD0 | Input | Address select |
| 8 | INT | Output | Interrupt output |

**Teaching model:** strictly, I²C allows a peripheral to hold SCL low to pause the controller, so some libraries mark SCL as bidirectional. Either is defensible. Write down which you chose and why.

**Step 3: Lay out for readability.** Put power at the top (`VCC`) and bottom (`GND`). Put signals that go to the microcontroller on the left, and pins that go elsewhere or are unused on the right. Keep the grid KiCad uses, so wires snap cleanly onto the pins.

```text
                 VCC (1)
                   │
             ┌─────┴─────┐
   SCL (3) ──┤           ├── XDA (5)
   SDA (4) ──┤  MPU-6050 ├── XCL (6)
   INT (8) ──┤  module   │
   AD0 (7) ──┤           │
             └─────┬─────┘
                   │
                 GND (2)
```

**Step 4: Fill in the symbol's fields.** Reference designator prefix `U`. Value `MPU-6050_Module`. Footprint: the header footprint for this module. Leaving the footprint field empty is allowed, but linking it now saves a mistake later.

**Step 5: Check the symbol, pin by pin, against your source.** Tick each pin: number, name, type. Do this *before* placing the symbol in the schematic.

**Check.** Place the symbol, connect `VCC` to `+3V3`, `GND` to ground, `SCL` and `SDA` to the bus, `INT` to `IMU_INT`, `AD0` to ground. Put a **no-connect flag** on `XDA` and `XCL` to show they are unused on purpose. Run ERC. The pins should produce no errors of their own.

<!-- MEDIA
type: screenshot
id: C1-01
caption: Drawing a module symbol in KiCad's Symbol Editor
brief: KiCad 9 Symbol Editor, full window. A symbol named "MPU-6050_Module" open in a
  project library "esp_watch_symbols". Rectangle body with 8 pins laid out as in the
  reading: VCC top, GND bottom, SCL/SDA/INT/AD0 on the left, XDA/XCL on the right. The
  Pin Properties dialog is open for pin 8, showing Name "INT", Number "8", Electrical
  type "Output" (dropdown visible), Graphic style "Line". The Symbol Properties
  "Footprint" field visible in the side panel. Light theme.
-->

> **Try it: Find the wrong pin.** A classmate's symbol for a 4-pin OLED module has these pins: 1 `VCC` (power input), 2 `GND` (power input), 3 `SCL` (input), 4 `SDA` (bidirectional). The module's silkscreen, read from pin 1, says: `GND VCC SCL SDA`.
> 1. **Predict.** What would happen on a board built from this symbol?
> 2. **Do.** Compare the symbol with the silkscreen pin by pin, and correct it.
> 3. **Explain.** Would ERC have caught this? Why not?
>
> **Extra challenge:** Suggest one habit that would have caught this before ERC, and write it into your own symbol checklist.

## Library Management

Save your symbols in a **project symbol library** (a `.kicad_sym` file kept with your project), so you can fix a symbol once and copy it to your next project. Name symbols so that they describe exactly what they are: `MAX30102_Module_Black_2x4` says far more than `MAX`.

<!-- REFPRODUCT:START -->
esp_watch keeps its three hand-drawn symbols (MAX30102 module, MPU-6050 module, SSD1306 module) in a project library. The details of each symbol will be added to the course files later.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/kicad/esp_watch_symbols.kicad_sym -->

## Downloaded Symbols Need Checking Too

<!-- REFPRODUCT:START -->
esp_watch's microcontroller symbol and footprint were downloaded from an open-source repository for the XIAO ESP32-C3 [3]. It is a useful resource: KiCad files with battery pads included, published under the GPL-3.0 licence. But read its most recent commit message: *"the symbol didn't have the right reference to the footprint. Not sure if this fixes it or not"* [3].

That is an honest note, and a warning. A symbol's footprint field links it to the copper, and if the link is wrong, the schematic can be perfect while the board is not. Before using a downloaded symbol, open it in the Symbol Editor and check: every pin number against the module's own documentation, every electrical type, and the footprint field.
<!-- REFPRODUCT:END -->

The licence matters as well. GPL-3.0 content can be used, but check what the licence asks of you if you share or sell your design files.

---

# Part 3 — Running ERC

## What ERC Checks

The **Electrical Rules Check** walks every net and checks the connected pin types against a table of allowed combinations. It also reports pins left unconnected without a no-connect flag, labels that connect to nothing, and power inputs with no power source.

ERC checks the drawing's *consistency*. It does not know what the circuit is for. A schematic can pass ERC and still have SDA and SCL swapped, or an interrupt on a boot pin. That is why the pin-map comparison from Part 1 matters: ERC checks the symbols against each other, and you check the schematic against your design.

## The Errors You Will Meet

| ERC message (paraphrased) | What it usually means | Fix |
|---|---|---|
| Input power pin not driven by any output power pin | Power arrives through passive pins (connector, battery, or a downloaded symbol with passive power pins) | Add a PWR_FLAG to the net, after checking the net really is powered |
| Pin not connected | A pin with no wire and no flag | Connect it, or add a no-connect flag if it is unused on purpose |
| Pins of type output and output are connected | Two push-pull outputs on one net | Check the design; if one is really open-drain, fix its type |
| Label not connected to anything | A label with a typo, or on the wrong sheet | Check spelling against the interface table |
| Unspecified pin connected | A symbol pin with type "unspecified" | Give the pin a proper type in the symbol |

<!-- REFPRODUCT:START -->
On esp_watch, the 3.3 V rail comes from the XIAO's `3V3` pin, and the battery arrives on its BAT pads. Whether ERC sees those nets as driven depends entirely on how the downloaded XIAO symbol typed those pins. If the `3V3` pin is a power output, the modules' power inputs are satisfied. If it is passive, ERC reports every module's `VCC` as undriven, and a PWR_FLAG on `+3V3` is the correct fix.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — the electrical types used for the 3V3 and BAT pins in the downloaded XIAO symbol, and whether PWR_FLAGs were needed, are not recorded in REFERENCE-PRODUCT.md -->

**Zero errors** is the goal and the deliverable. Warnings deserve the same attention, but some may be accepted. When you accept one, write down why, as you did for DRC warnings in the verification stack.

<!-- MEDIA
type: screenshot
id: C1-02
caption: KiCad's ERC dialog after a clean run
brief: KiCad 9 Schematic Editor with the Electrical Rules Checker dialog open, after
  running ERC on a small module-based schematic. The dialog shows "0 Errors" and a
  small number of warnings (for example 0–2) in the summary, with the Violations tab
  selected and empty or with one accepted warning marked as excluded. The schematic
  behind it is visible and uncluttered. Light theme.
-->

> **Try it: Break it on purpose.** In your own schematic, after ERC passes:
> 1. **Predict.** What will ERC say if you change one module's `VCC` pin type to *passive*? If you delete the no-connect flag on an unused pin?
> 2. **Do.** Make each change, run ERC, and read the message. Then undo it.
> 3. **Explain.** Which change made ERC *quieter* rather than louder? Why is that more dangerous?

---

# Putting It All Together

## Applying What You Have Learned

**1. Draw your symbols.** For every part without a trustworthy symbol, draw one in a project library. Take pin numbers from the part you will actually solder. Record each pin's type and your reason for it.

**2. Check every symbol, including downloaded ones.** Pin number, name and type against the source. Footprint field filled and correct.

**3. Capture the schematic.** Transcribe your B3 pin map and B2 interface table. Use net names from the interface table. Tick off each connection as you draw it.

**4. Add test points and fabrication notes.** Test points on power, ground and every bus. A note for anything the builder must do that the wiring cannot show.

**5. Run ERC to zero errors.** Fix each error at its cause. Write down every accepted warning and its reason.

**Deliverable:** your KiCad project (schematic and project symbol library), an ERC report showing zero errors, and a symbol checklist, saved in your design pack.

## Self-Check

Open your KiCad project and answer each item Y or N.

1. ERC reports zero errors. — Y/N
2. Every accepted ERC warning has a written reason. — Y/N
3. Every signal net has a name matching the B2 interface table. — Y/N
4. Every connection in the schematic matches the B3 pin map. — Y/N
5. At least one symbol was drawn by you, and is stored in a project library. — Y/N
6. Every symbol's pin numbers were checked against the part you will solder. — Y/N
7. No symbol pin is "unspecified", and no active pin is marked passive to hide an error. — Y/N
8. Every unused pin has a no-connect flag. — Y/N
9. Every symbol has its footprint field filled in. — Y/N
10. Test points exist on every power rail, ground and every bus line. — Y/N

---

## Check Your Understanding

**1.** A student uses the MAX30102 *chip* symbol from a library for a MAX30102 *module* with an 8-pin header. What goes wrong?

- A. Nothing; the chip is the same.
- B. The symbol's 14 pin numbers match the chip's pads, not the module's 8 header pins, so the schematic will not match the part being soldered.
- C. ERC will fail.
- D. The I²C address changes.

<details>
<summary>Answer</summary>

**B.** Pin numbers must match the part you solder, and the module's header is not the chip's pad layout. **A** ignores that the module is a different physical part. **C** is unlikely: ERC checks pin types and connections, not whether you chose the right physical part. **D** is wrong; the address is a property of the chip, unaffected by the symbol.

</details>

**2.** ERC reports "Input power pin not driven" on every module's VCC. The 3.3 V comes from a downloaded microcontroller symbol whose 3V3 pin is typed as passive. What is the correct fix?

- A. Change every module's VCC pin to passive.
- B. After confirming the net really is powered, add a PWR_FLAG to the +3V3 net, or correct the 3V3 pin's type to power output in the downloaded symbol.
- C. Ignore the error.
- D. Delete the power symbols.

<details>
<summary>Answer</summary>

**B.** Either tells ERC the truth: the net is driven. **A** silences the error by removing information, so ERC can no longer catch a real unpowered part. **C** leaves a known error in a deliverable that must have zero. **D** breaks the connections the power symbols make.

</details>

**3.** The MAX30102's interrupt pin is open-drain, active-low, and shares its net with a 10 kΩ pull-up. Which electrical type is correct for that pin?

- A. Output
- B. Open collector
- C. Power output
- D. Passive

<details>
<summary>Answer</summary>

**B.** An open-drain output can only pull low, and KiCad's "open collector" type describes exactly that, allowing it to share a net with a pull-up and with other open-collector pins. **A** would describe a push-pull output that also drives high, which this pin cannot. **C** is for supply pins. **D** hides the pin's behaviour from ERC.

</details>

**4.** A schematic passes ERC with zero errors. Which of these could it still contain?

- A. A power input with no power source
- B. An unconnected pin with no flag
- C. SDA and SCL swapped between the microcontroller and one sensor
- D. Two push-pull outputs on one net

<details>
<summary>Answer</summary>

**C.** Both nets connect bidirectional or input pins, so ERC sees nothing wrong. Only comparing the schematic with your pin map catches this. **A**, **B** and **D** are exactly what ERC reports as errors.

</details>

**5.** Which fabrication note from the reference watch prevents a failure that the wiring alone cannot show?

- A. "Connect SDA to GPIO6."
- B. "Remove the I²C pull-ups from the three modules before fitting; the only pull-ups are the 4.7 kΩ pair on this board."
- C. "GND is common to all parts."
- D. "The display address is 0x3C."

<details>
<summary>Answer</summary>

**B.** The module pull-ups are invisible in the schematic, which only shows the carrier board, yet they change the bus. A note is the only way to pass that on. **A** and **C** are already shown by the wiring. **D** is useful information but fixed by the part, so a builder cannot get it wrong.

</details>

---

## What You Can Now Do, and What Comes Next

- Capture a schematic by transcribing earlier decisions, with meaningful net names.
- Draw a symbol whose numbers match the physical part and whose types let ERC work.
- Check downloaded symbols as carefully as your own.
- Reach zero ERC errors by fixing causes, not by hiding them.
- Add the test points and notes that a builder will need.

The idea to carry forward: **ERC can only check what your symbols tell it.** Accurate pin types make ERC a useful assistant; lazy ones turn it off without telling you.

In [C2 — PCB Layout and Footprints](C2-pcb-layout-and-footprints.md) you will turn this schematic into a board, and meet the symbol's physical partner, the footprint, which has its own ways of being wrong.

---

## References

1. KiCad. *Schematic Editor documentation, version 9.0* (pin electrical types; power pins and PWR_FLAG; labels; ERC). https://docs.kicad.org/9.0/en/eeschema/eeschema.html
2. Analog Devices. *MAX30102 datasheet* (interrupt pin: active-low, open-drain). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
3. VectorSpaceHQ. *XIAO_ESP32C3: KiCad footprint and symbol for XIAO ESP32C3* (KiCad v7 files; battery pads included; GPL-3.0; commit history). https://github.com/VectorSpaceHQ/XIAO_ESP32C3

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
