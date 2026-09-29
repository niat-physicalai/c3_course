# E1 — The PCB Manufacturing Package
## What a Fab House Needs, and What Every File in the Zip Is For

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Sourcing and Manufacturing Handoff
**Time:** ~1 hour · **You will produce:** a complete fabrication zip, and a file-by-file annotation of its contents

---

### A One-Click Export You Cannot Explain Is a Liability

A board fabricator never sees your KiCad project. It receives a zip file of manufacturing data and makes exactly what that data describes. If a file is missing, the board may be made without a layer. If a file is wrong, the board is made wrong, precisely and quickly.

Modern tools make the export easy. A KiCad plugin can produce a fabricator-ready zip in one click. That is genuinely useful, and the reference watch's board was exported that way. But the first time a board comes back with a missing slot, a mirrored silkscreen or a part rotated the wrong way, "I clicked export" is not a diagnosis. This unit explains what a fabricator and an assembler need and why, shows you the real files, and asks you to open your own zip and account for everything inside it.

### What You Will Be Able to Do After This Reading

- **List** the files a fabricator needs, and **explain** what each one controls.
- **Read** the header of a Gerber and a drill file, and identify the layer and units.
- **Explain** the extra files an assembler needs, and why component rotation errors are so common.
- **Generate** a fabrication zip from your own board, and **annotate** every file in it.

### What Part 1 Already Covered

Part 1 did not cover board manufacturing. **Everything here is new.**

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## Two Jobs, Two Sets of Files

There are two separate jobs, often done by the same company:

```text
FABRICATION: making the bare board         ASSEMBLY: putting parts on it
────────────────────────────────           ─────────────────────────────
Gerber files (one per layer)               BOM (which part goes where)
Drill files (every hole)                   CPL / pick-and-place (position, rotation, side)
Stackup and fab notes                      Assembly drawing
Board outline and dimensions               (plus the fabrication files)
```

<!-- REFPRODUCT:START -->
esp_watch's board will be assembled **by hand**: every part is through-hole, plus a few larger surface-mount parts that can be soldered with an iron. So its order needs only the fabrication files. The assembly files still matter to you, because a module-based design that later moves to machine assembly will need them, and because you may use a fab's assembly service for your own design.
<!-- REFPRODUCT:END -->

## The Fabrication Files

### Gerber Files: One Picture per Layer

A **Gerber file** describes one layer of the board as a precise 2D drawing: where copper is, where solder mask is removed, where silkscreen ink goes, where the board edge is. The format is maintained by Ucamco, and its modern version, **Gerber X2**, adds attributes that say what each file *is* [1].

Here is the start of a real top-copper Gerber, exported from one of KiCad's demo boards with KiCad 10:

```text
%TF.GenerationSoftware,KiCad,Pcbnew,10.0.6-10.0.6~ubuntu26.04.1*%
%TF.FileFunction,Copper,L1,Top*%
%TF.FilePolarity,Positive*%
%FSLAX46Y46*%
G04 Gerber Fmt 4.6, Leading zero omitted, Abs format (unit mm)*
%MOMM*%
```

Read it line by line:

- `TF.FileFunction,Copper,L1,Top` is an **X2 attribute**: this file is copper layer 1, the top. The fabricator does not have to guess from the file name.
- `FSLAX46Y46` sets the number format: coordinates with 4 whole digits and 6 decimal places.
- `MOMM` means the units are **millimetres**.

Every board needs at least these layers, one file each:

| Layer | Typical file extension (KiCad default) | What it controls |
|---|---|---|
| Top copper | `.gtl` | Tracks, pads and pours on the top |
| Bottom copper | `.gbl` | The same, underneath |
| Top / bottom solder mask | `.gts` / `.gbs` | Where the coloured coating is **removed**, exposing pads |
| Top / bottom silkscreen | `.gto` / `.gbo` | Printed text and outlines |
| Top / bottom paste | `.gtp` / `.gbp` | Stencil openings for solder paste (needed only for machine assembly) |
| Board outline | `.gm1` (KiCad's Edge.Cuts) | The shape the board is cut to, including slots and cut-outs |

A common misunderstanding is that the solder mask file shows where the mask *is*. It is the other way round: it shows the openings. A pad missing from the mask file ends up covered in mask and cannot be soldered.

### Drill Files: Every Hole

Holes are not drawn in the Gerbers. They are listed in a separate **drill file**, usually in the Excellon format, one line per hole with its tool size and position. The start of the same demo board's drill file:

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

`METRIC` sets the units. Each `T` line defines a tool: `T1C0.600` is a 0.6 mm drill, and the attribute above it says it is used for **plated vias**. `T2` is a 0.75 mm drill for **plated component holes**. Plated holes have copper inside them, connecting the layers; non-plated holes, such as mounting holes, do not, and are often listed separately.

<!-- REFPRODUCT:START -->
On esp_watch, the MAX30102 module's footprint uses **1.0 mm** holes with 1.7 mm pads (B5), and the board's design rules used a via hole of 0.3 mm on signal nets and 0.4 mm on power nets. All of them appear in the drill file, and nowhere in the Gerbers.
<!-- REFPRODUCT:END -->

### Stackup, Fab Notes and the Board Drawing

The fabricator also needs to know things no drawing shows:

- **Stackup**: number of layers, board thickness, copper weight.
- **Finish** and **colour**.
- **Fab notes**: anything unusual, such as tight tolerances, slots, or controlled impedance.
- A **board dimension drawing**: overall size and hole positions, for anyone checking the board against the case.

For a simple two-layer board ordered online, most of these are chosen as options on the order form. Write them down anyway, in a README in the zip, so that the order can be repeated exactly.

## The Assembly Files

If a machine will place parts, the assembler needs two more files.

**The BOM** lists every part by designator. JLCPCB's help pages describe the minimum fields: a comment such as the value, the designator, the footprint, and the supplier's part number [2].

**The CPL** (component placement list, also called the centroid or pick-and-place file) gives each part's position, rotation and side. KiCad writes it with the headings `Ref, PosX, PosY, Rot, Side`; JLCPCB expects `Designator, Mid X, Mid Y, Rotation, Layer`, so the columns must be renamed or produced by a plugin [2]. Here are the first lines of the demo board's KiCad placement file:

```text
Ref,Val,Package,PosX,PosY,Rot,Side
"C1","100µF","CP_Axial_L18.0mm_D6.5mm_P25.00mm_Horizontal",110.490000,-78.867000,180.000000,top
"C3","22uF/25V","C_Axial_L12.0mm_D6.5mm_P20.00mm_Horizontal",134.112000,-62.230000,-90.000000,top
```

### Why Rotations Go Wrong

JLCPCB defines rotation in degrees, with positive values counter-clockwise [3]. The difficulty is that "0°" for a part means whatever orientation its footprint was drawn in, and footprint libraries and assembly machines do not all agree on what 0° should look like for each package. A part drawn with pin 1 at the top-left in one library may be expected with pin 1 at the bottom-left by the machine. The CPL is then correct by KiCad's definition and wrong by the machine's.

This is common enough that JLCPCB's own KiCad export guide recommends a plugin option that automatically corrects part rotations for its assembly line [2]. The practical defence is to **check the assembler's preview**: most fab houses show a render of every part on the board before you pay. Look at every polarised part, such as diodes, electrolytic capacitors, chips and connectors, and confirm pin 1 is where it should be.

## The One-Click Route

<!-- REFPRODUCT:START -->
esp_watch's fabrication files were produced with a JLCPCB fabrication plugin for KiCad, which assembles the complete zip in one action. The plugin version is not relevant to the course and is not recorded. The resulting zip is a course asset, to be added when the order completes.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/fab/esp_watch_jlcpcb.zip -->

JLCPCB's help pages describe both routes: KiCad's own plot and position exports, with columns renamed by hand, and the JLCPCB Fabrication Toolkit plugin, which produces the Gerbers, drill files, BOM and CPL together [2]. Either is fine. What matters is the next step.

## Worked Example: Annotating the Zip

Open the zip. For every file, write its **layer or purpose**, **what it controls**, and **how you checked it**. Here is the annotation for the KiCad demo board's export:

| File | Purpose | Controls | Check |
|---|---|---|---|
| `pic_programmer-top_layer.gtl` | Top copper | Tracks and pads on top | Header says `Copper,L1,Top`; viewed in a Gerber viewer |
| `pic_programmer-bottom_layer.gbl` | Bottom copper | Tracks and pads underneath | Viewed; matches the board |
| `pic_programmer-F_Mask.gts` | Top solder mask | Openings over top pads | Every pad has an opening |
| `pic_programmer-B_Mask.gbs` | Bottom solder mask | Openings over bottom pads | As above |
| `pic_programmer-F_Silkscreen.gto` | Top silkscreen | Printed labels | Text not on pads; readable |
| `pic_programmer-B_Silkscreen.gbo` | Bottom silkscreen | Printed labels underneath | Text reads mirrored correctly when viewed from below |
| `pic_programmer-F_Paste.gtp` / `B_Paste.gbp` | Paste stencils | Solder paste for machine assembly | Almost empty here: a through-hole board needs little paste |
| `pic_programmer-Edge_Cuts.gm1` | Board outline | Shape and cut-outs | Header says `Profile`; outline closed |
| `pic_programmer.drl` | Drill | Every plated hole, by tool size | Units `METRIC`; tool sizes match the design |
| `pic_programmer-job.gbrjob` | Gerber job file | Describes the set: layer order, board size | Lists every Gerber |
| `pic_programmer-pos.csv` | Placement (CPL) | Position, rotation, side of each part | Columns present; only needed for assembly |

**Check.** Every file has a purpose, and every layer the board uses has a file. Notice what the annotation caught on the way: the paste files are almost empty (a through-hole board), and the bottom silkscreen must be checked from below. That kind of observation is the point of opening the zip.

> **Try it: View your own layers.** Generate your board's fabrication files, from the plugin or KiCad's plot dialog.
> 1. **Predict.** How many files will there be, and which layers?
> 2. **Do.** Open them in a Gerber viewer: KiCad includes one, and many fab houses show a viewer when you upload. Turn layers on and off.
> 3. **Explain.** Did every layer look as expected? Find one pad and follow it through copper, mask, paste and silkscreen. What does each layer do to that pad?

<!-- MEDIA
type: screenshot
id: E1-01
caption: A fabrication zip opened in KiCad's Gerber viewer, with each layer listed
brief: KiCad's GerbView (Gerber viewer) with all files from a small two-layer board's
  fabrication zip loaded. The layers panel on the right lists each file with its detected
  function (top copper, bottom copper, masks, silkscreens, edge cuts, drill). The board
  view shows top copper and the outline, with one mounting hole and one via visible.
  Light theme.
-->

<!-- MEDIA
type: screenshot
id: E1-02
caption: An assembler's placement preview, with one part rotated the wrong way
brief: Screenshot of a fab house's assembly preview (for example JLCPCB's) showing a small
  board render with placed parts. One polarised part, such as an SOT-23 transistor or a
  diode, is shown rotated 90° from its footprint, with its pin-1 marker misaligned.
  Highlight it with a red circle and the label "pin 1 mismatch". Another correctly placed
  part is marked with a green tick for comparison. No account details visible.
-->

---

# Putting It All Together

## Applying What You Have Learned

**1. Export your fabrication files**, using a fab house plugin or KiCad's plot and drill dialogs.

**2. Open the zip and view every layer** in a Gerber viewer.

**3. Annotate every file**: purpose, what it controls, how you checked it.

**4. Write a README** with stackup, thickness, finish, colour and any fab notes, and add it to the zip.

**5. If your design will be machine-assembled**, generate the BOM and CPL in your chosen assembler's format, and list every polarised part to check in its preview.

**Deliverable:** the fabrication zip, including the README, and the file-by-file annotation table, saved in your design pack.

## Self-Check

1. The zip contains a Gerber for every copper, mask, silkscreen and outline layer your board uses. — Y/N
2. The zip contains a drill file, and its units match your design. — Y/N
3. Every file is listed in your annotation with its purpose and check. — Y/N
4. Every layer has been viewed in a Gerber viewer. — Y/N
5. The README states layers, thickness, finish and colour. — Y/N
6. If assembled by machine: the BOM and CPL use the assembler's column names. — Y/N
7. If assembled by machine: every polarised part is listed for checking in the preview. — Y/N

---

## Check Your Understanding

**1.** A board comes back with no holes, although every layer looks correct. Which file was most likely missing from the zip?

- A. The top copper Gerber
- B. The drill file
- C. The silkscreen
- D. The BOM

<details>
<summary>Answer</summary>

**B.** Holes are defined only in the drill file, not in any Gerber. **A** and **C** would show as missing layers, not missing holes. **D** is only used for assembly.

</details>

**2.** A pad on a returned board is covered in solder mask and cannot be soldered. What went wrong?

- A. The pad was missing from the copper layer.
- B. The pad had no opening in the solder mask file; the mask file shows where the mask is removed.
- C. The drill file was wrong.
- D. The silkscreen covered it.

<details>
<summary>Answer</summary>

**B.** The mask Gerber describes openings, so a missing opening means covered copper. **A** would mean no pad at all. **C** affects holes, not the coating. **D** is ink on top, not the mask.

</details>

**3.** A Gerber header contains `%TF.FileFunction,Copper,L2,Bot*%`. What does it tell the fabricator?

- A. The file's units.
- B. That this file is the bottom copper layer, the second copper layer, without relying on the file name.
- C. The board thickness.
- D. The drill sizes.

<details>
<summary>Answer</summary>

**B.** The X2 file-function attribute states what the file is. **A** is set by the `MO` command. **C** and **D** are not in a copper Gerber.

</details>

**4.** After machine assembly, a chip is soldered rotated 90° from where it should be, though the CPL matches KiCad exactly. What is the most likely cause?

- A. The pick-and-place machine is broken.
- B. The footprint's 0° orientation differs from the assembler's convention for that package, so a correct KiCad rotation is wrong for the machine.
- C. The Gerbers were mirrored.
- D. The BOM had the wrong value.

<details>
<summary>Answer</summary>

**B.** Rotation reference differences between libraries and assemblers are a common cause, which is why rotation-correction options and assembly previews exist. **A** would affect many parts at random. **C** would show on every layer. **D** would give the wrong part, not the wrong angle.

</details>

**5.** Why annotate every file in a one-click export, rather than trusting the plugin?

- A. Plugins are unreliable.
- B. So you can diagnose any fault on a returned board, and catch problems such as a missing layer or a wrong outline before paying.
- C. The fab house requires it.
- D. It makes the zip smaller.

<details>
<summary>Answer</summary>

**B.** Understanding the files is what lets you check them and fix problems. **A** is not the reason; plugins are usually fine. **C** and **D** are not true.

</details>

---

## What You Can Now Do, and What Comes Next

- List and explain every file a fabricator and an assembler need.
- Read Gerber and drill headers for layer, units and hole type.
- Explain why rotations go wrong, and how to catch them.
- Account for every file in your own fabrication zip.

The idea to carry forward: **the zip is the board.** The fabricator makes exactly what it describes, so you must know exactly what it says.

In [E2 — Quoting Without Ordering](E2-quoting-without-ordering.md) you will upload this zip to a fab house, read its automated checks, get a real quote, and build a cost model for 10, 100 and 1,000 units, stopping just before you pay.

---

## References

1. Ucamco. *The Gerber Format* (official Gerber format site, including Gerber X2 attributes). https://www.ucamco.com/en/gerber
2. JLCPCB. *How To Export BOM and Pick & Place Files From KiCad 10* (BOM minimum fields; KiCad CPL headings `Ref, PosX, PosY, Rot, Side` versus JLCPCB's `Designator, Mid X, Mid Y, Rotation, Layer`; Fabrication Toolkit plugin with automatic component translations). https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad
3. JLCPCB. *Pick & Place File for PCB Assembly* (rotation in degrees; positive values counter-clockwise). https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
