<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">B1 — Talking to Sensors: Choosing the Interface</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Picking I²C, SPI, UART or Analog for Each Part, and Saying Why</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 2 — Sensing and Hardware Architecture <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> an interface comparison table and a justified interface choice for each peripheral</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Display Is Using Most of the Bus. Should It Move?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's display, redrawn 30 times a second over I²C at 400 kHz, would take about 75% of the bus (you will check that sum yourself in B2), leaving the two sensors to share the rest. You can buy the same 0.96-inch SSD1306 display in a version with an SPI connection. SPI is much faster. Should esp\_watch have used it?</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Compare</strong> I²C, SPI, UART, analog and pulse interfaces on pins, speed, device count, distance and failure modes.</li><li style="margin:6px 0;">​<strong>Calculate</strong> how long a transfer takes on each interface, and what that means for a shared bus.</li><li style="margin:6px 0;">​<strong>Select</strong> an interface for each peripheral, and <strong>justify</strong> it from your pin budget and data rates.</li><li style="margin:6px 0;">​<strong>Diagnose</strong> the common interface faults: wrong pull-ups, address clashes, baud mismatches and a missing common ground.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 taught how I²C, SPI and UART work. Here you choose between them under a full pin budget, and write down a reason for each choice.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Interfaces Side by Side</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;"></th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">I²C</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">SPI</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">UART</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Analog (ADC)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Pulse / one-wire</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Wires (plus ground)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2, shared by all devices</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3 shared + 1 chip select per device</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2 per device (TX, RX)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1 per signal</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1 per device</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Devices per connection</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Many, by address</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Many, by chip select</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">One</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">One</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">One (or a few, for one-wire buses)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Typical speed</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">100 or 400 kHz</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Several MHz</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">9,600 to 115,200 baud is common</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Limited by the ADC and filtering</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Depends on the protocol</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Needs pull-ups</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Often</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Can read back from the device</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Usually; some devices are write-only</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Typical distance</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Centimetres, on one board</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Centimetres</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Metres</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Short; noise-sensitive</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Varies</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Typical parts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensors, small displays, clocks</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fast displays, memory, fast sensors</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">GPS, modems, self-contained modules</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Potentiometers, simple light or temperature sensors, battery sense</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Some temperature sensors, ultrasonic distance</td></tr></tbody></table>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>These are typical values to help you compare, not limits. Some I²C devices run faster, some UARTs much faster, and an analog signal's usable speed depends on the sensor as much as the ADC. The datasheets of your actual parts decide.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Three ideas from this table matter more than the rest.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Pins cost more than speed on a small board.</strong> esp\_watch uses every pin it can safely spare (B3 builds its full pin budget). An interface that needs four pins where another needs zero extra is often decided by the pin budget before speed even comes into it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Sharing is both the strength and the weakness of a bus.</strong> I²C lets many devices share two wires, but they then share the bus time, the pull-ups and the fate of the bus: one faulty device can stop all of them.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Some interfaces cannot read back.</strong> The SSD1306 datasheet states that in its serial (SPI) mode "only write operations are allowed" [1]. That matches a lesson esp\_watch learned the hard way (below): if you can only write to a device, you cannot use it to check that the connection works.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Should esp\_watch's Display Move to SPI?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: What does SPI need?</strong> In 4-wire SPI mode the SSD1306 uses a clock (SCLK), data in (SDIN), chip select (CS#) and data/command select (D/C#), plus a reset line (RES#) [1]. That is 4 to 5 microcontroller pins, depending on whether reset is tied to the microcontroller or wired separately.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: How fast would it be?</strong> The datasheet's minimum clock cycle for SPI is 100 ns [1], so up to 10 MHz.</div>

```text
One full screen: 1,024 bytes × 8 bits = 8,192 bits
At 10 MHz: 8,192 ÷ 10,000,000 = 0.82 ms
On I²C at 400 kHz (measured on esp_watch): about 25 ms
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">SPI would be about 30 times faster, and it would take the display off the I²C bus entirely, leaving the sensors the whole of it.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 3: Can the pin budget pay for it?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch uses only 4 of the XIAO's 11 pins: SDA, SCL and the two buttons. Neither sensor's interrupt is wired, and there is no battery-sense pin. So pins are free, but look at which ones: D1, D2 and D3 are clear, D0 and D8 are strapping pins that must be high at reset (D9, the third, already carries a button), and D6/D7 are the UART used for debugging. Four or five SPI lines would need at least one strapping pin or the debug UART.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">So the budget can pay, but only by driving strapping pins (which must not be held low at reset) or giving up the debug UART. Possible, with care.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 4: Is there a cheaper fix for the real problem?</strong> The real problem was bus time, not bus speed. Redrawing the display only when something changes removes most of its bus use (B2 and D2 show how). That costs no pins and no hardware.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> SPI is faster and esp\_watch could just about find the pins, but the problem it would solve has a free firmware fix. <strong>Conclusion: keep the display on I²C and redraw on change.</strong> For a product with a bigger microcontroller, or animations that genuinely need 30 frames a second, the answer could reasonably be the opposite. Writing down the reasoning, not just the result, is what lets someone make that call later.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Choosing, Peripheral by Peripheral</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For each peripheral, ask these questions in order:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>What does the part offer?</strong> Many sensors only have one interface. If so, the choice is made, and your job is to fit it in.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>How many pins can you spend?</strong> Count your MCU's free pins now; B3 turns this into a full pin budget.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>How much data, how often?</strong> Estimate bytes per second: bytes per reading × readings per second.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>How many devices will share the connection?</strong> Check addresses on I²C, chip selects on SPI.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>How far does the signal travel?</strong> Across a 39 mm board, anything works. Down a cable, UART or a differential interface may be needed.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. <strong>How does it fail, and can you detect it?</strong> A2's failure table needs an answer for each.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's choices, justified:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Peripheral</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Interface</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Watch out for</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MAX30102 heart rate</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C (0x57)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Only I²C is offered [2]. The module also has an interrupt pin, but esp\_watch leaves it unconnected and polls the sensor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Module's pull-up voltage (the green module's 1.8 V problem)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MPU-6050 motion</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C (0x68)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C is what the module exposes and the data rate is tiny; its interrupt pin is left unconnected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">AD0 must be tied to a defined level</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SSD1306 display</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C (0x3C)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shares the bus with no extra pins; redrawing only on change would fix the bus-time problem</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Writes cannot confirm the bus works</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Buttons</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Digital input, internal pull-up</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Simplest possible, one pin each</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Switch bounce</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Analog (ADC1) through a divider</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A voltage is exactly what needs measuring</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Chip-to-chip ADC variation; settling time</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">One point about the ESP32-C3 makes the I²C column worth thinking about. Its datasheet lists a single I²C interface [3]. Everything on esp\_watch's I²C bus shares one controller, so a second I²C bus, a common fix for address clashes or overloaded buses on larger chips, is not a simple option here.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/images/B1-01.svg" alt="The same display, wired two ways: I²C (2 shared wires) versus 4-wire SPI (4–5 dedicated wires)" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The same display, wired two ways: I²C (2 shared wires) versus 4-wire SPI (4–5 dedicated wires)</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">When Interfaces Fail</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Most interface faults come down to a handful of causes. Learn to recognise them from their symptoms:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Symptom</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Likely cause</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How to confirm</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C device missing from a scan, or appearing and disappearing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Address pin floating; device unpowered; wrong address</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Scan repeatedly; check how the address pin is set</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Two devices "on" one address, garbled reads</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Address clash</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Scan with one device removed; check both datasheets</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I²C works at 100 kHz, fails at 400 kHz</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pull-ups too weak for the capacitance, or too many in parallel</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Calculate rise time (taught in B3; simulated in B5)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">UART output is random characters</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Baud-rate mismatch</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Try the other side's rate; check both settings</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">UART silent</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">TX connected to TX instead of RX</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Swap the two lines</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Everything behaves oddly, readings drift</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Missing common ground between two powered boards</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check a ground wire joins every board</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SPI device ignores commands</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Chip select not driven, or wrong SPI mode</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check chip select goes low during a transfer</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Analog reading jumps around</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Floating input, or a high-impedance source without a capacitor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check the source; add filtering</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's bench testing with the author's <a href="https://github.com/niat-physicalai/esp_watch/blob/main/firmware/PlatformIO/esp_watch/src/i2c_debug.cpp">i2c\_debug</a> sketch produced two of these:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Floating address pin</strong>: with the motion sensor's AD0 unconnected, it appeared and disappeared between scans, with 6% to 80% of reads failing.</li><li style="margin:6px 0;">​<strong>Floating analog inputs</strong>: unconnected ADC pins read <strong>142 mV</strong>. That was not a bus voltage, just an artefact of an input connected to nothing. It is a useful reminder that an analog reading from a floating pin looks like data.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">One fault fits no row: a write-only display can hide a broken bus, because nothing is read back from it (the full story is in D5). The author's rule: <strong>judge the bus by a device you read from.</strong></div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Read the symptoms.</div><div>For each report, name the most likely cause and the one check you would make first.</div><div>1. <strong>Predict.</strong> Before reading the table again, guess each cause.</div><div>2. <strong>Do.</strong> (a) "The GPS module prints ÿÿÿ characters." (b) "The pressure sensor shows up in the scan at 0x76 on some boots and not others." (c) "My two sensors both answer at 0x68 and the readings make no sense." (d) "The sensor board works on the bench but gives drifting readings when powered from a separate battery pack."</div><div>3. <strong>Explain.</strong> Which of these could you catch in Wokwi, and which only on real hardware?</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">(a) Baud-rate mismatch: check both baud settings. (b) Floating address pin: check how the address pin is tied. (c) Address clash: check whether either device has an alternative address. (d) Missing common ground between the two supplies: check that a ground wire joins them. Wokwi could catch (a), since both baud rates are set in code you can see, and (c), since two parts with one address appear in the simulator's bus. (b) and (d) are electrical effects that Wokwi's digital model does not include.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Build your interface comparison table.</strong> For each interface your parts could use, fill in pins, device count, speed, pull-ups, read-back and main failure mode, from your parts' datasheets rather than the typical values above.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Justify each peripheral.</strong> One row per peripheral: interface, the reason in terms of pins, data rate and sharing, and what to watch out for. Where a part offers only one interface, say so.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Check your busiest connection.</strong> Estimate its load at your chosen speed: bytes per second × bits per byte ÷ bus speed. Use 9 for I²C and 10 for UART. If the load is over about 50%, record your fix.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Plan for failure.</strong> For each interface, write how the firmware will detect a fault, linking back to your A2 failure table. For any write-only device, name the device on the same bus you will use to check the bus's health.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> add the comparison table and per-peripheral justifications to your design pack as B1-interfaces.md.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open B1-interfaces.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every peripheral has an interface and a written reason. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every reason refers to at least one of: pins, data rate, device count, distance, or what the part offers. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. The total pin use fits within your MCU's free pins. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every I²C device has an address and a note of how it is set. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. No two devices on one bus share an address. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The busiest connection has a load estimate at its chosen speed. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Every interface has a detection method for faults. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Every write-only device has a named read-back device on the same bus for health checks. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A watch has two spare GPIO pins. Its display is on I²C and uses 70% of the bus through constant redraws. What is the best first step?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Move the display to SPI.</li><li style="margin:6px 0;">B. Redraw the display only when its content changes.</li><li style="margin:6px 0;">C. Add a second I²C controller.</li><li style="margin:6px 0;">D. Lower the bus speed to 100 kHz.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> It removes most of the load with no pins or hardware. <strong>A</strong> needs 4 to 5 pins, and there are only 2. <strong>C</strong> is not available on a chip with a single I²C interface, such as the ESP32-C3. <strong>D</strong> makes every transfer four times longer, which makes the load worse.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> Two SPI devices share SCLK, MOSI and MISO. Reading device A works alone, but returns garbage once device B is connected. B's chip-select pin is not connected to anything. What is the most likely cause?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. B's chip select floats low, so B drives MISO at the same time as A.</li><li style="margin:6px 0;">B. SCLK has no pull-up resistor.</li><li style="margin:6px 0;">C. A and B have the same address.</li><li style="margin:6px 0;">D. A baud-rate mismatch between A and the microcontroller.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> Any SPI device whose chip select is low drives the shared MISO line. A floating chip select lets B answer over A. <strong>B</strong>: SPI lines need no pull-ups. <strong>C</strong> and <strong>D</strong> are I²C and UART faults, not SPI ones.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> An I²C bus carries a write-only display and a temperature sensor. Your firmware checks the bus once a minute. Which check can detect a broken bus?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Confirm the last display write returned no error.</li><li style="margin:6px 0;">B. Read the sensor's ID register and compare it with the datasheet value.</li><li style="margin:6px 0;">C. Confirm the display still shows text.</li><li style="margin:6px 0;">D. Count how many display writes were sent.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Only a read proves that data came back across the bus. <strong>A</strong> and <strong>D</strong> can pass on a broken bus: esp\_watch's display accepted writes while showing corrupted output. <strong>C</strong> needs a person watching, and corrupted output can still look like text.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Before wiring a battery divider to an ADC pin, you print that pin's reading and see about 140 mV. What should you conclude?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The pin is measuring a real voltage on the board.</li><li style="margin:6px 0;">B. The pin is floating; the value is a false reading, not a measurement.</li><li style="margin:6px 0;">C. The ADC is broken.</li><li style="margin:6px 0;">D. The battery is almost flat.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> An input connected to nothing reads whatever charge and noise are on it. esp\_watch's floating ADC pins read 142 mV. <strong>A</strong> and <strong>D</strong> treat the number as data, but nothing is connected yet. <strong>C</strong> is unlikely: the ADC is behaving normally for a floating input.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A sensor offers both I²C and SPI. The product has plenty of spare pins, the sensor needs 20 kB per second, and the I²C bus already carries a display. Which choice is best supported?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. I²C, because it uses fewer wires.</li><li style="margin:6px 0;">B. SPI, because pins are available, the data rate is high, and it keeps the load off the already busy I²C bus.</li><li style="margin:6px 0;">C. UART, because it is simplest.</li><li style="margin:6px 0;">D. Analog, because it needs only one pin.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> 20 kB per second is 180,000 I²C clocks per second, nearly half of a 400 kHz bus by itself. With pins to spare, SPI takes that load away. <strong>A</strong> optimises the wrong constraint here. <strong>C</strong> is not offered by the sensor. <strong>D</strong> does not apply to a digital sensor.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="B2-hardware-architecture.md">B2 — Hardware Architecture</a> you will turn your sensors and interfaces into a block diagram and an interface table, the drawing a schematic is built from.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Solomon Systech. SSD1306 datasheet, hosted by Adafruit (4-wire SPI pins SCLK, SDIN, CS#, D/C#, RES#; SPI clock cycle time minimum 100 ns; "Under serial mode, only write operations are allowed"; I²C addresses 0111100/0111101). https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Analog Devices. MAX30102 datasheet (I²C interface; open-drain interrupt). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Espressif Systems. ESP32-C3 Series Datasheet (connectivity interfaces: two UARTs, three SPI, one I²C; I²C standard mode 100 kbit/s and fast mode 400 kbit/s). https://www.espressif.com/sites/default/files/documentation/esp32-c3\_datasheet\_en.pdf</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
