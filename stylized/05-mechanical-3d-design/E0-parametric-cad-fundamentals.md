<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">E0 — Parametric CAD Fundamentals</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Fusion Walkthrough: A Case That Follows the Board</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 5 — Mechanical and 3D Design <strong>Time:</strong> ~2 hours · <strong>You will produce:</strong> a parametric practice part and a shelled two-part enclosure</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Board Will Change. Will the Case Follow?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">You finish an enclosure model on Friday. On Monday, the board grows by 2 mm because a connector moved in your layout. You open the case model and change the outer width. The lid no longer matches. The screw bosses are now off-centre. The display window is in the wrong place. The fillets fail because the edges they were attached to have gone. By Tuesday you are drawing the case again from scratch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This is what happens when a model is built from typed-in numbers with no relationships between them. <strong>Parametric CAD</strong> works differently. Each dimension is defined in terms of a few named <strong>parameters</strong>, such as the board's width, the wall thickness and the clearance, and every feature is built on the ones before it. Change the board width in one place, and the case, lid and openings all recalculate.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit walks through a simple two-part case for esp\_watch's board in <strong>Autodesk Fusion</strong>, step by step. As in the KiCad walkthroughs, it shows only the tools you need to build one enclosure; Fusion's help covers the rest [4]. This course uses only <strong>solid modelling</strong>: the <strong>Solid</strong> tab of Fusion's Design workspace. The Surface, Mesh, Sheet Metal and Form tools are not needed for a printed case.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Find</strong> your way round the Fusion window: browser, toolbar, canvas, ViewCube and timeline.</li><li style="margin:6px 0;">​<strong>Define</strong> named user parameters and formulas, so that one change updates the whole model.</li><li style="margin:6px 0;">​<strong>Draw</strong> fully constrained sketches using geometric constraints and dimensions.</li><li style="margin:6px 0;">​<strong>Build</strong> solids with extrude, fillet, shell and split body, in an order that survives change.</li><li style="margin:6px 0;">​<strong>Read and repair</strong> the timeline when a change breaks a feature, and <strong>export</strong> the model for E2.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Before You Start</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">You need</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">From</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Autodesk Fusion, installed, with an education licence</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Autodesk's education site [1]</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your board's width, length and height with parts fitted</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">C3 (the board file) and your C0 concept</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The openings your case needs: display, buttons, ports</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your C0 concept</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">esp\_watch's board size, to follow along</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">37.8 × 39 mm, 14.044 mm tall with parts fitted</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Autodesk offers eligible students and educators free, one-year access to Fusion for educational use, renewable while you remain eligible [1]. <strong>Onshape</strong> is a browser-based alternative with the same core ideas.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's enclosure was modelled in <strong>Onshape</strong>, not Fusion: a case with a top lid carrying four openings (the display window, two buttons and the slide switch). Onshape calls its parameters <strong>variables</strong>, and keeps them in a <strong>Variable Studio</strong> that several part studios can share [2]. The walkthrough below builds a simpler case for the same board in Fusion. It does not need to match the Onshape one; the steps matter more than the shape.</div>

<div style="text-align:center;margin:16px 0;"><img src="../reference-files/images/enclosure-lid.png" alt="esp_watch enclosure (Onshape), lid with display window, button and switch openings" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch enclosure (Onshape), lid with display window, button and switch openings</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Decide the Design Intent First</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Before touching the software, decide the <strong>design intent</strong>: which dimensions drive the model and which follow. For an enclosure, the board drives everything:</div>

```text
DRIVERS (you set these)           FOLLOWERS (the model calculates these)
────────────────────────          ──────────────────────────────────────
pcb_w, pcb_l   board size   ──►   inner cavity = board + clearance
stack_h        board height ──►   cavity depth
wall           wall thickness ─►  outer size = cavity + 2 × wall
clearance      air gap      ──►   lid position, window positions
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Write these down before modelling. A model built without a clear intent can still be parametric, but its parameters will control the wrong things.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 1: Start a Design</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open Fusion and start a new design (<strong>File → New Design</strong>). Fusion saves designs to its cloud, inside a <strong>project</strong>; make one project for your product and keep every design in it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two settings to check once:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Units.</strong> In the browser, expand <strong>Document Settings → Units</strong> and make sure it reads <strong>mm</strong>.</li><li style="margin:6px 0;">​<strong>Timeline.</strong> If there is no timeline along the bottom of the window, right-click the top item in the browser and choose <strong>Capture Design History</strong>. Without it, Fusion does not record the features, and nothing in this unit works.</li></ul>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Area</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it is for</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Toolbar</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tabs along the top (stay on <strong>Solid</strong>), and the tools grouped into panels: <strong>Create</strong>, <strong>Modify</strong>, <strong>Construct</strong>, <strong>Inspect</strong></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Browser</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Left</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Everything in the design: document settings, origin planes, bodies, sketches. Rename bodies here.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Canvas</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Centre</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The model</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>ViewCube</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top right</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Click a face or corner to look from that direction</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Timeline</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bottom</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every feature, in the order it was made. Fusion replays it on every change.</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">To move round the model: scroll to zoom, hold the middle button to pan, and hold <strong>Shift</strong> with the middle button to orbit. Press <strong>S</strong> anywhere to open a search box and type a tool's name; it is the quickest way to find a tool you cannot see.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 2: Create the Parameters</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Parameters come first, so that every dimension you add later can use a name instead of a number.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open <strong>Modify → Change Parameters</strong>. Click the <strong>+</strong> beside <strong>User Parameters</strong>, and for each row enter a <strong>name</strong>, <strong>unit</strong>, <strong>expression</strong> and <strong>comment</strong> [3]. An expression can be a number, or a formula that uses other parameters. Names are case-sensitive and cannot contain spaces.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Here is the parameter set for a two-part case around a board:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Name</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Unit</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Expression</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Comment</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pcb\_w</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">37.8</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">board width</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pcb\_l</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">39</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">board length</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">stack\_h</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">14.044</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">height of the parts stack (E2 measures the full stack)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">clearance</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0.5</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">air gap between board and inner wall</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">wall</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1.5</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">side wall thickness</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">floor\_t</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1.5</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">base thickness</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">lid\_t</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1.5</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">lid thickness</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">corner\_r</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">outer corner radius</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">cavity\_w</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pcb\_w + 2 \* clearance</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">inner width</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">cavity\_l</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pcb\_l + 2 \* clearance</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">inner length</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">cavity\_h</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">stack\_h + 2 \* clearance</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">inner height</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">outer\_w</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">cavity\_w + 2 \* wall</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">outer width</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">outer\_l</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">cavity\_l + 2 \* wall</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">outer length</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">outer\_h</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">cavity\_h + floor\_t + lid\_t</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">total height</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The first three values are esp\_watch's recorded board: 37.8 × 39 mm, and 14.044 mm from the board to the top of the OLED. E2 measures the full stack, including the board and the MAX30102 underneath, and updates stack\_h. The wall, floor, lid, corner and clearance values are <strong>example values</strong> for teaching. E3 explains how to choose them for 3D printing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Only the first eight are ever typed in. The other six are formulas. That split is the design intent, written in a form the software can enforce.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: What the Parameters Produce</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 1: Cavity.</div>

```text
cavity_w = 37.8 + 2 × 0.5   = 38.8 mm
cavity_l = 39 + 2 × 0.5     = 40.0 mm
cavity_h = 14.044 + 2 × 0.5 = 15.044 mm
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 2: Outer size.</div>

```text
outer_w = 38.8 + 2 × 1.5     = 41.8 mm
outer_l = 40.0 + 2 × 1.5     = 43.0 mm
outer_h = 15.044 + 1.5 + 1.5 = 18.044 mm
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 3: Change a driver.</strong> The board grows to 40 mm wide. Change pcb\_w from 37.8 to 40, and nothing else:</div>

```text
cavity_w = 40 + 1   = 41.0 mm
outer_w  = 41 + 3   = 44.0 mm
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The outer height of about 18 mm matches the thickness budget from C0, which is a good sign that the model's structure matches the concept. And a 2.2 mm change to the board produced a 2.2 mm change to the case with one edit. If any feature fails to follow, it is using a typed number somewhere instead of a parameter.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 3: Start a Sketch on a Plane</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every 3D feature starts from a <strong>sketch</strong>: a 2D drawing on a plane or a face.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Choose <strong>Create → Create Sketch</strong>, then click the origin plane that lies flat. That is <strong>XY</strong> if Fusion's default modelling orientation (<strong>Preferences → General</strong>) is <strong>Z up</strong>, and <strong>XZ</strong> if it is <strong>Y up</strong>. The view turns to look straight down at the plane, and the toolbar changes to the sketch tools.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 4: Draw and Constrain the Outline</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A sketch has two kinds of rules that fix its shape:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Geometric constraints</strong>: relationships between lines and points. Horizontal, vertical, parallel, perpendicular, tangent, equal, coincident, concentric, midpoint, symmetric.</li><li style="margin:6px 0;">​<strong>Dimensions</strong>: sizes and distances, such as "this line is 42 mm".</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A sketch is <strong>fully constrained</strong> when every line and point has exactly one possible position. In Fusion, geometry that can still move is shown in <strong>blue</strong>, and fully constrained geometry turns <strong>black</strong>, so you can see at a glance what is still free.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Why does it matter? An under-constrained sketch can change shape unexpectedly when you edit something nearby, and every feature built on it changes too. A fully constrained sketch changes only when you change one of its dimensions.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A common habit is to draw shapes roughly and add dimensions until they look right. That produces sketches held in place by accident. Work the other way round: <strong>constraints first</strong>, so the sketch has the right shape, then <strong>dimensions</strong>, so it has the right size. Adding a rule that conflicts with an existing one <strong>over-constrains</strong> the sketch, and Fusion refuses to apply it.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Do it:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Create → Rectangle → Center Rectangle.</strong> Click the origin, then click anywhere to place a corner. Fusion adds horizontal and vertical constraints to the sides, and the centre sits on the origin, so the case will grow evenly in every direction.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Sketch Dimension (D).</strong> Click the top side, place the dimension, and type outer\_w instead of a number. Do the same for a vertical side with outer\_l.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Check the colour.</strong> Every line should now be black. If one is still blue, something can move: find it by dragging it, and add the missing constraint or dimension.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Click <strong>Finish Sketch</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A dimension driven by a parameter shows <strong>fx:</strong> before its value. That is how you spot a typed number later: it has no <strong>fx:</strong>.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Break it and fix it.</div><div>Finish Steps 4 and 5 first, so you have a block.</div><div>1. <strong>Predict.</strong> If you change wall from 1.5 to 2.0, what will the block's width become?</div><div>2. <strong>Do.</strong> Change it, and check the width with <strong>Inspect → Measure (I)</strong>. Then edit the sketch, replace the outer\_w dimension with the plain number 42, and change wall again.</div><div>3. <strong>Explain.</strong> Which direction followed the change and which did not? How would you find a typed number hiding in a large model? (Hint: the <strong>Model Parameters</strong> section of Change Parameters lists every dimension in the design.)</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 5: Extrude the Block (E)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Create → Extrude</strong> (<strong>E</strong>). Click inside the rectangle to select the profile. Set <strong>Distance</strong> to outer\_h, <strong>Direction</strong> to one side, and <strong>Operation</strong> to <strong>New Body</strong>. Click <strong>OK</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The result is a solid block the size of the finished case. A body appears in the browser under <strong>Bodies</strong>.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 6: Round the Corners (F)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Modify → Fillet</strong> (<strong>F</strong>). Select the <strong>four vertical edges</strong> of the block and set the radius to corner\_r.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Fillet <strong>before</strong> shelling. The shell in Step 7 then follows the rounded outside, so the inner corners are rounded too and the wall stays the same thickness all the way round. Fillet before splitting, too: one fillet on one body gives the base and the lid exactly matching corners.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 7: Hollow It Out (Shell)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Modify → Shell.</strong> Instead of picking a face, select the <strong>body</strong> (click it in the browser), so that no face is removed. Set <strong>Inside Thickness</strong> to wall and <strong>Direction</strong> to <strong>Inside</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The block becomes a closed hollow box with walls all round. Closing it completely now, and splitting it in Step 8, keeps the base and lid walls consistent.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Assumption.</div><div>Shell uses one thickness everywhere, so floor\_t and lid\_t should equal wall here. If you want them different, extrude a block and cut a cavity sketch instead of using Shell. The parameter table already has separate values ready.</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 8: Split Into Base and Lid</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Construct → Offset Plane.</strong> Select the bottom face of the box and set the distance to outer\_h - lid\_t. A plane appears just below the top.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Modify → Split Body.</strong> <strong>Body to Split</strong>: the box. <strong>Splitting Tool</strong>: the new plane. Click <strong>OK</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. In the browser, double-click each new body and rename it: base and lid.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The lid is now a flat plate sitting on the base's walls. A real case also needs a lip to locate the lid and a way to hold it shut; E3 adds those.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 9: Cut the Openings</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Create Sketch</strong> on the lid's top face.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Draw the display window (a centre rectangle) and the button holes (<strong>Create → Circle</strong>). Dimension every position <strong>from the origin</strong>, not from the lid's edge: the origin never moves, but edges can.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Finish Sketch</strong>, then <strong>Extrude</strong> each profile downwards with <strong>Operation: Cut</strong>. Under <strong>Objects To Cut</strong>, leave only lid ticked, so the cut cannot reach the base.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's lid has four openings: the display window, two buttons and the slide switch. Its case also needs openings this simple model does not have: the XIAO's USB-C port on the side, and a way for the heart-rate sensor on the underside to reach the wrist. Both belong to E2 and E4, where the real board model is placed inside the case.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 10: Read the Timeline</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Fusion records every feature in the <strong>timeline</strong> at the bottom of the window, in the order you made them. When you change a parameter, Fusion replays the timeline from the start, rebuilding each feature from the ones before it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">That makes order a design decision. Two rules keep the timeline robust:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Big shapes first, details last.</strong> Block, corner fillets, shell, split, then openings. A feature that refers to an edge a later feature removes will fail when the model rebuilds.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Reference stable things.</strong> Sketch on the origin planes or on faces that will always exist, and dimension from the origin rather than from an edge that a fillet might round away.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">When a change breaks a feature, Fusion colours it in the timeline, usually because an edge or face it referred to no longer exists. Double-click the feature, see which selection is missing, and re-select the new edge or face. Fixing the <strong>reference</strong>, not the dimension, is almost always the answer.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Use <strong>Inspect → Measure (I)</strong> on the base's inside: it should equal cavity\_w by cavity\_l.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 11: Test It by Changing It</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A parametric model that has never been changed is only presumed to be parametric. Open <strong>Change Parameters</strong>, set pcb\_w to 44, and close the dialog. Every step should rebuild: base and lid both widen, the openings stay centred, and the fillets remain. Set it back, then do the same with wall.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Order matters.</div><div>In your timeline, drag the fillet feature (Step 6) to after the split (Step 8).</div><div>1. <strong>Predict.</strong> Will the model still rebuild? Will the lid and base corners still match? Will the inner corners still be rounded?</div><div>2. <strong>Do.</strong> Move it, and change pcb\_w. Look for warnings in the timeline.</div><div>3. <strong>Explain.</strong> What does the fillet now refer to? Why did "big shapes first, details last" matter?</div><div>​<strong>Extra challenge:</strong> Add a window\_w parameter for the display window, set as a formula from pcb\_w. When the board grows, should the window grow too? Write down your design intent before deciding.</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 12: Save and Export</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Fusion keeps the design in its cloud project. For your design pack you also need copies on your own disk:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>File → Export</strong>, type <strong>Fusion Archive (.f3d)</strong>: the full model with its timeline and parameters, which anyone with Fusion can open and edit.</li><li style="margin:6px 0;">​<strong>File → Export</strong>, type <strong>STEP</strong>: the solid shapes only, readable by any CAD tool, including Onshape.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Commit both to your design pack's Git repository each time the case changes, with a message saying what changed, for example "case: wall 1.5 → 2.0 mm". <a href="../01-system-architecture/REF-version-control.md">Version Control for a Hardware Project</a> shows how.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Tool Reference</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Tool</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Key</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Use it to</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Search for a tool</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Anywhere</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">S</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Find any tool by typing its name</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Change Parameters</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modify</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Add user parameters and formulas; list every model dimension</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Create Sketch</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Create</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Start a 2D sketch on a plane or face</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Center Rectangle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sketch: Create → Rectangle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Draw a rectangle centred on a point</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sketch Dimension</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sketch: Create</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">D</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Size and position sketch geometry</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Extrude</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Create</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">E</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Make a solid from a profile, or cut one away</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fillet</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modify</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">F</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Round edges</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shell</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modify</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hollow a body to a set wall thickness</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Offset Plane</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Construct</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Make a plane at a set distance from a face or plane</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Split Body</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modify</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cut one body into two</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Measure</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Inspect</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">I</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check a size or gap</td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Parametric Discipline</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The tools matter less than the habits. Keep these three:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Every dimension is a parameter or a formula.</strong> A typed number is a future bug.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Drivers are few and named clearly.</strong> pcb\_w, not d1. Add a comment to every parameter saying what it is and where its value comes from.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Test the model by changing it.</strong> Before calling a model finished, change each driver by a meaningful amount and check that everything follows.</div>

---

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:center;line-height:1.7;"><div style="font-weight:700;color:#1e40af;">This cookbook will be continued in Part 2.</div></div>
