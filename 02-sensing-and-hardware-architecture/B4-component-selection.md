# B4 — Component Selection: Modules or Discrete ICs?
## Choosing Real Parts, and Reading the Documents That Decide Them

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 2 — Sensing and Hardware Architecture
**Time:** ~1.5 hours · **You will produce:** a module-versus-IC decision table, a comparison matrix for three candidate parts, and a preliminary BOM

---

### The Same Sensor, Three Different Decisions

Search any Indian electronics shop for "MAX30102" and you will find a small, ready-made board for under ₹200, often in two colours. Search a component distributor for the same name and you will find the bare chip, a tiny 5.6 × 3.3 mm optical package, for more than the whole ready-made board costs.

Which should you use? The ready-made board is easier to design with and cheaper today. The bare chip is thinner and gives you full control. And the two colours of ready-made board are not the same: on the reference watch, one of them made the whole I²C bus fail.

Every line of a bill of materials involves this decision: use a **module** someone else designed, or place the **chip** yourself.

### What You Will Be Able to Do After This Reading

- **Decide**, per part, between a module and a discrete IC, and justify the decision against your spec.
- **Extract** absolute maximum ratings, recommended operating conditions and the application circuit from a datasheet.
- **Distinguish** what a module's listing tells you from what the chip's datasheet tells you, and find the gap between them.
- **Compare** three candidate parts in a weighted matrix.
- **Produce** a preliminary BOM with part numbers, suppliers, prices, stock and lifecycle status.

Part 1 had you wire modules and read pinouts. New here: choosing parts, reading datasheets for their limits, and recording price, stock and lifecycle.

---

# Module or Chip?

## What You Gain and What You Give Up

A **breakout module** is a small board carrying a chip plus the parts it needs: regulators, capacitors, pull-up resistors and sometimes level shifters. A **discrete IC** is the chip alone, and you design the supporting circuit yourself.

| | Breakout module | Discrete IC |
|---|---|---|
| Design effort | Connect power, ground and signals | Design the full application circuit |
| Supporting parts | Included | You choose and place them |
| Price per unit, small quantities | Often lower | Often higher |
| Price per unit, large quantities | Higher | Lower |
| Board area and height | More, often much more | Less |
| Assembly | Headers, hand solderable | Often fine-pitch or leadless; needs reflow |
| What you control | Only what the module maker exposes | Everything |
| Supply risk | Module can vanish or change without notice | Chip has a published lifecycle |
| Radio certification (for radio parts) | Often already done by the maker | Your responsibility |

The last-but-one row catches students out. A module from a marketplace seller has no datasheet of its own, no revision history and no promise that next month's batch is the same design. The chip inside has all three. You may find that a module you relied on has quietly changed its pull-ups, its regulator or its chip.

A common belief is that modules are a beginner's shortcut and "real" products use chips. Many real products do move to chips, but usually at volume, once the design is proven. For a first design, especially one that will be hand-soldered, a module is often the correct engineering choice. What matters is that you can say *why*.

## Deciding Per Part

Make the decision separately for each part, because the answer is often different. Ask four questions, each tied to your spec:

1. **Does it fit?** Check your size envelope from A0, especially height.
2. **Can we assemble it?** Leadless and fine-pitch chips need reflow soldering. If your build will be hand-soldered, that decides a lot.
3. **What does the application circuit need?** Extra supply voltages, precise analog parts or an antenna all push towards a module.
4. **What happens at our quantity?** Check prices at 1 and 10.

<!-- REFPRODUCT:START -->
esp_watch chose modules for every active part, and recorded it as its design approach: the microcontroller, both sensors and the display are all pre-made modules on a custom carrier board. No discrete ICs were placed. Assembly will be done by hand: everything is through-hole or large surface-mount, so no assembly service is needed. The reasons in the table below are reconstructed from the design as built.

| Part | Choice | Main reason | Main cost |
|---|---|---|---|
| ESP32-C3 microcontroller | XIAO module | Radio, crystal, flash, charger and regulator already done | Board area; 11 pins only |
| MAX30102 heart rate | Breakout module | Chip needs a 1.8 V supply and a separate LED supply, and is a leadless optical package | Height; module variants differ (see below) |
| MPU-6050 motion | Breakout module | Hand solderable; ready-made | Height under the display; chip is obsolete |
| SSD1306 display | Display module | A bare OLED panel needs a flexible cable and driver circuit | Fixed size and height |

Modules made the design fast and hand-solderable. They also made it thick: the display sits on a female header above the motion-sensor module, and E2 measures how that stack sets the watch's height.
<!-- REFPRODUCT:END -->

![esp_watch board, KiCad 3D render, angled view: the display module stands above the other modules](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_front.png)

---

# Reading a Datasheet for Its Limits

For selection, you need the sections that tell you whether a part will survive and work in your design.

## Absolute Maximum vs Recommended Operating Conditions

These two tables are easy to confuse, and confusing them destroys parts.

- **Absolute maximum ratings** are the limits beyond which the part may be *permanently damaged*. They are not operating conditions. A part run just below its absolute maximum should survive, but nothing says it will work.
- **Recommended operating conditions** (or the electrical characteristics' supply range) are where the part is *guaranteed to work as specified*. Design within these, with margin.

Here is the MAX30102 heart-rate chip [1]:

| Parameter | Absolute maximum | Recommended / specified |
|---|---|---|
| Main supply, VDD | −0.3 V to +2.2 V | 1.7 V to 2.0 V (typical 1.8 V) |
| LED supply, VLED+ | −0.3 V to +6.0 V | 3.1 V to 5.0 V (typical 3.3 V) |
| All other pins (SDA, SCL, INT) | −0.3 V to +6.0 V | — |
| Supply current, measuring | — | 600 µA typical, 1,200 µA maximum |
| Supply current, shut down | — | 0.7 µA typical, 10 µA maximum |

Read that first row carefully. The chip's main supply must be **1.8 V**, and 3.3 V would exceed its absolute maximum. Yet the LED supply wants 3.3 V, and the I²C pins tolerate up to 6 V. So a MAX30102 needs *two* supply voltages, and a module built around it must generate 1.8 V somewhere on the board.

<!-- MEDIA
type: datasheet
id: B4-01
caption: MAX30102 datasheet: absolute maximum ratings beside the electrical characteristics
brief: Two crops from the Analog Devices MAX30102 datasheet placed side by side. Left:
  the "Absolute Maximum Ratings" block, with the rows "VDD to GND −0.3V to +2.2V",
  "VLED+ to PGND −0.3V to +6.0V" and "All Other Pins to GND −0.3V to +6.0V" boxed in red.
  Right: the "Electrical Characteristics" table, with the "Power-Supply Voltage VDD 1.7
  1.8 2.0" and "LED Supply Voltage 3.1 3.3 5.0" rows boxed in green. Add two short
  labels: red "will be damaged beyond this" and green "guaranteed to work within this".
  Keep the datasheet's own text legible; do not retype it.
-->

## The Application Circuit

Most datasheets include a **typical application circuit**: the manufacturer's recommended way to connect the chip. It lists every supporting part a bare-chip design needs. For the MAX30102 [1], that means a 1.8 V regulator, decoupling, and I²C pull-ups to a voltage both sides accept.

The chip's I²C inputs treat anything above a low, fixed threshold (VIH, about 1.4 V [1]) as HIGH, and tolerate up to 6 V. So a 3.3 V microcontroller can read it with pull-ups to 3.3 V. Pull-ups to 1.8 V also suit the chip, but they drag down a 3.3 V bus shared with other devices.
<!-- FACT:VERIFY MAX30102 SDA/SCL VIH: reviewer recalls a fixed 1.4 V minimum, not 0.7 × VDD. Confirm against the datasheet's digital input characteristics. -->

## The Module's Listing Is Not the Chip's Datasheet

A module's product page and the chip's datasheet are **different documents saying different things**. The datasheet describes the chip. It cannot tell you what regulator the module maker fitted, what the pull-ups connect to, or whether the design changed last month.

<!-- REFPRODUCT:START -->
esp_watch's two heart-rate modules carry the same chip. The green one ties its I²C lines to 1.8 V and broke the shared bus. The black one uses 3.3 V and worked (B3). Only the module's schematic, or a measurement, could show the difference.
<!-- REFPRODUCT:END -->

Even the listing for the black module needs care. Robu's page describes its communication interface voltage as "1.8, 3.3V, 5V (optional)" [2], which suggests the level is selectable on the board. A module that *can* be set to 1.8 V may *arrive* set to 1.8 V. Before you accept a module, find out how its pull-up voltage is set, and write it in your interface table.

For a labelled photo of a MAX30102 breakout module, see Last Minute Engineers' pinout guide: https://lastminuteengineers.com/wp-content/uploads/arduino/MAX30102-Module-Pinout.png

<!-- ASSET:PLACEHOLDER reference-files/images/max30102-green-vs-black.jpg — author's own side-by-side photo of the green and black modules still wanted; third-party images are linked, not embedded -->

## Package and Footprint

Finally, the **package** section tells you the part's physical size and how it is soldered. The bare MAX30102 is a 14-pin optical module measuring 5.6 × 3.3 × 1.55 mm, with integrated cover glass [1]. Its pads are underneath the package, so it cannot be soldered with an iron. You will return to packages and footprints in C2; for selection, just ask whether you can assemble it.

---

# Comparing Candidates and Writing the First BOM

## The Comparison Matrix

When more than one part could do the job, compare them in a **matrix**: candidates as columns, criteria as rows. Take the criteria from your spec and B3's electrical architecture, not from the product page. Give each criterion a **weight** for how much it matters to *your* product, score each candidate, and multiply.

> **Teaching model.** A weighted matrix makes your reasoning visible and forces you to name what matters. It does not make the decision for you. If the winner feels wrong, one of your weights is probably wrong, and finding out which is useful.

### Worked Example: Three Ways to Measure Heart Rate

Compare the three candidates for esp_watch's heart-rate sensor: the green module, the black module and the bare chip. Prices are **example values**: listings checked on 24 September 2026, which will have changed by the time you read this. **Assumption:** ₹88 per US dollar.

**Step 1: List the facts.**

<!-- REFPRODUCT:START -->
| | Green MAX30102 module | Black MAX30102 module | Bare MAX30102 chip |
|---|---|---|---|
| I²C voltage | 1.8 V (internal rail) | 3.3 V as used on esp_watch | Set by your own pull-ups |
| Works on esp_watch's shared 3.3 V bus? | No: bus clamped to 1.82 V | Yes: 0 failures in 400 reads | Yes, if designed correctly |
| Supplies needed from your board | 3.3 V | 3.3 V | 1.8 V **and** 3.3 V |
| Hand solderable? | Yes, headers | Yes, by its edge pads | No, pads underneath |
| Footprint on carrier | Header pins | 8 SMD pads under its edges, 20 × 15 mm module (C2) | 5.6 × 3.3 mm package |
| Price, quantity 1 | ₹265 (what the author paid) | ₹179 incl. GST, Robu [2] | $14.73 ≈ ₹1,296, LCSC [3] |
| Stock (24 Sep 2026) | — | Out of stock at Robu | Listed by LCSC and Mouser; stock not recorded |
<!-- REFPRODUCT:END -->


**Step 2: Choose criteria and weights** (1 = minor, 3 = critical). For esp_watch: works on the shared bus (3), hand solderable (3), height (2), price at quantity 10 (1), stock (2).

**Step 3: Score each candidate** from 0 (fails) to 2 (good), and multiply by the weight.

| Criterion | Weight | Green | Black | Bare chip |
|---|---|---|---|---|
| Works on shared 3.3 V bus | 3 | 0 → 0 | 2 → 6 | 2 → 6 |
| Hand solderable | 3 | 2 → 6 | 2 → 6 | 0 → 0 |
| Height | 2 | 1 → 2 | 1 → 2 | 2 → 4 |
| Price | 1 | 1 → 1 | 2 → 2 | 0 → 0 |
| Stock | 2 | 1 → 2 | 1 → 2 | 1 → 2 |
| **Total** | | **11** | **18** | **12** |

Score an unknown as 1 (neutral) and mark it.

**Check.** The black module wins, and the reason is visible: it is the only candidate that scores on *both* critical criteria. The green module fails the most important row outright. When a candidate scores 0 on a weight-3 criterion, treat it as disqualified whatever its total, and say so in the matrix.

Notice also the price row. The bare chip at quantity 1 costs about seven times as much as a complete module carrying the same chip. Module makers buy chips in enormous volumes and assemble thousands of boards at once. Cheap modules can also carry chips that are not genuine: esp_watch's motion sensor reports itself as a clone. A price that looks too good is a reason to check, not a reason to relax.

<!-- MEDIA
type: screenshot
id: B4-02
caption: Parametric search for a heart-rate sensor IC on LCSC
brief: LCSC website, "Specialized Sensors" or heart-rate sensor category, full browser
  window. Filters applied in the left panel: category "Heart Rate Sensors" (or the
  closest available), "In Stock" checked, manufacturer filter showing Analog Devices /
  Maxim. Results list shows MAX30102EFD+T near the top, with the price-break table
  (1+, 10+, 30+) and stock quantity visible. Highlight the filter panel and the
  price-break column. No account details visible.
-->

## Parametric Search and Stock

To find candidates, use a distributor's **parametric search**: choose a category, then filter by the numbers that matter to you, such as supply voltage, interface, package and stock. LCSC, Mouser and DigiKey all work this way, and Indian shops such as Robu, Robocraze and Element14 India list the common modules. Filter by your *requirements*, not by the first result.

For each candidate you shortlist, record three more things:

- **Stock**, at more than one supplier. On the day this unit was written, three of esp_watch's four modules were out of stock at Robu [2][4][5]. A second supplier is not a luxury.
- **Price at 1 and 10**, the quantities of your prototype and funded build.
- **Lifecycle status**: whether the part is still in production. Just note what the distributor says for now; F0 teaches how to check it properly.

<!-- REFPRODUCT:START -->
One of esp_watch's parts, the MPU-6050, is officially obsolete. F0 tells that story in full.
<!-- REFPRODUCT:END -->

## The Preliminary BOM

A **bill of materials** (BOM) lists every part on the board. At this stage it is *preliminary*: enough to check cost, stock and lifecycle, but expect it to change. Use these columns:

| Column | Example |
|---|---|
| Reference | U2 |
| Description | Heart-rate and SpO2 sensor module, I²C, 3.3 V |
| Manufacturer part number (MPN) | For a module, the seller's product name; for a chip, the exact MPN |
| Quantity | 1 |
| Supplier and link | Robu, product page |
| Unit price at 1 / 10 | ₹179 / — |
| Stock, date checked | Out of stock, 24 Sep 2026 |
| Lifecycle | As the distributor states it, e.g. Active or Obsolete (F0 explains the rest) |
| Second source | Another supplier or an alternative part |

<!-- REFPRODUCT:START -->
esp_watch's main modules, as a preliminary BOM (prices are **example values** from Robu listings on 24 September 2026, including GST):

| Ref | Description | Supplier | Price (qty 1) | Stock | Lifecycle |
|---|---|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | Robu [4] | ₹849 | Out of stock | Check in F0 |
| U2 | MAX30102 module, black | Robu [2] | ₹179 | Out of stock | Chip: check in F0 |
| U3 | MPU-6050 module | Robu [5] | ₹159 | Out of stock | **Chip obsolete** |
| U4 | SSD1306 0.96" 128 × 64 OLED, I²C | Robu [6] | ₹229 | In stock | Check in F0 |
| SW1, SW2 | Tactile pushbuttons | — | add in F0 | — | — |
| SW3 | Slide switch (pads on the board; switch not yet fitted) | — | add in F0 | — | — |
| BT1 | Protected LiPo cell, 300 mAh, 30 × 12 × 4 mm | — | add in F0 | — | — |
| | **Main modules subtotal** | | **₹1,416** | | |
<!-- REFPRODUCT:END -->

The subtotal is 849 + 179 + 159 + 229 = ₹1,416 before small parts, the battery, the circuit board and shipping. F0 completes this BOM with every line priced at three quantities.

---

# Putting It All Together

## Applying What You Have Learned

**1. Build your module-versus-IC decision table.** One row per active part in your B2 block diagram. Columns: part, choice, main reason (traced to a requirement or an assembly constraint), main cost.

**2. Extract datasheet limits.** For each chip, even those on modules, record absolute maximum supply, recommended supply, I²C HIGH threshold if relevant, typical and shutdown current, and the application circuit's supporting parts. For each module, record how its bus voltage and pull-ups are set.

**3. Compare three candidates.** Pick the part in your design with the most realistic alternatives. Build a weighted matrix with at least five criteria from your spec and B3. Mark any disqualifying zero.

**4. Write your preliminary BOM.** Every part, with supplier, price, stock and date, lifecycle status and a second source for each active part.

**Deliverable:** save all four in your design pack as `B4-component-selection.md`, with the BOM also as a spreadsheet.

## Self-Check

Open your B4 files and answer each item Y or N.

1. Every active part has a module-or-IC decision with a reason traced to a requirement or constraint. — Y/N
2. For every chip, the absolute maximum and the recommended supply voltages are recorded separately. — Y/N
3. Every module has a note of how its bus voltage and pull-ups are set. — Y/N
4. The comparison matrix has at least three candidates and at least five weighted criteria. — Y/N
5. Every matrix criterion traces to your spec or B3. — Y/N
6. Any candidate scoring 0 on a critical criterion is marked as disqualified. — Y/N
7. Every BOM line has a supplier, a price, a stock status and the date checked. — Y/N
8. Every active part has a lifecycle status. — Y/N
9. Every active part has a second source. — Y/N
10. Prices are marked as example values with the date and currency rate stated. — Y/N

---

## Check Your Understanding

**1.** A chip's datasheet lists VDD absolute maximum as 2.2 V and recommended VDD as 1.7–2.0 V. A student plans to run it at 2.1 V "because it's under the maximum". What is wrong?

- A. Nothing; 2.1 V is below 2.2 V.
- B. The absolute maximum is a damage limit, not an operating point. At 2.1 V the chip is outside its guaranteed range, so its behaviour is not specified.
- C. The chip will be damaged immediately.
- D. The chip needs exactly 1.8 V or it will not start.

<details>
<summary>Answer</summary>

**B.** Operate within the recommended range; the absolute maximum only says where damage may begin. **A** confuses "not broken" with "working as specified". **C** overstates it; 2.1 V is below the damage limit, but that guarantees nothing about correct operation. **D** is too strict; the whole 1.7–2.0 V range is specified.

</details>

**2.** Two MAX30102 modules from different sellers use the same chip. One works on a shared 3.3 V I²C bus; the other drags the bus to 1.8 V. Where would you find the difference?

- A. In the MAX30102 datasheet
- B. In the I²C specification
- C. In the module's own schematic, or by measuring its pull-up voltage
- D. In the microcontroller's datasheet

<details>
<summary>Answer</summary>

**C.** The chip datasheet describes only the chip. Pull-up voltage is the module maker's choice, visible only in its schematic or by measurement. **A** is identical for both modules. **B** defines the bus, not how any module is built. **D** describes the other end of the bus.

</details>
**3.** A bare sensor chip costs about ₹1,300 at quantity 1, while a module carrying the same chip costs ₹179. For a 10-unit hand-soldered build, which is the best reason to choose the module?

- A. Modules are always higher quality.
- B. It is cheaper at this quantity, hand solderable, and already provides the second supply voltage the chip needs.
- C. Bare chips cannot be bought in India.
- D. The module has a longer lifecycle guarantee.

<details>
<summary>Answer</summary>

**B** ties the choice to the quantity, the assembly method and the application circuit. **A** is false; module quality varies widely, as the reference watch's two modules show. **C** is false; the bare chip is stocked by distributors that ship to India. **D** is backwards: a marketplace module usually has *no* lifecycle guarantee, while the chip has a published status.

</details>

**4.** In a weighted matrix, candidate X totals 20 but scores 0 on "works at 3.3 V" (weight 3). Candidate Y totals 17 and scores 2 on every critical criterion. What should the matrix conclude?

- A. X wins, because 20 > 17.
- B. The weights must be wrong, so start again.
- C. Choose both and decide later.
- D. Y wins: X fails a critical criterion, so it is disqualified.

<details>
<summary>Answer</summary>

**D.** A part that cannot work in your design cannot be rescued by scoring well elsewhere. **A** trusts the sum over the reason for the matrix. **B** may be worth checking, but a disqualifying zero is not evidence of bad weights. **C** delays the decision without adding information.

</details>
**5.** On the day a BOM is checked, three of four modules show "out of stock" at one shop. What is the best response?

- A. Record the stock status and date, and find a second source for each part.
- B. Wait for restock.
- C. Remove those parts from the design.
- D. Stock does not matter at the design stage.

<details>
<summary>Answer</summary>

**A.** Stock changes daily. Recording it with a date, plus a second source, makes the BOM useful to whoever builds it. **B** may leave the build waiting indefinitely. **C** overreacts to a temporary state. **D** is wrong: a design that cannot be bought cannot be built.

</details>

---

## What Comes Next

In [B5 — Virtual Prototyping](B5-virtual-prototyping.md) you will build your circuit in a simulator and watch the parts you chose work together, before anything is ordered.

---

## References

1. Analog Devices. *MAX30102 datasheet* (absolute maximum ratings, electrical characteristics, I²C input thresholds, package 5.6 × 3.3 × 1.55 mm, single 1.8 V supply with separate LED supply). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
2. Robu.in. *MAX30102 Heart Rate and Pulse Oximeter Sensor Module (Black)*, listing checked 24 September 2026 (₹179 incl. GST, out of stock; interface voltage 1.8 / 3.3 / 5 V). https://robu.in/product/max30102-heart-rate-and-pulse-oximeter-sensor-module-black/
3. LCSC. *MAX30102EFD+T* (price breaks at 1+, 10+ and 30+). https://www.lcsc.com/product-detail/C6454833.html
4. Robu.in. *Seeed Studio XIAO ESP32C3*, listing checked 24 September 2026 (₹849 incl. GST, out of stock). https://robu.in/product/seeed-studio-xiao-esp32c3-tiny-mcu-board-with-wi-fi-and-ble-battery-charge-supported-power-efficiency-and-rich-interface/
5. Robu.in. *MPU-6050 3-Axis Accelerometer and Gyro Sensor*, listing checked 24 September 2026 (₹159 incl. GST, out of stock; operating voltage 3–5 V). https://robu.in/product/mpu-6050-gyro-sensor-2-accelerometer/
6. Robu.in. *0.96 Inch I2C/IIC 4-Pin OLED Display Module (White)*, listing checked 24 September 2026 (₹229 incl. GST, in stock; SSD1306). https://robu.in/product/0-96-inch-i2c-iic-oled-lcd-module-4pin-with-vcc-gnd-white/

