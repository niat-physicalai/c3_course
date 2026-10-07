# Build Progress — C3

Style model: reference/applied-iot/
Reference product: REFERENCE-PRODUCT.md
Spelling: British

## Decisions (from the author, 2026-09-24)

- **Part 1 language:** treat Part 1 as Arduino C++ on ESP32, as `CURRICULUM.md` says. The Part 1
  files currently show CircuitPython on ESP32-S3; the Part 1 team is correcting that. Do not cite
  Part 1 code or module numbers beyond Modules 1–5.
- **Capstone unit ID:** `F` (renumbered to `G` on 2026-09-29).
- **C5 split** into C5a and C5b (now D3 and D4, in `04-firmware`). Hours are now 1.0 + 1.0 (author, 2026-09-29).
- **File size cap: 50,000 characters per `.md` file**, including comments and code. One unit
  per file is the default. Two whole units may share a file if both fit under the cap. A unit is
  **never** split across files. Check with `wc -m` before marking
  a unit DRAFTED.
- **Verification stack** (`CURRICULUM.md` §8) is written as a standalone, untimed reference page
  in `01-system-architecture`. It carries the tag
  `<!-- ASSIGNABLE: verification-stack · home: 01-system-architecture -->` on its first line so it
  can be found and moved to another module later.
- **Product name:** esp_watch. XIAO ESP32-C3 module only. The IMU is the MPU-6050. The ICM-42670-P appears only as the lifecycle example in F0 and the driver-swap argument in D0 (was E0 and C0), never specified in detail.
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

## Restructure 2026-10-06 (author-approved)

- **Purpose:** students will use the course as a **reference** when they build their own product later in the
  programme. It must enable them to build one; it must not require them to build anything to finish.
  Laptop-only hands-on stays: system architecture, brainstorming, BOM, schematic, PCB, CAD.
- **Section C grows from 4 to 6 hours and four units.** C1 is a KiCad 10 schematic walkthrough, C2 covers
  symbols and footprints, and C3 (new) is a KiCad PCB-layout walkthrough ending at the board STEP. Gerbers stay in F1.
- **Walkthroughs follow esp_watch's real KiCad project.** They show the **bare minimum** to make one board, with
  one image per step and a one-table tool reference. The official KiCad 10 manuals in `reference/kicad/` cover
  everything else and are cited, never reproduced.
- **CAD tool: Fusion 360.** E0 gains a short Fusion walkthrough, and E2 adds where to get 3D models for every tall part.
- **Version control:** a new untimed page, `01-system-architecture/REF-version-control.md`, with pointers from C1, D0, E0 and G.
- **Pin naming (author, 2026-10-07):** the buttons are **D10** ("next") and **D9** ("previous"), named by XIAO label only, never by
  GPIO number. I²C is on **D4/D5**. The carrier has **no resistors**: the I²C pull-ups are the modules' own, and the buttons use
  internal pull-ups. Applied to REFERENCE-PRODUCT, B1, B2, B3 (and B3-02.svg), B4, B5, C1, D2, G, the Wokwi sims and the BOM workbook.
- **Order of work:** C1 → C2 → C3 → E0 → E2 → REF-version-control. Then update the links in every unit that
  points to the old C2. Image needs are listed in `review/ASSETS-TODO.md` §6.

## Units

No word targets (author, 2026-09-29): each unit is as long as a student needs to understand its
`CURRICULUM.md` row and produce its deliverable. Every unit has 5–15 MCQs (scaled to the topic) and a ~8-item self-check.
The 50,000-character file cap still applies.

| # | Unit | Module folder | File | Hours | Was | Max chars | Status |
|---|------|---------------|------|-------|-----|-----------|--------|
| 1 | A0 — Product Specification | 01-system-architecture | A0-product-specification.md | 1.0 | — | 50000 | DRAFTED |
| 2 | REF — The Verification Stack (untimed reference page) | 01-system-architecture | REF-verification-stack.md | — | — | 50000 | DRAFTED |
| 2b | REF — Version Control for a Hardware Project (untimed reference page) | 01-system-architecture | REF-version-control.md | — | — | 50000 | DRAFTED (2026-10-07) |
| 3 | A1 — Overall System Architecture | 01-system-architecture | A1-overall-system-architecture.md | 1.0 | — | 50000 | DRAFTED |
| 4 | A2 — Operating Modes, Failure Behaviour & Decisions | 01-system-architecture | A2-operating-modes-and-decisions.md | 1.0 | — | 50000 | DRAFTED |
| 5 | B0 — Common Sensors and Choosing the Right One | 02-sensing-and-hardware-architecture | B0-choosing-sensors.md | 1.5 | C3 | 50000 | DRAFTED |
| 6 | B1 — Talking to Sensors: Choosing the Interface | 02-sensing-and-hardware-architecture | B1-choosing-the-interface.md | 1.0 | C2 | 50000 | DRAFTED |
| 7 | B2 — Hardware Architecture & Block Diagram | 02-sensing-and-hardware-architecture | B2-hardware-architecture.md | 1.0 | B0 | 50000 | DRAFTED |
| 8 | B3 — Electrical Architecture: MCU, Power, Bus & I/O | 02-sensing-and-hardware-architecture | B3-electrical-architecture.md | 2.0 | B1 | 50000 | DRAFTED |
| 9 | B4 — Component Selection: Modules or Discrete ICs? | 02-sensing-and-hardware-architecture | B4-component-selection.md | 1.5 | B2 | 50000 | DRAFTED |
| 10 | B5 — Virtual Prototyping | 02-sensing-and-hardware-architecture | B5-virtual-prototyping.md | 1.5 | B3 | 50000 | DRAFTED |
| 11 | C0 — Form Factor & Concept | 03-form-schematic-and-pcb | C0-form-factor-and-concept.md | 1.0 | D0 | 50000 | DRAFTED |
| 12 | C1 — KiCad Walkthrough: From Pin Map to Schematic | 03-form-schematic-and-pcb | C1-kicad-schematic-walkthrough.md | 1.5 | C1 | 50000 | DRAFTED (2026-10-06; symbol drawing moved to C2) |
| 13 | C2 — Symbols and Footprints the Library Does Not Have | 03-form-schematic-and-pcb | C2-symbols-and-footprints.md | 1.0 | C1 + C2 | 50000 | DRAFTED (2026-10-07; layout moved to C3) |
| 13b | C3 — KiCad Walkthrough: PCB Layout | 03-form-schematic-and-pcb | C3-kicad-pcb-walkthrough.md | 2.0 | C2 | 50000 | DRAFTED (2026-10-07) |
| 14 | D0 — Firmware Architecture | 04-firmware | D0-firmware-architecture.md | 1.5 | C0 | 50000 | DRAFTED |
| 15 | D1 — Design Before Code: Flowcharts and State Diagrams | 04-firmware | D1-flowcharts-and-state-diagrams.md | 1.0 | C1 | 50000 | DRAFTED |
| 16 | D2 — Non-Blocking Logic and Sleep Modes | 04-firmware | D2-non-blocking-logic-and-sleep.md | 2.0 | C4 | 50000 | DRAFTED |
| 17 | D3 — Data Off the Device: Serial Format, Logging and Live Plotting | 04-firmware | D3-data-off-the-device.md | 1.0 | C5a | 50000 | DRAFTED |
| 18 | D4 — Connectivity and Settings That Persist | 04-firmware | D4-connectivity-and-persistence.md | 1.0 | C5b | 50000 | DRAFTED |
| 19 | D5 — Debugging & Robustness | 04-firmware | D5-debugging-and-robustness.md | 1.0 | C6 | 50000 | DRAFTED |
| 20 | D6 — Going Further (reading only) | 04-firmware | D6-going-further.md | 0.5 | C7 | 50000 | DRAFTED |
| 21 | E0 — Parametric CAD Fundamentals | 05-mechanical-3d-design | E0-parametric-cad-fundamentals.md | 2.0 | D1 | 50000 | DRAFTED (2026-10-07, Fusion walkthrough) |
| 22 | E1 — Materials, Colour & Rendering | 05-mechanical-3d-design | E1-materials-colour-rendering.md | 1.0 | D1b | 50000 | DRAFTED (revised 2026-10-07: coloured-model screenshot; render optional) |
| 23 | E2 — PCB ↔ Enclosure Co-Design | 05-mechanical-3d-design | E2-pcb-enclosure-co-design.md | 1.5 | D2 | 50000 | DRAFTED (2026-10-07, 3D models, Fusion steps, C3 links) |
| 24 | E3 — Design for Manufacturing (printed prototypes) | 05-mechanical-3d-design | E3-design-for-manufacturing.md | 1.5 | D3 | 50000 | DRAFTED |
| 25 | E4 — Functional Mechanical Design for a Wearable | 05-mechanical-3d-design | E4-functional-mechanical-design.md | 1.5 | D4 | 50000 | DRAFTED |
| 26 | E5 — Slicing & Printability Validation | 05-mechanical-3d-design | E5-slicing-and-printability.md | 0.5 | D5 | 50000 | DRAFTED |
| 27 | F0 — Sourcing Components, and the Lifecycle Trap | 06-sourcing-and-manufacturing | F0-sourcing-and-lifecycle.md | 1.0 | E0 | 50000 | DRAFTED |
| 28 | F1 — The PCB Manufacturing Package | 06-sourcing-and-manufacturing | F1-pcb-manufacturing-package.md | 1.0 | E1 | 50000 | DRAFTED |
| 29 | F2 — Quoting Without Ordering | 06-sourcing-and-manufacturing | F2-quoting-without-ordering.md | 1.0 | E2 | 50000 | DRAFTED |
| 30 | G — Capstone: Design Pack and Reference Review | 07-capstone | G-capstone-design-pack.md | 2.0 | F | 50000 | DRAFTED |

**Restructure 2026-09-29 (author-approved).** Units were renumbered to follow the learning flow:
sensing and interfaces now come before hardware architecture and component selection, and the
form-factor concept comes before schematic and PCB. The "Was" column gives each unit's old ID. Files,
folders, code assets (`assets/code/`), cross-references and next-unit links were all updated. Sleep
modes moved from C7 into D2 (was C4). E3 (was D3) now covers prototype fastening hardware, with
injection moulding cut down to a short note. Units whose `CURRICULUM.md` row shrank were trimmed to match: A2 (ADRs → 2 decision
notes), B3/B4 (certification, lifecycle → pointers), C0 (+ board outline sketch), C1 (hierarchy, libraries),
D1 (sequence diagrams → reference example), D4 (buffering, HTTP vs MQTT), E4 (IP rating), F0–F2 (qty 1 and 10;
assembly files → one paragraph). A1 changed hours only (1.5 → 1.0); its length is left to `/review-unit`.

**C5 split detail (now D3 and D4).** C5a (now D3) covers everything off the device: serial monitor vs plotter, designing a serial data
format, logging a session and the Python plotting script. Its deliverables are the serial protocol doc, a
logged CSV session and a live plot screenshot. C5b (now D4) covers robust WiFi, the payload contract, HTTP vs MQTT,
offline buffering, what a good dashboard shows, and Preferences/NVS with provisioning. Its deliverables are
a device publishing to a dashboard and config that survives a power cycle.

**Totals:** 32 files (30 timed units + 2 reference pages) · 38.5 hours (was 36.5) · no word targets

**2026-09-28 update (author):** added **D1b — Materials, Colour & Rendering** (now E1, 1.0 h) to cover the
"rendering, material, colour, material selection" requirement, which had no unit. Reference product
is now documented at [`niat-physicalai/esp_watch`](https://github.com/niat-physicalai/esp_watch) —
see the "2026-09-28" note in `REFERENCE-PRODUCT.md` for what changed and what still needs the
author's confirmation before B1 and B4/B5 (now B3 and C1/C2) are written or revised. Memory management (from the
original requirements sheet) is confirmed **out of scope** — too deep a topic for this course.
Word targets were removed on 2026-09-29 — see `review/RUBRIC.md`.