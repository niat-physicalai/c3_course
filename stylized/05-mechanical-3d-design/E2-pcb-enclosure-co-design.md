<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">E2 — PCB and Enclosure Co-Design</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting the Real Board Inside the Real Case, and Checking Nothing Collides</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 5 — Mechanical and 3D Design <strong>Time:</strong> ~1.5 hours · <strong>You will produce:</strong> a CAD assembly with the real board model inside the enclosure, and a clean interference check</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Two Correct Designs That Do Not Fit Together</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">By now you have a board that passes DRC and an enclosure that updates when its parameters change. Each is correct on its own. Put them together for the first time and problems appear that neither could show alone: a connector sits 1 mm lower than the case opening; a mounting hole lands on a rib; the tallest module pushes into the lid; the antenna cable has nowhere to go.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">To find these problems, put the real board model inside the real case model and check. Some fixes belong on the board, so this unit also covers sending changes back to KiCad. As in E0, everything here uses Fusion's Design workspace and its Solid tools.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Make sure</strong> every part on the board has a 3D model, and <strong>find</strong> one, or make a stand-in, when it does not.</li><li style="margin:6px 0;">​<strong>Insert</strong> the board STEP from C3 into your E0 case, and <strong>fix</strong> it in place.</li><li style="margin:6px 0;">​<strong>Design</strong> mounting bosses and connector openings from the board's real geometry.</li><li style="margin:6px 0;">​<strong>Measure</strong> the component stack in CAD and <strong>decide</strong> whether it meets your thickness requirement.</li><li style="margin:6px 0;">​<strong>Run</strong> an interference check and a section analysis, <strong>resolve</strong> what they find, and <strong>send</strong> board changes back to KiCad.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Before You Start</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">You need</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">From</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your board exported as STEP, with every part's 3D model attached</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">C3 Step 13</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your parametric two-part case (base and lid)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">E0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The thickness requirement and openings list</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 and your C0 concept</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">esp\_watch's board STEP, to follow along</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<a href="https://github.com/niat-physicalai/esp_watch/blob/main/pcb/esp_Watch/esp_Watch.step">pcb/esp\_Watch/esp\_Watch.step</a></td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — From KiCad to Fusion</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Trap: Parts With No 3D Model</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The board STEP you exported in C3 contains only the components whose footprints have a <strong>3D model</strong> attached (C2 Step 8). A part with no model exports as nothing: just its pads on a flat board. The CAD model looks tidy, the interference check passes, and the real module, sitting on its header, crashes into the lid.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">So before importing, open KiCad's 3D viewer (<strong>View → 3D Viewer</strong>) and check that every part is there. For each one that is missing, find a model in this order:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Good for</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">KiCad's own library</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Standard parts: headers, sockets, buttons, passives. Library footprints usually have one attached already.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The manufacturer's or seller's product page</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Branded parts and modules, such as Würth switches or Seeed boards</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A model-sharing site, such as GrabCAD</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Common hobby modules, uploaded by other users. Check the size against your part before trusting it.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A box you model yourself in Fusion</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Anything with no model. Measure the outline and height, extrude a box, export it as STEP, and attach it to the footprint.</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A box is a stand-in, like the mock sensors in the firmware module: it has the size that matters for this check and nothing else. A beautiful model is not required.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Some parts are not on the board at all: the battery, a strap, a cable. They will not be in the board STEP, so model them as boxes directly in your Fusion case.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's repository has STEP models for every part on its board: the XIAO, the MAX30102, MPU-6050 and OLED modules, the female header and the Würth slide switch, in pcb/esp\_Watch/3d models/; the push buttons use KiCad's library model. Its exported esp\_Watch.step therefore shows the full stack. The battery is not on the board and has no model, so it is a box: <strong>30 × 12 × 4 mm</strong>, standing on end in the slot behind the OLED's header.</div>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_side.png" alt="esp_watch board, KiCad 3D render from the side: the module stack that the enclosure must fit around" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch board, KiCad 3D render from the side: the module stack that the enclosure must fit around</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 1: Insert the Board Into the Case</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Upload the STEP.</strong> Open the <strong>Data Panel</strong> (the grid icon at the top left), go to your product's project, click <strong>Upload</strong>, and choose the board's .step file. Fusion converts it into a design [2].</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Insert it.</strong> With your E0 case open, right-click the uploaded board in the Data Panel and choose <strong>Insert into Current Design</strong>. It arrives as its own <strong>component</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Position it.</strong> Use <strong>Modify → Move/Copy (M)</strong> to drop the board into the base, centred on the origin, resting at the height its standoffs or bosses will give it.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Fix it.</strong> Right-click the board component in the browser and choose <strong>Ground</strong>. A grounded component cannot be moved by accident. You place case features around it; you never edit it.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Name it</strong> with its revision, for example pcb\_v1. When C3 changes the board, you insert pcb\_v2 beside it and see what moves.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — Designing Around the Board</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 2: Mounting Bosses From the Real Holes</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>boss</strong> is a raised post in the case that the board sits on or screws to. A <strong>standoff</strong> is a separate spacer between two boards or between a board and a module. Place them from the board's actual mounting holes, not from a guess.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Create Sketch</strong> on the inside face of the base's floor.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Create → Project / Include → Project (P)</strong>, and click the edge of each mounting hole on the board. Fusion copies their circles into your sketch, linked to the board.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Draw a circle around each projected hole for the boss's outside, dimensioned with a parameter such as boss\_d.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Extrude (E)</strong> the ring up to the underside of the board, with <strong>Operation: Join</strong> onto the base body.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Because the circles are projected, the bosses follow the board if the holes move in the next revision. E3 sizes the boss and the screw hole for printing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch has <strong>four mounting holes</strong>: two at the top corners and two in the middle. They hold the MPU-6050 and OLED modules on standoffs; the OLED also sits on a female header, which raises it above the MPU-6050 with a 4–5 mm air gap. Take the hole positions by projecting them from the board model, not by measuring a render.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 3: Openings for Connectors and Controls</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every part the user touches or plugs into needs an opening, sized from the part and positioned from the board model. Sketch each one on the case wall or lid, <strong>project</strong> the part's outline from the board as a guide, and cut it with <strong>Extrude → Cut</strong>, with only the right body ticked under <strong>Objects To Cut</strong> (E0 Step 9).</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Opening</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Size it from</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Check</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">USB-C port</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The plug's overmould, not the socket, because the cable must fit</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The plug fully seats with the case in place</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Button caps or plungers</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The button's actuator, plus clearance for movement</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The button can travel fully without binding</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Slide switch</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The slider's full travel</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Both end positions are reachable</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Display window</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The display's active area, not the whole module</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No border visible, no pixels hidden</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's openings: the XIAO's <strong>USB-C port on the left side</strong> of the case, and four in the lid for the <strong>display window, two buttons and the slide switch</strong>.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Sizing the USB-C Opening</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: Find the socket's position</strong> in the imported board: its centre height above the case floor and its position along the wall. Use <strong>Inspect → Measure (I)</strong> on the board model.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: Size the opening for the plug</strong>, not the socket. <strong>Example values:</strong> a USB-C cable's plug overmould about 12 × 6.5 mm, with 0.5 mm clearance each side.</div>

```text
Opening width  = 12.0 + 2 × 0.5 = 13.0 mm
Opening height =  6.5 + 2 × 0.5 =  7.5 mm
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 3: Check the wall.</strong> The plug must reach the socket through the wall. If the wall is 1.5 mm thick and the socket's face sits 0.5 mm inside the board edge, which itself sits 0.5 mm (the clearance) inside the wall, the plug must travel 2.5 mm before it meets the socket face.</div>

```text
Wall thickness                  1.5 mm
Board-to-wall clearance         0.5 mm
Socket face set back from edge  0.5 mm   (example value; measure yours)
─────────────────────────────────────
Distance plug travels in        2.5 mm
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> An opening sized for the overmould lets the overmould enter the wall, so the plug seats. If the opening is smaller, the overmould stops at the outside of the wall. The metal shell must then cross these 2.5 mm and still go fully into the socket, which many cables cannot. Fixes: enlarge the opening, thin the wall locally, or move the socket closer to the board edge in C3.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Clearance to Tall Parts, and Keep-Outs</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Leave a gap between every part and the case, as you did with the clearance parameter in E0. The gap matters most above the tallest part and beside anything that moves, bends or gets warm.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Also mark areas the case must stay clear of:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>The antenna.</strong> No case features, screws or metal close to it, and a path along the inside of the case for its cable.</li><li style="margin:6px 0;">​<strong>The battery.</strong> A bay that holds it without pressing on it (E4 covers this).</li><li style="margin:6px 0;">​<strong>Cables</strong>, such as a display's flexible ribbon, which need room to bend gently.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's external antenna is to be routed along the inside of the case, away from the battery, which stands on end behind the OLED's header. In CAD, sketch the intended antenna path as a line along the inner wall and keep features off it.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 3 — Measuring the Stack</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Number That Sets the Thickness</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On a module-based board, the tallest stack of parts decides the product's thickness.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On esp\_watch, the OLED sits on a female header above the MPU-6050, with a 4–5 mm air gap between them. The recorded height is <strong>14.044 mm</strong>, measured from the board to the top of the OLED. The board itself and the MAX30102 module on the underside add to that, so the case must hold more than 14.044 mm. In C0, the thickness budget added walls and clearance and reached about 18 mm, against an example requirement of 16 mm.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Measure, Then Decide</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: Measure in CAD.</strong> With the board inserted, use <strong>Measure</strong> from the underside of the lowest part to the top of the highest part. Compare it with the number you used in C0 and E0's stack\_h. If they differ, update stack\_h in <strong>Change Parameters</strong>, and the case follows.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: Find what sets it.</strong> Section the assembly through the tallest point (Step 4). Identify each layer in the stack and its height. <strong>Example breakdown</strong> for a stacked module design:</div>

```text
Display module thickness           ~ 3 mm
Header gap above the IMU           ~ 5 mm
IMU module on its header           ~ 4 mm
Board thickness                    ~ 1.6 mm
Parts below the board              ~ rest
```

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>These layer heights are illustrative, to show how a stack is broken down. Measure yours in CAD.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Decide.</strong> For each layer, ask whether it could be smaller: a lower header, a shorter standoff, a module moved from above another to beside it, as in C0's concept B.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The decision is either "accept the thickness and update the requirement in writing" or "change the board". Either is fine. Leaving the two out of step is not.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 4 — Checking and Closing the Loop</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 4: Interference Check and Section Analysis</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two tools in the <strong>Inspect</strong> panel answer the question "does it fit?":</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Inspect → Interference</strong> [2] compares what you select and reports every place where two solids overlap. Select the board component, the battery box, base and lid, and click <strong>Compute</strong>. Each overlap is listed and shown in red.</li><li style="margin:6px 0;">​<strong>Inspect → Section Analysis</strong> cuts the model along a plane so you can see inside it: gaps, wall thickness, how parts stack. Pick a plane, drag the arrow to move the cut, and measure across it.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A clean interference check means <strong>no overlaps</strong> between the board, every part on it, and the case. But "no overlap" is not "enough clearance". Section through the tallest part and the connectors, and measure the gaps. A 0.05 mm gap passes the interference check and will fail in a real print.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 5: Send Changes Back to the Board</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Some fixes belong on the board: moving a connector closer to the edge, shifting a mounting hole off a rib, changing the outline to fit a rounded case. Make those changes in KiCad, not by forcing the case to fit a board that is wrong.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">For the <strong>board outline</strong>, the case is often the better place to design it, because the outline must match the inside of the case. Sketch it in Fusion, right-click the sketch in the browser and choose <strong>Save As DXF</strong>. In KiCad's PCB Editor, use <strong>File → Import → Graphics</strong> to place the DXF on the <strong>Edge.Cuts</strong> layer [1]. Then re-export the board as STEP, insert it as the next revision, and repeat the checks.</div>

```text
Fusion: board outline sketch ──(DXF)──► KiCad: Edge.Cuts
                                           │
          KiCad: layout, DRC               │
                                           ▼
Fusion: interference check ◄──(STEP)── KiCad: export board with 3D models
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Expect to run this loop several times. Commit the board and the case to your design pack's repository together each time, so a case version always has the board version it was checked against (<a href="../01-system-architecture/REF-version-control.md">Version Control</a>, Step 3).</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Tool Reference</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Tool</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Key</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Use it to</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Upload</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Data Panel</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bring the board STEP into your Fusion project</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Insert into Current Design</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Data Panel, right-click</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Place the board in the case design as a component</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move/Copy</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modify</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">M</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Position the board</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Ground</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Browser, right-click a component</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fix the board in place</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Project</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sketch: Create → Project / Include</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">P</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Copy board geometry, such as hole circles, into a sketch</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Interference</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Inspect</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Find solids that overlap</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Section Analysis</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Inspect</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cut the view open to see and measure gaps</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Measure</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Inspect</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Measure heights and gaps</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Save As DXF</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Browser, right-click a sketch</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Send an outline to KiCad</td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Give every part a 3D model.</strong> Check your board in KiCad's 3D viewer. For each part without a model, find one or make a box of its measured outline and height, and attach it. Model off-board parts, such as the battery, as boxes in Fusion.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Insert and ground.</strong> Insert your board STEP into your E0 case, position it, ground it and name it with its revision.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Build the mounting and openings</strong> from the board's real geometry: bosses from projected hole centres, and every opening sized from the part. Check that the charging plug seats, as in the USB-C worked example.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Measure the stack.</strong> Update stack\_h to the measured value, and write your thickness decision.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Check.</strong> Run the interference check to zero overlaps, then section through the tallest part and every connector, and record the gaps.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> the Fusion assembly with the real board inside (.f3d export), a screenshot of a clean interference check, and your section measurements and thickness decision, saved in your design pack as E2-fit/.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your assembly and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every component on the board appears in the CAD model, with at least a box of the right size. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Off-board parts, such as the battery, are modelled as boxes. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. The board is a separate, named, grounded component. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Mounting bosses are built from projected hole positions. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every connector and control has an opening sized from the part. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The charging plug's travel through the wall has been checked. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. stack\_h equals the height measured in CAD. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The interference check reports zero overlaps. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. Section measurements show at least your chosen clearance above the tallest part. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">10. Any board change is recorded as a change to make in KiCad, not only in the case. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> An interference check between a board and its case reports no overlaps, but the real board will not fit. What is the most likely cause?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The interference check is broken.</li><li style="margin:6px 0;">B. The case is too big.</li><li style="margin:6px 0;">C. One or more footprints have no 3D model, so a tall module was missing from the exported STEP.</li><li style="margin:6px 0;">D. The board is too thin.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Parts without 3D models export as nothing, so the check cannot see them. <strong>A</strong> blames the tool for data it was never given. <strong>B</strong> would not stop a board fitting. <strong>D</strong> is not the usual cause.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> Why build mounting bosses from projected hole circles rather than typed coordinates?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Projected geometry follows the board, so if the holes move in a board revision, the bosses move with them.</li><li style="margin:6px 0;">B. It is faster to draw.</li><li style="margin:6px 0;">C. Fusion cannot use typed coordinates.</li><li style="margin:6px 0;">D. It makes the bosses stronger.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> It links the case to the board's real geometry. <strong>B</strong> may or may not be true, and is not the point. <strong>C</strong> is false. <strong>D</strong> is unrelated.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A USB-C opening is sized exactly to the socket on the board. What is likely to go wrong?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing.</li><li style="margin:6px 0;">B. The socket will fall out.</li><li style="margin:6px 0;">C. The board will overheat.</li><li style="margin:6px 0;">D. The cable's plug overmould is larger than the socket, so the plug cannot enter the opening far enough to seat.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> The plug is what passes through the wall, so the opening must fit the plug. <strong>A</strong> ignores the plug. <strong>B</strong> and <strong>C</strong> have no connection to the opening size.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> The interference check is clean, but a section shows 0.05 mm between the display and the lid. What should you do?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing; no overlap means it fits.</li><li style="margin:6px 0;">B. Increase the gap to your chosen clearance, because a 3D-printed part will not hold 0.05 mm, and the display could be pressed or the lid may not close.</li><li style="margin:6px 0;">C. Remove the lid.</li><li style="margin:6px 0;">D. Make the display thinner.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> "No overlap" and "enough clearance" are different tests; printing tolerances need a real gap (E3). <strong>A</strong> confuses the two. <strong>C</strong> and <strong>D</strong> are not sensible fixes.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A connector needs to be 1 mm closer to the board edge for the plug to seat. Where should the change be made?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. In the CAD case, by carving the wall away.</li><li style="margin:6px 0;">B. In the slicer.</li><li style="margin:6px 0;">C. In KiCad, by moving the connector footprint, then re-exporting the STEP and re-checking.</li><li style="margin:6px 0;">D. Nowhere; users can push harder.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> The root cause is the connector's position on the board, so fix it there and re-check. <strong>A</strong> can be a valid local fix if the wall allows it, but it weakens the wall and hides the real cause. <strong>B</strong> cannot change geometry. <strong>D</strong> is not engineering.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6.</strong> Your board STEP looks complete, but the case still needs to hold a 30 × 12 × 4 mm battery. Why is the battery not in the STEP, and what do you do?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. KiCad left it out by mistake; re-export.</li><li style="margin:6px 0;">B. It is not a part on the board, so it has no footprint; model it as a box in Fusion and include it in the checks.</li><li style="margin:6px 0;">C. Batteries never need clearance.</li><li style="margin:6px 0;">D. Add a battery footprint to the board just to get the model.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The STEP holds only what has a footprint on the board. Off-board parts are modelled in the case design. <strong>A</strong> is not a fault. <strong>C</strong> is false: E4 needs a bay that does not press on the cell. <strong>D</strong> adds a fake part to the board and its BOM.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="E3-design-for-manufacturing.md">E3 — Design for Manufacturing</a> you will make sure the case you have designed can actually be 3D printed, and see what would change if it were moulded instead.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. KiCad. PCB Editor documentation, version 10.0 (importing graphics onto board layers; board outline on Edge.Cuts; 3D models in footprint properties). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Autodesk. Fusion Help (Data Panel upload, Insert into Current Design, Interference, Section Analysis). https://help.autodesk.com/view/fusion360/ENU/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
