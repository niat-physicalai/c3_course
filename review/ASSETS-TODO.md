# Assets still to supply

Generated 2026-10-01. Line numbers are as of this date; the placeholder ID (or path) is the stable thing to search for.

Put each real file at the path shown, then tell Claude to swap the placeholder for the image. Images already in the public repo (`asset/pcb/Schematic.png`, `pcb_top.png`, `pcb_FCu.png`, `asset/breadboard/photo_9.jpeg`) are now linked directly and are not listed.

## 1. Reference files from you

| File to supply | Used in | Location |
|---|---|---|
| `reference-files/fab/esp_watch_jlcpcb.zip` | F1 | `06-sourcing-and-manufacturing/F1-pcb-manufacturing-package.md:120` |
| `reference-files/firmware/i2c_debug/i2c_debug.ino` | B1 | `02-sensing-and-hardware-architecture/B1-choosing-the-interface.md:120` |
| `reference-files/images/enclosure-*.png` | E1 | `05-mechanical-3d-design/E1-materials-colour-rendering.md:193` |
| `reference-files/images/enclosure-lid.png` | E0 | `05-mechanical-3d-design/E0-parametric-cad-fundamentals.md:36` |
| `reference-files/images/i2c-debug-output.png` | A2, B5 | `01-system-architecture/A2-operating-modes-and-decisions.md:121`<br>`02-sensing-and-hardware-architecture/B5-virtual-prototyping.md:285` |
| `reference-files/images/jlcpcb-dfm.png` | F2 | `06-sourcing-and-manufacturing/F2-quoting-without-ordering.md:51` |
| `reference-files/images/jlcpcb-order.png` | F2 | `06-sourcing-and-manufacturing/F2-quoting-without-ordering.md:102` |
| `reference-files/images/max30102-green-vs-black.jpg` | B4 | `02-sensing-and-hardware-architecture/B4-component-selection.md:132` |
| `reference-files/images/render-bottom.png` | C0, C2 | `03-form-schematic-and-pcb/C0-form-factor-and-concept.md:76`<br>`03-form-schematic-and-pcb/C2-pcb-layout-and-footprints.md:252` |
| `reference-files/images/render-iso.png` | B4, E2 | `02-sensing-and-hardware-architecture/B4-component-selection.md:74`<br>`05-mechanical-3d-design/E2-pcb-enclosure-co-design.md:64` |
| `reference-files/kicad/MAX30102_Module_21x16mm_2x4_P2.54mm.kicad_mod` | C2 | `03-form-schematic-and-pcb/C2-pcb-layout-and-footprints.md:125` |
| `reference-files/kicad/esp_watch_symbols.kicad_sym` | C1 | `03-form-schematic-and-pcb/C1-schematic-capture-and-symbols.md:193` |
| `reference-files/kicad/make_max30102_footprint.py` | C2 | `03-form-schematic-and-pcb/C2-pcb-layout-and-footprints.md:126` |
| `reference-files/images/assembled-top.jpg`, `assembled-bottom.jpg` (new: board is built) | throughout | not yet referenced; say where you want them |

## 2. Screenshots, photos, GIF and datasheet crops to capture

Each slot is a `<!-- MEDIA ... -->` comment with a full brief of what to capture.

| ID | Type | Caption | Location |
|---|---|---|---|
| A1-01 | screenshot | A context diagram for a wrist-worn tracker, drawn in draw.io | `01-system-architecture/A1-overall-system-architecture.md:96` |
| B3-01 | screenshot | The power budget sheet from esp32c3_watch_bom_power.xlsx | `02-sensing-and-hardware-architecture/B3-electrical-architecture.md:154` |
| B4-01 | datasheet | MAX30102 datasheet: absolute maximum ratings beside the electrical characteristics | `02-sensing-and-hardware-architecture/B4-component-selection.md:102` |
| B4-02 | screenshot | Parametric search for a heart-rate sensor IC on LCSC | `02-sensing-and-hardware-architecture/B4-component-selection.md:187` |
| B5-01 | screenshot | Falstad: rising edges with 4.7 kΩ, 10 kΩ and 1.57 kΩ pull-ups on a 50 pF bus at 400 kHz | `02-sensing-and-hardware-architecture/B5-virtual-prototyping.md:66` |
| B5-02 | screenshot | The virtual watch running in Wokwi, with the serial monitor showing the bus scan and frame times | `02-sensing-and-hardware-architecture/B5-virtual-prototyping.md:201` |
| B5-03 | screenshot | PulseView decoding an I²C read of the MPU-6050, captured from the Wokwi logic analyser | `02-sensing-and-hardware-architecture/B5-virtual-prototyping.md:260` |
| C0-01 | photo | An annotated concept sketch: top and side views, with each constraint labelled | `03-form-schematic-and-pcb/C0-form-factor-and-concept.md:142` |
| C1-01 | screenshot | Drawing a module symbol in KiCad's Symbol Editor | `03-form-schematic-and-pcb/C1-schematic-capture-and-symbols.md:166` |
| C1-02 | screenshot | KiCad's ERC dialog after a clean run | `03-form-schematic-and-pcb/C1-schematic-capture-and-symbols.md:233` |
| C2-01 | photo | Calibrating a module photo: the header pitch used as the ruler | `03-form-schematic-and-pcb/C2-pcb-layout-and-footprints.md:128` |
| C2-02 | screenshot | The MAX30102 module footprint in KiCad's Footprint Editor | `03-form-schematic-and-pcb/C2-pcb-layout-and-footprints.md:140` |
| C2-03 | screenshot | KiCad's DRC dialog after a clean run | `03-form-schematic-and-pcb/C2-pcb-layout-and-footprints.md:289` |
| D0-01 | screenshot | The layered example project open in VS Code with PlatformIO | `04-firmware/D0-firmware-architecture.md:239` |
| D1-02 | screenshot | The state-machine sketch running, with each transition printed in the Serial Monitor | `04-firmware/D1-flowcharts-and-state-diagrams.md:228` |
| D1-01 | screenshot | esp_watch's state diagram rendered in the Mermaid Live Editor | `04-firmware/D1-flowcharts-and-state-diagrams.md:279` |
| D2-01 | screenshot | The non-blocking watch sketch running in Wokwi, with the worst-loop-time messages in the serial monitor | `04-firmware/D2-non-blocking-logic-and-sleep.md:227` |
| D3-02 | screenshot | Wokwi for VS Code forwarding the simulated serial port to the plotting script | `04-firmware/D3-data-off-the-device.md:136` |
| D3-01 | screenshot | The live plot: raw PPG on top, filtered below, where the heartbeat finally appears | `04-firmware/D3-data-off-the-device.md:149` |
| D4-01 | screenshot | A device dashboard answering the four questions: value now, history, status, last seen | `04-firmware/D4-connectivity-and-persistence.md:204` |
| D4-02 | screenshot | MQTT Explorer subscribed to the simulated watch's topics | `04-firmware/D4-connectivity-and-persistence.md:216` |
| D5-01 | screenshot | A crash report decoded by PlatformIO's exception decoder | `04-firmware/D5-debugging-and-robustness.md:95` |
| D5-02 | screenshot | The watchdog at work: a simulated hang, a reset, and the reason logged on the next boot | `04-firmware/D5-debugging-and-robustness.md:168` |
| E0-01 | screenshot | A fully constrained centre rectangle in Fusion, dimensioned with parameter names | `05-mechanical-3d-design/E0-parametric-cad-fundamentals.md:87` |
| E0-02 | screenshot | Fusion's Parameters dialog with the enclosure's user parameters, drivers and formulas | `05-mechanical-3d-design/E0-parametric-cad-fundamentals.md:157` |
| E0-03 | screenshot | The two-part enclosure in Fusion, with its timeline showing the six features in order | `05-mechanical-3d-design/E0-parametric-cad-fundamentals.md:222` |
| E0-04 | gif | Changing one parameter, and watching the whole enclosure follow | `05-mechanical-3d-design/E0-parametric-cad-fundamentals.md:233` |
| E1-01 | photo | The same small test box printed in four finishes: matte grey, silk white, translucent and matte black | `05-mechanical-3d-design/E1-materials-colour-rendering.md:117` |
| E1-02 | screenshot | Fusion's Render workspace with Scene Settings open and in-canvas rendering on | `05-mechanical-3d-design/E1-materials-colour-rendering.md:148` |
| E1-03 | diagram | The same case rendered two ways: a wide-angle top-down view, and the finished presentation image | `05-mechanical-3d-design/E1-materials-colour-rendering.md:196` |
| E2-01 | screenshot | The esp_watch board STEP, with module stand-in boxes, placed inside the enclosure in Fusion | `05-mechanical-3d-design/E2-pcb-enclosure-co-design.md:52` |
| E2-02 | screenshot | Fusion's interference check between the board and the case, with one collision found | `05-mechanical-3d-design/E2-pcb-enclosure-co-design.md:179` |
| E2-03 | screenshot | A section view through the tallest stack, with each gap measured | `05-mechanical-3d-design/E2-pcb-enclosure-co-design.md:189` |
| E3-01 | photo | A clearance test print: four pin-and-hole pairs at 0.1, 0.2, 0.3 and 0.4 mm | `05-mechanical-3d-design/E3-design-for-manufacturing.md:99` |
| E3-03 | photo | Prototype fastening hardware: heat-set inserts, M2/M3 screws, a captive nut and disc magnets, beside the printed features that hold them | `05-mechanical-3d-design/E3-design-for-manufacturing.md:161` |
| E4-02 | screenshot | The battery slot in section, with the swelling gap and the nearest sharp feature measured | `05-mechanical-3d-design/E4-functional-mechanical-design.md:126` |
| E5-01 | screenshot | PrusaSlicer preview of the enclosure base, with supports and the time and material estimate | `05-mechanical-3d-design/E5-slicing-and-printability.md:64` |
| F0-02 | screenshot | Reading a distributor listing: MPN, stock, price breaks and lifecycle in one view | `06-sourcing-and-manufacturing/F0-sourcing-and-lifecycle.md:53` |
| F0-01 | screenshot | The manufacturer's product page for the MPU-6050: status Obsolete, with its recommended alternate | `06-sourcing-and-manufacturing/F0-sourcing-and-lifecycle.md:77` |
| F1-01 | screenshot | A fabrication zip opened in KiCad's Gerber viewer, with each layer listed | `06-sourcing-and-manufacturing/F1-pcb-manufacturing-package.md:144` |
| F1-02 | screenshot | An assembler's placement preview, with one part rotated the wrong way | `06-sourcing-and-manufacturing/F1-pcb-manufacturing-package.md:155` |
| F2-01 | screenshot | A fab house's automated DFM report for a small two-layer board | `06-sourcing-and-manufacturing/F2-quoting-without-ordering.md:53` |
| G-01 | screenshot | A well-organised Design Pack: numbered folders and a one-page README | `07-capstone/G-capstone-design-pack.md:108` |

## 3. Waiting on data that does not exist yet

| What | Unit | Location |
|---|---|---|
| rendered presentation image of the esp_watch enclosure (black PLA) | E1 | `05-mechanical-3d-design/E1-materials-colour-rendering.md:194` |
| esp_watch slicing results (printer, layer height, print time, filament use) and slicer preview screenshot | E5 | `05-mechanical-3d-design/E5-slicing-and-printability.md:108` |

## 4. Feature placeholders (sleep / shake-to-wake)

Marked `<!-- PLACEHOLDER:FEATURE sleep / shake-to-wake -->`. If the feature is added to the firmware, restore it at these spots:

| Unit | Location |
|---|---|
| A0 | `01-system-architecture/A0-product-specification.md:166` |
| A1 | `01-system-architecture/A1-overall-system-architecture.md:185` |
| A2 | `01-system-architecture/A2-operating-modes-and-decisions.md:80` |
| B0 | `02-sensing-and-hardware-architecture/B0-choosing-sensors.md:175` |
| D0 | `04-firmware/D0-firmware-architecture.md:71` |
| D1 | `04-firmware/D1-flowcharts-and-state-diagrams.md:123` |
| D2 | `04-firmware/D2-non-blocking-logic-and-sleep.md:321` |

## 5. Diagrams drawn by Claude: please review

| Diagram | File | Placed at |
|---|---|---|
| B0-01 | `assets/images/B0-01.svg` | `02-sensing-and-hardware-architecture/B0-choosing-sensors.md:63` |
| B0-02 | `assets/images/B0-02.svg` | `02-sensing-and-hardware-architecture/B0-choosing-sensors.md:153` |
| B1-01 | `assets/images/B1-01.svg` | `02-sensing-and-hardware-architecture/B1-choosing-the-interface.md:102` |
| B3-02 | `assets/images/B3-02.svg` | `02-sensing-and-hardware-architecture/B3-electrical-architecture.md:346` |
| E4-01 | `assets/images/E4-01.svg` | `05-mechanical-3d-design/E4-functional-mechanical-design.md:68` |
| G-02 | `assets/images/G-02.svg` | `07-capstone/G-capstone-design-pack.md:237` |
