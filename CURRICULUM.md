# C3 — From Problem Statement to Manufacturable Design

**Format:** self-paced, online. **Nominal effort:** ~38 hrs, no hard cap.

**What students produce:** not a physical device — a complete, review-ready **design pack** they could hand to a fab house tomorrow. That pack becomes the input to their funded build later.

**Explicitly out of scope:** soldering, PCB fabrication, assembly, 3D printing, bring-up. Manufacturing is taught as *"what you must produce, where you'd send it, and what it would cost"* — the workflow stops at the sliced/quoted stage. Physical breadboard prototyping and 3D printing are part of the wider programme, not of this course — students do them later, during the funded build/competition, on the design this course produces.

**Reference product:** a custom **ESP32-C3 smart watch**, built by the course author — repository: [`niat-physicalai/esp_watch`](https://github.com/niat-physicalai/esp_watch). A Seeed Studio XIAO ESP32-C3 carries a MAX30102 heart-rate/SpO2 sensor, an MPU-6050 six-axis IMU and a 0.96" SSD1306 OLED on a custom carrier PCB, with two user buttons, a power slide switch and a LiPo cell. It was designed in KiCad — with hand-drawn schematic symbols for all three peripherals and a hand-drawn footprint for the MAX30102 — fabricated by JLCPCB via their KiCad export plugin, and enclosed in an **Onshape** model. (The enclosure was modelled in Onshape by the author; the course teaches **Fusion 360**, and tells students the reference was built in Onshape because the concepts transfer directly.)

Because it is the author's own design, students get the real schematic, the real board file, the real fabrication package and the real invoice, with no licensing constraint. They also get something no public reference design offers: an honest account of what went wrong. The design contains at least one formally obsolete component and at least one decision worth arguing with. Both are taught deliberately.

> **Naming note:** the courses in this series are referred to throughout as **Part 1 / Part 2 / Part 3**, not C1/C2/C3, because unit IDs inside this document also use letters (Module 03 units are C0, C1, C2…).

> **Terminology:** this document's **Sections** become **Modules** on the platform (one folder each); its **units** (A0, B1…) become one `.md` reading file each.

**Effort by section:**

| Section | Topic | Hrs |
|---|---|---|
| A | System Architecture | 3.5 |
| B | Hardware & Electronics Design | 9.5 |
| C | Firmware | 11.0 |
| D | Mechanical / 3D Design | 9.0 |
| E | Sourcing & Manufacturing Handoff | 3.0 |
| F | Capstone | 2.0 |
| | **Total** | **38.0** |

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

A laptop that can run KiCad and browser-based CAD — 8 GB RAM minimum, 16 GB comfortable, a discrete GPU helps but isn't required. Stable internet. Accounts on GitHub, Onshape (or Autodesk Education for Fusion 360), Wokwi, and a fab portal like JLCPCB or PCBWay for quoting.

### Numeracy

Unit prefixes and conversions (mA ↔ µA, mAh, mm ↔ mil), percentages for tolerance, simple algebra.

### Not required

Any prior system design, PCB design, CAD, or mechanical engineering exposure. All are taught from zero here.

---

## 1. Section A — System Architecture (~3.5 hrs)

**Why this section exists and where it stops.** Students coming out of Part 2 have a validated problem but no picture of the *whole* system. Left alone they jump straight to "which sensor should I buy," and every downstream decision inherits that mistake.

This section stays deliberately at the **top level**. It draws the whole system on one page — device, firmware, communication, backend, user — and records the big decisions and their consequences. Hardware architecture is developed properly in Section B; firmware architecture in Section C; communication detail in Section C. Section A only goes as deep as it needs to in order to make those three sections consistent with each other.

**Section deliverable:** a **System Architecture Document (SAD)** that every later section refers back to.

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **A0** | **Problem statement → product specification.** Convert the Part 2 output into a written spec. Functional requirements ("measures heart rate from 40–180 bpm") vs non-functional requirements (accuracy, response time, battery life, cost ceiling, size and weight envelope, expected lifetime, serviceability). Operating environment — in this case worn against skin, exposed to sweat and impact. Who the user is and what they do with it. Success criteria that can actually be checked. And a hard, explicit list of what is **not** in v1 — scope discipline is a taught skill and most student projects fail for want of it. | 1.0 | Filled spec template (provided) |
| **A1** | **Overall system architecture.** Draw the system boundary: what is inside the product, what is outside but interacts with it (the wearer, a phone, a WiFi router, a cloud server, the charger). Context diagram. Then decompose the inside into subsystems — sensing, processing, power, connectivity, local UI, enclosure, backend — and allocate every requirement from A0 to a subsystem so nothing is orphaned. Kept generic, one pass each, no deep dives: roughly where the work happens (device vs phone vs server) and why that matters when the link drops; roughly what data flows and how much of it; roughly which connectivity route the product takes and the one-line reason. The point is a coherent single picture, not a finished design. | 1.5 | Context diagram + subsystem decomposition + requirement allocation table |
| **A2** | **Operating modes, failure behaviour & architecture decisions.** Define the system's states: boot, pairing, normal, measuring, low battery, charging, fault. What happens when the wearer takes the watch off mid-measurement, the battery hits cut-off, a sensor stops responding, or the network is gone all day? Graceful degradation vs hard failure. A first pass at security and privacy — heart-rate data is health data, so who can read it, where does it live, and does it leave the device at all? Then how to record a decision so it survives the team: **Architecture Decision Records** (context, options considered, decision, consequences). Case study: read the reference watch as a system and reverse-engineer its architecture. | 1.0 | System state diagram + failure mode table + 3 written ADRs |

---

## 2. Section B — Hardware & Electronics Design (~9.5 hrs)

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **B0** | **Hardware architecture & block diagram.** Take the subsystem decomposition from A1 down to the electrical level. Every block on the board, every connection between them. An interface table listing each link: signal, protocol, voltage, direction, expected data rate. This is the drawing the schematic will be built from. Worked against the reference watch, where three peripherals share one I²C bus and the power path runs through a slide switch. | 1.0 | Hardware block diagram + interface table |
| **B1** | **Electrical architecture — MCU, power, comms & I/O.** The core architectural decisions of the board, made *before* specific parts are chosen. **MCU class:** how much flash/RAM/pins do you actually need, does it need onboard WiFi/BLE, module vs bare chip and the certification consequence of that choice. **Power:** rail plan, USB vs LiPo, charge path, battery cut-off, current budget per operating mode, decoupling, protection. The reference watch makes this concrete with a worked current budget across boot, idle, measuring and sleep — students build the same table for their own product and see which state actually dominates the runtime for *their* usage pattern. <!-- FACT:VERIFY author to confirm which state dominates the reference watch's own budget before this is asserted in the unit; CURRICULUM previously said "the optical sensor's LEDs", REFERENCE-PRODUCT's modelled figures say sleep current dominates under the stated usage profile — do not pick one without the author's sign-off. --> **Communication:** which buses carry what, bus voltage levels, addressing conflicts, pull-up sizing (and what happens when three breakout modules each bring their own pull-ups onto the same bus). **I/O:** a pin budget — every peripheral mapped to a pin, with strapping pins, ADC-capable pins and boot pins accounted for before the schematic starts. | 2.0 | Power tree + current budget spreadsheet + bus/pin allocation map |
| **B2** | **Component selection: modules or discrete ICs?** The decision the reference watch makes on every line of its BOM. A breakout module is faster to design with, needs no passives, and is often already certified — but it costs more per unit, occupies more board area, adds height, and may vanish from the market without notice. A discrete IC is cheaper at volume and thinner, but you now own the reference circuit, the crystal, the antenna and the RF certification. Students decide, per peripheral, and justify it against the A0 spec. Then datasheet literacy on whichever they chose: absolute maximums vs recommended operating conditions, electrical characteristics, timing diagrams, the recommended application circuit, package and footprint — plus the distinction between a *module's* datasheet and the *chip's* datasheet underneath it, which are different documents saying different things. Then parametric search, stock levels, lifecycle status. | 2.0 | Module-vs-IC decision table + comparison matrix for 3 candidate parts + preliminary BOM |
| **B3** | **Virtual prototyping.** Build the circuit in simulation. Pull-ups, level shifting, the divider maths, regulator behaviour under load, and what a logic analyzer trace on a shared I²C bus actually looks like when three devices are talking (as annotated captures, since students can't take their own). | 1.5 | Working Wokwi / Falstad project link |
| **B4** | **Schematic capture, and drawing your own symbols.** KiCad: net naming, hierarchical sheets, ERC, test points, fab notes. Then the part the reference design forces and most courses skip — **creating a schematic symbol from a datasheet**. None of the three peripherals on the reference watch had a usable symbol, so all three were drawn by hand. Students learn pin numbering and naming, electrical pin types and why ERC depends on them, symbol size and readability, and library management so a symbol is reusable rather than trapped in one project. The pin map from B1 is transcribed here, not invented here. | 1.5 | KiCad schematic (ERC clean) + at least one hand-drawn symbol |
| **B5** | **PCB layout, and the footprint problem.** Stackup, connector-driven placement, decoupling placement, ground pour, board outline imported from CAD, mounting holes, DRC. Then **footprints: draw, source, or verify** — the reference watch did all three. The MAX30102 footprint was drawn from scratch against a mechanical drawing; the other two were downloaded. The lesson is that a downloaded footprint is *unverified* until you check pad pitch, pad size, courtyard and pin 1 orientation against the manufacturer's drawing yourself, and that a wrong footprint is discovered when the board arrives, not by DRC. Also covered: antenna placement — the XIAO ESP32-C3 uses an external antenna, so where it sits, what is underneath it, and what a LiPo pouch does to its tuning are layout decisions, not afterthoughts. | 1.5 | Routed PCB, DRC clean, 3D render + footprint verification checklist |

---

## 3. Section C — Firmware (~11 hrs)

**Scope note.** Part 1 covers the mechanics — reading sensors with libraries, I²C/SPI/UART basics, WiFi, HTTP, MQTT, JSON, dashboards. This section is about the layer above that: **deciding** what to sense and how to talk to it, **designing** the firmware before writing it, **structuring** it so it survives change, and **hardening** it so it runs unattended.

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **C0** | **Firmware architecture.** Layered design — drivers, services, application — and why the layering pays for itself the moment a sensor is swapped. This is not hypothetical on the reference watch: its IMU is obsolete, so a v2 will change the driver, and only a layered design keeps that change out of the application code. Separation of concerns: sensor code that doesn't know about WiFi, network code that doesn't know about the OLED. Header/source split, one module per subsystem, a single config header. | 1.5 | Firmware architecture diagram + module responsibility table |
| **C1** | **Design before code: flowcharts and state diagrams.** The design notation students use for the rest of the course. Flowcharts for procedural logic — standard symbols, decision branches, loop structure, and how to avoid a chart that is just spaghetti in boxes. State diagrams for device behaviour — states, events, transitions, entry/exit actions — derived from A2's operating modes. Sequence diagrams for who-talks-to-whom over time. Then the discipline: draw it, review it, *then* write the code. | 1.5 | Main-loop flowchart + device state diagram + one sequence diagram |
| **C2** | **Talking to sensors: choosing the interface.** A practical comparison of the common interfaces. **I²C** — two wires, many devices, addressing, pull-ups, speed limits; the reference watch puts all three peripherals on one bus, so address allocation and bus loading are worked through concretely. **SPI** — fast, separate chip select per device, more pins. **UART** — simple point-to-point, common on self-contained modules. **Analog** — direct ADC read, when it's still right. **Pulse and one-wire outputs.** How to pick: pin count, distance, number of devices, data rate, what the sensor actually offers. Plus the practical failures — wrong pull-ups, address clash, baud mismatch, missing common ground. | 1.0 | Interface comparison table + interface choice justified for each peripheral |
| **C3** | **Common sensors and choosing the right one for the job.** The unit that stops students defaulting to whatever sensor was in the last tutorial. A survey of sensor families — presence and proximity, position and motion, optical and biometric, environmental, force and level, electrical, identification. For each: what it actually measures, typical range, output type, cost, and how it fails. Then a **selection framework**: what physical quantity genuinely indicates the thing you care about, contact vs non-contact, range and resolution needed, response time, environmental tolerance, output type, power, cost, and which error is more expensive — a false positive or a false negative. Taught through worked examples of increasing difficulty (see below). | 1.5 | Sensor selection matrix for their own product + solved scenario exercise |
| **C4** | **Non-blocking application logic.** Why `delay()` ruins products. The `millis()` scheduling pattern, implementing the state machine drawn in C1, running sensors at different intervals — an IMU that samples continuously, an optical sensor that runs in short bursts to save power, and a display that only refreshes when something changed. Keeping `loop()` readable and bounded. | 1.5 | Refactored sketch: three peripherals, three intervals, no blocking calls |
| **C5** | **Data & connectivity — from device to PC to dashboard.** One continuous pipeline taught end to end. **Off the device:** Serial Monitor vs Serial Plotter; designing a *serial data format* rather than printing prose — CSV lines or newline-delimited JSON, header row, consistent field order, units declared once; logging a session to a file; a provided ~40-line Python script (pyserial + matplotlib) students run to read the stream, plot it live and save it. A raw PPG waveform is an excellent thing to plot, because it looks like nothing until you filter it. **Over the network:** robust WiFi — connect, detect disconnect, reconnect with backoff, never block the main loop; building the JSON payload against a written contract; HTTP POST vs MQTT publish; buffering readings while offline and flushing on reconnect. **Onto a screen:** pushing to a dashboard, and what a good device dashboard shows — live value, history, device status, last-seen. **Settings that persist:** why hardcoded WiFi credentials are a dead end; saving credentials and calibration with Preferences/NVS; factory reset; captive-portal provisioning as concept and reference, not built from scratch. | 2.5 | Serial protocol doc + logged CSV session + live plot screenshot + device publishing to a dashboard + config surviving a power cycle |
| **C6** | **Debugging & robustness.** Serial logging discipline and log levels. Reading an ESP32 crash dump and decoding a backtrace. The four things that actually go wrong: brownout, stack overflow, watchdog reset, blocking network call. The hardware watchdog. Defensive coding around every external dependency — timeouts and retries on every bus transaction and every network call. | 1.0 | "Spot the bug" exercise set |
| **C7** | **Going further — reading only.** *(extension)* OTA updates, FreeRTOS tasks and queues, ESP-IDF vs Arduino, MQTT with TLS, BLE as an alternative to WiFi for a wearable, deep sleep and battery duty-cycling, unit testing embedded code. One page each, with pointers into the reference watch's firmware repository where applicable. | 0.5 | MCQ only |

### C3 worked examples (author these in this order)

**Example 1 — single sensing decision.** *"A wrist-worn device must measure heart rate continuously without the wearer doing anything."* Candidates: optical PPG, ECG electrodes, a chest strap, a piezo pulse sensor. Students discover that ECG gives a cleaner signal but needs two electrodes with skin contact at separated points, which a single-wrist device cannot provide; that a chest strap is more accurate and completely unacceptable to the user; that optical PPG works passively but degrades with motion, skin tone and fit. The lesson is that "measure heart rate" is not a specification — the physical quantity, the wearing position, the user's tolerance and the failure mode are.

**Example 2 — multiple sensing decisions in one machine.** *"A small conveyor counts bottles going past, checks whether each has a cap, and needs to know how fast the belt is moving."* Three different problems: counting a discrete event, checking a feature, and measuring rate. Students see that the cheapest sensor is often enough for one job and hopeless for another in the same machine. This example is deliberately outside wearables, so students don't over-fit to the reference product.

**Exercise for the student's own product.** Fill the selection matrix for every quantity their own device must sense, with a rejected alternative and a stated reason for each. This feeds directly into B2.

---

## 4. Section D — Mechanical / 3D Design (~8 hrs)

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **D0** | **Form factor & concept.** For a wearable the constraints bite immediately: overall thickness, weight, how the strap attaches, which face touches skin, where the charge port opens, how buttons are reached one-handed. Sketching concepts and evaluating them against the A0 spec. **Sensor orientation is decided here, not later** — an optical sensor that ends up on the wrong face produces a board that is beautifully routed, DRC clean, and unable to do its job. The reference watch is examined on exactly this point. | 1.0 | 3 annotated concept sketches + a chosen direction with justification |
| **D1** | **Parametric CAD fundamentals.** Fusion 360 or Onshape. Sketch constraints, extrude/revolve/shell/fillet, feature history, and above all **naming parameters** so the model regenerates when the PCB changes. Teach parametric discipline, not just modelling. | 2.0 | Parametric practice part + a shelled two-part enclosure |
| **D1b** | **Materials, colour & rendering.** Choosing an FDM material for a wearable enclosure — PLA vs PETG vs ABS vs TPU, on stiffness, layer adhesion, heat tolerance next to skin, and printability, not on marketing claims. Colour as a design decision, not decoration: visibility, how it photographs, and what a translucent or textured finish hides or reveals about the print. Then producing one rendered image of the enclosure in the CAD tool's render workspace — camera angle, material preview, lighting — as the presentation image for the Design Pack and any pitch that follows it. | 1.0 | Material choice justified against the A0 spec + one rendered presentation image |
| **D2** | **PCB ↔ enclosure co-design.** Export the board STEP from KiCad into CAD. Mounting bosses and standoffs, connector cutouts, clearance to tall components, keepout zones, and feeding the outline back to **B5**. Module-based designs make this vivid: on the reference watch the OLED sits on standoffs above the IMU, and that stack height alone sets how thick the watch can be. Students measure the stack in CAD and decide whether it is acceptable. | 1.5 | Assembly with the real board model inside, interference check clean |
| **D3** | **Design for manufacturing.** FDM realities: wall thickness, clearance for fits, print orientation, overhangs and supports, warping. Fastening strategy — self-tapping screws vs heat-set inserts vs snap fits, with when each is appropriate, plus sourcing off-the-shelf mechanical hardware. Then a contrast section on injection moulding (draft angles, uniform walls, ribs, gate location, tooling cost) so students understand what changes at 10,000 units — and why almost every real watch case is moulded or machined rather than printed. | 1.5 | DFM self-audit checklist, completed |
| **D4** | **Functional mechanical design for a wearable.** The constraints that are specific to something worn on a body. A **skin-contact window** for the optical sensor: the enclosure must present the sensor to the skin without a gap, because ambient light leaking into the photodiode destroys the signal. **Strap lugs** and the load they carry. A **retained battery bay** that cannot puncture a LiPo pouch. **FPC routing** for the display, without strain or a tight bend radius. **Button travel and feel** through a wall. **Charge-port access.** **Sweat ingress** and what an IP rating would actually require. Each is traced back to a requirement in A0. | 1.5 | Revised enclosure with sensor-window and battery-retention reasoning documented |
| **D5** | **Slicing & printability validation.** Cura / PrusaSlicer / Bambu Studio. Layer height, walls, infill, supports, orientation. Read the preview: where will it fail, where does it need support, what will it cost in time and filament. | 0.5 | Sliced file + preview screenshot + time/material estimate |

---

## 5. Section E — Sourcing & Manufacturing Handoff (~3 hrs)

Nothing in Part 1 covers this, and the funded build depends on it. Highest-leverage section in the course per hour spent.

| # | Unit | Hrs | Deliverable |
|---|---|---|---|
| **E0** | **Sourcing components, and the lifecycle trap.** Parametric search on LCSC, Mouser, Digikey; Indian suppliers (Robu, Element14 India, Sunrom) and when to use them vs importing. Reading a stock listing: MOQ, lead time, price breaks at 1/10/100/1000, and **lifecycle status** — Active, NRND, EOL, Obsolete, and why two distributors can label the same part differently. **The reference watch is the case study.** Its MPU-6050 IMU was formally discontinued by TDK InvenSense in 2023 with a published last-time-buy schedule; TDK names the ICM-42670-P as a recommended alternate while stating that interchangeability is not guaranteed. Yet modules are still sold everywhere. Students work through the consequences: why an obsolete chip stays available for years through module makers, what happens to your product in year three, and why swapping to the successor is a *firmware* job too, because the register map changes. Then customs, GST and shipping as real BOM line items. | 1.0 | Fully costed BOM with MPNs, links, lifecycle status per line, unit price at qty 1 / 10 / 100 |
| **E1** | **The PCB manufacturing package.** What a fab house actually needs and why each file exists: Gerbers (RS-274X), NC drill files, stackup and fab notes, board dimension drawing, BOM in the assembler's required CSV format, CPL/pick-and-place file, assembly drawing, README. Then the practical route the reference watch used — **the JLCPCB KiCad plugin**, which assembles the complete fabrication zip in one action. Students run it on their own board, then **open the zip and identify every file inside against the list above**, because a one-click export that you cannot explain is a liability the first time something is wrong. Where rotation errors come from and why they are the number one cause of assembly failures. | 1.0 | Complete fabrication zip + a file-by-file annotation of its contents |
| **E2** | **Quoting without ordering.** Upload the package to JLCPCB or PCBWay, read the automated DFM report, fix what it flags, and pull an instant quote — then stop at checkout. Compare against the reference watch's **real order**: what was quoted, what it actually cost once shipping, customs and GST were added, and how long it actually took versus the estimate. Do the same for the enclosure with a 3D printing service quote. Build a unit-cost model at 10, 100 and 1000 units, including NRE, tooling, assembly and test time. | 1.0 | DFM report screenshots, resolved issues list, three-tier cost model |

---

## 6. Section F — Capstone (~2 hrs + own pace)

Assemble everything into a single **Design Pack**, self-review it against the provided rubric, then run a structured comparison against the reference watch's published files: where did you converge, where did you diverge, and can you justify each divergence?

**Design Pack contents:**

1. Product specification and system architecture document (context diagram, subsystem decomposition, state diagram, ADRs)
2. Hardware block diagram, power tree, pin map
3. Sensor selection matrix, module-vs-IC decision table, costed BOM with lifecycle status
4. KiCad schematic (ERC clean) and PCB (DRC clean), including any symbols or footprints drawn by hand
5. Firmware architecture diagram, flowcharts and state diagram
6. Firmware repo with README, serial protocol doc and a working simulation link
7. CAD assembly, STEP export, sliced enclosure file, material choice and one rendered presentation image
8. Fabrication package and three-tier cost model
9. A one-page "what I'd change in v2"

This pack is exactly what they should submit when they apply for the funded build. **Say that explicitly in the course intro** — it converts an academic exercise into a proposal.

---

## 7. The verification stack (how to be correct without building)

Since nothing is physically tested, tell students explicitly which tool gives them a verdict at each stage. This should be a standing reference page available from day one, not a timed unit.

| Question | Tool that answers it |
|---|---|
| Is my architecture coherent? | Requirement allocation table — every requirement traces to a subsystem, every subsystem traces to a requirement |
| Did I pick the right sensor? | Selection matrix with a stated rejection reason per alternative, plus the failure-mode column |
| Is this part going to exist in three years? | Lifecycle status on two independent distributors, plus the manufacturer's own product page |
| Does my circuit logic work? | Wokwi (ESP32 + I²C peripherals, runs real Arduino code), Tinkercad Circuits for simpler cases |
| Does my analog/power circuit behave? | Falstad Circuit Simulator (intuitive) or LTspice (rigorous) |
| Is my schematic self-consistent? | KiCad ERC — must be zero errors |
| Is my symbol right? | Pin-by-pin diff against the datasheet's pin table, and correct electrical pin types |
| Is my footprint right? | Pad pitch, pad size, courtyard and pin 1 checked against the manufacturer's mechanical drawing — never trust a download |
| Is my board manufacturable? | KiCad DRC, then the fab house's automated DFM report |
| Does the board fit the enclosure? | CAD interference detection + section analysis with the real board STEP |
| Will the enclosure print? | Slicer preview — overhang, support and adhesion warnings |
| Does my firmware match my design? | Diff the code's state transitions against the C1 state diagram |
| Are my *choices* sound? | Diff against the reference watch — including where it got things wrong |

That last row carries a lot of weight in an unsupervised course. Where a student's design differs from the reference, they must either justify the difference or learn something. And because the reference is the course author's own work rather than a polished commercial product, it can be criticised openly — which is a more honest model of engineering than a design presented as correct.

Two caveats to hand students in writing: simulators don't model everything (Wokwi has no MAX30102, so teach them to write a **mock sensor class** returning synthetic data — a genuinely useful production habit anyway), and a clean DRC means *manufacturable*, not *functional*.

---

## 8. Assessment design without an instructor *(internal — for us)*

Every unit should end with at least one, or a mix, of these formats:

- **MCQs (auto-graded).** Best used for datasheet interpretation: show a real datasheet excerpt, ask what the absolute maximum V<sub>DD</sub> is, or which pin needs a pull-up. Follow Part 1's five-level model (recall → understanding → application → analysis → debugging); Part 3 should sit mostly at levels 3–5.
- **Coding questions with a checkable output.** Plain C++ functions run against test cases, or a Wokwi project where the expected serial output is specified exactly.
- **Scenario-based selection questions.** The natural fit for C3 and E0: describe an application in two lines, give four options, ask which is correct *and* which failure mode eliminates each of the other three.
- **Diagram-matching exercises.** For Sections A and C: give a written system description and four candidate architecture or state diagrams, ask which correctly represents it.
- **Artifact-diff exercises.** New, and the natural fit for B4 and B5: give a datasheet pin table and a drawn symbol containing one error, or a mechanical drawing and a footprint with the wrong pad pitch, and ask what is wrong. This is exactly the skill the reference design needed and it is cheap to author.
- **Binary self-review checklists.** Unambiguous, tool-verifiable items only. Never "is your design good."
- **Spot-the-bug exercises.** Give a broken schematic, sketch, state diagram or CAD file with a specific defect and a multiple-choice diagnosis.
- **Reference-diff walkthroughs.** "Here's how the reference watch handled sensor placement, and here's the argument that it got it wrong. What would you do?"

**On completion rates:** self-paced technical courses shed most students in the first third. Three things help — keep every unit under 90 minutes, make every unit end in a tangible artifact rather than just a checkmark, and make the running project cumulative so quitting means abandoning something they've built.

---

## 9. Asset inventory — one unit specified in full (sample pattern)

Here is **B5 (PCB layout and footprints)** written out as the pattern to replicate. It maps onto the Part 1 asset structure (PPT / reading / POC / MCQ) with two additions — cookbooks and templates — because Part 3 is design work rather than build work.

**Learning outcomes:** place components on a board from a mechanical and functional starting point; route a two-layer board and pass DRC; draw a footprint from a manufacturer's mechanical drawing; verify a downloaded footprint before trusting it; place an external antenna with awareness of what sits beneath it.

**Assets to author:**

- Reading (~4,500 words), following the Part 1 structure: situation → concept → how it works → worked example → common mistakes → troubleshooting → activities → takeaways
- Screenshots: KiCad footprint editor mid-edit on the real MAX30102 footprint; the DRC dialog after a clean run; the 3D viewer showing the assembled stack
- Image: the manufacturer's mechanical drawing beside the drawn footprint, with pad pitch and pin 1 called out
- Diagram (ASCII): decision flow for draw / source / verify a footprint
- Worked example: verifying a downloaded footprint against a mechanical drawing, step by step, with the four measurements that matter
- Template: footprint verification checklist, one row per footprint in the student's BOM
- Cookbook: "Draw a footprint for a through-hole breakout module in KiCad" — 8 steps
- Cookbook: "Check a downloaded footprint before you trust it" — 5 steps
- PPT (~18 slides), authored later from this reading

**Exercise:** verify one downloaded footprint against its mechanical drawing and record the four measurements. Then draw one footprint from scratch for a part in your own BOM.

**Assessment:** 6 MCQs on reading a mechanical drawing; 2 artifact-diff questions (a footprint with the wrong pad pitch; a symbol with a mislabelled pin 1); self-check rubric of 10 binary items.

**Deliverable into the Design Pack:** routed PCB, DRC clean, plus the footprint verification checklist.