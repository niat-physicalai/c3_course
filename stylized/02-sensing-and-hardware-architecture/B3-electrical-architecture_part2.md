<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 3 — Communication Buses</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Bus Voltage and Addresses</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every device on a bus must agree on two things: the <strong>voltage</strong> that means HIGH, and a unique <strong>address</strong>. You recorded both in B2's interface table. Now make sure they are consistent:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Voltage:</strong> every device on the bus should be pulled up to the same voltage, and every device must tolerate it. A 5 V module on a 3.3 V bus needs a <strong>level shifter</strong>. A module whose bus lines sit at 1.8 V internally will drag the whole bus down. esp\_watch's first heart-rate module, a green one, clamped its bus to 1.82 V, so the build uses the black module instead.</li><li style="margin:6px 0;">​<strong>Addresses:</strong> list every device's address and how it is set. Where an address depends on a pin, that pin must be tied to a defined level, never left floating.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's three addresses (0x3C, 0x57, and 0x68 with AD0 tied to ground) do not clash. B1 tells the address and clone-sensor story. the motion sensor's identity register reads 0x70 rather than the genuine part's 0x68, which marks it as a <strong>clone</strong> chip. It works correctly, but it is a reminder that cheap modules may not contain exactly what the label says.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Sizing Pull-up Resistors</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">I²C lines are <strong>open-drain</strong>: devices can only pull a line LOW. A <strong>pull-up resistor</strong> pulls it back HIGH. Its value is a trade-off:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Too large</strong>, and the line rises too slowly, because the resistor must charge the bus's capacitance. Slow edges limit the bus speed.</li><li style="margin:6px 0;">​<strong>Too small</strong>, and a device pulling the line LOW must sink too much current, and may not pull it low enough to count as a clear LOW.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The I²C specification turns both limits into formulas [2]:</div>

```text
R_min = (V_DD − V_OL) / I_OL        V_OL = 0.4 V at I_OL = 3 mA
R_max = t_r / (0.8473 × C_b)        t_r max = 1000 ns (100 kHz), 300 ns (400 kHz)
                                    C_b = total capacitance of the bus line
```

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: How Many Pull-ups Is Too Many?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Assumption:</strong> the bus capacitance is 50 pF. The real value depends on every device pin and every track, and you will estimate it more carefully during layout.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 1: The smallest allowed resistor at 3.3 V.</div>

```text
R_min = (3.3 − 0.4) / 0.003 = 967 Ω
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 2: The largest allowed resistor.</div>

```text
At 400 kHz: R_max = 300 ns / (0.8473 × 50 pF) = 7,081 Ω
At 100 kHz: R_max = 1000 ns / (0.8473 × 50 pF) = 23,604 Ω
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">So at 400 kHz, any value between about 1 kΩ and 7 kΩ is inside the specification. 4.7 kΩ sits comfortably in the middle.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 3: What happens when modules bring their own?</strong> Many breakout modules fit their own pull-ups. Three modules, each with a 4.7 kΩ pair, put three resistors in parallel on each line:</div>

```text
R_parallel = 4.7 kΩ / 3 = 1.57 kΩ
Current when a device pulls LOW: 3.3 V / 1.57 kΩ = 2.1 mA
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Add the carrier board's own pair and it becomes 4.7 / 4 = 1.18 kΩ, needing 2.8 mA. That is within a hair of the 3 mA every device must be able to sink. One more module, or one module with 2.2 kΩ pull-ups, and the bus is outside the specification.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Three pairs (1.57 kΩ) are legal on paper, but each device must now sink three times the current of a single pair (2.1 mA against 0.7 mA).</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch shows both sides of this. Its carrier board has <strong>no pull-up resistors</strong>: the three modules' own pairs stay fitted, about 1.5 kΩ in parallel. On the breadboard, with the green MAX30102 module, the bus was unreliable at 400 kHz, and the author noted the parallel pairs as one possible contributor. With the black module, the same three pairs passed at both 100 and 400 kHz. Three pairs worked; a fourth module, or a carrier pair added "to be safe", would take the bus to 1.18 kΩ and the edge of the specification.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The rule to take away: <strong>count the pull-ups on every bus before you add any.</strong> Check each module's schematic for its own pair. If the modules already give a total inside the specification, add none, as esp\_watch does. If they push it below about 1 kΩ, remove some, or fit one pair on your board instead.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 4 — Pin Allocation</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Not All Pins Are Equal</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>pin allocation map</strong> assigns every signal to a specific pin. It is not a matter of taking the next free number. Some pins have special jobs that can trap you:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Strapping pins</strong> are read at the moment the chip starts up, to decide how it starts, for example normal operation or waiting for new firmware. Anything connected to them must hold the right level at reset.</li><li style="margin:6px 0;">​<strong>Analog-capable pins</strong> are the only ones that can read a voltage with the ADC.</li><li style="margin:6px 0;">​<strong>Pins shared with a built-in function</strong>, such as the USB serial port or the boot button, may be busy at startup or during programming.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On the ESP32-C3, the strapping pins are <strong>GPIO2, GPIO8 and GPIO9</strong>, which the XIAO brings out as <strong>D0, D8 and D9</strong>. Espressif's datasheet shows that GPIO9 selects between normal start-up and download mode, that GPIO8 must be high for download mode to work, and that GPIO2 is recommended to be pulled high to avoid glitches [3]. Seeed repeats the warning for the XIAO: the wrong level on these pins can stop the board uploading or running its program [1]. The simplest safe rule, and the one esp\_watch follows, is to <strong>keep all three high at reset</strong>.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: esp\_watch's Pin Map</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">XIAO pin</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Capabilities</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">esp\_watch signal</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why this pin</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ADC1, <strong>strapping</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">not connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Left free, so nothing can pull this strapping pin low at reset</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ADC1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">not connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Free; an ADC1 pin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ADC1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">not connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Free; an ADC1 pin, so a natural home for a battery divider in a v2</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ADC2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">not connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Free, with no start-up role</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D4</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C SDA (default)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SDA</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO's default I²C pin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D5</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C SCL (default)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SCL</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO's default I²C pin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D6</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">UART TX</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">not assigned</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Left free</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D7</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">UART RX</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">not assigned</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Left free</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D8</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>strapping</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">not connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Kept high at reset (required for download mode); nothing attached that could pull it low</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D9</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>strapping</strong>, boot button</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Previous" button</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">To ground, internal pull-up. It shares the pin with the XIAO's own BOOT button, so it behaves the same way: unpressed, the watch starts normally; held during reset, it starts in download mode</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D10</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Next" button</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">To ground, internal pull-up</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The D6 and D7 functions come from Seeed's pinout [1]; esp\_watch's recorded pin map does not assign them.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch leaves D0 and D8 unconnected and puts a button on D9. A button to ground is safe on a strapping pin only if nobody presses it during reset, and D9 already carries the XIAO's BOOT button, so nothing new can go wrong there. If your design uses sensor interrupts, each one's idle level decides where it can go:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">An <strong>active-low, open-drain</strong> interrupt, like the MAX30102's [4], sits high through its pull-up and only pulls low when it has data. On a strapping pin such as D0, that pull-up would also hold the pin high at reset, which is safe.</li><li style="margin:6px 0;">An interrupt that <strong>idles low</strong>, like the MPU-6050's, would hold a strapping pin low at reset and could stop the chip starting normally. It must go on a pin with no start-up role, such as D3.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's free pins are D0–D3 and D6–D8. D0 and D8 are strapping pins, and D6 and D7 carry the debug UART. That leaves D1, D2 and D3 fully free: room for one more button or a battery divider in a v2.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For analog inputs, such as a battery divider, use ADC1 pins (D0 to D2 on the XIAO). On the ESP32-C3, Espressif no longer supports single ADC2 readings because a hardware erratum makes them unstable [7].</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/images/B3-02.svg" alt="XIAO ESP32-C3 pin map with esp_watch&#x27;s allocation and the strapping pins marked" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">XIAO ESP32-C3 pin map with esp\_watch's allocation and the strapping pins marked</div></div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Find the boot trap.</div><div>A student assigns: motion-sensor interrupt (idles low) → D9; heart-rate interrupt (open-drain with a 10 kΩ pull-up, idles high) → D3; buttons to ground → D0 and D1.</div><div>1. <strong>Predict.</strong> Will this board start up reliably?</div><div>2. <strong>Do.</strong> For each strapping pin, write the level it will sit at during reset with this allocation. Remember a button to ground reads high through its internal pull-up only after the firmware turns that pull-up on.</div><div>3. <strong>Explain.</strong> Which assignment is the problem, and what is the smallest change that fixes it?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Choose your microcontroller class.</strong> Answer the four questions in Part 1, count pins from your interface table plus 20%, and decide module or bare chip with a reason.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Draw your power tree.</strong> From every source to every load, including switches, regulators, the charger and any measurement circuit. For each switch, write what happens when it is off and USB is connected.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Build your current budget spreadsheet.</strong> One row per mode from your A2 state diagram, with the source of every number. Calculate runtime and compare with your A0 requirement. Add a duty-cycling comparison for your most power-hungry sensor.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Size your pull-ups.</strong> Estimate bus capacitance as 10 pF per device plus 10 pF for wiring (<strong>assumption</strong>). Calculate R\_min and R\_max at your bus speed. List every module's own pull-ups, work out their combined value, and state which pull-ups you keep (and whether your board adds any).</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Allocate your pins.</strong> Build a pin map like esp\_watch's, with a Why this pin column. Mark every strapping pin and state its level at reset.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> add the power tree, current budget spreadsheet and pin allocation map to your design pack as B3-electrical-architecture.md plus your spreadsheet file.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your B3 files and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The microcontroller choice states flash, RAM, pin count and radio requirements, each traced to a source. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. The pin count includes at least 20% spare. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. The power tree shows every source, switch, regulator and load. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every switch has a note of what happens when it is off with USB connected. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every row in the current budget names the source of its current figure. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Runtime is calculated and compared with the A0 battery requirement. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. R\_min and R\_max are calculated for your bus speed, with the capacitance assumption stated. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Every module's own pull-ups are listed, and the combined value on each bus is calculated and inside the specification. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. Every strapping pin is marked with its level at reset. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">10. Every analog signal is on an ADC-capable pin. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A team chooses a bare ESP32-C3 chip instead of a module to save ₹150 per unit on a 50-unit run. What is the strongest argument against this?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Bare chips cannot run Arduino code.</li><li style="margin:6px 0;">B. The team now owns the crystal, flash, RF layout and antenna design, and the radio certification that goes with them, which far outweighs ₹7,500 in total savings.</li><li style="margin:6px 0;">C. Bare chips have fewer GPIO pins.</li><li style="margin:6px 0;">D. Modules are always cheaper.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> At 50 units the saving is ₹7,500 in total, while the extra design, testing and certification work costs far more. <strong>A</strong> is false; the chip runs the same code. <strong>C</strong> is backwards; a bare chip often exposes more pins, because none are used internally. <strong>D</strong> is false at volume, where bare chips are usually cheaper per unit.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> In esp\_watch's power tree, the slide switch sits between the cell and the BAT pads. A wearer switches the watch off and plugs in USB overnight. What happens?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The battery charges normally.</li><li style="margin:6px 0;">B. The watch runs from USB, but the battery does not charge, because the switch has disconnected it from the charger.</li><li style="margin:6px 0;">C. The watch is damaged.</li><li style="margin:6px 0;">D. Nothing, because USB is ignored when the switch is off.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The switch isolates the cell from everything, including the charger. <strong>A</strong> would need the switch to be somewhere else, for example on the load side after the charger. <strong>C</strong> is wrong; nothing is overloaded. <strong>D</strong> is wrong; USB powers the XIAO directly regardless of the battery switch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A watch draws 44 mA while measuring heart rate and about 2 mA asleep. Measuring continuously gives about 5.5 hours from 240 mAh. Which change most improves runtime while still giving regular readings?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Increase the I²C speed to 400 kHz.</li><li style="margin:6px 0;">B. Measure for 30 s every 10 minutes instead of continuously.</li><li style="margin:6px 0;">C. Use a larger pull-up resistor.</li><li style="margin:6px 0;">D. Turn the display brightness down.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Duty cycling cuts sensor-on time from 24 hours to about 1.2 hours a day, taking runtime from hours to days. <strong>A</strong> barely changes energy, since bus time is a tiny part of the budget. <strong>C</strong> saves microamps at most. <strong>D</strong> helps only while the screen is on, which is a small part of the day.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A motion sensor's interrupt output idles LOW. Why must it not be connected to GPIO9 on an ESP32-C3?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. GPIO9 cannot be used as an input.</li><li style="margin:6px 0;">B. GPIO9 is a strapping pin; held LOW at reset, it puts the chip into download mode instead of running the program.</li><li style="margin:6px 0;">C. GPIO9 has no pull-up.</li><li style="margin:6px 0;">D. Interrupts only work on ADC pins.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Espressif's boot table shows GPIO9 at 0 selects download mode. A sensor holding it low at reset stops the watch starting normally. <strong>A</strong> is false; it works as an input once the chip is running. <strong>C</strong> is false; GPIO9 has a weak internal pull-up by default, but a sensor actively driving low overrides it. <strong>D</strong> is false; interrupts work on digital pins.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A battery divider uses 10 kΩ + 10 kΩ instead of 1 MΩ + 1 MΩ. What changes?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing; the ratio is the same.</li><li style="margin:6px 0;">B. The ADC voltage doubles.</li><li style="margin:6px 0;">C. It wastes 100 times more current, about 185 µA at 3.7 V, which is around 4.4 mAh a day.</li><li style="margin:6px 0;">D. It no longer needs a capacitor, and has no disadvantages.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> 3.7 V ÷ 20 kΩ = 185 µA, about 4.4 mAh a day. That is significant in a 40–87 mAh daily budget. <strong>A</strong> holds for the voltage ratio, not the current. <strong>B</strong> is false; the ratio is still one half. <strong>D</strong> is half right: smaller resistors need the capacitor less, but the constant drain is a real cost.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="B4-component-selection.md">B4 — Component Selection</a> you will choose the actual parts, deciding for each whether a ready-made module or a bare chip is the better fit, and learn to read the datasheets that decide it.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Seeed Studio. Getting Started with Seeed Studio XIAO ESP32C3 (memory, pinout table, strapping-pin warning, battery-voltage divider example, ADC full-scale note, power figures including 500 mA maximum 3.3 V output). https://wiki.seeedstudio.com/XIAO\_ESP32C3\_Getting\_Started/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. NXP Semiconductors. UM10204: I²C-bus specification and user manual (V\_OL and I\_OL limits, R\_p(min) and R\_p(max) equations, rise-time limits). https://www.nxp.com/docs/en/user-guide/UM10204.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Espressif Systems. ESP32-C3 Series Datasheet (strapping pins GPIO2, GPIO8 and GPIO9; boot-mode table). https://www.espressif.com/sites/default/files/documentation/esp32-c3\_datasheet\_en.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Analog Devices. MAX30102 datasheet (interrupt pin: active-low, open-drain). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Department of Telecommunications, Government of India. Equipment Type Approval (ETA) (certification issued by the WPC Wing for wireless equipment). https://www.eservices.dot.gov.in/equipment-type-approval-eta</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. FCC ID database. Z4T-XIAOESP32C3: Seeed Studio XIAO ESP32C3 with Bluetooth and WiFi. https://fccid.io/Z4T-XIAOESP32C3</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Espressif Systems. ESP-IDF Programming Guide (ESP32-C3): ADC Oneshot Mode Driver ("ADC2 oneshot mode is no longer supported, due to hardware limitations"). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/peripherals/adc/adc\_oneshot.html</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
