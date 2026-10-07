# Assets still to supply

Generated 2026-10-01. Line numbers are as of this date; the placeholder ID (or path) is the stable thing to search for.

Put each real file at the path shown, then tell Claude to swap the placeholder for the image. Images already in the public repo (`asset/pcb/Schematic.png`, `pcb_top.png`, `pcb_FCu.png`, `asset/breadboard/photo_9.jpeg`) are now linked directly and are not listed.

## 1. Reference files from you

Updated 2026-10-01 from the author's reference column.

| File | Used in | Status |
|---|---|---|
| Fabrication zip | F1 | **Done**: linked to repo `fabrication/Gerber/esp_watch.zip` |
| `i2c_debug` sketch | B1 | **Done**: linked to repo `firmware/PlatformIO/esp_watch/src/i2c_debug.cpp` |
| JLCPCB DFM screenshot | F2 | **Done**: embedded `asset/pcb/DFM_check.png` (replaced the generic F2-01 slot) |
| JLCPCB quote screenshot | F2 | **Done**: embedded `asset/pcb/JLCPCB_quote.png` |
| PCB underside render | C0, C2 | **Done**: embedded `asset/pcb/pcb_back.png` |
| PCB angled / stack render ("render-iso") | B4, E2 | **Done**: B4 uses `pcb_front.png` (angled 3D view), E2 uses `pcb_side.png` (stack height) |
| Symbol library | C1 | **Done**: linked to repo `pcb/esp_Watch/symbol.kicad_sym` |
| Footprint generator script | C2 | **Done**: removed; there is no script |
| Assembled board, top | F1 | **Done**: embedded `asset/Assembled/Top_assembled.png` |
| Assembled board, bottom | F1 | Waiting: placeholder `reference-files/images/assembled-bottom.jpg` |
| Enclosure images | E0, E1 | Waiting: placeholders kept (being made) |
| `i2c_debug` serial output screenshot | A2, B5 | Waiting: placeholder kept |
| Green vs black MAX30102 photo | B4 | Partly: the third-party pinout image is **linked, not embedded**. The Google thumbnail URL was not used because it is not a stable source. Your own side-by-side photo is still wanted. |
| MAX30102 footprint file | C2 | **Done**: author's file copied to `assets/kicad/MAX30102_module.kicad_mod` and linked; C2's worked example rewritten for its SMD pads |

## 2. Screenshots, photos, GIF and datasheet crops to capture

Each slot is a `<!-- MEDIA ... -->` comment with a full brief of what to capture.

| ID | Type | Caption | Location | reference |
|---|---|---|---|---|
| A1-01 | screenshot | A context diagram for a wrist-worn tracker, drawn in draw.io | `01-system-architecture/A1-overall-system-architecture.md:96` |  |
| B3-01 | screenshot | The Power Budget sheet from esp32c3_watch_bom_power.xlsx | `02-sensing-and-hardware-architecture/B3-electrical-architecture.md:154` | **Done** (2026-10-07): embedded as `assets/images/B3-01.png` (renamed from `A1-01.png`). It shows the Power Budget sheet, so the caption now says so |
| B4-01 | datasheet | MAX30102 datasheet: absolute maximum ratings beside the electrical characteristics | `02-sensing-and-hardware-architecture/B4-component-selection.md:102` | Waiting: the PDF in `reference/` is truncated (34 KB, will not open). Put the full Analog Devices datasheet there and Claude will crop the two tables |
| B4-02 | screenshot | Parametric search for a heart-rate sensor IC on LCSC | `02-sensing-and-hardware-architecture/B4-component-selection.md:187` | Answered in `review/CAPTURE-GUIDE.md` (B4-02): steps and code. Need |
| B5-01 | screenshot | Falstad: rising edges with 4.7 kΩ, 10 kΩ and 1.57 kΩ pull-ups on a 50 pF bus at 400 kHz | `02-sensing-and-hardware-architecture/B5-virtual-prototyping.md:66` | Answered in `review/CAPTURE-GUIDE.md` (B5-01): steps and code. Need |
| B5-02 | screenshot | The virtual watch running in Wokwi, with the serial monitor showing the bus scan and frame times | `02-sensing-and-hardware-architecture/B5-virtual-prototyping.md:201` | Answered in `review/CAPTURE-GUIDE.md` (B5-02): steps and code. Need |
| B5-03 | screenshot | PulseView decoding an I²C read of the MPU-6050, captured from the Wokwi logic analyser | `02-sensing-and-hardware-architecture/B5-virtual-prototyping.md:260` | Answered in `review/CAPTURE-GUIDE.md` (B5-03): steps and code. Need |
| C0-01 | photo | An annotated concept sketch: top and side views, with each constraint labelled | `03-form-schematic-and-pcb/C0-form-factor-and-concept.md:142` | Answered in `review/CAPTURE-GUIDE.md` (C0-01): steps and code. Need |
| D0-01 | screenshot | The layered example project open in VS Code with PlatformIO | `04-firmware/D0-firmware-architecture.md:239` | **Done** (2026-10-07): embedded in D0's build-problems section as esp_watch's own PlatformIO project. **Check:** it shows `board = seeed_xiao_esp32s3`; esp_watch is a C3 (`seeed_xiao_esp32c3`). Fix and recapture, or confirm |
| D1-02 | screenshot | The state-machine sketch running, with each transition printed in the Serial Monitor | `04-firmware/D1-flowcharts-and-state-diagrams.md:228` | Answered in `review/CAPTURE-GUIDE.md` (D1-02): steps and code. Need |
| D1-01 | screenshot | esp_watch's state diagram rendered in the Mermaid Live Editor | `04-firmware/D1-flowcharts-and-state-diagrams.md:279` | Answered in `review/CAPTURE-GUIDE.md` (D1-01): steps and code. Need |
| D2-01 | screenshot | The non-blocking watch sketch running in Wokwi, with the worst-loop-time messages in the serial monitor | `04-firmware/D2-non-blocking-logic-and-sleep.md:227` | Answered in `review/CAPTURE-GUIDE.md` (D2-01): steps and code. Need |
| D3-02 | screenshot | Wokwi for VS Code forwarding the simulated serial port to the plotting script | `04-firmware/D3-data-off-the-device.md:136` | Answered in `review/CAPTURE-GUIDE.md` (D3-02): steps and code. Need |
| D3-01 | screenshot | The live plot: raw PPG on top, filtered below, where the heartbeat finally appears | `04-firmware/D3-data-off-the-device.md:149` | Answered in `review/CAPTURE-GUIDE.md` (D3-01): steps and code. Need |
| D4-01 | screenshot | A device dashboard answering the four questions: value now, history, status, last seen | `04-firmware/D4-connectivity-and-persistence.md:204` | Answered in `review/CAPTURE-GUIDE.md` (D4-01): steps and code. Need |
| D4-02 | screenshot | MQTT Explorer subscribed to the simulated watch's topics | `04-firmware/D4-connectivity-and-persistence.md:216` | Postponed by the author until the v2 firmware (MQTT not used in esp_watch yet). Placeholder kept |
| D5-01 | screenshot | A crash report decoded by PlatformIO's exception decoder | `04-firmware/D5-debugging-and-robustness.md:95` | Answered in `review/CAPTURE-GUIDE.md` (D5-01): steps and code. Need |
| D5-02 | screenshot | The watchdog at work: a simulated hang, a reset, and the reason logged on the next boot | `04-firmware/D5-debugging-and-robustness.md:168` | Answered in `review/CAPTURE-GUIDE.md` (D5-02): steps and code. Need |
| E1-01 | photo | The same small test box printed in four finishes: matte grey, silk white, translucent and matte black | `05-mechanical-3d-design/E1-materials-colour-rendering.md:117` | Answered in `review/CAPTURE-GUIDE.md` (E1-01): steps and code. Need |
| E1-02 | screenshot | The coloured case in Fusion's Design workspace, ready to capture | `05-mechanical-3d-design/E1-materials-colour-rendering.md:148` | will share later |
| E1-03 | diagram | The same case captured two ways: a careless view, and the finished presentation image | `05-mechanical-3d-design/E1-materials-colour-rendering.md:196` | will share later |
| E3-01 | photo | A clearance test print: four pin-and-hole pairs at 0.1, 0.2, 0.3 and 0.4 mm | `05-mechanical-3d-design/E3-design-for-manufacturing.md:99` | **Done** (2026-10-07): embedded at the end of E3's Clearance section, credited to the Bambu Lab Wiki |
| E3-03 | photo | Prototype fastening hardware: heat-set inserts, M2/M3 screws, a captive nut and disc magnets, beside the printed features that hold them | `05-mechanical-3d-design/E3-design-for-manufacturing.md:161` | **Done** (2026-10-07): embedded beside E3's heat-set insert example, credited to CNC Kitchen |
| E4-02 | screenshot | The battery slot in section, with the swelling gap and the nearest sharp feature measured | `05-mechanical-3d-design/E4-functional-mechanical-design.md:126` | yet to be done will add later |
| E5-01 | screenshot | Bambu Studio preview of the enclosure base, with supports and the time and material estimate | `05-mechanical-3d-design/E5-slicing-and-printability.md:64` | Will add later. Brief and caption switched to **Bambu Studio** |
| F0-02 | screenshot | Reading a distributor listing: MPN, stock, price breaks and lifecycle in one view | `06-sourcing-and-manufacturing/F0-sourcing-and-lifecycle.md:53` | Answered in `review/CAPTURE-GUIDE.md` (F0-02): steps and code. Need |
| F0-01 | screenshot | The manufacturer's product page for the MPU-6050: status Obsolete, with its recommended alternate | `06-sourcing-and-manufacturing/F0-sourcing-and-lifecycle.md:77` | Answered in `review/CAPTURE-GUIDE.md` (F0-01): steps and code. Need |
| F1-01 | screenshot | A fabrication zip opened in KiCad's Gerber viewer, with each layer listed | `06-sourcing-and-manufacturing/F1-pcb-manufacturing-package.md:144` | **Done** (2026-10-07): embedded `assets/kicad/F1-01.png` (esp_watch's ordered Gerbers in GerbView) |
| F1-02 | screenshot | An assembler's placement preview, with one part rotated the wrong way | `06-sourcing-and-manufacturing/F1-pcb-manufacturing-package.md:155` | assembler part is not covered yet, might add later, keep placeholder for now |
| F2-01 | screenshot | **Done** (real DFM screenshot used) | `06-sourcing-and-manufacturing/F2-quoting-without-ordering.md:53` | https://github.com/niat-physicalai/esp_watch/blob/main/asset/pcb/DFM_check.png |
| G-01 | screenshot | A well-organised Design Pack: numbered folders and a one-page README | `07-capstone/G-capstone-design-pack.md:108` | **Done** (2026-10-07): slot replaced by links to the esp_watch repo and its KiCad folder |

## 3. Waiting on data that does not exist yet

| What | Unit | Location |
|---|---|---|
| presentation image (coloured-model screenshot) of the esp_watch enclosure (black PLA) | E1 | `05-mechanical-3d-design/E1-materials-colour-rendering.md:194` |
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

## 6. Walkthrough assets: KiCad, Fusion, 3D models and version control

Added 2026-10-06 for the restructure in `PROGRESS.md` (C1 and C3 KiCad walkthroughs, C2 symbols and footprints, the E0 Fusion walkthrough, E2 3D models, and `REF-version-control.md`).

**How to capture.**
- **Software and project:** KiCad **10.0**, in one theme throughout. Capture on **esp_watch's own project** (`pcb/esp_Watch/`), except the new-project steps.
- **Files:** save as PNG under `assets/kicad/` (KiCad) or `assets/fusion/` (Fusion), named `<ID>-<short-name>.png`.
- **Cropping:** crop each shot to the dialog or area that matters. Use the full window only where the table says so.
- **GIFs:** 5–10 s, about 1000 px wide, no cursor wandering.
- **Callouts:** leave them off. Claude adds numbered callouts.
- **Your own design:** where a shot shows something about esp_watch that the files don't record, add a one-line note in the "reference" column.

Slots that this section **replaces** (do not capture them separately): C1-01, C1-02, C2-02, C2-03, E0-01, E0-02, E0-03, E2-01, E2-02, E2-03.

### 6a. C1: KiCad schematic walkthrough

| ID | Step | What to capture | Status | reference |
|---|---|---|---|---|
| C1-W01 | Create the project | New-project dialog, location, project type | **Done**: embedded in C1 Step 1; checked against the text 2026-10-07 |  |
| C1-W02 | Open the schematic editor | Project manager with the schematic file highlighted | **Done**: embedded in C1 Step 2; checked 2026-10-07 |  |
| C1-W03 | The window | Full window, empty sheet | **Done**: embedded in C1 Step 2 |  |
| C1-W04 | Page settings | Page Settings dialog with title, revision and date filled | **Done**: `Drawing_sheet_properties1.png` (right-click → Properties), `…properties2.png` (dialog), `Drawing_sheet_table.png` embedded in C1 Step 3 |  |
| C1-W05 | Place a symbol (A) | Symbol chooser | **Done**: the generic Choose Symbol shot stays; the recapture slot is removed |  |
| C1-W06 | Place power (P) | Power-symbol chooser | **Done**: embedded in C1 Step 5 |  |
| C1-W07 | Draw wires (W) | **GIF**: wiring one button from D10 to GND on the esp_watch sheet | **Done**: `C1-W07.gif` embedded in C1 Step 6 |  |
| C1-W08 | Net labels (L) | SDA/SCL labels on the XIAO and two modules, so the connection is visible without wires | **Done**: W08 (button), W082 (Label Properties), W083 (placing SCL) embedded in Step 7. Step 7 now explains: type the name, OK, then click on the wire; a label needs a name; esp_watch's SDA/SCL are global labels, which behave like net labels on one sheet |  |
| C1-W09 | No-connect flags (Q) | The XIAO's unused pins (D0, D2, D3, D8) with no-connect flags | **Done**: W09 (button) and W092 (MAX30102 flags) embedded in Step 8 |  |
| C1-W10 | Symbol properties (E) | U1's properties dialog: Reference, Value, Footprint and Datasheet fields | **Done**: embedded in Step 9 (MAX30102 module's properties) |  |
| C1-W11 | Annotate | Annotate Schematic dialog (the icon alone is not enough) | Need: see `review/CAPTURE-GUIDE.md` (C1-W11). It is the Annotate Schematic dialog, not Place Text |  |
| C1-W12 | Assign footprints | Assign Footprints window, with every esp_watch symbol given a footprint | **Done**: W12, W122, W123 embedded in Step 11, with your workflow (library → symbol → double-click footprint; View Selected Footprint; check size and availability) written in |  |
| C1-W13 | ERC with an error | ERC dialog listing one error (e.g. a pin left unconnected on purpose), and its arrow marker on the sheet | **Done**: embedded in Step 12. Step 12 now gives both fixes: PWR_FLAG (recommended) or ignoring the test after a manual check, as esp_watch does; library-mismatch warning added to the table |  |
| C1-W14 | ERC clean | ERC dialog with 0 errors and 0 warnings | **Done**: embedded in Step 12 |  |
| C1-W15 | Finished schematic | Full sheet of esp_watch's schematic, readable at 100% | **Done**: the repo's `asset/pcb/Schematic.png` is used at the top of C1 |  |
| C1-T | Tool table icons | Place symbol, power, wire, net label, no-connect, junction, annotate, ERC, assign footprints, highlight nets, switch to PCB | **Done**: the table lists only the common tools (symbol, power, wire, net label, no-connect, junction, highlight, annotate, footprints, ERC, symbol editor, switch to PCB). Broken icon paths fixed to W08/W09/W12 |  |

### 6b. C2: symbols and footprints

| ID | Step | What to capture | Status | reference |
|---|---|---|---|---|
| C2-W01 | Open the Symbol Editor | Symbol Editor window with the project library in the tree | **Have**: icon `tools/symbol_editor.png`. Need: the window | |
| C2-W02 | New symbol | New Symbol dialog (name, reference designator) | Need | |
| C2-W03 | Add a pin | Pin Properties dialog: name, number, **electrical type** open as a dropdown | Need | |
| C2-W04 | Finished symbol | Your MPU-6050 (or MAX30102) module symbol, all pins placed | Need | |
| C2-W05 | Project libraries | **Not needed**: C2 creates the library with File → New Library → Project, which registers it | — | |
| C2-W06 | Calibrated photo | Module photo with the 2.54 mm edge pads used as the ruler (was C2-01) | Need (C2-01) | |
| C2-W07 | Footprint Editor | Footprint Editor with `MAX30102_module` open | **Have**: icon `tools/footprint_editor.png`. Need: the window | |
| C2-W08 | SMD pad | Pad Properties dialog for one MAX30102 pad: SMD, 2 × 3 mm, F.Cu/F.Paste/F.Mask | Need | |
| C2-W09 | Layers | Footprint Editor's layer list, with F.Fab / User.Drawings and Margin visible (known issue 11) | Need | |
| C2-W10 | Manage footprint libraries | **Not needed** (as C2-W05) | — | |

### 6c. C3: KiCad PCB layout walkthrough

| ID | Step | What to capture | Status | reference |
|---|---|---|---|---|
| C3-W01 | Switch to the PCB | PCB Editor first view, with the Layers and Appearance panels | **Have**: icon `tools/switch_to_pcb_editor.png`. Need: the full window | |
| C3-W02 | Board setup | Board Setup → Design Rules → Constraints, with the fab house's minimums entered | Need | |
| C3-W03 | Net classes | Board Setup → Net Classes: Default and a wider Power class | Need | |
| C3-W04 | Update from schematic | Update PCB from Schematic dialog, then the parts dropped in a heap with their unrouted connections showing | Need (2 shots) | |
| C3-W05 | Board outline | The 37.8 × 39 mm outline on Edge.Cuts, with a dimension on each side | Need | |
| C3-W06 | Mounting holes | Mounting-hole footprints placed, if esp_watch has them (note it if it does not) | Need | |
| C3-W07 | Placement | Parts placed, before routing: USB-C edge, MAX30102 on the underside, antenna end clear | Need | |
| C3-W08 | Flip to the bottom | The MAX30102 footprint flipped to B.Cu (F key), seen from below | Need | |
| C3-W09 | Route a track (X) | **GIF**: routing SDA from the XIAO to a module; track-width selector visible | Need | |
| C3-W10 | Via | A via dropped mid-route to change layer (V while routing) | Need | |
| C3-W11 | Ground pour | Copper Zone Properties dialog (GND, both layers), then the filled board (B to fill) | Need (2 shots) | |
| C3-W12 | Antenna keep-out | Rule Area dialog (no copper, no tracks), and the area on the board | Need | |
| C3-W13 | DRC with errors | DRC dialog with one or two violations and their markers | Need | |
| C3-W14 | DRC clean | DRC dialog, 0 violations, 0 unconnected (was C2-03) | Need | |
| C3-W15 | 3D viewer | Top and bottom 3D views (repo `pcb_front.png` / `pcb_back.png` may serve, if current) | Partly have | |
| C3-W16 | Export STEP | File → Export → STEP dialog, with its options | Need | |
| C3-T | Tool table icons | Route track, via, zone, rule area, measure, DRC, 3D viewer, flip, update from schematic | Need: icon crops, same style as `schematic_view/tools/` | |

### 6d. 3D models for the board and the enclosure (E2)

Say which you have. Put each at `pcb/esp_Watch/3d/` in the esp_watch repo, assigned in KiCad's footprint 3D tab, or note "none".

| Part | Model needed | Status | reference |
|---|---|---|---|
| XIAO ESP32-C3 | STEP | **Have** in repo: `pcb/esp_Watch/3d models/Seeed Studio XIAO-ESP32-C3.step` | |
| MAX30102 module, black | STEP | **Have** in repo: `MAX30102_MH_ET_LIVE_BOARD_v8.step` | |
| MPU-6050 (GY-521) module | STEP | **Have** in repo: `MPU6050 v2.step` | |
| SSD1306 0.96" OLED module | STEP | **Have** in repo: `Pantalla OLED 0.96'' 128x64.stp` | |
| Female header 1×4 | STEP | **Have** in repo: `Female 4 Pin Header.step` | |
| SW1, SW2 tactile buttons | KiCad library model (`SW_PUSH_6mm`) | Probably built in: confirm it shows in the 3D viewer | |
| SW3 Würth WS-SLTV | **Have** (in repo) | have | |
| LiPo 300 mAh, 30 × 12 × 4 mm | stand-in box is enough | Not in repo: model it in Fusion | |
| Whole board | STEP | **Have** in repo: `pcb/esp_Watch/esp_Watch.step` | |
| C2-W11 | KiCad footprint Properties → 3D Models tab, MAX30102 module STEP assigned, offset fields and preview visible (used in C2 Step 8) | Need | |

### 6e. E0 and E2: Fusion walkthrough

Capture in Fusion while modelling the esp_watch case. The case doesn't need to match the Onshape one exactly; the steps matter more than the shape.

| ID | Step | What to capture | Status | reference |
|---|---|---|---|---|
| E0-W01 | The window | Full Fusion window: browser, toolbar, canvas, ViewCube, navigation bar, timeline (Claude labels them) | Need | |
| E0-W02 | Parameters | Change Parameters dialog: the user parameters from E0 Step 2 (`pcb_w`, `pcb_l`, `stack_h`, `clearance`, `wall`, …) with the formulas evaluated (was E0-02) | Need | |
| E0-W03 | Sketch on a plane | Create Sketch, cursor over the flat origin plane | Need | |
| E0-W04 | Constrain | Centre rectangle, dimensioned `outer_w` / `outer_l` (showing "fx:"), all lines black (fully constrained) (was E0-01) | Need | |
| E0-W05 | Extrude | Extrude dialog, Distance `outer_h`, Operation New Body | Need | |
| E0-W06 | Fillet | Fillet dialog on the four vertical edges, radius `corner_r` | Need | |
| E0-W07 | Shell | Shell dialog with the body selected (no faces removed), Inside Thickness `wall`, inside visible | Need | |
| E0-W08 | Split into base and lid | Split Body dialog with the offset plane, and the bodies `base` and `lid` in the browser | Need | |
| E0-W09 | Timeline | Finished case, lid lifted, with its timeline: sketch, extrude, fillet, shell, plane, split, sketch, cut (was E0-03) | Need | |
| E0-W10 | Parameter change | **GIF**: change `pcb_w` and the whole case follows (was E0-04) | Need | |
| E2-W01 | Insert the board | Board STEP uploaded and inserted into the E0 case (Data Panel → Insert into Current Design), grounded as `pcb_v1`, with the battery box (was E2-01) | Need | |
| E2-W02 | Interference | Inspect → Interference, with one collision found (was E2-02) | Need | |
| E2-W03 | Section | Section Analysis through the tallest stack, gaps measured (was E2-03) | Need | |
| E2-W04 | Export (used in E5) | Right-click a body → Save As Mesh: STL/3MF of the base and lid | Need | |

### 6f. Version control (`REF-version-control.md`)

| ID | What | Status | reference |
|---|---|---|---|
| VC-01 | GitHub Desktop: the changed-files list and a commit message (any esp_watch change) | Need | |
| VC-02 | The esp_watch repository's folder layout on GitHub (firmware, pcb, fabrication, asset) | Need, or Claude links the live repo | |
| VC-03 | A tag or release on GitHub marking the version sent to JLCPCB | The repo has **no tags** (checked 2026-10-06). Either create `v0.1.0` on the ordered commit and screenshot it, or the page uses an illustration | |
| VC-04 | A root `.gitignore` with KiCad entries | **Not needed**: the page gives one to copy. Optional: add it to the esp_watch repo root | |
