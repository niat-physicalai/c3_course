<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Footprints</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What a Footprint Is</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>footprint</strong> is the set of copper pads, holes and outlines that stands for one part on the board. Each pad has a number, and it must match the symbol's pin number. A footprint also carries non-copper layers:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Layer</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it holds</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Who uses it</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Copper (F.Cu, B.Cu)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pads</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The fab house</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Silkscreen (F.Silkscreen)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Outline and pin-1 mark printed on the board</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The person soldering</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fabrication (F.Fab)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The part's true body outline</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Assembly drawings</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Courtyard (F.Courtyard)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The area no other part may enter</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">DRC</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">User.Drawings</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your own notes and markers</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">You, and the enclosure designer</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Draw, Source or Verify</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Every footprint on your board falls into one of three cases:</div>

```text
                   Does a footprint already exist?
                         │
             ┌───────────┴───────────┐
            no                       yes
             │                        │
     ┌───────▼───────┐        ┌───────▼────────────────┐
     │  DRAW it from │        │ From KiCad's own        │
     │  a mechanical │        │ library, for a standard │
     │  drawing or a │        │ part (e.g. a pushbutton)│
     │  calibrated   │        └───────┬────────┬───────┘
     │  photo        │               yes       no (downloaded
     └───────┬───────┘                │         from elsewhere)
             │              spot-check│   ┌──────▼──────┐
             │              pin 1 and │   │ VERIFY all  │
             │              pitch     │   │ four        │
             │                        │   │ measurements│
             └──────────┬─────────────┘   └──────┬──────┘
                        ▼                        │
              Record it in the footprint ◄───────┘
              verification checklist
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A downloaded footprint is unverified until you have checked it yourself.</strong> DRC checks that pads keep their distance from each other; it has no idea whether they are where the real part's pins are.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch used all three routes:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Part</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Route</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Source</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">XIAO ESP32-C3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sourced</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Downloaded from an open-source repository [3]</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MAX30102 module</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Drawn</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">By the author, from a calibrated photo</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MPU-6050 and OLED modules</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sourced</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Downloaded</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SW1, SW2, SW3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sourced</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">KiCad's standard library: SW\_PUSH\_6mm and the Würth slide switch</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Four Measurements</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">#</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Measurement</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What goes wrong if it is off</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Pad pitch</strong>: centre to centre, along a row and between rows</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pins miss their pads; the error grows along the row</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Pad and hole size</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pins do not fit, or pads are too small to solder</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Courtyard and body outline</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Parts overlap, or the enclosure does not fit</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">4</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Pin 1 position and numbering</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The part fits but is wired backwards</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The pitch error grows along the row. A footprint drawn at 2.50 mm instead of 2.54 mm has pin 2 0.04 mm out, and pin 8 7 × 0.04 = 0.28 mm out. A 0.64 mm square pin is about 0.9 mm across its corners, so a 1.0 mm hole leaves only about 0.05 mm of slack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: The MAX30102 Module Footprint</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The author drew esp\_watch's black MAX30102 module footprint from a <strong>calibrated photo</strong>: a photo taken straight down, using the module's own edge pads as the ruler.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 1: Calibrate the photo.</strong> The edge pads are on a standard 2.54 mm grid, so their spacing is a known length. In the photo, the pitch measured <strong>62.2 pixels</strong>.</div>

```text
Scale = 62.2 px ÷ 2.54 mm = 24.5 px/mm
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 2: Measure the body.</strong> At that scale the body measured <strong>20.2 × 15.6 mm</strong>. The seller's nominal size is 21 × 16 mm; the footprint outlines it as <strong>20 × 15 mm</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Notice how the module is mounted.</strong> esp\_watch's module is not on header pins. It is soldered <strong>flat</strong>, sensor-side out, through the pads along its edges, so the footprint needs <strong>surface-mount (SMD) pads</strong>, not holes.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 4: Place the pads.</strong> Two rows of four at <strong>2.54 mm</strong> pitch. The rows are <strong>18 mm</strong> apart, centre to centre, so each sits under one edge of the module.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 5: Size the pads for hand soldering.</strong> Each pad is a <strong>2 × 3 mm</strong> rectangle that starts at the module's edge and runs 3 mm outward, so the iron can reach copper the module does not cover.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 6: Outline the body</strong> on a drawing layer, so the enclosure designer can see where the module sits. Use F.Fab or User.Drawings, never <strong>Margin</strong>: graphics on Margin inside esp\_watch's footprint stopped KiCad's router reaching the pads.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 7: Mark what the enclosure needs.</strong> The footprint outlines the module, not the 5.6 × 3.3 mm sensor on it. The case window must line up with the sensor, so add that rectangle yourself, measured from the photo.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The result: <a href="../assets/kicad/MAX30102_module.kicad_mod">assets/kicad/MAX30102\_module.kicad\_mod</a>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Pad 1 to pad 4 along a row should measure 3 × 2.54 = 7.62 mm; row to row, 18 mm. Measure both in the Footprint Editor before saving.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">How To: Draw a Footprint in the Footprint Editor</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: Open the Footprint Editor</strong> and create a project footprint library (<strong>File → New Library</strong>, <strong>Project</strong>), as for symbols [4].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 2: Create the footprint</strong> (right-click the library → <strong>New Footprint</strong>). Name it after the part, as for symbols.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Set the grid</strong> to 2.54 mm, or 1.27 mm, so pads land on the module's pitch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 4: Place pad 1</strong> with the <strong>Add Pad</strong> tool, then edit it (<strong>E</strong>). Choose <strong>SMD</strong> for a module soldered flat, or <strong>Through-hole</strong> for one on header pins, and set the size and number.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 5: Place the other pads</strong> on the grid, numbered in the same order as the module and your symbol.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 6: Draw the outlines on the right layers.</strong> Body on F.Fab; a silkscreen outline just outside it with a pin-1 mark; a courtyard on F.Courtyard about 0.25 mm outside everything. Pick the layer in the Layers panel before drawing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 7: Measure.</strong> Use the measure tool from pad 1 to the last pad of the row, and row to row. Record both in your checklist.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 8: Attach a 3D model.</strong> Open the footprint's properties, <strong>3D Models</strong> tab, and add the part's STEP file. Without it, the part is missing from the board's 3D view and from the STEP you will export to Fusion in Module 5.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's repository has STEP models for the XIAO, the MAX30102, MPU-6050 and OLED modules, the female header and the Würth switch, in <a href="https://github.com/niat-physicalai/esp_watch/tree/main/pcb/esp_Watch/3d%20models">pcb/esp\_Watch/3d models/</a>. For your own parts, look on the manufacturer's or seller's page, or on a model-sharing site such as GrabCAD; if there is none, a box of the right size is enough.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 9: Save, and assign it</strong> to the symbol: the Footprint field in the symbol, or Assign Footprints (C1, Step 11).</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Verifying a Downloaded Footprint</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Five steps before you trust it:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Open it in the Footprint Editor</strong> and look at every layer, not just copper.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Measure the pitch</strong> between the first two pins and across the full row, against the part's drawing or your calibrated photo.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Check pad and hole sizes</strong> against the part's pins.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Check pin 1</strong>: which pad is marked, and does the numbering match your symbol?</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Check for stray graphics</strong> on copper, courtyard, edge or Margin layers.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Step 5 comes from esp\_watch: graphics on the <strong>Margin</strong> layer inside a footprint stopped the router reaching its pads. Moving them to F.Fab or User.Drawings fixed it. The footprint was electrically correct; a drawing on the wrong layer was enough to block routing.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Footprint Verification Checklist</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">One row per footprint on your board. This table is part of your deliverable.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Part</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Route</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Source</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Pitch</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Pad/hole</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Courtyard</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Pin 1</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Checked against</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Date</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">e.g. MAX30102 module</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Drawn</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Calibrated photo</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2.54 / rows 18</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SMD 2 × 3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">body 20 × 15</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Matches symbol</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Photo, 24.5 px/mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>List every part</strong> on your C1 schematic and decide, for each, whether its symbol and footprint are drawn, sourced or need verifying.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Draw at least one symbol</strong> in a project library. Number the pins from the part you will solder, and type each one by what it does.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Draw at least one footprint</strong> in a project library, from a mechanical drawing or a calibrated photo. Record the four measurements, and attach a 3D model (or a box).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Verify every downloaded symbol and footprint</strong> with the steps above.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Assign every footprint</strong> in your schematic and re-run ERC to zero errors.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> your project symbol and footprint libraries, and the completed footprint verification checklist, saved in your design pack as C2-symbols-and-footprints/.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your libraries and checklist and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. At least one symbol and one footprint were drawn by you, in project libraries. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every drawn symbol's pin numbers were checked against the part you will solder. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. No pin is "unspecified", and no active pin is marked passive to hide an error. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every footprint's pad numbers match its symbol's pin numbers. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every footprint is in the checklist, with all four measurements ticked. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Every body outline is on F.Fab or User.Drawings, and nothing is drawn on Margin. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Every footprint has a 3D model or a stand-in box attached. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. ERC still reports zero errors with every footprint assigned. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A student uses the MAX30102 chip symbol from a library for a MAX30102 module with 8 edge pads. What goes wrong?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing; the chip is the same.</li><li style="margin:6px 0;">B. ERC fails on every pin, because chip symbols cannot be used for modules.</li><li style="margin:6px 0;">C. The pin numbers match the chip, not the module's pads.</li><li style="margin:6px 0;">D. The I²C address changes.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Pin numbers must match the part you solder, and the module's 8 pads are not the chip's 14. <strong>A</strong> ignores that the module is a different physical part. <strong>B</strong> is unlikely: ERC checks types and connections, not which physical part you chose. <strong>D</strong> is a property of the chip, unaffected by the symbol.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A light sensor's interrupt pin is open-drain, active-low, and shares its net with a pull-up resistor. Which electrical type is correct?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Output</li><li style="margin:6px 0;">B. Power output</li><li style="margin:6px 0;">C. Passive</li><li style="margin:6px 0;">D. Open collector</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> Open collector describes a pin that can only pull low, and lets it share a net with a pull-up. <strong>A</strong> describes a push-pull output that also drives high, which this pin cannot. <strong>B</strong> is for supply pins. <strong>C</strong> hides the pin's behaviour from ERC.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A classmate sets every pin on their new symbol to passive, and ERC goes quiet. What have they lost?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing; ERC checks passive pins exactly as it checks every other type.</li><li style="margin:6px 0;">B. ERC's ability to catch an unpowered part or two outputs on one net.</li><li style="margin:6px 0;">C. The ability to assign a footprint.</li><li style="margin:6px 0;">D. The pin numbers.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> ERC's checks depend on pin types; passive tells it nothing. <strong>A</strong> is false for the same reason. <strong>C</strong> and <strong>D</strong> are unaffected by pin types.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A downloaded footprint for a 10-pin header uses a 2.50 mm pitch. If pin 1 is lined up, how far out is pin 10?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 0.04 mm</li><li style="margin:6px 0;">B. 0.40 mm</li><li style="margin:6px 0;">C. 0.36 mm</li><li style="margin:6px 0;">D. 2.54 mm</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Pin 10 is nine pitches from pin 1: 9 × 0.04 = 0.36 mm. <strong>A</strong> is the error at pin 2 only. <strong>B</strong> counts ten pins instead of nine gaps. <strong>D</strong> confuses the pitch with the error.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A module photo shows edge pads 50.8 pixels apart, and the body is 406 pixels wide. How wide is the body?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 20.3 mm</li><li style="margin:6px 0;">B. 8.0 mm</li><li style="margin:6px 0;">C. 16.0 mm</li><li style="margin:6px 0;">D. 203 mm</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> The scale is 50.8 ÷ 2.54 = 20 px/mm, so 406 ÷ 20 = 20.3 mm. <strong>B</strong> divides by the pixel pitch, counting pitches, not millimetres. <strong>C</strong> uses 25.4 px/mm, mixing up the pitch with an inch. <strong>D</strong> is a factor-of-ten slip.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6.</strong> A calibrated photo of a 2 × 3 header module gives a row spacing of 7.51 mm, at 20 px/mm. What should the footprint use?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 7.51 mm, because it was measured.</li><li style="margin:6px 0;">B. 7.80 mm, to leave some clearance.</li><li style="margin:6px 0;">C. 7.50 mm, rounded to the nearest 0.5 mm.</li><li style="margin:6px 0;">D. 7.62 mm (3 × 2.54).</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> Header pins sit on the 2.54 mm grid by construction, and 0.11 mm is about 2 pixels of measuring error. <strong>A</strong> trusts the less reliable source. <strong>B</strong> and <strong>C</strong> match neither the grid nor the measurement.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>7.</strong> In the PCB editor, the router will not reach the pads of one footprint, though DRC shows no clearance problem in the footprint itself. What should you check first?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The track width set in the board's default net class.</li><li style="margin:6px 0;">B. Graphics on the Margin layer inside the footprint.</li><li style="margin:6px 0;">C. The board thickness.</li><li style="margin:6px 0;">D. The silkscreen font size.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Graphics on Margin inside a footprint can block the router, exactly as on esp\_watch; move them to F.Fab or User.Drawings. <strong>A</strong> would affect every footprint, not one. <strong>C</strong> and <strong>D</strong> do not affect routing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>8.</strong> Your symbol numbers a module's pins 1 to 8 starting from VCC; your footprint numbers its pads 1 to 8 starting from INT, at the other end. Both look correct on their own. What happens on the board?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Every pin connects to the wrong pad, mirrored end to end.</li><li style="margin:6px 0;">B. ERC reports the mismatch.</li><li style="margin:6px 0;">C. KiCad renumbers the pads to match.</li><li style="margin:6px 0;">D. Only pin 1 is wrong; the other seven pads still line up with their pins.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> Pads join nets by number, so counting from opposite ends reverses every connection. <strong>B</strong> and <strong>C</strong> do not happen: neither tool knows which end is the real pin 1. <strong>D</strong> underestimates it: all eight move.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every part now has a symbol, a checked footprint and a 3D model. In <a href="C3-kicad-pcb-walkthrough.md">C3 — KiCad Walkthrough: PCB Layout</a> you lay out the board itself.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. KiCad. Schematic Editor reference manual, version 10.0 (pin electrical types, PWR\_FLAG, Symbol Editor, symbol library tables). https://docs.kicad.org/10.0/en/eeschema/eeschema.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Analog Devices. MAX30102 datasheet (interrupt pin: active-low, open-drain). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. VectorSpaceHQ. XIAO\_ESP32C3: KiCad footprint and symbol for XIAO ESP32C3 (KiCad v7 files; battery pads; GPL-3.0; commit history). https://github.com/VectorSpaceHQ/XIAO\_ESP32C3</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. KiCad. PCB Editor reference manual, version 10.0 (Footprint Editor, pad properties, layers, 3D models). https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html</div>
