<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">E1 — Materials, Colour and Rendering</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Choosing What the Case Is Made Of, What It Looks Like, and How You Show It</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 5 — Mechanical and 3D Design <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a material choice justified against your A0 spec, and one presentation image of your coloured enclosure</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Case That Sagged in the Car</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A student prints a watch case in PLA, because PLA is what the lab printer had loaded. It fits, and it survives a week of wear. Then the owner leaves it on the dashboard of a parked car on a May afternoon. By evening the lid has slumped and the interference fit has gone loose.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Nothing in the CAD model was wrong. The material was never chosen; it came with the spool on the printer. Your E0 model now has a shape. This unit decides what plastic it is printed in, what colour and finish it has, and how you show it in one image to someone who has never seen your project.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Compare</strong> PLA, PETG, ABS and TPU on stiffness, layer adhesion, heat tolerance and printability.</li><li style="margin:6px 0;">​<strong>Select</strong> an enclosure material by testing each candidate against your A0 requirements, and <strong>justify</strong> the choice in writing.</li><li style="margin:6px 0;">​<strong>Choose</strong> a colour and finish for stated reasons: visibility, how it photographs, and what it shows about the print.</li><li style="margin:6px 0;">​<strong>Produce</strong> a presentation image of the coloured model in Fusion, with a deliberate camera angle, and know when a render is worth making.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Four Filaments, Four Questions</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Filament listings call almost everything "strong" and "easy to print". Ask four questions instead:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Stiffness.</strong> Does the case keep its shape when the lid is pressed on and the strap pulls on a lug?</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Layer adhesion.</strong> An FDM part is weakest between layers (E3). How well do this material's layers bond, and how does it break?</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Heat tolerance.</strong> When does it start to soften? A wrist is only at body temperature, but a watch is also left in the sun and in cars.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Printability.</strong> Can your printer, or the print service you will use, print it without special equipment?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The table follows Prusa's material guides [1][2][3][4].</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;"></th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">PLA</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">PETG</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">ABS</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">TPU</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Stiffness</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Stiff, but brittle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tough; bends a little before breaking</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tough</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Flexible, rubber-like</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Layer adhesion</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Weaker than the others; breaks along layers or into shards</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Very good</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Good</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Very good</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Heat tolerance</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Softens and deforms above about 60 °C [1]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Suitable below about 80 °C [2]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Good high-temperature resistance [3]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Not a concern at wrist temperature</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Printability</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Easiest; little warping</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Easy; strings, and bridges and overhangs are poor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hard: warps, needs an enclosed printer, gives off styrene fumes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hard: slow (about 20 mm/s), clogs, tangles in the extruder</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Typical wearable use</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Prototypes, fit checks</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cases</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cases, with an enclosed printer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Straps, button covers, gaskets</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>PLA's heat limit is lower than it sounds.</strong> No wrist reaches 60 °C, but a car parked in the sun does inside, and its dashboard gets hotter still.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>TPU is too flexible for a case</strong>, but right for the parts that bend: a strap, a button cover, a gasket.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>These are generic descriptions. Brands and additives differ, so for a real product read the technical data sheet (TDS) of the exact filament you will buy.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Skin contact.</strong> No filament is automatically "skin-safe" as printed. If your case touches skin, record what that filament's data sheet says, and claim nothing more.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Cost barely decides it.</strong> A watch case uses about 13 g of filament, around ₹11 of PLA (E5); other materials change that by a few rupees.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Choosing the Case Material Against the Spec</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Eliminate first, then rank.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: List the requirements the material affects.</strong> From an example A0 spec:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">ID</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Requirement (example values)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it asks of the material</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-08</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The case shall not deform after 1 h in a parked car in summer. Check: analysis against the data sheet.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heat tolerance above the car's temperature</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-09</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The lid shall stay on through 200 removals. Check: test after build.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Stiff enough to hold an interference fit, tough enough not to crack</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-10</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The case shall be printable on the college lab's open-frame printer. Check: inspection.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No enclosure needed</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-11</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The heart-rate sensor shall read the wrist with outside light blocked. Check: test after build.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Opaque base (E4)</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 2: Eliminate on hard limits.</div>

```text
Candidate   NFR-08 heat    NFR-10 open printer   NFR-09 lid fit         Result
─────────   ───────────    ───────────────────   ────────────────────   ──────────────
PLA         ✗ ~60 °C       ✓                     ✗ brittle, may crack   out
PETG        ? ~80 °C       ✓                     ✓ tough                keep
ABS         ✓              ✗ needs enclosure     ✓                      out (this lab)
TPU         —              ✓                     ✗ too flexible         out (as case)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Resolve the "?".</strong> About 80 °C is above a hot car's air but below a sunlit dashboard. So PETG passes NFR-08 if the watch is left in the car and fails if it is left on the dashboard, and the requirement does not say which. Either tighten the wording, or accept that the only candidate meeting the harsher version is ABS, which fails NFR-10.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 4: Write the decision.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>Material: PETG for the case and lid, TPU for the strap. PLA is rejected because it softens at about 60 °C (NFR-08) and is brittle under the interference fit (NFR-09). ABS is rejected because the lab printer is open-frame (NFR-10). NFR-08 is reworded to "inside a parked car, out of direct sun", since nothing that meets NFR-10 survives a sunlit dashboard. Base in black PETG to block light (FR-11).</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Every rejection names the requirement it failed, and the requirement no candidate met was changed in writing, as in the C0 concept decision.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's enclosure will be printed in <strong>black PLA</strong>. PLA is stiff, cheap and easy to print, and black is opaque, which helps keep outside light away from the heart-rate sensor. Its weak points for a wearable are heat (a watch left in a hot car) and brittleness, which matters for the <strong>interference-fit lid</strong> that is pressed on and off. Both are worth testing on the first print.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Colour and Finish Are Design Decisions</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Can it be seen?</strong> A bright case stands out on a wrist, which the wearer may or may not want. A dark bezel makes an OLED look sharper, because the screen's black background blends into it. A dark case in the sun also runs hotter.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>How does it photograph?</strong> Pure black loses its edges; pure white overexposes and shows every layer line. Mid-tones such as grey show the shape best.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">What does the finish show about the print?</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Finish</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Effect on a printed part</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Matte</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hides layer lines; looks less like a print</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Glossy or "silk"</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Catches light on every layer line, making them more visible</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Translucent</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shows the infill, internal walls and anything inside, and lets light through</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On the sensor side of a wearable, letting light through is a fault: E4 explains why that base must be opaque.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Making the Presentation Image</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The Design Pack needs one image of the enclosure on its first page, answering at a glance: what is it, which way up is it worn, and how big is it? A <strong>screenshot of the coloured model</strong>, taken in Fusion's Design workspace, is enough for that. A <strong>render</strong>, a photograph-like image Fusion calculates from the model, lighting and camera, is only worth the extra time when you need a good-looking image, for a pitch or a poster.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Appearance is not material</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Fusion keeps two settings on each body [5]. A <strong>physical material</strong> sets engineering properties such as density, which Fusion uses to calculate mass. An <strong>appearance</strong> changes only how the body looks and overrides the material's colour. Set both, so Inspect, Properties gives a realistic mass for your C0 weight constraint.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The coloured screenshot, in five steps</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">All of this happens in the Design workspace, where you built the case in E0.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Set the physical material.</strong> <strong>Modify → Physical Material</strong>, and drag a plastic (for example ABS or a generic plastic close to your choice) onto each body.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Set the appearance.</strong> <strong>Modify → Appearance</strong> (<strong>A</strong>), and drag a plastic in your chosen colour onto each body [7]. Use a second appearance for anything visibly different, such as a TPU strap.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Tidy the view.</strong> In the browser, click the eye (or light bulb) icon to hide sketches, construction planes and the origin. In the navigation bar, open <strong>Display Settings</strong>: set <strong>Visual Style</strong> to <strong>Shaded</strong>, choose a plain light <strong>Environment</strong>, and set <strong>Camera</strong> to <strong>Orthographic</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Frame the view</strong> as described below, and save it as a named view so you can return to it after changes.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Capture.</strong> <strong>File → Capture Image</strong>, choose a size, and save it as E1-image.png.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">An <strong>orthographic</strong> camera has no perspective at all, so the case's thickness looks exactly as it is. That is the honest choice for a design image.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Camera angle</div>

```text
   side view                                  top view

   camera ●                                   ┌──────────┐
           ╲  ~30° above the table            │  watch   │
            ╲     ┌──────────┐                └──────────┘
             ╲──► │  watch   │                           ╲
   ────────────── └──────────┘ ── ground                  ● camera, turned 30–45°
                                                            so a corner faces it
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>three-quarter view</strong>, looking down at about 30° with a corner towards the camera, shows the display, the buttons, the thickness and a side opening in one image. Straight-on views hide the thickness or the display.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Show the scale.</strong> A simple strap, or a wrist-sized cylinder beneath the watch, tells the reader the size at once.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">When You Need a Render</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For a pitch or a poster, a render looks more like a product photograph: soft shadows, reflections, a studio background. Use the <strong>Render</strong> workspace [6]:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Switch</strong> the workspace from Design to <strong>Render</strong>. The appearances you set carry over.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Set the scene</strong> in <strong>Setup → Scene Settings</strong> [8]: a studio environment, a light grey Solid Color background, Ground Plane on so the watch casts a shadow, Reflections off, and a Perspective camera.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Frame the camera</strong> with the same three-quarter view.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Render.</strong> Turn on <strong>In-canvas render</strong> and use <strong>Capture Image</strong>; its size is fixed by your screen [9]. For a set resolution, use the <strong>Render</strong> command with the local renderer. The cloud renderer uses tokens [9], and you do not need it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Use a longer focal length.</strong> A render uses a perspective camera. A short, wide-angle lens close to a small object exaggerates perspective, so the nearest corner bloats and a thin watch looks like a brick. A longer lens, around 90 mm as in the Fusion tutorial [6], with the camera further back, removes this.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Lens test.</div><div>Only if you make a render. Set up the three-quarter view of your enclosure in the Render workspace.</div><div>1. <strong>Predict.</strong> How will the case's thickness look at a 20 mm focal length compared with 90 mm?</div><div>2. <strong>Do.</strong> Capture the in-canvas render at both, moving the camera back at 90 mm to fill the frame.</div><div>3. <strong>Explain.</strong> Which looks more like the watch held in your hand? Which is more honest about thickness?</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">An honest image</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A screenshot or render shows a finish your printer cannot make: no layer lines, a smooth coat. Say so in the caption, for example "PETG case design in Fusion; the printed part will show layer lines", so a reviewer who later sees the print is not misled.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's enclosure was modelled in Onshape (E0), and its enclosure images are placeholders for now. The camera and caption rules above apply in any CAD tool.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Decide.</strong> List every A0 requirement the case material affects. If none is about temperature, add one with a check method. Run the elimination table for your product and write the decision as in the worked example.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Present.</strong> Write one reason each for your colour and finish. Set the physical material and appearances in Fusion, then capture one presentation image of the coloured model with an honest caption. Render it only if you need a polished image.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> E1-material.md in your Design Pack, with the elimination table, the written decision and the colour and finish reasons; plus E1-image.png with its caption.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open E1-material.md and E1-image.png and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every requirement in the elimination table has an A0 ID. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. The spec contains a temperature requirement with a check method. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every rejected material names the requirement it failed. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Any requirement no candidate met is reworded in A0, with the reason written. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The colour and the finish each have a written reason. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. If the case touches skin, the file states what the filament's data sheet says. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. The image is a three-quarter view showing the display face, at least one side and something that shows scale. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The caption says it is a CAD image and how the printed part will differ. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A case must hold an interference-fit lid that the user removes to change the battery. The team chooses PLA because it is the stiffest. What is the main risk?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. PLA is too flexible to hold the lid.</li><li style="margin:6px 0;">B. PLA is brittle, so repeatedly pressing the lid on and off can crack it, often along a layer.</li><li style="margin:6px 0;">C. PLA cannot be printed on an open-frame printer.</li><li style="margin:6px 0;">D. PLA costs much more than PETG.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Stiffness is not toughness. PLA is stiff but brittle, with weaker layer adhesion, so a repeatedly strained fit is where it fails. <strong>A</strong> describes TPU, not PLA. <strong>C</strong> is wrong: PLA is the easiest material on an open printer. <strong>D</strong> is wrong: a case's filament costs a few rupees in any of these.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A spec says "The case shall survive being left in a parked car." PETG is suitable below about 80 °C. What is the best next step?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Choose PETG, because 80 °C is far above body temperature.</li><li style="margin:6px 0;">B. Choose TPU, because it does not soften at wrist temperature.</li><li style="margin:6px 0;">C. Make the requirement say whether the watch is inside the car or on a sunlit dashboard, because PETG's answer depends on which.</li><li style="margin:6px 0;">D. Drop the requirement, since nobody will test a student project in a car.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Cabin air and a sunlit dashboard are very different temperatures, and PETG sits between them. <strong>A</strong> compares against the wrong condition. <strong>B</strong> confuses flexibility with heat resistance, and TPU cannot hold a case's shape. <strong>D</strong> removes a real use condition instead of making it checkable.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> The base under an optical heart-rate sensor is printed in translucent white PETG because it "looks technical". What is the likely effect?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. None, because the sensor has its own light source.</li><li style="margin:6px 0;">B. Outside light passes through the plastic around the sensor and adds noise to its signal.</li><li style="margin:6px 0;">C. The base will warp more than an opaque one.</li><li style="margin:6px 0;">D. The render will take longer.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Light through the base reaches the photodiode, which is what E4's opaque-rim rule prevents. <strong>A</strong> is wrong: the sensor's own light is the signal and extra light is noise. <strong>C</strong> is not a property of colour. <strong>D</strong> is irrelevant to whether the product works.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A render (perspective camera) of a 42 mm watch looks chunky, with the nearest corner far larger than the others. What is the most likely cause?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The appearance is glossy.</li><li style="margin:6px 0;">B. The ground plane is on.</li><li style="margin:6px 0;">C. A short, wide-angle focal length with the camera close to the object.</li><li style="margin:6px 0;">D. The physical material is set wrongly.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> A wide lens close to a small object exaggerates perspective; a longer lens further back removes it, and an orthographic screenshot has no perspective at all. <strong>A</strong> and <strong>B</strong> change reflections and shadows, not proportions. <strong>D</strong> affects mass, not the image.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A student sets a red appearance on the case but leaves the physical material as steel. What goes wrong?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The model shows steel instead of red.</li><li style="margin:6px 0;">B. The case looks right, but Inspect, Properties reports a mass several times too high, so the weight check is wrong.</li><li style="margin:6px 0;">C. Nothing, because appearance and physical material are the same setting.</li><li style="margin:6px 0;">D. The Appearance dialog will not open.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The appearance overrides only the look; mass comes from the physical material, and steel is far denser than any printed plastic. <strong>A</strong> is wrong because the appearance does override the colour. <strong>C</strong> is wrong: Fusion keeps them separate. <strong>D</strong> is not a real effect.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="E2-pcb-enclosure-co-design.md">E2 — PCB ↔ Enclosure Co-Design</a> you will bring the real board model into the case and check that everything fits.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Prusa Research. PLA, Prusa Knowledge Base. https://help.prusa3d.com/article/pla\_2062</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Prusa Research. PETG, Prusa Knowledge Base. https://help.prusa3d.com/article/petg\_2059</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Prusa Research. ABS, Prusa Knowledge Base. https://help.prusa3d.com/article/abs\_2058</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Prusa Research. Flexible materials, Prusa Knowledge Base. https://help.prusa3d.com/article/flexible-materials\_2057</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Autodesk. Physical materials and appearances, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/GUID-55EC2C42-60E1-48C7-B802-D2AA7AB6F0CB.htm</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Autodesk. Tutorial: Rendering a design, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Render/files/GUID-834C5728-53CA-41BA-AF07-2DC992A568AD.htm</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Autodesk. Apply appearances to components, bodies, and faces in a design, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/GUID-D59206EC-875D-4890-8088-AD23E5364951.htm</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Autodesk. Set the lighting, background, and camera in your render, Fusion Help. https://help.autodesk.com/view/fusion360/ENU/?contextId=RND-SCENE-SETTINGS</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. Autodesk. Rendering in the cloud and locally, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Render/files/RND-RENDER-CLOUD-LOCAL.htm</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
