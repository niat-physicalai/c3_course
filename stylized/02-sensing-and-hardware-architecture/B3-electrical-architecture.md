<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">B3 — Electrical Architecture: MCU, Power, Buses and Pins</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Big Electrical Decisions, Made Before Any Part Is Chosen</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 2 — Sensing and Hardware Architecture <strong>Time:</strong> ~2 hours · <strong>You will produce:</strong> a power tree, a current budget spreadsheet and a pin allocation map</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Four Decisions That Are Expensive to Change Later</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Your block diagram from B2 still has gaps marked "TBD". Which microcontroller? Where does power come from, and how does it reach each part? How big are the pull-up resistors? Which pin does each signal use?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each choice locks in others. Too few pins, and the last sensor has nowhere to go. A switch in the wrong place, and the battery cannot charge. An interrupt on a strapping pin, and the board may not start. All are painful to fix once the board exists.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Select</strong> a microcontroller class from your requirements: memory, pins, radio, and module versus bare chip.</li><li style="margin:6px 0;">​<strong>Draw</strong> a power tree from charger to every load, and <strong>identify</strong> what each switch and regulator does.</li><li style="margin:6px 0;">​<strong>Calculate</strong> a current budget per operating mode, and show how duty cycling changes battery life.</li><li style="margin:6px 0;">​<strong>Size</strong> I²C pull-up resistors from the bus specification, including the effect of several modules' pull-ups in parallel.</li><li style="margin:6px 0;">​<strong>Produce</strong> a pin allocation map that avoids boot pins and puts analog signals on suitable pins.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 covered dividers, GPIO, ADC and I²C. What is new here is making these choices for a whole board before the schematic starts.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — Choosing the Microcontroller Class</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Do You Actually Need?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Choose a <strong>class</strong> of microcontroller first, and a specific part later. The class is defined by four questions, and your spec and interface table already contain the answers.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Question</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where the answer comes from</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How much program memory (flash) and working memory (RAM)?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Firmware size, display buffer, data you store (A1's data estimate)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How many pins, and of what kinds?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your B2 interface table: count digital, analog and bus pins</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Does it need a radio, and which?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your A1 connection choice</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Module or bare chip?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your team's ability to design RF circuits, and your certification budget</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Count pins from the interface table, not from memory. Add about 20% spare, because designs grow and a debug pin is priceless later.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Module or Bare Chip?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>bare chip</strong> is the microcontroller alone. A <strong>module</strong> carries the chip plus its crystal, flash, regulator and antenna or antenna connector. For a first product, choose a module. A device that transmits radio needs government approval before it can be sold in India [5], and a pre-certified module saves you most of that work. B4 compares the two in full.: a crystal, flash memory, a regulator, and usually an antenna or antenna connector.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The difference shows up clearly in schematic symbols. The bare ESP32-C3 chip has pins for an external crystal, external SPI flash and an antenna input (LNA\_IN). A module has none of these on its edge, because they are already inside.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;"></th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Module</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Bare chip</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Design effort</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Low: power, ground and signals</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">High: crystal, flash, RF matching and antenna layout</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Radio certification</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Module maker has often certified the module</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">You certify your own design</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Unit cost at volume</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Higher</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lower</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Board area and height</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">More</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Less</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hand soldering</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Often possible</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Usually needs reflow</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The certification row settles it for a first product: a device that transmits radio needs government approval before it can be sold in India [5], and a pre-certified module saves you most of that work.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch uses the <strong>Seeed Studio XIAO ESP32-C3</strong>: a small module-style board with a 32-bit RISC-V processor, WiFi and Bluetooth, 400 KB of SRAM and 4 MB of flash [1]. It exposes 11 pins labelled D0 to D10, a USB-C port, battery pads and a U.FL connector for an external antenna. esp\_watch's interface table needs only four signal pins: two for I²C and two buttons. Both sensors are polled over I²C, so their interrupt pins are not wired, and the watch does not measure its battery. Four of eleven leaves seven spare, but several come with restrictions, as Part 4 shows.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The XIAO ESP32-C3 itself carries an FCC certification (FCC ID Z4T-XIAOESP32C3), and Seeed publishes its CE and other certificates [6]. That is the work a module saves you.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — Power Architecture</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Power Tree</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>power tree</strong> shows every source of energy, every conversion and every switch, down to every load. Draw it before choosing any power part.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is esp\_watch's power tree:</div>

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
                              slide switch (SW3)   ├──► ESP32-C3 (internal)
                                            │          ├──► SSD1306 display
                         protected LiPo cell 3.7 V     ├──► MPU-6050 motion sensor
                                                       └──► MAX30102 heart rate
                                                            (each module carries its own I²C pull-ups)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Three things in this tree are design decisions worth examining.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The charger and regulator are on the XIAO.</strong> No external charger was needed. The BAT pads accept a 3.7 V lithium cell only, never 5 V, and the onboard regulator holds 3.3 V as the cell voltage falls.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The slide switch sits between the cell and the BAT pads.</strong> (On the built board its pads are in place; the switch itself is still to be fitted.) When the switch is off, the cell is disconnected from everything, including the charger. So plugging in USB with the switch off runs the watch from USB but <strong>cannot charge the battery</strong>. That may be acceptable, but it must be a known behaviour, written in the user instructions, not a surprise.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>There is no battery measurement.</strong> The XIAO handles charging, and the cell is a <strong>protected</strong> LiPo with its own cut-off circuit, so esp\_watch does not add a battery-sense divider. The cost of that choice: the firmware cannot show a battery level or warn before the cell cuts off.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Is the regulator big enough? Seeed lists a maximum 3.3 V output current of <strong>500 mA</strong> with the battery input at 3.8 V [1]. The largest modelled load on esp\_watch is a WiFi burst averaging about 100 mA. Radio transmissions draw short peaks above their average, so the margin matters, but 500 mA leaves plenty.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">If Your Product Needs a Battery Level: a Divider</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch does without one, but many battery products show a battery level. The XIAO has no pin for measuring its own battery, so you would add one: <strong>example values</strong> are two 1 MΩ resistors in series across the battery, with the midpoint on an ADC pin and a 100 nF capacitor from the midpoint to ground. Seeed's own documentation describes the same approach, halving the battery voltage so the ADC can read it [1].</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Checking the Divider</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 1: Will the ADC voltage stay in range?</strong> A fully charged lithium cell is typically about 4.2 V (<strong>assumption</strong>, typical for this chemistry). The divider halves it:</div>

```text
V_adc = 4.2 V × 1 MΩ / (1 MΩ + 1 MΩ) = 2.1 V
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Seeed notes a nominal full-scale ADC reading of 2,500 mV on this board, varying by about ±10% from chip to chip [1]. The worst case is 2,500 × 0.9 = 2,250 mV, which is still above 2.1 V. It fits.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 2: How much current does it waste?</div>

```text
I = 3.7 V / (1 MΩ + 1 MΩ) = 1.85 µA
Per day: 1.85 µA × 24 h = 44 µAh = 0.044 mAh
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Against a daily budget of 40–87 mAh (from A0), this is under 0.1%. Large resistors were the right choice.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Why the capacitor?</strong> Large resistors come with a catch. When the ADC takes a sample, it briefly draws current to charge its own internal sampling capacitor. Through 500 kΩ (the two resistors seen in parallel from the midpoint), that charge arrives too slowly and the reading comes out low. The 100 nF capacitor holds a small reservoir of charge right at the pin, so the ADC samples from the capacitor rather than through the resistors.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Because the ADC's full scale varies ±10% between chips, calibrate the firmware against a known voltage rather than trusting the nominal scale.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Current Budget</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>current budget</strong> lists every operating mode, the current in each, and how long the device spends there. You met a simple version in A0. Here it becomes a spreadsheet you maintain for the rest of the course.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's figures come from a power model, <strong>not from measurement</strong>. No current was ever measured on the reference watch.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Mode</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Current (modelled)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Power at 3.7 V</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Screen on, WiFi connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">~36 mA</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">~135 mW</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate measurement</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">~44 mA</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">~165 mW</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">WiFi sync burst</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">~100 mA average</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">~370 mW</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Optimised idle (light sleep + BLE)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1–3 mA</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">4–10 mW</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Seeed's published figures for the XIAO board alone: active below 75 mA, modem-sleep below 25 mA, light sleep below 4 mA, deep sleep about 44 µA [1].</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/images/B3-01.png" alt="The Power Budget sheet of esp32c3_watch_bom_power.xlsx: current for each block in each operating state, with its source, and Seeed&#x27;s published XIAO figures for comparison" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Power Budget sheet of esp32c3\_watch\_bom\_power.xlsx: current for each block in each operating state, with its source, and Seeed's published XIAO figures for comparison</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Hours or Days? Duty Cycling the Heart-Rate Sensor</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Heart-rate measurement is the largest regular load in esp\_watch's model (44 mA). How often you measure decides whether the battery lasts hours or days.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Use esp\_watch's modelled figures and its 300 mAh cell, 80% usable, so 240 mAh.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Case 1: Measure continuously.</div>

```text
44 mA × 24 h = 1,056 mAh per day
Runtime: 240 mAh ÷ 44 mA = 5.5 hours
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Case 2: Measure for 30 s every 10 minutes</strong> (144 times a day). <strong>Assumption:</strong> the screen stays off during these background readings; the wearer still wakes the screen 50 times a day for 30 s.</div>

```text
Heart rate: 144 × 30 s = 4,320 s = 1.2 h   × 44 mA = 52.8 mAh
Screen:      50 × 30 s = 1,500 s = 0.417 h × 36 mA = 15.0 mAh
Sleep:      24 − 1.2 − 0.417     = 22.38 h × 1 mA  = 22.4 mAh  (best)
                                            × 3 mA  = 67.1 mAh  (worst)
Per day:                                    90.2 mAh (best)  134.9 mAh (worst)
Runtime:    240 ÷ 90.2 = 2.7 days          240 ÷ 134.9 = 1.8 days
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Case 3: Measure only when asked</strong>, 5 times a day, which is A0's usage pattern UP-1: <strong>2.7 to 6.0 days</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The same hardware lasts about 5 hours, about 2 days, or up to about 6 days, depending only on how often the firmware turns on the sensor. The electrical architecture sets the ceiling; the firmware decides how close you get to it. That is why the current budget must be written per mode, not as one number.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Start the spreadsheet for activity 3 from this template. Give a source for every figure.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>1. <strong>Predict.</strong> Which mode will dominate your daily total?</div><div>2. <strong>Do.</strong> Fill one row per mode from your A2 state diagram. Use datasheet or module figures, and write where each number came from in the Source column. Add a sleep row for the rest of the day. Sum mAh per day, then divide your usable battery capacity by it.</div><div>3. <strong>Explain.</strong> Was your prediction right? Does your runtime meet your A0 battery requirement?</div><div>​<strong>Extra challenge:</strong> Add a column for a worst case that uses the highest datasheet figure for each mode. Does the requirement still hold?</div></div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A starting template you can paste into any spreadsheet:</div>

```text
Mode,Current_mA,Times_per_day,Duration_s,Hours_per_day,mAh_per_day,Source
Screen on,36,50,30,=C2*D2/3600,=B2*E2,modelled (esp_watch)
Heart rate,44,5,30,=C3*D3/3600,=B3*E3,modelled (esp_watch)
Sleep,2,1,,=24-E2-E3,=B4*E4,modelled mid-range
Total,,,,,=SUM(F2:F4),
Usable capacity mAh,240,,,,,300 mAh x 0.8
Runtime days,=B6/F5,,,,,
```

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Decoupling and Protection</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two more items belong in the power architecture.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Decoupling capacitors</strong> sit right next to each chip's supply pins and supply the sudden bursts of current a chip draws when it switches. A common starting point is a 100 nF capacitor at every supply pin, plus a larger bulk capacitor where power enters the board. With modules, the question changes: most breakout modules already carry their own decoupling, so your job is to check each module's schematic rather than add capacitors by habit.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's carrier board adds <strong>no</strong> decoupling capacitors of its own. Every part on it is a module, and each module carries its own capacitors next to its chip.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Protection</strong> means deciding what happens when something goes wrong electrically:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Risk</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Typical protection</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where it can live</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery drained too far</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cut off below a safe voltage</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cell's own protection circuit, charger, or firmware using the battery-sense pin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery connected backwards</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Keyed connector, or a protection device</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connector choice, carrier board</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">USB and battery both connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power-path switching</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charger or module</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Static discharge through buttons or port</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ESD protection parts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Carrier board</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Seeed states that the XIAO ESP32-C3 can stay connected to USB while running from the battery, because of a protection chip on the board. With no battery measurement, esp\_watch relies on the protected cell's own cut-off: when the cell is flat, the watch simply stops, which is the hard stop recorded in A2's failure table.</div>

---

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:center;line-height:1.7;"><div style="font-weight:700;color:#1e40af;">This cookbook will be continued in Part 2.</div></div>
