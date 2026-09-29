# Curriculum audit — 2026-09-29

Inputs: `review/REQUIREMENTS.md`, `CURRICULUM.md`, `REFERENCE-PRODUCT.md`, `PROGRESS.md`,
`old_prompt.md` (the original full build prompt), `COURSE-BUILD-PROMPT-v2.md` (the patch record only),
`review/lint-report.md`. `review/SUMMARY.md` does not exist yet.

**Length policy used in this audit (author, 2026-09-29):** no word targets and no word ceiling.
A unit is as long as a student needs to understand its `CURRICULUM.md` row and produce its
deliverable, and no longer.

> **Applied 2026-09-29.** The decisions below have been applied to `CURRICULUM.md`, `PROGRESS.md` and the unit files, and the course was renumbered (see `PROGRESS.md` "Was" column). **Unit IDs in this audit are the old ones.** Hours in the final curriculum: 36.5 (E2/F2 quoting kept at 1.0 h because the real order will be added; C4/D2 grew to 2.0 h for sleep modes).

## Author decisions on this audit (2026-09-29)

| Item | Decision | Status |
|---|---|---|
| MCQs and self-checks | Required in **every** unit | Kept (see §4) |
| "Present and substantial", ≥ 2 Try-its, 5-step activities, 2–4 Parts per unit | Drop | Decided (see §4) |
| Real invoice / real order | Author will add the real figures once the JLCPCB order completes | Deferred to the author |
| "a v2 will change the driver" (C0) | Remove | **Done:** the sentence was cut from the C0 row in `CURRICULUM.md`. No unit file repeats it. |
| Injection moulding and other niche topics | Shrink to a short mention; don't cut completely | Decided (see §2) |
| D3 DFM | Refocus on rapid prototyping: FDM/3D printing, threaded and heat-set inserts, magnets, M3/M4 screws, snap fits, fit tolerances | Decided (see §2, §5) |
| Deep sleep: C7 → core | Moved into C4 (now D2) with modem / light / deep sleep, when and how | **Done** |

## 1. Coverage

| Requirement | Unit(s) | Status | Note |
|---|---|---|---|
| Basic electronics | Part 1 prerequisite; B1, B3 | Covered | Assumed from Part 1 (§0). B1/B3 revisit dividers, pull-ups and rails one level up. |
| Basic circuit | B3, B4 | Covered | Simulated in B3, drawn as a schematic in B4. |
| Researching components / datasheets | B2, E0 | Covered | B2 teaches datasheet reading, including module vs chip datasheets. |
| Choosing the right component | B2, C3 | Covered | C3 covers sensors, B2 modules vs ICs. |
| Building a POC on Zero board / breadboard | B3 (virtual stand-in) | Out of scope by design | Author decision 2026-09-28: happens in the funded build. |
| Debugging (hardware) | B3, C2 (bus failures as captures) | Out of scope by design | Only paper and simulation versions are taught. The reference's I²C failures carry it. |
| PCB design software | B4, B5 | Covered | KiCad. |
| PCB design | B5, D2, E1 | Covered | |
| Firmware architecture | C0 (A1 at system level) | Covered | |
| Programming logic | C1, C4 | Covered | |
| Memory management | — | Out of scope by design | Author decision 2026-09-28. |
| Debugging (software) | C6 | Covered | |
| Production-ready code | C4, C5b, C6; C7 (OTA, tests) | Partly | Robustness is covered. Unit testing and OTA are only a reading in C7. |
| Design thinking | Part 2; A0, D0 | Partly | Ideation lives in Part 2. C3 only applies it (spec, concept sketches). |
| 2D sketching | D0, D1 | Covered | Concept sketches (D0) and constrained CAD sketches (D1). |
| 3D sketching if required | D1 | Covered | |
| Basic & advanced CAD tools | D1, D2, D4 | Partly | "Advanced" = assemblies and interference checks. No surfacing or ergonomic modelling. That is enough for this course. |
| Component searching | B2, E0, D3 (mechanical hardware) | Covered | |
| Rendering, material, colour | D1b | Covered | New unit, added 2026-09-28. |
| Material selection | D1b | Covered | Limited to FDM materials. |
| Fabrication practices | D3, D5, E1 | Covered | Stops at the slicer and the fab package. |
| 3D printing | D5 (up to slicing) | Out of scope by design | Author decision 2026-09-28: printing happens in the funded build. |
| Overall intent: problem → product | A0 → F | Covered | The Design Pack (F) is the product-level output. |

## 2. Beyond the brief

| Content | Where | Why the student doesn't need it | Action | Hrs saved |
|---|---|---|---|---|
| Injection moulding contrast (draft, ribs, gate location, tooling cost, 10,000 units) | D3 | No requirement asks for it. The student prototypes by 3D printing. | Shrink to a short mention: what changes at volume and why real watch cases are moulded. Use the freed time for prototype DFM: FDM limits and fit tolerances; threaded/heat-set inserts; M3/M4 screws and bosses; magnets; snap fits. | 0 (time moves to prototype DFM) |
| Unit-cost model at 10 / 100 / 1000 units with NRE, tooling, assembly and test time | E2 | This is volume costing. The funded build is qty 1–10. | Shrink to a qty-1 and qty-10 cost model | 0.3 |
| Price breaks at 1/10/100/1000; BOM costed at 1/10/100 | E0 | Same reason as above | Cost at qty 1 and 10 only | 0.1 |
| RF certification consequence of module vs chip | B1, B2 | Enterprise concern. The student uses a pre-certified module anyway. | One sentence | 0.15 |
| IP rating requirements | D4 | Certification. Sweat ingress alone covers the real need. | Replace with one paragraph on sweat and gaps | 0.1 |
| ADRs "so a decision survives the team"; 3 formal ADRs | A2 | Team process for a solo student | One or two short decision notes (choice · options · why) | 0.25 |
| Sequence diagrams | C1 | Third notation. Flowcharts and state diagrams already cover the deliverables. | Cut, or give one example with no deliverable | 0.25 |
| Assembly files (assembler BOM CSV, CPL, assembly drawing, "rotation errors = #1 assembly failure") | E1 | The reference is hand-soldered and needs no assembly service. | Shrink to one paragraph: "needed only if you order assembly" | 0.2 |
| Offline buffering and flush, HTTP vs MQTT re-comparison, captive-portal provisioning | C5b | Part 1 covers MQTT/HTTP. The reference uses WiFi once at boot and then turns it off. | Keep reconnect and NVS. Shrink the rest to pointers. | 0.4 |
| Hierarchical sheets, library management | B4 | A one-page carrier board doesn't need them | One line each | 0.1 |
| LTspice as the "rigorous" option | §7, B3 | Falstad is enough at this level | Mention in one line | 0.05 |
| **Total** | | | | **≈ 1.9** |

Author rule for every row above: each niche topic keeps a short mention (a sentence or two) so the student knows it exists. It is not cut to zero.

## 3. Contradictions

| Topic | CURRICULUM.md says | REFERENCE-PRODUCT.md / PROGRESS.md says |
|---|---|---|
| Real invoice | "students get the real schematic, the real board file, the real fabrication package and the real invoice" (intro) | "PCB fabrication cost: placeholder — order placed with JLCPCB, invoice not yet available" (§3) |
| Real order in E2 | "Compare against the reference watch's **real order**: what was quoted, what it actually cost … how long it actually took" (E2) | "Quantity, options, quoted vs actual lead time, total cost, customs and GST: **PLACEHOLDER**" (§6) |
| Build status | "fabricated by JLCPCB … and enclosed in an Onshape model" (intro) | "sent to JLCPCB for fabrication; not yet delivered/assembled"; enclosure "almost complete" (§1, §7) |
| What dominates the power budget | "see which state actually dominates" (B1). Earlier text said "the optical sensor's LEDs" (see the FACT:VERIFY in B1). | "under this profile **sleep current dominates** the budget" (§4) |
| Current budget states | "a worked current budget across boot, idle, measuring and sleep" (B1) | Modelled states are screen-on/WiFi, HR measurement, WiFi burst, optimised idle. "No current measurements were ever taken." (§4) |
| Deep sleep's place | "deep sleep and battery duty-cycling" is extension reading only (C7) | Sleep current decides runtime, so "the choice of sleep mode matters more than screen or sensor use" (§4). This is core content, not an extension. |
| IMU v2 (**resolved 2026-09-29**, sentence removed) | "its IMU is obsolete, so a v2 will change the driver" (C0) | "**esp_watch keeps the MPU-6050.** The ICM-42670-P is mentioned only as … alternate" (§8) |
| MAX30102 footprint source | "drawn from scratch against a mechanical drawing" (B5) | "Derived from a calibrated photo … generated by `make_max30102_footprint.py`" (§5) |
| Other footprints | "the other two were downloaded" (B5) | The XIAO footprint was downloaded. The module headers are "KiCad standard library" (§5). No other peripheral footprints exist. |
| Board outline | "board outline imported from CAD" (B5) | Not stated. The outline is 38 × 38 mm, and the enclosure is not finished (§5, §7). |
| OLED stack | "the OLED sits on standoffs above the IMU" (D2) | "hold the MPU-6050 and OLED modules on standoffs". It does not say the OLED is above the IMU (§5). |
| Slide switch / interrupts | "the power path runs through a slide switch" (B0) | The public README omits SW3, the battery divider and both interrupts. FACT:VERIFY pending (§4). |
| CAD tool | "Fusion 360 or Onshape" (D1); "Accounts on … Onshape (or Autodesk Education for Fusion 360)" (§0) | "The course teaches Fusion 360" (CURRICULUM intro; REF §1, §7) |
| Section D hours | "Section D — Mechanical / 3D Design (~8 hrs)" (heading) | Effort table and unit rows sum to **9.0** (same file) |
| Unit length | "keep every unit under 90 minutes" (§8) | B1, B2, D1 and F are 2.0 h, and C5 was 2.5 h before the split (tables) |
| Assessment size | "6 MCQs … 2 artifact-diff … self-check rubric of 10 binary items" (§9 pattern) | "Five MCQs, a short activity set and about 8 self-check items are enough" (PROGRESS, author feedback) |
| Reading length | "Reading (~4,500 words)" for a 1.5 h unit (§9) | "the readings are for students to learn from, not a showcase" (PROGRESS). Word targets are now removed altogether (author, 2026-09-29). |

## 4. Build-prompt causes

Source: `old_prompt.md` unless marked. "v2" = what `COURSE-BUILD-PROMPT-v2.md` records as already changed.

| Rule that pushes length | Where in old prompt | v2 status | Replacement rule |
|---|---|---|---|
| "Target words: 2,500–3,500 for a 1-hour unit, 4,000–5,500 … 5,500–7,000 for a 2-hour unit. **The Applied IoT readings are long and dense; match that.**" | Run 1 | Still a band, now called a ceiling | **Remove word targets.** "Write what the student needs to understand this unit's row and produce its deliverable. Stop there." Drop the Target words column from PROGRESS, and the Target / vs-target columns from lint. Keep only the 50,000-char file cap (platform limit). |
| "Word count is within the target band for the unit's hours" | Quality bar | Kept as a ceiling | Delete. Use the check "would the student notice if this paragraph were gone?" |
| "Every section of the template is present and **substantial**. No stubs." | Quality bar | Replaced | Required sections: outcomes, content, one worked example, activity = deliverable, self-check, MCQs. All others are optional. (Author: drop.) |
| "Match its voice, structure and **density**"; "Follow the Applied IoT readings closely. That structure is proven and the client likes it." | Input files; template | "voice, not length" | "Match Part 1's voice only. Don't copy its structure or length." |
| "What Part 1 Already Covered … **This section is not optional**" | Template | 1–2 sentences, or omit | Omit unless the unit truly builds on a named Part 1 module. Then one sentence. |
| Labels box ("Teaching model / Example values / Assumption") in every unit | Template | A0 only | A0 only (as v2) |
| Opening bridge of "2 to 4 paragraphs" | Template | ≤ 2 short paragraphs | ≤ 2 short paragraphs (as v2) |
| "Use two to four Parts for a unit of 1.5 hours or more" | Template | Not changed | Use Part headings only when the unit has distinct stages. Never as a minimum. |
| Activities that "build in difficulty: recognise → reproduce → modify → diagnose → design" (5 steps) | Template | Not changed | One activity that produces the deliverable. Add a second only if the deliverable has a separate hard step. |
| Self-check "Eight to twelve binary items" | Template | Not changed (PROGRESS says ~8) | **Required in every unit** (author). About 8 binary items, each checkable against the student's own file. |
| "Five to eight MCQs"; answer "on why C is right and why each of A, B and D is wrong"; "MCQ answers explain why each wrong option is wrong" | Template; quality bar | ≤ 60 words; wrong options explained only if not obvious | **Required in every unit** (author). 5 MCQs; answers ≤ 60 words (as v2). |
| "At least two Try-it boxes", each with Predict / Do / Explain + Extra challenge | Quality bar; Try-it format | 1–2, never duplicating an activity | 0–2. Drop the "Extra challenge" line. A Try-it is never a copy of the end activity. |
| "What You Can Now Do": "Three to five bullets … then a short paragraph naming the mental model … then what the next unit picks up" | Template | One short paragraph | One or two sentences on what comes next. No recap of outcomes. |
| "Build intuition before formalism. Analogy or situation first"; "Say when an analogy breaks" | Voice | One analogy only, no closing moral | Use an analogy only when the idea is hard. At most one per idea. Skip the "where it breaks" note unless the break would mislead. |
| "Rhetorical questions … or deliberately left open as 'Think about it'"; "Anticipate the misconception" | Voice | Not changed | Name a misconception only if students really hold it. No rhetorical questions as section openers. |
| "Explanatory prose, not bullet soup. Reasoning goes in paragraphs." | Voice | Not changed | Use a table wherever it replaces three or more parallel sentences. Keep prose for reasoning. |
| "Worked examples show every step, with a check at the end" | Voice | Not changed | Show every step that is new. Collapse steps the student already knows from earlier units. |
| "Cross-reference with relative links" | Content constraints | PROGRESS: link only where it adds something | Link another unit only when the student must go there. No running cross-references. |
| "Note on numbers" footer and a References section in every unit | Template | Not changed | Put the numbers note in A0 only. Include References only if the unit cites something. |
| Reference product = "AirGradient ONE / Open Air"; REFPRODUCT example about a "3.3 V LDO … 400 mW" | Config; content constraints | Config fixed to esp_watch | Also replace the LDO example with an esp_watch one. It isn't true of this product. |
| "Build it up in successive appends rather than one enormous write" | Run 2 step 3 | Not changed | Harmless for truncation, but add: "Before marking DRAFTED, reread and cut anything the student would not miss." |
| Run 1: report "anything … under-budgeted" | Run 1 | Not changed | Ask for "anything over-scoped or beyond the requirements" too |
| CURRICULUM gives the same reference story to many units (I²C / green MAX: B0, B1, B3, C2, C6; IMU obsolescence: B2, C0, E0) | CURRICULUM rows; REF §9 "Needed by" | Rule added: "one owner, others one-line pointer" | Also name the owning unit per story in CURRICULUM, so the writer and reviewer can check it |

## 5. Proposed revised hours table

| Section | Current hrs | Proposed hrs | Why |
|---|---|---|---|
| A — System Architecture | 3.5 | 3.0 | A1 1.5 → 1.0 (the brief says "one pass each, no deep dives"). A2 ADRs become short decision notes. |
| B — Hardware & Electronics | 9.5 | 9.0 | B2 2.0 → 1.5: certification is cut. B1 keeps 2.0 (power budget and pin map are core). |
| C — Firmware | 11.0 | 10.0 | C1 1.5 → 1.0 (no sequence diagrams). C5b 1.5 → 1.0 (Part 1 already covers MQTT; the reference uses WiFi once). Move deep sleep from C7 into C4. |
| D — Mechanical / 3D | 9.0 (heading says ~8) | 9.0 | D3 stays at 1.5 h. Injection moulding shrinks to a mention, and the time goes to prototype DFM (inserts, screws, magnets, snap fits, tolerances). Fix the heading to ~9. |
| E — Sourcing & Handoff | 3.0 | 2.5 | E2 1.0 → 0.5: there is no real order to compare against yet, and costing is at qty 1/10 only. |
| F — Capstone | 2.0 | 2.0 | Unchanged |
| **Total** | **38.0** | **35.5** | Hours are study time (reading + activity). They no longer set a word count. |
