# E1 — Materials, Colour and Rendering
## Choosing What the Case Is Made Of, What It Looks Like, and How You Show It

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Mechanical and 3D Design
**Time:** ~1 hour · **You will produce:** a material choice justified against your A0 spec, and one presentation image of your coloured enclosure

---

### The Case That Sagged in the Car

A student prints a watch case in PLA, because PLA is what the lab printer had loaded. It fits, and it survives a week of wear. Then the owner leaves it on the dashboard of a parked car on a May afternoon. By evening the lid has slumped and the interference fit has gone loose.

Nothing in the CAD model was wrong. The material was never chosen; it came with the spool on the printer. Your E0 model now has a shape. This unit decides what plastic it is printed in, what colour and finish it has, and how you show it in one image to someone who has never seen your project.

### What You Will Be Able to Do After This Reading

- **Compare** PLA, PETG, ABS and TPU on stiffness, layer adhesion, heat tolerance and printability.
- **Select** an enclosure material by testing each candidate against your A0 requirements, and **justify** the choice in writing.
- **Choose** a colour and finish for stated reasons: visibility, how it photographs, and what it shows about the print.
- **Produce** a presentation image of the coloured model in Fusion, with a deliberate camera angle, and know when a render is worth making.

---

## Four Filaments, Four Questions

Filament listings call almost everything "strong" and "easy to print". Ask four questions instead:

1. **Stiffness.** Does the case keep its shape when the lid is pressed on and the strap pulls on a lug?
2. **Layer adhesion.** An FDM part is weakest between layers (E3). How well do this material's layers bond, and how does it break?
3. **Heat tolerance.** When does it start to soften? A wrist is only at body temperature, but a watch is also left in the sun and in cars.
4. **Printability.** Can your printer, or the print service you will use, print it without special equipment?

The table follows Prusa's material guides [1][2][3][4].

| | PLA | PETG | ABS | TPU |
|---|---|---|---|---|
| **Stiffness** | Stiff, but brittle | Tough; bends a little before breaking | Tough | Flexible, rubber-like |
| **Layer adhesion** | Weaker than the others; breaks along layers or into shards | Very good | Good | Very good |
| **Heat tolerance** | Softens and deforms above about 60 °C [1] | Suitable below about 80 °C [2] | Good high-temperature resistance [3] | Not a concern at wrist temperature |
| **Printability** | Easiest; little warping | Easy; strings, and bridges and overhangs are poor | Hard: warps, needs an enclosed printer, gives off styrene fumes | Hard: slow (about 20 mm/s), clogs, tangles in the extruder |
| **Typical wearable use** | Prototypes, fit checks | Cases | Cases, with an enclosed printer | Straps, button covers, gaskets |

<!-- FACT:VERIFY ABS softening temperature — Prusa's ABS guide gives no figure; get heat deflection or Vicat temperature from a manufacturer TDS before quoting a number -->

**PLA's heat limit is lower than it sounds.** No wrist reaches 60 °C, but a car parked in the sun does inside, and its dashboard gets hotter still.

<!-- FACT:VERIFY parked-car cabin air and dashboard temperatures in Indian summer — studies elsewhere report about 70 °C air and close to 100 °C on the dashboard; find a citable source -->
<!-- SOURCE for the cabin-temperature rise: McLaren, Null and Quinn, "Heat Stress From Enclosed Vehicles", Pediatrics 116(1), e109 (2005), https://doi.org/10.1542/peds.2004-2368. The dashboard figure still needs its own source. -->

**TPU is too flexible for a case**, but right for the parts that bend: a strap, a button cover, a gasket.

> **Teaching model.** These are generic descriptions. Brands and additives differ, so for a real product read the technical data sheet (TDS) of the exact filament you will buy.

**Skin contact.** No filament is automatically "skin-safe" as printed. If your case touches skin, record what that filament's data sheet says, and claim nothing more.

<!-- FACT:VERIFY whether any common Indian-market PETG or PLA brand publishes a skin-contact statement — check before naming one -->

**Cost barely decides it.** A watch case uses about 13 g of filament, around ₹11 of PLA (E5); other materials change that by a few rupees.

---

## Worked Example: Choosing the Case Material Against the Spec

Eliminate first, then rank.

**Step 1: List the requirements the material affects.** From an example A0 spec:

| ID | Requirement (example values) | What it asks of the material |
|---|---|---|
| NFR-08 | The case shall not deform after 1 h in a parked car in summer. *Check:* analysis against the data sheet. | Heat tolerance above the car's temperature |
| NFR-09 | The lid shall stay on through 200 removals. *Check:* test after build. | Stiff enough to hold an interference fit, tough enough not to crack |
| NFR-10 | The case shall be printable on the college lab's open-frame printer. *Check:* inspection. | No enclosure needed |
| FR-11 | The heart-rate sensor shall read the wrist with outside light blocked. *Check:* test after build. | Opaque base (E4) |

**Step 2: Eliminate on hard limits.**

```text
Candidate   NFR-08 heat    NFR-10 open printer   NFR-09 lid fit         Result
─────────   ───────────    ───────────────────   ────────────────────   ──────────────
PLA         ✗ ~60 °C       ✓                     ✗ brittle, may crack   out
PETG        ? ~80 °C       ✓                     ✓ tough                keep
ABS         ✓              ✗ needs enclosure     ✓                      out (this lab)
TPU         —              ✓                     ✗ too flexible         out (as case)
```

**Step 3: Resolve the "?".** About 80 °C is above a hot car's air but below a sunlit dashboard. So PETG passes NFR-08 if the watch is left *in* the car and fails if it is left *on the dashboard*, and the requirement does not say which. Either tighten the wording, or accept that the only candidate meeting the harsher version is ABS, which fails NFR-10.

**Step 4: Write the decision.**

> *Material: PETG for the case and lid, TPU for the strap. PLA is rejected because it softens at about 60 °C (NFR-08) and is brittle under the interference fit (NFR-09). ABS is rejected because the lab printer is open-frame (NFR-10). NFR-08 is reworded to "inside a parked car, out of direct sun", since nothing that meets NFR-10 survives a sunlit dashboard. Base in black PETG to block light (FR-11).*

**Check.** Every rejection names the requirement it failed, and the requirement no candidate met was changed in writing, as in the C0 concept decision.

<!-- REFPRODUCT:START -->
esp_watch's enclosure will be printed in **black PLA**. PLA is stiff, cheap and easy to print, and black is opaque, which helps keep outside light away from the heart-rate sensor. Its weak points for a wearable are heat (a watch left in a hot car) and brittleness, which matters for the **interference-fit lid** that is pressed on and off. Both are worth testing on the first print.
<!-- REFPRODUCT:END -->

---

## Colour and Finish Are Design Decisions

**Can it be seen?** A bright case stands out on a wrist, which the wearer may or may not want. A dark bezel makes an OLED look sharper, because the screen's black background blends into it. A dark case in the sun also runs hotter.

**How does it photograph?** Pure black loses its edges; pure white overexposes and shows every layer line. Mid-tones such as grey show the shape best.

**What does the finish show about the print?**

| Finish | Effect on a printed part |
|---|---|
| **Matte** | Hides layer lines; looks less like a print |
| **Glossy or "silk"** | Catches light on every layer line, making them more visible |
| **Translucent** | Shows the infill, internal walls and anything inside, and lets light through |

On the sensor side of a wearable, letting light through is a fault: E4 explains why that base must be opaque.

<!-- MEDIA
type: photo
id: E1-01
caption: The same small test box printed in four finishes: matte grey, silk white, translucent and matte black
brief: Four identical 30 × 30 × 15 mm printed boxes with 1.5 mm walls, side by side on a plain
  mid-grey card background, photographed from about 30° above horizontal under one soft light
  from the upper left. Left to right: matte grey, silk (glossy) white, translucent natural with
  infill and inner walls visible through the side, matte black. Layer lines clearly visible on
  the silk box and hard to see on the matte grey; the black box's edges fading into shadow.
  Small printed labels under each: "matte grey", "silk", "translucent", "matte black". Sharp
  focus on all four.
-->

---

## Making the Presentation Image

The Design Pack needs one image of the enclosure on its first page, answering at a glance: what is it, which way up is it worn, and how big is it? A **screenshot of the coloured model**, taken in Fusion's Design workspace, is enough for that. A **render**, a photograph-like image Fusion calculates from the model, lighting and camera, is only worth the extra time when you need a good-looking image, for a pitch or a poster.

### Appearance is not material

Fusion keeps two settings on each body [5]. A **physical material** sets engineering properties such as density, which Fusion uses to calculate mass. An **appearance** changes only how the body looks and overrides the material's colour. Set both, so Inspect, Properties gives a realistic mass for your C0 weight constraint.

### The coloured screenshot, in five steps

All of this happens in the Design workspace, where you built the case in E0.

1. **Set the physical material.** **Modify → Physical Material**, and drag a plastic (for example ABS or a generic plastic close to your choice) onto each body.
2. **Set the appearance.** **Modify → Appearance** (**A**), and drag a plastic in your chosen colour onto each body [7]. Use a second appearance for anything visibly different, such as a TPU strap.
3. **Tidy the view.** In the browser, click the eye (or light bulb) icon to hide sketches, construction planes and the origin. In the navigation bar, open **Display Settings**: set **Visual Style** to **Shaded**, choose a plain light **Environment**, and set **Camera** to **Orthographic**.
4. **Frame the view** as described below, and save it as a named view so you can return to it after changes.
5. **Capture.** **File → Capture Image**, choose a size, and save it as `E1-image.png`.

An **orthographic** camera has no perspective at all, so the case's thickness looks exactly as it is. That is the honest choice for a design image.

<!-- MEDIA
type: screenshot
id: E1-02
caption: The coloured case in Fusion's Design workspace, ready to capture
brief: Autodesk Fusion, Design workspace, light theme. Canvas shows a simple two-part watch
  enclosure (about 42 × 43 × 18 mm, rounded corners, display window and two button holes in
  the lid) with a mid-grey matte plastic appearance, three-quarter view from above,
  orthographic camera, sketches and origin hidden. The Appearance dialog open on the right,
  and the navigation bar's Display Settings menu open showing Camera set to Orthographic.
  Red boxes around Modify → Appearance and Display Settings.
-->

### Camera angle

```text
   side view                                  top view

   camera ●                                   ┌──────────┐
           ╲  ~30° above the table            │  watch   │
            ╲     ┌──────────┐                └──────────┘
             ╲──► │  watch   │                           ╲
   ────────────── └──────────┘ ── ground                  ● camera, turned 30–45°
                                                            so a corner faces it
```

A **three-quarter view**, looking down at about 30° with a corner towards the camera, shows the display, the buttons, the thickness and a side opening in one image. Straight-on views hide the thickness or the display.

**Show the scale.** A simple strap, or a wrist-sized cylinder beneath the watch, tells the reader the size at once.

### When You Need a Render

For a pitch or a poster, a render looks more like a product photograph: soft shadows, reflections, a studio background. Use the **Render** workspace [6]:

1. **Switch** the workspace from Design to **Render**. The appearances you set carry over.
2. **Set the scene** in **Setup → Scene Settings** [8]: a studio environment, a light grey Solid Color background, Ground Plane on so the watch casts a shadow, Reflections off, and a Perspective camera.
3. **Frame the camera** with the same three-quarter view.
4. **Render.** Turn on **In-canvas render** and use **Capture Image**; its size is fixed by your screen [9]. For a set resolution, use the **Render** command with the local renderer. The cloud renderer uses tokens [9], and you do not need it.

**Use a longer focal length.** A render uses a perspective camera. A short, wide-angle lens close to a small object exaggerates perspective, so the nearest corner bloats and a thin watch looks like a brick. A longer lens, around 90 mm as in the Fusion tutorial [6], with the camera further back, removes this.

> **Try it: Lens test.** Only if you make a render. Set up the three-quarter view of your enclosure in the Render workspace.
> 1. **Predict.** How will the case's thickness look at a 20 mm focal length compared with 90 mm?
> 2. **Do.** Capture the in-canvas render at both, moving the camera back at 90 mm to fill the frame.
> 3. **Explain.** Which looks more like the watch held in your hand? Which is more honest about thickness?

### An honest image

A screenshot or render shows a finish your printer cannot make: no layer lines, a smooth coat. Say so in the caption, for example "PETG case design in Fusion; the printed part will show layer lines", so a reviewer who later sees the print is not misled.

<!-- REFPRODUCT:START -->
esp_watch's enclosure was modelled in Onshape (E0), and its enclosure images are placeholders for now. The camera and caption rules above apply in any CAD tool.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/enclosure-*.png -->
<!-- PLACEHOLDER:ASSET presentation image (coloured-model screenshot) of the esp_watch enclosure (black PLA) — not made yet; author to add -->

<!-- MEDIA
type: diagram
id: E1-03
caption: The same case captured two ways: a careless view, and the finished presentation image
brief: Two Fusion images of the same simple watch enclosure (about 42 × 43 × 18 mm, mid-grey
  matte plastic, display window and two button holes in the lid, black strap) side by side at
  equal size. Left, labelled "before": camera almost straight down, perspective camera close
  in, sketches and origin still showing, near corner visibly distorted, thickness invisible.
  Right, labelled "after": orthographic camera, three-quarter view about 30° above and turned
  35°, plain light background, sketches and origin hidden, left-side USB-C opening visible,
  and a caption strip below reading "PLA case design in Fusion; the printed part will show
  layer lines."
-->

---

# Putting It All Together

## Applying What You Have Learned

**1. Decide.** List every A0 requirement the case material affects. If none is about temperature, add one with a check method. Run the elimination table for your product and write the decision as in the worked example.

**2. Present.** Write one reason each for your colour and finish. Set the physical material and appearances in Fusion, then capture one presentation image of the coloured model with an honest caption. Render it only if you need a polished image.

**Deliverable:** `E1-material.md` in your Design Pack, with the elimination table, the written decision and the colour and finish reasons; plus `E1-image.png` with its caption.

## Self-Check

Open `E1-material.md` and `E1-image.png` and answer each item Y or N.

1. Every requirement in the elimination table has an A0 ID. — Y/N
2. The spec contains a temperature requirement with a check method. — Y/N
3. Every rejected material names the requirement it failed. — Y/N
4. Any requirement no candidate met is reworded in A0, with the reason written. — Y/N
5. The colour and the finish each have a written reason. — Y/N
6. If the case touches skin, the file states what the filament's data sheet says. — Y/N
7. The image is a three-quarter view showing the display face, at least one side and something that shows scale. — Y/N
8. The caption says it is a CAD image and how the printed part will differ. — Y/N

---

## Check Your Understanding

**1.** A case must hold an interference-fit lid that the user removes to change the battery. The team chooses PLA because it is the stiffest. What is the main risk?

- A. PLA is too flexible to hold the lid.
- B. PLA is brittle, so repeatedly pressing the lid on and off can crack it, often along a layer.
- C. PLA cannot be printed on an open-frame printer.
- D. PLA costs much more than PETG.

<details>
<summary>Answer</summary>

**B.** Stiffness is not toughness. PLA is stiff but brittle, with weaker layer adhesion, so a repeatedly strained fit is where it fails. **A** describes TPU, not PLA. **C** is wrong: PLA is the easiest material on an open printer. **D** is wrong: a case's filament costs a few rupees in any of these.

</details>

**2.** A spec says "The case shall survive being left in a parked car." PETG is suitable below about 80 °C. What is the best next step?

- A. Choose PETG, because 80 °C is far above body temperature.
- B. Choose TPU, because it does not soften at wrist temperature.
- C. Make the requirement say whether the watch is inside the car or on a sunlit dashboard, because PETG's answer depends on which.
- D. Drop the requirement, since nobody will test a student project in a car.

<details>
<summary>Answer</summary>

**C.** Cabin air and a sunlit dashboard are very different temperatures, and PETG sits between them. **A** compares against the wrong condition. **B** confuses flexibility with heat resistance, and TPU cannot hold a case's shape. **D** removes a real use condition instead of making it checkable.

</details>

**3.** The base under an optical heart-rate sensor is printed in translucent white PETG because it "looks technical". What is the likely effect?

- A. None, because the sensor has its own light source.
- B. Outside light passes through the plastic around the sensor and adds noise to its signal.
- C. The base will warp more than an opaque one.
- D. The render will take longer.

<details>
<summary>Answer</summary>

**B.** Light through the base reaches the photodiode, which is what E4's opaque-rim rule prevents. **A** is wrong: the sensor's own light is the signal and extra light is noise. **C** is not a property of colour. **D** is irrelevant to whether the product works.

</details>

**4.** A render (perspective camera) of a 42 mm watch looks chunky, with the nearest corner far larger than the others. What is the most likely cause?

- A. The appearance is glossy.
- B. The ground plane is on.
- C. A short, wide-angle focal length with the camera close to the object.
- D. The physical material is set wrongly.

<details>
<summary>Answer</summary>

**C.** A wide lens close to a small object exaggerates perspective; a longer lens further back removes it, and an orthographic screenshot has no perspective at all. **A** and **B** change reflections and shadows, not proportions. **D** affects mass, not the image.

</details>

**5.** A student sets a red appearance on the case but leaves the physical material as steel. What goes wrong?

- A. The model shows steel instead of red.
- B. The case looks right, but Inspect, Properties reports a mass several times too high, so the weight check is wrong.
- C. Nothing, because appearance and physical material are the same setting.
- D. The Appearance dialog will not open.

<details>
<summary>Answer</summary>

**B.** The appearance overrides only the look; mass comes from the physical material, and steel is far denser than any printed plastic. **A** is wrong because the appearance does override the colour. **C** is wrong: Fusion keeps them separate. **D** is not a real effect.

</details>

---

## What Comes Next

In [E2 — PCB ↔ Enclosure Co-Design](E2-pcb-enclosure-co-design.md) you will bring the real board model into the case and check that everything fits.

---

## References

1. Prusa Research. *PLA*, Prusa Knowledge Base. https://help.prusa3d.com/article/pla_2062
2. Prusa Research. *PETG*, Prusa Knowledge Base. https://help.prusa3d.com/article/petg_2059
3. Prusa Research. *ABS*, Prusa Knowledge Base. https://help.prusa3d.com/article/abs_2058
4. Prusa Research. *Flexible materials*, Prusa Knowledge Base. https://help.prusa3d.com/article/flexible-materials_2057
5. Autodesk. *Physical materials and appearances*, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/GUID-55EC2C42-60E1-48C7-B802-D2AA7AB6F0CB.htm
6. Autodesk. *Tutorial: Rendering a design*, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Render/files/GUID-834C5728-53CA-41BA-AF07-2DC992A568AD.htm
7. Autodesk. *Apply appearances to components, bodies, and faces in a design*, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/GUID-D59206EC-875D-4890-8088-AD23E5364951.htm
8. Autodesk. *Set the lighting, background, and camera in your render*, Fusion Help. https://help.autodesk.com/view/fusion360/ENU/?contextId=RND-SCENE-SETTINGS
9. Autodesk. *Rendering in the cloud and locally*, Fusion Help. https://help.autodesk.com/cloudhelp/ENU/Fusion-Render/files/RND-RENDER-CLOUD-LOCAL.htm

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
