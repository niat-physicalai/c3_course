# A0 — Product Specification
## Turning Your Problem Statement into Requirements You Can Check

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 1 — System Architecture
**Time:** ~1 hour · **You will produce:** a filled product specification (template at the end of this reading)

---

### Wishes Are Not Requirements

Two students start from the same problem statement: *hostel students cannot easily see how active they are, or how their resting heart rate changes through a semester.* Both buy the same heart-rate sensor, display and battery on the same day.

Three weeks later, one device reads well at a desk but is flat before lunch. The other lasts four days but is too thick to wear to class. Neither student made an electrical mistake. Nobody wrote down, *before* buying parts, how long the device must last or how thick it may be.

"Long battery life" and "small" are wishes. A **specification** turns them into statements with a number, a condition and a way to check them. Every design decision you make later in this course is judged against that document. This reading shows you how to write one.

### What You Will Be Able to Do After This Reading

- **Produce** a product specification from your problem statement, using the template provided.
- **Rewrite** a vague requirement so it has a number, a condition and a check method.
- **Classify** requirements as functional or non-functional.
- **Calculate** whether a battery-life requirement is achievable from a usage pattern and a battery size.
- **Write** an out-of-scope list that keeps version 1 small enough to finish.

### What Parts 1 and 2 Already Covered

Part 2 gave you a problem statement with a defined user. Here you turn it into checkable requirements and a list of what version 1 will not do.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## What a Specification Is

A specification says **what** the product must do and **how well**, but not **how**. "Measures heart rate" belongs in a spec. "Uses a MAX30102 sensor" is a design choice made later. If that part is discontinued, the spec stays the same and only the design changes.

A spec is built in this order:

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

A spec is not paperwork written after the design. Changing "3 days of battery" to "1 day" costs one sentence today, and a new board if you discover it after manufacture.

## Two Kinds of Requirement

A **functional requirement** describes something the product *does*, a behaviour you could watch happen: *"The watch shall show the wearer's heart rate when asked."*

A **non-functional requirement** (NFR) describes *how well* it does it, or the limits it must stay within: accuracy, speed, battery life, cost, size.

A shirt with the right pockets that does not fit is still a failed order. Unlike a shirt, a circuit board cannot be altered once it arrives.

For a wearable these often matter most: a watch that measures perfectly but is 25 mm thick will not be worn. Cover each category:

| Category | Question it answers | Example for a wrist device (example values) |
|---|---|---|
| Accuracy | How close to the true value, and when? | Heart rate within ±5 bpm, wearer sitting still |
| Response time | How long does the wearer wait? | First heart-rate value within 15 s of asking |
| Battery life | How long between charges, **used how**? | ≥ 2 days with the usage pattern in section 3 of the spec |
| Cost | Maximum parts cost, at what quantity? | ≤ ₹2,500 per unit when making 10 |
| Size and weight | How big and heavy, including the case? | ≤ 45 × 45 × 16 mm, ≤ 40 g |
| Lifetime | How long must it keep working? | 1 year of daily wear |
| Serviceability | What can be repaired or replaced? | Battery replaceable with a screwdriver |

Note "wearer sitting still" in the accuracy row. Optical heart-rate sensors lose accuracy when the wrist moves, so without that condition you would promise something no such sensor delivers.

## Making a Requirement Checkable

Every requirement you write has four parts:

1. **An ID** such as `FR-03` (functional) or `NFR-02` (non-functional), so later documents can refer to it.
2. **A "shall" statement**: *the watch shall…*
3. **A number, a unit and a condition**: how much, measured how, under what circumstances.
4. **A check method**: how someone else could confirm it is met.

NASA's engineering handbook uses the same checklist: state what is needed rather than how, number every requirement, and make each one checkable [1].

| First draft | Problem | Rewritten |
|---|---|---|
| The battery should last a long time. | No number, no condition | NFR-03: The watch shall run ≥ 2 days between charges with usage pattern UP-1. |
| The watch uses Bluetooth to sync. | Names a solution, not a need | FR-07: The watch shall make the day's step count available on the wearer's phone at least once a day. |
| The watch should be cheap. | Cheap to whom, in what quantity? | NFR-04: Parts cost shall be ≤ ₹2,500 per unit at a quantity of 10. |

### Checking Without Building

Normally you would check many requirements by testing real hardware. In this course nothing is built, so you use four methods that work at a laptop:

| Method | What you do | Example |
|---|---|---|
| Inspection | Look at a design file | Measure the board outline in KiCad |
| Analysis | Calculate from datasheet figures | Work out battery life (see the worked example) |
| Simulation | Run the design in a simulator | Check a screen-timeout rule in Wokwi |
| Review | Compare against a datasheet or the reference design | Confirm the sensor faces the skin in the CAD model |

Some requirements, such as heart-rate accuracy, can only be proven on real hardware. Mark these *test (after build)* and note what you can check now, such as the sensor touching the skin in your CAD model.

## The User, Their Day and Their Environment

A spec that does not describe its user assumes the user is you, at a desk, next to a charger. Write a short **use scenario** for a normal day:

*A hostel student puts the watch on at 7 am, glances at it about 50 times during lectures and meals, checks their heart rate a few times, and charges it overnight every second night.*

That paragraph holds a wake count, a charging interval and a battery target. Turn it into a table called a **usage pattern** (UP-1), because every battery calculation depends on it.

Next, list the **operating environment**: everything the product is exposed to while it works. A wrist is a harsh place:

| Condition | Requirement it leads to |
|---|---|
| Constant skin contact | Sensor must press against the skin; no sharp edges |
| Sweat (salty, conductive) | State a water-resistance target, even if it is "splash only" |
| Knocks and drops | State a drop height the watch and battery must survive |
| Summer heat plus body heat | State an operating temperature range |

For water and dust, engineers use the **IP code**: one digit for solids (0 to 6), one for liquids (0 to 9) [2]. You need not claim a rating in version 1, but write down your target.

<!-- REFPRODUCT:START -->
On esp_watch, the heart-rate sensor sits on the underside of the board so that it touches the wrist. C0 looks at this choice.
<!-- REFPRODUCT:END -->

## Deciding What Version 1 Will Not Do

Most student projects fail not from a wrong part but from growth: blood-oxygen readings because the sensor "can do it anyway", then an app, then notifications, until nobody finishes. The defence is an **out-of-scope list**. Each entry names an expected feature, why it is left out, and where it goes instead:

| Not in version 1 | Why | Where it goes |
|---|---|---|
| Blood-oxygen (SpO2) readings | A blood-oxygen number looks like medical advice, and the device cannot support that claim | Never, unless it becomes a certified medical device |
| Phone app | Doubles the software work; the watch meets the core need alone | Version 2 |
| Waterproofing beyond splashes | Needs sealed buttons and ports that a 3D-printed case cannot provide | Version 2 |
| Continuous heart-rate logging | The sensor's LEDs drain the battery fast | Reconsider after the power budget |

"We ran out of time" is not a reason. It is what happens when this list is never written.

---

## Worked Example: Can esp_watch Last Two Days?

Here is one requirement taken from a vague wish to a checked statement, using the reference watch.

**Step 1: The wish.** "The battery should last a while."

**Step 2: Tie it to the user.** A student who charges every second night needs at least 2 days. **Target: ≥ 2 days.**

**Step 3: Write the usage pattern.**

<!-- REFPRODUCT:START -->
esp_watch connects to WiFi once when first switched on, then keeps WiFi off. The screen turns off 30 s after the last button press and the watch goes to sleep. The motion sensor stays on during sleep so a shake of the wrist wakes it. Heart rate is measured only when asked. So UP-1 is:

| Activity | Per day | Total time |
|---|---|---|
| Screen on | 50 wakes × 30 s | 25 min = 0.417 h |
| Heart-rate reading | 5 × 30 s | 2.5 min = 0.042 h |
| Sleep | rest of the day | 24 − 0.417 − 0.042 = 23.54 h |

**Step 4: Find the current for each activity.** These are **estimates from a power model, not measurements**:

| Activity | Current (estimated) |
|---|---|
| Screen on | about 36 mA |
| Heart-rate reading | about 44 mA |
| Sleep | 1 to 3 mA |
<!-- REFPRODUCT:END -->

**Step 5: Multiply current by time** to get the charge used per day, in milliamp-hours (mAh):

```text
Screen on:   0.417 h × 36 mA = 15.0 mAh
Heart rate:  0.042 h × 44 mA =  1.8 mAh
Sleep:      23.54 h ×  1 mA = 23.5 mAh   (best case)
            23.54 h ×  3 mA = 70.6 mAh   (worst case)
──────────────────────────────────────────────
Per day:     40.3 mAh (best)     87.4 mAh (worst)
```

**Step 6: Work out the usable battery.** A lithium cell should not be run flat, and it loses capacity with age. **Assumption:** 80% is usable.

<!-- REFPRODUCT:START -->
esp_watch's battery has not been chosen yet. The **placeholder** is 400 mAh, so usable charge is 400 × 0.8 = **320 mAh**.
<!-- FACT:VERIFY placeholder cell: 400 mAh is unusually high for the 20 × 5 × 13 mm size recorded in REFERENCE-PRODUCT.md §4; author to confirm -->
<!-- REFPRODUCT:END -->

**Step 7: Divide.**

```text
Best case:   320 ÷ 40.3 = 7.9 days
Worst case:  320 ÷ 87.4 = 3.7 days
```

**Check against an outside figure.** Seeed, who make the XIAO ESP32-C3 board, give light-sleep current as below **4 mA** [3]. Take 4 mA as a pessimistic case: 23.54 h × 4 mA = 94.2 mAh, so 111 mAh a day and 320 ÷ 111 = **2.9 days**. This holds with the 400 mAh placeholder. Redo the check once the real cell is chosen.

Sleep uses 58% of the daily charge in the best case and 81% in the worst. The screen *feels* hungry, but the small current that runs all day decides battery life.

**The finished requirement:**

> **NFR-03.** The watch shall run ≥ 2 days between charges with usage pattern UP-1. *Check:* analysis (above); test after build.

<!-- REFPRODUCT:START -->
esp_watch's board is 14.044 mm tall before any case is added. A thickness limit in the spec is what tells you whether that is acceptable. E2 checks it.
<!-- REFPRODUCT:END -->

> **Try it: A heavier user.** Keep everything from the worked example, but the wearer now checks the watch 150 times a day.
> 1. **Predict.** Does the watch still last 2 days with 3 mA sleep? With 4 mA?
> 2. **Do.** Recalculate screen time, sleep time, charge per day and days of use.
> 3. **Explain.** Which activity uses the most charge now? Was your prediction right?

---

## The Specification Template

Copy this into your design pack as `A0-specification.md` and fill in every section. If a section does not apply, write why rather than leaving it blank.

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

# Putting It All Together

## Applying What You Have Learned

**1. Find the faults.** Three of these five requirements are faulty. Find them and rewrite them.

```text
FR-02   The watch shall show the step count on the second screen.
NFR-02  Battery: 5 days.
FR-04   The watch shall use an MPU-6050 to count steps.
NFR-06  The watch shall be comfortable.
NFR-07  The board outline shall be ≤ 40 × 40 mm. Check: inspection in KiCad.
```

<details>
<summary>Answer</summary>

**NFR-02** has no usage pattern and no check method. Five days of doing what? **FR-04** names a part. Instead, say what is needed, for example "count steps within ±10% of a manual count over 500 steps". **NFR-06** cannot be checked. Replace it with measurable limits such as weight, thickness and no sharp edges. FR-02 and NFR-07 are fine.

</details>

**2. Write your own.** Fill in the whole template for your Part 2 problem statement. Include the battery calculation, showing every step, and at least four entries in "Not in version 1". **This file is your deliverable for this unit.**

## Self-Check

Open your `A0-specification.md` and answer each item Y or N.

1. Every requirement has a unique ID. — Y/N
2. Every non-functional requirement has a number and a unit. — Y/N
3. Every requirement has a check method (inspection, analysis, simulation, review, or test after build). — Y/N
4. No requirement names a specific part. — Y/N
5. All seven non-functional categories appear. — Y/N
6. The battery requirement refers to a usage pattern written as a table. — Y/N
7. The battery calculation shows every step and the usable-capacity assumption. — Y/N
8. "Not in version 1" has at least four entries, each with a reason. — Y/N

---

## Check Your Understanding

**1.** Which requirement can be checked without building anything?

- A. Heart rate shall be within ±5 bpm of a chest strap, wearer sitting still.
- B. The watch shall survive a 1 m drop onto tiles.
- C. The circuit board shall fit within 40 × 40 mm.
- D. The buttons shall be easy to press.

<details>
<summary>Answer</summary>

**C.** You can measure the outline in KiCad. **A** is well written but needs a real wrist to prove. **B** can be supported by CAD, but only a real drop proves it. **D** cannot be checked until "easy" becomes a number, such as a press force.

</details>

**2.** A student writes *"NFR-03: Battery life shall be at least 3 days."* What is most importantly missing?

- A. The battery chemistry
- B. The usage pattern the 3 days applies to
- C. The battery's part number
- D. The charging current

<details>
<summary>Answer</summary>

**B.** The same watch can last a week or a day depending on use, so without a usage pattern nobody can check the figure. **A** and **C** are design choices, not requirements. **D** affects charging speed, not battery life.

</details>

**3.** A watch spends 20 minutes a day with the screen on at 36 mA and 23.7 hours asleep at 2 mA. Which single change gives the longest battery life?

- A. Halve the screen-on time to 10 minutes
- B. Halve the sleep current to 1 mA
- C. Skip the one daily WiFi sync
- D. Take 3 heart-rate readings a day instead of 5

<details>
<summary>Answer</summary>

**B.** Screen: 0.333 h × 36 mA = 12 mAh a day. Sleep: 23.7 h × 2 mA = 47.4 mAh. Halving sleep current saves about 24 mAh; halving screen time (**A**) saves 6 mAh. **C** and **D** are short events and save even less.

</details>

**4.** Which "not in version 1" entry is written best?

- A. "No SpO2."
- B. "SpO2 — maybe later."
- C. "SpO2 readings — left out because a blood-oxygen number looks like medical advice the device cannot support — never, unless it becomes a certified medical device."
- D. "SpO2 — the sensor supports it, so add it if there is time."

<details>
<summary>Answer</summary>

**C** names the feature, a real reason and a destination. **A** gives no reason, so someone will add it back. **B** decides nothing. **D** adds a feature just because the hardware can, which is the opposite of scope control.

</details>

**5.** A spec says *"FR-09: The display shall always be on"* and *"NFR-03: The watch shall run 7 days on a 100 mAh battery."* With the screen drawing 36 mA, what is wrong?

- A. Nothing, because they are about different parts of the watch.
- B. They contradict each other. The screen alone uses about 864 mAh a day, but 7 days on 100 mAh allows only about 14 mAh a day.
- C. NFR-03 cannot be checked.
- D. FR-09 should be a non-functional requirement.

<details>
<summary>Answer</summary>

**B.** 36 mA × 24 h = 864 mAh a day, against a budget of 100 ÷ 7 ≈ 14 mAh a day. **A** is wrong because both draw on the same battery. **C** is wrong: it has a number and can be checked by calculation. **D** is wrong: "always on" is a behaviour, so it is correctly functional.

</details>

---

## What Comes Next

The idea to carry forward: **a requirement is only real if someone else can check it.**

Next, in [A1 — Overall System Architecture](A1-overall-system-architecture.md), you will draw the whole system on one page and give every requirement you wrote here to the part of the system responsible for it.

---

## References

1. NASA. *Systems Engineering Handbook, Appendix C: How to Write a Good Requirement* (checklists for "shall" statements, numbered and verifiable requirements, and stating needs rather than solutions). https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/
2. International Electrotechnical Commission. *Ingress Protection (IP) ratings* (the two-digit code for protection against solids and liquids). https://www.iec.ch/ip-ratings
3. Seeed Studio. *Getting Started with Seeed Studio XIAO ESP32C3* (power figures, including light-sleep and deep-sleep current). https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
