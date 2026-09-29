# E3 — Design for Manufacturing
## Making the Case Printable, and Holding a Prototype Together

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Mechanical and 3D Design
**Time:** ~1.5 hours · **You will produce:** a completed DFM self-audit checklist for your enclosure, and a hardware list with supplier links

---

### A Perfect Model Is Not a Printable Part

The enclosure in your CAD tool has walls exactly 1.5 mm thick, a lid that slides onto the base with 0.1 mm to spare, crisp square corners and a display window with a perfectly flat overhanging lip. On screen it is flawless.

Printed, the walls come out a slightly different thickness than you asked for, because the printer lays plastic in lines of a fixed width. The lid will not go on, because the printer's accuracy is looser than your 0.1 mm gap. The first layer spreads outwards, so the base is wider at the bottom than at the top. The overhanging lip droops into strings.

**Design for manufacturing** (DFM) means shaping the part to suit the process that will make it. Your prototype will be 3D printed, so this unit is about FDM printing and the off-the-shelf hardware that holds printed prototypes together: threaded inserts, M2–M4 screws, nuts, magnets and snap fits. A short section at the end explains why mass-produced cases are moulded instead.

### What You Will Be Able to Do After This Reading

- **Choose** wall thicknesses, clearances and orientations that suit FDM printing.
- **Identify** overhangs, bridges and first-layer problems in a model before printing.
- **Select** fastening hardware (heat-set insert, self-tapping screw, captive nut, magnet, snap fit or press fit) and **design** the boss, hole or pocket it needs.
- **Complete** a DFM self-audit of your own enclosure.

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

In E0 the example wall was 1.5 mm. **Assumption:** a 0.4 mm nozzle with 0.45 mm lines.

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

**Step 3: Check against the product.** For a small watch case that must survive knocks, and whose strap lugs carry load (E4), four perimeters is the safer choice for the side walls. The base and lid could stay at three. With E0's parameters, that means `wall = 1.8`, `floor_t = 1.35`, `lid_t = 1.35`, and the model updates itself.

**Check.** The outer width becomes 38 + 1 + 3.6 = 42.6 mm, and the height becomes 14.044 + 1 + 2.7 = 17.7 mm, slightly thinner than before. Both changes are one parameter edit each.

<!-- REFPRODUCT:START -->
esp_watch's printer, material, layer height and wall settings are not recorded. The numbers above are **example values** for a common 0.4 mm nozzle. Take your own from your printer or print service.
<!-- REFPRODUCT:END -->

## Clearance Between Parts

Printed parts are not exact. Prusa states that its printers are accurate to at least 0.2 mm, and that materials can warp and shrink, so parts that must fit together need a deliberate gap; for parts that move, it suggests starting with at least 0.3 mm [1]. Another printer maker's design rules suggest about 0.2 mm for a loose fit and 0.1 mm for a tight fit [2].

There is no single right value. It depends on your printer, material, part size and orientation. The professional habit is to **print a test**: a small pair of parts with a range of clearances, such as 0.1, 0.2, 0.3 and 0.4 mm, and use the one that fits the way you want. Make the clearance a parameter (E0), so the result can be applied everywhere at once.

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

> **Try it: Find the print problems.** Open your E0 or E2 enclosure.
> 1. **Predict.** Which features will need support if you print the base floor-down and the lid face-down?
> 2. **Do.** Look at every face that points downwards in each orientation, and every opening in a vertical wall. Measure any horizontal span.
> 3. **Explain.** Which could you redesign to print without support: a chamfer, an arch-topped opening, a shorter span, or a different orientation?

<!-- MEDIA
type: photo
id: E3-01
caption: A clearance test print: four pin-and-hole pairs at 0.1, 0.2, 0.3 and 0.4 mm
brief: A small FDM test print on a desk or cutting mat: a flat plate with four holes and
  four matching separate pins, each pair labelled in raised text "0.1", "0.2", "0.3",
  "0.4". One pin is shown fully inserted in the 0.2 hole, another stuck halfway in the
  0.1 hole. Photographed from above at an angle, in good light, with a ruler for scale.
  The filament colour contrasts with the background.
-->

---

# Part 2 — Holding a Prototype Together

## The Prototyping Toolkit

Printed parts are held together with a small set of cheap, standard hardware. All of it is sold by Indian maker suppliers such as Robu, usually in packs.

| Method | How it works | Strengths | Weaknesses | Good for |
|---|---|---|---|---|
| **Heat-set insert + machine screw** | A brass insert is pressed into a printed hole with a hot soldering iron and melts itself in. A machine screw (M2, M2.5, M3…) threads into the brass. | Strong threads that survive many openings | One extra part and a step; needs a boss wide enough | Cases opened often, for example for battery service |
| **Self-tapping screw** | A screw with a sharp thread cuts its own thread into a plain printed hole | No extra parts; cheapest | Plastic threads wear out after a few openings | Cases opened rarely |
| **Captive nut** | A hexagonal pocket holds a standard nut; a machine screw passes through the other part into it | Cheap, strong, no heat step | Needs space for the hex pocket | Larger parts and mounts; M3/M4 |
| **Magnets** | Small neodymium disc magnets are pressed or glued into matching pockets in the two parts | No tools; opens and closes by hand; hidden | Weak against a knock; must get polarity right | Battery hatches and lids that open often |
| **Snap fit** | A flexible hook on one part clicks over a lip on the other | No extra parts | Can break if flexed too far; takes test prints to tune | Lids that open by hand |
| **Press (interference) fit** | One part is slightly larger than the hole it goes into, and friction holds it | Simple, invisible | Very sensitive to print accuracy; loosens with wear | Parts that rarely come apart |

## Choosing a Screw Size

| Size | Typical use in a prototype |
|---|---|
| **M2 / M2.5** | Small wearables and handheld cases, and mounting small PCBs. M2 and M2.5 match many module mounting holes. |
| **M3** | The default prototyping size: enclosures, brackets, mounting larger boards. Screws, nuts, inserts and standoffs are the easiest to find. |
| **M4** | Larger products, wall or desk mounts, and anything carrying real load. Too big for a watch. |

The "M" number is the thread's outer diameter in millimetres, so an M3 screw is 3 mm across the thread. Pick one or two sizes for the whole product, so one screwdriver and one bag of inserts do everything.

## Designing the Boss, Hole or Pocket

The hardware decides the hole, so **buy or choose the part first, then design to its datasheet or listing**. Put every size in a named parameter (E0), so a change of hardware is one edit.

| Hardware | What to design | Where the size comes from |
|---|---|---|
| Heat-set insert | A hole slightly smaller than the insert's outside diameter, a little deeper than the insert, inside a **boss** with a wall of at least about the insert's own diameter around it | The insert supplier's recommended hole diameter and depth |
| Self-tapping screw | A pilot hole a little smaller than the screw's thread | The screw supplier's pilot-hole figure, then a test print |
| Captive nut | A hexagonal pocket sized to the nut's across-flats width plus your clearance (Part 1) | Nut size (for example, an M3 nut is 5.5 mm across flats) |
| Magnet | A round pocket sized to the magnet plus clearance, at a depth that leaves a thin skin (about one or two layers) or lets the magnet sit flush | The magnet's diameter and thickness |
| Clearance hole (screw passes through) | A hole slightly larger than the screw, for example about 3.2–3.4 mm for M3 | Standard clearance tables, then a test print |

<!-- FACT:VERIFY M3 nut 5.5 mm across flats (ISO 4032) and M3 clearance hole 3.2–3.4 mm — confirm against a standard clearance table before publishing -->

**Example values.** A common M3 heat-set insert is roughly 4–5 mm across and 4–6 mm long, and needs a boss of about 8–9 mm outside diameter. Sizes differ between brands, which is exactly why you design from the listing of the insert you actually bought.

<!-- FACT:VERIFY typical M3 heat-set insert dimensions and recommended hole sizes — take from a real supplier listing (Robu or similar) -->

**Magnets, three habits:**

1. **Mark the polarity.** Put all magnets in one part with the same face up, then place the other part's magnets by letting them attract. A reversed magnet repels the lid.
2. **Glue or embed them.** A press fit alone can let a magnet pull out. A drop of glue, or pausing the print to drop the magnet in and printing over it, holds it for good. Your slicer can insert a pause at a chosen layer (E5).
3. **Keep them away from a magnetometer.** A magnet next to a compass sensor ruins its readings. The MPU-6050 has no magnetometer, so this does not affect esp_watch, but it would affect a nine-axis IMU.

<!-- MEDIA
type: photo
id: E3-03
caption: Prototype fastening hardware: heat-set inserts, M2/M3 screws, a captive nut and disc magnets, beside the printed features that hold them
brief: Top-down photo on a cutting mat with a ruler. Left: a few brass heat-set inserts (M2 and
  M3), M2 and M3 screws, an M3 hex nut, three 6 × 2 mm disc magnets. Right: a small printed
  test piece with a boss with an insert melted in, a hexagonal nut pocket with the nut in
  place, and a round magnet pocket with a magnet flush in it. Label each item with small
  text labels. Good even light.
-->

<!-- REFPRODUCT:START -->
esp_watch's lid is held on by an **interference fit**. It is simple and invisible, and it fits the design's small size. It is also the fastening method most sensitive to the printer: the lid may be too tight on one printer and too loose on another, and it will loosen each time the case is opened. Because the battery sits inside, a case that is opened for charging or service would benefit from a more repeatable method, such as a snap fit tuned with test prints, small M2 screws into heat-set inserts, or a pair of magnets. That is a trade-off worth recording as a decision note (A2).
<!-- REFPRODUCT:END -->

> **Teaching model.** The table compares methods for printed plastic. Moulded parts use the same ideas with far tighter tolerances, which is why snap fits and press fits are far more reliable in moulded products than in printed ones.

---

# Part 3 — A Note on Mass Production

Printing is right for a prototype: no tooling, parts in hours, and every print can be different. Commercial watch cases are **injection moulded** instead. Molten plastic is forced into a steel mould, and a part comes out in seconds. The mould is a large one-off cost, so moulding only pays off over thousands of parts.

A printed design usually needs rework before it can be moulded. Walls need a slight taper (**draft**, about 1–2°) so the part slides out [4]. Walls must be a uniform thickness to avoid sink marks, and they are stiffened with thin ribs rather than made thicker [5][6]. Side holes need extra moving parts in the mould [6]. You don't need to design for any of this now. If your product ever goes to volume, the moulding company will review the design with you.

---

# Putting It All Together

## Applying What You Have Learned

**1. Fix walls to whole perimeters.** Set your wall, floor and lid parameters to multiples of your line width, with a reason for each.

**2. Set clearances from a test.** Choose your fit clearance from a test print, or, if you cannot print, from your printer's documentation, and record where the number came from.

**3. Choose orientations.** Decide how each part will be printed, and remove or reshape overhangs and long bridges.

**4. Choose your fastening hardware.** Pick the method and the screw size, with a reason tied to how often the case is opened. Find a real listing for the insert, screw, nut or magnet. Design each boss, hole or pocket from its sizes, as named parameters.

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
| 9 | The fastening method and screw size are chosen, with a reason | | |
| 10 | Holes, bosses and pockets for inserts, screws, nuts or magnets are sized from a real supplier listing | | |
| 11 | Every hardware size is a named parameter | | |
| 12 | A hardware list (part, size, quantity, supplier link) is saved with the design | | |

**Deliverable:** the completed checklist, with a note on every "N", and your hardware list (part, size, quantity, supplier link), saved in your design pack as `E3-dfm-audit.md`.

## Self-Check

Open `E3-dfm-audit.md` and answer each item Y or N.

1. Every row of the audit has a Y or N. — Y/N
2. Every "N" has a note explaining the plan or the accepted risk. — Y/N
3. Your wall parameter is a whole number of perimeters. — Y/N
4. Your clearance value has a stated source. — Y/N
5. Each part's print orientation is written down. — Y/N
6. The fastening choice is justified by how often the case will be opened. — Y/N
7. Every insert, screw, nut or magnet in the design appears in the hardware list with a supplier link. — Y/N
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

**5.** A battery hatch on a desk-top device must open by hand many times, with no tools. Which fastening suits it best?

- A. Self-tapping screws
- B. A pair of disc magnets in glued pockets, polarity marked
- C. A press fit
- D. Captive M4 nuts

<details>
<summary>Answer</summary>

**B.** Magnets open and close by hand indefinitely without wearing anything. **A** and **D** need a tool, and self-tapped threads wear out. **C** loosens with every opening and depends on print accuracy.

</details>

---

## What You Can Now Do, and What Comes Next

- Set walls, clearances and orientations that suit FDM.
- Spot overhangs, bridges and first-layer problems before printing.
- Choose fastening hardware (inserts, screws, nuts, magnets, snap fits) and design the features that hold it.

The idea to carry forward: **design for the process and the hardware that will actually make the part: choose the part first, then draw the hole.**

In [E4 — Functional Mechanical Design for a Wearable](E4-functional-mechanical-design.md) you will design the features that make the case work on a body: the sensor window, strap lugs, battery bay, button feel and sweat protection.

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
