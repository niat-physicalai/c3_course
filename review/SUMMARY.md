# Review summary — 2026-09-29

30 units reviewed (A0 from the earlier run). Findings are in `review/findings/<ID>.md`. Tick `[x] accept`, then `/apply-review <ID>`.

**Course total:** 97,158 words now → about 81,775 after all proposed cuts (−16 %). **88 P1**, **321 P2**.

| Unit | Words now | After cuts | P1 | P2 | Verdict |
|---|---|---|---|---|---|
| A0 | 3,395 | 2,780 | 2 | 5 | Invents an esp_watch history ("built before its spec"); retells C0/E2 stories |
| A1 | 4,462 | 3,500 | 2 | 18 | Sound method, heavily padded; "D2 model" should be "C4 model" (renumbering slip) |
| A2 | 3,195 | 2,720 | 4 | 9 | Proposed esp_watch behaviour and motives stated as recorded fact |
| REF | 1,185 | 860 | 0 | 5 | Lists the same checks twice; retells the green-MAX story |
| B0 | 3,620 | 2,945 | 8 | 12 | Worked-example tables invent esp_watch design decisions and a test plan |
| B1 | 3,083 | 2,600 | 3 | 10 | SPI-vs-I²C verdict rests on a disputed pin count |
| B2 | 3,352 | 2,780 | 2 | 10 | Teaches disputed interrupt/divider/switch wiring as fact |
| B3 | 5,119 | 4,000 | 6 | 20 | Teaches disputed wiring as fact; never says sleep current dominates |
| B4 | 4,112 | 3,450 | 4 | 19 | Unconfirmed product details; doubtful 0.7 × VDD rule; every MCQ answer is B |
| B5 | 4,088 | 3,560 | 7 | 10 | Code, simulation and text disagree, so the activities won't show what is promised |
| C0 | 2,813 | 2,370 | 1 | 11 | Sound but padded; the board-outline step has no example |
| C1 | 3,300 | 2,950 | 3 | 8 | Invents esp_watch net names and schematic notes |
| C2 | 4,070 | 3,330 | 2 | 15 | Invented design-rule motive; wrong pin-slack arithmetic |
| D0 | 3,782 | 3,180 | 2 | 14 | Layer diagram leaves the OLED off the bus and adds an unrecorded battery feature |
| D1 | 3,218 | 2,640 | 1 | 11 | State diagram presents unrecorded behaviour as esp_watch's own |
| D2 | 4,947 | 4,170 | 5 | 10 | Light-sleep how-to has a real bug; several sleep figures misstated |
| D3 | 2,841 | 2,510 | 1 | 8 | Filter explanation wrong (0.83 s beat vs 0.5 s window) |
| D4 | 3,296 | 2,950 | 3 | 8 | Two Wokwi Try-its rely on things the simulator can't do |
| D5 | 3,034 | 2,670 | 1 | 13 | Watchdog snippet won't compile; self-check tests a sketch nobody wrote |
| D6 | 1,700 | 1,500 | 3 | 8 | Unsupported BLE figure; wrong firmware file name; short self-check |
| E0 | 3,503 | 2,740 | 1 | 12 | Padded; MCQ 1 explanation arithmetic wrong |
| E1 | 2,930 | 2,560 | 0 | 4 | Clean; only template scaffolding to cut |
| E2 | 3,113 | 2,500 | 5 | 9 | "Display above the motion sensor" invented (3×); wrong USB-C seating rule |
| E3 | 3,411 | 3,080 | 2 | 11 | Boss rule contradicts its own example; lid "opened for charging" is wrong |
| E4 | 3,504 | 3,080 | 5 | 10 | Lug print orientation backwards; illustrative decisions stated as esp_watch's |
| E5 | 1,880 | 1,700 | 3 | 5 | Pause-at-layer MCQ contradicts the body; "elephant's foot" preview row wrong |
| F0 | 2,694 | 2,230 | 2 | 14 | Unsourced qty-10 price; stock table contradicts B4's dated listings |
| F1 | 2,303 | 1,950 | 0 | 12 | Facts fine; padded; wrong drill-file row |
| F2 | 2,166 | 1,910 | 5 | 6 | Cost model charges a prototype 1/5 of a board order (4 linked P1s) |
| G | 3,042 | 2,560 | 5 | 14 | Pack table misses 3 required items; invented esp_watch facts and v2 plan |

## P1 issues across the course (fix first)

**Author decision needed before these can be fixed (one answer clears many P1s):**
- **Interrupt wiring, battery divider, slide switch** (REFERENCE-PRODUCT §4 FACT:VERIFY vs the public README). Taught as fact in B0 F7 · B1 F1, F2 · B2 F1 · B3 F1, F2, F5 · B4 F4 · B5 F2, F3 · C1 F1 · D0 F1. Confirm which is current, and B1's SPI-vs-I²C verdict may reverse.
- **"Display sits above the motion sensor" / stack arrangement** is not in REFERENCE-PRODUCT. It appears in B4 F1, F2 · E2 F2, F3, F5 · G F3. Confirm or remove.
- **Order of spec vs build** ("built before its spec", "no thickness limit"): A0 F2 · G F4. REFERENCE-PRODUCT §1 implies the opposite.

**Invented or unrecorded esp_watch facts:**
- A0 · F1 · `render-bottom.png` is not a §9 asset (also C0).
- A1 · F2 · `render-top.png` is not a §9 asset; use the public `pcb_top.png`.
- A2 · F1–F4 · sleep contribution, failure-table responses and the decision note's reasons are unrecorded.
- B0 · F1–F6 · selection tables invent design responses, rejected alternatives and a test plan.
- B1 · F3 · the ~1.5 kΩ pull-up figure is calculated, not measured by `i2c_debug`.
- B3 · F3 · 44 µA vs REFERENCE-PRODUCT's 43 µA. F4 · invented clone-to-pull-up link.
- C1 · F2, F3 · the schematic's fab notes are invented.
- C2 · F1 and F2 · F1 · the design rules were set *to* JLCPCB minimums, not "more conservative".
- D1 · F1 · button wake, abort path and LED actions are unrecorded.
- D2 · F1–F3 · WiFi burst, not measuring, is the highest state; 30 s is assumed; "60–80 % of the daily charge", not of the battery.
- D4 · F3 · "sends nothing … chosen for privacy" is unrecorded.
- D6 · F1 · the "10 mA with BLE" figure is unsupported. F2 · the firmware is `esp_watch.ino`, not `watch_ui_test.ino`.
- E2 · F1 · XIAO "on a header" is unrecorded.
- E3 · F2 · the lid is not opened for charging (USB-C is on the side).
- E4 · F3, F4 · the 42 × 42 mm case and the feature table are illustrations, not esp_watch facts.
- F0 · F1 · unsourced qty-10 price. F2 · stock status contradicts B4.
- G · F5 · the v2 IMU plan contradicts §8 (esp_watch keeps the MPU-6050).

**Wrong technical content, maths or code:**
- B0 · F8 · arm swing is ~1 per second, not 2.
- B2 · F2 · 23 vs 25 ms is 9 %, not "a few percent".
- B4 · F3 · MAX30102 VIH is likely fixed, not 0.7 × VDD (FACT:VERIFY).
- B5 · F1 · a 10 kΩ pull-up is slow but does not visibly fail. F4 · the SSD1306 library resets the bus clock, so the 100 kHz Try-it shows nothing. F5, F6 · MPU reads are 14 bytes, not 6. F7 · the pull-up/idle-level explanation is wrong.
- C0 · F1 · the thickness was calculated, not measured.
- C2 · F2 · the pin-slack "doubles the misfit" is wrong.
- D2 · F4 · "10× per step" doesn't match the table. F5 · light-sleep bug: a timer wake leaves the watch stuck in ASLEEP with the screen lit.
- D3 · F1 · the filter explanation is backwards.
- D4 · F1 · `WiFi.begin()` doesn't block; the `while` does.
- D5 · F1 · the watchdog snippet won't compile.
- E0 · F1 · the MCQ 1 arithmetic is wrong (40.5 mm).
- E2 · F4 · the USB-C seating rule is wrong.
- E3 · F1 · the boss rule contradicts its own example.
- E4 · F1, F2, F5 · lug print orientation is backwards.
- E5 · F1, F2 · the pause-at-layer answer is wrong. F3 · the preview shows no elephant's foot.
- F2 · F2–F5 · the minimum-order cost is wrong (accept all four together).

**Structure:**
- B3 · F6 · 6 MCQs, not 5.
- D4 · F2 · a Wokwi Try-it can't be done.
- D6 · F3 · 5 self-check items; about 8 needed.
- G · F1, F2 · the pack table omits the B1 interface choices, the E1 material and render, and the E3 hardware list.

## Repeated stories — who should own each

| Story | Owner | Units that should replace it with a one-line pointer |
|---|---|---|
| Green MAX30102 / 1.82 V bus clamp | B3 | A2, REF, B1, B2, B4, B5, C1 |
| Three pull-up pairs in parallel (~1.5 kΩ) | B3 | B1, C1 |
| Strapping pins GPIO2/8/9 | B3 | B1, G |
| Clone MPU-6050 (WHO_AM_I 0x70) | **B3** (CURRICULUM says B1, but B1 never tells it; change the owner table) | B1, D0 |
| AD0 floating / I²C addresses | B1 | B2, B3, B5, C1, D5 |
| Board sides, sensor orientation | C0 | A0, C2 |
| Module stack height 14.044 mm | E2 | A0, A1, B4, C0, E0, E3, G |
| OLED write never fails visibly | D5 | A2, B1 |
| MPU-6050 obsolescence / ICM-42670-P | F0 | B4, D0, G |
| `'WxType' does not name a type` build error | D1 | D0 |

## Patterns the build prompt keeps producing

- **Template scaffolding survives in nearly every unit:** the labels box, "What Part 1 Already Covered", "What You Can Now Do" and "Note on numbers". *Rule: these sections do not exist except the labels box in A0; the numbers note is replaced by labelling each example value where it appears.*
- **Worked examples narrate esp_watch decisions nobody recorded:** tables of "esp_watch's" responses, rejected options, test plans and motives. *Rule: a reference-watch claim is either quoted from REFERENCE-PRODUCT.md or written as "a design like esp_watch could…". Anything under a FACT:VERIFY in REFERENCE-PRODUCT (§4 wiring) is never taught as fact.*
- **Try-its duplicate the end activity or an MCQ.** *Rule: a Try-it must practise something no activity or MCQ asks for, or it is left out.*
- **MCQs test recall, reuse the worked example's numbers, or give away the answer** (always B, or the longest option). *Rule: every MCQ uses new numbers or a new scenario; correct letters are spread across A–D; the correct option is not the longest.*
- **Code and simulator claims are written without running the asset:** byte counts, library clock defaults, what Wokwi can simulate. *Rule: every claim about what a sketch or simulation shows is checked against the file in `assets/code/`, and every snippet compiles as shown.*
- **Arithmetic in worked examples and MCQ explanations is not re-checked.** *Rule: recompute every number in the "Check" step and in each MCQ explanation before marking a unit DRAFTED.*

## Units to consider cutting or merging

None. The findings support trimming every unit (10–22 %), but no unit is out of scope or redundant as a whole. REF duplicates itself internally (F-level fix), not another unit.

## Notes

- **Errors introduced during the 2026-09-29 restructure:**
  - Content edits (my own, since the reviews ran on the new text): D2 F1–F5 (sleep section), E3 F1–F2 (fastening section), E5 F1–F2 (pause-at-layer), F0 F1 (qty-10 price) and F2 F2–F5 (cost model).
  - Renumbering slips: A1 F1 ("D2 model"), E4 line 162 ("a E2 section") and `assets/code/C2-header-module-footprint.py` (`generator "c3_course_B5"`, outside the findings).
  - G F1–F2 and C0's missing outline example also come from CURRICULUM changes not carried through.
- **Content the reviewers would not add** (their rule is to cut, not add), for the author to decide:
  - B1 never tells the clone story it is assigned.
  - B3 lacks deep-sleep wake pins in the pin budget.
  - B5 doesn't name LTspice.
  - E4 lacks FPC routing (F11 proposes one sentence).
  - C0's board-outline step needs an example (a proposal is in C0.md).
