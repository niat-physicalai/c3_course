# Crux — module 01: System Architecture

## A0 — Product Specification
- "Long battery life" and "small" are wishes; a spec gives each a number, a condition and a check. (A0#wishes-are-not-requirements)
- A spec says what the product must do and how well, not how; built in order problem → user → environment → requirements → checks → not-in-v1. (A0#what-a-specification-is)
- Functional = what it does; non-functional = how well / limits; cover all seven NFR categories, with conditions like "wearer sitting still". (A0#two-kinds-of-requirement)
- Every requirement: ID, "shall" statement, number + unit + condition, check method; checks without building = inspection, analysis, simulation, review. (A0#making-a-requirement-checkable, A0#checking-without-building)
- Write a use scenario → usage pattern UP-1; list the operating environment (skin, sweat, knocks, heat; IP code target). (A0#the-user-their-day-and-their-environment)
- esp_watch battery: 40.3–87.4 mAh/day vs 240 mAh usable → 2.7–6.0 days (2.2 at 4 mA); sleep current decides battery life. (A0#worked-example-can-espwatch-last-two-days)
- Out-of-scope list: feature, why, where it goes; "we ran out of time" is not a reason. (A0#deciding-what-version-1-will-not-do)
- Carry forward: a requirement is only real if someone else can check it. (A0#what-comes-next)
- Images: none local in the unit → Claude-made diagrams/chart.

## A1 — Overall System Architecture
- System boundary: inside = you can change it by editing design files; outside = external actors exchanging information, energy or contact. (A1#inside-and-outside)
- Context diagram: one box, every actor, arrows labelled with what flows, direction meaningful. (A1#the-context-diagram)
- Seven standard subsystems; enclosure and backend are the ones regularly forgotten. (A1#seven-standard-subsystems)
- esp_watch broken down; the PCB render shows sensing, processing, local UI, power — a photo cannot replace the diagram. (A1#the-reference-watch-broken-down)
- Allocation: one owner per requirement, others support; budget requirements, orphans, unused subsystems. FR-04 (semester trend) is an orphan in esp_watch; three ways out. (A1#allocating-every-requirement, A1#worked-example-holding-espwatch-against-a-problem-statement)
- Anything the wearer needs at the moment belongs on the device; only work that can wait depends on a link. (A1#where-does-the-work-happen)
- Raw signal 7.2 MB vs results 20 kB per semester (≈355×); on-watch storage becomes realistic. (A1#how-much-data)
- Choose no connection / BLE to phone / WiFi direct with a one-line reason; esp_watch: WiFi once at first boot. (A1#which-connection)
- Images: pcb_top.png (A1#the-reference-watch-broken-down) → assets/slides/01/esp_watch-pcb_top.png.

## A2 — Operating Modes, Failure Behaviour and Decisions
- State = mode until an event; transition = move caused by an event; charging is an overlay, not a box. (A2#states-what-mode-is-the-system-in)
- esp_watch: BOOT → AWAKE ⇄ MEASURING, always on; gaps: WiFi failing at boot, abort detection, no sleep, no battery-measurement pin. (A2#worked-example-the-reference-watchs-states)
- Graceful degradation by default; hard stop when continuing could damage something or show a number the wearer might trust. (A2#failure-behaviour)
- Judge I²C bus health by a device you read from; a failure you cannot detect is a failure you cannot handle. (A2#failure-behaviour)
- Health data: where it lives, who can read it, does it leave the device; safest data never leaves. (A2#where-health-data-lives)
- Decision note = decision, options considered, why, what it costs; "what it costs" turns into follow-on work. (A2#writing-down-your-decisions, A2#worked-example-a-reconstructed-decision-note-for-the-reference-watch)
- Images: photo_9.jpeg (A2#failure-behaviour) → assets/slides/01/esp_watch-breadboard-photo_9.jpeg. i2c-debug-output.png is MISSING.

## REF — The Verification Stack
- For each stage a named check with a clear pass/fail (spec, allocation table, Wokwi, ERC, DRC, firmware vs state diagram…). (REF-verification-stack#the-full-table)
- A clean DRC means "can be made", not "will work"; Wokwi has no MAX30102 → mock sensor; simulator pass = "my logic is right". (REF-verification-stack#what-a-pass-does-not-tell-you)
- Record check, date, verdict in the design pack. (REF-verification-stack#how-to-use-this-page)

## REF — Version Control for a Hardware Project
- One repo for the whole design pack; commit small, commit often, with messages that say what changed. (REF-version-control#step-1-one-repository-for-the-whole-design-pack, REF-version-control#step-3-commit-small-commit-often)
- Commit what you made; ignore what tools make for themselves. (REF-version-control#step-4-decide-what-git-ignores)
- Tag the commit sent to the fab; same revision in tag, title block and silkscreen; never move or reuse a tag. (REF-version-control#step-5-tag-the-version-you-send-to-the-fab)
