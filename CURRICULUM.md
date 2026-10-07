# C3 — From Problem Statement to Manufacturable Design

**Format:** self-paced, online. **Nominal effort:** ~38.5 hrs, no hard cap.

**Purpose (author, 2026-10-06):** the course takes a student from a breadboard proof of concept to a product-ready design: a real PCB, an enclosure built around it, a BOM and a manufacturing package. Students will **come back to it as a reference** when they build their own product later in the programme, so the tool chapters show the bare minimum needed to make one board and one enclosure, step by step, on esp_watch. Hands-on work stays on the laptop (system architecture, brainstorming, BOM, schematic, PCB, CAD). Finishing the course never requires building anything physical.

**What students produce:** not a physical device — a complete, review-ready **design pack** they could hand to a fab house tomorrow. That pack becomes the input to their funded build later.

**Explicitly out of scope:** soldering, PCB fabrication, assembly, 3D printing, bring-up. Manufacturing is taught as *"what you must produce, where you'd send it, and what it would cost"* — the workflow stops at the sliced/quoted stage. Physical breadboard prototyping and 3D printing are part of the wider programme, not of this course — students do them later, during the funded build/competition, on the design this course produces.

**Reference product:** a custom **ESP32-C3 smart watch**, built by the course author — repository: [`niat-physicalai/esp_watch`](https://github.com/niat-physicalai/esp_watch). A Seeed Studio XIAO ESP32-C3 carries a MAX30102 heart-rate/SpO2 sensor, an MPU-6050 six-axis IMU and a 0.96" SSD1306 OLED on a custom carrier PCB, with two user buttons, a power slide switch and a LiPo cell. It was designed in KiCad — with hand-drawn schematic symbols for all three peripherals and a hand-drawn SMD footprint for the MAX30102 module — fabricated by JLCPCB via their KiCad export plugin, hand-soldered and tested. The enclosure is modelled in **Onshape** (almost complete). The course teaches **Fusion 360**, and tells students the reference was built in Onshape because the concepts transfer directly.

**How the reference is used:** esp_watch is an **example**, not a project students build. Units use it wherever a concept needs a real example (a pull-up, an I²C address, a footprint, a DRC run) and to show the process a real product went through: spec → breadboard → schematic → PCB → DRC → DFM → order → power probe → solder → firmware test on the PCB. Units do not need to cover every detail of the watch.

Because it is the author's own design, students get the real schematic, the real board file and the real fabrication package with no licensing constraint. The real JLCPCB order is recorded too: 5 boards, $4 fabrication, $24.68 shipping, $18.68 paid after a $10 discount. Students also get something no public reference design offers: an honest account of what went wrong. The design contains at least one formally obsolete component and at least one decision worth arguing with. Both are taught openly.

> **Naming note:** the courses in this series are referred to throughout as **Part 1 / Part 2 / Part 3**, not C1/C2/C3, because unit IDs inside this document also use letters (Module 03 units are C0, C1, C2…).

> **Terminology:** this document's **Sections** become **Modules** on the platform (one folder each); its **units** (A0, B1…) become one `.md` reading file each.

> **Learning flow (restructured 2026-09-29):** decide *what* the product is (A), decide what to sense and design the circuit (B), give it a shape and a board (C), write the firmware (D), design the enclosure (E), then prepare it for manufacture (F) and assemble the pack (G). Sensor and interface choice now come before component selection, and the form-factor concept now comes before PCB layout.

**Effort by section:**

| Section | Topic | Hrs |
|---|---|---|
| A | System Architecture | 3.0 |
| B | Sensing & Hardware Architecture | 8.5 |
| C | Form Factor, Schematic & PCB | 6.0 |
| D | Firmware | 8.0 |
| E | Mechanical / 3D Design | 8.0 |
| F | Sourcing & Manufacturing Handoff | 3.0 |
| G | Capstone | 2.0 |
| | **Total** | **38.5** |

**Unit length and assessment (author, 2026-09-29):** there are no word targets. Each unit is as long as a student needs to understand its row below and produce its deliverable, and no longer. **Every unit ends with 5–15 MCQs, scaled to the size of its topic, and a binary self-check of about 8 items.** Try-it boxes, Part headings and multi-step activity ladders are optional.

**Reference-product stories — one owner each.** A story is told in full once, in its owning unit. Every other unit points to it in one line.

| Story | Owner |
|---|---|
| Wearing position, which face touches the skin, board sides | C0 |
| AD0 floating, I²C addresses | B1 |
| Green vs black MAX30102 (1.82 V bus clamp), three pull-up pairs in parallel, strapping pins, clone MPU-6050 (WHO_AM_I 0x70) | B3 |
| Modelled current budget (example) | B3 |
| Module-vs-IC choice on every BOM line | B4 |
| Annotated I²C captures, mock sensor for simulation | B5 |
| Hand-drawn symbols | C2 |
| MAX30102 footprint from a calibrated photo; downloaded XIAO footprint | C2 |
| OLED write never fails visibly | D5 |
| Module stack height 14.044 mm | E2 |
| Interference-fit lid | E3 |
| MPU-6050 obsolescence and the ICM-42670-P alternate | F0 |
| JLCPCB plugin fabrication zip | F1 |
| Routing, ground pour, antenna keep-out and DRC on the real board | C3 |

---

## 0. Prerequisites

Publish these upfront with a **20-question entry diagnostic (70% to proceed)** and a remediation link per topic. Don't gate access on it — gate *confidence* on it.

### Carried from Parts 1 and 2

**Part 1 (Applied IoT)** is a broad course and Part 3 leans on it heavily. Students are assumed to arrive already able to:

- Explain voltage, current, resistance, Ohm's law, and read a simple schematic
- Use a breadboard, a multimeter, and basic components (resistor, capacitor, diode, LED, MOSFET, relay, regulator)
- Distinguish digital vs analog I/O, use GPIO, ADC and PWM on an ESP32
- Wire and read common sensors using existing libraries
- Use I²C, SPI and UART at a working level
- Connect an ESP32 to WiFi, call a REST API, publish over MQTT, format JSON
- Send data to a backend and view it on a dashboard
- Write C/C++ Arduino firmware with loops, functions, structs and serial debugging
- Recognise the *idea* of a block diagram, BOM, pin map, power budget and non-functional requirement (Part 1 Module 11)

**Part 3 does not re-teach any of the above.** Where a topic reappears here, it reappears one level up — Part 1 teaches students to *use* MQTT; Part 3 makes them decide whether MQTT is the right choice and write down the payload contract. Part 1 introduces the *concept* of a block diagram; Part 3 makes them produce one that a schematic is actually built from.

**Part 2** must have produced a **chosen and validated problem statement** with a defined user. This is a hard prerequisite — Unit A0 starts by consuming it. Students arriving without one should be given a fallback statement (a wrist-worn activity and heart-rate tracker for hostel students) so they aren't blocked.

### Tools and accounts (all free)

A laptop that can run KiCad and Fusion 360 — 8 GB RAM minimum, 16 GB comfortable, a discrete GPU helps but isn't required. Stable internet. Accounts on GitHub, Autodesk Education (Fusion 360), Wokwi, and a fab portal like JLCPCB or PCBWay for quoting.

### Numeracy

Unit prefixes and conversions (mA ↔ µA, mAh, mm ↔ mil), percentages for tolerance, simple algebra.

### Not required

Any prior system design, PCB design, CAD, or mechanical engineering exposure. All are taught from zero here.

**Version control — untimed reference page (author, 2026-10-06).** `01-system-architecture/REF-version-control.md`, written once and pointed to from C1, D0, E0 and G. The bare minimum for a hardware project: one Git repository for the whole design pack; what to commit (KiCad project, schematic, board and project libraries; Fusion exports — STEP and `.f3d`; firmware; documents) and what to ignore (KiCad backups and caches, build folders); small commits with clear messages; **tagging the exact version sent to the fab house**, so the Gerbers always match a commit; GitHub Desktop as the no-command-line route. esp_watch's public repository is the example. Branching, pull requests and merge conflicts get one line each.

---

## 1. Section A — System Architecture (~3 hrs)

**Why this section exists and where it stops.** Students coming out of Part 2 have a validated problem but no picture of the *whole* system. Left alone they jump straight to "which sensor should I buy," and every downstream decision inherits that mistake.

This section stays at the **top level**. It draws the whole system on one page — device, firmware, communication, backend, user — and records the big decisions and their consequences. Sensing and hardware are developed in Sections B and C, firmware and communication in Section D. Section A only goes as deep as it needs to in order to keep those sections consistent with each other.

**Section deliverable:** a **System Architecture Document (SAD)** that every later section refers back to.

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **A0** | **Problem statement → product specification.** Convert the Part 2 output into a written spec. Functional requirements ("measures heart rate from 40–180 bpm") vs non-functional requirements (accuracy, response time, battery life, cost ceiling, size and weight envelope, expected lifetime, serviceability). Operating environment — in this case worn against skin, exposed to sweat and impact. Who the user is and what they do with it. Success criteria that can actually be checked. And a hard, explicit list of what is **not** in v1 — keeping scope small is a taught skill, and most student projects fail for want of it. | 1.0 | Filled spec template (provided) |
| **A1** | **Overall system architecture.** Draw the system boundary: what is inside the product, what is outside but interacts with it (the wearer, a phone, a WiFi router, a cloud server, the charger). Context diagram. Then split the inside into subsystems — sensing, processing, power, connectivity, local UI, enclosure, backend — and give every requirement from A0 to a subsystem so nothing is orphaned. Kept generic, one pass each, no deep dives: roughly where the work happens (device vs phone vs server) and why that matters when the link drops; roughly what data flows and how much of it; roughly which connectivity route the product takes and the one-line reason. The point is a coherent single picture, not a finished design. | 1.0 | Context diagram + subsystem list + requirement-to-subsystem table |
| **A2** | **Operating modes, failure behaviour & decisions.** Define the system's states: boot, pairing, normal, measuring, low battery, charging, fault. What happens when the wearer takes the watch off mid-measurement, the battery hits cut-off, a sensor stops responding, or the network is gone all day? Graceful degradation vs hard failure. A first pass at security and privacy — heart-rate data is health data, so who can read it, where does it live, and does it leave the device at all? Then how to write a decision down so you can defend it later: a short **decision note** (the choice, the options considered, why). Case study: read the reference watch as a system and reverse-engineer its architecture. | 1.0 | System state diagram + failure mode table + 2 decision notes |

---

## 2. Section B — Sensing & Hardware Architecture (~8.5 hrs)

**Flow.** First decide what the product must sense and how each sensor talks to the MCU (B0, B1). Then draw the board's architecture from those choices (B2), make the electrical decisions (B3), pick the actual parts (B4), and check the circuit in simulation (B5).

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **B0** | **Common sensors and choosing the right one for the job.** The unit that stops students defaulting to whatever sensor was in the last tutorial. A survey of sensor families — presence and proximity, position and motion, optical and biometric, environmental, force and level, electrical, identification. For each: what it actually measures, typical range, output type, cost, and how it fails. Then a **selection framework**: what physical quantity really indicates the thing you care about, contact vs non-contact, range and resolution needed, response time, environmental tolerance, output type, power, cost, and which error is more expensive — a false positive or a false negative. Taught through worked examples of increasing difficulty (see below). | 1.5 | Sensor selection matrix for their own product + solved scenario exercise |
| **B1** | **Talking to sensors: choosing the interface.** A practical comparison of the common interfaces. **I²C** — two wires, many devices, addressing, speed limits; the reference watch puts all three peripherals on one bus, so address allocation is worked through concretely. **SPI** — fast, separate chip select per device, more pins. **UART** — simple point-to-point, common on self-contained modules. **Analog** — direct ADC read, when it's still right. **Pulse and one-wire outputs.** How to pick: pin count, distance, number of devices, data rate, what the sensor actually offers. Plus the practical failures — address clash, a floating address pin, baud mismatch, missing common ground. (Pull-up sizing and bus voltage are in B3.) | 1.0 | Interface comparison table + interface choice justified for each peripheral |
| **B2** | **Hardware architecture & block diagram.** Take the subsystems from A1 and the sensor and interface choices from B0–B1 down to the electrical level. Every block on the board, every connection between them. An interface table listing each link: signal, protocol, voltage, direction, expected data rate. This is the drawing the schematic will be built from. Worked against the reference watch, where three peripherals share one I²C bus. | 1.0 | Hardware block diagram + interface table |
| **B3** | **Electrical architecture — MCU, power, bus & I/O.** The core electrical decisions of the board, made *before* specific parts are chosen. **MCU class:** how much flash/RAM/pins do you actually need, does it need onboard WiFi/BLE, module vs bare chip (one sentence on why a pre-certified radio module saves you RF certification). **Power:** rail plan, USB vs LiPo, charge path, battery cut-off, current budget per operating mode, decoupling, protection. The reference watch's **modelled** current budget (screen on, heart-rate measurement, WiFi burst, sleep) is the worked example. Students build the same table for their own product and see which state uses most of *their* battery; sleep modes are taught in D2. **Bus electrical design:** bus voltage levels, pull-up sizing, and what happens when three breakout modules each bring their own pull-ups onto the same bus. **I/O:** a pin budget — every peripheral mapped to a pin, with strapping pins, ADC-capable pins, boot pins and deep-sleep wake pins accounted for before the schematic starts. | 2.0 | Power tree + current budget spreadsheet + bus/pin allocation map |
| **B4** | **Component selection: modules or discrete ICs?** The decision the reference watch makes on every line of its BOM. A breakout module is faster to design with, needs no extra parts, and its radio is often already certified — but it costs more, occupies more board area, adds height, and may vanish from the market without notice. A discrete IC is cheaper and thinner, but you now own the reference circuit, the crystal and the antenna. Students decide, per peripheral, and justify it against the A0 spec. Then datasheet reading on whichever they chose: absolute maximums vs recommended operating conditions, electrical characteristics, timing diagrams, the recommended application circuit, package and footprint — plus the difference between a *module's* datasheet and the *chip's* datasheet underneath it. Then parametric search and stock levels (lifecycle is taught in F0). | 1.5 | Module-vs-IC decision table + comparison matrix for 3 candidate parts + preliminary BOM |
| **B5** | **Virtual prototyping.** Build the circuit in simulation. Pull-ups, level shifting, the divider maths, regulator behaviour under load, and what a logic analyzer trace on a shared I²C bus actually looks like when three devices are talking (as annotated captures, since students can't take their own). Wokwi has no MAX30102, so students write a **mock sensor class** that returns synthetic data. Falstad for analog behaviour; LTspice named in one line as the next step. | 1.5 | Working Wokwi / Falstad project link |

### B0 worked examples (author these in this order)

**Example 1 — single sensing decision.** *"A wrist-worn device must measure heart rate continuously without the wearer doing anything."* Candidates: optical PPG, ECG electrodes, a chest strap, a piezo pulse sensor. Students discover that ECG gives a cleaner signal but needs two electrodes with skin contact at separated points, which a single-wrist device cannot provide; that a chest strap is more accurate and completely unacceptable to the user; that optical PPG works passively but degrades with motion, skin tone and fit. The lesson is that "measure heart rate" is not a specification — the physical quantity, the wearing position, the user's tolerance and the failure mode are.

**Example 2 — multiple sensing decisions in one machine.** *"A small conveyor counts bottles going past, checks whether each has a cap, and needs to know how fast the belt is moving."* Three different problems: counting a discrete event, checking a feature, and measuring rate. Students see that the cheapest sensor is often enough for one job and hopeless for another in the same machine. This example is deliberately outside wearables, so students don't over-fit to the reference product.

**Exercise for the student's own product.** Fill the selection matrix for every quantity their own device must sense, with a rejected alternative and a stated reason for each. This feeds B1 (interfaces) and B4 (component selection).

---

## 3. Section C — Form Factor, Schematic & PCB (~6 hrs)

**Flow.** Decide the product's shape and which face each part sits on (C0). Then build the board in KiCad 10, following esp_watch's real project step by step: the schematic (C1), the symbols and footprints the libraries do not have (C2), and the PCB layout through to a DRC-clean board (C3). The walkthroughs show the **bare minimum** of each tool needed to make one board; everything else in KiCad is left to the official manuals (`reference/kicad/`). Students do the same steps on their own product.

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **C0** | **Form factor & concept.** For a wearable the constraints bite immediately: overall thickness, weight, how the strap attaches, which face touches skin, where the charge port opens, how buttons are reached one-handed. Sketching concepts by hand and evaluating them against the A0 spec. **Sensor orientation is decided here, not later** — an optical sensor that ends up on the wrong face produces a board that is beautifully routed, DRC clean, and unable to do its job. The reference watch is examined on exactly this point. The chosen concept gives C3 a board outline, mounting-hole positions and a side for every part. | 1.0 | 3 annotated concept sketches + a chosen direction with justification + board outline and part-side sketch |
| **C1** | **KiCad walkthrough: from pin map to schematic.** Hands-on, on esp_watch's project. Create the project; the KiCad window and the few tools that matter (place symbol, power symbol, wire, net label, no-connect flag, junction); net naming; annotate; assign footprints; ERC, and the errors you will meet. The pin map from B3 is transcribed here, not invented here. Test points and fab notes in one paragraph. A one-table tool reference (icon, shortcut, when to use) replaces explaining every tool. | 1.5 | KiCad schematic, ERC clean |
| **C2** | **Symbols and footprints the library does not have.** None of esp_watch's three peripherals had a usable symbol, and the MAX30102 module had no footprint, so the author drew them. Symbol Editor: pin numbers from the part you will solder, electrical pin types and why ERC needs them. Footprint Editor: **draw, source, or verify** — the MAX30102 module footprint drawn from a calibrated photo (SMD pads), the XIAO footprint downloaded, headers from KiCad's library; a downloaded footprint is unverified until pitch, pad size, courtyard and pin 1 are checked against the drawing. Project libraries in one short step. | 1.0 | At least one hand-drawn symbol and one footprint + footprint verification checklist |
| **C3** | **KiCad walkthrough: PCB layout.** Hands-on, on esp_watch's board. Update PCB from schematic; board setup with the fab house's minimums; board outline and mounting holes from the C0 concept; placement outside-in (connectors, sensor face, antenna first); routing tracks and vias; ground pour on two layers; the antenna keep-out; DRC and what it does not catch; the 3D viewer; exporting the board STEP for Section E. Gerbers are left to F1. | 2.0 | Routed PCB, DRC clean, 3D render + board STEP |

---

## 4. Section D — Firmware (~8 hrs)

**Scope note.** Part 1 covers the mechanics — reading sensors with libraries, I²C/SPI/UART basics, WiFi, HTTP, MQTT, JSON, dashboards. This section is about the layer above that: **designing** the firmware before writing it, **structuring** it so it survives change, making it **run and sleep** efficiently, and **hardening** it so it runs unattended. (Which sensor and which interface are decided in B0–B1.)

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **D0** | **Firmware architecture.** Layered design — drivers, services, application — and why the layering pays for itself the moment a sensor is swapped: only the driver changes, and the application code does not. Separation of concerns: sensor code that doesn't know about WiFi, network code that doesn't know about the OLED. Header/source split, one module per subsystem, a single config header. | 1.5 | Firmware architecture diagram + module responsibility table |
| **D1** | **Design before code: flowcharts and state diagrams.** The design notation students use for the rest of the course. Flowcharts for procedural logic — standard symbols, decision branches, loop structure, and how to avoid a chart that is just spaghetti in boxes. State diagrams for device behaviour — states, events, transitions, entry/exit actions — derived from A2's operating modes. One short example of a sequence diagram, for reference only. Then the habit: draw it, review it, *then* write the code. | 1.0 | Main-loop flowchart + device state diagram |
| **D2** | **Non-blocking logic and sleep modes.** Why `delay()` ruins products. The `millis()` scheduling pattern, implementing the state machine drawn in D1, running sensors at different intervals — an IMU that samples continuously, an optical sensor that runs in short bursts, and a display that only refreshes when something changed. Keeping `loop()` readable and bounded. Then **sleep**, because a battery product spends most of its life idle: in plain terms, what **modem sleep, light sleep and deep sleep** switch off, what they keep, how they wake, and when to use each; why the ESP32-C3 has no deeper "hibernation" or ULP mode and "off" is the only step below deep sleep; putting the whole board to sleep, not just the chip; and how-to code for light sleep with a button wake-up and deep sleep with a timer or pin wake-up. | 2.0 | Refactored sketch: three peripherals, three intervals, no blocking calls, a sleep state with a wake-up + sleep-mode choice with reason |
| **D3** | **Data off the device: serial format, logging and live plotting.** Serial Monitor vs Serial Plotter; designing a *serial data format* rather than printing prose — CSV lines or newline-delimited JSON, header row, consistent field order, units declared once; logging a session to a file; a provided ~40-line Python script (pyserial + matplotlib) students run to read the stream, plot it live and save it. A raw PPG waveform is an excellent thing to plot, because it looks like nothing until you filter it. | 1.0 | Serial protocol doc + logged CSV session + live plot screenshot |
| **D4** | **Connectivity and settings that persist.** Robust WiFi — connect, detect disconnect, reconnect with backoff, never block the main loop; building the JSON payload against a written contract; publishing it with whichever of HTTP or MQTT A1 chose (one paragraph on the choice; Part 1 taught both). What a good device dashboard shows — live value, history, device status, last-seen. Why hardcoded WiFi credentials are a dead end; saving credentials and calibration with Preferences/NVS; factory reset. Offline buffering and captive-portal provisioning named in one line each, as pointers. | 1.0 | Device publishing to a dashboard + config surviving a power cycle |
| **D5** | **Debugging & robustness.** Serial logging habits and log levels. Reading an ESP32 crash dump and decoding a backtrace. The four things that actually go wrong: brownout, stack overflow, watchdog reset, blocking network call. The hardware watchdog. Defensive coding around every external dependency — timeouts and retries on every bus transaction and every network call. | 1.0 | "Spot the bug" exercise set |
| **D6** | **Going further — reading only.** *(extension)* OTA updates, FreeRTOS tasks and queues, ESP-IDF vs Arduino, MQTT with TLS, BLE as an alternative to WiFi for a wearable, unit testing embedded code. One page each, with pointers into the reference watch's firmware repository where applicable. (Sleep modes moved to D2.) | 0.5 | MCQ only |

---

## 5. Section E — Mechanical / 3D Design (~8 hrs)

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **E0** | **Parametric CAD fundamentals, with a Fusion walkthrough.** Fusion 360 (the reference enclosure was modelled in Onshape; the concepts transfer directly). Hands-on, bare minimum: the Fusion window (browser, timeline, toolbar), named **user parameters** set up first so the model regenerates when the PCB changes, a sketch on a plane with constraints until it is fully defined, then extrude, fillet, shell and split body into a base and lid, openings cut into the lid only, and `.f3d` + STEP exports. Solid modelling only (the Solid tab); no surface, mesh, sheet-metal or freeform (Form) tools (author, 2026-10-07). Teach parametric habits, not every tool. | 2.0 | Parametric practice part + a shelled two-part enclosure |
| **E1** | **Materials, colour & rendering.** Choosing an FDM material for a wearable enclosure — PLA vs PETG vs ABS vs TPU, on stiffness, layer adhesion, heat tolerance next to skin, and printability, not on marketing claims. Colour as a design decision, not decoration: visibility, how it photographs, and what a translucent or textured finish hides or reveals about the print. Then one presentation image for the Design Pack: a screenshot of the coloured model in Fusion's Design workspace (physical material + appearance, three-quarter view, orthographic camera). A render in the Render workspace only when a good-looking image is needed, e.g. for a pitch (author, 2026-10-07). | 1.0 | Material choice justified against the A0 spec + one presentation image of the coloured model |
| **E2** | **PCB ↔ enclosure co-design.** Import the board STEP from C3 into Fusion, with a 3D model for every tall part (where to get one, and a stand-in box when none exists). Mounting bosses and standoffs, connector cutouts, clearance to tall components, keepout zones, and feeding any outline change back to **C3**. Module-based designs make this vivid: on the reference watch the modules stand on standoffs and header sockets, and that stack (14.044 mm) alone sets how thick the watch can be. Students measure the stack in CAD and decide whether it is acceptable. | 1.5 | Assembly with the real board model inside, interference check clean |
| **E3** | **Design for manufacturing — printed prototypes.** FDM realities: wall thickness in whole perimeters, clearance for fits from a test print, print orientation, overhangs and bridges, first layer and warping. Then the hardware that holds a printed prototype together, and how to design for it: **heat-set threaded inserts** (boss and hole sizes from the supplier), **M2/M2.5/M3/M4 machine and self-tapping screws** and which size suits which product, **captive nuts**, **magnets** (pockets, polarity, embedding), **snap fits** and **press fits** — choosing by how often the case is opened, and sourcing the hardware before drawing the hole. A short closing note on injection moulding (draft, uniform walls, why mass-produced cases are moulded) so students know it exists. | 1.5 | DFM self-audit checklist, completed + hardware list with supplier links |
| **E4** | **Functional mechanical design for a wearable.** The constraints that are specific to something worn on a body. A **skin-contact window** for the optical sensor: the enclosure must present the sensor to the skin without a gap, because ambient light leaking into the photodiode destroys the signal. **Strap lugs** and the load they carry. A **retained battery bay** that cannot puncture a LiPo pouch. **FPC routing** for the display, without strain or a tight bend radius. **Button travel and feel** through a wall. **Charge-port access.** **Sweat ingress**: where sweat gets in and how gaps and gaskets keep it out (IP ratings named in one sentence). Each is traced back to a requirement in A0. | 1.5 | Revised enclosure with sensor-window and battery-retention reasoning documented |
| **E5** | **Slicing & printability validation.** Cura / PrusaSlicer / Bambu Studio. Layer height, walls, infill, supports, orientation, and a pause-at-layer for embedded magnets or nuts. Read the preview: where will it fail, where does it need support, what will it cost in time and filament. | 0.5 | Sliced file + preview screenshot + time/material estimate |

---

## 6. Section F — Sourcing & Manufacturing Handoff (~3 hrs)

Nothing in Part 1 covers this, and the funded build depends on it. Highest-leverage section in the course per hour spent.

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **F0** | **Sourcing components, and the lifecycle trap.** Parametric search on LCSC, Mouser, Digikey; Indian suppliers (Robu, Element14 India, Sunrom) and when to use them vs importing. Reading a stock listing: MOQ, lead time, price at qty 1 and 10 (volume price breaks named in one line), and **lifecycle status** — Active, not recommended for new designs, end of life, Obsolete, and why two distributors can label the same part differently. **The reference watch is the case study.** Its MPU-6050 IMU was formally discontinued by TDK InvenSense in 2023 with a published last-time-buy schedule; TDK names the ICM-42670-P as a recommended alternate while stating that interchangeability is not guaranteed. Yet modules are still sold everywhere. Students work through the consequences: why an obsolete chip stays available for years through module makers, what happens to a product in year three, and why swapping to the successor would be a *firmware* job too, because the register map changes. (esp_watch keeps the MPU-6050.) Then customs, GST and shipping as real BOM line items. | 1.0 | Fully costed BOM with MPNs, links, lifecycle status per line, unit price at qty 1 and 10 |
| **F1** | **The PCB manufacturing package.** What a fab house actually needs and why each file exists: Gerbers (RS-274X), NC drill files, stackup and fab notes, board dimension drawing, README. Assembly files (BOM in the assembler's CSV format, pick-and-place file, assembly drawing) in one short paragraph — only needed if you order assembly; the reference watch is hand-soldered. Then the practical route the reference watch used — **the JLCPCB KiCad plugin**, which assembles the complete fabrication zip in one action. Students run it on their own board, then **open the zip and identify every file inside against the list above**, because a one-click export that you cannot explain is a liability the first time something is wrong. | 1.0 | Complete fabrication zip + a file-by-file annotation of its contents |
| **F2** | **Quoting without ordering.** Upload the package to JLCPCB or PCBWay, read the automated DFM report, fix what it flags, and pull an instant quote — then stop at checkout. Compare against the reference watch's order: what was quoted, what it actually cost once shipping, customs and GST were added, and how long it took versus the estimate (5 boards: $4 fabrication + $24.68 shipping = $28.68 quoted, $18.68 paid after a $10 discount; 2-day build, 2–5 business days to ship). Do the same for the enclosure with a 3D printing service quote. Build a cost model at qty 1 and 10 for the funded build, with one line on how setup and tooling costs spread out at volume. | 1.0 | DFM report screenshots, resolved issues list, qty 1 / 10 cost model |

---

## 7. Section G — Capstone (~2 hrs + own pace)

Assemble everything into a single **Design Pack**, self-review it against the provided rubric, then run a structured comparison against the reference watch's published files: where did you converge, where did you diverge, and can you justify each divergence?

**Design Pack contents:**

1. Product specification and system architecture document (context diagram, subsystems, state diagram, decision notes)
2. Sensor selection matrix and interface choices
3. Hardware block diagram, power tree, current budget, pin map
4. Module-vs-IC decision table, costed BOM with lifecycle status
5. Form-factor concept, KiCad schematic (ERC clean) and PCB (DRC clean), including any symbols or footprints drawn by hand
6. Firmware architecture diagram, flowcharts and state diagram, sleep-mode choice
7. Firmware with README, serial protocol doc and a working simulation link — the whole pack in one Git repository, with the fab version tagged
8. CAD assembly, STEP export, sliced enclosure file, hardware list, material choice and one presentation image of the coloured model
9. Fabrication package and qty 1 / 10 cost model
10. A one-page "what I'd change in v2"

This pack is exactly what they should submit when they apply for the funded build. **Say that explicitly in the course intro** — it converts an academic exercise into a proposal.

---

## 8. The verification stack (how to be correct without building)

Since nothing is physically tested, tell students explicitly which tool gives them a verdict at each stage. This should be a standing reference page available from day one, not a timed unit.

| Question | Tool that answers it |
|---|---|
| Is my architecture coherent? | Requirement-to-subsystem table — every requirement traces to a subsystem, every subsystem traces to a requirement |
| Did I pick the right sensor? | Selection matrix with a stated rejection reason per alternative, plus the failure-mode column |
| Is this part going to exist in three years? | Lifecycle status on two independent distributors, plus the manufacturer's own product page |
| Does my circuit logic work? | Wokwi (ESP32 + I²C peripherals, runs real Arduino code), Tinkercad Circuits for simpler cases |
| Does my analog/power circuit behave? | Falstad Circuit Simulator (LTspice if you need more) |
| Is my schematic self-consistent? | KiCad ERC — must be zero errors |
| Is my symbol right? | Pin-by-pin diff against the datasheet's pin table, and correct electrical pin types |
| Is my footprint right? | Pad pitch, pad size, courtyard and pin 1 checked against the manufacturer's mechanical drawing — never trust a download |
| Is my board manufacturable? | KiCad DRC, then the fab house's automated DFM report |
| Does the board fit the enclosure? | CAD interference detection + section analysis with the real board STEP |
| Will the enclosure print? | Slicer preview — overhang, support and adhesion warnings |
| Does my firmware match my design? | Diff the code's state transitions against the D1 state diagram |
| Are my *choices* sound? | Diff against the reference watch — including where it got things wrong |

That last row carries a lot of weight in an unsupervised course. Where a student's design differs from the reference, they must either justify the difference or learn something. And because the reference is the course author's own work rather than a polished commercial product, it can be criticised openly — which is a more honest model of engineering than a design presented as correct.

Two caveats to hand students in writing: simulators don't model everything (Wokwi has no MAX30102, so teach them to write a **mock sensor class** returning synthetic data — a useful production habit anyway), and a clean DRC means *manufacturable*, not *functional*.

---

## 9. Assessment design without an instructor *(internal — for us)*

**Every unit has 5–15 MCQs, scaled to the size of its topic (a short topic needs fewer), and a binary self-check of about 8 items.** On top of that, each unit uses whichever one of these formats suits it best:

- **MCQs (auto-graded).** Best used for datasheet interpretation: show a real datasheet excerpt, ask what the absolute maximum V<sub>DD</sub> is, or which pin needs a pull-up. Follow Part 1's five-level model (recall → understanding → application → analysis → debugging); Part 3 should sit mostly at levels 3–5.
- **Coding questions with a checkable output.** Plain C++ functions run against test cases, or a Wokwi project where the expected serial output is specified exactly.
- **Scenario-based selection questions.** The natural fit for B0 and F0: describe an application in two lines, give four options, ask which is correct *and* which failure mode eliminates each of the other three.
- **Diagram-matching exercises.** For Sections A and D: give a written system description and four candidate architecture or state diagrams, ask which correctly represents it.
- **Artifact-diff exercises.** The natural fit for C1 and C2: give a datasheet pin table and a drawn symbol containing one error, or a mechanical drawing and a footprint with the wrong pad pitch, and ask what is wrong. This is exactly the skill the reference design needed and it is cheap to author.
- **Binary self-review checklists.** Unambiguous, tool-verifiable items only. Never "is your design good."
- **Spot-the-bug exercises.** Give a broken schematic, sketch, state diagram or CAD file with a specific defect and a multiple-choice diagnosis.
- **Reference-diff walkthroughs.** "Here's how the reference watch handled sensor placement, and here's the argument that it got it wrong. What would you do?"

**On completion rates:** self-paced technical courses shed most students in the first third. Three things help — keep every unit short and focused (a 2-hour unit must have clearly separate parts), make every unit end in a tangible artifact rather than just a checkmark, and make the running project cumulative so quitting means abandoning something they've built.

---

## 10. Asset inventory — one unit specified in full (sample pattern)

Here is **the old C2 (PCB layout and footprints, now split into C2 and C3)** written out as the pattern to replicate. It maps onto the Part 1 asset structure (PPT / reading / POC / MCQ) with two additions — cookbooks and templates — because Part 3 is design work rather than build work.

**Learning outcomes:** place components on a board from a mechanical and functional starting point; route a two-layer board and pass DRC; draw a footprint from a manufacturer's mechanical drawing; verify a downloaded footprint before trusting it; place an external antenna with awareness of what sits beneath it.

**Assets to author:**

- Reading, as long as the student needs and no longer. Required parts: outcomes, the content, one worked example on the reference watch, the activity that produces the deliverable, self-check, MCQs. Everything else (Try-its, Part headings, "What Part 1 covered") only if it helps.
- Screenshots: KiCad footprint editor mid-edit on the real MAX30102 footprint; the DRC dialog after a clean run; the 3D viewer showing the assembled stack
- Image: the calibrated photo measurements beside the generated footprint, with pad pitch and pin 1 called out
- Diagram (ASCII): decision flow for draw / source / verify a footprint
- Worked example: verifying a downloaded footprint against a mechanical drawing, step by step, with the four measurements that matter
- Template: footprint verification checklist, one row per footprint in the student's BOM
- Cookbook: "Draw a footprint for a through-hole breakout module in KiCad" — 8 steps
- Cookbook: "Check a downloaded footprint before you trust it" — 5 steps
- PPT (~18 slides), authored later from this reading

**Exercise:** verify one downloaded footprint against its mechanical drawing and record the four measurements. Then draw one footprint from scratch for a part in your own BOM.

**Assessment:** 5–15 MCQs (scaled to the topic), including 2 artifact-diff questions (a footprint with the wrong pad pitch; a symbol with a mislabelled pin 1); self-check of about 8 binary items.

**Deliverable into the Design Pack:** routed PCB, DRC clean, plus the footprint verification checklist.
