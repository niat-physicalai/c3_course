<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">F1 — The PCB Manufacturing Package</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What a Fab House Needs, and What Every File in the Zip Is For</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 6 — Sourcing and Manufacturing Handoff <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a complete fabrication zip, and a file-by-file annotation of its contents</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A One-Click Export You Cannot Explain Is a Liability</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A fabricator never sees your KiCad project. It makes exactly what your zip of manufacturing files describes. A missing file can mean a missing layer. A wrong file means a wrong board.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A KiCad plugin can export the zip in one click, and the reference watch's board was exported that way. But when a board comes back with a missing slot, a mirrored silkscreen or a part rotated the wrong way, "I clicked export" is not a diagnosis. So in this unit you open your own zip and account for every file in it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>List</strong> the files a fabricator needs, and <strong>explain</strong> what each one controls.</li><li style="margin:6px 0;">​<strong>Read</strong> the header of a Gerber and a drill file, and identify the layer and units.</li><li style="margin:6px 0;">​<strong>Name</strong> the extra files an assembler needs, and when you need them.</li><li style="margin:6px 0;">​<strong>Generate</strong> a fabrication zip from your own board, and <strong>annotate</strong> every file in it.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Two Jobs, Two Sets of Files</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">There are two separate jobs, often done by the same company:</div>

```text
FABRICATION: making the bare board         ASSEMBLY: putting parts on it
────────────────────────────────           ─────────────────────────────
Gerber files (one per layer)               BOM (which part goes where)
Drill files (every hole)                   CPL / pick-and-place (position, rotation, side)
Stackup and fab notes                      Assembly drawing
Board outline and dimensions               (plus the fabrication files)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's board was soldered <strong>by hand</strong>. Its parts are through-hole, plus a few larger surface-mount parts that can be soldered with an iron. So its order needed only the fabrication files.</div>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/Assembled/Top_assembled.png" alt="The assembled esp_watch board, top side, running its firmware" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The assembled esp\_watch board, top side, running its firmware</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Fabrication Files</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Gerber Files: One Picture per Layer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>Gerber file</strong> describes one layer of the board as a precise 2D drawing: where copper is, where solder mask is removed, where silkscreen ink goes, where the board edge is. The format is maintained by Ucamco, and its modern version, <strong>Gerber X2</strong>, adds attributes that say what each file is [1].</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is the start of a real top-copper Gerber, exported from one of KiCad's demo boards with KiCad 10:</div>

```text
%TF.GenerationSoftware,KiCad,Pcbnew,10.0.6-10.0.6~ubuntu26.04.1*%
%TF.FileFunction,Copper,L1,Top*%
%TF.FilePolarity,Positive*%
%FSLAX46Y46*%
G04 Gerber Fmt 4.6, Leading zero omitted, Abs format (unit mm)*
%MOMM*%
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Read it line by line:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">TF.FileFunction,Copper,L1,Top is an <strong>X2 attribute</strong>: this file is copper layer 1, the top. The fabricator does not have to guess from the file name.</li><li style="margin:6px 0;">FSLAX46Y46 sets the number format: coordinates with 4 whole digits and 6 decimal places.</li><li style="margin:6px 0;">MOMM means the units are <strong>millimetres</strong>.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every board needs at least these layers, one file each:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Layer</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Typical file extension (KiCad default)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it controls</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top copper</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.gtl</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tracks, pads and pours on the top</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bottom copper</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.gbl</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The same, underneath</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top / bottom solder mask</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.gts / .gbs</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Where the coloured coating is <strong>removed</strong>, exposing pads</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top / bottom silkscreen</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.gto / .gbo</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Printed text and outlines</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top / bottom paste</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.gtp / .gbp</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Stencil openings for solder paste (needed only for machine assembly)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Board outline</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.gm1 (KiCad's Edge.Cuts)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The shape the board is cut to, including slots and cut-outs</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A common misunderstanding is that the solder mask file shows where the mask is. It is the other way round: it shows the openings. A pad missing from the mask file ends up covered in mask and cannot be soldered.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Drill Files: Every Hole</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Holes are not drawn in the Gerbers. They are listed in a separate <strong>drill file</strong>, usually in the Excellon format, one line per hole with its tool size and position. The start of the same demo board's drill file:</div>

```text
M48
; FORMAT={-:-/ absolute / metric / decimal}
; #@! TF.FileFunction,MixedPlating,1,2
METRIC
; #@! TA.AperFunction,Plated,PTH,ViaDrill
T1C0.600
; #@! TA.AperFunction,Plated,PTH,ComponentDrill
T2C0.750
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">METRIC sets the units. Each T line defines a tool: T1C0.600 is a 0.6 mm drill, and the attribute above it says it is used for <strong>plated vias</strong>. T2 is a 0.75 mm drill for <strong>plated component holes</strong>. Plated holes have copper inside them, connecting the layers; non-plated holes, such as mounting holes, do not, and are often listed separately.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On esp\_watch, the through-hole parts (the buttons, the slide switch and the module headers) and its four vias (each 0.6 mm across with a 0.3 mm drill, the 3.3 V one included) all appear in the drill file, and nowhere in the Gerbers. The MAX30102 module is soldered on SMD pads (C2), so it adds no holes.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Stackup, Fab Notes and the Board Drawing</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The fabricator also needs to know things no drawing shows:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Stackup</strong>: number of layers, board thickness, copper weight.</li><li style="margin:6px 0;">​<strong>Finish</strong> and <strong>colour</strong>.</li><li style="margin:6px 0;">​<strong>Fab notes</strong>: anything unusual, such as tight tolerances, slots, or controlled impedance.</li><li style="margin:6px 0;">A <strong>board dimension drawing</strong>: overall size and hole positions, for anyone checking the board against the case.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For a simple two-layer board ordered online, most of these are chosen as options on the order form. Write them down anyway, in a README in the zip, so that the order can be repeated exactly.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Assembly Files (Only If You Order Assembly)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">If a machine will place the parts, the assembler also needs a <strong>BOM</strong> in its own format and a <strong>CPL</strong> (placement list: each part's position, rotation and side). KiCad can export both, but the column names must match what the assembler expects, and part rotations should be checked in the assembler's preview before you pay [2]. You need them only if you choose machine assembly.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The One-Click Route</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's fabrication files were produced with a JLCPCB fabrication plugin for KiCad, which assembles the complete zip in one action. The plugin version is not relevant to the course and is not recorded. The resulting zip is a course asset, to be added when the order completes.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The zip esp\_watch actually sent to JLCPCB is in its public repository: <a href="https://github.com/niat-physicalai/esp_watch/blob/main/fabrication/Gerber/esp_watch.zip">fabrication/Gerber/esp\_watch.zip</a>. Download it and annotate it alongside your own.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">JLCPCB's help pages describe both routes: KiCad's own plot and position exports, with columns renamed by hand, and the JLCPCB Fabrication Toolkit plugin, which produces the Gerbers, drill files, BOM and CPL together [2]. Either is fine. What matters is the next step.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Annotating the Zip</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open the zip. For every file, write its <strong>layer or purpose</strong>, <strong>what it controls</strong>, and <strong>how you checked it</strong>. Here is the annotation for the KiCad demo board's export:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">File</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Purpose</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Controls</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Check</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-top\_layer.gtl</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top copper</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tracks and pads on top</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Header says Copper,L1,Top; viewed in a Gerber viewer</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-bottom\_layer.gbl</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bottom copper</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Tracks and pads underneath</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Viewed; matches the board</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-F\_Mask.gts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top solder mask</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Openings over top pads</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every pad has an opening</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-B\_Mask.gbs</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bottom solder mask</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Openings over bottom pads</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">As above</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-F\_Silkscreen.gto</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Top silkscreen</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Printed labels</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Text not on pads; readable</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-B\_Silkscreen.gbo</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bottom silkscreen</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Printed labels underneath</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Text reads mirrored correctly when viewed from below</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-F\_Paste.gtp / B\_Paste.gbp</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Paste stencils</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Solder paste for machine assembly</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Almost empty here: a through-hole board needs little paste</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-Edge\_Cuts.gm1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Board outline</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shape and cut-outs</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Header says Profile; outline closed</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer.drl</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Drill</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every hole, plated and non-plated, by tool size</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Units METRIC; header says MixedPlating; tool sizes match the design</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-job.gbrjob</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Gerber job file</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Describes the set: layer order, board size</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lists every Gerber</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pic\_programmer-pos.csv</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Placement (CPL)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Position, rotation, side of each part</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Columns present; only needed for assembly</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Every file has a purpose, and every layer the board uses has a file. Notice what the annotation caught on the way: the paste files are almost empty (a through-hole board), and the bottom silkscreen must be checked from below. That kind of observation is the point of opening the zip.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/F1-01.png" alt="esp_watch&#x27;s ordered fabrication files in KiCad&#x27;s Gerber viewer: one file per layer listed on the right, and the drill map below the board" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch's ordered fabrication files in KiCad's Gerber viewer: one file per layer listed on the right, and the drill map below the board</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Export your fabrication files</strong>, using a fab house plugin or KiCad's plot and drill dialogs.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Open the zip and view every layer</strong> in a Gerber viewer (KiCad includes one, called GerbView). Pick one pad and follow it through copper, mask, paste and silkscreen.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Annotate every file</strong>: purpose, what it controls, how you checked it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Write a README</strong> with stackup, thickness, finish, colour and any fab notes, and add it to the zip.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> the fabrication zip, including the README, and the file-by-file annotation table, saved in your design pack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The zip contains a Gerber for every copper, mask, silkscreen and outline layer your board uses. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. The zip contains a drill file, and its units match your design. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every file is listed in your annotation with its purpose and check. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every layer has been viewed in a Gerber viewer. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The README states layers, thickness, finish and colour. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The board outline in the Gerbers matches your board's dimensions. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. The zip was generated from the final, DRC-clean board. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The README states whether the order includes assembly. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A board comes back with no holes, although every layer looks correct. Which file was most likely missing from the zip?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The top copper Gerber</li><li style="margin:6px 0;">B. The drill file</li><li style="margin:6px 0;">C. The silkscreen</li><li style="margin:6px 0;">D. The BOM</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Holes are defined only in the drill file, not in any Gerber. <strong>A</strong> and <strong>C</strong> would show as missing layers, not missing holes. <strong>D</strong> is only used for assembly.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A pad on a returned board is covered in solder mask and cannot be soldered. What went wrong?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The pad was missing from the copper layer.</li><li style="margin:6px 0;">B. The pad had no opening in the solder mask file.</li><li style="margin:6px 0;">C. The drill file was wrong.</li><li style="margin:6px 0;">D. The silkscreen covered it.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The mask Gerber describes openings, so a missing opening means covered copper. <strong>A</strong> would mean no pad at all. <strong>C</strong> affects holes, not the coating. <strong>D</strong> is ink on top, not the mask.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A Gerber header contains %TF.FileFunction,Copper,L2,Bot\*%. What does it tell the fabricator?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The file's units.</li><li style="margin:6px 0;">B. That this file is the bottom copper layer, the second copper layer, without relying on the file name.</li><li style="margin:6px 0;">C. The board thickness.</li><li style="margin:6px 0;">D. The drill sizes.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The X2 file-function attribute states what the file is. <strong>A</strong> is set by the MO command. <strong>C</strong> and <strong>D</strong> are not in a copper Gerber.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Your board will be hand-soldered after it arrives. Which files must the order include?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Only the BOM</li><li style="margin:6px 0;">B. The Gerbers, the drill file and a README with the fab notes</li><li style="margin:6px 0;">C. The Gerbers, drill file, BOM and CPL</li><li style="margin:6px 0;">D. Only the KiCad project file</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A bare board needs only the fabrication files. <strong>A</strong> makes nothing. <strong>C</strong> adds assembly files you only need if a machine places the parts. <strong>D</strong> is not what fab houses build from.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> In the Gerber viewer, seen from the top, the text on your bottom silkscreen layer reads backwards. What should you do?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Mirror the text in KiCad and export again.</li><li style="margin:6px 0;">B. Nothing. Bottom silkscreen is seen from below, so it looks mirrored from the top.</li><li style="margin:6px 0;">C. Move the text to the top silkscreen.</li><li style="margin:6px 0;">D. Delete the bottom silkscreen file from the zip.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Bottom-layer text is drawn mirrored so that it reads correctly when the board is turned over. <strong>A</strong> would make it read backwards on the real board. <strong>C</strong> changes the design for no reason. <strong>D</strong> removes the labels completely.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="F2-quoting-without-ordering.md">F2 — Quoting Without Ordering</a> you will upload this zip to a fab house, read its automated checks, get a real quote, and build a cost model for 1 and 10 units, stopping just before you pay.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Ucamco. The Gerber Format (official Gerber format site, including Gerber X2 attributes). https://www.ucamco.com/en/gerber</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. JLCPCB. How To Export BOM and Pick &amp; Place Files From KiCad 10 (BOM minimum fields; KiCad CPL headings Ref, PosX, PosY, Rot, Side versus JLCPCB's Designator, Mid X, Mid Y, Rotation, Layer; Fabrication Toolkit plugin with automatic component translations). https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad</div>
