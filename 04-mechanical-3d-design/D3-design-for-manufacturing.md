# D3 — Design for Manufacturing
## Making the Case Printable Now, and Understanding What Changes at 10,000 Units

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Mechanical and 3D Design
**Time:** ~1.5 hours · **You will produce:** a completed DFM self-audit checklist for your enclosure

---

### A Perfect Model Is Not a Printable Part

The enclosure in your CAD tool has walls exactly 1.5 mm thick, a lid that slides onto the base with 0.1 mm to spare, crisp square corners and a display window with a perfectly flat overhanging lip. On screen it is flawless.

Printed, the walls come out a slightly different thickness than you asked for, because the printer lays plastic in lines of a fixed width. The lid will not go on, because the printer's accuracy is looser than your 0.1 mm gap. The first layer spreads outwards, so the base is wider at the bottom than at the top. The overhanging lip droops into strings.

**Design for manufacturing** (DFM) means shaping the part to suit the process that will make it. This unit covers the realities of FDM 3D printing, the process esp_watch's case uses; how to hold the parts together; and, as a contrast, what changes if the same case were injection moulded at volume, which is why almost every commercial watch case is moulded or machined rather than printed.

### What You Will Be Able to Do After This Reading

- **Choose** wall thicknesses, clearances and orientations that suit FDM printing.
- **Identify** overhangs, bridges and first-layer problems in a model before printing.
- **Select** a fastening method (self-tapping screw, heat-set insert, snap fit or press fit) and justify it.
- **Explain** what injection moulding would require of the same design: draft, uniform walls, ribs and tooling.
- **Complete** a DFM self-audit of your own enclosure.

### What Part 1 Already Covered

Part 1 did not cover manufacturing processes. **Everything here is new**: how a process shapes a design, and how the right design changes as quantities grow.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — FDM Realities

## How FDM Builds a Part

**FDM** (fused deposition modelling, also called FFF) melts a plastic filament and lays it down through a nozzle, one line at a time, one layer at a time. Almost every FDM design rule follows from three facts:

1. **Plastic goes down in lines of a fixed width.** With a 0.4 mm nozzle, a line is about 0.45 mm wide.
2. **Each layer needs something underneath it.** A layer printed over empty air droops.
3. **Hot plastic shrinks as it cools.** Parts pull and curl, especially at their base.

## Wall Thickness: Count the Lines

A wall is printed as a number of side-by-side lines, called **perimeters**. Prusa's guidance for a 0.4 mm nozzle gives approximate wall thicknesses for each count [1]:

| Perimeters | Approximate wall thickness |
|---|---|
| 1 | 0.45 mm |
| 2 | 0.9 mm |
| 3 | 1.35 mm |
| 4 | 1.8 mm |

A wall that falls between two of these, such as 1.5 mm, is printed as three perimeters plus a thin, awkward gap fill. It is better to choose a wall that is a whole number of perimeters.

### Worked Example: Choosing esp_watch's Wall

In D1 the example wall was 1.5 mm. **Assumption:** a 0.4 mm nozzle with 0.45 mm lines.

**Step 1: How many lines is 1.5 mm?**

```text
1.5 mm ÷ 0.45 mm = 3.33 lines
```

It is three full perimeters with a 0.15 mm gap to fill, which the slicer handles poorly.

**Step 2: Round to a whole number.**

```text
3 perimeters = 1.35 mm   (thinner, lighter)
4 perimeters = 1.80 mm   (stronger, adds 0.9 mm to the overall width)
```

**Step 3: Check against the product.** For a small watch case that must survive knocks, and whose strap lugs carry load (D4), four perimeters is the safer choice for the side walls. The base and lid could stay at three. With D1's parameters, that means `wall = 1.8`, `floor_t = 1.35`, `lid_t = 1.35`, and the model updates itself.

**Check.** The outer width becomes 38 + 1 + 3.6 = 42.6 mm, and the height becomes 14.044 + 1 + 2.7 = 17.7 mm, slightly thinner than before. Both changes are one parameter edit each.

<!-- REFPRODUCT:START -->
esp_watch's printer, material, layer height and wall settings are not recorded. The numbers above are **example values** for a common 0.4 mm nozzle. Take your own from your printer or print service.
<!-- REFPRODUCT:END -->

## Clearance Between Parts

Printed parts are not exact. Prusa states that its printers are accurate to at least 0.2 mm, and that materials can warp and shrink, so parts that must fit together need a deliberate gap; for parts that move, it suggests starting with at least 0.3 mm [1]. Another printer maker's design rules suggest about 0.2 mm for a loose fit and 0.1 mm for a tight fit [2].

There is no single right value. It depends on your printer, material, part size and orientation. The professional habit is to **print a test**: a small pair of parts with a range of clearances, such as 0.1, 0.2, 0.3 and 0.4 mm, and use the one that fits the way you want. Make the clearance a parameter (D1), so the result can be applied everywhere at once.

## Orientation, Overhangs and Bridges

**Orientation** decides which faces are smooth, where supports go and in which direction the part is strong. FDM parts are weakest *between* layers, so orient the part so that loads run along the layers rather than trying to peel them apart.

An **overhang** is a surface that leans out over nothing. The Hubs design guide notes that an overhang up to about 45° can usually be printed without support, because each new layer still rests about half on the one below; beyond that, support is needed [3]. A **bridge** is a horizontal span between two supports; long bridges sag, and the same guide warns of sagging beyond about 5 mm [3].

For an enclosure, orientation usually means:

- **Base:** print it open side up, floor on the bed. The floor is flat, the walls are vertical, and nothing overhangs except the openings in the walls.
- **Lid:** print it outer face down, for a smooth visible face, with any lip or inner features pointing up.
- **Side openings**, such as a USB-C port, are holes in vertical walls, so their tops are bridges. Keep them short, or shape the top of the opening as a pointed arch or a 45° chamfer so it needs no support.

## The First Layer

The first layer is pressed onto the bed to make it stick. It spreads slightly wider than the rest, a flare called **elephant's foot** [3], so a base printed floor-down is a little wider at the bottom. Materials that print hot, such as ABS, also tend to **warp**, curling up at the corners as they cool [3].

Two design habits help: add a small **chamfer** (about 0.3–0.5 mm) to edges that touch the bed, so the flare does not interfere with fits; and give corners a **radius** rather than a sharp point, which reduces warping.

> **Try it: Find the print problems.** Open your D1 or D2 enclosure.
> 1. **Predict.** Which features will need support if you print the base floor-down and the lid face-down?
> 2. **Do.** Look at every face that points downwards in each orientation, and every opening in a vertical wall. Measure any horizontal span.
> 3. **Explain.** Which could you redesign to print without support: a chamfer, an arch-topped opening, a shorter span, or a different orientation?

<!-- MEDIA
type: photo
id: D3-01
caption: A clearance test print: four pin-and-hole pairs at 0.1, 0.2, 0.3 and 0.4 mm
brief: A small FDM test print on a desk or cutting mat: a flat plate with four holes and
  four matching separate pins, each pair labelled in raised text "0.1", "0.2", "0.3",
  "0.4". One pin is shown fully inserted in the 0.2 hole, another stuck halfway in the
  0.1 hole. Photographed from above at an angle, in good light, with a ruler for scale.
  The filament colour contrasts with the background.
-->

---

# Part 2 — Holding the Parts Together

## Four Ways to Fasten

| Method | How it works | Strengths | Weaknesses | Good for |
|---|---|---|---|---|
| **Self-tapping screw** | A screw cuts its own thread into a printed hole | No extra parts; cheap | Threads wear if opened often | Cases opened rarely |
| **Heat-set insert** | A brass insert is melted into a printed hole with a soldering iron; a machine screw threads into it | Strong, reusable threads | Extra part and a step; needs a boss wide enough | Cases opened often, such as for battery service |
| **Snap fit** | A flexible hook on one part clicks over a lip on the other | No tools, no extra parts | Can break if flexed too far; tuning takes test prints | Lids that must open by hand |
| **Press (interference) fit** | One part is slightly larger than the hole it goes into, and friction holds it | Simple, no visible fasteners | Very sensitive to print accuracy; loosens with wear | Parts that rarely come apart |

For every method, **source the hardware before designing for it**. A heat-set insert or a screw comes with its own recommended hole size from the supplier. Design the hole to that, as a parameter, not to a number from a forum.

<!-- REFPRODUCT:START -->
esp_watch's lid is held on by an **interference fit**. It is simple and invisible, and it fits the design's small size. It is also the fastening method most sensitive to the printer: the lid may be too tight on one printer and too loose on another, and it will loosen each time the case is opened. Because the battery sits inside, a case that is opened for charging or service would benefit from a more repeatable method, such as a snap fit tuned with test prints or small screws into heat-set inserts. That is a trade-off worth recording as an ADR.
<!-- REFPRODUCT:END -->

> **Teaching model.** The table compares methods for printed plastic. Moulded parts use the same ideas with far tighter tolerances, which is why snap fits and press fits are far more reliable in moulded products than in printed ones.

---

# Part 3 — What Changes at 10,000 Units

## Why Commercial Watch Cases Are Not Printed

FDM is ideal for a first product: no tooling, parts in hours, and every print can be different. But each part takes time on the printer, the surface shows its layers, and the accuracy is limited. At thousands of units, **injection moulding** takes over: molten plastic is forced into a steel or aluminium **mould**, and a part pops out in seconds. The mould itself is a large one-off cost, so moulding only makes sense when that cost is spread over many parts. You will put numbers on that in E2.

Moulding brings its own design rules, and a case designed for printing usually breaks several of them.

## Moulding Rules, Briefly

**Draft.** Walls must taper slightly so the part can slide out of the mould. Protolabs suggests 1–2° works in most situations, with at least 0.5° on all vertical faces, and more for textured surfaces [4]. Printed parts need no draft, so printed designs rarely have it.

**Uniform walls.** Plastic shrinks as it cools, and thick sections cool slower than thin ones, which causes sink marks and warping. Walls should be as uniform as possible. Protolabs advises that adjoining walls should not drop below about 40–60% of each other's thickness [5].

**Ribs, not thickness.** To make a moulded wall stiffer, add thin **ribs**, rather than thickening the wall. Protolabs suggests ribs about 40–60% of the adjoining wall's thickness [6].

**Radii.** Rounded inside corners help the plastic flow and reduce stress [6].

**Undercuts.** A feature that would stop the part sliding straight out of the mould, such as a side hole or a snap-fit hook, needs a moving section of mould, called a side action, which adds cost [6].

**Gates.** The plastic enters the mould through a **gate**, which leaves a small mark. Its position is chosen with the moulder, away from visible faces.

## Worked Example: The Printed Case, Reviewed for Moulding

<!-- REFPRODUCT:START -->
Take a printed case like esp_watch's and review it as if it were going to be moulded.

| Feature | As designed for FDM | Moulding problem | Moulding change |
|---|---|---|---|
| Side walls | Vertical, 1.8 mm | No draft | Add 1–2° draft to walls |
| Base floor and walls | Floor thicker than walls in places | Non-uniform, risk of sink | Even out to a common thickness; add ribs where stiffness is needed |
| Mounting bosses | Solid posts | Thick, will sink | Hollow bosses with thinner walls, tied to walls with ribs |
| USB-C opening in the left wall | A hole in a vertical wall | An undercut | Side action in the mould, or move the parting line |
| Interference-fit lid | Relies on print tolerance | Works well at moulding tolerances | Could become a snap fit, designed with the moulder |
| Sharp inside corners | Easy to print | Stress and poor flow | Add inside radii |
<!-- REFPRODUCT:END -->

**Check.** Nearly every row changes. That is normal, and it is why a design intended for volume is usually reworked for moulding with the moulder's input, rather than simply sent off. The printed version is still the right choice for version 1: it proves the product works before anyone pays for a mould.

<!-- MEDIA
type: diagram
id: D3-02
caption: The same wall designed for printing and for moulding
brief: Two side-by-side cross-sections of an enclosure corner. Left, "FDM": vertical outer
  and inner walls, a thick solid screw boss merged into the wall, a sharp inside corner,
  and a 45° chamfer at the bed edge. Right, "Injection moulded": walls with a small draft
  angle labelled "1–2°", a hollow boss connected to the wall by a thin rib labelled
  "rib ≈ 50% of wall", a rounded inside corner labelled "radius", and uniform wall
  thickness arrows. Clean line drawing, labels in a sans-serif font.
-->

> **Try it: Review for volume.** Take your own enclosure.
> 1. **Predict.** How many features would need to change for moulding?
> 2. **Do.** Go through every feature and check it against draft, uniform walls, ribs, radii and undercuts, as in the table above.
> 3. **Explain.** Which change would be the most expensive in a mould, and why?

---

# Putting It All Together

## Applying What You Have Learned

**1. Fix walls to whole perimeters.** Set your wall, floor and lid parameters to multiples of your line width, with a reason for each.

**2. Set clearances from a test.** Choose your fit clearance from a test print, or, if you cannot print, from your printer's documentation, and record where the number came from.

**3. Choose orientations.** Decide how each part will be printed, and remove or reshape overhangs and long bridges.

**4. Choose a fastening method.** Pick one, with a reason tied to how often the case is opened, and design the holes from the hardware supplier's recommended sizes.

**5. Complete the DFM self-audit** below for your enclosure.

### DFM Self-Audit Checklist

| # | Item | Y/N | Note |
|---|---|---|---|
| 1 | Every wall is a whole number of perimeters for my nozzle | | |
| 2 | Clearances come from a test print or documented printer accuracy | | |
| 3 | Clearance is a single parameter used for every fit | | |
| 4 | Each part has a chosen print orientation | | |
| 5 | No overhang steeper than about 45° without support, or support is planned | | |
| 6 | No bridge longer than about 5 mm, or it is reshaped | | |
| 7 | Edges touching the bed have a small chamfer | | |
| 8 | Inside corners have a radius | | |
| 9 | The fastening method is chosen, with a reason | | |
| 10 | Holes for screws or inserts are sized from the supplier's figures | | |
| 11 | A moulding review lists the changes needed for volume | | |

**Deliverable:** the completed checklist, with a note on every "N", saved in your design pack as `D3-dfm-audit.md`.

## Self-Check

Open `D3-dfm-audit.md` and answer each item Y or N.

1. Every row of the audit has a Y or N. — Y/N
2. Every "N" has a note explaining the plan or the accepted risk. — Y/N
3. Your wall parameter is a whole number of perimeters. — Y/N
4. Your clearance value has a stated source. — Y/N
5. Each part's print orientation is written down. — Y/N
6. The fastening choice is justified by how often the case will be opened. — Y/N
7. The moulding review covers draft, walls, ribs, radii and undercuts. — Y/N
8. Any change you made in CAD was made through parameters. — Y/N

---

## Check Your Understanding

**1.** With a 0.4 mm nozzle printing 0.45 mm lines, which wall thickness prints most cleanly?

- A. 1.5 mm
- B. 1.35 mm
- C. 1.0 mm
- D. 0.6 mm

<details>
<summary>Answer</summary>

**B.** 1.35 mm is exactly three perimeters. **A** is 3.33 lines and leaves an awkward gap to fill. **C** is 2.2 lines and **D** is 1.3 lines, both leaving partial lines.

</details>

**2.** A lid designed with 0.05 mm clearance will not fit on its printed base. What is the best fix?

- A. Sand the lid until it fits.
- B. Increase the clearance parameter to a value found from a test print, such as 0.2 mm, and reprint.
- C. Print slower.
- D. Remove the clearance entirely.

<details>
<summary>Answer</summary>

**B.** Printers are only accurate to a few tenths of a millimetre, so fits need a tested clearance, applied through the parameter so every fit updates. **A** fixes one part and teaches nothing. **C** may help slightly, but will not make 0.05 mm reliable. **D** makes the problem worse.

</details>

**3.** A USB-C opening in a vertical wall prints with a drooping top edge. What is the simplest design fix?

- A. Make the wall thicker.
- B. Shape the top of the opening as a 45° chamfer or pointed arch, so it needs no support.
- C. Print the case upside down.
- D. Use ABS instead of PLA.

<details>
<summary>Answer</summary>

**B.** The top of a hole in a vertical wall is a bridge; shaping it so each layer rests on the one below removes the need for support. **A** makes the bridge longer, not better. **C** may create other overhangs. **D** is more prone to warping, and does not solve bridging.

</details>

**4.** A case with the battery inside is opened often for service. Which fastening method is best supported?

- A. Interference fit
- B. Self-tapping screws into plastic
- C. Machine screws into heat-set inserts
- D. Glue

<details>
<summary>Answer</summary>

**C.** Brass inserts give reusable threads that survive repeated opening. **A** loosens with each opening and depends on print accuracy. **B** wears its plastic threads each time. **D** makes service impossible.

</details>

**5.** Why does a case designed for FDM usually need changes before it can be injection moulded?

- A. Moulds cannot make plastic parts.
- B. FDM designs often lack draft, have uneven wall thickness and solid bosses, and contain undercuts, all of which cause problems in a mould.
- C. Moulded parts are always larger.
- D. Moulding cannot make holes.

<details>
<summary>Answer</summary>

**B.** Each of these is harmless in printing and costly or defective in moulding. **A**, **C** and **D** are false.

</details>

---

## What You Can Now Do, and What Comes Next

- Set walls, clearances and orientations that suit FDM.
- Spot overhangs, bridges and first-layer problems before printing.
- Choose a fastening method and design for the real hardware.
- Review a printed design for moulding, and explain what changes at volume.

The idea to carry forward: **design for the process that will actually make the part, and know which process that will be at each quantity.**

In [D4 — Functional Mechanical Design for a Wearable](D4-functional-mechanical-design.md) you will design the features that make the case work on a body: the sensor window, strap lugs, battery bay, button feel and sweat protection.

---

## References

1. Prusa Research. *Modeling with 3D printing in mind* (wall thickness per perimeter for a 0.4 mm nozzle; accuracy "at least 0.2 mm"; at least 0.3 mm for movable parts). https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
2. Hydra Research. *Design Rules for FFF 3D Printing* (clearance about 0.2 mm loose, 0.1 mm tight; walls at least two extrusions wide). https://www.hydraresearch3d.com/design-rules
3. Protolabs Network (Hubs). *How to design parts for FDM 3D printing* (overhangs up to about 45° without support; bridges sag beyond about 5 mm; elephant's foot; warping; chamfer bed edges). https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
4. Protolabs. *Draft Angle Guidelines for Injection Molding* (0.5° on vertical faces strongly advised; 1–2° works in most situations). https://www.protolabs.com/resources/design-tips/improving-part-moldability-with-draft/
5. Protolabs. *Injection Molding Wall Thickness Guidelines* (uniform walls; adjoining walls no less than 40–60% of each other). https://www.protolabs.com/resources/design-tips/improving-part-design-with-uniform-wall-thickness/
6. Protolabs. *Injection Molding Basics* (radii, ribs at 40–60% of adjacent wall, core-cavity approach, undercuts and side actions). https://www.protolabs.com/resources/design-tips/injection-molding-basics/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
