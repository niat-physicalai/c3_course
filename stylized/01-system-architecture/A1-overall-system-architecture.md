<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">A1 — Overall System Architecture</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Drawing the Whole System on One Page, and Giving Every Requirement an Owner</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 1 — System Architecture <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a context diagram, a subsystem breakdown and a requirement allocation table</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A List of Requirements Is Not Yet a Design</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">You now have a specification: numbered requirements, each with a number and a check method. It tells you what the product must achieve. It does not tell you what the product is made of, what it talks to, or which part is responsible for which requirement.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Suppose your spec asks for a semester of resting heart rate. Does that history live on the watch, a phone or a server? Each answer is a different product. If nobody asks, the requirement falls through the gap and nobody builds it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit gives you one page that shows the whole system, and a table that makes such gaps impossible to miss.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Draw</strong> a context diagram showing your product, everything outside it that it interacts with, and what flows between them.</li><li style="margin:6px 0;">​<strong>Break down</strong> your product into standard subsystems.</li><li style="margin:6px 0;">​<strong>Allocate</strong> every requirement from your specification to one owning subsystem, and find any requirement with no owner.</li><li style="margin:6px 0;">​<strong>Decide</strong> roughly where each piece of work happens (device, phone or server), and <strong>predict</strong> what the user sees when the link between them drops.</li><li style="margin:6px 0;">​<strong>Estimate</strong> how much data your product produces, and use the estimate to decide what to process on the device.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 drew systems as a chain (sensors → ESP32 → WiFi → MQTT → cloud → dashboard). New here: a boundary around your product, and a table giving every requirement an owner.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — Drawing the Boundary</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Inside and Outside</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every product has a <strong>system boundary</strong>: a line with everything you design and build on the inside, and everything you do not control on the outside.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The outside matters as much as the inside. Your watch does not design the wearer's wrist, the hostel WiFi router or the phone charger, but it depends on all of them. Each is an <strong>external actor</strong>: a person or system outside the boundary that your product exchanges something with. That something might be information, energy or physical contact.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A useful test: could I change it by editing my design files? If yes, it is inside. If no, it is outside, and your design must cope with whatever it does.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For a wrist-worn device, the external actors usually include:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">External actor</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What crosses the boundary</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The wearer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Button presses and wrist movement in; displayed information out</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The wearer's skin</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pulse signal and motion in; pressure and heat both ways</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A charger</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Electrical energy in</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A WiFi router</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Network traffic both ways</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A phone</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Data both ways, if the product uses one</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">An internet service</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Time, weather or stored history, if the product uses one</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A common mistake is to treat the phone or the server as "part of my product" without saying so. If your requirement needs an app, that app is either inside the boundary (you must design it) or outside it (someone else's app you depend on). Both are allowed. Leaving it unstated is not.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Context Diagram</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>context diagram</strong> shows your product as a single box in the centre, surrounded by its external actors, with labelled arrows for what flows between them [1]. It shows nothing inside the box yet. Its only job is to make the boundary and the outside world visible on one page.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Four rules keep it useful:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>One box for your product.</strong> Do not draw its insides here.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Every actor from your spec appears.</strong> If the spec mentions charging, a charger appears.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Every arrow is labelled with what flows</strong>, such as "heart-rate reading" or "5 V charging power", not how it travels.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Arrow direction means something.</strong> Draw a two-way arrow only if things genuinely flow both ways.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is the context diagram for the reference watch, <strong>esp\_watch</strong>. When first switched on, it connects to WiFi once to fetch the time and the weather, then keeps WiFi off. It charges over USB-C, and its heart-rate sensor on the underside of the board reads the pulse through the skin.</div>

```text
                         ┌──────────────────┐
                         │      Wearer      │
                         └───┬──────────▲───┘
     button presses          │          │  time, weather, steps,
                             ▼          │  heart rate on screen
┌──────────────┐     ┌──────────────────┴─┐     ┌──────────────┐
│ USB charger  │────►│                    │◄───►│ WiFi router  │
└──────────────┘     │     esp_watch      │     └──────┬───────┘
 charging power      │                    │  once, at  │ internet
                     └─────────▲──────────┘  first boot▼
                               │              ┌───────────────────┐
                 pulse, motion │              │ Time and weather  │
                         ┌─────┴──────┐       │ services          │
                         │ Wrist/skin │       └───────────────────┘
                         └────────────┘
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">At first boot esp\_watch sets its clock (shown in IST) and fetches the current temperature and weather code from the free <strong>Open-Meteo</strong> forecast API, then turns WiFi off.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Notice what is not in this diagram: there is no phone and no server that stores the wearer's data. That is a design decision, and in Part 2 you will see what it costs.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">You can draw your own diagram on paper and photograph it, or use a free tool such as draw.io [2].</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — Splitting the Inside into Subsystems</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Seven Standard Subsystems</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Now open the box. A <strong>subsystem</strong> is a part of the product with a clear job, one you could describe in a sentence and hand to a single person. Most connected devices can be split into the same seven:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Subsystem</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Its job</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Typical contents in a wearable</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Turn physical quantities into signals</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate sensor, motion sensor</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Processing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Run the firmware and make decisions</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Microcontroller</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Store, charge, regulate and switch energy</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery, charger, regulator, power switch</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connectivity</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Exchange data with the outside</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">WiFi or Bluetooth radio and antenna</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Local user interface</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Let the wearer see and control it</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Display, buttons</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Enclosure</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hold, protect and present everything</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Case, strap, sensor window</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Backend</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Store and process data away from the device</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Phone app, server, cloud database</td></tr></tbody></table>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>These seven are a starting point, not a law. A product with a motor would add an "actuation" subsystem. A very simple product might merge connectivity into processing. Use the list to make sure nothing is forgotten, then adjust it to fit your product.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two of these are regularly forgotten. The <strong>enclosure</strong> is treated as "the box it goes in later", yet it decides whether the heart-rate sensor touches the skin. The <strong>backend</strong> is forgotten because it is not on the circuit board. If a requirement needs data to outlive the device, or to be seen somewhere other than the wrist, a backend exists whether you drew it or not.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Reference Watch, Broken Down</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is esp\_watch split into the seven subsystems:</div>

```text
┌──────────────────────────── esp_watch ─────────────────────────────┐
│                                                                     │
│  SENSING                 PROCESSING              LOCAL UI           │
│  MAX30102 heart rate ──► XIAO ESP32-C3 ────────► SSD1306 display    │
│  MPU-6050 motion ──────► (firmware)    ◄──────── 2 buttons          │
│        (shared I²C bus)       │                                     │
│                               │                                     │
│  POWER                        │                 CONNECTIVITY        │
│  LiPo cell ─► slide switch ─► │ ◄─────────────► WiFi radio on the   │
│  charger + 3.3 V regulator    │                 XIAO, external      │
│  (on the XIAO); protected cell│                 antenna             │
│                                                                     │
│  ENCLOSURE: 3D-printed case, lid with 4 openings, sensor underneath │
└─────────────────────────────────────────────────────────────────────┘
   BACKEND: none of its own. Uses public time and weather services.
```

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_top.png" alt="esp_watch circuit board, top view: the display, motion sensor, ESP32-C3 board, buttons and power switch" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch circuit board, top view: the display, motion sensor, ESP32-C3 board, buttons and power switch</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In the render you can see sensing, processing, local UI and power. Connectivity is mostly inside the ESP32-C3 board, with the antenna on a cable. The enclosure and backend do not appear, so a photo cannot replace the diagram.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Allocating Every Requirement</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>requirement allocation table</strong> lists every requirement in your spec and names the subsystem that <strong>owns</strong> it: the one responsible if the requirement is not met. Other subsystems may <strong>support</strong> it, but only one owns it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">If two subsystems share a requirement equally, each assumes the other is handling it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Three situations need special handling:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Budget requirements.</strong> Battery life, cost, weight and thickness are not delivered by one subsystem; every subsystem uses up part of the budget. Give the owner role to the subsystem that manages the budget (power for battery life, enclosure for thickness), or to "System" when no single subsystem does, as with cost. List every subsystem that draws on it as supporting.</li><li style="margin:6px 0;">​<strong>Orphans.</strong> A requirement that no subsystem can own is an <strong>orphaned requirement</strong>. It will not be built unless you add a subsystem, change the requirement, or move it out of version 1.</li><li style="margin:6px 0;">​<strong>Unused subsystems.</strong> A subsystem that owns or supports no requirement is either serving a requirement you forgot to write, or it is unnecessary. Either way, write down which.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Holding esp\_watch Against a Problem Statement</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">We will test esp\_watch against the hostel problem statement from A0: "Hostel students cannot easily see how active they are, or how their resting heart rate changes through a semester." esp\_watch was not designed for this exact statement, so this is a fair test of what the method reveals.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: List the requirements.</strong> These are <strong>example values</strong>, a short spec for the problem statement:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">ID</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Requirement</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-01</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Show the time of day</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-02</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Show heart rate on request, 40–180 bpm</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-03</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Count steps during the day</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-04</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Show how resting heart rate has changed over the semester</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-01</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart rate within ±5 bpm, wearer sitting still</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-03</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">≥ 2 days between charges with usage pattern UP-1</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-04</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charge from a USB-C phone charger</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-07</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Total thickness ≤ 16 mm including the case</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 2: Give each requirement an owner, and list its supporters.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">ID</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Owner</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Supporting</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How esp\_watch meets it</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-01</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Processing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connectivity, Local UI</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Firmware keeps time; WiFi sets it once at first boot</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-02</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Processing, Local UI, Enclosure</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MAX30102 on the underside; firmware calculates bpm</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-03</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Processing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MPU-6050 motion sensor; firmware counts steps</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-04</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>none</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Orphan.</strong> Nothing stores readings across a semester</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-01</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Enclosure</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Needs firm skin contact and blocked outside light</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-03</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">every subsystem</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sleep current dominates (see A0)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-04</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Enclosure</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">USB-C on the XIAO, reached from the left side of the case</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-07</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Enclosure</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensing, Processing, Local UI, Power</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Board alone is 14.044 mm high, leaving ~2 mm for the case</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Look for orphans.</strong> FR-04 has no owner. To show a semester's trend, readings must be stored for months and then displayed as a trend. esp\_watch has no storage subsystem for history and no backend. The requirement is the heart of the problem statement, and nothing in the design delivers it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">There are three honest ways out:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Add a backend</strong>, such as a phone app or a server that the watch uploads to.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Make processing own it</strong>: store a few bytes per day in the watch's own memory and draw a simple trend on the display.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Move it out of version 1</strong>, and say so in the spec, accepting that version 1 only partly solves the problem.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The best choice depends on how much data is involved (Part 3).</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 4: Look for unused subsystems.</strong> Connectivity supports only FR-01, setting the clock. esp\_watch also fetches the weather, but no requirement in this spec asks for weather. So either a requirement is missing, or part of the connectivity work serves nothing in this problem statement.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> 9 requirements: 8 with owners, 1 orphan. Every existing subsystem appears at least once.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">NFR-07 is also in trouble. The board stack leaves about 2 mm for the whole case (E2 covers the stack). The enclosure owns a number it cannot meet, so the fix lies with the subsystems that spend the budget.</div>

---

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:center;line-height:1.7;"><div style="font-weight:700;color:#1e40af;">This cookbook will be continued in Part 2.</div></div>
