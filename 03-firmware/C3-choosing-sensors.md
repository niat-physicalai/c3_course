# C3 — Common Sensors, and Choosing the Right One for the Job
## From "Measure Heart Rate" to a Sensor You Can Defend

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Firmware
**Time:** ~1.5 hours · **You will produce:** a sensor selection matrix for your own product and a solved scenario exercise

---

### The Sensor From the Last Tutorial Is Not a Decision

Ask a class to design a step counter and most students will reach for the accelerometer they used last time. Ask them to detect a person in a room and they reach for the PIR sensor from the kit. Sometimes that is right. Often it is just familiar.

A sensor is not chosen by what you have used before. It is chosen by answering a harder question first: **what physical quantity actually tells you the thing you care about?** "Measure heart rate" sounds like a specification, but it is not. Heart rate can be sensed through light, through electrical signals, through pressure, and each of those works differently on a wrist, in a lab and during a run. The right choice depends on where the sensor is worn, what the user will put up with, and which kind of mistake you can afford.

This unit gives you a map of the common sensor families, a framework for choosing between them, and two worked examples: one from the reference watch and one deliberately far from wearables, so the method does not become "whatever a smartwatch uses".

### What You Will Be Able to Do After This Reading

- **Identify** the physical quantity that genuinely indicates what your product needs to know.
- **Compare** sensor families on what they measure, their output, their cost and how they fail.
- **Apply** a selection framework: contact, range, response time, environment, output, power, cost, and which error is more expensive.
- **Justify** each sensor in your design, with a rejected alternative and a stated reason.
- **Produce** a sensor selection matrix for your own product.

### What Part 1 Already Covered

Part 1 had you read many common sensors through libraries: light, temperature, distance, motion, and digital and analog outputs. **What is new here** is *choosing* a sensor from the problem backwards: starting from the quantity that matters and the errors you can tolerate, comparing families, and writing down why the alternatives lost.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — A Map of Sensor Families

## Seven Families

Most sensors in connected products fall into seven families. For each, know what it *actually* measures, which is often not the thing you care about, and how it fails.

| Family | Common examples | What it actually measures | Typical output | How it typically fails |
|---|---|---|---|---|
| Presence and proximity | PIR, infrared reflective, ultrasonic, capacitive | Changing heat pattern, reflected light, echo time, capacitance | Digital, analog or pulse | PIR misses a still person; reflective sensors fooled by dark or shiny surfaces |
| Position and motion | Accelerometer, gyroscope, rotary encoder, Hall-effect sensor | Acceleration (including gravity), rotation rate, shaft position, magnetic field | I²C/SPI, pulses | Accelerometers mix gravity with motion; gyroscopes drift over time |
| Optical and biometric | Photoplethysmography (PPG), light sensor, colour sensor | Light reflected or transmitted through tissue or a surface | I²C, analog | Ambient light, poor contact, motion |
| Environmental | Temperature, humidity, pressure, gas | The conditions at the sensor itself | I²C, analog | Self-heating; reads the enclosure, not the room; gas sensors drift |
| Force and level | Load cell, force-sensitive resistor, float switch, ultrasonic level | Strain, resistance change, float position, distance | Analog (often needs an amplifier), digital | Creep, temperature drift, mechanical wear |
| Electrical | Current shunt, Hall current sensor, voltage divider | Voltage across a resistance, magnetic field around a conductor | Analog, I²C | Offset and noise at small currents |
| Identification | RFID/NFC reader, barcode or QR scanner | Presence and code of a tag | UART, SPI, I²C | Range, orientation, metal nearby |

> **Teaching model.** Families overlap: an ultrasonic sensor measures distance, which can indicate presence *or* level. Use the table to widen your search, not to limit it.

The middle column is the important one. An accelerometer does not measure steps; it measures acceleration, and a step is something your firmware infers from a pattern. A PPG sensor does not measure heart rate; it measures changes in reflected light, from which a heartbeat is inferred. Every inference adds a way to be wrong.

## Sensing Is Measuring a Stand-In

The distinction has a name. The quantity you want is the **measurand**. The quantity the sensor responds to is often a **proxy**: something that usually moves with the measurand, but not always.

| You want | The sensor measures | When the proxy lies |
|---|---|---|
| Steps taken | Acceleration at the wrist | Clapping, typing, a bumpy auto-rickshaw ride |
| Heart rate | Changing reflected light under the skin | Wrist movement, loose fit, bright sunlight |
| A person in the room | A moving heat pattern (PIR) | The person sits perfectly still |
| Tank level | Distance from the lid to the surface | Foam, ripples, condensation on the sensor |

For every sensor in your design, write down when its proxy lies. That list becomes part of your failure table from A2, and part of what your firmware must detect.

<!-- MEDIA
type: diagram
id: C3-01
caption: How a wrist PPG sensor works, and where its signal goes wrong
brief: A cross-section of a wrist: skin surface, tissue, and a blood vessel whose width
  pulses. On the skin sits a sensor with an LED and a photodiode side by side. Arrows
  show light entering the skin, scattering, and part of it returning to the photodiode;
  label the returning light "varies slightly with each heartbeat". Add three red
  annotations showing error sources: "ambient light leaking in at a loose edge",
  "sensor sliding over the skin as the wrist moves", "rhythmic arm swing at the same
  rate as a heartbeat (signal crossover)". Flat, clear style; no brand names.
-->

---

# Part 2 — A Selection Framework

## The Questions, in Order

Work through these questions for every quantity your product must sense. Record the answers; they become your selection matrix.

1. **What physical quantity genuinely indicates what you care about?** Name the measurand and every candidate proxy.
2. **Contact or non-contact?** Must the sensor touch the thing, and will the user accept that?
3. **Range and resolution.** What is the smallest change that matters, and the largest value you must read?
4. **Response time.** How quickly must a change be noticed?
5. **Environment.** Heat, sweat, dust, light, vibration: what will the sensor face (A0)?
6. **Output type.** Does it fit your interfaces and pin budget (C2, B1)?
7. **Power.** How much, and can it be duty-cycled (B1)?
8. **Cost** at your quantities (B2).
9. **Which error is more expensive: a false positive or a false negative?**

The last question changes decisions more than any other. A **false positive** reports something that did not happen: a step that was a clap. A **false negative** misses something that did happen: a heartbeat not detected. For a step counter, both are mild. For a fall detector, a false negative, a real fall missed, is far worse than a false alarm. For a factory reject gate, a false positive, a good product thrown away, costs money, but a false negative, a faulty product shipped, can cost a customer. Decide which matters more *before* choosing, because it tells you which sensor weakness you cannot accept.

## Worked Example 1: Heart Rate From a Wrist, Without the Wearer Doing Anything

**The requirement:** *"A wrist-worn device must measure heart rate without the wearer doing anything."*

**Step 1: Name the measurand and the candidates.** The measurand is the heartbeat. Four ways to sense it:

| Candidate | What it measures |
|---|---|
| Optical PPG | Changes in light reflected from blood under the skin |
| ECG electrodes | The heart's electrical activity, between two points on the body |
| Chest strap | ECG, from electrodes held against the chest |
| Piezo pulse sensor | Pressure from the pulse at an artery |

**Step 2: Test each against the requirement's conditions.** The requirement contains two conditions: *wrist-worn* and *without the wearer doing anything*.

- **ECG** gives a clean signal, but it needs electrodes touching the body at two separated points, with the heart between them. A single wrist is one point. Watches that record an ECG ask the wearer to touch the watch with the *other* hand, which breaks "without doing anything". **Rejected: needs a deliberate action.**
- **Chest strap** is accurate and continuous. It is also on the chest, not the wrist, and for a hostel student wearing it all day it is simply unacceptable. **Rejected: user tolerance.**
- **Piezo pulse sensor** needs to sit firmly over an artery. On a wrist that moves and a strap that shifts, it loses the pulse easily. **Rejected: placement too fragile.**
- **Optical PPG** works passively from the back of the wrist. **Kept**, with its weaknesses written down.

**Step 3: State how the chosen sensor fails.** Published research gives this real numbers. A study comparing six consumer and research wearables against a medical ECG found heart-rate error during activity was on average about 30% higher than at rest [1]. It also describes **signal crossover**: the sensor can lock on to the rhythm of repetitive motion, such as walking, and report that as the heart rate [1]. Whether skin tone affects wrist PPG accuracy is still debated. That study found no significant difference across skin tones [1], while a published response argued its sample of the darkest skin tones was too small to be sure [2]. Pulse oximeters, which use similar optics to estimate blood oxygen, have a documented racial bias in their readings [3], which is one more reason for A0's decision to leave SpO2 out of version 1.

**Step 4: Turn the weaknesses into design requirements.**

<!-- REFPRODUCT:START -->
esp_watch's design already answers several of these:

| PPG weakness | Design response | Where it lives |
|---|---|---|
| Motion error, signal crossover | Measure on request, with the wearer still; the motion sensor can flag readings taken while moving | Firmware (C4); MPU-6050 already on board |
| Ambient light | Sensor on the underside, pressed to the skin; enclosure window aligned with the sensor | Board (B5); enclosure (Module 4) |
| Loose fit | Case and strap hold the sensor against the wrist | Enclosure (Module 4) |
| Skin-tone uncertainty | Test across skin tones during the funded build | Test plan |
<!-- REFPRODUCT:END -->

**Check.** The lesson is not "PPG is best". It is that **"measure heart rate" was never a specification.** The physical quantity (reflected light, not the heartbeat itself), the wearing position (one wrist), the user's tolerance (no chest strap, no second hand) and the failure modes (motion, fit, light) decided it. A different product, say a gym machine with metal hand grips, would reasonably choose ECG.

> **Try it: Change one condition.** Rewrite the requirement as *"A device must measure heart rate accurately during a 30-minute run."*
> 1. **Predict.** Does PPG still win?
> 2. **Do.** Re-run Step 2 with the new condition. Give each candidate a verdict and a reason.
> 3. **Explain.** Which candidate's rejection reason changed? What does that tell you about where the decision really came from?

## Worked Example 2: Three Sensing Jobs in One Machine

This example is deliberately far from wearables.

**The requirement:** *"A small conveyor counts bottles going past, checks whether each has a cap, and measures how fast the belt is moving."*

**Step 1: Split it into separate sensing problems.** These are three different jobs:

| Job | Measurand | Kind of problem |
|---|---|---|
| Count bottles | A bottle passing a point | Detect a discrete event |
| Check for a cap | A feature at the top of each bottle | Inspect a feature |
| Belt speed | Rate of belt movement | Measure a rate |

**Step 2: Pick candidates for each.**

| Job | Candidates | Choice and reason |
|---|---|---|
| Count bottles | Infrared break-beam; reflective infrared; camera | **Break-beam**: simple, fast, cheap, and a bottle reliably blocks it. A camera is overkill for "something passed". |
| Check for a cap | Reflective sensor at cap height; inductive proximity sensor (metal caps only); camera | **Reflective sensor at cap height**, if caps and bottle necks look different to it. If caps are metal, an **inductive sensor** ignores bottle colour entirely. |
| Belt speed | Encoder on a roller; magnet on the roller with a Hall-effect sensor; timing bottles between two break-beams | **Magnet and Hall sensor**: one pulse per turn, simple and non-contact. Timing bottles fails when there are gaps in the line. |

**Step 3: Which error is more expensive?** For counting, a missed bottle or a double count is a small bookkeeping error. For cap checking, a **false negative**, an uncapped bottle passed as capped, reaches a customer. So the cap check is where money should go: a better sensor, a second sensor, or a check that fails safe.

**Check.** The cheapest sensor, a break-beam, is enough for counting and hopeless for cap checking, even in the same machine. Each job gets its own measurand, its own sensor and its own tolerance for error.

<!-- MEDIA
type: diagram
id: C3-02
caption: One conveyor, three sensing jobs, three different sensors
brief: A side view of a short conveyor belt carrying bottles left to right. At one point,
  an infrared break-beam crosses the belt at bottle-body height, labelled "count: break-
  beam". Further along, a small sensor points down at cap height, labelled "cap check:
  reflective or inductive". Under the belt, one roller has a small magnet on its end and a
  Hall sensor beside it, labelled "belt speed: 1 pulse per turn". One bottle without a cap
  is highlighted. Clean isometric or flat style.
-->

---

# Part 3 — Your Selection Matrix

## The Matrix

The deliverable records the whole decision for every quantity your product senses. Use one row per quantity:

| Quantity (measurand) | Chosen sensor | What it actually measures | Rejected alternative | Why rejected | How the chosen sensor fails | Costlier error (FP or FN) | Design response |
|---|---|---|---|---|---|---|---|

<!-- REFPRODUCT:START -->
esp_watch's matrix:

| Quantity | Chosen | Actually measures | Rejected | Why rejected | How it fails | Costlier error | Design response |
|---|---|---|---|---|---|---|---|
| Heart rate | MAX30102 (PPG) | Reflected red and infrared light | ECG electrodes | Needs a second contact point, so the wearer must act | Motion, loose fit, ambient light | FN is mild (retry); FP could mislead | Measure on request, when still; enclosure blocks light |
| Steps | MPU-6050 accelerometer | Acceleration at the wrist, including gravity | Pedometer switch | Crude, no data for other uses | Non-walking arm motion counted | Mild either way | Thresholds and pattern checks in firmware |
| Wrist shake to wake | MPU-6050 accelerometer | Acceleration | A dedicated button only | Wearer wants a hands-free wake | Wakes on bumps | FP costs battery; FN costs a button press | Wake threshold; 30 s timeout limits the cost |
| Battery level | Voltage divider to ADC | Cell voltage | Fuel-gauge chip | Extra part and cost for a simple watch | Voltage sags under load; ADC varies by chip | FN (runs flat without warning) | Measure at rest; calibrate |
<!-- REFPRODUCT:END -->

Two things stand out in this matrix. One sensor, the accelerometer, serves three rows, which is a good use of a part already on the board. And the heart-rate row shows the whole of Worked Example 1 compressed into a single line, which is what makes the matrix useful to a reviewer: every choice arrives with its reasoning.

> **Try it: Add a row.** esp_watch's team wants to show skin temperature.
> 1. **Predict.** Will a temperature sensor on the board measure skin temperature?
> 2. **Do.** Fill a full matrix row. Consider where the sensor sits, what it will actually measure (hint: the board, the battery and the enclosure all have temperatures too), and name one rejected alternative.
> 3. **Explain.** What design response would make the reading mean what the requirement says?

---

# Putting It All Together

## Applying What You Have Learned

**1. List every quantity.** From your A0 requirements, list every physical quantity your product must sense.

**2. Name the measurand and proxies.** For each, write what you really want to know and what candidate sensors actually measure.

**3. Run the framework.** For each quantity, answer the nine questions, reject at least one alternative with a stated reason, and decide which error is costlier.

**4. Fill the selection matrix.** One row per quantity, every column complete, including the design response to each failure mode.

**5. Solve a scenario.** Pick one: *(a) a smart bin that knows when it is full; (b) a hostel room monitor that knows whether a window is open; (c) a cycle-stand that counts free slots.* Split it into sensing jobs, choose a sensor for each, and state the costlier error.

**Deliverable:** add your selection matrix and solved scenario to your design pack as `C3-sensor-selection.md`. This matrix feeds your B2 component choices.

## Self-Check

Open `C3-sensor-selection.md` and answer each item Y or N.

1. Every quantity from your A0 requirements has a row. — Y/N
2. Every row names what the sensor actually measures, separately from what you want to know. — Y/N
3. Every row has at least one rejected alternative with a reason. — Y/N
4. Every rejection reason refers to a requirement, a constraint or a failure mode. — Y/N
5. Every row states how the chosen sensor fails. — Y/N
6. Every row states which error is costlier. — Y/N
7. Every failure mode has a design response, linked to a unit or file. — Y/N
8. The scenario exercise splits the problem into separate sensing jobs. — Y/N

---

## Check Your Understanding

**1.** A fall detector for elderly people must alert a carer. Which error should the sensor choice work hardest to avoid, and why?

- A. False positives, because false alarms annoy the carer.
- B. False negatives, because a real fall that is missed could leave someone without help.
- C. Neither; both are equally bad.
- D. Whichever is cheaper to fix in firmware.

<details>
<summary>Answer</summary>

**B.** A missed fall has a far higher cost than a false alarm. **A** is a real concern, but a secondary one: it is usually handled with a "cancel" button, not by accepting missed falls. **C** ignores the consequences. **D** puts implementation convenience ahead of the requirement.

</details>

**2.** A room-occupancy system uses a PIR sensor. It reports the room empty while a student sits studying. What is the best explanation?

- A. The PIR sensor is faulty.
- B. PIR detects a *changing* heat pattern, so a still person is invisible to it; the proxy (movement) does not match the measurand (presence).
- C. The room is too warm.
- D. The sensor needs a faster interface.

<details>
<summary>Answer</summary>

**B.** PIR responds to movement of heat, not to presence. That is a known failure mode of the family, not a fault. **A** blames the part for doing exactly what it measures. **C** can reduce sensitivity, but it does not explain a still person being missed. **D** is unrelated to what the sensor detects.

</details>

**3.** Why was ECG rejected for esp_watch's heart rate, even though it gives a cleaner signal than PPG?

- A. ECG sensors are more expensive.
- B. ECG needs contact at two separated points, so a single wrist device needs the wearer to touch it with the other hand, which breaks "without the wearer doing anything".
- C. ECG does not work at 3.3 V.
- D. ECG cannot use I²C.

<details>
<summary>Answer</summary>

**B.** The requirement's condition, not the signal quality, decided it. **A** may be true of some parts, but it was not the deciding reason. **C** and **D** are not properties of ECG sensing in general, and many ECG front-end chips work at 3.3 V.

</details>

**4.** A wrist PPG sensor reports 120 bpm while the wearer walks at 2 steps per second. A chest-strap reference shows 95 bpm. What is the most likely explanation?

- A. The chest strap is wrong.
- B. Signal crossover: the PPG has locked on to the arm-swing rhythm (2 per second = 120 per minute) instead of the heartbeat.
- C. The wearer's skin tone.
- D. The I²C bus is too slow.

<details>
<summary>Answer</summary>

**B.** Two steps per second is exactly 120 per minute, matching the wrong reading. Published research describes this "signal crossover" effect [1]. The accelerometer on the same device can detect this: if the heart rate matches the step rate, be suspicious. **A** has no support; chest straps are the usual reference. **C** does not explain a reading that matches the step rate. **D** would lose or delay data; it would not create a precise false rhythm.

</details>

**5.** A bottling line's sensor passes uncapped bottles about once in 500. Where should improvements focus?

- A. The bottle counter, because counting errors add up.
- B. The cap check, because a false negative (an uncapped bottle passed as capped) reaches customers.
- C. The belt-speed sensor.
- D. All three sensors equally.

<details>
<summary>Answer</summary>

**B.** The expensive error is the one that leaves the factory. **A** matters for bookkeeping, but a miscount does not harm a customer. **C** has nothing to do with caps. **D** spreads effort evenly instead of where the costlier error is.

</details>

**6.** A team wants to show *room* temperature on a watch, using a temperature sensor on the watch's circuit board. What is the main problem?

- A. Temperature sensors need SPI.
- B. The sensor measures the board's own temperature, which is warmed by the wrist, the battery and the electronics, not the room.
- C. The display cannot show decimals.
- D. There is no problem.

<details>
<summary>Answer</summary>

**B.** The proxy is the board's temperature, and on a wrist it is dominated by body heat and self-heating. **A** is false; many temperature sensors use I²C. **C** is irrelevant. **D** ignores what the sensor actually measures.

</details>

---

## What You Can Now Do, and What Comes Next

- Separate what you want to know from what a sensor actually measures, and say when the proxy lies.
- Compare sensor families by output, cost and failure mode.
- Choose a sensor with a framework, including which error is costlier.
- Defend every choice with a rejected alternative and a reason.

The idea to carry forward: **"measure X" is not a specification.** The quantity, the position, the user and the failure you can afford decide the sensor.

In [C4 — Non-Blocking Application Logic](C4-non-blocking-application-logic.md) you will make the firmware run all of these sensors at their own rates, together with the display and the state machine, without any of them waiting for the others.

---

## References

1. Bent, B., Goldstein, B. A., Kibbe, W. A. and Dunn, J. P. *Investigating sources of inaccuracy in wearable optical heart rate sensors.* npj Digital Medicine 3, 18 (2020) (error during activity about 30% higher than at rest; signal crossover; no significant difference across skin tones in this study). https://www.nature.com/articles/s41746-020-0226-6
2. Colvonen, P. J. *Response to: Investigating sources of inaccuracy in wearable optical heart rate sensors.* npj Digital Medicine (2021) (argues the sample of darker skin tones was too small, and questions the skin-tone scale used). https://pmc.ncbi.nlm.nih.gov/articles/PMC7910598/
3. Sjoding, M. W., Dickson, R. P., Iwashyna, T. J., Gay, S. E. and Valley, T. S. *Racial bias in pulse oximetry measurement.* New England Journal of Medicine 383, 2477–2478 (2020), doi:10.1056/NEJMc2029240.
   <!-- LINK:VERIFY  want: "Sjoding et al. 2020 NEJM, Racial bias in pulse oximetry measurement"  search: "doi 10.1056/NEJMc2029240" -->

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
