# The Electrical Foundation (continued from Part 1)

> *This is Part 2 of the RM1 reading material. Part 1 covered Understanding IoT Systems and the first half of the Electrical Foundation (voltage, current, resistance, Ohm's Law, series/parallel circuits, voltage dividers, and Kirchhoff's Laws). This part continues with power and energy, safety, troubleshooting and the key takeaways.*

---

### Power and Energy

Voltage and current tell you about the push and the flow. But there is a third question that matters a great deal in practice: **how fast is energy being converted?** The answer is **power**, measured in **watts (W)**, where 1 W means one joule of energy per second.

For any component:

```text
P = V × I
```

Combining this with Ohm's Law gives two more useful forms:

```text
P = I² × R          P = V² ÷ R
```

Use whichever form uses the quantities you already know.

#### Power Becomes Heat

In a resistor, all the electrical power ends up as **heat**. Each resistor has a maximum power it can safely dissipate, and many common through-hole resistors are rated for around a quarter of a watt (check the rating of the ones in your kit). Exceed the rating and the resistor gets hot, changes value, discolours or fails.

**Worked example.** A 220 Ω resistor is placed directly across 5 V.
- Current: 5 V ÷ 220 Ω ≈ 22.7 mA
- Power: 5 V × 22.7 mA ≈ **114 mW** (about 0.11 W)

That is under 0.25 W, so it is safe with a comfortable margin. But if you halve the resistance at the same voltage, the power does not halve. Because P = V² ÷ R, *halving R doubles P*. Powers grow quickly as resistance falls.

#### Power in the LED Circuit

Return to the LED example we just worked through (150 Ω resistor, about 8.7 mA, 3.3 V supply):

| Part | Voltage | Current | Power |
|---|---|---|---|
| Resistor | 1.3 V | 8.7 mA | ≈ 11 mW |
| LED | 2.0 V | 8.7 mA | ≈ 17 mW |
| **Supply delivers** | 3.3 V | 8.7 mA | **≈ 29 mW** |

The supply's power equals the sum of what the components use, which is the energy version of KVL. Notice also that roughly 40% of the supply's power is going into heating the resistor rather than making light. That is the price of using a resistor to limit current, and it is one example of a **trade-off** that engineers accept for simplicity.

#### Supply Ratings and Loads: A Common Misunderstanding

You will often see a power adapter or USB port described with a rating such as "5 V, 2 A". Beginners often think this means the supply will push 2 A into whatever is connected. It does not.

- The **voltage** is set by the supply (5 V).
- The **current** is decided by the **load** (Ohm's Law again). A 1 kΩ load draws 5 mA from that supply, whether or not the supply *could* provide 2 A.
- The **2 A** is the **maximum** the supply can deliver properly. If the load tries to draw more, the voltage drops, the supply may overheat or shut down and the circuit may behave strangely.

So there are two separate checks when you connect a load: does the **voltage** match what the part needs, and can the supply provide enough **current**? This explains why large actuators such as motors cannot be driven directly from a microcontroller's signal pins. Those pins are designed to carry logic-level signals, not large power currents, and the datasheet of your board specifies the limits. Motors get their power from a separate supply through a suitable driver, and you will learn how to do this properly in later units.

#### Energy and Battery Life

Power over time is **energy**. In battery-powered IoT devices this becomes the central design question: how long will it run?

A battery's capacity is often given in **mAh** (milliamp-hours). As a first estimate:

```text
Runtime (hours) ≈ Battery capacity (mAh) ÷ Average current (mA)
```

For example, a 2000 mAh battery powering a sensor node that draws an average of 1 mA would last about 2000 hours, roughly 83 days. If the node draws 20 mA on average, the runtime drops to about 100 hours, roughly four days.

> **Teaching model.** This is an idealised estimate. Real batteries deliver less than their rated capacity under load, voltage falls as they discharge and the electronics that adjust the battery voltage waste some energy. Use the formula to compare designs, not to promise exact runtimes.

The big lesson for IoT is that **average current matters more than peak current**. This is why many battery-powered devices spend most of their time in a low-power sleep state and wake only briefly to sense and transmit.

---

# Building Safely and Thinking Like an Engineer

Until now, we have reasoned about circuits on paper. The next step is to touch them, and that calls for two things: knowing how to stay safe, and having an engineer's way of thinking about what a circuit is doing.

## Working Safely

Circuit experiments are safe when a few habits are followed, and unsafe when they are not. The purpose here is not to frighten you but to explain *why* the rules exist, so that you apply them sensibly.

### How Electric Current Affects the Body

Electrical injury is caused by **current passing through the body**, not by "voltage" in the abstract. But voltage matters because it decides how much current a given path can carry (Ohm's Law again). Standards bodies have studied this for decades. IEC 60479-1, the international standard on the effects of current on the human body, classifies AC responses in zones that run from being barely perceptible, to involuntary muscle contraction, to difficulty breathing and, at higher currents and longer durations, to risk of heart fibrillation and burns.

As rough orders of magnitude for AC at the frequency of household supply:

- Around **1 mA**: a faint tingle is perceptible.
- Around **10 mA**: many people can no longer let go of a live conductor (the "let-go" threshold).
- **Tens of milliamperes and above**, sustained: a serious risk to the heart and breathing.

This is why residual-current devices (safety switches that cut the supply when they detect current leaking through an unintended path) in many countries are designed to trip at around **30 mA**.

> **Teaching model.** These figures are typical orders of magnitude, not personal safety limits. The current that flows through a person depends on the voltage, the path through the body, how long contact lasts and how wet the skin is. Wet or broken skin can reduce body resistance dramatically. Never test these limits.

### Household Electricity Is Not for Experiments

In India, the household supply, often called **mains electricity**, is around **230 V AC**. That is more than enough to push a dangerous current through a person, and it is delivered from a source that can supply far more current than the body can withstand.

**In this course, you will not open, modify or work on anything connected to mains electricity.** Your experiments use low-voltage sources such as batteries and USB supplies, in the 3–5 V range. At these voltages, the risk of dangerous shock is very low, but that does not mean there is no risk. The remaining hazards are different and worth knowing:

- **Short circuits** can make wires, batteries and components hot very quickly. A shorted battery can burn fingers or start a fire.
- **Lithium-based rechargeable batteries** (Li-ion, LiPo) can deliver very large currents when shorted, and can overheat, swell or ignite if damaged, overcharged or shorted. Use them only with the correct protection and under instructor guidance.
- **Overloaded components** get hot. A resistor or any other component that is too hot to touch is telling you something.
- **Wrong voltage or reversed polarity** can destroy electronic parts instantly, even though nobody is in danger. Many microcontroller boards use **3.3 V logic** (their signal pins are designed to work with signals of around 3.3 V), and connecting 5 V to such a pin can damage it. Always check the documentation for the board you are using.

### Habits That Prevent Most Problems

- **Power off before you change anything.** Wire the circuit with the supply disconnected, check it and only then connect power.
- **Check before you connect.** Confirm polarity (+ and −), supply voltage and every component's rating.
- **Predict before you power.** Estimate the expected current and voltages. If you cannot explain what the circuit should do, do not switch it on yet.
- **Never bridge the supply directly.** Do not let a bare wire connect + to − .
- **Use resistors with LEDs** and keep an eye on power ratings.
- **Keep the bench dry and tidy.** Loose wires and spilled liquids cause shorts.
- **Trust your senses.** If something smells hot, feels hot or smokes, disconnect the power immediately and inform your instructor.
- **Use the multimeter correctly.** Measure voltage *across* components (in parallel). Measure current only by placing the meter *in series*, and never connect a meter set to measure current directly across a supply. That creates a short circuit through the meter.

## Predict → Measure → Explain

Safety keeps you and your components intact. The habit that turns building into learning is a short routine you will use in every experiment in this course:

1. **Predict.** Before powering the circuit, calculate the expected voltages and currents using Ohm's Law, the series and parallel rules and Kirchhoff's laws.
2. **Measure.** Power the circuit and measure the real values.
3. **Explain.** If prediction and measurement agree (within the tolerance of the parts and the meter), you understand the circuit. If they do not, the *difference* is information: something in your model, your wiring or your components is not what you thought.

Four questions keep the routine moving:

- What *should* happen?
- What *actually* happened?
- What could explain the difference?
- What should I measure next?

### An Example of the Routine

You build the LED circuit from earlier: 3.3 V supply, a 150 Ω resistor and a red LED. Your prediction was about **1.3 V across the resistor** and about 8.7 mA. You measure **1.0 V** across the resistor.

The measurement disagrees with the prediction, so we explain it. If the resistor really has 1.0 V across it, the current is about 6.7 mA, and by KVL the LED must be dropping about 2.3 V (assuming the supply is 3.3 V). Two explanations are plausible: this LED's forward voltage is higher than the 2.0 V we assumed (an LED of a different colour, perhaps), or the supply is lower than 3.3 V. What should you measure next? The supply voltage settles that question in seconds. Either way, the exercise taught you something about the circuit that your first prediction did not know.

This is the same habit professionals use on far more complex systems, and it is the foundation of the troubleshooting method that follows.

## Troubleshooting Basics

Predict, measure and explain works well when things go roughly as planned. When they do not, you need a method for deciding *where* to look, instead of changing things at random and losing track of what you tried.

A simple beginner-friendly sequence works for almost any simple circuit:

```text
Observe → Identify → Check → Test → Change → Retest
```

| Step | What you do |
|---|---|
| **Observe** | Look, listen and (carefully) feel. What is actually happening? Is anything hot, smoking, dim, dark or behaving differently from what you predicted? |
| **Identify** | Name the specific symptom in one sentence: "the LED stays dark", "the meter reads 0 V where I expected 5 V". |
| **Check** | Compare the circuit against your diagram and your prediction, one part at a time: power, wiring, component values, polarity. |
| **Test** | Measure something, usually a voltage, to gather evidence rather than guess. |
| **Change** | Make **one** change based on what you found. Do not change several things at once, or you will not know which change fixed it. |
| **Retest** | Power up again and see whether the symptom is gone. If not, return to Observe with what you have just learned. |

Two ideas from earlier in this module make the **Check** and **Test** steps far more powerful than guessing: professionals move from the most common and easiest-to-check causes toward the rarer ones, and they let their measurements point directly at the fault.

The order that usually finds a fault fastest:

```text
Safety ─► Power ─► Connections ─► Components ─► Measurements ─► Expected vs Actual
```

| Step | Question to ask | How to check |
|---|---|---|
| **Safety** | Is anything hot, smoking or shorted? | Look, smell, feel carefully. Disconnect power if in doubt. |
| **Power** | Is the supply actually delivering the right voltage? | Measure the supply voltage at the circuit, not just at the source. |
| **Connections** | Is the path complete? Are there wrong or loose connections? | Compare with the diagram wire by wire. On a breadboard, check that each part is in the row you think it is. |
| **Components** | Is each part the right value, and the right way round? | Check resistor values, LED polarity and component ratings. |
| **Measurements** | Where do the voltages start to differ from your prediction? | Measure voltage across each component and follow the path. |
| **Expected vs Actual** | What does the difference tell you? | Use Ohm's Law, KVL and KCL to interpret it. |

(When programs are added to the system in later units, one more step joins the list: check that the software is doing what you believe it is doing.)

### Let the Voltages Point to the Fault

![Debugging with evidence: measuring at each point and comparing with what was expected](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-29-debug-with-evidence.png)

Ohm's Law and KVL give you very practical rules for reading measurements:

- **Zero volts across a resistor in a series path means zero current through it.** (V = I × R; if I = 0, then V = 0.) So if a resistor that "should" have a voltage across it reads 0 V, the current is not flowing. Look for a break elsewhere in the loop.
- **Across an open break, you measure the full supply voltage.** Since no current flows, no other component drops any voltage, and the entire supply voltage appears across the gap by KVL. A voltmeter placed across a suspected break will read the supply voltage and *point directly at the fault*.
- **Voltage across a shorted component reads 0 V**, even though current may be flowing through the short.

### Common Symptoms and What to Suspect

| Symptom | Possible causes | First thing to check |
|---|---|---|
| LED does not light | Reversed LED, open circuit, no power, resistor far too large | Supply voltage at the circuit; then voltage across the LED and across the resistor |
| LED very dim | Resistor too large, supply lower than expected, weak battery | Voltage across the resistor, then compute the current |
| LED unusually bright, hot, or fails | Resistor missing or far too small | Disconnect power. Re-check the resistor value against your calculation |
| Supply voltage drops when the load is connected | Load draws more than the supply can provide, weak battery, partial short | Measure supply voltage with and without the load |
| A part becomes hot | Too much power in the part, or a short | Disconnect power. Compute expected power (P = V × I) and compare with the rating |
| Adding a second branch makes everything worse | Total current now exceeds the supply's capability | Add up the branch currents (KCL) and compare with the supply's rating |

---

## Key Takeaways

### The Mental Model

![The complete mental model: physical world, sense, compute, actuate, and back to the physical world](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-31-complete-mental-model.png)

An IoT system is a physical system that can **sense** the world, **process** information, **act** on decisions and, eventually, **communicate** with other systems.

Underneath that description is a loop that repeats in almost everything you will build: Sense → Compute → Actuate, with the result of the action feeding back into the physical world. IoT adds communication to the loop. AIoT adds AI to the compute stage. Physical AI applies AI-driven perception, reasoning and action to machines that move and interact with the world. And every arrow in that loop is carried by **electrical signals and electrical power**.

### The Electrical Toolkit

| Idea | Relationship | Remember |
|---|---|---|
| Ohm's Law | V = I × R | Current is set by voltage and resistance together. |
| Power | P = V × I = I² × R = V² ÷ R | Power in a resistor becomes heat. Check ratings. |
| Series | Same current; voltages add; R_total = R1 + R2 + … | One break stops everything. Larger R takes larger voltage. |
| Parallel | Same voltage; currents add; R_total is less than the smallest | Independent branches. Total current grows with each branch. |
| KVL | Voltages around a closed loop sum to zero | Sources' rises equal components' drops. |
| KCL | Current into a junction equals current out | Charge doesn't accumulate at a junction. |
| Voltage divider | V_out = V_in × R_bottom ÷ (R_top + R_bottom) | How a changing resistance becomes a changing voltage. |

### The Habits

- **Predict before you power**, measure to check, and explain any difference.
- **Let the voltages point to the fault** when something does not work.
- **Keep the circuit safe**: low voltage only, power off when wiring, and check ratings before connecting.

### What Comes Next

You now have both the vocabulary of IoT systems and the reasoning tools to understand what happens electrically inside them. In the modules ahead, we will progressively turn these foundations into working systems:

- The **ESP32-S3** microcontroller will take the place of the "Compute" box in our diagrams. You will program it to read inputs and control outputs.
- **Sensors** will show how physical conditions become signals your program can read. The voltage-divider thinking you practised here will keep coming back.
- **Actuators** will show how to turn decisions into motion, light and sound. The power and current reasoning will decide what you can connect and how.
- **Communication protocols** and **cloud services** will let your devices share data, be monitored and be controlled from anywhere.
- **AI** and **embedded vision** will add intelligence to the compute stage, so systems can interpret complex signals such as images.

None of these are separate from what you have learned in this module. They are the same loop, extended. Whenever a new component or a strange behaviour appears, you can return to the same questions: *What is it sensing? What is it deciding? What does it change? Where does the electrical energy go?* And when something does not behave as expected: *What did I predict? What did I measure? What could explain the difference?*

---

## References

1. NVIDIA. *What is Physical AI?* Glossary. https://www.nvidia.com/en-eu/glossary/physical-ai/
2. ITU-T. *Internet of Things Global Standards Initiative* (definition from Recommendation ITU-T Y.2060). https://www.itu.int/en/ITU-T/gsi/iot
3. Voas, J. *Networks of "Things"* (Demystifying IoT). NIST. https://www.nist.gov/document/jeffvoaspdf
4. TechTarget. *Artificial Intelligence of Things (AIoT)*. https://www.techtarget.com/iotagenda/definition/Artificial-Intelligence-of-Things-AIoT
5. IEC. *IEC 60479-1 — Effects of current on human beings and livestock, Part 1: General aspects.* Overview: https://standards.globalspec.com/std/10031392/iec-ts-60479-1
6. IPD. *Why 30 mA and 300 ms?* (summary of IEC 60479-1 shock zones and RCD thresholds). https://ipd.com.au/why-30ma-and-300ms
7. Espressif Systems. *ESP32-S3 Hardware Design Guidelines* (recommended 3.3 V supply). https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32s3/index.html
8. Standard introductory circuit-theory references for Ohm's Law, Kirchhoff's laws, series/parallel networks and power. These are foundational results found in any university-level basic electrical engineering text.

> **Note on numbers.** Component values, LED forward voltage, LDR resistances and battery figures in this reading are **example values** chosen for clear calculation. Always use the datasheet of the actual part you are using.