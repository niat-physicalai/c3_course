<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">E4 — Functional Mechanical Design for a Wearable</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Features That Make a Case Work on a Body</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 5 — Mechanical and 3D Design <strong>Time:</strong> ~1.5 hours · <strong>You will produce:</strong> a revised enclosure, with the sensor-window and battery-retention reasoning written down</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Box That Fits Is Not Yet a Watch</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">After E2 and E3 your case fits the board and can be printed. Put it on a wrist and new questions appear. Does the heart-rate sensor actually touch the skin, or is there a millimetre of plastic and air between them? What holds the strap on when the wearer catches it on a door handle? What stops the battery from being squashed by the lid, or rubbed by a screw head? Can the button be pressed through the wall without pushing the whole watch into the wrist? Where does sweat go?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">None of these is about fitting parts in a box. They are about the product doing its job on a moving, sweating human body. This unit takes each one in turn and traces it back to a requirement from A0, so every feature has a reason you can write down.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Design</strong> a skin-contact window that presents an optical sensor to the skin and blocks outside light.</li><li style="margin:6px 0;">​<strong>Size</strong> strap lugs for the loads a strap puts on the case.</li><li style="margin:6px 0;">​<strong>Design</strong> a battery bay that retains the cell without pressing on or puncturing it.</li><li style="margin:6px 0;">​<strong>Design</strong> buttons and openings that work through a wall, and plan for sweat.</li><li style="margin:6px 0;">​<strong>Trace</strong> every wearable feature back to a requirement, and record the reasoning.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">1. The Skin-Contact Window</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Why It Matters Most</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">An optical heart-rate sensor shines light into the skin and measures the small part that comes back (B0). Any outside light that reaches the photodiode is noise, and the signal it is hiding in is small. The MAX30102 datasheet shows how well the sensor copes when it is used as intended: with a finger on the sensor, in direct sunlight, its ambient light rejection holds the error to about 2 counts [1]. The condition matters. The sensor rejects outside light well <strong>when it is pressed against skin</strong>. Leave a gap, and light leaks in from the sides.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">So the window has two jobs: <strong>press the sensor against the skin</strong>, and <strong>seal out light around it</strong>.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Three Ways to Build It</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Option</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How it works</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Strengths</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Weaknesses</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Open cut-out</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A hole in the base, the sensor's face sits flush with or slightly proud of the base</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Direct skin contact; simple to print</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The sensor's face is exposed to sweat; the edge of the hole must seal against skin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Clear insert</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A transparent window bonded into the base, the sensor behind it</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Protects the sensor; can be sealed</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Any gap between sensor and window, or a thick window, lets light bounce sideways; needs a clear part</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Raised boss</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The sensor sits in a small dome that pushes into the skin</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Good contact, even on a loose strap</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Can be uncomfortable; more complex to print</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Whichever you choose, apply three rules:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>The sensor must reach the skin</strong>, or the window's inner face, with no air gap. Set the sensor's height in CAD and check it in a section (E2).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Keep light out at the edges.</strong> An opaque rim around the sensor, pressed into the skin, blocks light from the side. Print the base in an opaque colour; thin light-coloured plastic can pass light.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Line the window up with the sensor, not the module.</strong> The module is much bigger than the sensor on it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's MAX30102 footprint outlines only the module body, <strong>20 × 15 mm</strong>, not the <strong>5.6 × 3.3 mm</strong> sensor package on it. So rule 3 takes one extra step: find the sensor's position on the module (from the calibrated photo in C2) and mark it before placing the window. The window goes over that rectangle, not the centre of the module. A board STEP export may not include drawing layers, so export the mark as a DXF or read its position from the board file.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: How Far Does the Sensor Sit From the Skin?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The sensor sits on the underside of the board. The case base sits below it. Will the sensor reach the skin?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Assumption:</strong> an open cut-out design. <strong>Example values</strong> for the heights, to show the method.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: Find the sensor face.</strong> In a section, measure how far the sensor face sits below the board: header, module PCB, then the 1.55 mm sensor package [1]. With <strong>example values</strong> (2.5 + 1.6 + 1.55 mm), that is 5.65 mm, and the sensor is the lowest part.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 2: Find the outside of the base.</strong> E0 put the base 0.5 mm clearance plus 1.5 mm thickness below the lowest part. So the outer surface is 2.0 mm below the sensor face.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Compare.</strong> With a cut-out, the sensor face sits 2.0 mm inside the base. Skin will not push 2 mm into a 5.6 × 3.3 mm hole.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 4: Fix it.</strong> Raise the sensor to the outer surface: reduce the clearance under the module, make the base thinner around the window (a local pocket), or add a raised rim so the skin is pressed towards the sensor. Aim for the sensor face to sit flush with, or up to about 0.5 mm proud of, the outer surface.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> A section through the sensor in CAD should show the sensor face at the outer surface of the base, with an opaque rim around it. If there is air between the sensor and where the skin will be, the requirement "heart rate within ±5 bpm, wearer sitting still" (A0) is already at risk, however good the firmware is.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/images/E4-01.svg" alt="Section through the base: a sensor set back in a cut-out, and the same sensor brought flush with an opaque rim" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Section through the base: a sensor set back in a cut-out, and the same sensor brought flush with an opaque rim</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">2. Strap Lugs</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Lugs</strong> are the features that hold the strap. A strap pulls on them every time the wearer moves, and hard when it snags on something. The lug is where a printed case is most likely to break, especially if the strap pulls across the printed layers.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Design rules for printed lugs:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Orient the print so the strap does not pull across the layers.</strong> Printed floor-down, the lugs lie along the layers, which is the strong direction. Printed on its side, the lugs stand upright and the strap pulls the layers apart. Check the orientation before slicing (E5). If the pull must cross the layers, make the lugs thicker.</li><li style="margin:6px 0;">​<strong>Use solid lugs.</strong> Set more perimeters or 100% infill in that region.</li><li style="margin:6px 0;">​<strong>Round the inside corners</strong> where the lug meets the case (E3), to spread the stress.</li><li style="margin:6px 0;">​<strong>Use standard hardware.</strong> Watch straps commonly use spring bars between the lugs, in standard widths. Choose the strap first, then design the lug gap and hole to its spring bar.</li></ul>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>The load on a lug depends on the strap, the wearer and the accident. For a design exercise, it is enough to ask: if the strap is pulled hard, which part breaks first, and is it a part that is cheap to replace? A strap that tears is better than a case that cracks.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's strap attachment is not recorded yet. With the USB-C opening on the left side, lugs at the 12 and 6 o'clock edges keep clear of it.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">3. The Battery Bay</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A lithium-polymer <strong>pouch cell</strong> has no rigid case. The Battery University reference on pouch cells makes three points directly relevant to the bay [2]: the cell needs support from its compartment, because it has no metal can; some swelling can occur, so the compartment must allow for expansion; and the compartment must protect the cell from mechanical stress and have no sharp edges. MIT's lithium battery safety guidance adds the plain rule: never puncture or crush a cell, and do not use one that has become puffy [3].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Turn those into design rules:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Rule</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Design feature</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hold the cell so it cannot move</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A pocket or ribs that locate it on all sides</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Do not press on it</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A small gap around it; nothing clamping its faces</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Leave room to swell</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Extra space on its thick faces</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No sharp edges or screw points near it</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Round the pocket edges; keep screws and inserts away</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Protect it from the board</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No pins, solder joints or component legs touching the pouch</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Keep the wires from being pinched</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A route for the leads to the board</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch stands its cell <strong>vertically in a slot behind the display's header</strong>, a face about 38 × 14 mm, to use height the electronics stack already claims (C0). The cell is 30 × 12 × 4 mm. The slot needs a gap on the cell's two large faces to allow for swelling, and nothing sharp on either side: the header pins of the display module are exactly the kind of feature that must not touch the pouch.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Sizing the Slot</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: Start from the cell.</strong> 30 mm long, 4 mm thick, 12 mm tall.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: Add clearance and swelling allowance.</strong> <strong>Example values:</strong> 0.3 mm fit clearance on every side (from your E3 clearance test), plus an extra 0.5 mm swelling allowance on each large face.</div>

```text
Slot length    = 30 + 2 × 0.3               = 30.6 mm
Slot thickness =  4 + 2 × 0.3 + 2 × 0.5     =  5.6 mm
Slot height    = 12 + 0.3 (top gap)         = 12.3 mm
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Check the space.</strong> A 5.6 mm-thick slot must fit between the display header and the case wall, and 12.3 mm must fit under the lid. Check both in an E2 section.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> If the slot does not fit, do not squeeze the swelling allowance to zero. Either choose a thinner cell, and recalculate battery life from B3, or rearrange. The allowance values above are illustrative; the principle, that a pouch cell needs room and must never be clamped, is not.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">4. Buttons Through a Wall</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A button on the board sits behind the case wall, so the wearer presses a <strong>plunger</strong> or a <strong>flexible tab</strong> in the case, which in turn presses the button. Three things decide whether it feels right:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Travel.</strong> The plunger must move far enough to press the switch fully, and no further. Leave the switch's own travel, plus a little, between the plunger and the switch.</li><li style="margin:6px 0;">​<strong>Retention.</strong> The plunger must not fall out of the case or into it. A small flange inside the wall stops it.</li><li style="margin:6px 0;">​<strong>Support behind the switch.</strong> Pressing a button pushes the board. On a wrist, it pushes the whole watch into the wearer. Support the board directly behind the button with a boss or rib, and put side buttons where the other hand can pinch the watch while pressing.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's two buttons and slide switch are on the top face, and the lid has an opening for each. A slide switch needs an opening as long as its full travel, plus room for a fingertip or fingernail, at both ends. The OLED's flexible ribbon (FPC) must be routed without strain: keep the lid and battery slot clear of it, and let it curve gently rather than crease.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">5. Charge Port and Sweat</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Charge-Port Access</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">E2 sized the opening for the plug. Here the question is where it is: on a side, away from the skin, where sweat does not run into it, and where the wearer can plug in without removing the strap.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's USB-C port faces the <strong>left side</strong> of the case. That keeps it off the skin, but it is also an open hole in the wall, and the easiest way in for sweat and dust.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Keeping Sweat Out</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Sweat is salty and conductive, and a wrist device sees it every day. Writing down a target for how much it must keep out shapes the design. (Commercial products state this as an <strong>IP rating</strong>, which must be earned by passing formal tests [4]; a student prototype does not claim one.)</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Target</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What the design would need</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Keep sweat off the electronics"</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Openings away from the skin; a lip or channel so sweat runs off rather than in; a coating on the board</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Survive splashes and rain"</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Seals on the lid joint, button membranes, a cover or seal over the USB-C port</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Survive immersion"</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Moulded case, gaskets, sealed buttons, a sealed or wireless charging port: beyond a printed version 1</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">FDM prints are not naturally watertight: water can creep between layers and through tiny gaps in the walls. That is a strong reason to set a modest target for version 1 and record the rest as version 2 work, exactly as A0's out-of-scope list suggested.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch has no sweat protection: it is not part of its design. Treat it as a version 2 item.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Tracing Every Feature to a Requirement</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For each wearable feature, write one line linking it to A0. The rows below are an illustration for a watch like esp\_watch. esp\_watch's own window, lug, button and sweat decisions are not recorded yet.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Feature</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Requirement it serves (A0)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Design decision</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Checked by</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensor window</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate accuracy, wearer still</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensor face flush with base; opaque rim; aligned to the sensor's own 5.6 × 3.3 mm rectangle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Section in CAD</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery slot</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Safety; battery life</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cell stood on end; gaps and swelling allowance; no sharp features nearby</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Section and proximity measurement</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lugs</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Survive knocks and snags</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Solid lugs, rounded roots, standard spring bars</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Print orientation review</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Buttons</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Buttons usable with one hand</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Plungers with set travel; board supported behind</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Section in CAD</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">USB-C opening</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charge from a phone charger</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Left side, away from skin, sized for the plug</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">E2 plug travel check</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sweat</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Water-resistance target</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Target set to "splash"; openings away from skin</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Written target and review</td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Design the sensor window.</strong> Choose cut-out, insert or boss, with a reason. Bring the sensor face flush or slightly proud, and add an opaque rim. Check in section.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Design the lugs</strong> for a strap you have chosen, oriented and reinforced for printing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Size the battery bay</strong> with clearance and swelling allowance. Hide everything except the cell and the parts within 2 mm of it. Measure the gap to each header pin, screw, insert and board edge.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Design the buttons</strong> with travel, retention and support behind the switch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Set a sweat target</strong> and design to it, recording what is left for version 2.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6. Write the traceability table</strong>, one row per feature.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> your revised enclosure, with the sensor-window and battery-bay reasoning and the traceability table saved in your design pack as E4-functional-design.md.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your revised enclosure and E4-functional-design.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. A section shows the sensor face flush with, or slightly proud of, the outer surface. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. The sensor window is aligned to the sensor itself, not the module. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. An opaque rim surrounds the sensor window. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. The battery bay has clearance on every side and a swelling allowance on its large faces. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. No sharp feature is within your chosen clearance of the battery. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Lugs are designed for a named strap and its spring bar. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Each button has set travel and support behind it. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. A written sweat target exists, with what is deferred to version 2. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. Every wearable feature traces to an A0 requirement in the table. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> An optical sensor sits 2 mm inside a cut-out in the case base. Readings are noisy outdoors and fine indoors. What is the most likely cause?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The firmware filter is too weak.</li><li style="margin:6px 0;">B. Outside light is leaking into the gap between the sensor and the skin; the sensor's light rejection works well only when it is pressed against skin.</li><li style="margin:6px 0;">C. The I²C bus is too slow.</li><li style="margin:6px 0;">D. The sensor is broken.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The datasheet's ambient light figure is measured with a finger on the sensor. A gap lets sunlight in from the sides, which is why it only fails outdoors. <strong>A</strong> treats a mechanical problem in software. <strong>C</strong> is unrelated. <strong>D</strong> is unlikely when it works indoors.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A 5 mm-thick pouch cell must fit between the display header pins and the case wall. With 0.3 mm clearance and 0.5 mm swelling allowance per face, the slot needs 6.6 mm, but only 5.8 mm is free. What should you do?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Make the slot 5.0 mm so the cell cannot rattle.</li><li style="margin:6px 0;">B. Cut the swelling allowance to 0.1 mm per face so it fits.</li><li style="margin:6px 0;">C. Keep the allowances, and choose a thinner cell or move the cell.</li><li style="margin:6px 0;">D. Let the cell rest against the header pins to gain space.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> A pouch cell needs room and must never be clamped, so change the space, not the allowance. <strong>A</strong> clamps a cell that may swell. <strong>B</strong> removes the swelling room. <strong>D</strong> puts sharp pins against the pouch, which risks puncture.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> Pressing a side button makes the whole watch dig into the wrist. What is the best fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Use a stronger spring in the button.</li><li style="margin:6px 0;">B. Support the board directly behind the switch, and place the button where the wearer can pinch the watch while pressing.</li><li style="margin:6px 0;">C. Remove the button.</li><li style="margin:6px 0;">D. Make the case heavier.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The force should go into the case and the wearer's opposing finger, not through the board into the wrist. <strong>A</strong> makes pressing harder. <strong>C</strong> drops a requirement. <strong>D</strong> does not stop the push.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> To save support material, a student plans to print the watch case on its side, so the lugs stand upright. What is the main risk?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The lugs will be too thin to print.</li><li style="margin:6px 0;">B. The strap will pull across the printed layers, so a lug may snap along a layer line.</li><li style="margin:6px 0;">C. The spring-bar holes will print oversized.</li><li style="margin:6px 0;">D. The walls will need more infill.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> FDM parts are weakest between layers. Standing the lugs upright puts the strap's pull straight across them. <strong>A</strong> is not true at watch sizes. <strong>C</strong> is a tolerance issue, not a strength one. <strong>D</strong>: thin walls are mostly perimeters, so infill barely matters there.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A printed watch has a tight lid, but the board corrodes after a week of daily wear. Where is sweat most likely getting in?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nowhere; corrosion comes from the battery.</li><li style="margin:6px 0;">B. Through the open USB-C port and between the printed layers, neither of which a tight lid seals.</li><li style="margin:6px 0;">C. Through the display glass.</li><li style="margin:6px 0;">D. Only through the strap.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> An open port and porous FDM walls are the obvious leak paths; a tight lid seals only the lid joint. <strong>A</strong> ignores the salty, conductive sweat. <strong>C</strong> faces away from the skin, so little sweat reaches it. <strong>D</strong> is outside the case.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="E5-slicing-and-printability.md">E5 — Slicing and Printability</a> you will prepare the enclosure for printing, read the slicer's preview for problems, and get a time and material estimate, without printing anything.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Analog Devices. MAX30102 datasheet (DC ambient light rejection of 2 counts with a finger on the sensor under direct sunlight, 100k lux; package 5.6 × 3.3 × 1.55 mm with integrated cover glass). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Battery University. Pouch Cell: Small but not Trouble Free (the cell needs support in its compartment; allow for some expansion; protect from mechanical stress; no sharp edges). https://www.batteryuniversity.com/article/pouch-cell-small-but-not-trouble-free/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. MIT Environment, Health and Safety Office. Lithium-Ion Battery Safety Guidance (never puncture or crush cells; do not use damaged or puffy batteries). https://ehs.mit.edu/wp-content/uploads/2019/09/Lithium\_Battery\_Safety\_Guidance.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. International Electrotechnical Commission. Ingress Protection (IP) ratings. https://www.iec.ch/ip-ratings</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
