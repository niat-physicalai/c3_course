# B0 — Hardware Architecture and Block Diagram
## Every Block on the Board, and Every Wire Between Them

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 2 — Hardware and Electronics Design
**Time:** ~1 hour · **You will produce:** a hardware block diagram and an interface table

---

### From "Sensing Subsystem" to Actual Wires

In A1 you split your product into subsystems: sensing, processing, power, connectivity, local user interface. That was the right level for deciding what the system does. It is the wrong level for drawing a circuit. "Sensing talks to processing" does not tell you how many wires, at what voltage, in which direction, or how fast.

Those details are where designs break. Two sensors on the same bus can have the same address. A module can work at a different voltage from the microcontroller. A display can use so much of a shared bus that the sensors struggle to get a turn. None of these problems is visible in a subsystem diagram, and all of them are visible in a well-made block diagram and interface table.

This unit takes the hardware subsystems down one level: every block that will appear on the board, and every connection between them, described precisely enough that the schematic can be drawn from it without guessing.

### What You Will Be Able to Do After This Reading

- **Draw** a hardware block diagram showing every block on the board and every connection between them.
- **Produce** an interface table listing each connection's signal, protocol, voltage, direction and data rate.
- **Calculate** how long a transfer takes on an I²C bus, and check the result against a measurement.
- **Identify** when a shared bus is too busy, before any hardware exists.

### What Part 1 Already Covered

Part 1 taught you to wire and use I²C, SPI and UART devices, scan an I²C bus for addresses, and drive an OLED display. **What is new here** is documenting every connection on a board *before* drawing a schematic, and using simple numbers to spot conflicts such as a crowded bus while they are still cheap to fix.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## What a Hardware Block Diagram Shows

A **hardware block diagram** is a drawing of the board's electrical parts as boxes, with lines for every connection between them. It sits between the subsystem breakdown and the schematic:

```text
A1 subsystem breakdown        "Sensing talks to processing"
        │
        ▼
B0 hardware block diagram     "Heart-rate sensor ↔ microcontroller:
        │                      I²C at 3.3 V, plus one interrupt line"
        ▼
B4 schematic                  Every pin, resistor and net name
```

Each level adds detail without changing the one above. If your block diagram shows something the subsystem breakdown does not explain, one of them is wrong.

A good block diagram follows four rules:

1. **One box per physical part or module** that will appear on the board or plug into it: the microcontroller module, each sensor, the display, the battery, the switches.
2. **Every connection is drawn**, including power and ground. Missing a ground line on a diagram is how a missing ground ends up on a board.
3. **Each line is labelled** with its name and type: `I²C`, `INT`, `3V3`, `analog`.
4. **Shared connections are drawn as shared.** If three devices sit on one bus, draw one bus with three taps, not three separate lines. The sharing is the most important fact about it.

A common misunderstanding is that the block diagram is a rough sketch to throw away once the schematic exists. In fact it is the document you check the schematic *against*. When the schematic has a connection the block diagram does not, you have found either an undocumented decision or a mistake.

## The Interface Table

The block diagram shows *that* two blocks connect. The **interface table** says exactly *how*. It has one row per connection and these columns:

| Column | What it records | Why it matters |
|---|---|---|
| Signal | The name of the connection | Becomes the net name in the schematic |
| From → To | Which blocks it connects | Catches connections to nowhere |
| Protocol / type | I²C, SPI, UART, GPIO, analog, power | Decides pins and parts |
| Voltage | The logic or supply level | Catches 5 V meeting a 3.3 V pin |
| Direction | In, out or both, from the microcontroller's view | Catches two outputs fighting |
| Data rate | How much data, how often | Catches overloaded buses |
| Notes | Addresses, pull-ups, anything unusual | Where the traps are written down |

The **voltage** column earns its place quickly. Many breakout modules carry their own regulators and level shifters, and a module's pins are not always at the voltage you expect. The **data rate** column is the one students skip, and the one that catches the problems that are hardest to see.

## Worked Example: The Reference Watch

<!-- REFPRODUCT:START -->
esp_watch is built from modules on a custom carrier board. The XIAO ESP32-C3 module is the microcontroller. The MAX30102 heart-rate sensor, the MPU-6050 motion sensor and the SSD1306 display are breakout modules. There are two buttons, a slide switch in the battery line, and a small circuit to measure the battery.

### The Block Diagram

```text
                               3.3 V rail (from XIAO 3V3 pin)
        ┌───────────────┬────────────────┬────────────────┬─────────────┐
        │               │                │                │             │
  ┌───────────┐   ┌───────────┐    ┌───────────┐          │       4.7 kΩ × 2
  │  SSD1306  │   │ MPU-6050  │    │ MAX30102  │          │       pull-ups
  │  display  │   │  motion   │    │ heart rate│          │             │
  │   0x3C    │   │   0x68    │    │   0x57    │          │             │
  └─────┬─────┘   └──┬─────┬──┘    └──┬─────┬──┘          │             │
        │  I²C       │     │ INT      │     │ INT         │             │
 SDA/SCL├────────────┴─────┼──────────┴─────┼─────────────┼─────────────┘
 (shared bus)              │                │             │
        │                  │                │             │
  ┌─────┴──────────────────┴────────────────┴─────────────┴─────────────┐
  │                        XIAO ESP32-C3 module                         │
  │  SDA GPIO6 · SCL GPIO7 · IMU INT GPIO5 · MAX INT GPIO2              │
  │  "next" GPIO10 · "previous" GPIO3 · battery sense GPIO4 (ADC)       │
  │  USB-C (charging) · onboard charger · 3.3 V regulator · U.FL antenna│
  └────┬──────────────┬───────────────┬────────────────┬────────────────┘
       │              │               │                │
  SW1 "next"     SW2 "previous"   1 MΩ / 1 MΩ      BAT+ / BAT−
  to GND         to GND           divider +        │
                                  100 nF           slide switch
                                                   │
                                                LiPo cell
```

All four modules share one 3.3 V supply and one ground (ground lines are not drawn above, to keep the diagram readable; the table below lists them). All three peripherals share one I²C bus, with a single pair of pull-up resistors on the carrier board.

### The Interface Table

| Signal | From → To | Type | Voltage | Direction (MCU view) | Data rate | Notes |
|---|---|---|---|---|---|---|
| SDA, SCL | XIAO ↔ display, motion, heart rate | I²C | 3.3 V | Both | 100 or 400 kHz bus clock | Addresses 0x3C, 0x68, 0x57. One 4.7 kΩ pull-up pair on the carrier; module pull-ups removed |
| MAX_INT | Heart rate → XIAO GPIO2 | Digital, open-drain | 3.3 V | In | Once per batch of samples | 10 kΩ pull-up; idles high. Pin chosen to keep a boot pin high (see B1) |
| IMU_INT | Motion → XIAO GPIO5 | Digital | 3.3 V | In | On motion events | Idles low, so must not be on a boot pin |
| BTN_NEXT | SW1 → XIAO GPIO10 | Digital | 3.3 V | In | Human speed | To ground; internal pull-up |
| BTN_PREV | SW2 → XIAO GPIO3 | Digital | 3.3 V | In | Human speed | To ground; internal pull-up |
| VBAT_SENSE | Divider → XIAO GPIO4 | Analog (ADC) | About half of battery voltage | In | Occasional | 1 MΩ / 1 MΩ divider with 100 nF; the XIAO has no battery-measurement pin |
| 3V3 | XIAO 3V3 pin → all modules, pull-ups | Power | 3.3 V | Out | — | XIAO regulator |
| BAT+, BAT− | LiPo → slide switch → XIAO pads | Power | 3.7 V nominal | In | — | 3.7 V cell only, never 5 V |
| USB | Charger → XIAO USB-C | Power | 5 V | In | — | Onboard charging |
| Antenna | XIAO → external antenna | RF, U.FL cable | — | Both | WiFi, once at first boot | No copper beneath it; keep away from the battery |
| GND | Common to all | Ground | 0 V | — | — | Shared reference for every signal |
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/schematic.png -->
![esp_watch schematic, for comparison with the block diagram above](../reference-files/images/schematic.png)

Compare the schematic with the block diagram. Every line in the diagram should become one or more nets in the schematic. If you find a net in the schematic that is missing from the diagram, add it to the diagram. The diagram is the record of intent.

## How Busy Is the Shared Bus?

The data-rate column raises a real question for esp_watch: three devices share one I²C bus, and one of them is a display. How much of the bus does the display use?

### Worked Example: Predicting a Display Update

**Step 1: How much data is a full screen?** The display is 128 × 64 pixels, one bit per pixel.

```text
128 × 64 = 8,192 pixels
8,192 bits ÷ 8 = 1,024 bytes per full screen
```

**Step 2: How many clock pulses does each byte take?** On I²C, every byte is followed by an acknowledge bit from the receiver [1], so each byte takes 9 clock pulses.

```text
1,024 bytes × 9 clocks = 9,216 clock pulses
```

**Teaching model:** this ignores the address byte, command bytes and short gaps between transfers. They add a little.

**Step 3: Divide by the bus clock.**

```text
At 100 kHz:  9,216 ÷ 100,000 = 0.092 s = 92 ms per screen
At 400 kHz:  9,216 ÷ 400,000 = 0.023 s = 23 ms per screen
```

**Step 4: Check against a real measurement.**

<!-- REFPRODUCT:START -->
The author measured a full screen update on esp_watch's breadboard prototype: **about 90 ms at 100 kHz** (around 12 updates a second) and **about 25 ms at 400 kHz** (around 30 a second).
<!-- REFPRODUCT:END -->

The prediction is within a few percent at both speeds. At 400 kHz the measured time is a little longer than predicted, because the fixed overheads the teaching model ignored become a bigger share when the data itself moves faster.

**Step 5: What does this mean for the other devices?** Suppose the display is redrawn 30 times a second at 400 kHz:

```text
30 screens × 25 ms = 750 ms of every second
Bus left for the two sensors: 250 ms per second (25%)
```

At 100 kHz it is worse. A full screen takes 90 ms, so the display alone cannot exceed about 11 or 12 updates a second, and at that rate the bus is almost never free for the sensors.

Compare that with what the sensors need. **Example values:** the heart-rate sensor producing 100 samples a second, at 6 bytes per sample in its red-plus-infrared mode [2], and the motion sensor read 50 times a second, at 6 bytes of acceleration data per read.

```text
Heart rate:  100 × 6 = 600 bytes/s
Motion:       50 × 6 = 300 bytes/s
Total:                  900 bytes/s × 9 clocks = 8,100 clocks/s

At 400 kHz: 8,100 ÷ 400,000 = 2% of the bus
```

**Check.** The sensors need about 2% of the bus. A display redrawing constantly takes 75%. The conclusion for the architecture is clear: **the display should only be redrawn when something on it changes**, not on every pass through the program. That one decision, visible from a data-rate column, protects the sensors' share of the bus. You will build exactly this behaviour when you write the firmware.

> **Try it: Half a screen.** Most screen changes on a watch only affect part of the display, such as the heart-rate number.
> 1. **Predict.** If only the top quarter of the screen (128 × 16 pixels) is sent, how long does an update take at 400 kHz?
> 2. **Do.** Work through steps 1 to 3 for 128 × 16 pixels.
> 3. **Explain.** Compare with a full screen. What would you need from the display library for this to be possible?
>
> **Extra challenge:** At 100 kHz, how many partial updates a second could you send while still leaving 50% of the bus free?

## What the Reference Watch Learned the Hard Way

The voltage and notes columns look like paperwork until you see what they would have caught.

<!-- REFPRODUCT:START -->
During breadboard testing, esp_watch's builder first used a **green** version of the MAX30102 module. It worked perfectly on a bus of its own: 0 failed reads out of 400. On the shared bus, the bus's idle voltage sat at **1.82 V** instead of 3.3 V. The motion sensor failed 80% of its reads and often vanished from bus scans altogether, and the display quietly showed corrupted output. The cause: the green module ties its I²C lines to its own internal 1.8 V supply. It was not a 3.3 V device on its I²C pins, whatever the rest of the module said.

The **black** version of the module keeps its I²C lines at 3.3 V. With it, all three devices were found at both 100 kHz and 400 kHz, with 0 failures out of 800 motion reads and 0 out of 400 heart-rate reads.

A careful voltage column for the interface table, filled in from the module's own documentation or a measurement of its pull-ups, would have flagged the green module before it went on the bus.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/max30102-green-vs-black.jpg -->
![The green and black MAX30102 modules side by side. They look almost the same but use different I²C voltages](../reference-files/images/max30102-green-vs-black.jpg)

Two more lessons from the same build belong in every interface table:

<!-- REFPRODUCT:START -->
- **Check address-select pins.** The MPU-6050's address depends on a pin called AD0. Left unconnected, the motion sensor appeared and disappeared between scans, with between 6% and 80% of reads failing. Tied to ground, it sits reliably at 0x68. The notes column should say "AD0 tied to GND", not just "0x68".
- **Check the supply range.** Powering the motion-sensor module's VCC pin from 5 V stopped it responding entirely. The MPU-6050 chip itself is rated for about 2.4 to 3.5 V [3], and whether a module survives 5 V depends on whether it has its own regulator. The voltage column should record the *chip's* limits, not what the module's label suggests.
<!-- REFPRODUCT:END -->

> **Try it: Audit an interface table.** A classmate's table has this row: `SDA/SCL | MCU ↔ OLED, IMU, pulse sensor | I²C | — | Both | — | Addresses 0x3C, 0x68, 0x57`.
> 1. **Predict.** Which blank or vague entries could hide a problem like the green module's?
> 2. **Do.** Rewrite the row with every column filled, and add what must be checked for each module.
> 3. **Explain.** Which column would have caught the 1.82 V problem, and which would have caught the AD0 problem?

---

# Putting It All Together

## Applying What You Have Learned

**1. Draw your hardware block diagram.** Start from the hardware subsystems in your A1 breakdown. Draw one box per module or part, every connection including power and ground, and shared buses as shared.

**2. Build your interface table.** One row per connection, every column filled. Where you do not know a value yet, write "TBD in B1" or "TBD in B2", never leave it blank.

**3. Check your busiest bus.** Estimate the data rate of every device on it, as in the worked example. If any bus exceeds about 50% use, write down how you will reduce it: a faster clock, partial updates, fewer reads, or a second bus.

**Deliverable:** save the block diagram and interface table in your design pack as `B0-hardware-architecture.md`.

## Self-Check

Open `B0-hardware-architecture.md` and answer each item Y or N.

1. Every hardware subsystem from A1 appears as at least one block. — Y/N
2. Every block has a power connection and a ground connection. — Y/N
3. Shared buses are drawn as one bus with several taps. — Y/N
4. Every connection in the diagram has a row in the interface table. — Y/N
5. Every row has a voltage, or "TBD" with the unit that will decide it. — Y/N
6. Every I²C device's address is listed, with how it is set. — Y/N
7. No two devices on the same bus share an address. — Y/N
8. The busiest bus has a data-rate estimate with every step shown. — Y/N

---

## Check Your Understanding

**1.** A student's block diagram shows three separate lines from the microcontroller, one each to a display, a motion sensor and a heart-rate sensor, all labelled "I²C". What is wrong?

- A. Nothing, because each device is connected.
- B. It hides that the three share one bus, which is the key fact for addresses, pull-ups and bus load.
- C. I²C devices cannot share a bus.
- D. Each line needs its own pull-up.

<details>
<summary>Answer</summary>

**B.** Drawing one shared bus makes the shared problems visible: address conflicts, combined pull-up resistance and competition for bus time. **A** misses the point of the diagram. **C** is false; sharing is what I²C is designed for. **D** follows from the wrong drawing. Adding pull-ups for each "line" would put several in parallel on the same bus, which is exactly what the reference watch had to remove.

</details>

**2.** A 128 × 32 display (1 bit per pixel) is sent in full over I²C at 100 kHz. Using 9 clocks per byte and ignoring overheads, how long does one update take?

- A. About 5 ms
- B. About 23 ms
- C. About 46 ms
- D. About 92 ms

<details>
<summary>Answer</summary>

**C.** 128 × 32 = 4,096 bits = 512 bytes. 512 × 9 = 4,608 clocks. 4,608 ÷ 100,000 = 0.046 s. **D** is the time for a 128 × 64 display. **B** is the 128 × 64 time at 400 kHz. **A** is the time at 1 MHz, ten times faster than the bus in the question.

</details>

**3.** A heart-rate module works perfectly alone but, on a shared bus, makes other devices fail and pulls the idle bus voltage to 1.8 V. Which interface-table column should have flagged this in advance?

- A. Direction
- B. Data rate
- C. Voltage
- D. Signal name

<details>
<summary>Answer</summary>

**C.** The module's I²C lines were tied to its internal 1.8 V supply, while the bus and the other devices expected 3.3 V. A voltage entry checked against the module's actual pull-up arrangement would have caught it. **A** and **D** are correct for the module, and **B** has nothing to do with the voltage level of an idle bus.

</details>

**4.** An interface table lists the motion sensor as "I²C, 0x68". On the bench, the sensor appears and disappears between scans. What note was missing?

- A. The bus clock speed
- B. How the address is set, for example "AD0 tied to GND"
- C. The sensor's sample rate
- D. The interrupt pin number

<details>
<summary>Answer</summary>

**B.** The address depends on a pin that must be tied to a defined level. Left floating, it drifts, and so does the address. Recording *how* the address is set turns an easy-to-miss wiring detail into a checklist item. **A**, **C** and **D** are useful notes but would not explain a device that comes and goes.

</details>

**5.** On a shared 400 kHz bus, the display is redrawn 30 times a second (25 ms each), and two sensors need about 2% of the bus. The sensors occasionally miss readings. Which change helps most?

- A. Add a second pair of pull-up resistors.
- B. Redraw the display only when its content changes.
- C. Reduce the sensors' sample rate.
- D. Slow the bus to 100 kHz.

<details>
<summary>Answer</summary>

**B.** The display uses about 75% of the bus. Redrawing only on change frees most of that time. **A** lowers the pull-up resistance but does nothing about bus time, and too many pull-ups caused problems on the reference watch. **C** cuts data that the sensors need, while leaving the real cause untouched. **D** makes every transfer four times slower, and the display would then take almost the whole bus.

</details>

---

## What You Can Now Do, and What Comes Next

- Draw a block diagram in which every part, bus and supply is visible.
- Write an interface table that records voltage, direction, data rate and the traps.
- Predict bus timing from first principles and check it against a measurement.
- Spot an overloaded shared bus and fix it at the architecture level.

The idea to carry forward: **the block diagram records your intent, and the schematic is checked against it.** Anything in the schematic that is not in the diagram is either a new decision or a mistake.

In [B1 — Electrical Architecture](B1-electrical-architecture.md) you will make the decisions this unit left as "TBD": which microcontroller, how power flows, how large the pull-ups should be, and which pin carries each signal.

---

## References

1. NXP Semiconductors. *UM10204: I²C-bus specification and user manual* ("Each byte must be followed by an Acknowledge bit"). https://www.nxp.com/docs/en/user-guide/UM10204.pdf
2. Analog Devices. *MAX30102 datasheet* (I²C addresses 0xAE/0xAF, FIFO data format: 6 bytes per sample in SpO2 mode, 3 bytes per LED channel; active-low open-drain interrupt). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
3. TDK. *MPU-6050 detailed information* (VDD supply 2.375 to 3.46 V). https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part_no=MPU-6050

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
