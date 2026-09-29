# REFERENCE-PRODUCT.md

> **Purpose.** This is the only source of truth about the reference product. Claude Code has no
> other knowledge of this board — it is not public, not searchable, and not in any training data.
> Anything not written here **must not be asserted** in course material. If a unit needs a fact
> that is missing from this file, Claude Code writes a `<!-- FACT:VERIFY ... -->` comment and
> continues; it never guesses.
>
> Facts in §4, §5, §8 and §9 were supplied by the author on 2026-09-24 and are safe to quote.
> Remaining `TODO`s are genuinely unknown. Items the author never did are recorded as
> **out of scope** rather than guessed at.

---

## 1. What it is

**Name:** **esp_watch**. Course material may also say "the reference watch".

**One-line description:** A wrist-worn ESP32-based device that measures heart rate and motion,
shows readings on a small OLED, and runs from a LiPo battery.

**Why it was chosen as the reference:** It is a complete, real product design taken from problem
statement through schematic, custom symbols and footprints, PCB layout, fabrication order and
enclosure CAD — built by the course author, so every file, screenshot and cost figure in this
course is real and unrestricted.

**Status (2026-09-28, author update):** breadboard prototype, firmware and PCB design are done.
Carrier PCB designed in KiCad and **sent to JLCPCB for fabrication; not yet delivered/assembled**.
Enclosure (Onshape; students are taught Fusion 360, told the reference was built in Onshape) and
**real-life testing of the finished watch** are the two things still outstanding. Battery fitted in
the physical build only (not on the PCB).

**Public repository:** [`niat-physicalai/esp_watch`](https://github.com/niat-physicalai/esp_watch)
— README, breadboard photos, schematic and PCB render images, and both firmware projects
(Arduino IDE and PlatformIO) are public there. Treat it as a second source alongside this file;
where the two disagree, flag it rather than silently picking one (see the 2026-09-28 note in §4).

**Firmware language:** Arduino C++ (Arduino IDE and PlatformIO both used — see §8 issues 7–9).

---

## 2. Architecture

```text
                          3.3 V rail (from XIAO 3V3 pin)
                 ┌──────────────┬──────────────┬──────────────┐
                 │              │              │              │
           [ SSD1306 ]    [ MPU-6050 ]   [ MAX30102 ]    4.7 kΩ ×2
           0.96" OLED      6-axis IMU    HR / SpO2      (SDA, SCL)
             0x3C            0x68          0x57         on carrier
                 │              │              │              │
   SDA GPIO6 ────┴──────────────┴──────────────┴──────────────┘
   SCL GPIO7      (one shared I²C bus, 100 or 400 kHz)
                                │ INT → GPIO5   │ INT → GPIO2 (10 kΩ pull-up)
                                ▼               ▼
                      ┌──────────────────────────────┐
   "next"   GPIO10 ──►│                              │
   "prev"   GPIO3  ──►│      XIAO ESP32-C3           │── U.FL ── external antenna
   Batt sense GPIO4 ─►│  (onboard charger, 3.3 V     │           (WiFi / BLE)
   (1 MΩ/1 MΩ + 100 nF)│   regulator, USB-C)          │
                      └──────────────┬───────────────┘
                                     │ BAT+ / BAT− pads
                             optional slide switch
                                     │
                              LiPo cell, 3.7 V
```

**Board sides:**

```text
            TOP (faces the wearer's eyes)
   ┌────────────────────────────────────────┐
   │  SSD1306 OLED · MPU-6050 · XIAO ESP32-C3│
   │  SW1 "next" · SW2 "previous" · SW3 slide│
USB-C ◄── XIAO USB-C port faces the LEFT side of the watch
   ├────────────────────────────────────────┤  ← 38 × 38 mm, 2-layer PCB
   │  MAX30102 (black module)               │
   └────────────────────────────────────────┘
            BOTTOM (touches the wrist)
```

The OLED, MPU-6050, XIAO, both buttons and the slide switch are on the top face. The MAX30102 is
on the underside, so its optical window touches the wrist when the watch is worn.

**Design approach:** carrier PCB plus off-the-shelf breakout modules. The MCU, both sensors and
the display are all pre-made modules mounted on a custom board that carries the
interconnections, switches, the single I²C pull-up pair and mounting. No discrete ICs were placed.

---

## 3. Bill of materials

| Ref | Part | Form | Interface | Source | Unit cost (INR) |
|---|---|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 (with U.FL antenna) | Module | — | see note | see note |
| U2 | MAX30102 heart-rate / SpO2, **black module** (3.3 V I²C reference) | Breakout module | I²C, 0x57 | see note | see note |
| U3 | MPU-6050 6-axis IMU (GY-521-style module; clone, WHO_AM_I = 0x70) | Breakout module | I²C, 0x68 | see note | see note |
| U4 | SSD1306 0.96" OLED, 128×64 | Breakout module | I²C, 0x3C | see note | see note |
| SW1, SW2 | Tactile pushbutton ("next", "previous") | THT | GPIO | see note | see note |
| SW3 | Slide switch, `SW_Ndec_CA5-120A1` (optional, in battery line) | THT | Power | see note | see note |
| R | 4.7 kΩ ×2 (I²C pull-ups), 10 kΩ (MAX INT pull-up), 1 MΩ ×2 (battery divider) | — | — | see note | see note |
| C | 100 nF (battery divider filter) | — | — | see note | see note |
| BT1 | LiPo cell. **Placeholder: 400 mAh, ~20 × 5 × 13 mm** (final choice pending). Earlier candidates: 301235 (~100 mAh), 401235 (~130–150 mAh), 501235 (~170–200 mAh) | Off-board | — | see note | see note |

**Sourcing and cost note.** The author's actual purchase prices are **not recorded**. Units use
current listings from suppliers available in India — Robu, Robocraze, Element14 India, Sunrom,
Mouser India, DigiKey India, LCSC — as **example values**, dated, with USD in brackets for imported
parts. Never present these as the author's real costs.

The full BOM, alternates, pin map, power budget and runtime model live in
`esp32c3_watch_bom_power.xlsx` (§9). Its individual cell values have not been transcribed here.

**Total BOM cost at qty 1:** not recorded — use dated example values.
**PCB fabrication cost:** placeholder — order placed with JLCPCB, invoice not yet available (§6).

---

## 4. Electrical facts

**Pin assignments (XIAO ESP32-C3):**

| XIAO label | GPIO | Signal | Note |
|---|---|---|---|
| D4 | GPIO6 | SDA | XIAO's default I²C pin |
| D5 | GPIO7 | SCL | XIAO's default I²C pin |
| D10 | GPIO10 | Button "next" | to GND, internal pull-up |
| D1 | GPIO3 | Button "previous" | to GND, internal pull-up |
| D2 | GPIO4 | Battery sense | ADC1_CH4, 1 MΩ / 1 MΩ divider + 100 nF |
| D3 | GPIO5 | IMU interrupt | must not be a strapping pin: idles low |
| D0 | GPIO2 | MAX30102 interrupt | 10 kΩ pull-up; open-drain, idles high |
| D8 | GPIO8 | unconnected | strapping pin, must be high at boot |
| D9 | GPIO9 | boot | strapping pin; XIAO has its own button |
| 3V3 | — | 3.3 V rail | OLED, IMU, MAX30102, pull-ups |
| BAT+ / BAT− | — | battery | via optional slide switch to LiPo |

GPIO2, GPIO8 and GPIO9 are strapping pins on the ESP32-C3 and must all be high at reset. The MAX
interrupt's pull-up is what holds GPIO2 high, which is why that interrupt is assigned to GPIO2
rather than GPIO8. The IMU interrupt idles low, so it must not sit on a strapping pin.

<!-- FACT:VERIFY 2026-09-28 — the public README at niat-physicalai/esp_watch says plainly "No
interrupt pins are used for the MPU-6050 or MAX30102", and its own pinout table lists only SDA,
SCL and the two buttons. That contradicts the interrupt wiring above (GPIO5 IMU interrupt, GPIO2
MAX interrupt with a 10 kΩ pull-up), which came from the author directly on 2026-09-24. Do not
teach either version in B3/B4/B5 until the author confirms which is current — the design may
genuinely have dropped interrupt-driven reads in favour of polling, or the README may simply be a
simplified public write-up. Same applies to the battery-sense divider (GPIO4) and the slide switch
(SW3): present in the detailed facts below, absent from the README. -->

Earlier breadboard work used an ESP32 dev module with I²C on GPIO21/22. Those pins do not exist on
the C3.

**I²C addresses:**

| Device | Address | Set by |
|---|---|---|
| SSD1306 OLED | 0x3C | fixed |
| MAX30102 | 0x57 | fixed |
| MPU-6050 | 0x68 | AD0 tied to GND |

No conflict. The MPU's WHO_AM_I register reads 0x70, not the genuine 0x68, which identifies it as
a clone. It works correctly regardless.

**Pull-ups:** one pair only — 4.7 kΩ from SDA and SCL to 3.3 V, on the carrier board. The pull-ups
fitted to the OLED, IMU and MAX modules are removed. Three pairs in parallel gave roughly 1.5 kΩ,
which was one contributor to unreliable operation at 400 kHz.

**Power path:**

```text
LiPo cell (3.7 V) ── optional slide switch ── XIAO BAT+ / BAT− pads
XIAO 3V3 pin ── 3.3 V rail ── OLED, IMU, MAX30102, pull-ups
```

The XIAO ESP32-C3 has a charging IC on board, so no external charger is used. The BAT pads accept a
3.7 V cell only — not 5 V. The onboard regulator holds 3.3 V as the cell falls, and can supply up to
700 mA. Seeed states the board may be connected to USB while running on battery, as it has a
built-in protection chip. The XIAO has no battery-measurement pin, which is why the external divider
on GPIO4 exists.

**Measured figures (breadboard, `i2c_debug` sketch — measurements, not estimates):**

| Configuration | Result |
|---|---|
| Green MAX module on shared 3.3 V bus | bus idle clamped to 1.82 V; MPU 80% of reads failed; MPU often absent from scans |
| Green MAX module alone on its own bus | 0 of 400 reads failed |
| MPU alone, AD0 grounded | 0 of 800 reads failed per round, all four access styles |
| Black MAX + MPU + OLED on one bus | all three found at 100 kHz and 400 kHz; MPU 0/800; MPU accel burst 0/100; MAX 0/400 |
| ADC pins left floating | read 142 mV — not a bus level, an artefact |

**Timing (measured):** a full 128×64 OLED frame takes about 90 ms at 100 kHz (~12 fps) and about
25 ms at 400 kHz (~30 fps). A 200-iteration register read loop takes 92–101 ms.

**Current consumption — MODELLED, NOT MEASURED.** No current measurements were ever taken. These
come from the power model in `esp32c3_watch_bom_power.xlsx` and must always be labelled as modelled.

| State | Current (modelled) | Power at 3.7 V |
|---|---|---|
| Screen on, WiFi connected | ~36 mA | ~135 mW |
| Heart-rate measurement | ~44 mA | ~165 mW |
| WiFi sync burst | ~100 mA average | ~370 mW |
| Optimised idle (light sleep + BLE) | 1–3 mA | 4–10 mW |

Seeed's published figures for the XIAO alone: active below 75 mA, modem-sleep below 25 mA,
light-sleep below 4 mA, deep sleep about 43 µA.

**Usage profile (author's intended firmware behaviour):**
1. First boot: connect to WiFi once, fetch data (time/weather), then WiFi stays **off** for the
   rest of the session.
2. Screen timeout **30 s**. After the timeout the watch enters sleep mode.
3. The MPU-6050 **stays active during sleep** so a wrist shake can wake the watch.
4. Heart-rate (MAX30102) and step/motion features run **on demand**, when the user asks.

**Estimated runtime — ROUGH BALLPARK, derived from modelled currents, not measured.**
Worked example; every assumption is listed so a unit can reproduce or change it.

| Assumption | Value | Basis |
|---|---|---|
| Wakes per day | 50 × 30 s = 25 min screen-on | assumed usage |
| Screen-on current | 36 mA | modelled "screen on, WiFi connected". Conservative, because WiFi is actually off after boot |
| HR measurements | 5 × 30 s = 2.5 min at 44 mA | assumed usage, modelled current |
| Sleep current | 1–3 mA for the remaining ~23.5 h | modelled "optimised idle". The MPU's contribution during sleep is not in the model: FACT:VERIFY |
| First-boot WiFi burst | ~100 mA for a few seconds, once | negligible over a day |
| Battery divider leakage | 3.7 V / 2 MΩ ≈ 1.9 µA | negligible |
| Usable capacity | 80% of rated | assumption |

| Daily charge | Low (1 mA sleep) | High (3 mA sleep) |
|---|---|---|
| Screen on: 0.417 h × 36 mA | 15.0 mAh | 15.0 mAh |
| HR: 0.042 h × 44 mA | 1.8 mAh | 1.8 mAh |
| Sleep: 23.5 h × 1 or 3 mA | 23.5 mAh | 70.6 mAh |
| **Total per day** | **~40 mAh** | **~87 mAh** |

| Cell (usable 80%) | Runtime, low | Runtime, high |
|---|---|---|
| 301235, ~100 mAh (80) | ~2.0 days | ~0.9 days |
| 401235, ~150 mAh (120) | ~3.0 days | ~1.4 days |
| 501235, ~200 mAh (160) | ~4.0 days | ~1.8 days |

Teaching point: under this profile **sleep current dominates** the budget, so the choice of sleep mode
matters more than screen or sensor use.

**Placeholder cell (final cell to be decided by the author):** 400 mAh, about 20 × 5 × 13 mm.
Label it as a placeholder wherever it's used. At 80% usable (320 mAh) the profile above gives
**~8 days (low) to ~3.7 days (high)**.
<!-- FACT:VERIFY placeholder cell: 400 mAh is unusually high for a 20 × 5 × 13 mm (1,300 mm³) LiPo pouch.
     Typical cells of that size are nearer 100–120 mAh. Author to confirm the size or the capacity. -->

**Antenna:** the XIAO ESP32-C3 uses an external antenna on a U.FL connector, supplied with the
board. Requirements: no copper under it on either layer, keep it away from the battery, and route it
along the inside of the case.

---

## 5. KiCad project facts

**Custom schematic symbols:** MAX30102 module, MPU-6050 module, SSD1306 OLED module.
Symbol details (pin count, reference designator prefix, library file) will be added by the author later. Until then units describe the symbols only in general terms.

Note for C1: the bare ESP32-C3 chip symbol is **not** the module. It has XTAL, SPI flash and LNA_IN
pins that the module contains internally.

**Footprints:**

| Part | Source |
|---|---|
| Seeed XIAO ESP32-C3 | Downloaded: `xiao_esp32c3.kicad_mod` + `xiao_esp32c3.kicad_sym` from the open-source repo https://github.com/VectorSpaceHQ/XIAO_ESP32C3 (verified 2026-09-24: KiCad v7 footprint and symbol, battery pads included, GPL-3.0, single maintainer, last commit Sep 2024 with the message "the symbol didn't have the right reference to the footprint. Not sure if this fixes it or not") |
| MAX30102 black module | Generated by the author: `MAX30102_Module_21x16mm_2x4_P2.54mm.kicad_mod` (from `make_max30102_footprint.py`) |
| Module headers | `PinSocket_1x08_P2.54mm_Vertical`, KiCad standard library |

The board uses the **XIAO module only**. There is no bare-chip or ESP32-C3-MINI-1 variant.

**MAX30102 footprint dimensions.** Derived from a calibrated photo, anchored on the 2.54 mm header
pitch (62.2 px pitch → 24.5 px/mm):

| Property | Value |
|---|---|
| Body, measured | 20.2 × 15.6 mm |
| Body, footprint (vendor nominal) | 21 × 16 mm |
| Pads | 2 rows × 4 |
| Pitch | 2.54 mm |
| Row spacing | 10.16 mm (measured 10.3 mm) |
| Drill / pad | 1.0 mm / 1.7 mm |

The footprint marks the sensor package (5.6 × 3.3 mm) on User.Drawings so the enclosure window can
be aligned to it.

**Board:**

| Property | Value |
|---|---|
| Outline | 38 × 38 mm |
| Height with components | 14.044 mm |
| Layers | 2 |
| Thickness | not recorded (not needed) |
| Mounting holes | **4**: two at the top left and top right, two in the middle. They hold the MPU-6050 and OLED modules on standoffs. Diameter and exact positions not recorded |
| Side placement | Top: OLED, MPU-6050, XIAO, SW1, SW2, SW3. Bottom: MAX30102. XIAO USB-C faces left |
| Battery location | stood vertically in the slot behind the OLED header, face about 38 × 14 mm, oriented to minimise height and width |

**Design rules used:**

| Class | Track | Clearance | Via |
|---|---|---|---|
| Default | 0.25 mm | 0.2 mm | 0.6 / 0.3 mm |
| Power (3V3, GND, BAT+, BAT−) | 0.5 mm | 0.2 mm | 0.8 / 0.4 mm |

Constraints set to JLCPCB two-layer minimums: 0.127 mm track and clearance, 0.5 mm via, 0.3 mm
drill, 0.13 mm annular ring, 0.3 mm copper-to-edge.

Ground is poured on both layers and stitched every 5–10 mm. 3.3 V is routed as a track, not a plane
— on two layers a power plane would be cut apart by the routing and would spoil the signal return
paths.

**DRC status:** **zero errors**. Warnings were present. The author judged them acceptable for a hobbyist board and did not fix them. Which warnings they were is not recorded. Teaching point: a warning left in place should be a written, reasoned decision, not an unexamined one.

---

## 6. Fabrication

**Fab house:** JLCPCB. **Export method:** a JLCPCB fabrication plugin for KiCad, which
produces the complete fabrication zip in one action. The version is not relevant to the course and is
not recorded.

**Order:** placed; board is at fabrication and **not yet delivered**. Quantity, options, quoted vs
actual lead time, total cost, customs and GST: **PLACEHOLDER — to be filled when the order
completes.** Units must use a clearly marked placeholder and may use other fab houses (PCBWay,
PCBPower, and other Indian fabs) as illustrative examples.

<!-- NOTE 2026-09-28: author is reviewing F2 (quoting/DFM/cost model) separately and may revise
its figures and structure. Do not treat this section's placeholders as final until that review lands. -->

**DFM feedback received:** TODO — not yet available.

**Assembly:** will be **hand-soldered** once delivered. All components are through-hole, plus a few
larger surface-mount parts that can be soldered by hand. This is a teaching point about
module-based design: no assembly service was needed.

---

## 7. Mechanical

**Enclosure:** almost complete, designed in **Onshape**, to be **3D printed**. The course teaches Fusion 360; students are
told the reference was built in Onshape and that the concepts transfer.

**Known design facts:**
- Top lid with four openings: OLED window, two buttons, one slide switch.
- Lid fit is an **interference fit**.
- Placeholder images and a description exist (placeholder paths in §9).

**Constraints that drove the design:**
- Worn on the wrist: overall thickness, strap attachment, weight. Board stack is 14.044 mm high.
- The MAX30102 is on the **underside** of the board and touches the wrist. The footprint marks the
  sensor package on User.Drawings for aligning a window in the case base (§5). TODO: the design
  of the base window (open cut-out, clear insert, or other).
- The OLED must be visible and its FPC ribbon routed without strain.
- SW1 and SW2 need travel and a reachable actuator.
- SW3 needs an accessible slider.
- The XIAO's USB-C port faces the **left side** of the watch and needs a side opening for charging.
- The LiPo cell needs a retained bay with no risk of puncture. It stands **vertically in the slot behind
  the OLED's header**, oriented to add as little height and width as possible. Placeholder cell:
  400 mAh, ~20 × 5 × 13 mm (§4).
- The antenna is routed along the inside of the case, away from the battery.
- Sweat ingress: TODO.

**Manufacturing process:** 3D printed. Printer type, material, layer height and print time not recorded.
**Fasteners:** lid is an interference fit; anything else TODO.

---

## 8. Known issues and v2 changes

| # | Issue | Symptom | Resolution |
|---|---|---|---|
| 1 | Green MAX30102 module references its I²C lines to an internal 1.8 V rail | Shared bus clamped to 1.82 V; MPU unreadable; OLED corrupted silently | Use the black module, which references 3.3 V |
| 2 | MPU AD0 floating | Device appears and disappears between scans; 6–80% read failures | Tie AD0 to GND |
| 3 | Powering a GY-521 VCC from 5 V | Module stopped responding entirely | Only safe if the board carries its own regulator; use 3.3 V |
| 4 | Adafruit GFX text wrap on by default | Off-screen text during slide animations wrapped onto new lines, looking garbled | `display.setTextWrap(false)` |
| 5 | Three sets of module pull-ups in parallel | 400 kHz unreliable | One 4.7 kΩ pair on the carrier board |
| 6 | Screen blanked after 15 s with no button wired | Appeared as a crash | Screen sleep timeout; set to 0 for testing |
| 7 | Arduino IDE inserts function prototypes above the first function | `'WxType' does not name a type` | Declare enums used as return types before any function |
| 8 | PlatformIO compiles `src/*.cpp` as plain C++ | `'Serial' was not declared` | Add `#include <Arduino.h>` |
| 9 | Two sketches in `src/` | Multiple definition of `setup()` and `loop()` | Separate environments with `build_src_filter` |
| 10 | SparkFun MAX3010x defines its own `I2C_BUFFER_LENGTH` | Redefinition warning | Harmless; the library expects 32 bytes |
| 11 | Margin layer graphics inside a footprint | Router refuses to reach pads | Move those graphics to F.Fab or User.Drawings |
| 12 | Writing to the OLED never fails visibly | A corrupted bus looks healthy because nothing is read back | Judge bus health by a device you read from, not by the display |

Open issues and v2 decisions:
- MPU-6050 lifecycle: formally obsolete (TDK PCN-000614, July 2023). **esp_watch keeps the
  MPU-6050.** The ICM-42670-P is mentioned only as TDK's named alternate for the F0 lifecycle
  lesson and the D0 driver-swap argument. It is not specified in detail anywhere in the course.
- Module stack height (14.044 mm) versus acceptable watch thickness.
- Anything the JLCPCB DFM check flags, and anything found after the board arrives.

---

## 9. Assets — required, all placeholders for now

None of these files are in the course repository yet. Each has a **placeholder path**, and units
reference that exact path so the real file can be dropped in later without editing the prose.
Units mark every use with `<!-- ASSET:PLACEHOLDER <path> -->`. **No unit may quote the contents of
a placeholder file.** Code shown in units is written fresh for the unit.

| # | Asset | Placeholder path | Status | Needed by |
|---|---|---|---|---|
| 1 | KiCad schematic | `reference-files/kicad/esp_watch.kicad_sch` | placeholder | B2, C1, G |
| 2 | KiCad PCB | `reference-files/kicad/esp_watch.kicad_pcb` | placeholder | C2, E2, F1, G |
| 3 | Custom symbol library (MAX30102, MPU-6050, SSD1306) | `reference-files/kicad/esp_watch_symbols.kicad_sym` | placeholder | C1 |
| 4 | MAX30102 footprint | `reference-files/kicad/MAX30102_Module_21x16mm_2x4_P2.54mm.kicad_mod` | exists, not in repo | C2 |
| 5 | Footprint generator script | `reference-files/kicad/make_max30102_footprint.py` | exists, not in repo | C2 |
| 6 | Schematic screenshot | now public: `esp_watch/asset/pcb/Schematic.png` in the repo | **exists in repo** | B2, C1 |
| 7 | PCB render, top view | now public: `esp_watch/asset/pcb/pcb_top.png` | **exists in repo** | C2, E2 |
| 8 | PCB front-copper view | now public: `esp_watch/asset/pcb/pcb_FCu.png` | **exists in repo** | C2, C0, E4 |
| 9 | PCB 3D render, isometric | `reference-files/images/render-iso.png` | placeholder — not seen in the public repo listing | E2, E3 |
| 10 | Photo: green vs black MAX30102 modules side by side | `reference-files/images/max30102-green-vs-black.jpg` | placeholder | B3, B4, B5 |
| 11 | Photo: breadboard prototype | now public: `esp_watch/asset/breadboard/photo_9.jpeg` and others in that folder | **exists in repo** | A2, B5, D5 |
| 12 | Screenshot: `i2c_debug` serial output (scan + read-failure counts) | `reference-files/images/i2c-debug-output.png` | placeholder | B5, B1, D5 |
| 13 | Bus diagnostic sketch | `reference-files/firmware/i2c_debug/i2c_debug.ino` | exists, not in repo | B5, B1, D5 |
| 14 | Watch firmware (3 screens, animations, 2 buttons, steps, HR, WiFi/weather) | now public: `esp_watch/firmware/Arduino-IDE/esp_watch/esp_watch.ino` and `esp_watch/firmware/PlatformIO/esp_watch/` | **exists in repo** | Module 4 (D0–D6) |
| 15 | Original sensor test | `reference-files/firmware/sensor_test/sensor_test.ino` | placeholder — not seen in the public repo listing | B0 |
| 16 | BOM, alternates, pin map, power budget, runtime model (6 sheets) | `reference-files/esp32c3_watch_bom_power.xlsx` | exists, not in repo | B3, B4, F0 |
| 17 | Net-by-net connection list | `reference-files/schematic_netlist.md` | exists, not in repo | B2, C1 |
| 18 | Carrier board build notes | `reference-files/carrier_board_build.md` | exists, not in repo | B2, C2 |
| 19 | Fabrication zip (JLCPCB plugin output) | `reference-files/fab/esp_watch_jlcpcb.zip` | placeholder | F1 |
| 20 | JLCPCB order / quote screenshot | `reference-files/images/jlcpcb-order.png` | placeholder, order in progress | F0, F2 |
| 21 | JLCPCB DFM report screenshot | `reference-files/images/jlcpcb-dfm.png` | placeholder | F2 |
| 22 | Enclosure images (lid, base, exploded) | `reference-files/images/enclosure-*.png` | placeholder images exist — placeholder path | C0, E0–E5 |
| 23 | Enclosure CAD export (STEP) | `reference-files/cad/esp_watch_enclosure.step` | placeholder | E2, E4, E5 |
| 24 | Photo: assembled board, both sides | `reference-files/images/assembled-*.jpg` | placeholder, board not yet delivered | throughout |

---

## 10. Rules for using this file

1. State only what is written above. Anything else gets a `FACT:VERIFY` comment.
2. Wrap product-specific passages in `<!-- REFPRODUCT:START -->` / `<!-- REFPRODUCT:END -->`.
3. The design is a teaching specimen, not a model of perfection. Where it made a debatable
   choice, say so and explain the trade-off. Section 8 exists precisely so students see that a
   real design has open issues.
4. Students are not building this board. They dissect it and design their own.
5. **Current figures are modelled, never measured.** Always label them so.
6. **Costs are example values from current Indian supplier listings**, never the author's actual
   spend. Fabrication cost is a placeholder until the JLCPCB order completes.