# B2 — Component Selection: Modules or Discrete ICs?
## Choosing Real Parts, and Reading the Documents That Decide Them

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 2 — Hardware and Electronics Design
**Time:** ~2 hours · **You will produce:** a module-versus-IC decision table, a comparison matrix for three candidate parts, and a preliminary BOM

---

### The Same Sensor, Three Different Decisions

Search any Indian electronics shop for "MAX30102" and you will find a small, ready-made board for under ₹200, often in two colours. Search a component distributor for the same name and you will find the bare chip, a tiny 5.6 × 3.3 mm optical package, for more than the whole ready-made board costs.

Which should you use? The ready-made board is easier to design with and cheaper today. The bare chip is thinner and gives you full control. And the two colours of ready-made board are not the same: on the reference watch, one of them made the whole I²C bus fail.

Every line of a bill of materials involves this decision: use a **module** someone else designed, or place the **chip** yourself. This unit teaches you to make that decision per part and justify it against your spec, to read the datasheets that settle it, and to write down a first bill of materials with real part numbers, prices and stock.

### What You Will Be Able to Do After This Reading

- **Decide**, per part, between a module and a discrete IC, and justify the decision against your spec.
- **Extract** absolute maximum ratings, recommended operating conditions and the application circuit from a datasheet.
- **Distinguish** what a module's listing tells you from what the chip's datasheet tells you, and find the gap between them.
- **Compare** three candidate parts in a weighted matrix.
- **Produce** a preliminary BOM with part numbers, suppliers, prices, stock and lifecycle status.

### What Part 1 Already Covered

Part 1 had you wire ready-made sensor modules and use libraries to read them, and you have looked up pinouts in datasheets. **What is new here** is choosing parts deliberately: deciding between a module and a bare chip, reading a datasheet for its limits rather than just its pinout, and recording each choice with its price, stock and lifecycle so it can be checked later.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Module or Chip?

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
4. **What happens at our quantity?** Check prices at 1, 10 and 100.

<!-- REFPRODUCT:START -->
esp_watch chose modules for every active part, and recorded it as its design approach: the microcontroller, both sensors and the display are all pre-made modules on a custom carrier board. No discrete ICs were placed. Assembly will be done by hand: everything is through-hole or large surface-mount, so no assembly service is needed. The reasons in the table below are reconstructed from the design as built.

| Part | Choice | Main reason | Main cost |
|---|---|---|---|
| ESP32-C3 microcontroller | XIAO module | Radio, crystal, flash, charger and regulator already done | Board area; 11 pins only |
| MAX30102 heart rate | Breakout module | Chip needs a 1.8 V supply and a separate LED supply, and is a leadless optical package | Height; module variants differ (see below) |
| MPU-6050 motion | Breakout module | Hand solderable; ready-made | Height under the display; chip is obsolete |
| SSD1306 display | Display module | A bare OLED panel needs a flexible cable and driver circuit | Fixed size and height |

The total cost of this approach shows up in one number: the board with its parts fitted is **14.044 mm** tall, because the display sits on spacers above the motion-sensor module. Modules made the design fast and hand-solderable. They also made it thick.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/render-iso.png -->
![esp_watch board, angled view, showing the module stack that sets the board's height](../reference-files/images/render-iso.png)

---

# Part 2 — Reading a Datasheet for Its Limits

In Part 1 you used datasheets mainly for pinouts. For selection, you need the sections that tell you whether a part will survive and work in your design.

## Absolute Maximum vs Recommended Operating Conditions

These two tables are easy to confuse, and confusing them destroys parts.

- **Absolute maximum ratings** are the limits beyond which the part may be *permanently damaged*. They are not operating conditions. A part held just below its absolute maximum is not guaranteed to work, only not guaranteed to break.
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
id: B2-01
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

Most datasheets include a **typical application circuit**: the manufacturer's recommended way to connect the chip. It tells you every supporting part you would have to design if you used the bare chip. The MAX30102's operates from a 1.8 V supply with a separate LED supply [1], which means a bare-chip design needs its own 1.8 V regulator, careful decoupling, and I²C pull-ups to a voltage both sides accept.

The chip's I²C input thresholds are defined relative to its 1.8 V supply: a HIGH is anything above 0.7 × VDD [1], about 1.26 V. That is why a MAX30102 can be read by a 3.3 V microcontroller *if* the pull-ups go to 3.3 V: the chip sees 3.3 V as a clear HIGH, and its pins tolerate up to 6 V. It is also why the pull-ups *can* go to 1.8 V instead, which is fine for the chip and fatal for a 3.3 V bus shared with other devices.

## The Module's Listing Is Not the Chip's Datasheet

A module's product page and the chip's datasheet are **different documents saying different things**. The datasheet describes the chip. It cannot tell you what regulator the module maker fitted, what the pull-ups connect to, or whether the design changed last month.

<!-- REFPRODUCT:START -->
esp_watch's two heart-rate modules show exactly this gap. Both carry the same MAX30102 chip, and both work. But the **green** module ties its I²C lines to its internal 1.8 V rail. On a bus of its own it read perfectly: 0 failures in 400 reads. On the shared bus it clamped the bus to 1.82 V, and the motion sensor failed 80% of its reads. The **black** module references its I²C lines to 3.3 V and worked on the shared bus with no failures.

Nothing in the chip's datasheet could have told you which module did which. That information lives only on the module, in its schematic if one exists, or in a measurement.
<!-- REFPRODUCT:END -->

Even the listing for the black module needs care. Robu's page describes its communication interface voltage as "1.8, 3.3V, 5V (optional)" [2], which suggests the level is selectable on the board. A module that *can* be set to 1.8 V may *arrive* set to 1.8 V. Before you accept a module, find out how its pull-up voltage is set, and write it in your interface table.

<!-- ASSET:PLACEHOLDER reference-files/images/max30102-green-vs-black.jpg -->
![The green and black MAX30102 modules. Same chip, different I²C voltage](../reference-files/images/max30102-green-vs-black.jpg)

## Package and Footprint

Finally, the **package** section tells you the part's physical size and how it is soldered. The bare MAX30102 is a 14-pin optical module measuring 5.6 × 3.3 × 1.55 mm, with integrated cover glass [1]. Its pads are underneath the package, so it cannot be soldered with an iron. You will return to packages and footprints in B5; for selection, just ask whether you can assemble it.

> **Try it: Find the limits.** Open the datasheet for one chip in your design, not the module listing.
> 1. **Predict.** What supply voltage does it need, and is that the same as your microcontroller's?
> 2. **Do.** Copy the absolute maximum supply voltage, the recommended supply range, the I²C input HIGH threshold, and the typical and shutdown supply currents into your notes. Find the typical application circuit and list every supporting part it shows.
> 3. **Explain.** Would a bare-chip design need any voltage your board does not already have? If you are using a module, which of those supporting parts must the module provide, and how will you confirm it does?
>
> **Extra challenge:** Find one number that differs between the module's listing and the chip's datasheet. Which one should your design trust, and why?

---

# Part 3 — Comparing Candidates and Writing the First BOM

## The Comparison Matrix

When more than one part could do the job, compare them in a **matrix**: candidates as columns, criteria as rows. Take the criteria from your spec and B1's electrical architecture, not from the product page. Give each criterion a **weight** for how much it matters to *your* product, score each candidate, and multiply.

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
| Hand solderable? | Yes, headers | Yes, headers | No, pads underneath |
| Footprint on carrier | Header pins | 2 × 4 header, 21 × 16 mm module | 5.6 × 3.3 mm package |
| Price, quantity 1 | not recorded | ₹179 incl. GST, Robu [2] | $14.73 ≈ ₹1,296, LCSC [3] |
| Stock (24 Sep 2026) | — | Out of stock at Robu | Listed by LCSC and Mouser; stock not recorded |
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY green MAX30102 module price and source are not recorded in REFERENCE-PRODUCT.md -->

**Step 2: Choose criteria and weights** (1 = minor, 3 = critical). For esp_watch: works on the shared bus (3), hand solderable (3), height (2), price at quantity 10 (1), stock (2).

**Step 3: Score each candidate** from 0 (fails) to 2 (good), and multiply by the weight.

| Criterion | Weight | Green | Black | Bare chip |
|---|---|---|---|---|
| Works on shared 3.3 V bus | 3 | 0 → 0 | 2 → 6 | 2 → 6 |
| Hand solderable | 3 | 2 → 6 | 2 → 6 | 0 → 0 |
| Height | 2 | 1 → 2 | 1 → 2 | 2 → 4 |
| Price | 1 | 2 → 2 | 2 → 2 | 0 → 0 |
| Stock | 2 | 1 → 2 | 1 → 2 | 1 → 2 |
| **Total** | | **12** | **18** | **12** |

**Check.** The black module wins, and the reason is visible: it is the only candidate that scores on *both* critical criteria. The green module fails the most important row outright. When a candidate scores 0 on a weight-3 criterion, treat it as disqualified whatever its total, and say so in the matrix.

Notice also the price row. The bare chip at quantity 1 costs about seven times as much as a complete module carrying the same chip. Module makers buy chips in enormous volumes and assemble thousands of boards at once. Cheap modules can also carry chips that are not genuine: esp_watch's motion sensor reports itself as a clone. A price that looks too good is a reason to check, not a reason to relax.

<!-- MEDIA
type: screenshot
id: B2-02
caption: Parametric search for a heart-rate sensor IC on LCSC
brief: LCSC website, "Specialized Sensors" or heart-rate sensor category, full browser
  window. Filters applied in the left panel: category "Heart Rate Sensors" (or the
  closest available), "In Stock" checked, manufacturer filter showing Analog Devices /
  Maxim. Results list shows MAX30102EFD+T near the top, with the price-break table
  (1+, 10+, 30+) and stock quantity visible. Highlight the filter panel and the
  price-break column. No account details visible.
-->

## Parametric Search, Stock and Lifecycle

To find candidates, use a distributor's **parametric search**: choose a category, then filter by the numbers that matter to you, such as supply voltage, interface, package and stock. LCSC, Mouser and DigiKey all work this way, and Indian shops such as Robu, Robocraze and Element14 India list the common modules. Filter by your *requirements*, not by the first result.

For each candidate you shortlist, record three more things:

- **Stock**, at more than one supplier. On the day this unit was written, three of esp_watch's four modules were out of stock at Robu [2][4][5]. A second supplier is not a luxury.
- **Price at 1, 10 and 100**, because price breaks change which option wins.
- **Lifecycle status**: Active, NRND (not recommended for new designs), EOL (end of life) or Obsolete. Check it on the manufacturer's page as well as the distributor's.

<!-- REFPRODUCT:START -->
esp_watch carries a lifecycle problem: the MPU-6050 motion sensor was formally made obsolete by its manufacturer, TDK InvenSense, in 2023. Modules are still sold everywhere, and the reference watch keeps it. You will work through what that means for a product in E0.
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
| Unit price at 1 / 10 / 100 | ₹179 / — / — |
| Stock, date checked | Out of stock, 24 Sep 2026 |
| Lifecycle | Active / NRND / EOL / Obsolete |
| Second source | Another supplier or an alternative part |

<!-- REFPRODUCT:START -->
esp_watch's main modules, as a preliminary BOM (prices are **example values** from Robu listings on 24 September 2026, including GST):

| Ref | Description | Supplier | Price (qty 1) | Stock | Lifecycle |
|---|---|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | Robu [4] | ₹849 | Out of stock | Active (module) |
| U2 | MAX30102 module, black | Robu [2] | ₹179 | Out of stock | Chip: check in E0 |
| U3 | MPU-6050 module | Robu [5] | ₹159 | Out of stock | **Chip obsolete** |
| U4 | SSD1306 0.96" 128 × 64 OLED, I²C | Robu [6] | ₹229 | In stock | Check in E0 |
| SW1, SW2 | Tactile pushbuttons | — | add in E0 | — | — |
| SW3 | Slide switch | — | add in E0 | — | — |
| R, C | 4.7 kΩ × 2, 10 kΩ, 1 MΩ × 2, 100 nF | — | add in E0 | — | — |
| BT1 | LiPo cell (placeholder: 400 mAh) | — | add in E0 | — | — |
| | **Main modules subtotal** | | **₹1,416** | | |
<!-- REFPRODUCT:END -->

The subtotal is 849 + 179 + 159 + 229 = ₹1,416 before small parts, the battery, the circuit board and shipping. E0 completes this BOM with every line priced at three quantities.

> **Try it: Price breaks change the answer.** A bare-chip version of a sensor costs $14.73 at 1, $14.15 at 10 and $13.15 at 30 [3]. A module costs ₹179 at any quantity.
> 1. **Predict.** Is there any quantity in this range at which the bare chip becomes cheaper than the module?
> 2. **Do.** Convert each price at ₹88 per dollar and compare.
> 3. **Explain.** If the chip never gets cheaper here, what else would have to be true for a company to choose it anyway?

---

# Putting It All Together

## Applying What You Have Learned

**1. Build your module-versus-IC decision table.** One row per active part in your B0 block diagram. Columns: part, choice, main reason (traced to a requirement or an assembly constraint), main cost.

**2. Extract datasheet limits.** For each chip, even those on modules, record absolute maximum supply, recommended supply, I²C HIGH threshold if relevant, typical and shutdown current, and the application circuit's supporting parts. For each module, record how its bus voltage and pull-ups are set.

**3. Compare three candidates.** Pick the part in your design with the most realistic alternatives. Build a weighted matrix with at least five criteria from your spec and B1. Mark any disqualifying zero.

**4. Write your preliminary BOM.** Every part, with supplier, price, stock and date, lifecycle status and a second source for each active part.

**Deliverable:** save all four in your design pack as `B2-component-selection.md`, with the BOM also as a spreadsheet.

## Self-Check

Open your B2 files and answer each item Y or N.

1. Every active part has a module-or-IC decision with a reason traced to a requirement or constraint. — Y/N
2. For every chip, the absolute maximum and the recommended supply voltages are recorded separately. — Y/N
3. Every module has a note of how its bus voltage and pull-ups are set. — Y/N
4. The comparison matrix has at least three candidates and at least five weighted criteria. — Y/N
5. Every matrix criterion traces to your spec or B1. — Y/N
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
- B. In the module's own schematic or by measuring its pull-up voltage, because the chip datasheet cannot describe how each module maker wired the pull-ups
- C. In the I²C specification
- D. In the microcontroller's datasheet

<details>
<summary>Answer</summary>

**B.** The chip datasheet describes only the chip. Pull-up voltage is a module design choice, visible only in the module's schematic or by measurement. **A** is identical for both modules. **C** defines the bus, not how any module is built. **D** describes the other end of the bus.

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
- B. Y wins, because X fails a critical criterion and is disqualified whatever its total.
- C. The weights must be wrong, so start again.
- D. Choose both and decide later.

<details>
<summary>Answer</summary>

**B.** A part that cannot work in your design cannot be rescued by scoring well elsewhere. **A** trusts the sum over the reason for the matrix. **C** may be worth checking, but a disqualifying zero is not evidence of bad weights. **D** delays the decision without adding information.

</details>

**5.** On the day a BOM is checked, three of four modules show "out of stock" at one shop. What is the best response?

- A. Wait for restock.
- B. Record the stock status with the date, and find a second source for each part: another shop, a distributor, or an equivalent part.
- C. Remove those parts from the design.
- D. Stock does not matter at the design stage.

<details>
<summary>Answer</summary>

**B.** Stock changes daily. Recording it with a date, plus a second source, makes the BOM useful to whoever builds it. **A** may leave the build waiting indefinitely. **C** overreacts to a temporary state. **D** is wrong: a design that cannot be bought cannot be built, and the funded build will need these parts.

</details>

**6.** Which statement about modules and lifecycle is most accurate?

- A. If modules are for sale, the chip is in production.
- B. A chip can be formally obsolete while modules carrying it are still widely sold, so check the chip's status with its manufacturer, not the module's availability.
- C. Modules do not have lifecycles.
- D. Obsolete parts cannot be used.

<details>
<summary>Answer</summary>

**B.** The MPU-6050 on the reference watch is exactly this case: obsolete since 2023 and still sold on modules everywhere. **A** is the trap it illustrates. **C** is misleading; a module can disappear or change without notice, which is a lifecycle risk with no warning. **D** is too strong; you can use an obsolete part knowingly, with a plan for replacing it.

</details>

---

## What You Can Now Do, and What Comes Next

- Decide between a module and a chip for each part, with reasons tied to your spec.
- Read a datasheet for its limits, and keep damage limits separate from operating ranges.
- Spot what a module's listing cannot tell you, and check it.
- Compare candidates in a matrix that shows your reasoning.
- Write a first BOM that records price, stock, date and lifecycle.

The idea to carry forward: **the chip's datasheet and the module's listing are different documents.** When they disagree, or when one is silent, measure or check before you trust.

In [B3 — Virtual Prototyping](B3-virtual-prototyping.md) you will build your circuit in a simulator and watch the parts you chose work together, before anything is ordered.

---

## References

1. Analog Devices. *MAX30102 datasheet* (absolute maximum ratings, electrical characteristics, I²C input thresholds, package 5.6 × 3.3 × 1.55 mm, single 1.8 V supply with separate LED supply). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
2. Robu.in. *MAX30102 Heart Rate and Pulse Oximeter Sensor Module (Black)*, listing checked 24 September 2026 (₹179 incl. GST, out of stock; interface voltage 1.8 / 3.3 / 5 V). https://robu.in/product/max30102-heart-rate-and-pulse-oximeter-sensor-module-black/
3. LCSC. *MAX30102EFD+T* (price breaks at 1+, 10+ and 30+). https://www.lcsc.com/product-detail/C6454833.html
4. Robu.in. *Seeed Studio XIAO ESP32C3*, listing checked 24 September 2026 (₹849 incl. GST, out of stock). https://robu.in/product/seeed-studio-xiao-esp32c3-tiny-mcu-board-with-wi-fi-and-ble-battery-charge-supported-power-efficiency-and-rich-interface/
5. Robu.in. *MPU-6050 3-Axis Accelerometer and Gyro Sensor*, listing checked 24 September 2026 (₹159 incl. GST, out of stock; operating voltage 3–5 V). https://robu.in/product/mpu-6050-gyro-sensor-2-accelerometer/
6. Robu.in. *0.96 Inch I2C/IIC 4-Pin OLED Display Module (White)*, listing checked 24 September 2026 (₹229 incl. GST, in stock; SSD1306). https://robu.in/product/0-96-inch-i2c-iic-oled-lcd-module-4pin-with-vcc-gnd-white/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
