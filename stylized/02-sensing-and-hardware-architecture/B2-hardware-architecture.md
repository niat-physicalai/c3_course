<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">B2 — Hardware Architecture and Block Diagram</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Every Block on the Board, and Every Wire Between Them</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 2 — Sensing and Hardware Architecture <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a hardware block diagram and an interface table</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">From "Sensing Subsystem" to Actual Wires</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In A1 you split your product into subsystems: sensing, processing, power, connectivity, local user interface. That was the right level for deciding what the system does. It is the wrong level for drawing a circuit. "Sensing talks to processing" does not tell you how many wires, at what voltage, in which direction, or how fast.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Those details are where designs break. Two sensors on the same bus can have the same address. A module can work at a different voltage from the microcontroller. A display can use so much of a shared bus that the sensors struggle to get a turn. None of these problems is visible in a subsystem diagram, and all of them are visible in a well-made block diagram and interface table.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Draw</strong> a hardware block diagram showing every block on the board and every connection between them.</li><li style="margin:6px 0;">​<strong>Produce</strong> an interface table listing each connection's signal, protocol, voltage, direction and data rate.</li><li style="margin:6px 0;">​<strong>Calculate</strong> how long a transfer takes on an I²C bus, and check the result against a measurement.</li><li style="margin:6px 0;">​<strong>Identify</strong> when a shared bus is too busy, before any hardware exists.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 taught you to wire and use I²C, SPI and UART devices, scan an I²C bus for addresses, and drive an OLED display. <strong>What is new here</strong> is documenting every connection on a board before drawing a schematic, and using simple numbers to spot conflicts such as a crowded bus while they are still cheap to fix.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What a Hardware Block Diagram Shows</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A <strong>hardware block diagram</strong> is a drawing of the board's electrical parts as boxes, with lines for every connection between them. It sits between the subsystem breakdown and the schematic:</div>

```text
A1 subsystem breakdown        "Sensing talks to processing"
        │
        ▼
B2 hardware block diagram     "Heart-rate sensor ↔ microcontroller:
        │                      I²C at 3.3 V"
        ▼
C1 schematic                  Every pin, resistor and net name
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each level adds detail without changing the one above. If your block diagram shows something the subsystem breakdown does not explain, one of them is wrong.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A good block diagram follows four rules:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>One box per physical part or module</strong> that will appear on the board or plug into it: the microcontroller module, each sensor, the display, the battery, the switches.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Every connection is recorded</strong>, including power and ground. A shared ground can be a note on the diagram, but it must have a row in the interface table.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Each line is labelled</strong> with its name and type: I²C, INT, 3V3, analog.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Shared connections are drawn as shared.</strong> If three devices sit on one bus, draw one bus with three taps, not three separate lines. The sharing is the most important fact about it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A common misunderstanding is that the block diagram is a rough sketch to throw away once the schematic exists. In fact it is the document you check the schematic against. When the schematic has a connection the block diagram does not, you have found either an undocumented decision or a mistake.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Interface Table</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The block diagram shows that two blocks connect. The <strong>interface table</strong> says exactly how. It has one row per connection and these columns:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Column</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it records</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why it matters</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Signal</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The name of the connection</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Becomes the net name in the schematic</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">From → To</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Which blocks it connects</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Catches connections to nowhere</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Protocol / type</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C, SPI, UART, GPIO, analog, power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Decides pins and parts</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Voltage</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The logic or supply level</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Catches 5 V meeting a 3.3 V pin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Direction</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">In, out or both, from the microcontroller's view</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Catches two outputs fighting</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Data rate</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How much data, how often</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Catches overloaded buses</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Notes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Addresses, pull-ups, anything unusual</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Where the traps are written down</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The <strong>voltage</strong> column earns its place quickly. Many breakout modules carry their own regulators and level shifters, and a module's pins are not always at the voltage you expect. The <strong>data rate</strong> column is the one students skip, and the one that catches the problems that are hardest to see.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: The Reference Watch</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch is built from modules on a custom carrier board. The XIAO ESP32-C3 module is the microcontroller. The MAX30102 heart-rate sensor, the MPU-6050 motion sensor and the SSD1306 display are breakout modules. There are two buttons and a slide switch in the battery line (its pads are on the board; the switch itself is still to be fitted). Both sensors are read over I²C only: their interrupt pins are not used, and the watch does not measure its battery, because the XIAO handles charging and the protected cell cuts itself off.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Block Diagram</div>

```text
                               3.3 V rail (from XIAO 3V3 pin)
        ┌───────────────┬────────────────┬────────────────┐
        │               │                │                │
  ┌───────────┐   ┌───────────┐    ┌───────────┐          │
  │  SSD1306  │   │ MPU-6050  │    │ MAX30102  │          │
  │  display  │   │  motion   │    │ heart rate│          │
  │   0x3C    │   │   0x68    │    │   0x57    │          │
  │ +pull-ups │   │ +pull-ups │    │ +pull-ups │          │
  └─────┬─────┘   └─────┬─────┘    └─────┬─────┘          │
        │  I²C          │                │                │
 SDA/SCL├───────────────┴────────────────┘                │
 (shared bus)                                             │
        │                                                 │
  ┌─────┴─────────────────────────────────────────────────┴─────────────┐
  │                        XIAO ESP32-C3 module                         │
  │  SDA D4 · SCL D5 · "next" D10 · "previous" D9                       │
  │  USB-C (charging) · onboard charger · 3.3 V regulator · U.FL antenna│
  └────┬──────────────┬────────────────────────────────┬────────────────┘
       │              │                                │
  SW1 "next"     SW2 "previous"                    BAT+ / BAT−
  to GND         to GND                                │
                                                   slide switch (SW3)
                                                       │
                                                 protected LiPo cell
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">All four modules share one 3.3 V supply and one ground (ground lines are not drawn above, to keep the diagram readable; the table below lists them). All three peripherals share one I²C bus. The carrier board adds no pull-up resistors: each module already carries its own pair, and those stay in place (B3 checks that three pairs in parallel are still within the specification).</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Interface Table</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Signal</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">From → To</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Type</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Voltage</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Direction (MCU view)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Data rate</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Notes</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SDA, SCL</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO ↔ display, motion, heart rate</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3.3 V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Both</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">100 or 400 kHz bus clock</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Addresses 0x3C, 0x68, 0x57. Pull-ups: the modules' own, left fitted; none on the carrier</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">BTN\_NEXT</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SW1 → XIAO D10</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Digital</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3.3 V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">In</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Human speed</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">To ground; internal pull-up</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">BTN\_PREV</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SW2 → XIAO D9</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Digital</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3.3 V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">In</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Human speed</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">To ground; internal pull-up</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3V3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO 3V3 pin → all modules</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3.3 V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Out</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO regulator</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">BAT+, BAT−</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Protected LiPo → slide switch SW3 → XIAO pads</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3.7 V nominal</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">In</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3.7 V cell only, never 5 V. SW3's pads are on the board; switch not yet fitted</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">USB</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charger → XIAO USB-C</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">5 V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">In</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Onboard charging</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Antenna</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO → external antenna</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">RF, U.FL cable</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Both</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">WiFi, once at first boot</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No copper beneath it; keep away from the battery</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">GND</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Common to all</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Ground</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0 V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shared reference for every signal</td></tr></tbody></table>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/Schematic.png" alt="esp_watch schematic, for comparison with the block diagram above" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch schematic, for comparison with the block diagram above</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every line in the diagram should become one or more nets in the schematic. A schematic net that is missing from the diagram is either a mistake or an undocumented decision. Fix it, or add it to the diagram.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">How Busy Is the Shared Bus?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The data-rate column raises a real question for esp\_watch: three devices share one I²C bus, and one of them is a display. How much of the bus does the display use?</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Predicting a Display Update</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 1: How much data is a full screen?</strong> The display is 128 × 64 pixels, one bit per pixel.</div>

```text
128 × 64 = 8,192 pixels
8,192 bits ÷ 8 = 1,024 bytes per full screen
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: How many clock pulses does each byte take?</strong> On I²C, every byte is followed by an acknowledge bit from the receiver [1], so each byte takes 9 clock pulses.</div>

```text
1,024 bytes × 9 clocks = 9,216 clock pulses
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Teaching model:</strong> this ignores the address byte, command bytes and short gaps between transfers. They add a little.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 3: Divide by the bus clock.</div>

```text
At 100 kHz:  9,216 ÷ 100,000 = 0.092 s = 92 ms per screen
At 400 kHz:  9,216 ÷ 400,000 = 0.023 s = 23 ms per screen
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 4: Check against a real measurement.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The author measured a full screen update on esp\_watch's breadboard prototype: <strong>about 90 ms at 100 kHz</strong> (around 12 updates a second) and <strong>about 25 ms at 400 kHz</strong> (around 30 a second).</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The prediction is close at both speeds. At 100 kHz it is within the rounding of "about 90 ms". At 400 kHz it is about 10% short, because the overheads the model ignores become a bigger share when the data moves faster.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 5: What does this mean for the other devices?</strong> Suppose the display is redrawn 30 times a second at 400 kHz:</div>

```text
30 screens × 25 ms = 750 ms of every second
Bus left for the two sensors: 250 ms per second (25%)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">At 100 kHz it is worse. A full screen takes 90 ms, so the display alone cannot exceed about 11 or 12 updates a second, and at that rate the bus is almost never free for the sensors.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Compare that with what the sensors need. <strong>Example values:</strong> the heart-rate sensor producing 100 samples a second, at 6 bytes per sample in its red-plus-infrared mode [2], and the motion sensor read 50 times a second, at 6 bytes of acceleration data per read.</div>

```text
Heart rate:  100 × 6 = 600 bytes/s
Motion:       50 × 6 = 300 bytes/s
Total:                  900 bytes/s × 9 clocks = 8,100 clocks/s

At 400 kHz: 8,100 ÷ 400,000 = 2% of the bus
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The sensors need about 2% of the bus. A display redrawing constantly takes 75%. The conclusion for the architecture is clear: <strong>the display should only be redrawn when something on it changes</strong>, not on every pass through the program. That one decision, visible from a data-rate column, protects the sensors' share of the bus. You will build exactly this behaviour when you write the firmware.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What the Reference Watch Learned the Hard Way</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The voltage and notes columns catch faults that a subsystem diagram cannot show. esp\_watch hit three:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>I²C line voltage.</strong> A green MAX30102 module held the shared bus at 1.82 V instead of 3.3 V (full story in B3). Record the voltage of the module's I²C lines, not just its supply pin.</li><li style="margin:6px 0;">​<strong>Address-select pins.</strong> A floating AD0 pin made the MPU-6050 come and go between scans (see B1). The notes column should say "AD0 tied to GND", not just "0x68".</li><li style="margin:6px 0;">​<strong>Supply range.</strong> Powering the MPU-6050 module from 5 V stopped it responding. The chip is rated for about 2.4 to 3.5 V [3]. Whether a module survives 5 V depends on its own regulator, so record the chip's limits.</li></ul>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Audit an interface table.</div><div>A classmate's table has this row: SDA/SCL | MCU ↔ OLED, IMU, pulse sensor | I²C | — | Both | — | Addresses 0x3C, 0x68, 0x57.</div><div>1. <strong>Predict.</strong> Which blank or vague entries could hide a problem like the green module's?</div><div>2. <strong>Do.</strong> Rewrite the row with every column filled, and add what must be checked for each module.</div><div>3. <strong>Explain.</strong> Which column would have caught the 1.82 V problem, and which would have caught the AD0 problem?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Draw your hardware block diagram.</strong> Start from the hardware subsystems in your A1 breakdown. Draw one box per module or part, every connection including power and ground, and shared buses as shared.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Build your interface table.</strong> One row per connection, every column filled. Where you do not know a value yet, write "TBD in B3" or "TBD in B4", never leave it blank.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Check your busiest bus.</strong> Estimate the data rate of every device on it, as in the worked example. If any bus exceeds about 50% use, write down how you will reduce it: a faster clock, partial updates, fewer reads, or a second bus.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> save the block diagram and interface table in your design pack as B2-hardware-architecture.md.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open B2-hardware-architecture.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every hardware subsystem from A1 appears as at least one block. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every module and IC block has a power connection and a ground connection, in the diagram or the table. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Shared buses are drawn as one bus with several taps. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every connection in the diagram has a row in the interface table. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every row has a voltage, or "TBD" with the unit that will decide it. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Every I²C device's address is listed, with how it is set. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. No two devices on the same bus share an address. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The busiest bus has a data-rate estimate with every step shown. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A student's block diagram shows three separate lines from the microcontroller, one each to a display, a motion sensor and a heart-rate sensor, all labelled "I²C". What is wrong?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing, because each device is connected.</li><li style="margin:6px 0;">B. It hides that the three share one bus, which is the key fact for addresses, pull-ups and bus load.</li><li style="margin:6px 0;">C. I²C devices cannot share a bus.</li><li style="margin:6px 0;">D. Each line needs its own pull-up.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> One shared bus makes the shared problems visible: address conflicts, combined pull-ups and competition for bus time. <strong>A</strong> misses the point of the diagram. <strong>C</strong> is false; I²C is designed for sharing. <strong>D</strong> follows from the wrong drawing. A pull-up pair per "line" puts several pairs in parallel on one bus, which the reference watch had to remove.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A 128 × 32 display (1 bit per pixel) is sent in full over I²C at 100 kHz. Using 9 clocks per byte and ignoring overheads, how long does one update take?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. About 5 ms</li><li style="margin:6px 0;">B. About 23 ms</li><li style="margin:6px 0;">C. About 46 ms</li><li style="margin:6px 0;">D. About 92 ms</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> 128 × 32 = 4,096 bits = 512 bytes. 512 × 9 = 4,608 clocks. 4,608 ÷ 100,000 = 0.046 s. <strong>D</strong> is the time for a 128 × 64 display. <strong>B</strong> is the 128 × 64 time at 400 kHz. <strong>A</strong> is the time at 1 MHz, ten times faster than the bus in the question.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A heart-rate module works perfectly alone but, on a shared bus, makes other devices fail and pulls the idle bus voltage to 1.8 V. Which interface-table column should have flagged this in advance?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Direction</li><li style="margin:6px 0;">B. Data rate</li><li style="margin:6px 0;">C. Voltage</li><li style="margin:6px 0;">D. Signal name</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> The module's I²C lines were tied to its internal 1.8 V supply, while the bus and the other devices expected 3.3 V. A voltage entry checked against the module's actual pull-up arrangement would have caught it. <strong>A</strong> and <strong>D</strong> are correct for the module, and <strong>B</strong> has nothing to do with the voltage level of an idle bus.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> An interface table lists the motion sensor as "I²C, 0x68". On the bench, the sensor appears and disappears between scans. What note was missing?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The bus clock speed</li><li style="margin:6px 0;">B. How the address is set, for example "AD0 tied to GND"</li><li style="margin:6px 0;">C. The sensor's sample rate</li><li style="margin:6px 0;">D. The interrupt pin number</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The address depends on a pin that must be tied to a defined level. Left floating, it drifts, and so does the address. Recording how the address is set turns an easy-to-miss wiring detail into a checklist item. <strong>A</strong>, <strong>C</strong> and <strong>D</strong> are useful notes but would not explain a device that comes and goes.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> On a shared 400 kHz bus, the display is redrawn 30 times a second (25 ms each), and two sensors need about 2% of the bus. The sensors occasionally miss readings. Which change helps most?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Add a second pair of pull-up resistors.</li><li style="margin:6px 0;">B. Redraw the display only when its content changes.</li><li style="margin:6px 0;">C. Reduce the sensors' sample rate.</li><li style="margin:6px 0;">D. Slow the bus to 100 kHz.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The display uses about 75% of the bus, and redrawing only on change frees most of it. <strong>A</strong> changes the pull-ups, not bus time. <strong>C</strong> throws away data the sensors need and leaves the cause untouched. <strong>D</strong> makes every transfer four times slower, so the display would take almost the whole bus.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="B3-electrical-architecture.md">B3 — Electrical Architecture</a> you will make the decisions this unit left as "TBD": which microcontroller, how power flows, how large the pull-ups should be, and which pin carries each signal.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. NXP Semiconductors. UM10204: I²C-bus specification and user manual ("Each byte must be followed by an Acknowledge bit"). https://www.nxp.com/docs/en/user-guide/UM10204.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Analog Devices. MAX30102 datasheet (I²C addresses 0xAE/0xAF, FIFO data format: 6 bytes per sample in SpO2 mode, 3 bytes per LED channel; active-low open-drain interrupt). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. TDK. MPU-6050 detailed information (VDD supply 2.375 to 3.46 V). https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part\_no=MPU-6050</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
