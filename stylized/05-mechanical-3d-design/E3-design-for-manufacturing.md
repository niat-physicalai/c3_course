<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">E3 — Design for Manufacturing</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Making the Case Printable, and Holding a Prototype Together</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 5 — Mechanical and 3D Design <strong>Time:</strong> ~1.5 hours · <strong>You will produce:</strong> a completed DFM self-audit checklist for your enclosure, and a hardware list with supplier links</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Perfect Model Is Not a Printable Part</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Your CAD enclosure has 1.5 mm walls, a lid with 0.1 mm to spare, square corners and a display window with a flat overhanging lip. Printed, the walls come out a different thickness, the lid will not go on, the base flares at the bottom and the lip droops into strings. Part 1 explains why.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Design for manufacturing</strong> (DFM) means shaping the part to suit the process that will make it. Your prototype will be 3D printed, so this unit is about FDM printing and the off-the-shelf hardware that holds printed prototypes together: threaded inserts, M2–M4 screws, nuts, magnets and snap fits. A short section at the end explains why mass-produced cases are moulded instead.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Choose</strong> wall thicknesses, clearances and orientations that suit FDM printing.</li><li style="margin:6px 0;">​<strong>Identify</strong> overhangs, bridges and first-layer problems in a model before printing.</li><li style="margin:6px 0;">​<strong>Select</strong> fastening hardware (heat-set insert, self-tapping screw, captive nut, magnet, snap fit or press fit) and <strong>design</strong> the boss, hole or pocket it needs.</li><li style="margin:6px 0;">​<strong>Complete</strong> a DFM self-audit of your own enclosure.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — FDM Realities</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">How FDM Builds a Part</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>FDM</strong> (fused deposition modelling, also called FFF) melts a plastic filament and lays it down through a nozzle, one line at a time, one layer at a time. Almost every FDM design rule follows from three facts:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Plastic goes down in lines of a fixed width.</strong> With a 0.4 mm nozzle, a line is about 0.45 mm wide.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Each layer needs something underneath it.</strong> A layer printed over empty air droops.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Hot plastic shrinks as it cools.</strong> Parts pull and curl, especially at their base.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Wall Thickness: Count the Lines</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A wall is printed as a number of side-by-side lines, called <strong>perimeters</strong>. Prusa's guidance for a 0.4 mm nozzle gives approximate wall thicknesses for each count [1]:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Perimeters</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Approximate wall thickness</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0.45 mm</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0.9 mm</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1.35 mm</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">4</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1.8 mm</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A wall that falls between two of these, such as 1.5 mm, is printed as three perimeters plus a thin, awkward gap fill. It is better to choose a wall that is a whole number of perimeters.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Choosing a Wall for the E0 Enclosure</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In E0 the example wall was 1.5 mm. <strong>Assumption:</strong> a 0.4 mm nozzle with 0.45 mm lines.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 1: How many lines is 1.5 mm?</div>

```text
1.5 mm ÷ 0.45 mm = 3.33 lines
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">It is three full perimeters with a 0.15 mm gap to fill, which the slicer handles poorly.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 2: Round to a whole number.</div>

```text
3 perimeters = 1.35 mm   (thinner, lighter)
4 perimeters = 1.80 mm   (stronger, adds 0.9 mm to the overall width)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Check against the product.</strong> For a small watch case that must survive knocks, and whose strap lugs carry load (E4), four perimeters is the safer choice for the side walls. The base and lid could stay at three. With E0's parameters, that means wall = 1.8, floor\_t = 1.35, lid\_t = 1.35, and the model updates itself.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The outer width becomes 37.8 + 1 + 3.6 = 42.4 mm, and the height becomes 14.044 + 1 + 2.7 = 17.7 mm, slightly thinner than before. Both changes are one parameter edit each.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;background:#fef2f2;border-left:4px solid #dc2626;border-radius:6px;padding:8px 14px;color:#991b1b;">esp\_watch's printer, material, layer height and wall settings are not recorded. The numbers above are <strong>example values</strong> for a common 0.4 mm nozzle. Take your own from your printer or print service.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Clearance Between Parts</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Printed parts are not exact. Prusa states that its printers are accurate to at least 0.2 mm, and that materials can warp and shrink, so parts that must fit together need a deliberate gap; for parts that move, it suggests starting with at least 0.3 mm [1]. Another printer maker's design rules suggest about 0.2 mm for a loose fit and 0.1 mm for a tight fit [2].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">There is no single right value. It depends on your printer, material, part size and orientation. The professional habit is to <strong>print a test</strong>: a small pair of parts with a range of clearances, such as 0.1, 0.2, 0.3 and 0.4 mm, and use the one that fits the way you want. Make the clearance a parameter (E0), so the result can be applied everywhere at once.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/CAD/E3-01.png" alt="A clearance test print: pins beside a row of holes, each hole labelled with its clearance" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">A clearance test print: pins beside a row of holes, each hole labelled with its clearance</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Image: Bambu Lab Wiki, <a href="https://wiki.bambulab.com/software/bambu-studio/ksr-fdm-test/pins_dimensions_wiki.jpg">FDM test: pins dimensions</a>.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Orientation, Overhangs and Bridges</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Orientation</strong> decides which faces are smooth, where supports go and in which direction the part is strong. FDM parts are weakest between layers, so orient the part so that loads run along the layers rather than trying to peel them apart.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">An <strong>overhang</strong> is a surface that leans out over nothing. The Hubs design guide notes that an overhang up to about 45° can usually be printed without support, because each new layer still rests about half on the one below; beyond that, support is needed [3]. A <strong>bridge</strong> is a horizontal span between two supports; long bridges sag, and the same guide warns of sagging beyond about 5 mm [3].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For an enclosure, orientation usually means:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Base:</strong> print it open side up, floor on the bed. The floor is flat, the walls are vertical, and nothing overhangs except the openings in the walls.</li><li style="margin:6px 0;">​<strong>Lid:</strong> print it outer face down, for a smooth visible face, with any lip or inner features pointing up.</li><li style="margin:6px 0;">​<strong>Side openings</strong>, such as a USB-C port, are holes in vertical walls, so their tops are bridges. Keep them short, or shape the top of the opening as a pointed arch or a 45° chamfer so it needs no support.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The First Layer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The first layer is pressed onto the bed to make it stick. It spreads slightly wider than the rest, a flare called <strong>elephant's foot</strong> [3], so a base printed floor-down is a little wider at the bottom. Materials that print hot, such as ABS, also tend to <strong>warp</strong>, curling up at the corners as they cool [3].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two design habits help: add a small <strong>chamfer</strong> (about 0.3–0.5 mm) to edges that touch the bed, so the flare does not interfere with fits; and give corners a <strong>radius</strong> rather than a sharp point, which reduces warping.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — Holding a Prototype Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Prototyping Toolkit</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Printed parts are held together with a small set of cheap, standard hardware. All of it is sold by Indian maker suppliers such as Robu, usually in packs.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Method</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How it works</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Strengths</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Weaknesses</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Good for</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Heat-set insert + machine screw</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A brass insert is pressed into a printed hole with a hot soldering iron and melts itself in. A machine screw (M2, M2.5, M3…) threads into the brass.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Strong threads that survive many openings</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">One extra part and a step; needs a boss wide enough</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cases opened often, for example for battery service</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Self-tapping screw</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A screw with a sharp thread cuts its own thread into a plain printed hole</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No extra parts; cheapest</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Plastic threads wear out after a few openings</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cases opened rarely</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Captive nut</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A hexagonal pocket holds a standard nut; a machine screw passes through the other part into it</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cheap, strong, no heat step</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Needs space for the hex pocket</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Larger parts and mounts; M3/M4</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Magnets</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Small neodymium disc magnets are pressed or glued into matching pockets in the two parts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No tools; opens and closes by hand; hidden</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Weak against a knock; must get polarity right</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery hatches and lids that open often</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Snap fit</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A flexible hook on one part clicks over a lip on the other</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No extra parts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Can break if flexed too far; takes test prints to tune</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lids that open by hand</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Press (interference) fit</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">One part is slightly larger than the hole it goes into, and friction holds it</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Simple, invisible</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Very sensitive to print accuracy; loosens with wear</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Parts that rarely come apart</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Choosing a Screw Size</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Size</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Typical use in a prototype</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>M2 / M2.5</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Small wearables and handheld cases, and mounting small PCBs. M2 and M2.5 match many module mounting holes.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>M3</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The default prototyping size: enclosures, brackets, mounting larger boards. Screws, nuts, inserts and standoffs are the easiest to find.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>M4</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Larger products, wall or desk mounts, and anything carrying real load. Too big for a watch.</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The "M" number is the thread's outer diameter in millimetres, so an M3 screw is 3 mm across the thread. Pick one or two sizes for the whole product, so one screwdriver and one bag of inserts do everything.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Designing the Boss, Hole or Pocket</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The hardware decides the hole, so <strong>buy or choose the part first, then design to its datasheet or listing</strong>. Put every size in a named parameter (E0), so a change of hardware is one edit.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Hardware</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What to design</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where the size comes from</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heat-set insert</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A hole slightly smaller than the insert's outside diameter, a little deeper than the insert, inside a <strong>boss</strong> about twice the insert's outside diameter</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The insert supplier's recommended hole diameter and depth</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Self-tapping screw</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A pilot hole a little smaller than the screw's thread</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The screw supplier's pilot-hole figure, then a test print</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Captive nut</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A hexagonal pocket sized to the nut's across-flats width plus your clearance (Part 1)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Nut size (for example, an M3 nut is 5.5 mm across flats)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Magnet</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A round pocket sized to the magnet plus clearance, at a depth that leaves a thin skin (about one or two layers) or lets the magnet sit flush</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The magnet's diameter and thickness</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Clearance hole (screw passes through)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A hole slightly larger than the screw, for example about 3.2–3.4 mm for M3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Standard clearance tables, then a test print</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Example values.</strong> A common M3 heat-set insert is roughly 4–5 mm across and 4–6 mm long, and needs a boss of about 8–9 mm outside diameter. Sizes differ between brands, which is exactly why you design from the listing of the insert you actually bought.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/CAD/E3-03.png" alt="A brass heat-set insert being pressed into a printed part with a soldering iron" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">A brass heat-set insert being pressed into a printed part with a soldering iron</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Image: CNC Kitchen, <a href="https://www.cnckitchen.com/blog/threaded-inserts-for-3d-prints-cheap-vs-expensive">Threaded inserts for 3D prints: cheap vs expensive</a>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Magnets, three habits:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Mark the polarity.</strong> Put all magnets in one part with the same face up, then place the other part's magnets by letting them attract. A reversed magnet repels the lid.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Glue or embed them.</strong> A press fit alone can let a magnet pull out. A drop of glue, or pausing the print to drop the magnet in and printing over it, holds it for good. Your slicer can insert a pause at a chosen layer (E5).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Keep them away from a magnetometer.</strong> A magnet next to a compass sensor ruins its readings. The MPU-6050 has no magnetometer, so this does not affect esp\_watch, but it would affect a nine-axis IMU.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's lid is held on by an <strong>interference fit</strong>. It is simple and invisible, but it is the method most sensitive to the printer: the lid may be too tight on one printer and too loose on another, and it loosens each time the case is opened. Charging is through the side USB-C opening, so the lid comes off only for battery or board service. If that is frequent, a snap fit tuned with test prints, M2 screws into heat-set inserts, or a pair of magnets would be more repeatable. Record the trade-off as a decision note (A2).</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 3 — A Note on Mass Production</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Printing is right for a prototype: no tooling, parts in hours, and every print can be different. Commercial watch cases are <strong>injection moulded</strong> instead. Molten plastic is forced into a steel mould, and a part comes out in seconds. The mould is a large one-off cost, so moulding only pays off over thousands of parts.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A printed design usually needs rework before it can be moulded. Walls need a slight taper (<strong>draft</strong>, about 1–2°) so the part slides out [4]. Walls must be a uniform thickness to avoid sink marks, and they are stiffened with thin ribs rather than made thicker [5][6]. Side holes need extra moving parts in the mould [6]. You don't need to design for any of this now. If your product ever goes to volume, the moulding company will review the design with you.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Fix walls to whole perimeters.</strong> Set your wall, floor and lid parameters to multiples of your line width, with a reason for each.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Set clearances from a stated source.</strong> Take your fit clearance from your printer's (or print service's) documentation and record the source. If you can print, model the 0.1–0.4 mm test pair as a parametric part and use the fit you prefer.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Choose orientations.</strong> Decide how each part will be printed, and remove or reshape overhangs and long bridges.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Choose your fastening hardware.</strong> Pick the method and the screw size, with a reason tied to how often the case is opened. Find a real listing for the insert, screw, nut or magnet. Design each boss, hole or pocket from its sizes, as named parameters.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Complete the DFM self-audit</strong> below for your enclosure.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">DFM Self-Audit Checklist</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">#</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Item</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Y/N</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Note</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every wall is a whole number of perimeters for my nozzle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Clearances come from a test print or documented printer accuracy</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Clearance is a single parameter used for every fit</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">4</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Each part has a chosen print orientation</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">5</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No overhang steeper than about 45° without support, or support is planned</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">6</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No bridge longer than about 5 mm, or it is reshaped</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">7</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Edges touching the bed have a small chamfer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">8</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Corners touching the bed have a radius, to reduce warping</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">9</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The fastening method and screw size are chosen, with a reason</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">10</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Holes, bosses and pockets for inserts, screws, nuts or magnets are sized from a real supplier listing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">11</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every hardware size is a named parameter</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">12</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A hardware list (part, size, quantity, supplier link) is saved with the design</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> the completed checklist, with a note on every "N", and your hardware list (part, size, quantity, supplier link), saved in your design pack as E3-dfm-audit.md.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open E3-dfm-audit.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every row of the audit has a Y or N. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every "N" has a note explaining the plan or the accepted risk. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Your wall parameter is a whole number of perimeters. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Your clearance value has a stated source. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Each part's print orientation is written down. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The fastening choice is justified by how often the case will be opened. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Every insert, screw, nut or magnet in the design appears in the hardware list with a supplier link. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Any change you made in CAD was made through parameters. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> With a 0.4 mm nozzle printing 0.45 mm lines, which wall thickness prints most cleanly?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 1.5 mm</li><li style="margin:6px 0;">B. 1.35 mm</li><li style="margin:6px 0;">C. 1.0 mm</li><li style="margin:6px 0;">D. 0.6 mm</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> 1.35 mm is exactly three perimeters. <strong>A</strong> is 3.33 lines and leaves an awkward gap to fill. <strong>C</strong> is 2.2 lines and <strong>D</strong> is 1.3 lines, both leaving partial lines.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A lid designed with 0.05 mm clearance will not fit on its printed base. What is the best fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Sand the lid until it fits.</li><li style="margin:6px 0;">B. Increase the clearance parameter to a value found from a test print, such as 0.2 mm, and reprint.</li><li style="margin:6px 0;">C. Print slower.</li><li style="margin:6px 0;">D. Remove the clearance entirely.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Printers are only accurate to a few tenths of a millimetre, so fits need a tested clearance, applied through the parameter so every fit updates. <strong>A</strong> fixes one part and teaches nothing. <strong>C</strong> may help slightly, but will not make 0.05 mm reliable. <strong>D</strong> makes the problem worse.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A USB-C opening in a vertical wall prints with a drooping top edge. What is the simplest design fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Make the wall thicker.</li><li style="margin:6px 0;">B. Shape the top of the opening as a 45° chamfer or pointed arch, so it needs no support.</li><li style="margin:6px 0;">C. Print the case upside down.</li><li style="margin:6px 0;">D. Use ABS instead of PLA.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The top of a hole in a vertical wall is a bridge; shaping it so each layer rests on the one below removes the need for support. <strong>A</strong> leaves the span unchanged, so the top still sags. <strong>C</strong> may create other overhangs. <strong>D</strong> is more prone to warping, and does not solve bridging.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A case with the battery inside is opened often for service. Which fastening method suits it best?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Interference fit</li><li style="margin:6px 0;">B. Self-tapping screws into plastic</li><li style="margin:6px 0;">C. Machine screws into heat-set inserts</li><li style="margin:6px 0;">D. Glue</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Brass inserts give reusable threads that survive repeated opening. <strong>A</strong> loosens with each opening and depends on print accuracy. <strong>B</strong> wears its plastic threads each time. <strong>D</strong> makes service impossible.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A battery hatch on a desk-top device must open by hand many times, with no tools. Which fastening suits it best?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Self-tapping screws</li><li style="margin:6px 0;">B. A pair of disc magnets in glued pockets, polarity marked</li><li style="margin:6px 0;">C. A press fit</li><li style="margin:6px 0;">D. Captive M4 nuts</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Magnets open and close by hand indefinitely without wearing anything. <strong>A</strong> and <strong>D</strong> need a tool, and self-tapped threads wear out. <strong>C</strong> loosens with every opening and depends on print accuracy.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="E4-functional-mechanical-design.md">E4 — Functional Mechanical Design for a Wearable</a> you will design the features that make the case work on a body: the sensor window, strap lugs, battery bay, button feel and sweat protection.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Prusa Research. Modeling with 3D printing in mind (wall thickness per perimeter for a 0.4 mm nozzle; accuracy "at least 0.2 mm"; at least 0.3 mm for movable parts). https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind\_164135</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Hydra Research. Design Rules for FFF 3D Printing (clearance about 0.2 mm loose, 0.1 mm tight; walls at least two extrusions wide). https://www.hydraresearch3d.com/design-rules</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Protolabs Network (Hubs). How to design parts for FDM 3D printing (overhangs up to about 45° without support; bridges sag beyond about 5 mm; elephant's foot; warping; chamfer bed edges). https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Protolabs. Draft Angle Guidelines for Injection Molding (0.5° on vertical faces strongly advised; 1–2° works in most situations). https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Protolabs. Injection Molding Wall Thickness Guidelines (uniform walls; adjoining walls no less than 40–60% of each other). https://www.protolabs.com/resources/design-tips/improving-part-design-with-uniform-wall-thickness/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Protolabs. Injection Molding Basics (radii, ribs at 40–60% of adjacent wall, core-cavity approach, undercuts and side actions). https://www.protolabs.com/resources/design-tips/injection-molding-basics/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
