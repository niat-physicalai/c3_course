<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">A0 — Product Specification</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Turning Your Problem Statement into Requirements You Can Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 1 — System Architecture <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a filled product specification (template at the end of this reading)</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Wishes Are Not Requirements</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two students start from the same problem statement: hostel students cannot easily see how active they are, or how their resting heart rate changes through a semester. Both buy the same heart-rate sensor, display and battery on the same day.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Three weeks later, one device reads well at a desk but is flat before lunch. The other lasts four days but is too thick to wear to class. Neither student made an electrical mistake. Nobody wrote down, before buying parts, how long the device must last or how thick it may be.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">"Long battery life" and "small" are wishes. A <strong>specification</strong> turns them into statements with a number, a condition and a way to check them. Every design decision you make later in this course is judged against that document. This reading shows you how to write one.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Produce</strong> a product specification from your problem statement, using the template provided.</li><li style="margin:6px 0;">​<strong>Rewrite</strong> a vague requirement so it has a number, a condition and a check method.</li><li style="margin:6px 0;">​<strong>Classify</strong> requirements as functional or non-functional.</li><li style="margin:6px 0;">​<strong>Calculate</strong> whether a battery-life requirement is achievable from a usage pattern and a battery size.</li><li style="margin:6px 0;">​<strong>Write</strong> an out-of-scope list that keeps version 1 small enough to finish.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Parts 1 and 2 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 2 gave you a problem statement with a defined user. Here you turn it into checkable requirements and a list of what version 1 will not do.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">How to read the labels in this material.</div><ul style="margin:6px 0 0 0;padding-left:22px;"><li style="margin:3px 0;">​<strong>Teaching model</strong> — a simplification that is useful for thinking but not the full truth.</li><li style="margin:3px 0;">​<strong>Example values</strong> — numbers chosen to make a calculation clear. The datasheet always wins.</li><li style="margin:3px 0;">​<strong>Assumption</strong> — something this reading assumes because your tools or kit will define it precisely.</li></ul></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What a Specification Is</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A specification says <strong>what</strong> the product must do and <strong>how well</strong>, but not <strong>how</strong>. "Measures heart rate" belongs in a spec. "Uses a MAX30102 sensor" is a design choice made later. If that part is discontinued, the spec stays the same and only the design changes.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A spec is built in this order:</div>

```text
Problem statement  (from Part 2)
      │
      ▼
Who is the user, and what does their day look like?
      │
      ▼
Where is the product used?  (environment)
      │
      ▼
Requirements:  what it does  +  how well it does it
      │
      ▼
How each requirement will be checked
      │
      ▼
What version 1 will NOT do
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A spec is not paperwork written after the design. Changing "3 days of battery" to "1 day" costs one sentence today, and a new board if you discover it after manufacture.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Two Kinds of Requirement</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>functional requirement</strong> describes something the product does, a behaviour you could watch happen: "The watch shall show the wearer's heart rate when asked."</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>non-functional requirement</strong> (NFR) describes how well it does it, or the limits it must stay within: accuracy, speed, battery life, cost, size.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A shirt with the right pockets that does not fit is still a failed order. Unlike a shirt, a circuit board cannot be altered once it arrives.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For a wearable these often matter most: a watch that measures perfectly but is 25 mm thick will not be worn. Cover each category:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Category</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Question it answers</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Example for a wrist device (example values)</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Accuracy</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How close to the true value, and when?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart rate within ±5 bpm, wearer sitting still</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Response time</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How long does the wearer wait?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">First heart-rate value within 15 s of asking</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery life</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How long between charges, <strong>used how</strong>?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">≥ 2 days with the usage pattern in section 3 of the spec</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cost</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Maximum parts cost, at what quantity?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">≤ ₹2,500 per unit when making 10</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Size and weight</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How big and heavy, including the case?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">≤ 45 × 45 × 16 mm, ≤ 40 g</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lifetime</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How long must it keep working?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1 year of daily wear</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Serviceability</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What can be repaired or replaced?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery replaceable with a screwdriver</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Note "wearer sitting still" in the accuracy row. Optical heart-rate sensors lose accuracy when the wrist moves, so without that condition you would promise something no such sensor delivers.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Making a Requirement Checkable</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every requirement you write has four parts:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>An ID</strong> such as FR-03 (functional) or NFR-02 (non-functional), so later documents can refer to it.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>A "shall" statement</strong>: the watch shall…</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>A number, a unit and a condition</strong>: how much, measured how, under what circumstances.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>A check method</strong>: how someone else could confirm it is met.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">NASA's engineering handbook uses the same checklist: state what is needed rather than how, number every requirement, and make each one checkable [1].</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">First draft</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Problem</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Rewritten</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The battery should last a long time.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No number, no condition</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-03: The watch shall run ≥ 2 days between charges with usage pattern UP-1.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The watch uses Bluetooth to sync.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Names a solution, not a need</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">FR-07: The watch shall make the day's step count available on the wearer's phone at least once a day.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The watch should be cheap.</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cheap to whom, in what quantity?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">NFR-04: Parts cost shall be ≤ ₹2,500 per unit at a quantity of 10.</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Checking Without Building</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Normally you would check many requirements by testing real hardware. In this course nothing is built, so you use four methods that work at a laptop:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Method</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What you do</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Example</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Inspection</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Look at a design file</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Measure the board outline in KiCad</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Analysis</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Calculate from datasheet figures</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Work out battery life (see the worked example)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Simulation</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Run the design in a simulator</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check a screen-timeout rule in Wokwi</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Review</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Compare against a datasheet or the reference design</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Confirm the sensor faces the skin in the CAD model</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Some requirements, such as heart-rate accuracy, can only be proven on real hardware. Mark these test (after build) and note what you can check now, such as the sensor touching the skin in your CAD model.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The User, Their Day and Their Environment</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A spec that does not describe its user assumes the user is you, at a desk, next to a charger. Write a short <strong>use scenario</strong> for a normal day:</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A hostel student puts the watch on at 7 am, glances at it about 50 times during lectures and meals, checks their heart rate a few times, and charges it overnight every second night.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">That paragraph holds a wake count, a charging interval and a battery target. Turn it into a table called a <strong>usage pattern</strong> (UP-1), because every battery calculation depends on it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Next, list the <strong>operating environment</strong>: everything the product is exposed to while it works. A wrist is a harsh place:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Condition</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Requirement it leads to</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Constant skin contact</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sensor must press against the skin; no sharp edges</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sweat (salty, conductive)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">State a water-resistance target, even if it is "splash only"</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Knocks and drops</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">State a drop height the watch and battery must survive</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Summer heat plus body heat</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">State an operating temperature range</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For water and dust, engineers use the <strong>IP code</strong>: one digit for solids (0 to 6), one for liquids (0 to 9) [2]. You need not claim a rating in version 1, but write down your target.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On esp\_watch, the heart-rate sensor sits on the underside of the board so that it touches the wrist. C0 looks at this choice.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Deciding What Version 1 Will Not Do</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Most student projects fail not from a wrong part but from growth: blood-oxygen readings because the sensor "can do it anyway", then an app, then notifications, until nobody finishes. The defence is an <strong>out-of-scope list</strong>. Each entry names an expected feature, why it is left out, and where it goes instead:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Not in version 1</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where it goes</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Blood-oxygen (SpO2) readings</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A blood-oxygen number looks like medical advice, and the device cannot support that claim</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Never, unless it becomes a certified medical device</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Phone app</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Doubles the software work; the watch meets the core need alone</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Version 2</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Waterproofing beyond splashes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Needs sealed buttons and ports that a 3D-printed case cannot provide</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Version 2</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Continuous heart-rate logging</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The sensor's LEDs drain the battery fast</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reconsider after the power budget</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">"We ran out of time" is not a reason. It is what happens when this list is never written.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Can esp\_watch Last Two Days?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Here is one requirement taken from a vague wish to a checked statement, using the reference watch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: The wish.</strong> "The battery should last a while."</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 2: Tie it to the user.</strong> A student who charges every second night needs at least 2 days. <strong>Target: ≥ 2 days.</strong></div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 3: Write the usage pattern.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch connects to WiFi once when first switched on, then keeps WiFi off, and measures heart rate only when asked. Today's firmware keeps the watch always on; the author's power model plans for the screen to turn off 30 s after the last button press and the watch to sleep. UP-1 is that <strong>planned</strong> pattern:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Activity</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Per day</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Total time</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Screen on</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">50 wakes × 30 s</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">25 min = 0.417 h</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate reading</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">5 × 30 s</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2.5 min = 0.042 h</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sleep</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">rest of the day</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">24 − 0.417 − 0.042 = 23.54 h</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 4: Find the current for each activity.</strong> These are <strong>estimates from a power model, not measurements</strong>:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Activity</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Current (estimated)</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Screen on</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">about 36 mA</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate reading</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">about 44 mA</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sleep</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1 to 3 mA</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 5: Multiply current by time</strong> to get the charge used per day, in milliamp-hours (mAh):</div>

```text
Screen on:   0.417 h × 36 mA = 15.0 mAh
Heart rate:  0.042 h × 44 mA =  1.8 mAh
Sleep:      23.54 h ×  1 mA = 23.5 mAh   (best case)
            23.54 h ×  3 mA = 70.6 mAh   (worst case)
──────────────────────────────────────────────
Per day:     40.3 mAh (best)     87.4 mAh (worst)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 6: Work out the usable battery.</strong> A lithium cell should not be run flat, and it loses capacity with age. <strong>Assumption:</strong> 80% is usable.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's cell is a protected 300 mAh LiPo, so usable charge is 300 × 0.8 = <strong>240 mAh</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 7: Divide.</div>

```text
Best case:   240 ÷ 40.3 = 6.0 days
Worst case:  240 ÷ 87.4 = 2.7 days
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check against an outside figure.</strong> Seeed, who make the XIAO ESP32-C3 board, give light-sleep current as below <strong>4 mA</strong> [3]. Take 4 mA as a pessimistic case: 23.54 h × 4 mA = 94.2 mAh, so 111 mAh a day and 240 ÷ 111 = <strong>2.2 days</strong>. The 2-day requirement still holds, just.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Sleep uses 58% of the daily charge in the best case and 81% in the worst. The screen feels hungry, but the small current that runs all day decides battery life.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">The finished requirement:</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">NFR-03.</div><div>The watch shall run ≥ 2 days between charges with usage pattern UP-1. Check: analysis (above); test after build.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's board is 14.044 mm tall before any case is added. A thickness limit in the spec is what tells you whether that is acceptable. E2 checks it.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: A heavier user.</div><div>Keep everything from the worked example, but the wearer now checks the watch 150 times a day.</div><div>1. <strong>Predict.</strong> Does the watch still last 2 days with 3 mA sleep? With 4 mA?</div><div>2. <strong>Do.</strong> Recalculate screen time, sleep time, charge per day and days of use.</div><div>3. <strong>Explain.</strong> Which activity uses the most charge now? Was your prediction right?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Specification Template</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Copy this into your design pack as A0-specification.md and fill in every section. If a section does not apply, write why rather than leaving it blank.</div>

```markdown
# Product Specification — <product name> — v0.1

## 1. Problem statement (copied from Part 2)
## 2. User — who they are, and what they use today instead
## 3. Use scenario — one paragraph describing a normal day
### Usage pattern UP-1
| Activity | Times per day | Duration each | Total per day |
## 4. Operating environment
| Condition | Range or description | Requirement it leads to |
## 5. Functional requirements
| ID | The product shall… | Number + condition | Check method |
## 6. Non-functional requirements (cover all seven categories)
| ID | Category | The product shall… | Number + condition | Check method |
## 7. Success criteria — the 3 to 5 requirements that matter most
## 8. Not in version 1
| Feature | Why | Where it goes |
## 9. Open questions — what you cannot decide yet
```

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>1. Find the faults.</strong> Three of these five requirements are faulty. Find them and rewrite them.</div>

```text
FR-02   The watch shall show the step count on the second screen.
NFR-02  Battery: 5 days.
FR-04   The watch shall use an MPU-6050 to count steps.
NFR-06  The watch shall be comfortable.
NFR-07  The board outline shall be ≤ 40 × 40 mm. Check: inspection in KiCad.
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>NFR-02</strong> has no usage pattern and no check method. Five days of doing what? <strong>FR-04</strong> names a part. Instead, say what is needed, for example "count steps within ±10% of a manual count over 500 steps". <strong>NFR-06</strong> cannot be checked. Replace it with measurable limits such as weight, thickness and no sharp edges. FR-02 and NFR-07 are fine.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Write your own.</strong> Fill in the whole template for your Part 2 problem statement. Include the battery calculation, showing every step, and at least four entries in "Not in version 1". <strong>This file is your deliverable for this unit.</strong></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your A0-specification.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every requirement has a unique ID. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every non-functional requirement has a number and a unit. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every requirement has a check method (inspection, analysis, simulation, review, or test after build). — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. No requirement names a specific part. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. All seven non-functional categories appear. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The battery requirement refers to a usage pattern written as a table. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. The battery calculation shows every step and the usable-capacity assumption. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. "Not in version 1" has at least four entries, each with a reason. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> Which requirement can be checked without building anything?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Heart rate shall be within ±5 bpm of a chest strap, wearer sitting still.</li><li style="margin:6px 0;">B. The watch shall survive a 1 m drop onto tiles.</li><li style="margin:6px 0;">C. The circuit board shall fit within 40 × 40 mm.</li><li style="margin:6px 0;">D. The buttons shall be easy to press.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> You can measure the outline in KiCad. <strong>A</strong> is well written but needs a real wrist to prove. <strong>B</strong> can be supported by CAD, but only a real drop proves it. <strong>D</strong> cannot be checked until "easy" becomes a number, such as a press force.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A student writes "NFR-03: Battery life shall be at least 3 days." What is most importantly missing?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The battery chemistry</li><li style="margin:6px 0;">B. The usage pattern the 3 days applies to</li><li style="margin:6px 0;">C. The battery's part number</li><li style="margin:6px 0;">D. The charging current</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The same watch can last a week or a day depending on use, so without a usage pattern nobody can check the figure. <strong>A</strong> and <strong>C</strong> are design choices, not requirements. <strong>D</strong> affects charging speed, not battery life.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A watch spends 20 minutes a day with the screen on at 36 mA and 23.7 hours asleep at 2 mA. Which single change gives the longest battery life?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Halve the screen-on time to 10 minutes</li><li style="margin:6px 0;">B. Halve the sleep current to 1 mA</li><li style="margin:6px 0;">C. Skip the one daily WiFi sync</li><li style="margin:6px 0;">D. Take 3 heart-rate readings a day instead of 5</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Screen: 0.333 h × 36 mA = 12 mAh a day. Sleep: 23.7 h × 2 mA = 47.4 mAh. Halving sleep current saves about 24 mAh; halving screen time (<strong>A</strong>) saves 6 mAh. <strong>C</strong> and <strong>D</strong> are short events and save even less.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Which "not in version 1" entry is written best?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. "No SpO2."</li><li style="margin:6px 0;">B. "SpO2 — maybe later."</li><li style="margin:6px 0;">C. "SpO2 readings — left out because a blood-oxygen number looks like medical advice the device cannot support — never, unless it becomes a certified medical device."</li><li style="margin:6px 0;">D. "SpO2 — the sensor supports it, so add it if there is time."</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C</strong> names the feature, a real reason and a destination. <strong>A</strong> gives no reason, so someone will add it back. <strong>B</strong> decides nothing. <strong>D</strong> adds a feature just because the hardware can, which is the opposite of scope control.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A spec says "FR-09: The display shall always be on" and "NFR-03: The watch shall run 7 days on a 100 mAh battery." With the screen drawing 36 mA, what is wrong?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing, because they are about different parts of the watch.</li><li style="margin:6px 0;">B. They contradict each other. The screen alone uses about 864 mAh a day, but 7 days on 100 mAh allows only about 14 mAh a day.</li><li style="margin:6px 0;">C. NFR-03 cannot be checked.</li><li style="margin:6px 0;">D. FR-09 should be a non-functional requirement.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> 36 mA × 24 h = 864 mAh a day, against a budget of 100 ÷ 7 ≈ 14 mAh a day. <strong>A</strong> is wrong because both draw on the same battery. <strong>C</strong> is wrong: it has a number and can be checked by calculation. <strong>D</strong> is wrong: "always on" is a behaviour, so it is correctly functional.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The idea to carry forward: <strong>a requirement is only real if someone else can check it.</strong></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Next, in <a href="A1-overall-system-architecture.md">A1 — Overall System Architecture</a>, you will draw the whole system on one page and give every requirement you wrote here to the part of the system responsible for it.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. NASA. Systems Engineering Handbook, Appendix C: How to Write a Good Requirement (checklists for "shall" statements, numbered and verifiable requirements, and stating needs rather than solutions). https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. International Electrotechnical Commission. Ingress Protection (IP) ratings (the two-digit code for protection against solids and liquids). https://www.iec.ch/ip-ratings</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Seeed Studio. Getting Started with Seeed Studio XIAO ESP32C3 (power figures, including light-sleep and deep-sleep current). https://wiki.seeedstudio.com/XIAO\_ESP32C3\_Getting\_Started/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
