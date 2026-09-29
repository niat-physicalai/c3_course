# B3 — Electrical Architecture: MCU, Power, Buses and Pins
## The Big Electrical Decisions, Made Before Any Part Is Chosen

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 2 — Sensing and Hardware Architecture
**Time:** ~2 hours · **You will produce:** a power tree, a current budget spreadsheet and a pin allocation map

---

### Four Decisions That Are Expensive to Change Later

Your block diagram from B2 still has gaps marked "TBD". Which microcontroller? Where does power come from, and how does it reach each part? How big are the pull-up resistors? Which pin does each signal use?

These look like details, but each one locks in others. Choose a microcontroller with too few pins, and the last sensor has nowhere to go. Put a switch in the wrong place, and the battery cannot charge. Put an interrupt on the wrong pin, and the board refuses to start one time in ten. None of these shows up in a subsystem diagram, and all of them are painful to fix once the board exists.

This unit makes the four core electrical decisions in order: the **microcontroller class**, the **power architecture**, the **communication buses** and the **pin allocation**. You will make them for your own design, and check each against the reference watch, including the places where it got things wrong first.

### What You Will Be Able to Do After This Reading

- **Select** a microcontroller class from your requirements: memory, pins, radio, and module versus bare chip.
- **Draw** a power tree from charger to every load, and **identify** what each switch and regulator does.
- **Calculate** a current budget per operating mode, and show how duty cycling changes battery life.
- **Size** I²C pull-up resistors from the bus specification, including the effect of several modules' pull-ups in parallel.
- **Produce** a pin allocation map that avoids boot pins and puts analog signals on suitable pins.

### What Part 1 Already Covered

Part 1 taught you Ohm's law, voltage dividers, GPIO, ADC and I²C at a working level, and you have used pull-up resistors on buttons. **What is new here** is making these choices *for a whole board at once*: planning every rail, budgeting every milliamp, sizing pull-ups from the specification, and allocating every pin before the schematic starts.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Choosing the Microcontroller Class

## What Do You Actually Need?

Choose a **class** of microcontroller first, and a specific part later. The class is defined by four questions, and your spec and interface table already contain the answers.

| Question | Where the answer comes from |
|---|---|
| How much program memory (flash) and working memory (RAM)? | Firmware size, display buffer, data you store (A1's data estimate) |
| How many pins, and of what kinds? | Your B2 interface table: count digital, analog and bus pins |
| Does it need a radio, and which? | Your A1 connection choice |
| Module or bare chip? | Your team's ability to design RF circuits, and your certification budget |

Count pins from the interface table, not from memory. Add about 20% spare, because designs grow and a debug pin is priceless later.

## Module or Bare Chip?

A **bare chip** is the microcontroller itself. A **module** is a small board carrying the chip plus everything it needs to run: a crystal, flash memory, a regulator, and usually an antenna or antenna connector.

The difference shows up clearly in schematic symbols. The bare ESP32-C3 chip has pins for an external crystal, external SPI flash and an antenna input (`LNA_IN`). A module has none of these on its edge, because they are already inside.

| | Module | Bare chip |
|---|---|---|
| Design effort | Low: power, ground and signals | High: crystal, flash, RF matching and antenna layout |
| Radio certification | Module maker has often certified the module | You certify your own design |
| Unit cost at volume | Higher | Lower |
| Board area and height | More | Less |
| Hand soldering | Often possible | Usually needs reflow |

The certification row settles it for a first product: a device that transmits radio needs government approval before it can be sold in India [5], and a pre-certified module saves you most of that work.

<!-- REFPRODUCT:START -->
esp_watch uses the **Seeed Studio XIAO ESP32-C3**: a small module-style board with a 32-bit RISC-V processor, WiFi and Bluetooth, 400 KB of SRAM and 4 MB of flash [1]. It exposes 11 pins labelled D0 to D10, a USB-C port, battery pads and a U.FL connector for an external antenna. esp_watch's interface table needs seven signal pins: two for I²C, two interrupts, two buttons and one analog battery measurement. Seven of eleven leaves four spare, and all four come with restrictions or other uses, as Part 4 shows.
<!-- REFPRODUCT:END -->

<!-- LINK:VERIFY  want: "Seeed or distributor statement of the XIAO ESP32-C3's radio certifications (FCC/CE/other)"  search: "Seeed XIAO ESP32C3 certification FCC CE" -->

> **Try it: Count your pins.** Open your B2 interface table.
> 1. **Predict.** How many microcontroller pins will your design need? Write a number.
> 2. **Do.** Count every row that ends at the microcontroller: bus lines, interrupts, buttons, analog inputs, chip selects, enable lines. Add 20%.
> 3. **Explain.** Was your prediction low? Which kind of signal did you forget?
>
> **Extra challenge:** If your count exceeds your chosen module's pins, list two ways to reduce it without dropping a requirement.

---

# Part 2 — Power Architecture

## The Power Tree

A **power tree** shows every source of energy, every conversion and every switch, down to every load. Draw it before choosing any power part.

<!-- REFPRODUCT:START -->
Here is esp_watch's power tree:

```text
USB-C 5 V (phone charger)
   │
   ▼
┌───────────────────────────────── XIAO ESP32-C3 ──────────────────────────────┐
│  onboard charger ◄──────────────── BAT+ / BAT− pads                          │
│        │                                  ▲                                  │
│        ▼                                  │                                  │
│  3.3 V regulator ─────────────────────────┼──────► 3V3 pin                   │
└───────────────────────────────────────────┼──────────┬───────────────────────┘
                                            │          │ 3.3 V rail
                                     slide switch      ├──► ESP32-C3 (internal)
                                            │          ├──► SSD1306 display
                                     LiPo cell 3.7 V   ├──► MPU-6050 motion sensor
                                            │          ├──► MAX30102 heart rate
                                  1 MΩ / 1 MΩ divider  └──► 4.7 kΩ I²C pull-ups
                                  → GPIO4 (battery sense)
```

Three things in this tree are design decisions worth examining.

**The charger and regulator are on the XIAO.** No external charger was needed. The BAT pads accept a 3.7 V lithium cell only, never 5 V, and the onboard regulator holds 3.3 V as the cell voltage falls.

**The slide switch sits between the cell and the BAT pads.** When the switch is off, the cell is disconnected from everything, including the charger. So plugging in USB with the switch off runs the watch from USB but **cannot charge the battery**. That may be acceptable, but it must be a known behaviour, written in the user instructions, not a surprise.

**The battery divider hangs off the battery.** It draws a small current all the time. Where exactly it connects, before or after the switch, decides whether it drains the cell while the watch is "off".
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — whether the 1 MΩ/1 MΩ battery divider connects before or after the slide switch is not recorded in REFERENCE-PRODUCT.md -->

<!-- FACT:VERIFY esp_watch — REFERENCE-PRODUCT.md §4 states the XIAO regulator can supply up to 700 mA; Seeed's wiki lists "Max 3.3V Output Current: 500mA" at a BAT input of 3.8 V. This reading uses the lower, documented figure. -->

Is the regulator big enough? Seeed lists a maximum 3.3 V output current of **500 mA** with the battery input at 3.8 V [1]. The largest modelled load on esp_watch is a WiFi burst averaging about 100 mA. Radio transmissions draw short peaks above their average, so the margin matters, but 500 mA leaves plenty.

## Battery Measurement with a Divider

<!-- REFPRODUCT:START -->
The XIAO has no pin for measuring its own battery, so esp_watch adds one: two 1 MΩ resistors in series across the battery, with the midpoint on GPIO4 and a 100 nF capacitor from the midpoint to ground.
<!-- REFPRODUCT:END -->

Seeed's own documentation describes the same approach, halving the battery voltage with a divider so the ADC can read it [1].

### Worked Example: Checking the Divider

**Step 1: Will the ADC voltage stay in range?** A fully charged lithium cell is typically about 4.2 V (**assumption**, typical for this chemistry). The divider halves it:

```text
V_adc = 4.2 V × 1 MΩ / (1 MΩ + 1 MΩ) = 2.1 V
```

Seeed notes a nominal full-scale ADC reading of 2,500 mV on this board, varying by about ±10% from chip to chip [1]. The worst case is 2,500 × 0.9 = 2,250 mV, which is still above 2.1 V. It fits.

**Step 2: How much current does it waste?**

```text
I = 3.7 V / (1 MΩ + 1 MΩ) = 1.85 µA
Per day: 1.85 µA × 24 h = 44 µAh = 0.044 mAh
```

Against a daily budget of 40–87 mAh (from A0), this is under 0.1%. Large resistors were the right choice.

**Step 3: Why the capacitor?** Large resistors come with a catch. When the ADC takes a sample, it briefly draws current to charge its own internal sampling capacitor. Through 500 kΩ (the two resistors seen in parallel from the midpoint), that charge arrives too slowly and the reading comes out low. The 100 nF capacitor holds a small reservoir of charge right at the pin, so the ADC samples from the capacitor rather than through the resistors.

**Check.** The divider stays inside the ADC range with a 10% margin, costs almost nothing in battery life, and the capacitor fixes the one weakness of using large resistors. Because the ADC varies ±10% between chips, the firmware should be **calibrated** against a known voltage rather than trusting the nominal scale.

## The Current Budget

A **current budget** lists every operating mode, the current in each, and how long the device spends there. You met a simple version in A0. Here it becomes a spreadsheet you maintain for the rest of the course.

<!-- REFPRODUCT:START -->
esp_watch's figures come from a power model, **not from measurement**. No current was ever measured on the reference watch.

| Mode | Current (modelled) | Power at 3.7 V |
|---|---|---|
| Screen on, WiFi connected | ~36 mA | ~135 mW |
| Heart-rate measurement | ~44 mA | ~165 mW |
| WiFi sync burst | ~100 mA average | ~370 mW |
| Optimised idle (light sleep) | 1–3 mA | 4–10 mW |

Seeed's published figures for the XIAO board alone: active below 75 mA, modem-sleep below 25 mA, light sleep below 4 mA, deep sleep about 44 µA [1].
<!-- REFPRODUCT:END -->

<!-- MEDIA
type: screenshot
id: B3-01
caption: The power budget sheet from esp32c3_watch_bom_power.xlsx
brief: Screenshot of the author's spreadsheet esp32c3_watch_bom_power.xlsx, on the
  sheet that holds the power budget and runtime model. Show the full table: one row
  per operating mode (screen on with WiFi, heart-rate measurement, WiFi sync burst,
  optimised idle), with columns for current, time per day, charge per day and power.
  Show the totals row and the runtime result cell. Crop to the table only, at a
  zoom where every number is readable. Highlight the sleep row, since it dominates.
  Mark the sheet visibly as "modelled, not measured".
-->

### Worked Example: Hours or Days? Duty Cycling the Heart-Rate Sensor

The heart-rate sensor works by shining LEDs into the skin, and those LEDs make heart-rate measurement the most power-hungry regular activity. How often you measure decides whether the battery lasts hours or days.

Use esp_watch's modelled figures and **placeholder** battery: 400 mAh, 80% usable, so 320 mAh.

**Case 1: Measure continuously.**

```text
44 mA × 24 h = 1,056 mAh per day
Runtime: 320 mAh ÷ 44 mA = 7.3 hours
```

**Case 2: Measure for 30 s every 10 minutes** (144 times a day). **Assumption:** the screen stays off during these background readings; the wearer still wakes the screen 50 times a day for 30 s.

```text
Heart rate: 144 × 30 s = 4,320 s = 1.2 h   × 44 mA = 52.8 mAh
Screen:      50 × 30 s = 1,500 s = 0.417 h × 36 mA = 15.0 mAh
Sleep:      24 − 1.2 − 0.417     = 22.38 h × 1 mA  = 22.4 mAh  (best)
                                            × 3 mA  = 67.1 mAh  (worst)
Per day:                                    90.2 mAh (best)  134.9 mAh (worst)
Runtime:    320 ÷ 90.2 = 3.5 days          320 ÷ 134.9 = 2.4 days
```

**Case 3: Measure only when asked**, 5 times a day, which is A0's usage pattern UP-1: **3.7 to 7.9 days**.

**Check.** The same hardware lasts 7 hours, about 3 days, or about a week, depending only on how often the firmware turns on the sensor. The electrical architecture sets the ceiling; the firmware decides how close you get to it. That is why the current budget must be written per mode, not as one number.

> **Try it: Build your budget.** Set up a spreadsheet with these columns: *Mode, Current (mA), Times per day, Duration each (s), Hours per day, mAh per day, Source*.
> 1. **Predict.** Which mode will dominate your daily total?
> 2. **Do.** Fill one row per mode from your A2 state diagram. Use datasheet or module figures, and write where each number came from in the *Source* column. Add a sleep row for the rest of the day. Sum mAh per day, then divide your usable battery capacity by it.
> 3. **Explain.** Was your prediction right? Does your runtime meet your A0 battery requirement?
>
> **Extra challenge:** Add a column for a worst case that uses the highest datasheet figure for each mode. Does the requirement still hold?

A starting template you can paste into any spreadsheet:

```text
Mode,Current_mA,Times_per_day,Duration_s,Hours_per_day,mAh_per_day,Source
Screen on,36,50,30,=C2*D2/3600,=B2*E2,modelled (esp_watch)
Heart rate,44,5,30,=C3*D3/3600,=B3*E3,modelled (esp_watch)
Sleep,2,1,,=24-E2-E3,=B4*E4,modelled mid-range
Total,,,,,=SUM(F2:F4),
Usable capacity mAh,320,,,,,placeholder 400 mAh x 0.8
Runtime days,=B6/F5,,,,,
```

## Decoupling and Protection

Two more items belong in the power architecture.

**Decoupling capacitors** sit right next to each chip's supply pins and supply the sudden bursts of current a chip draws when it switches. A common starting point is a 100 nF capacitor at every supply pin, plus a larger bulk capacitor where power enters the board. With modules, the question changes: most breakout modules already carry their own decoupling, so your job is to check each module's schematic rather than add capacitors by habit.

<!-- FACT:VERIFY esp_watch — whether the carrier board adds any decoupling capacitors beyond the modules' own is not recorded in REFERENCE-PRODUCT.md (only the battery divider's 100 nF is recorded) -->

**Protection** means deciding what happens when something goes wrong electrically:

| Risk | Typical protection | Where it can live |
|---|---|---|
| Battery drained too far | Cut off below a safe voltage | Cell's own protection circuit, charger, or firmware using the battery-sense pin |
| Battery connected backwards | Keyed connector, or a protection device | Connector choice, carrier board |
| USB and battery both connected | Power-path switching | Charger or module |
| Static discharge through buttons or port | ESD protection parts | Carrier board |

<!-- REFPRODUCT:START -->
Seeed states that the XIAO ESP32-C3 can stay connected to USB while running from the battery, because of a protection chip on the board. The battery-sense divider gives the firmware what it needs to shut down cleanly before cut-off, which is the hard stop recorded in A2's failure table.
<!-- REFPRODUCT:END -->

---

# Part 3 — Communication Buses

## Bus Voltage and Addresses

Every device on a bus must agree on two things: the **voltage** that means HIGH, and a unique **address**. You recorded both in B2's interface table. Now make sure they are consistent:

- **Voltage:** every device on the bus should be pulled up to the same voltage, and every device must tolerate it. A 5 V module on a 3.3 V bus needs a **level shifter**. A module whose bus lines sit at 1.8 V internally, like esp_watch's green heart-rate module, will drag the whole bus down.
- **Addresses:** list every device's address and how it is set. Where an address depends on a pin, that pin must be tied to a defined level, never left floating.

<!-- REFPRODUCT:START -->
esp_watch's bus: display 0x3C (fixed), heart rate 0x57 (fixed), motion 0x68 (AD0 tied to ground). No two are the same. One curiosity: the motion sensor's identity register reads 0x70 rather than the genuine part's 0x68, which marks it as a **clone** chip. It works correctly, but it is a reminder that cheap modules may not contain exactly what the label says.
<!-- REFPRODUCT:END -->

## Sizing Pull-up Resistors

I²C lines are **open-drain**: devices can only pull a line LOW. A **pull-up resistor** pulls it back HIGH. Its value is a trade-off:

- **Too large**, and the line rises too slowly, because the resistor must charge the bus's capacitance. Slow edges limit the bus speed.
- **Too small**, and a device pulling the line LOW must sink too much current, and may not pull it low enough to count as a clear LOW.

The I²C specification turns both limits into formulas [2]:

```text
R_min = (V_DD − V_OL) / I_OL        V_OL = 0.4 V at I_OL = 3 mA
R_max = t_r / (0.8473 × C_b)        t_r max = 1000 ns (100 kHz), 300 ns (400 kHz)
                                    C_b = total capacitance of the bus line
```

Think of the pull-up as a spring holding a door shut. A weak spring (large resistor) closes the door slowly. A very strong spring (small resistor) closes it fast, but anyone pushing it open must work very hard. The analogy stops working in one place: a door has one person pushing, while an I²C line may have several pull-up "springs" fitted without anyone noticing, one on every module.

### Worked Example: How Many Pull-ups Is Too Many?

**Assumption:** the bus capacitance is 50 pF. The real value depends on every device pin and every track, and you will estimate it more carefully during layout.

**Step 1: The smallest allowed resistor at 3.3 V.**

```text
R_min = (3.3 − 0.4) / 0.003 = 967 Ω
```

**Step 2: The largest allowed resistor.**

```text
At 400 kHz: R_max = 300 ns / (0.8473 × 50 pF) = 7,081 Ω
At 100 kHz: R_max = 1000 ns / (0.8473 × 50 pF) = 23,604 Ω
```

So at 400 kHz, any value between about 1 kΩ and 7 kΩ is inside the specification. 4.7 kΩ sits comfortably in the middle.

**Step 3: What happens when modules bring their own?** Many breakout modules fit their own pull-ups. Three modules, each with a 4.7 kΩ pair, put three resistors in parallel on each line:

```text
R_parallel = 4.7 kΩ / 3 = 1.57 kΩ
Current when a device pulls LOW: 3.3 V / 1.57 kΩ = 2.1 mA
```

Add the carrier board's own pair and it becomes 4.7 / 4 = 1.18 kΩ, needing 2.8 mA. That is within a hair of the 3 mA every device must be able to sink. One more module, or one module with 2.2 kΩ pull-ups, and the bus is outside the specification.

**Check.** On paper, three pairs (1.57 kΩ) is still legal. But every device on the bus must now sink more than twice the current it would with a single pair, and each extra module eats further into the margin.

<!-- REFPRODUCT:START -->
esp_watch learned this in practice. With three modules' pull-ups in parallel, about 1.5 kΩ, the bus was unreliable at 400 kHz, and the author records this as one contributor. The fix: remove the pull-ups from all three modules and fit **one 4.7 kΩ pair on the carrier board**. With a clone sensor on the bus, the design could not rely on every device meeting the specification exactly, so margin mattered more than the paper limits suggested.
<!-- REFPRODUCT:END -->

The rule to take away: **one pair of pull-ups per bus, placed on purpose.** Check every module's schematic for its own pull-ups, and plan to remove or disable them.

> **Try it: Size for your bus.** Use your B2 interface table.
> 1. **Predict.** Will a 10 kΩ pull-up work at 400 kHz on your bus?
> 2. **Do.** Estimate your bus capacitance at 10 pF per device plus 10 pF for wiring (**assumption**). Calculate R_min and R_max at your bus speed. Then list every module on the bus and whether it carries pull-ups, and calculate the combined value.
> 3. **Explain.** Was 10 kΩ inside the range? What is your combined pull-up, and what do you need to remove?
>
> **Extra challenge:** At what bus capacitance would 4.7 kΩ stop being legal at 400 kHz?

---

# Part 4 — Pin Allocation

## Not All Pins Are Equal

A **pin allocation map** assigns every signal to a specific pin. It is not a matter of taking the next free number. Some pins have special jobs that can trap you:

- **Strapping pins** are read at the moment the chip starts up, to decide *how* it starts, for example normal operation or waiting for new firmware. Anything connected to them must hold the right level at reset.
- **Analog-capable pins** are the only ones that can read a voltage with the ADC.
- **Pins shared with a built-in function**, such as the USB serial port or the boot button, may be busy at startup or during programming.

On the ESP32-C3, the strapping pins are **GPIO2, GPIO8 and GPIO9**. Espressif's datasheet shows that GPIO9 selects between normal start-up and download mode, that GPIO8 must be high for download mode to work, and that GPIO2 is recommended to be pulled high to avoid glitches [3]. Seeed repeats the warning for the XIAO: the wrong level on these pins can stop the board uploading or running its program [1]. The simplest safe rule, and the one esp_watch follows, is to **keep all three high at reset**.

## Worked Example: esp_watch's Pin Map

<!-- REFPRODUCT:START -->
| XIAO pin | GPIO | Capabilities | esp_watch signal | Why this pin |
|---|---|---|---|---|
| D0 | GPIO2 | ADC1, **strapping** | Heart-rate interrupt | Open-drain output with a 10 kΩ pull-up, so it idles **high**, which keeps this strapping pin high at reset |
| D1 | GPIO3 | ADC1 | "Previous" button | To ground, internal pull-up |
| D2 | GPIO4 | ADC1 | Battery sense | Needs an analog pin; ADC1 |
| D3 | GPIO5 | ADC2 | Motion-sensor interrupt | Idles **low**, so it must not be on a strapping pin |
| D4 | GPIO6 | I²C SDA (default) | SDA | XIAO's default I²C pin |
| D5 | GPIO7 | I²C SCL (default) | SCL | XIAO's default I²C pin |
| D6 | GPIO21 | UART TX | not assigned | Left free |
| D7 | GPIO20 | UART RX | not assigned | Left free |
| D8 | GPIO8 | **strapping** | not connected | Kept high at reset (required for download mode); nothing attached that could pull it low |
| D9 | GPIO9 | **strapping**, boot button | not connected | The XIAO's own boot button uses it |
| D10 | GPIO10 | — | "Next" button | To ground, internal pull-up |
<!-- REFPRODUCT:END -->

The D6 and D7 functions come from Seeed's pinout [1]; esp_watch's recorded pin map does not assign them.

Look at the two interrupt lines, because they show the whole method in one decision:

<!-- REFPRODUCT:START -->
- The heart-rate sensor's interrupt is **active-low and open-drain** [4]: it sits high through its pull-up and only pulls low when it has data. Put on GPIO2, the pull-up does double duty. It serves the interrupt *and* holds a strapping pin high at reset. That is why it was placed on GPIO2 rather than GPIO8.
- The motion sensor's interrupt **idles low**. On any strapping pin, it would hold that pin low at reset and could stop the watch starting normally. So it goes on GPIO5, which has no start-up role.
<!-- REFPRODUCT:END -->

Now count what is left. Of the four free pins, GPIO8 and GPIO9 are strapping pins, and D6 and D7 carry the UART, which is useful for debugging. esp_watch is effectively **full**. A v2 that adds even one more button would need to think carefully, which is exactly why you do this map before drawing the schematic.

For analog inputs, use ADC1 pins, as esp_watch does for its battery measurement. Read Espressif's notes on ADC2 before relying on it.

<!-- LINK:VERIFY  want: "Espressif ESP-IDF ADC documentation for ESP32-C3 describing ADC2 limitations"  search: "ESP-IDF ESP32-C3 ADC oneshot ADC2 limitation" -->

<!-- MEDIA
type: diagram
id: B3-02
caption: XIAO ESP32-C3 pin map with esp_watch's allocation and the strapping pins marked
brief: A clean top-view outline of the XIAO ESP32-C3 board (redrawn, not copied from
  Seeed), USB-C at the top. Label all 14 edge pins: D0–D10 down the two sides plus 5V,
  GND, 3V3. Beside each D-pin, show its GPIO number and esp_watch's signal (e.g. "D0 ·
  GPIO2 · MAX INT"). Colour the three strapping pins (GPIO2, GPIO8, GPIO9) amber with a
  small "must be high at reset" note. Colour ADC1-capable pins with a small "A" badge.
  Grey out the unassigned pins (D6, D7, D8, D9) with their reason. Show the BAT+ / BAT−
  pads on the underside as a dashed inset. Flat vector style, readable at 800 px wide.
-->

> **Try it: Find the boot trap.** A student assigns: motion-sensor interrupt (idles low) → GPIO9; heart-rate interrupt (open-drain with a 10 kΩ pull-up, idles high) → GPIO5; buttons to ground → GPIO2 and GPIO3.
> 1. **Predict.** Will this board start up reliably?
> 2. **Do.** For each strapping pin, write the level it will sit at during reset with this allocation. Remember a button to ground reads high through its internal pull-up only after the firmware turns that pull-up on.
> 3. **Explain.** Which assignment is the problem, and what is the smallest change that fixes it?

---

# Putting It All Together

## Applying What You Have Learned

**1. Choose your microcontroller class.** Answer the four questions in Part 1, count pins from your interface table plus 20%, and decide module or bare chip with a reason.

**2. Draw your power tree.** From every source to every load, including switches, regulators, the charger and any measurement circuit. For each switch, write what happens when it is off and USB is connected.

**3. Build your current budget spreadsheet.** One row per mode from your A2 state diagram, with the source of every number. Calculate runtime and compare with your A0 requirement. Add a duty-cycling comparison for your most power-hungry sensor.

**4. Size your pull-ups.** Calculate R_min and R_max for your bus. List every module's own pull-ups, and state which pair you keep.

**5. Allocate your pins.** Build a pin map like esp_watch's, with a *Why this pin* column. Mark every strapping pin and state its level at reset.

**Deliverable:** add the power tree, current budget spreadsheet and pin allocation map to your design pack as `B3-electrical-architecture.md` plus your spreadsheet file.

## Self-Check

Open your B3 files and answer each item Y or N.

1. The microcontroller choice states flash, RAM, pin count and radio requirements, each traced to a source. — Y/N
2. The pin count includes at least 20% spare. — Y/N
3. The power tree shows every source, switch, regulator and load. — Y/N
4. Every switch has a note of what happens when it is off with USB connected. — Y/N
5. Every row in the current budget names the source of its current figure. — Y/N
6. Runtime is calculated and compared with the A0 battery requirement. — Y/N
7. R_min and R_max are calculated for your bus speed, with the capacitance assumption stated. — Y/N
8. Every module's own pull-ups are listed, and exactly one pair per bus is kept. — Y/N
9. Every strapping pin is marked with its level at reset. — Y/N
10. Every analog signal is on an ADC-capable pin. — Y/N

---

## Check Your Understanding

**1.** A team chooses a bare ESP32-C3 chip instead of a module to save ₹150 per unit on a 50-unit run. What is the strongest argument against this?

- A. Bare chips cannot run Arduino code.
- B. The team now owns the crystal, flash, RF layout and antenna design, and the radio certification that goes with them, which far outweighs ₹7,500 in total savings.
- C. Bare chips have fewer GPIO pins.
- D. Modules are always cheaper.

<details>
<summary>Answer</summary>

**B.** At 50 units the saving is ₹7,500 in total, while the extra design, testing and certification work costs far more. **A** is false; the chip runs the same code. **C** is backwards; a bare chip often exposes *more* pins, because none are used internally. **D** is false at volume, where bare chips are usually cheaper per unit.

</details>

**2.** In esp_watch's power tree, the slide switch sits between the cell and the BAT pads. A wearer switches the watch off and plugs in USB overnight. What happens?

- A. The battery charges normally.
- B. The watch runs from USB, but the battery does not charge, because the switch has disconnected it from the charger.
- C. The watch is damaged.
- D. Nothing, because USB is ignored when the switch is off.

<details>
<summary>Answer</summary>

**B.** The switch isolates the cell from everything, including the charger. **A** would need the switch to be somewhere else, for example on the load side after the charger. **C** is wrong; nothing is overloaded. **D** is wrong; USB powers the XIAO directly regardless of the battery switch.

</details>

**3.** A watch draws 44 mA while measuring heart rate and about 2 mA asleep. Measuring continuously gives 7 hours from 320 mAh. Which change most improves runtime while still giving regular readings?

- A. Increase the I²C speed to 400 kHz.
- B. Measure for 30 s every 10 minutes instead of continuously.
- C. Use a larger pull-up resistor.
- D. Turn the display brightness down.

<details>
<summary>Answer</summary>

**B.** Duty cycling cuts sensor-on time from 24 hours to about 1.2 hours a day, taking runtime from hours to days. **A** barely changes energy, since bus time is a tiny part of the budget. **C** saves microamps at most. **D** helps only while the screen is on, which is a small part of the day.

</details>

**4.** Three breakout modules on one I²C bus each carry 4.7 kΩ pull-ups. What is the combined pull-up, and what is the main risk as more modules are added?

- A. 14.1 kΩ; the bus becomes too slow.
- B. 4.7 kΩ; no change.
- C. About 1.57 kΩ; each extra module lowers it further until devices can no longer sink enough current to pull the line clearly LOW.
- D. About 1.57 kΩ; the pull-ups overheat.

<details>
<summary>Answer</summary>

**C.** Resistors in parallel combine to a lower value: 4.7 kΩ ÷ 3 ≈ 1.57 kΩ. Each addition raises the current a device must sink, approaching the 3 mA limit. **A** adds the resistors as if they were in series. **B** ignores the parallel connection. **D** names the wrong risk; the power in each resistor is tiny.

</details>

**5.** A motion sensor's interrupt output idles LOW. Why must it not be connected to GPIO9 on an ESP32-C3?

- A. GPIO9 cannot be used as an input.
- B. GPIO9 is a strapping pin; held LOW at reset, it puts the chip into download mode instead of running the program.
- C. GPIO9 has no pull-up.
- D. Interrupts only work on ADC pins.

<details>
<summary>Answer</summary>

**B.** Espressif's boot table shows GPIO9 at 0 selects download mode. A sensor holding it low at reset stops the watch starting normally. **A** is false; it works as an input once the chip is running. **C** is false; GPIO9 has a weak internal pull-up by default, but a sensor actively driving low overrides it. **D** is false; interrupts work on digital pins.

</details>

**6.** A battery divider uses 10 kΩ + 10 kΩ instead of 1 MΩ + 1 MΩ. What changes?

- A. Nothing; the ratio is the same.
- B. The ADC voltage doubles.
- C. It wastes 100 times more current, about 185 µA at 3.7 V, which is around 4.4 mAh a day.
- D. It no longer needs a capacitor, and has no disadvantages.

<details>
<summary>Answer</summary>

**C.** 3.7 V ÷ 20 kΩ = 185 µA, and × 24 h ≈ 4.4 mAh a day, which is significant in a 40–90 mAh daily budget. **A** is true only of the voltage ratio, not of the current. **B** is false; the ratio is still one half. **D** is half right: smaller resistors charge the ADC's sampling capacitor faster, so the capacitor matters less, but the constant drain is a real disadvantage.

</details>

---

## What You Can Now Do, and What Comes Next

- Choose a microcontroller class from memory, pin, radio and certification needs.
- Draw a power tree and spot the switch that blocks charging.
- Build a current budget per mode and use duty cycling to move from hours to days.
- Size pull-ups from the specification, and remove the ones modules bring uninvited.
- Allocate pins so the board always starts up.

The idea to carry forward: **the electrical architecture sets the limits, and every later decision works inside them.** A pin map with no spare pins, or a budget with no margin, is a limit you have chosen.

In [B4 — Component Selection](B4-component-selection.md) you will choose the actual parts, deciding for each whether a ready-made module or a bare chip is the better fit, and learn to read the datasheets that decide it.

---

## References

1. Seeed Studio. *Getting Started with Seeed Studio XIAO ESP32C3* (memory, pinout table, strapping-pin warning, battery-voltage divider example, ADC full-scale note, power figures including 500 mA maximum 3.3 V output). https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/
2. NXP Semiconductors. *UM10204: I²C-bus specification and user manual* (V_OL and I_OL limits, R_p(min) and R_p(max) equations, rise-time limits). https://www.nxp.com/docs/en/user-guide/UM10204.pdf
3. Espressif Systems. *ESP32-C3 Series Datasheet* (strapping pins GPIO2, GPIO8 and GPIO9; boot-mode table). https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf
4. Analog Devices. *MAX30102 datasheet* (interrupt pin: active-low, open-drain). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
5. Department of Telecommunications, Government of India. *Equipment Type Approval (ETA)* (certification issued by the WPC Wing for wireless equipment). https://www.eservices.dot.gov.in/equipment-type-approval-eta

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
