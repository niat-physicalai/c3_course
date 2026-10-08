<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">C3 — KiCad Walkthrough: PCB Layout</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">From a Checked Schematic to a Board You Could Order</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 3 — Form Factor, Schematic and PCB <strong>Time:</strong> ~2 hours · <strong>You will produce:</strong> a routed two-layer PCB of your own product that passes DRC, a 3D render, and a STEP file of the board</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Board Can Pass Every Check and Still Not Work</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Your schematic passes ERC and every footprint is checked. Now the parts need places on a real board, and copper between them. The <strong>PCB Editor</strong> is where the product gets its size, where the sensor ends up facing the skin or not, and where the antenna is helped or blocked. Its <strong>Design Rules Check</strong> (DRC) will tell you whether the board can be made. It will not tell you whether the board is any good: that depends on decisions you make in the order this unit follows.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit walks through esp\_watch's real board in KiCad 10, step by step, then asks you to lay out your own. As in C1, it shows only what you need to make one board; the PCB Editor manual covers the rest [2].</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Set</strong> a board's design rules from your fab house's published capabilities.</li><li style="margin:6px 0;">​<strong>Draw</strong> the board outline and mounting holes from your C0 concept, and <strong>place</strong> parts outside-in.</li><li style="margin:6px 0;">​<strong>Route</strong> tracks and vias, and <strong>pour</strong> a ground plane on both layers.</li><li style="margin:6px 0;">​<strong>Keep</strong> an antenna clear of copper, and <strong>reach</strong> zero DRC errors with every warning explained.</li><li style="margin:6px 0;">​<strong>Export</strong> a 3D render and a STEP file for the enclosure work in Module 5.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Before You Start</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">You need</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">From</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A schematic with zero ERC errors, every symbol annotated</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">C1</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A footprint, checked and with a 3D model, for every symbol</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">C2</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The board outline, mounting-hole positions and the side for every part</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your C0 concept</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your fab house's current capabilities page</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">e.g. JLCPCB [3]</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">esp\_watch's KiCad project, to compare against</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pcb/esp\_Watch/ [4]</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What esp\_watch's board contains</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Item</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">On esp\_watch</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Layers</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Outline</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">37.8 × 39 mm</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top side</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO ESP32-C3, MPU-6050, OLED (on a female header above the MPU), SW1, SW2, SW3</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bottom side</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MAX30102 module, against the wrist</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tracks</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0.4 mm for signals, 0.6 mm for the 3.3 V and battery lines</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Vias</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">4</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Ground</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A GND pour on both layers</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Silkscreen</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pin names beside each module's pads, and version 0.1.0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">DRC</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Zero errors</td></tr></tbody></table>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_top.png" alt="esp_watch PCB render, top face" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch PCB render, top face</div></div>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_back.png" alt="esp_watch PCB render, bottom face, with the MAX30102 module" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch PCB render, bottom face, with the MAX30102 module</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 1: Open the PCB Editor</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">From the schematic, click <strong>Switch to PCB Editor</strong> in the top toolbar, or open the .kicad\_pcb file from the Project Manager.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Navigation is the same as in the schematic: drag with the middle or right button to pan, scroll to zoom [1]. On the right, the <strong>Layers</strong> tab of the Appearance panel shows each layer's colour, and clicking a layer's name makes it the <strong>active layer</strong>, the one you draw on. By default front copper (F.Cu) is red and back copper (B.Cu) is blue. Everything is viewed from the front, so parts on the bottom appear mirrored.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 2: Set the Design Rules</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>File → Board Setup</strong>. Three pages matter.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Board Stackup → Physical Stackup.</strong> Leave it at <strong>2</strong> copper layers. Two layers are enough for a module-based board, and cost the least.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Design Rules → Constraints.</strong> These are the smallest track, gap, via and hole the design may use. Take them from your fab house's capabilities page, then stay comfortably above them. JLCPCB currently allows 0.10 mm tracks and gaps on two-layer boards, and copper at least 0.2 mm from a routed edge [3]; numbers like these change, so check the page on the day.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's board file sets: minimum track 0.2 mm, minimum via 0.5 mm, minimum hole 0.3 mm, minimum annular ring 0.1 mm, and copper at least 0.5 mm from the edge. All sit well above JLCPCB's limits, so the board never depends on the fab's best day.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Design Rules → Net Classes.</strong> A <strong>net class</strong> gives a group of nets its own track width and clearance, so the router uses the right width automatically and DRC checks it. Make two: <strong>Default</strong> for signals, and <strong>Power</strong> (wider) for the supply and battery nets. Assign nets to Power with a pattern such as +3V3.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch uses one net class and picks the width by hand while routing: 0.4 mm for signals, 0.6 mm for the 3.3 V and battery lines, from the track-width list in <strong>Pre-defined Sizes</strong>. That works on a board this small. A Power class does the same job without relying on you to pick the right width every time.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 3: Bring the Parts In (F8)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>Tools → Update PCB from Schematic</strong> (<strong>F8</strong>). Read the list of changes, click <strong>Update PCB</strong>, close it, and click to drop the footprints on the canvas [1].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The thin lines between pads are the <strong>ratsnest</strong>: connections the schematic wants that are not yet copper. The count of unrouted connections is in the status bar.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The schematic and board do not sync themselves.</strong> After any schematic change, press <strong>F8</strong> again, or the board will be built from an old schematic.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 4: Draw the Board Outline</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Set the grid to <strong>1 mm</strong>, click <strong>Edge.Cuts</strong> in the Layers tab, and draw the outline with the <strong>rectangle</strong> tool [1]. The outline must be one closed shape. Add a <strong>dimension</strong> on each side, so the size is on every drawing of the board.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The size comes from your C0 concept, not from where the parts happen to land. If the parts do not fit, that is a C0 decision to revisit, not a reason to let the board grow quietly.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 5: Place the Mounting Holes</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Mounting holes come next, because the case's bosses and screws (Module 5) line up with them. Place them as footprints from KiCad's MountingHole library: MountingHole\_3.2mm\_M3 for an M3 screw, for example. Position them exactly, using the footprint's properties (<strong>E</strong>) to type in coordinates.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch has <strong>four mounting holes</strong>: two at the top corners and two in the middle. They hold the MPU-6050 and OLED modules on standoffs.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 6: Place the Parts, Outside In</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Select a footprint and use these keys:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Key</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Does</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>M</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>D</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Drag, keeping attached tracks</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>R</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Rotate</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>F</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Flip to the other side of the board</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>E</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Properties, to type an exact position</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Place in this order, because each step constrains the next:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Parts fixed by the outside world</strong>: connectors at the edge where the case opening will be, buttons where a finger reaches them, sensors on the face where they must look.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Parts that must be near another part</strong>: decoupling capacitors beside their chip, a crystal beside its pins.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Everything else</strong>, arranged so the ratsnest lines do not cross much. Untangled ratsnest means easy routing [1].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Keep courtyards from overlapping, unless two parts really do stack.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On esp\_watch, step 1 decided almost everything:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Board sides</strong> come from C0: everything on top except the MAX30102, which is flipped (<strong>F</strong>) to the bottom, against the wrist.</li><li style="margin:6px 0;">​<strong>The XIAO's USB-C</strong> faces the left edge, where the case will have its charging opening.</li><li style="margin:6px 0;">​<strong>The OLED</strong> sits on a female header above the MPU-6050, with a 4–5 mm air gap between them.</li><li style="margin:6px 0;">​<strong>The battery</strong> is not on the board. It stands in a slot behind the OLED's header, wired to the XIAO's BAT pads through SW3.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Breakout modules carry their own decoupling capacitors, so step 2 had nothing to place: esp\_watch's carrier board has none of its own.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 7: Route the Tracks (X)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click the layer to route on (F.Cu or B.Cu), press <strong>X</strong>, click a pad, then click the pad its ratsnest line leads to. The track follows, and the ratsnest line disappears once the connection is copper [1].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">While routing:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Change layer with a via:</strong> press <strong>V</strong> mid-track, click to drop the via, and carry on on the other layer [1].</li><li style="margin:6px 0;">​<strong>Through-hole pads join both layers</strong> already; a track can arrive on one layer and leave on the other.</li><li style="margin:6px 0;">​<strong>Pick the width</strong> from the track-width dropdown, or let the net class set it.</li><li style="margin:6px 0;">​<strong>Keep it short and direct.</strong> Route power first, at its wider width; then the bus lines, kept side by side; then the rest.</li><li style="margin:6px 0;">Watch the <strong>unrouted count</strong> in the status bar. Routing is finished at 0.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch routes 76 track segments, split almost evenly between the two layers, with only four vias: one each on SDA, SCL, the "previous" button line and 3.3 V. The through-hole pins of the modules and switches do most of the layer changes for free.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 8: Pour Ground on Both Layers (B)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>Add a filled zone</strong>, click the first corner, and in <strong>Copper Zone Properties</strong> choose the <strong>GND</strong> net and tick <strong>both</strong> F.Cu and B.Cu. Click round the board edge and double-click to finish. Press <strong>B</strong> to fill. Zones are not refilled automatically, so press <strong>B</strong> again after any change, and always before DRC and fabrication [1].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>ground pour</strong> fills the empty copper on a layer and connects it to GND. Every signal needs a path back to its source, and a solid ground under it gives the return current the shortest path. GND pads connect to the pour through thin <strong>thermal-relief</strong> spokes, which make them easier to solder [1]. <strong>Stitching vias</strong>, GND vias dropped every 5–10 mm, join the two pours so neither is left as a separate island.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch has a GND zone on both F.Cu and B.Cu and <strong>no stitching vias</strong>. The two pours join through the GND pins of the through-hole modules and switches, which pass through both layers. On a small board crowded with through-hole parts that is enough; on a board of mostly surface-mount parts, add stitching vias.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch routes its 3.3 V rail as a <strong>track</strong>, not as a second copper plane. On two layers, a power plane would be cut into pieces by every signal crossing it, and those cuts would break up the ground under the signals too. A wide track carries a watch's current just as well and leaves the ground pour whole.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A common belief is that more copper is always better, so students pour power on one side and ground on the other. On a two-layer board that usually makes things worse, for the reason above.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 9: Keep the Antenna Clear</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">An antenna radiates into the space around it. Copper nearby, especially a ground pour underneath, changes how it behaves. For a board with an antenna <strong>on</strong> it, such as a module with a printed antenna, draw a <strong>rule area</strong> (<strong>Ctrl+Shift+K</strong>) over the antenna on both layers, set to allow no copper, and refill the zones: the pour flows round it [2].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's board has no rule area, because its antenna is not on the board. The XIAO ESP32-C3 uses an <strong>external antenna</strong> on a U.FL cable, and its rules move into the case: no copper under the antenna on either layer, away from the battery's metal-foil pouch, and routed along the inside of the case wall. Mark the intended antenna position on User.Drawings now, so Module 5 can check it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 10: Label the Board</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Use the text tool on <strong>F.Silkscreen</strong> for anything someone holding the bare board needs: what each connector or pad is, + beside a battery pad, and the board's <strong>revision</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch prints the pin names beside each module's pads and version 0.1.0 on the board, matching the schematic's revision. When a board comes back from the fab, the revision on the copper is the only reliable way to tell which files made it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 11: Run DRC</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>Inspect → Design Rules Checker</strong>, keep <strong>Refill all zones before performing DRC</strong> ticked, and click <strong>Run DRC</strong>. Each violation is listed, and an arrow marks it on the board; click a line to jump to it [1].</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">DRC message (paraphrased)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Usual cause</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Fix</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Clearance violation</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A track or pad too close to another net</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move or reroute; refill zones (<strong>B</strong>)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Unconnected items</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A ratsnest line still open</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Route it; check the unrouted count</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Courtyards overlap</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Two parts placed in the same space</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move one, unless they really stack</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Copper too close to board edge</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A pad, track or pour near Edge.Cuts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move it, or let the pour clearance handle it</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Schematic parity</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The board and schematic disagree</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Press <strong>F8</strong> and update the board</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Aim for <strong>zero errors</strong>. A warning may stay, but only with a written reason: right-click it, choose <strong>Exclude</strong>, and add a comment.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch finished with <strong>zero DRC errors</strong>. Some warnings remained; the author judged them acceptable and did not record which. That is the one thing worth doing differently: an accepted warning should be a written decision, so the next person does not have to rediscover whether it matters.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Remember what a clean DRC means.</strong> It says the board <strong>can be made</strong>: every rule you set is met. It does not say the footprints match the parts (C2), that the sensor faces the skin (C0), or that the antenna works (Step 9).</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 12: Look at It in 3D</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>View → 3D Viewer</strong>. Drag to orbit, middle-drag to pan. Check that every part has a model (a missing one shows as bare pads), that the sensor is on the face you meant, and that nothing tall sits where the case will be thinnest. <strong>Preferences → Raytracing</strong> gives a slower, better-looking render; save one for your design pack [1].</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 13: Export the Board as STEP</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>File → Export → STEP / GLB / BREP / XAO / PLY / STL</strong>, choose <strong>STEP</strong>, and save [2]. The STEP file holds the board and every 3D model attached to its footprints. Module 5 imports it into Fusion to build the case around it. Gerbers and drill files, for the fab house, are F1's job.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's exported board is in its repository as <a href="https://github.com/niat-physicalai/esp_watch/blob/main/pcb/esp_Watch/esp_Watch.step">pcb/esp\_Watch/esp\_Watch.step</a>.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Tool Reference</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Tool</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Key</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Use it to</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Update PCB from Schematic</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">F8</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bring schematic changes onto the board</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Route Tracks</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">X</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Draw copper between pads</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Via (while routing)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Change layer mid-track</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Add a Filled Zone</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pour copper on a net</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fill All Zones</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">B</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Refill every pour</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Add Rule Area</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Ctrl+Shift+K</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Keep copper out of an area</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Flip</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">F</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move a footprint to the other side</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Design Rules Checker</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check the board against its rules</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3D Viewer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Inspect and render the board</td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Lay out your own product's board.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Set the rules.</strong> Two layers; constraints from your fab's capabilities page, with margin; a Power net class for supply and battery nets.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Update from the schematic</strong> (F8).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Draw the outline</strong> from your C0 concept, dimensioned, and <strong>place the mounting holes</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Place outside in</strong>: fixed parts first, then neighbours, then the rest. Flip any part that belongs on the bottom.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Route</strong> to an unrouted count of 0, power first.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. <strong>Pour GND on both layers</strong>, stitch the pours if few through-hole GND pins join them, and add a rule area over any on-board antenna. Mark a cable antenna's intended position on User.Drawings.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. <strong>Label</strong> the board with pin names and its revision.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. <strong>Run DRC to zero errors</strong>, with a written reason for every excluded warning.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. <strong>Save a 3D render and export a STEP file.</strong></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> your KiCad board (.kicad\_pcb), a screenshot of the clean DRC result, a 3D render, and the board's STEP file, saved in your design pack as C3-pcb/.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your board and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The board outline matches your C0 concept, and is dimensioned. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Your constraints are at or above your fab's current published minimums. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Supply and battery nets use a wider track than signals. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. The status bar shows 0 unrouted connections. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. GND is poured on both layers, and the pours are joined. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. No copper lies under any on-board antenna. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. DRC reports zero errors, and every excluded warning has a comment. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The board carries its revision on the silkscreen, and a STEP file has been exported. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> You add a test point to the schematic, then run DRC on the board. DRC reports the board and schematic disagree. What did you forget?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. To refill the zones.</li><li style="margin:6px 0;">B. To press F8 and update the board.</li><li style="margin:6px 0;">C. To re-run ERC.</li><li style="margin:6px 0;">D. To flip the test point to the bottom.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The board does not follow the schematic by itself; F8 brings the change across. <strong>A</strong> fixes stale copper pours, not missing parts. <strong>C</strong> checks the schematic, not the board. <strong>D</strong> changes nothing about the mismatch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> You move a part after pouring ground, and DRC reports clearance violations between its pads and the GND pour. What is the quickest correct fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Delete the zone and route ground as tracks.</li><li style="margin:6px 0;">B. Reduce the clearance rule until the errors go.</li><li style="margin:6px 0;">C. Refill the zones with B, then re-run DRC.</li><li style="margin:6px 0;">D. Exclude the violations.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Zones are not refilled automatically; the old fill still covers where the part now sits. <strong>A</strong> throws away the pour's benefits. <strong>B</strong> weakens the rule for the whole board. <strong>D</strong> hides a short circuit the fab would really make.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A board passes DRC with zero errors. Which problem could it still have?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A track narrower than the minimum set in the design rules</li><li style="margin:6px 0;">B. Two courtyards overlapping</li><li style="margin:6px 0;">C. Copper too close to the board edge</li><li style="margin:6px 0;">D. A heart-rate sensor on the face away from the skin</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> DRC checks the board against its rules; it cannot know which face should touch the wrist. <strong>A</strong>, <strong>B</strong> and <strong>C</strong> are all things DRC reports.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A two-layer board has the 3.3 V rail as a copper pour on the bottom layer and GND on the top. After routing, the bottom pour is in six separate pieces. What is the main problem?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The board costs more to make, because six separate pours need extra processing.</li><li style="margin:6px 0;">B. Signals crossing the cuts lose their ground return path below them, and the supply is fragmented.</li><li style="margin:6px 0;">C. The fab house will reject six pours.</li><li style="margin:6px 0;">D. Nothing; more copper is always better.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Every track cuts the plane, so the supply becomes islands and the return paths under the signals are broken. Route the supply as a track and pour GND on both layers instead. <strong>A</strong> and <strong>C</strong> are not true. <strong>D</strong> is the belief this example disproves.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> Your board uses a module with a printed antenna at one end. What should the layout include?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A ground pour under the antenna, to shield it from the other parts.</li><li style="margin:6px 0;">B. A wider track width near the antenna.</li><li style="margin:6px 0;">C. Stitching vias around the antenna.</li><li style="margin:6px 0;">D. A rule area with no copper under the antenna on both layers.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> Copper under an antenna changes its behaviour; a rule area keeps the pour out. <strong>A</strong> is the mistake the rule area prevents. <strong>B</strong> has nothing to do with the antenna. <strong>C</strong> puts more grounded copper beside it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6.</strong> Your fab's capabilities page lists a 0.10 mm minimum track. What should your design-rule minimum be?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 0.10 mm, to use the full capability.</li><li style="margin:6px 0;">B. 0.08 mm, since fabs have some margin.</li><li style="margin:6px 0;">C. Comfortably above it, such as 0.2 mm, unless the board really needs finer tracks.</li><li style="margin:6px 0;">D. Whatever KiCad's default happens to be, since KiCad ships with safe values.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Staying above the limit means the board never depends on the fab's best day. <strong>A</strong> works but leaves no margin. <strong>B</strong> is below what the fab promises. <strong>D</strong> may be fine or not; it was never checked against the fab.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>7.</strong> You export your board as STEP for the enclosure, and the OLED module is missing from the file. Why?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The OLED's footprint has no 3D model attached.</li><li style="margin:6px 0;">B. STEP files only include the bare board.</li><li style="margin:6px 0;">C. The OLED is on the top layer.</li><li style="margin:6px 0;">D. The zones were not refilled.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> The STEP export includes the models attached to footprints (C2, Step 8); a footprint without one adds nothing. <strong>B</strong> is false: the other parts appear. <strong>C</strong> and <strong>D</strong> do not affect the 3D export.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>8.</strong> You place a button footprint, then realise it belongs on the bottom of the board. Which key moves it there?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. F</li><li style="margin:6px 0;">B. R</li><li style="margin:6px 0;">C. M</li><li style="margin:6px 0;">D. X</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> F flips a footprint to the other side; its pads change layer and it appears mirrored. <strong>B</strong> rotates, <strong>C</strong> moves on the same side, and <strong>D</strong> starts routing a track.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>9.</strong> A route on the top layer is blocked, and the track must cross under another to reach its pad. What do you do?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Route straight through the other track; DRC will flag nothing.</li><li style="margin:6px 0;">B. Make the track narrower so it squeezes past the other one.</li><li style="margin:6px 0;">C. Press V to drop a via and continue on the bottom layer.</li><li style="margin:6px 0;">D. Delete the other track and route it again later, after this one.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> A via takes the track to the other layer, under the obstacle. <strong>A</strong> would short two nets, which DRC reports. <strong>B</strong> does not help it cross. <strong>D</strong> just moves the problem.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The hardware design is complete. Module 4 writes the firmware that runs on it, starting with <a href="../04-firmware/D0-firmware-architecture.md">D0 — Firmware Architecture</a>. Module 5 imports this board's STEP file into Fusion and builds the case around it, and F1 turns the board into the files a fab house needs.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. KiCad. Getting Started in KiCad, version 10.0 (PCB editor basics, board setup, update from schematic, outline, placement, routing, zones, DRC, 3D viewer). https://docs.kicad.org/10.0/en/getting\_started\_in\_kicad/getting\_started\_in\_kicad.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. KiCad. PCB Editor reference manual, version 10.0 (rule areas, 3D model export). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. JLCPCB. PCB Manufacturing and Assembly Capabilities (1–2 layer minimum track and spacing 0.10 / 0.10 mm; copper clearance from routed edges ≥ 0.2 mm). https://jlcpcb.com/capabilities/pcb-capabilities</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. niat-physicalai. esp\_watch (KiCad project and board STEP in pcb/esp\_Watch/). https://github.com/niat-physicalai/esp\_watch</div>
