# Build Progress — C3

Style model: reference/applied-iot/
Reference product: REFERENCE-PRODUCT.md
Spelling: British

## Decisions (from the author, 2026-09-24)

- **Part 1 language:** treat Part 1 as Arduino C++ on ESP32, as `CURRICULUM.md` says. The Part 1
  files currently show CircuitPython on ESP32-S3; the Part 1 team is correcting that. Do not cite
  Part 1 code or module numbers beyond Modules 1–5.
- **Capstone unit ID:** `F`.
- **C5 split** into C5a and C5b, both in `03-firmware`. The hours still add up to 2.5 and the deliverables are divided between the two, not changed.
- **File size cap: 50,000 characters per `.md` file**, including comments and code. One unit
  per file is the default. Two whole units may share a file if both fit under the cap. A unit is
  **never** split across files. At about 6.5–7 characters per word (the Part 1 files run at 6.2), the
  largest target here (6,250 words) comes to about 43,000 characters. Check with `wc -m` before marking
  a unit DRAFTED.
- **Verification stack** (`CURRICULUM.md` §7) is written as a standalone, untimed reference page
  in `01-system-architecture`. It carries the tag
  `<!-- ASSIGNABLE: verification-stack · home: 01-system-architecture -->` on its first line so it
  can be found and moved to another module later.
- **Product name:** esp_watch. XIAO ESP32-C3 module only. The IMU is the MPU-6050. The ICM-42670-P appears only as the lifecycle example in E0 and C0, never specified in detail.
- **Assets:** all reference files are placeholders at the `reference-files/...` paths listed in
  `REFERENCE-PRODUCT.md` §9. Units mark each use with `<!-- ASSET:PLACEHOLDER <path> -->` and
  never quote a placeholder's contents. Do not create `reference-files/`.
- **Reference facts** supplied by the author were written into `REFERENCE-PRODUCT.md` §1–§9.
  Current figures are modelled, not measured. Costs are dated example values from Indian supplier
  listings. The fabrication order is a placeholder until it completes.

- **Length and style (author feedback on A0):** the readings are for students to learn from, not a
  showcase. The **whole file** (assessment included) must fit the word range for its hours, counted
  without table pipes or box-drawing characters. Use plain, easy language. Mention other units only
  where the link adds something (for example, "you'll build the full current budget in B1"), not as
  a running cross-reference. Five MCQs, a short activity set and about 8 self-check items are enough
  for a 1-hour unit.
- **Part 2** already helps students choose a problem statement that is measurable. A0 builds on that
  and does not re-teach it.

## Units

| # | Unit | Module folder | File | Hours | Target words | Max chars | Status |
|---|------|---------------|------|-------|--------------|-----------|--------|
| 1 | A0 — Product Specification | 01-system-architecture | A0-product-specification.md | 1.0 | 3000 | 50000 | DRAFTED |
| 2 | REF — The Verification Stack (untimed reference page) | 01-system-architecture | REF-verification-stack.md | — | 1800 | 50000 | DRAFTED |
| 3 | A1 — Overall System Architecture | 01-system-architecture | A1-overall-system-architecture.md | 1.5 | 4750 | 50000 | DRAFTED |
| 4 | A2 — Operating Modes, Failure Behaviour & Architecture Decisions | 01-system-architecture | A2-operating-modes-and-decisions.md | 1.0 | 3000 | 50000 | DRAFTED |
| 5 | B0 — Hardware Architecture & Block Diagram | 02-hardware-electronics-design | B0-hardware-architecture.md | 1.0 | 3000 | 50000 | DRAFTED |
| 6 | B1 — Electrical Architecture: MCU, Power, Comms & I/O | 02-hardware-electronics-design | B1-electrical-architecture.md | 2.0 | 6250 | 50000 | DRAFTED |
| 7 | B2 — Component Selection: Modules or Discrete ICs? | 02-hardware-electronics-design | B2-component-selection.md | 2.0 | 6250 | 50000 | DRAFTED |
| 8 | B3 — Virtual Prototyping | 02-hardware-electronics-design | B3-virtual-prototyping.md | 1.5 | 4750 | 50000 | DRAFTED |
| 9 | B4 — Schematic Capture, and Drawing Your Own Symbols | 02-hardware-electronics-design | B4-schematic-capture-and-symbols.md | 1.5 | 4750 | 50000 | DRAFTED |
| 10 | B5 — PCB Layout, and the Footprint Problem | 02-hardware-electronics-design | B5-pcb-layout-and-footprints.md | 1.5 | 4750 | 50000 | DRAFTED |
| 11 | C0 — Firmware Architecture | 03-firmware | C0-firmware-architecture.md | 1.5 | 4750 | 50000 | DRAFTED |
| 12 | C1 — Design Before Code: Flowcharts and State Diagrams | 03-firmware | C1-flowcharts-and-state-diagrams.md | 1.5 | 4750 | 50000 | DRAFTED |
| 13 | C2 — Talking to Sensors: Choosing the Interface | 03-firmware | C2-choosing-the-interface.md | 1.0 | 3000 | 50000 | DRAFTED |
| 14 | C3 — Common Sensors and Choosing the Right One | 03-firmware | C3-choosing-sensors.md | 1.5 | 4750 | 50000 | DRAFTED |
| 15 | C4 — Non-Blocking Application Logic | 03-firmware | C4-non-blocking-application-logic.md | 1.5 | 4750 | 50000 | DRAFTED |
| 16 | C5a — Data Off the Device: Serial Format, Logging and Live Plotting | 03-firmware | C5a-data-off-the-device.md | 1.0 | 3000 | 50000 | DRAFTED |
| 17 | C5b — Connectivity: Network, Dashboard and Persistent Settings | 03-firmware | C5b-connectivity-and-persistence.md | 1.5 | 4750 | 50000 | DRAFTED |
| 18 | C6 — Debugging & Robustness | 03-firmware | C6-debugging-and-robustness.md | 1.0 | 3000 | 50000 | DRAFTED |
| 19 | C7 — Going Further (reading only) | 03-firmware | C7-going-further.md | 0.5 | 1500 | 50000 | DRAFTED |
| 20 | D0 — Form Factor & Concept | 04-mechanical-3d-design | D0-form-factor-and-concept.md | 1.0 | 3000 | 50000 | DRAFTED |
| 21 | D1 — Parametric CAD Fundamentals | 04-mechanical-3d-design | D1-parametric-cad-fundamentals.md | 2.0 | 6250 | 50000 | DRAFTED |
| 22 | D2 — PCB ↔ Enclosure Co-Design | 04-mechanical-3d-design | D2-pcb-enclosure-co-design.md | 1.5 | 4750 | 50000 | DRAFTED |
| 23 | D3 — Design for Manufacturing | 04-mechanical-3d-design | D3-design-for-manufacturing.md | 1.5 | 4750 | 50000 | DRAFTED |
| 24 | D4 — Functional Mechanical Design for a Wearable | 04-mechanical-3d-design | D4-functional-mechanical-design.md | 1.5 | 4750 | 50000 | DRAFTED |
| 25 | D5 — Slicing & Printability Validation | 04-mechanical-3d-design | D5-slicing-and-printability.md | 0.5 | 1500 | 50000 | DRAFTED |
| 26 | E0 — Sourcing Components, and the Lifecycle Trap | 05-sourcing-and-manufacturing | E0-sourcing-and-lifecycle.md | 1.0 | 3000 | 50000 | DRAFTED |
| 27 | E1 — The PCB Manufacturing Package | 05-sourcing-and-manufacturing | E1-pcb-manufacturing-package.md | 1.0 | 3000 | 50000 | DRAFTED |
| 28 | E2 — Quoting Without Ordering | 05-sourcing-and-manufacturing | E2-quoting-without-ordering.md | 1.0 | 3000 | 50000 | DRAFTED |
| 29 | F — Capstone: Design Pack and Reference Review | 06-capstone | F-capstone-design-pack.md | 2.0 | 6250 | 50000 | DRAFTED |

**C5 split detail.** C5a covers everything off the device: serial monitor vs plotter, designing a serial data
format, logging a session and the Python plotting script. Its deliverables are the serial protocol doc, a
logged CSV session and a live plot screenshot. C5b covers robust WiFi, the payload contract, HTTP vs MQTT,
offline buffering, what a good dashboard shows, and Preferences/NVS with provisioning. Its deliverables are
a device publishing to a dashboard and config that survives a power cycle.

**Totals:** 29 files (28 timed units + 1 reference page) · 37.0 hours · ~116,800 target words
