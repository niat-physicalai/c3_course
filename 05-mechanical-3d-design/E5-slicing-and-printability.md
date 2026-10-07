# E5 — Slicing and Printability Validation
## Checking the Print Before Anyone Prints It

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Mechanical and 3D Design
**Time:** ~30 minutes · **You will produce:** a sliced file, a preview screenshot and a time and material estimate

---

### The Slicer Is the Last Check

A **slicer** turns a 3D model into the instructions a printer follows: every layer, every line, every move. It is also the last free check before plastic is used. Its **preview** shows exactly what the printer will do, where supports will go, which areas will struggle, and how long and how much material the print will take. You will not print in this course, but you will stop at exactly the point where a printer would start, with a file ready to send and a cost you can defend.

### What You Will Be Able to Do After This Reading

- **Set** layer height, walls, infill and supports for an enclosure.
- **Choose** a print orientation in the slicer and check it against E3's decisions.
- **Read** the slicer preview to find overhangs, thin walls and first-layer risks.
- **Estimate** print time and material cost from the slicer's output.

---

## Choosing a Slicer

Any common slicer works: Cura, PrusaSlicer or Bambu Studio. PrusaSlicer is free and open source, and works with any FDM printer [1]. Pick the printer profile closest to the printer or print service you expect to use. If you do not know, choose a common 0.4 mm-nozzle printer, and say so.

Export each part from Fusion as a separate file: in the browser, right-click the `base` body, choose **Save As Mesh**, pick **3MF** (or STL) and save. Do the same for the `lid`. Then load both into the slicer.

<!-- MEDIA
type: screenshot
id: E2-W04
caption: Exporting a body from Fusion for the slicer
brief: Autodesk Fusion, Design workspace, the right-click menu on the "base" body in the
  browser with Save As Mesh highlighted, and the Save As Mesh dialog beside it with format
  3MF selected. Light theme.
-->

## The Settings That Matter

| Setting | What it controls | Starting point for a small case (example values) |
|---|---|---|
| **Layer height** | Smoothness against time | 0.2 mm; 0.12–0.16 mm for a finer surface |
| **Walls (perimeters)** | Strength and wall accuracy | Match your E3 decision, e.g. 3 or 4 |
| **Top and bottom layers** | Solid skin on flat faces | Enough for about 0.8–1 mm of solid skin |
| **Infill** | Strength inside solid regions | 15–20% for a case; more for lugs |
| **Supports** | Material under overhangs | "Only from the build plate" if possible |
| **Brim** | Extra first-layer grip | On, if corners lift (E3's warping) |

The most useful thing to know about a small case is that **most of it is walls**. A 1.35–1.8 mm wall is three or four perimeters with no infill at all, so infill matters mainly in thick features such as lugs and bosses.

## Orientation and Supports

Set each part in the orientation you chose in E3: the base floor-down, open side up; the lid outer face down. Then generate supports and look at where they appear.

**Supports inside the base or under the lid's openings are a design signal**, not just a slicer setting. Each one leaves a rough surface where it is removed. Go back to E3's fixes: chamfer or arch the top of a side opening, shorten a bridge, or rotate the part.

## Embedding Magnets or Nuts: Pause at a Layer

If E3 put a magnet or a nut inside a closed pocket, the printer has to stop so you can drop it in. PrusaSlicer, Cura and Bambu Studio can all insert a **pause** at a chosen layer. Find the first layer that would cover the pocket in the preview, add the pause just before it, and the printer will stop, wait for you to place the part, then print over it. Make sure the part sits flush with or below the top of its pocket, or the nozzle will hit it.

## Reading the Preview

Step through the preview layer by layer. Look for five things:

| Look for | What it means | Fix |
|---|---|---|
| Supports in unexpected places | An overhang you did not notice | Reshape in CAD (E3) |
| Walls shown as a single thin line, or gaps | A wall thinner than two perimeters | Thicken to a whole number of perimeters |
| Tiny isolated islands on a layer | Small features that may not stick | Enlarge, or merge with nearby geometry |
| Long travel moves or bridges over openings | Stringing or sagging risk | Shorten spans; reorient |
| Assembly faces sitting on the bed | Elephant's foot will flare them (the preview does not show it) | Add a bed-edge chamfer (E3), or turn on the slicer's elephant's-foot compensation |

<!-- MEDIA
type: screenshot
id: E5-01
caption: Bambu Studio preview of the enclosure base, with supports and the time and material estimate
brief: Bambu Studio, Preview tab, showing the watch enclosure base on the build plate,
  floor down. The layer slider on the right is set partway up, showing the walls as three
  or four perimeters and sparse infill in the bosses. Green support material visible under
  the top of the USB-C opening in the left wall. The sliced-info panel at the bottom right
  shows estimated print time and filament used in grams and metres. Legend showing feature
  types (perimeter, infill, support). Light theme.
-->

## Worked Example: Time and Material Cost

The slicer reports an estimated print time and the filament used, in grams. Turn those into a cost.

**Assumption:** the slicer estimates a base of 9 g and a lid of 4 g, taking 1 h 10 min and 35 min. These are **example values** for a case of about 42 × 43 × 18 mm; use your own slicer's numbers.

**Step 1: Material.** PLA filament listed at ₹649 per 1 kg spool, including GST, at Robu on 25 September 2026 [2].

```text
Filament used  = 9 g + 4 g              = 13 g
Price per gram = ₹649 ÷ 1,000 g         = ₹0.649 per g
Material cost  = 13 g × ₹0.649          = ₹8.44
```

**Step 2: Allow for waste.** Add supports, a brim and a failed first attempt. **Assumption:** 30% extra.

```text
13 g × 1.3 = 16.9 g → about ₹11
```

**Step 3: Time.**

```text
1 h 10 min + 35 min = 1 h 45 min of printer time per case
```

**Check.** The material is almost free: about ₹11. The printer's **time** is the real cost, because it limits how many cases one printer can make in a day, about 13 at 1 h 45 min each if it ran around the clock. That is exactly why the numbers change completely at volume, and why F2 includes time and a printing service's quote rather than filament alone.

<!-- REFPRODUCT:START -->
esp_watch's enclosure will be printed in black PLA but has not been sliced yet. When it is, its real printer settings, print time and filament use replace the example values above.
<!-- REFPRODUCT:END -->

<!-- PLACEHOLDER:DATA esp_watch slicing results (printer, layer height, print time, filament use) and slicer preview screenshot — author to add -->

> **Try it: Find the cheapest change.** Slice your own base.
> 1. **Predict.** Which setting will cut the print time the most: layer height, infill or walls?
> 2. **Do.** Change each one at a time (0.2 to 0.28 mm layers; 20% to 10% infill; 4 to 3 walls) and note the time each time.
> 3. **Explain.** Which saved the most? Which change would you accept for a wearable case, and which would you not?

---

# Putting It All Together

## Applying What You Have Learned

**1. Slice both parts** with a named printer profile and the settings from your E3 decisions.

**2. Read the preview** layer by layer, and fix in CAD anything that needs support you did not intend.

**3. Record the estimate:** time and grams for each part, and a material cost with a waste allowance.

**Deliverable:** the sliced file (G-code or 3MF project), a screenshot of the preview with the estimate panel visible, and your time and cost calculation, saved in your design pack.

## Self-Check

1. Both parts are sliced with a named printer profile and nozzle size. — Y/N
2. The walls setting matches your E3 wall decision. — Y/N
3. Each part is oriented as decided in E3. — Y/N
4. Every support in the preview is either intended or has been removed by a CAD change. — Y/N
5. The preview shows no walls thinner than two perimeters. — Y/N
6. Time and grams are recorded for each part. — Y/N
7. The material cost includes a stated waste allowance and a dated filament price. — Y/N

---

## Check Your Understanding

**1.** The slicer adds supports under the top edge of the USB-C opening in the base. What is the best response?

- A. Accept them; supports are normal.
- B. Reshape the top of the opening in CAD, for example as a 45° chamfer or arch, so it prints without support.
- C. Increase infill.
- D. Print the base upside down.

<details>
<summary>Answer</summary>

**B.** A small design change removes the need for support and gives a cleaner opening. **A** leaves rough marks on a visible, functional opening. **C** does not affect overhangs. **D** would put the open side on the bed and create far more overhangs.

</details>

**2.** A slicer estimates 13 g of PLA at ₹649 per kg. What is the material cost, before waste?

- A. About ₹0.65
- B. About ₹8.40
- C. About ₹84
- D. About ₹649

<details>
<summary>Answer</summary>

**B.** 13 g × ₹0.649 per g ≈ ₹8.44. **A** is the price of a single gram. **C** is ten times too large. **D** is the price of the whole spool.

</details>

**3.** For a small printed case with 1.8 mm walls, why does changing infill from 20% to 10% barely change the print time?

- A. Infill does not affect time.
- B. Most of a thin-walled case is perimeters, so there is little space for infill to fill.
- C. The slicer ignores infill below 20%.
- D. PLA cannot be printed at 10%.

<details>
<summary>Answer</summary>

**B.** A 1.8 mm wall is four solid perimeters; infill only appears in thicker regions. **A** is false in general. **C** and **D** are false.

</details>

**4.** A club wants 30 cases in two days from one printer. Each takes 1 h 45 min and about ₹11 of filament. What stops them?

- A. The filament cost
- B. The printer's time
- C. The 30% waste allowance
- D. The size of the STL file

<details>
<summary>Answer</summary>

**B.** 30 × 1 h 45 min = 52.5 h, more than the 48 h available. **A** is about ₹330 in total. **C** adds grams, not hours. **D** has no effect on printing.

</details>

**5.** Your base has two disc magnets that must be sealed inside the wall, 1 mm below the top face. How do you get them in?

- A. Glue them to the outside after printing.
- B. In the slicer, add a pause just before the first layer that covers the magnet pocket, drop the magnets in when the printer stops, then let it print over them.
- C. Print the pocket bigger and push them in later.
- D. Magnets cannot be used in printed parts.

<details>
<summary>Answer</summary>

**B.** Pausing just before the pocket is covered lets the printer seal the magnets inside (E3). Pause any earlier and the nozzle hits them. **A** leaves them exposed. **C** can work for an open pocket, but not one sealed under 1 mm of plastic. **D** is false.

</details>

---

## What Comes Next

This completes the mechanical module. Module 6 turns to buying parts and preparing the files a factory needs, starting with [F0 — Sourcing and the Lifecycle Trap](../06-sourcing-and-manufacturing/F0-sourcing-and-lifecycle.md).

---

## References

1. Prusa Research. *PrusaSlicer* ("Free, open-source slicer... Works with any FDM or resin printer"). https://www.prusa3d.com/p/prusaslicer/
2. Robu.in. *Pro-Range PLA Filament 1.75 mm 1 kg Spool, Black*, listing checked 25 September 2026 (₹649 incl. GST). https://robu.in/product/pro-range-pla-filament-1-75mm-1-kg-spool-black/

> supplier listing for the part you are actually using.
