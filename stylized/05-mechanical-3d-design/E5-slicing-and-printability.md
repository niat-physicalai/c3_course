<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">E5 — Slicing and Printability Validation</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Checking the Print Before Anyone Prints It</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 5 — Mechanical and 3D Design <strong>Time:</strong> ~30 minutes · <strong>You will produce:</strong> a sliced file, a preview screenshot and a time and material estimate</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Slicer Is the Last Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>slicer</strong> turns a 3D model into the instructions a printer follows: every layer, every line, every move. It is also the last free check before plastic is used. Its <strong>preview</strong> shows exactly what the printer will do, where supports will go, which areas will struggle, and how long and how much material the print will take. You will not print in this course, but you will stop at exactly the point where a printer would start, with a file ready to send and a cost you can defend.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Set</strong> layer height, walls, infill and supports for an enclosure.</li><li style="margin:6px 0;">​<strong>Choose</strong> a print orientation in the slicer and check it against E3's decisions.</li><li style="margin:6px 0;">​<strong>Read</strong> the slicer preview to find overhangs, thin walls and first-layer risks.</li><li style="margin:6px 0;">​<strong>Estimate</strong> print time and material cost from the slicer's output.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Choosing a Slicer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Any common slicer works: Cura, PrusaSlicer or Bambu Studio. PrusaSlicer is free and open source, and works with any FDM printer [1]. Pick the printer profile closest to the printer or print service you expect to use. If you do not know, choose a common 0.4 mm-nozzle printer, and say so.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Export each part from Fusion as a separate file: in the browser, right-click the base body, choose <strong>Save As Mesh</strong>, pick <strong>3MF</strong> (or STL) and save. Do the same for the lid. Then load both into the slicer.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Settings That Matter</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Setting</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it controls</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Starting point for a small case (example values)</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Layer height</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Smoothness against time</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0.2 mm; 0.12–0.16 mm for a finer surface</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Walls (perimeters)</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Strength and wall accuracy</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Match your E3 decision, e.g. 3 or 4</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Top and bottom layers</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Solid skin on flat faces</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Enough for about 0.8–1 mm of solid skin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Infill</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Strength inside solid regions</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">15–20% for a case; more for lugs</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Supports</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Material under overhangs</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Only from the build plate" if possible</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Brim</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Extra first-layer grip</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">On, if corners lift (E3's warping)</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The most useful thing to know about a small case is that <strong>most of it is walls</strong>. A 1.35–1.8 mm wall is three or four perimeters with no infill at all, so infill matters mainly in thick features such as lugs and bosses.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Orientation and Supports</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Set each part in the orientation you chose in E3: the base floor-down, open side up; the lid outer face down. Then generate supports and look at where they appear.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Supports inside the base or under the lid's openings are a design signal</strong>, not just a slicer setting. Each one leaves a rough surface where it is removed. Go back to E3's fixes: chamfer or arch the top of a side opening, shorten a bridge, or rotate the part.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Embedding Magnets or Nuts: Pause at a Layer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">If E3 put a magnet or a nut inside a closed pocket, the printer has to stop so you can drop it in. PrusaSlicer, Cura and Bambu Studio can all insert a <strong>pause</strong> at a chosen layer. Find the first layer that would cover the pocket in the preview, add the pause just before it, and the printer will stop, wait for you to place the part, then print over it. Make sure the part sits flush with or below the top of its pocket, or the nozzle will hit it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Reading the Preview</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Step through the preview layer by layer. Look for five things:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Look for</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it means</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Fix</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Supports in unexpected places</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">An overhang you did not notice</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reshape in CAD (E3)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Walls shown as a single thin line, or gaps</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A wall thinner than two perimeters</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Thicken to a whole number of perimeters</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tiny isolated islands on a layer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Small features that may not stick</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Enlarge, or merge with nearby geometry</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Long travel moves or bridges over openings</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Stringing or sagging risk</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shorten spans; reorient</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Assembly faces sitting on the bed</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Elephant's foot will flare them (the preview does not show it)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Add a bed-edge chamfer (E3), or turn on the slicer's elephant's-foot compensation</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Time and Material Cost</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The slicer reports an estimated print time and the filament used, in grams. Turn those into a cost.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;background:#fef2f2;border-left:4px solid #dc2626;border-radius:6px;padding:8px 14px;color:#991b1b;">​<strong>Assumption:</strong> the slicer estimates a base of 9 g and a lid of 4 g, taking 1 h 10 min and 35 min. These are <strong>example values</strong> for a case of about 42 × 43 × 18 mm; use your own slicer's numbers.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 1: Material.</strong> PLA filament listed at ₹649 per 1 kg spool, including GST, at Robu on 25 September 2026 [2].</div>

```text
Filament used  = 9 g + 4 g              = 13 g
Price per gram = ₹649 ÷ 1,000 g         = ₹0.649 per g
Material cost  = 13 g × ₹0.649          = ₹8.44
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: Allow for waste.</strong> Add supports, a brim and a failed first attempt. <strong>Assumption:</strong> 30% extra.</div>

```text
13 g × 1.3 = 16.9 g → about ₹11
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 3: Time.</div>

```text
1 h 10 min + 35 min = 1 h 45 min of printer time per case
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The material is almost free: about ₹11. The printer's <strong>time</strong> is the real cost, because it limits how many cases one printer can make in a day, about 13 at 1 h 45 min each if it ran around the clock. That is exactly why the numbers change completely at volume, and why F2 includes time and a printing service's quote rather than filament alone.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's enclosure will be printed in black PLA but has not been sliced yet. When it is, its real printer settings, print time and filament use replace the example values above.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Find the cheapest change.</div><div>Slice your own base.</div><div>1. <strong>Predict.</strong> Which setting will cut the print time the most: layer height, infill or walls?</div><div>2. <strong>Do.</strong> Change each one at a time (0.2 to 0.28 mm layers; 20% to 10% infill; 4 to 3 walls) and note the time each time.</div><div>3. <strong>Explain.</strong> Which saved the most? Which change would you accept for a wearable case, and which would you not?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Slice both parts</strong> with a named printer profile and the settings from your E3 decisions.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Read the preview</strong> layer by layer, and fix in CAD anything that needs support you did not intend.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Record the estimate:</strong> time and grams for each part, and a material cost with a waste allowance.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> the sliced file (G-code or 3MF project), a screenshot of the preview with the estimate panel visible, and your time and cost calculation, saved in your design pack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Both parts are sliced with a named printer profile and nozzle size. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. The walls setting matches your E3 wall decision. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Each part is oriented as decided in E3. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every support in the preview is either intended or has been removed by a CAD change. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The preview shows no walls thinner than two perimeters. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Time and grams are recorded for each part. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. The material cost includes a stated waste allowance and a dated filament price. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> The slicer adds supports under the top edge of the USB-C opening in the base. What is the best response?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Accept them; supports are normal.</li><li style="margin:6px 0;">B. Reshape the top of the opening in CAD, for example as a 45° chamfer or arch, so it prints without support.</li><li style="margin:6px 0;">C. Increase infill.</li><li style="margin:6px 0;">D. Print the base upside down.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A small design change removes the need for support and gives a cleaner opening. <strong>A</strong> leaves rough marks on a visible, functional opening. <strong>C</strong> does not affect overhangs. <strong>D</strong> would put the open side on the bed and create far more overhangs.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A slicer estimates 13 g of PLA at ₹649 per kg. What is the material cost, before waste?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. About ₹0.65</li><li style="margin:6px 0;">B. About ₹8.40</li><li style="margin:6px 0;">C. About ₹84</li><li style="margin:6px 0;">D. About ₹649</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> 13 g × ₹0.649 per g ≈ ₹8.44. <strong>A</strong> is the price of a single gram. <strong>C</strong> is ten times too large. <strong>D</strong> is the price of the whole spool.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> For a small printed case with 1.8 mm walls, why does changing infill from 20% to 10% barely change the print time?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Infill does not affect time.</li><li style="margin:6px 0;">B. Most of a thin-walled case is perimeters, so there is little space for infill to fill.</li><li style="margin:6px 0;">C. The slicer ignores infill below 20%.</li><li style="margin:6px 0;">D. PLA cannot be printed at 10%.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A 1.8 mm wall is four solid perimeters; infill only appears in thicker regions. <strong>A</strong> is false in general. <strong>C</strong> and <strong>D</strong> are false.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A club wants 30 cases in two days from one printer. Each takes 1 h 45 min and about ₹11 of filament. What stops them?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The filament cost</li><li style="margin:6px 0;">B. The printer's time</li><li style="margin:6px 0;">C. The 30% waste allowance</li><li style="margin:6px 0;">D. The size of the STL file</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> 30 × 1 h 45 min = 52.5 h, more than the 48 h available. <strong>A</strong> is about ₹330 in total. <strong>C</strong> adds grams, not hours. <strong>D</strong> has no effect on printing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> Your base has two disc magnets that must be sealed inside the wall, 1 mm below the top face. How do you get them in?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Glue them to the outside after printing.</li><li style="margin:6px 0;">B. In the slicer, add a pause just before the first layer that covers the magnet pocket, drop the magnets in when the printer stops, then let it print over them.</li><li style="margin:6px 0;">C. Print the pocket bigger and push them in later.</li><li style="margin:6px 0;">D. Magnets cannot be used in printed parts.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Pausing just before the pocket is covered lets the printer seal the magnets inside (E3). Pause any earlier and the nozzle hits them. <strong>A</strong> leaves them exposed. <strong>C</strong> can work for an open pocket, but not one sealed under 1 mm of plastic. <strong>D</strong> is false.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This completes the mechanical module. Module 6 turns to buying parts and preparing the files a factory needs, starting with <a href="../06-sourcing-and-manufacturing/F0-sourcing-and-lifecycle.md">F0 — Sourcing and the Lifecycle Trap</a>.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Prusa Research. PrusaSlicer ("Free, open-source slicer... Works with any FDM or resin printer"). https://www.prusa3d.com/p/prusaslicer/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Robu.in. Pro-Range PLA Filament 1.75 mm 1 kg Spool, Black, listing checked 25 September 2026 (₹649 incl. GST). https://robu.in/product/pro-range-pla-filament-1-75mm-1-kg-spool-black/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>supplier listing for the part you are actually using.</div></div>
