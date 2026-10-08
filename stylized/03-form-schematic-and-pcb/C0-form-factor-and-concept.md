<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">C0 — Form Factor and Concept</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Deciding the Product's Shape Before Anyone Opens CAD</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 3 — Form Factor, Schematic and PCB <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> three annotated concept sketches, a chosen direction with its justification, and a board outline sketch for C3</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Perfect Board Facing the Wrong Way</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Imagine a circuit board that is beautifully routed, passes every design rule check and has every footprint verified, and whose heart-rate sensor points at the wearer's face instead of their wrist. Nothing in KiCad can catch that. The board is correct. The product is wrong, because nobody decided which way the board sits in the watch before the layout started.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For a wearable, the physical constraints come first. This unit settles them on paper, with quick sketches compared against your spec, before any CAD.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Identify</strong> the physical constraints a wearable must meet, and trace each to a requirement in your A0 spec.</li><li style="margin:6px 0;">​<strong>Calculate</strong> a thickness budget from the parts that stack up inside the product.</li><li style="margin:6px 0;">​<strong>Sketch</strong> at least three distinct concepts and annotate them with those constraints.</li><li style="margin:6px 0;">​<strong>Evaluate</strong> the concepts against your spec with a comparison matrix, and <strong>justify</strong> a chosen direction.</li><li style="margin:6px 0;">​<strong>Decide</strong> the orientation of every part that must face a particular way, such as a sensor against the skin.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Constraints a Wrist Imposes</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">List the physical constraints before sketching anything. For a wrist-worn device they come straight from A0's environment and requirements:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Constraint</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Question it answers</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Comes from</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Thickness</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How far above the wrist may it stand?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 size envelope</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Outline</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How wide and long can it be on a small wrist?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 size envelope</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Weight</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Will it stay comfortable all day?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 size envelope</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Skin-facing side</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Which face touches skin, and what must be on it?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 environment; sensing requirement</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Viewing side</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Which face does the wearer look at?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 display requirement</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Strap attachment</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Where do the strap forces go into the case?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 lifetime and impact</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Button reach</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Can a button be pressed with one hand, without pushing the watch into the wrist?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 use scenario</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charge access</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Where does the charger plug in, and is the opening away from skin and sweat?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 charging requirement</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sweat and water</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What must be sealed, and to what level?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A0 environment (IP target)</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A useful way to think about a wearable is as layers stacked from the wrist upwards. Each layer claims part of the thickness budget, and each face has a job:</div>

```text
          wearer's eyes
               ▲
   ┌───────────────────────┐   lid: window, button openings
   │ display               │
   │ modules and board     │   the electronics stack
   │ battery (beside, or   │
   │ underneath)           │
   │ sensor                │
   └───────────────────────┘   base: sensor window against the skin
               ▼
             wrist
```

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Orientation Is Decided Here</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Some parts only work facing one way. Decide their orientation now and write it down, because the board layout in C3 depends on it.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Part</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Must face</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Optical heart-rate sensor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The skin, pressed flat, with outside light blocked</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">It reads light scattered back from tissue (B0)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Display</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The wearer's eyes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">It must be seen</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Buttons</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Outwards or sideways, reachable by the other hand</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">They must be pressed without removing the watch</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charging port</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A side, away from the skin</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sweat and skin contact</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Antenna</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Away from the wrist, the battery and copper</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Body tissue, a metal-foil battery and copper all detune it (C3)</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch decides these as follows. The display, motion sensor, XIAO board, both buttons and the slide switch are on the <strong>top</strong> face. The MAX30102 heart-rate module is on the <strong>underside</strong>, so its sensor touches the wrist. The XIAO's USB-C port faces the <strong>left side</strong>. The external antenna is to be routed along the inside of the case, away from the battery. The enclosure's lid has four openings: one for the display, two for the buttons and one for the slide switch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Putting the sensor on the underside makes the board two-sided, and the case base must present the sensor to the skin through a window. The board outline is 37.8 × 39 mm, with four mounting holes: two at the top left and right, two in the middle.</div>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_back.png" alt="esp_watch board, underside: the heart-rate sensor module that must face the wrist" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch board, underside: the heart-rate sensor module that must face the wrist</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: The Thickness Budget</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Before sketching shapes, add up what must stack. This is the calculation that most often rules concepts out.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: The electronics stack.</strong> esp\_watch's board with its parts fitted is <strong>14.044 mm</strong> tall. The display sits on a female header above the motion-sensor module (a 4–5 mm air gap between them), and that stack sets the height.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: Add the case.</strong> <strong>Example values:</strong> a 3D-printed lid 1.5 mm thick and a base 1.5 mm thick, and 0.5 mm of clearance above and below the electronics so nothing is squeezed.</div>

```text
Electronics stack         14.044 mm
Clearance, top + bottom    1.0   mm   (0.5 + 0.5)
Lid                        1.5   mm
Base                       1.5   mm
──────────────────────────────────
Total                     18.0   mm  (rounded)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Compare with the requirement.</strong> A0's example size envelope allowed 16 mm including the case. The concept is about 2 mm over.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 4: Check the battery fits the space it was given.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The battery stands vertically in a slot behind the display's header, a face about 38 × 14 mm. The cell is 30 × 12 × 4 mm. Standing on its 30 × 4 face, it is 12 mm tall, which fits under the 14.044 mm stack, and 30 mm long, which fits along the 38 mm board. Its 4 mm thickness is the width it takes from the slot.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The battery fits within the existing height, so it does not add thickness. That is exactly why it was stood on end. The electronics stack does not fit a 16 mm envelope once walls are added. Either the requirement grows to about 18 mm, with a written reason, or the concept changes. The quickest way to find out which is to sketch alternatives.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Sketching Concepts</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>concept sketch</strong> is a quick drawing, on paper or in any drawing tool, that shows the arrangement of the main parts and the product's outline. It is not CAD. Its job is to let you compare ideas in minutes rather than days.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Draw <strong>at least three concepts that are genuinely different</strong>, not three versions of the same idea. Change the arrangement, not just the corner radius. For each, draw two views, from the top and from the side, and annotate them:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">overall outline and thickness (from a thickness budget like the one above)</li><li style="margin:6px 0;">which face touches skin, which the wearer sees</li><li style="margin:6px 0;">where the buttons, charge port and strap attachments are</li><li style="margin:6px 0;">where the battery goes</li></ul>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here are three different arrangements of the same parts:</div>

```text
A: Stacked (esp_watch as built)      B: Side by side                 C: Sensor pod on the strap
   side view                            side view                       side view
   ┌──────────────┐                     ┌────────────────────────┐      ┌───────────┐
   │ display      │                     │ display │ board │ batt │      │ display,  │
   │ motion  batt │  ~18 mm             ├─────────┴───────┴──────┤~11mm│ board,    │ ~13 mm
   │ board        │                     │ sensor                 │      │ battery   │
   │ sensor       │                     └────────────────────────┘      └─────┬─────┘
   └──────────────┘                     wider: ~55 mm                   flex cable │ in the strap
   37.8 × 39 mm board                                                      ┌──────▼──────┐
                                                                          │ sensor pod  │ under the wrist
                                                                          └─────────────┘
```

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>The thicknesses above are rough, for comparing concepts only. They assume the same modules rearranged; real numbers come from CAD in E2.</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Choosing a Direction: The Comparison Matrix</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Compare the concepts against your spec with a simple matrix. Pick one concept as the <strong>datum</strong>, the reference, and score every other concept against it on each criterion: better (+), same (0) or worse (−). This is often called a <strong>Pugh matrix</strong>. It is quick, and it forces every comparison to name a criterion from the spec.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Choosing Between A, B and C</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Concept A, esp\_watch as built, is the datum.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Criterion (A0 spec, plus build effort)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">A: Stacked (datum)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">B: Side by side</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">C: Sensor pod on strap</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Thickness ≤ 16 mm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">+ (about 11 mm)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">+ (about 13 mm)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Outline fits a small wrist</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">− (about 55 mm wide)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensor pressed to skin, light blocked</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">+ (pod sits under the wrist)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Buttons reachable with one hand</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charge port away from skin</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Printable with FDM (E3)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">− (flexible strap section, two parts)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Uses the existing board unchanged</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">− (new layout)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">− (new layout, flex cable)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Total</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">−1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">0</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Reading the result.</strong> No concept beats the datum outright. B fixes thickness but becomes too wide and needs a new board. C fixes thickness and improves sensor contact, but adds a flexible cable through the strap, a harder-to-print part, and a new board. A remains the most buildable, and its one clear failure, thickness, now has a number.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The decision, and its justification</strong>, might then read:</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>Direction: Concept A. Accept a total thickness of about 18 mm for version 1 and update NFR-07 accordingly, because A uses the existing board and is printable as two parts. Record Concept C as the version 2 direction, since it solves both thickness and sensor contact.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> The decision names the criterion that was traded (thickness), changes the spec in writing rather than ignoring it, and records the better long-term option. That is what a justification looks like: not "A looked best", but which requirement moved and why.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Change the weights.</div><div>Suppose your A0 spec says thickness is the single most important requirement, because users in your Part 2 interviews refused to wear anything thick.</div><div>1. <strong>Predict.</strong> Does the choice change?</div><div>2. <strong>Do.</strong> Count the thickness row as three times the others, and recalculate the totals.</div><div>3. <strong>Explain.</strong> Which concept wins now? What would you have to accept to build it?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. List your constraints.</strong> Build the constraint table for your product, tracing each row to a requirement ID in your A0 spec.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Fix orientations.</strong> For every part that must face a particular way, write the face and the reason.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Calculate a thickness budget.</strong> Use your module heights from B4 and your best estimate of the stack (C3 and E2 will confirm it), plus example wall and clearance values.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Sketch three concepts</strong> that differ in arrangement. Two views each, all constraints annotated, thickness from the budget.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Choose a direction</strong> with a comparison matrix against your spec, and write a justification that names any requirement you changed.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6. Hand the board its shape.</strong> From the chosen concept, sketch the board outline with its rough dimensions, the mounting-hole positions, and which side (top or bottom) every part goes on. C3 lays out the board to this sketch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> three annotated concept sketches (photos or drawings), the comparison matrix, the written direction and the board outline sketch, saved in your design pack as C0-concept.md.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open C0-concept.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every constraint in the table traces to a requirement ID in your A0 spec. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every part that must face a particular way has its face and reason written. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. A thickness budget is calculated, with every layer listed. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. There are three concepts that differ in arrangement, not just styling. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every sketch has a top view and a side view. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Every sketch shows skin side, viewing side, buttons, charge port, strap attachment and battery. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. The comparison matrix uses criteria from your spec, with one concept as the datum. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The chosen direction names every requirement it trades, and any spec change is written into A0. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. The board outline sketch gives dimensions, mounting holes and a side for every part. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A student's concept puts the USB-C charging port on the base, next to the sensor window, "so the cable is hidden". Which constraint does this break, and when should it be fixed?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Charge access: the port must open on a side, away from skin and sweat. Fix it now, in the concept, before layout.</li><li style="margin:6px 0;">B. None. KiCad DRC will flag a port on the wrong face.</li><li style="margin:6px 0;">C. Thickness. Fix it in CAD in E2.</li><li style="margin:6px 0;">D. Strap attachment. Fix it in the slicer.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> The orientation table puts the charge port on a side, away from sweat and skin. <strong>B:</strong> DRC checks copper rules, not which face touches the wrist. <strong>C</strong> and <strong>D</strong> name constraints the port does not affect, at stages too late to move a part.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A concept's electronics stack is 14 mm, and the case adds 1.5 mm walls top and bottom plus 0.5 mm clearance on each side. The spec says ≤ 16 mm. What is the right response?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Make the walls 0.5 mm thick.</li><li style="margin:6px 0;">B. The total is about 18 mm, so either change the concept to reduce the stack, or change the requirement in writing with a reason.</li><li style="margin:6px 0;">C. Ignore it until the CAD model is finished.</li><li style="margin:6px 0;">D. Remove the clearances.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> 14 + 1 + 3 = 18 mm, which fails the requirement. The honest choices are to change the design or change the spec, visibly. <strong>A</strong> and <strong>D</strong> produce parts that are too thin to print reliably or that squeeze the electronics. <strong>C</strong> delays the discovery to a more expensive stage.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A student submits three concepts. All are stacked like Concept A: one has rounded corners, one has square corners, one is 2 mm narrower. What is the main problem?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing. Three concepts were drawn.</li><li style="margin:6px 0;">B. They differ only in styling, so they share the same thickness and board trade-offs, and nothing real has been compared.</li><li style="margin:6px 0;">C. They should have been drawn in CAD.</li><li style="margin:6px 0;">D. The narrower one breaks the strap constraint.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Same arrangement means the same thickness problem. A real alternative moves parts, as concepts B and C in this unit do. <strong>A</strong> counts sketches, not ideas. <strong>C:</strong> concept sketches are meant to be quick and on paper. <strong>D:</strong> nothing shows the strap is affected.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> In a Pugh matrix, a concept scores + on thickness but − on "uses the existing board". What does this tell you?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The concept is neutral overall, so it does not matter.</li><li style="margin:6px 0;">B. It trades an improvement in a requirement for extra design work; whether that is worth it depends on how much each criterion matters to your product.</li><li style="margin:6px 0;">C. The matrix is broken.</li><li style="margin:6px 0;">D. Choose it, because pluses outweigh minuses.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The matrix makes the trade-off visible; weighting the criteria, or discussing them, decides it. <strong>A</strong> misreads a balanced score as "no difference". <strong>C</strong> is wrong: trade-offs are what the matrix is for. <strong>D</strong> treats all criteria as equally important without checking.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> Your electronics stack is 12 mm tall over a 35 mm board. Your battery is 25 × 10 × 4 mm. Which placement adds no thickness?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Flat, under the board.</li><li style="margin:6px 0;">B. On its long edge beside the modules: 25 mm long, 4 mm wide, 10 mm tall.</li><li style="margin:6px 0;">C. On its end: 10 × 4 mm face down, 25 mm tall.</li><li style="margin:6px 0;">D. Flat, on top of the display.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> At 10 mm tall it fits under the 12 mm stack, and at 25 mm long it fits along the 35 mm board. Like esp\_watch's cell, it uses height the stack already claims. <strong>A</strong> and <strong>D</strong> add a 4 mm layer. <strong>C</strong> stands 13 mm above the stack.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Next:</strong> <a href="C1-kicad-schematic-walkthrough.md">C1 — KiCad Walkthrough: From Pin Map to Schematic</a> draws the circuit in KiCad. Your concept returns in C3 (board outline) and Module 5 (CAD).</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. International Electrotechnical Commission. Ingress Protection (IP) ratings (the two-digit code for solids and liquids, for your sweat and water constraint). https://www.iec.ch/ip-ratings</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
