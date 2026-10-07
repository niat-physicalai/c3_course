# F1 — The PCB Manufacturing Package
## What a Fab House Needs, and What Every File in the Zip Is For

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 6 — Sourcing and Manufacturing Handoff
**Time:** ~1 hour · **You will produce:** a complete fabrication zip, and a file-by-file annotation of its contents

---

### A One-Click Export You Cannot Explain Is a Liability

A fabricator never sees your KiCad project. It makes exactly what your zip of manufacturing files describes. A missing file can mean a missing layer. A wrong file means a wrong board.

A KiCad plugin can export the zip in one click, and the reference watch's board was exported that way. But when a board comes back with a missing slot, a mirrored silkscreen or a part rotated the wrong way, "I clicked export" is not a diagnosis. So in this unit you open your own zip and account for every file in it.

### What You Will Be Able to Do After This Reading

- **List** the files a fabricator needs, and **explain** what each one controls.
- **Read** the header of a Gerber and a drill file, and identify the layer and units.
- **Name** the extra files an assembler needs, and when you need them.
- **Generate** a fabrication zip from your own board, and **annotate** every file in it.

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
esp_watch's board was soldered **by hand**. Its parts are through-hole, plus a few larger surface-mount parts that can be soldered with an iron. So its order needed only the fabrication files.

![The assembled esp_watch board, top side, running its firmware](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/Assembled/Top_assembled.png)

<!-- ASSET:PLACEHOLDER reference-files/images/assembled-bottom.jpg — photo of the assembled board's underside; author to add -->
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
On esp_watch, the through-hole parts (the buttons, the slide switch and the module headers) and its four vias (each 0.6 mm across with a 0.3 mm drill, the 3.3 V one included) all appear in the drill file, and nowhere in the Gerbers. The MAX30102 module is soldered on SMD pads (C2), so it adds no holes.
<!-- REFPRODUCT:END -->

### Stackup, Fab Notes and the Board Drawing

The fabricator also needs to know things no drawing shows:

- **Stackup**: number of layers, board thickness, copper weight.
- **Finish** and **colour**.
- **Fab notes**: anything unusual, such as tight tolerances, slots, or controlled impedance.
- A **board dimension drawing**: overall size and hole positions, for anyone checking the board against the case.

For a simple two-layer board ordered online, most of these are chosen as options on the order form. Write them down anyway, in a README in the zip, so that the order can be repeated exactly.

## The Assembly Files (Only If You Order Assembly)

If a machine will place the parts, the assembler also needs a **BOM** in its own format and a **CPL** (placement list: each part's position, rotation and side). KiCad can export both, but the column names must match what the assembler expects, and part rotations should be checked in the assembler's preview before you pay [2]. You need them only if you choose machine assembly.

## The One-Click Route

<!-- REFPRODUCT:START -->
esp_watch's fabrication files were produced with a JLCPCB fabrication plugin for KiCad, which assembles the complete zip in one action. The plugin version is not relevant to the course and is not recorded. The resulting zip is a course asset, to be added when the order completes.
<!-- REFPRODUCT:END -->

The zip esp_watch actually sent to JLCPCB is in its public repository: [`fabrication/Gerber/esp_watch.zip`](https://github.com/niat-physicalai/esp_watch/blob/main/fabrication/Gerber/esp_watch.zip). Download it and annotate it alongside your own.

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
| `pic_programmer.drl` | Drill | Every hole, plated and non-plated, by tool size | Units `METRIC`; header says `MixedPlating`; tool sizes match the design |
| `pic_programmer-job.gbrjob` | Gerber job file | Describes the set: layer order, board size | Lists every Gerber |
| `pic_programmer-pos.csv` | Placement (CPL) | Position, rotation, side of each part | Columns present; only needed for assembly |

**Check.** Every file has a purpose, and every layer the board uses has a file. Notice what the annotation caught on the way: the paste files are almost empty (a through-hole board), and the bottom silkscreen must be checked from below. That kind of observation is the point of opening the zip.

<!-- MEDIA
type: screenshot
id: F1-01
caption: A fabrication zip opened in KiCad's Gerber viewer, with each layer listed
brief: KiCad's GerbView (Gerber viewer) with all files from a small two-layer board's
  fabrication zip loaded. The layers panel on the right lists each file with its detected
  function (top copper, bottom copper, masks, silkscreens, edge cuts, drill). The board
  view shows top copper and the outline, with one mounting hole and one via visible.
  Light theme.
-->

<!-- MEDIA
type: screenshot
id: F1-02
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

**2. Open the zip and view every layer** in a Gerber viewer (KiCad includes one, called GerbView). Pick one pad and follow it through copper, mask, paste and silkscreen.

**3. Annotate every file**: purpose, what it controls, how you checked it.

**4. Write a README** with stackup, thickness, finish, colour and any fab notes, and add it to the zip.

**Deliverable:** the fabrication zip, including the README, and the file-by-file annotation table, saved in your design pack.

## Self-Check

1. The zip contains a Gerber for every copper, mask, silkscreen and outline layer your board uses. — Y/N
2. The zip contains a drill file, and its units match your design. — Y/N
3. Every file is listed in your annotation with its purpose and check. — Y/N
4. Every layer has been viewed in a Gerber viewer. — Y/N
5. The README states layers, thickness, finish and colour. — Y/N
6. The board outline in the Gerbers matches your board's dimensions. — Y/N
7. The zip was generated from the final, DRC-clean board. — Y/N
8. The README states whether the order includes assembly. — Y/N

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
- B. The pad had no opening in the solder mask file.
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

**4.** Your board will be hand-soldered after it arrives. Which files must the order include?

- A. Only the BOM
- B. The Gerbers, the drill file and a README with the fab notes
- C. The Gerbers, drill file, BOM and CPL
- D. Only the KiCad project file

<details>
<summary>Answer</summary>

**B.** A bare board needs only the fabrication files. **A** makes nothing. **C** adds assembly files you only need if a machine places the parts. **D** is not what fab houses build from.

</details>

**5.** In the Gerber viewer, seen from the top, the text on your bottom silkscreen layer reads backwards. What should you do?

- A. Mirror the text in KiCad and export again.
- B. Nothing. Bottom silkscreen is seen from below, so it looks mirrored from the top.
- C. Move the text to the top silkscreen.
- D. Delete the bottom silkscreen file from the zip.

<details>
<summary>Answer</summary>

**B.** Bottom-layer text is drawn mirrored so that it reads correctly when the board is turned over. **A** would make it read backwards on the real board. **C** changes the design for no reason. **D** removes the labels completely.

</details>

---

## What Comes Next

In [F2 — Quoting Without Ordering](F2-quoting-without-ordering.md) you will upload this zip to a fab house, read its automated checks, get a real quote, and build a cost model for 1 and 10 units, stopping just before you pay.

---

## References

1. Ucamco. *The Gerber Format* (official Gerber format site, including Gerber X2 attributes). https://www.ucamco.com/en/gerber
2. JLCPCB. *How To Export BOM and Pick & Place Files From KiCad 10* (BOM minimum fields; KiCad CPL headings `Ref, PosX, PosY, Rot, Side` versus JLCPCB's `Designator, Mid X, Mid Y, Rotation, Layer`; Fabrication Toolkit plugin with automatic component translations). https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad

