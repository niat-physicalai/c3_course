# D1b — Materials, Colour and Rendering
## Choosing What the Case Is Made Of, What It Looks Like, and How You Show It

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Mechanical and 3D Design
**Time:** ~1 hour · **You will produce:** a material choice justified against your A0 spec, and one rendered presentation image of your enclosure

---

### The Case That Sagged in the Car

A student prints a watch case in PLA, because PLA is what the lab printer had loaded. It fits, and it survives a week of wear. Then the owner leaves it on the dashboard of a parked car on a May afternoon. By evening the lid has slumped and the interference fit has gone loose.

Nothing in the CAD model was wrong. The material was never chosen; it came with the spool on the printer. Your D1 model now has a shape. This unit decides what plastic it is printed in, what colour and finish it has, and how you show it in one image to someone who has never seen your project.

### What You Will Be Able to Do After This Reading

- **Compare** PLA, PETG, ABS and TPU on stiffness, layer adhesion, heat tolerance and printability.
- **Select** an enclosure material by testing each candidate against your A0 requirements, and **justify** the choice in writing.
- **Choose** a colour and finish for stated reasons: visibility, how it photographs, and what it shows about the print.
- **Produce** a rendered presentation image in Fusion, with a deliberate camera angle, appearance and lighting.

### What Part 1 Already Covered

Part 1 did not cover materials or rendering. **What is new here** is treating the plastic, the colour and the presentation image as design decisions that trace back to your specification.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## Four Filaments, Four Questions

Filament listings call almost everything "strong" and "easy to print". Ask four questions instead:

1. **Stiffness.** Does the case keep its shape when the lid is pressed on and the strap pulls on a lug?
2. **Layer adhesion.** An FDM part is weakest between layers (D3). How well do this material's layers bond, and how does it break?
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
<!-- LINK:VERIFY  want: "peer-reviewed measurement of parked-car cabin and dashboard temperatures in summer sun"  search: "parked vehicle cabin temperature solar measurement study dashboard" -->

**TPU is too flexible for a case**, but right for the parts that bend: a strap, a button cover, a gasket.

> **Teaching model.** These are generic descriptions. Brands and additives differ, so for a real product read the technical data sheet (TDS) of the exact filament you will buy.

**Skin contact.** No filament is automatically "skin-safe" as printed. If your case touches skin, record what that filament's data sheet says, and claim nothing more.

<!-- FACT:VERIFY whether any common Indian-market PETG or PLA brand publishes a skin-contact statement — check before naming one -->

**Cost barely decides it.** A watch case uses about 13 g of filament, around ₹11 of PLA (D5); other materials change that by a few rupees.

---

## Worked Example: Choosing the Case Material Against the Spec

Eliminate first, then rank.

**Step 1: List the requirements the material affects.** From an example A0 spec:

| ID | Requirement (example values) | What it asks of the material |
|---|---|---|
| NFR-08 | The case shall not deform after 1 h in a parked car in summer. *Check:* analysis against the data sheet. | Heat tolerance above the car's temperature |
| NFR-09 | The lid shall stay on through 200 removals. *Check:* test after build. | Stiff enough to hold an interference fit, tough enough not to crack |
| NFR-10 | The case shall be printable on the college lab's open-frame printer. *Check:* inspection. | No enclosure needed |
| FR-11 | The heart-rate sensor shall read the wrist with outside light blocked. *Check:* test after build. | Opaque base (D4) |

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

**Check.** Every rejection names the requirement it failed, and the requirement no candidate met was changed in writing, as in the D0 concept decision.

<!-- REFPRODUCT:START -->
esp_watch's enclosure material and colour are not recorded. Its **interference-fit lid** needs a material tough enough to be pressed on and off without cracking, which points away from PLA for the finished case.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — enclosure material, filament brand and colour are not recorded in REFERENCE-PRODUCT.md -->

> **Try it: Move the product.** The same watch is now for a worker in a workshop that reaches 45 °C, near hot machinery.
> 1. **Predict.** Does PETG still win?
> 2. **Do.** Add a requirement for the new environment to Step 1, and redo the elimination.
> 3. **Explain.** Which candidates survive? If none does on an open printer, what would you change: the printer, the requirement or the product?
>
> **Extra challenge:** Look up ASA in Prusa's material guide. Does it change your answer?

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

On the sensor side of a wearable, letting light through is a fault: D4 explains why that base must be opaque.

<!-- MEDIA
type: photo
id: D1b-01
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

A **render** is a photograph-like image the CAD tool calculates from your model, materials, lighting and camera. The Design Pack needs one on its first page, answering at a glance: what is it, which way up is it worn, and how big is it?

### Appearance is not material

Fusion keeps two settings on each body [5]. A **physical material** sets engineering properties such as density, which Fusion uses to calculate mass. An **appearance** changes only how the body looks and overrides the material's colour. Set both, so Inspect, Properties gives a realistic mass for your D0 weight constraint.

### The five steps in Fusion

1. **Switch** the workspace from Design to **Render** [6].
2. **Apply appearances.** Open Setup, Appearance, and drag a plastic from the Library onto each body in the browser or canvas [7]. Use a second appearance for anything visibly different, such as a TPU strap.
3. **Set the scene** in Setup, Scene Settings [8]: a studio environment from the Environment Library, a light grey Solid Color background, Ground Plane on so the watch casts a shadow, Reflections off, and a Perspective camera.
4. **Frame the camera** as described below, and save it as a named view so you can return to it after changes.
5. **Render.** Turn on **In-canvas render** and use **Capture Image**; its size is fixed by your screen [9]. For a set resolution, use the **Render** command with the local renderer and a resolution preset [9]. The cloud renderer uses tokens [9], and you do not need it here.

<!-- MEDIA
type: screenshot
id: D1b-02
caption: Fusion's Render workspace with Scene Settings open and in-canvas rendering on
brief: Autodesk Fusion, Render workspace, light theme. Canvas shows a simple two-part watch
  enclosure (about 42 × 42 × 18 mm, rounded corners, display window and two button holes in
  the lid) in mid-grey matte plastic, three-quarter view from above, on a ground plane with a
  soft shadow, in-canvas render partly resolved. Scene Settings panel open on the right showing
  Background set to Solid Color (light grey), Ground Plane ticked, Reflections unticked, Camera
  set to Perspective with focal length about 90 mm. Red boxes around the Setup panel's
  Appearance and Scene Settings buttons and the In-canvas render toggle.
-->

### Camera angle and lens

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

**Use a longer focal length.** A short, wide-angle lens close to a small object exaggerates perspective, so the nearest corner bloats and a thin watch looks like a brick. A longer lens, around 90 mm as in the Fusion tutorial [6], with the camera further back, removes this.

**Show the scale.** A simple strap, or a wrist-sized cylinder beneath the watch, tells the reader the size at once.

> **Try it: Lens test.** Set up the three-quarter view of your enclosure.
> 1. **Predict.** How will the case's thickness look at a 20 mm focal length compared with 90 mm?
> 2. **Do.** Capture the in-canvas render at both, moving the camera back at 90 mm to fill the frame.
> 3. **Explain.** Which looks more like the watch held in your hand? Which is more honest about thickness?

### An honest render

A render shows a finish your printer cannot make: no layer lines, a smooth coat. Say so in the caption, for example "Render of the PETG case design; the printed part will show layer lines", so a reviewer who later sees the print is not misled.

<!-- REFPRODUCT:START -->
esp_watch's enclosure was modelled in Onshape (D1), and its enclosure images are placeholders for now. The camera, lens and caption rules above apply to any CAD tool's renderer.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/enclosure-*.png -->
<!-- FACT:VERIFY esp_watch — whether a rendered presentation image of the enclosure exists, and which tool made it, is not recorded in REFERENCE-PRODUCT.md -->

<!-- MEDIA
type: diagram
id: D1b-03
caption: The same case rendered two ways: a wide-angle top-down view, and the finished presentation image
brief: Two renders of the same simple watch enclosure (about 42 × 42 × 18 mm, mid-grey matte
  plastic, display window and two button holes in the lid, black strap) side by side at equal
  size. Left, labelled "before": 20 mm focal length, camera almost straight down, busy
  environment background, reflections on, near corner visibly distorted, thickness invisible.
  Right, labelled "after": 90 mm focal length, three-quarter view about 30° above and turned
  35°, light grey solid background, ground shadow, reflections off, left-side USB-C opening
  visible, and a caption strip below reading "Render of the PETG case design; the printed part
  will show layer lines."
-->

---

# Putting It All Together

## Applying What You Have Learned

**1. Recognise.** For each of PLA, PETG, ABS and TPU, name the one of the four questions it answers worst.

**2. Reproduce.** List every A0 requirement the case material affects. If there is no temperature requirement, add one with a check method.

**3. Decide.** Run the elimination table for your product and write the decision as in the worked example.

**4. Diagnose.** A classmate's render shows a glossy, translucent case from directly above with a 20 mm lens. Name three problems, including one with the finish for a heart-rate wearable.

**5. Design.** Write one reason each for your colour and finish. Set the physical material and appearances in Fusion, then render one presentation image with an honest caption.

**Deliverable:** `D1b-material.md` in your Design Pack, with the elimination table, the written decision and the colour and finish reasons; plus `D1b-render.png` with its caption.

## Self-Check

Open `D1b-material.md` and `D1b-render.png` and answer each item Y or N.

1. Every requirement in the elimination table has an A0 ID. — Y/N
2. The spec contains a temperature requirement with a check method. — Y/N
3. Every rejected material names the requirement it failed. — Y/N
4. Any requirement no candidate met is reworded in A0, with the reason written. — Y/N
5. The colour and the finish each have a written reason. — Y/N
6. If the case touches skin, the file states what the filament's data sheet says. — Y/N
7. The render is a three-quarter view showing the display face, at least one side and something that shows scale. — Y/N
8. The caption says it is a render and how the printed part will differ. — Y/N

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

**B.** Light through the base reaches the photodiode, which is what D4's opaque-rim rule prevents. **A** is wrong: the sensor's own light is the signal and extra light is noise. **C** is not a property of colour. **D** is irrelevant to whether the product works.

</details>

**4.** A render of a 42 mm watch looks chunky, with the nearest corner far larger than the others. What is the most likely cause?

- A. The appearance is glossy.
- B. The ground plane is on.
- C. A short, wide-angle focal length with the camera close to the object.
- D. The physical material is set wrongly.

<details>
<summary>Answer</summary>

**C.** A wide lens close to a small object exaggerates perspective; a longer lens further back removes it. **A** and **B** change reflections and shadows, not proportions. **D** affects mass, not the image.

</details>

**5.** A student sets a red appearance on the case but leaves the physical material as steel. What goes wrong?

- A. The render shows steel instead of red.
- B. The case looks right, but Inspect, Properties reports a mass several times too high, so the weight check is wrong.
- C. Nothing, because appearance and physical material are the same setting.
- D. The Render workspace will not open.

<details>
<summary>Answer</summary>

**B.** The appearance overrides only the look; mass comes from the physical material, and steel is far denser than any printed plastic. **A** is wrong because the appearance does override the colour. **C** is wrong: Fusion keeps them separate. **D** is not a real effect.

</details>

---

## What You Can Now Do, and What Comes Next

- Compare FDM materials on stiffness, layer adhesion, heat and printability rather than marketing claims.
- Choose a case material by eliminating candidates against your spec, with a reason for every rejection.
- Choose a colour and finish for visibility, photography and what they show about the print.
- Produce an honest presentation render with a deliberate camera, lens and scene.

The idea to carry forward: **material and finish are requirements for the print, not choices made at the printer.**

In [D2 — PCB ↔ Enclosure Co-Design](D2-pcb-enclosure-co-design.md) you will bring the real board model into the case and check that everything fits.

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
