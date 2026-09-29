# E4 — Functional Mechanical Design for a Wearable
## The Features That Make a Case Work on a Body

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Mechanical and 3D Design
**Time:** ~1.5 hours · **You will produce:** a revised enclosure, with the sensor-window and battery-retention reasoning written down

---

### A Box That Fits Is Not Yet a Watch

After E2 and E3 your case fits the board and can be printed. Put it on a wrist and new questions appear. Does the heart-rate sensor actually touch the skin, or is there a millimetre of plastic and air between them? What holds the strap on when the wearer catches it on a door handle? What stops the battery from being squashed by the lid, or rubbed by a screw head? Can the button be pressed through the wall without pushing the whole watch into the wrist? Where does sweat go?

None of these is about fitting parts in a box. They are about the product doing its job on a moving, sweating human body. This unit takes each one in turn and traces it back to a requirement from A0, so every feature has a reason you can write down.

### What You Will Be Able to Do After This Reading

- **Design** a skin-contact window that presents an optical sensor to the skin and blocks outside light.
- **Size** strap lugs for the loads a strap puts on the case.
- **Design** a battery bay that retains the cell without pressing on or puncturing it.
- **Design** buttons and openings that work through a wall, and plan for sweat.
- **Trace** every wearable feature back to a requirement, and record the reasoning.

### What Part 1 Already Covered

Part 1 did not cover mechanical design for the body. **What is new here** is designing a case around a person: skin contact, strap loads, battery safety, touch and sweat.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## 1. The Skin-Contact Window

### Why It Matters Most

An optical heart-rate sensor shines light into the skin and measures the small part that comes back (B0). Any outside light that reaches the photodiode is noise, and the signal it is hiding in is small. The MAX30102 datasheet shows how well the sensor copes when it is used as intended: with a finger on the sensor, in direct sunlight, its ambient light rejection holds the error to about 2 counts [1]. The condition matters. The sensor rejects outside light well **when it is pressed against skin**. Leave a gap, and light leaks in from the sides.

So the window has two jobs: **press the sensor against the skin**, and **seal out light around it**.

### Three Ways to Build It

| Option | How it works | Strengths | Weaknesses |
|---|---|---|---|
| **Open cut-out** | A hole in the base, the sensor's face sits flush with or slightly proud of the base | Direct skin contact; simple to print | The sensor's face is exposed to sweat; the edge of the hole must seal against skin |
| **Clear insert** | A transparent window bonded into the base, the sensor behind it | Protects the sensor; can be sealed | Any gap between sensor and window, or a thick window, lets light bounce sideways; needs a clear part |
| **Raised boss** | The sensor sits in a small dome that pushes into the skin | Good contact, even on a loose strap | Can be uncomfortable; more complex to print |

Whichever you choose, apply three rules:

1. **The sensor must reach the skin**, or the window's inner face, with no air gap. Set the sensor's height in CAD and check it in a section (E2).
2. **Keep light out at the edges.** An opaque rim around the sensor, pressed into the skin, blocks light from the side. Print the base in an opaque colour; thin light-coloured plastic can pass light.
3. **Line the window up with the sensor, not the module.** The module is much bigger than the sensor on it.

<!-- REFPRODUCT:START -->
esp_watch makes rule 3 easy. Its MAX30102 footprint marks the sensor package itself, **5.6 × 3.3 mm**, on the board's `User.Drawings` layer, specifically so that the enclosure window can be lined up with it. Imported into CAD with the board (E2), that rectangle shows exactly where the window must go, rather than the centre of the 21 × 16 mm module.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — the chosen base-window design (open cut-out, clear insert or other) is not recorded in REFERENCE-PRODUCT.md -->

### Worked Example: How Far Does the Sensor Sit From the Skin?

The sensor sits on the underside of the board. The case base sits below it. Will the sensor reach the skin?

**Assumption:** an open cut-out design. **Example values** for the heights, to show the method.

**Step 1: List the stack from the board's underside downwards.**

```text
Board underside                          0.0 mm  (reference)
Module header height below the board     2.5 mm  (example)
Module PCB thickness                     1.6 mm  (example)
Sensor package height                    1.55 mm (MAX30102 datasheet)
──────────────────────────────────────────────
Sensor face below the board              5.65 mm
```

The package height, 1.55 mm, comes from the datasheet [1]. The header and module values are examples; measure yours in CAD.

**Step 2: Where is the outside of the base?** From E0: clearance 0.5 mm plus base thickness 1.5 mm below the lowest part. If the lowest part is the sensor module, the outside of the base is 2.0 mm below the sensor face.

**Step 3: Compare.** With a cut-out, the sensor face is 2.0 mm *inside* the base. On the wrist, skin will not push 2 mm into a 5.6 × 3.3 mm hole.

**Step 4: Fix it.** Raise the sensor to the outer surface: reduce the clearance under the module, make the base thinner around the window (a local pocket), or add a raised rim so the skin is pressed towards the sensor. Aim for the sensor face to sit flush with, or up to about 0.5 mm proud of, the outer surface.

**Check.** A section through the sensor in CAD should show the sensor face at the outer surface of the base, with an opaque rim around it. If there is air between the sensor and where the skin will be, the requirement "heart rate within ±5 bpm, wearer sitting still" (A0) is already at risk, however good the firmware is.

<!-- MEDIA
type: diagram
id: E4-01
caption: Section through the base: a sensor set back in a cut-out, and the same sensor brought flush with an opaque rim
brief: Two side-by-side cross-sections through the watch base and the heart-rate module,
  with skin drawn as a curved surface below. Left, labelled "set back 2 mm": the sensor
  sits inside the cut-out with a visible air gap to the skin, and yellow arrows show
  ambient light entering from the sides. Right, labelled "flush with rim": the base is
  locally thinned, the sensor face is level with the outer surface, an opaque rim
  presses into the skin, and the side-light arrows are blocked. Label the sensor, module,
  header, board, base and skin. Clean line drawing.
-->

> **Try it: Section your sensor.** Open your E2 assembly and cut a section through the centre of your optical sensor, or whichever part must touch the body.
> 1. **Predict.** How far from the outer surface is its face?
> 2. **Do.** Measure it. Then change the geometry around the window, preferably through parameters, until it sits flush or slightly proud.
> 3. **Explain.** Which change did you make: thinner base, less clearance, or a raised rim? What did it cost in strength or comfort?

---

## 2. Strap Lugs

**Lugs** are the features that hold the strap. A strap pulls on them every time the wearer moves, and hard when it snags on something. The lug is where a printed case is most likely to break, because the force pulls across the printed layers.

Design rules for printed lugs:

- **Orient the print so the lug is not snapped across its layers.** A lug that sticks out sideways from a case printed floor-down has its layers stacked across the direction of pull. Test the direction, or make the lugs thicker.
- **Use solid lugs.** Set more perimeters or 100% infill in that region.
- **Round the inside corners** where the lug meets the case (E3), to spread the stress.
- **Use standard hardware.** Watch straps commonly use spring bars between the lugs, in standard widths. Choose the strap first, then design the lug gap and hole to its spring bar.

> **Teaching model.** The load on a lug depends on the strap, the wearer and the accident. For a design exercise, it is enough to ask: if the strap is pulled hard, which part breaks first, and is it a part that is cheap to replace? A strap that tears is better than a case that cracks.

<!-- REFPRODUCT:START -->
esp_watch's strap attachment is not recorded yet. The case is a 38 × 38 mm board inside roughly 42 × 42 mm of plastic, so lugs on two opposite sides are the natural place, away from the USB-C opening on the left.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — strap attachment method and lug design are not recorded in REFERENCE-PRODUCT.md -->

---

## 3. The Battery Bay

A lithium-polymer **pouch cell** has no rigid case. The Battery University reference on pouch cells makes three points directly relevant to the bay [2]: the cell needs support from its compartment, because it has no metal can; some swelling can occur, so the compartment must allow for expansion; and the compartment must protect the cell from mechanical stress and have no sharp edges. MIT's lithium battery safety guidance adds the plain rule: never puncture or crush a cell, and do not use one that has become puffy [3].

Turn those into design rules:

| Rule | Design feature |
|---|---|
| Hold the cell so it cannot move | A pocket or ribs that locate it on all sides |
| Do not press on it | A small gap around it; nothing clamping its faces |
| Leave room to swell | Extra space on its thick faces |
| No sharp edges or screw points near it | Round the pocket edges; keep screws and inserts away |
| Protect it from the board | No pins, solder joints or component legs touching the pouch |
| Keep the wires from being pinched | A route for the leads to the board |

<!-- REFPRODUCT:START -->
esp_watch stands its cell **vertically in a slot behind the display's header**, a face about 38 × 14 mm, to use height the electronics stack already claims (C0). The **placeholder** cell is about 20 × 5 × 13 mm. The slot needs a gap on the cell's two large faces to allow for swelling, and nothing sharp on either side: the header pins of the display module are exactly the kind of feature that must not touch the pouch.
<!-- REFPRODUCT:END -->

### Worked Example: Sizing the Slot

**Step 1: Start from the cell.** Placeholder: 20 mm long, 5 mm thick, 13 mm tall.

**Step 2: Add clearance and swelling allowance.** **Example values:** 0.3 mm fit clearance on every side (from your E3 clearance test), plus an extra 0.5 mm swelling allowance on each large face.

```text
Slot length    = 20 + 2 × 0.3               = 20.6 mm
Slot thickness =  5 + 2 × 0.3 + 2 × 0.5     =  6.6 mm
Slot height    = 13 + 0.3 (top gap)         = 13.3 mm
```

**Step 3: Check the space.** A 6.6 mm-thick slot must fit between the display header and the case wall, and 13.3 mm must fit under the lid. Check both in a E2 section.

**Check.** If the slot does not fit, do not squeeze the swelling allowance to zero. Either choose a thinner cell, and recalculate battery life from B3, or rearrange. The allowance values above are illustrative; the principle, that a pouch cell needs room and must never be clamped, is not.

> **Try it: Find what could touch the cell.** In your assembly, hide everything except the battery and the parts within 2 mm of it.
> 1. **Predict.** Which features are closest to the pouch?
> 2. **Do.** Measure the gap to each: header pins, screws, inserts, board edges, component legs.
> 3. **Explain.** Which, if any, could press on or cut into the pouch if the case were squeezed or the cell swelled? What would you change?

<!-- MEDIA
type: screenshot
id: E4-02
caption: The battery slot in section, with the swelling gap and the nearest sharp feature measured
brief: Autodesk Fusion section view through the battery slot of a watch enclosure. The
  cell (a simple box of the placeholder size) stands vertically in its slot. Dimensions
  shown: clearance gaps on each side, the swelling allowance on the large faces, and the
  distance from the cell to the nearest header pins. The pins are highlighted in orange
  as the nearest sharp feature. Slot edges visibly rounded.
-->

---

## 4. Buttons Through a Wall

A button on the board sits behind the case wall, so the wearer presses a **plunger** or a **flexible tab** in the case, which in turn presses the button. Three things decide whether it feels right:

- **Travel.** The plunger must move far enough to press the switch fully, and no further. Leave the switch's own travel, plus a little, between the plunger and the switch.
- **Retention.** The plunger must not fall out of the case or into it. A small flange inside the wall stops it.
- **Support behind the switch.** Pressing a button pushes the board. On a wrist, it pushes the whole watch into the wearer. Support the board directly behind the button with a boss or rib, and put side buttons where the other hand can pinch the watch while pressing.

<!-- REFPRODUCT:START -->
esp_watch's two buttons and slide switch are on the top face, and the lid has an opening for each. A slide switch needs an opening as long as its full travel, plus room for a fingertip or fingernail, at both ends.
<!-- REFPRODUCT:END -->

---

## 5. Charge Port and Sweat

### Charge-Port Access

E2 sized the opening for the plug. Here the question is *where* it is: on a side, away from the skin, where sweat does not run into it, and where the wearer can plug in without removing the strap.

<!-- REFPRODUCT:START -->
esp_watch's USB-C port faces the **left side** of the case. That keeps it off the skin, but it is also an open hole in the wall, and the easiest way in for sweat and dust.
<!-- REFPRODUCT:END -->

### Keeping Sweat Out

Sweat is salty and conductive, and a wrist device sees it every day. Writing down a *target* for how much it must keep out shapes the design. (Commercial products state this as an **IP rating**, which must be earned by passing formal tests [4]; a student prototype does not claim one.)

| Target | What the design would need |
|---|---|
| "Keep sweat off the electronics" | Openings away from the skin; a lip or channel so sweat runs off rather than in; a coating on the board |
| "Survive splashes and rain" | Seals on the lid joint, button membranes, a cover or seal over the USB-C port |
| "Survive immersion" | Moulded case, gaskets, sealed buttons, a sealed or wireless charging port: beyond a printed version 1 |

FDM prints are not naturally watertight: water can creep between layers and through tiny gaps in the walls. That is a strong reason to set a modest target for version 1 and record the rest as version 2 work, exactly as A0's out-of-scope list suggested.

<!-- FACT:VERIFY esp_watch — sweat and ingress protection measures are not recorded in REFERENCE-PRODUCT.md -->

---

## Tracing Every Feature to a Requirement

The deliverable asks for reasoning, not just geometry. For each wearable feature, write one line linking it to A0:

<!-- REFPRODUCT:START -->
| Feature | Requirement it serves (A0) | Design decision | Checked by |
|---|---|---|---|
| Sensor window | Heart-rate accuracy, wearer still | Sensor face flush with base; opaque rim; aligned to the 5.6 × 3.3 mm mark | Section in CAD |
| Battery slot | Safety; battery life | Cell stood on end; gaps and swelling allowance; no sharp features nearby | Section and proximity measurement |
| Lugs | Survive knocks and snags | Solid lugs, rounded roots, standard spring bars | Print orientation review |
| Buttons | Buttons usable with one hand | Plungers with set travel; board supported behind | Section in CAD |
| USB-C opening | Charge from a phone charger | Left side, away from skin, sized for the plug | E2 plug travel check |
| Sweat | Water-resistance target | Target set to "splash"; openings away from skin | Written target and review |
<!-- REFPRODUCT:END -->

---

# Putting It All Together

## Applying What You Have Learned

**1. Design the sensor window.** Choose cut-out, insert or boss, with a reason. Bring the sensor face flush or slightly proud, and add an opaque rim. Check in section.

**2. Design the lugs** for a strap you have chosen, oriented and reinforced for printing.

**3. Size the battery bay** with clearance and swelling allowance, and check nothing sharp is near the cell.

**4. Design the buttons** with travel, retention and support behind the switch.

**5. Set a sweat target** and design to it, recording what is left for version 2.

**6. Write the traceability table**, one row per feature.

**Deliverable:** your revised enclosure, with the sensor-window and battery-bay reasoning and the traceability table saved in your design pack as `E4-functional-design.md`.

## Self-Check

Open your revised enclosure and `E4-functional-design.md` and answer each item Y or N.

1. A section shows the sensor face flush with, or slightly proud of, the outer surface. — Y/N
2. The sensor window is aligned to the sensor itself, not the module. — Y/N
3. An opaque rim surrounds the sensor window. — Y/N
4. The battery bay has clearance on every side and a swelling allowance on its large faces. — Y/N
5. No sharp feature is within your chosen clearance of the battery. — Y/N
6. Lugs are designed for a named strap and its spring bar. — Y/N
7. Each button has set travel and support behind it. — Y/N
8. A written sweat target exists, with what is deferred to version 2. — Y/N
9. Every wearable feature traces to an A0 requirement in the table. — Y/N

---

## Check Your Understanding

**1.** An optical sensor sits 2 mm inside a cut-out in the case base. Readings are noisy outdoors and fine indoors. What is the most likely cause?

- A. The firmware filter is too weak.
- B. Outside light is leaking into the gap between the sensor and the skin; the sensor's light rejection works well only when it is pressed against skin.
- C. The I²C bus is too slow.
- D. The sensor is broken.

<details>
<summary>Answer</summary>

**B.** The datasheet's ambient light figure is measured with a finger on the sensor. A gap lets sunlight in from the sides, which is why it only fails outdoors. **A** treats a mechanical problem in software. **C** is unrelated. **D** is unlikely when it works indoors.

</details>

**2.** Which battery bay design is safest for a pouch cell?

- A. A tight pocket that clamps the cell flat so it cannot move.
- B. A pocket that locates the cell on all sides with a small gap, room to swell, rounded edges and nothing sharp nearby.
- C. No pocket; the cell rests on the board.
- D. A pocket with a screw through the middle to hold it.

<details>
<summary>Answer</summary>

**B.** It follows every rule: located, not pressed, room to swell, nothing sharp. **A** clamps a cell that may swell. **C** lets it move and rest on component legs. **D** risks puncture, which is dangerous.

</details>

**3.** Pressing a side button makes the whole watch dig into the wrist. What is the best fix?

- A. Use a stronger spring in the button.
- B. Support the board directly behind the switch, and place the button where the wearer can pinch the watch while pressing.
- C. Remove the button.
- D. Make the case heavier.

<details>
<summary>Answer</summary>

**B.** The force should go into the case and the wearer's opposing finger, not through the board into the wrist. **A** makes pressing harder. **C** drops a requirement. **D** does not stop the push.

</details>

**4.** Why is a printed lug most likely to fail when the strap is pulled?

- A. Printed plastic is always weaker than moulded plastic.
- B. The pull often runs across the printed layers, which is the weakest direction for an FDM part.
- C. Lugs are too small to print.
- D. The spring bar is too strong.

<details>
<summary>Answer</summary>

**B.** FDM parts are weakest between layers, so orientation and reinforcement matter most at the lugs. **A** is a generalisation that ignores direction. **C** is not true at watch sizes. **D** is not the cause.

</details>

**5.** A printed watch has a tight lid, but the board corrodes after a week of daily wear. Where is sweat most likely getting in?

- A. Nowhere; corrosion comes from the battery.
- B. Through the open USB-C port and between the printed layers, neither of which a tight lid seals.
- C. Through the display glass.
- D. Only through the strap.

<details>
<summary>Answer</summary>

**B.** An open port and porous FDM walls are the obvious leak paths; a tight lid seals only the lid joint. **A** ignores the salty, conductive sweat. **C** is sealed by the display itself. **D** is outside the case.

</details>

---

## What You Can Now Do, and What Comes Next

- Present an optical sensor to the skin and keep outside light away from it.
- Design lugs, buttons and openings that survive use on a body.
- Hold a pouch cell safely, with room to swell and nothing sharp nearby.
- Set a realistic sweat target, and trace every feature to a requirement.

The idea to carry forward: **every wearable feature serves a requirement, and the body is part of the design.** If a feature cannot name its requirement, question it; if a requirement has no feature, it is at risk.

In [E5 — Slicing and Printability](E5-slicing-and-printability.md) you will prepare the enclosure for printing, read the slicer's preview for problems, and get a time and material estimate, without printing anything.

---

## References

1. Analog Devices. *MAX30102 datasheet* (DC ambient light rejection of 2 counts with a finger on the sensor under direct sunlight, 100k lux; package 5.6 × 3.3 × 1.55 mm with integrated cover glass). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
2. Battery University. *Pouch Cell: Small but not Trouble Free* (the cell needs support in its compartment; allow for some expansion; protect from mechanical stress; no sharp edges). https://www.batteryuniversity.com/article/pouch-cell-small-but-not-trouble-free/
3. MIT Environment, Health and Safety Office. *Lithium-Ion Battery Safety Guidance* (never puncture or crush cells; do not use damaged or puffy batteries). https://ehs.mit.edu/wp-content/uploads/2019/09/Lithium_Battery_Safety_Guidance.pdf
4. International Electrotechnical Commission. *Ingress Protection (IP) ratings*. https://www.iec.ch/ip-ratings

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
