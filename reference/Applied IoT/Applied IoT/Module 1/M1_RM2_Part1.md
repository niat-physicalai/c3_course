# From Components to a Microcontroller-Controlled System

## Opening the Boxes in the Loop

So far, you have met the pattern behind every IoT system: **Sense → Compute → Actuate**, with communication added when devices are connected. You have also built the electrical foundation underneath it: voltage, current, resistance, Ohm's Law, series and parallel circuits, voltage dividers, Kirchhoff's laws and power.

Those ideas described the *behaviour* of circuits. This reading looks at the *parts* that circuits are made of, and at the three boxes in the loop:

```text
   Sensor  ──►  Microcontroller  ──►  Actuator
```

We will open each of them in turn.

- **Components** are the small building blocks of every circuit: resistors, LEDs, diodes, capacitors, buttons and transistors. Each has a specific job, and knowing those jobs lets you read a circuit the way you read a sentence.
- **Sensors and actuators** are the parts of a system that touch the physical world. One brings information in. The other pushes an effect out.
- **The microcontroller** is the small computer that sits between them. It reads the signals from sensors, runs your program and drives the actuators.

By the end, you will be able to look at a working IoT device, identify what senses, what decides and what acts, trace the signal from one end to the other and explain how a program running on a chip ends up switching something in the physical world.

### What You Will Be Able to Do After This Reading

- Identify common electronic components and describe what each one does in a circuit.
- Predict the role of a component in a simple circuit, and build or analyse circuits using a resistor, an LED, a diode, a capacitor, a button and a transistor switch.
- Distinguish between sensors and actuators, and identify the inputs and outputs of a physical computing system.
- Trace the signal path from sensor to microcontroller to actuator.
- Explain what a microcontroller is, how it differs from a general-purpose computer, and what processing, memory, peripherals and GPIO mean.
- Choose a sensor and an actuator that suit a simple application.

> **How to read the labels in this material.** As before, three kinds of statements appear.
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. Real parts vary, and the datasheet of the actual part always wins.
> - **Assumption** — something this reading assumes because it depends on your specific hardware or on material that comes later.

> **Assumption about hardware.** The course hardware is ESP32-based, and the syllabus is built around the ESP32-S3 with CircuitPython. This reading explains microcontroller ideas in general and uses the ESP32-S3 only as an example where it helps. Board-specific details, such as pin names, are left to the board's own documentation and to the hands-on setup that follows this reading. If your board is a different ESP32 variant from the one in the syllabus, check the documentation of *your* board before relying on any board-specific detail.

> **A first taste of the hardware.** You have not yet set up a real board — that comes in the next Reading Material. But two of the ideas in this reading (a resistor-and-LED circuit, and a button read through a pull-up) are simple enough to try right now, in the free browser-based simulator **Wokwi**, on a simulated **ESP32-S3**, programmed in **Arduino C/C++**. These two short activities are collected in the companion projects file for this reading. They are optional at this stage, but seeing a program actually switch the LED you have been calculating voltages for is a good bridge into the next reading, where you set up real hardware.

---

# Electronic Components

## A Circuit Is a Team of Components

A circuit that does something useful is rarely a single component. It is a small team, and each member has a job. Looking at a circuit board, you might see dozens of tiny parts, but they mostly do a handful of jobs:

- **Limiting** how much current flows (resistors).
- **Directing** current so that it flows only one way (diodes).
- **Storing** a little electrical energy and releasing it later (capacitors).
- **Opening and closing** a path (buttons and switches).
- **Using a small signal to control a bigger flow** (transistors).
- **Converting** electrical energy into light, motion, or sound (LEDs, motors, buzzers), or converting a physical condition into an electrical signal (sensors).

### Passive and Active Components

You will often hear components described as *passive* or *active*. At an intuitive level:

- A **passive** component responds to the voltage and current in the circuit but cannot control them by itself. A resistor and a capacitor are typical examples. They cannot make a signal stronger and they do not need a separate power connection to do their job.
- An **active** component can use a small signal to control a larger flow of electrical energy, or can process signals. A transistor is the classic example. A microcontroller, which contains thousands or millions of transistors, is active too.

> **Teaching model.** Diodes and LEDs sit in an awkward middle: they need no separate power supply, but their behaviour depends strongly on the voltage across them. Different textbooks classify them differently. You do not need to memorise the classification. It is more useful to know what each component *does*.

We will go through the main components one at a time. As you read, keep in mind the question that matters most in practice: *what would this component do in a circuit I am looking at?*

---

## The Resistor: Controlling Current

You have already used resistors extensively. Ohm's Law gave you the relationship V = I × R, and you used it to size a resistor for an LED and to build a voltage divider. Here we summarise the resistor's jobs in an IoT circuit, and add the practical skill of recognising one.

A resistor has three everyday jobs:

1. **Limiting current**, for example to protect an LED.
2. **Sharing voltage** in a voltage divider, which is how many sensors turn a changing resistance into a changing voltage.
3. **Setting a default voltage level** on an input, as a pull-up or pull-down resistor. This third job is new, and it becomes important when we look at buttons.

![Three everyday jobs of a resistor: controlling current, forming a voltage divider, and setting a default input level](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-01-resistor-jobs.png)

A resistor has no polarity. It works the same whichever way round it is connected.

### Reading a Resistor

Through-hole resistors are marked with coloured bands. In the common four-band form, the first two bands are digits, the third is a multiplier (how many zeros to add) and the fourth is the tolerance, which tells you how far the real value may be from the marked value.

| Colour | Digit | Multiplier |
|---|---|---|
| Black | 0 | × 1 |
| Brown | 1 | × 10 |
| Red | 2 | × 100 |
| Orange | 3 | × 1,000 |
| Yellow | 4 | × 10,000 |
| Green | 5 | × 100,000 |
| Blue | 6 | × 1,000,000 |
| Violet | 7 | |
| Grey | 8 | |
| White | 9 | |

A gold fourth band means a tolerance of ±5%, and silver means ±10%.

**Worked example.** Brown, black, red, gold: the digits are 1 and 0, the multiplier is × 100, so the value is 10 × 100 = **1000 Ω = 1 kΩ**, with ±5% tolerance.

Many resistors in the wild use five bands or are tiny surface-mount parts with printed numbers. The reliable method that always works is to **measure the resistor with a multimeter**, with the resistor out of any powered circuit.

---

## The Diode and the LED: One-Way Components

### The Diode

A **diode** is a component that lets current flow easily in one direction and blocks it in the other. The closest everyday picture is a one-way valve in a pipe.

A diode has two terminals with names that matter:

- The **anode** is where current enters when the diode is conducting.
- The **cathode** is where current leaves. On a physical diode, a stripe marks the cathode end.

```text
   Anode ──►|── Cathode          (current flows easily this way →)
              ↑
       the triangle points in the direction of easy current flow
```

![The diode as a one-way valve: current flows easily in the forward direction and is blocked in reverse](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-02-diode-oneway.png)

Two behaviours are worth knowing:

- **Forward direction (anode to cathode):** the diode conducts once the voltage across it reaches its **forward voltage**, and then the voltage across it stays roughly constant. For a common silicon diode, this is typically around 0.7 V.
- **Reverse direction:** the diode blocks current. (Every diode has a maximum reverse voltage it can withstand, which is listed on its datasheet.)

> **Example values.** The 0.7 V forward voltage is a typical figure for a common silicon diode. Real parts differ, and some diode types have a lower forward voltage. Use the datasheet.

**Worked example.** A 5 V supply is connected through a diode, in the forward direction, to a 1 kΩ resistor to ground.

- The diode uses about 0.7 V, so the resistor sees about 5 − 0.7 = **4.3 V**.
- Current: 4.3 V ÷ 1 kΩ = **4.3 mA**.

Now reverse the diode. It blocks current, so the current is almost zero and nearly the whole 5 V appears across the diode.

Notice that a diode does *not* obey Ohm's Law the way a resistor does. Its voltage stays roughly constant while its current changes. This is the same behaviour you saw with an LED in the earlier discussion of Ohm's Law.

**What are diodes used for in IoT circuits?**

- **Protection from reversed power.** A diode in series with the supply lets current through in the correct direction and blocks it if the battery is connected backwards. The price is a lost forward voltage drop, roughly 0.7 V in the example above.
- **Protection from voltage spikes.** When we reach transistors, you will see a diode placed across a motor or relay coil to absorb a voltage spike that would otherwise damage the circuit.

### The LED

An **LED (light-emitting diode)** is a diode that gives off light when current flows through it in the forward direction. Everything about diodes applies: it has an anode and a cathode, it conducts only one way and it has a forward voltage. Unlike an ordinary diode, its forward voltage depends on its colour, and it is typically higher than 0.7 V.

- **Polarity.** On a typical through-hole LED, the longer leg is the anode and the side of the body with a flat edge is the cathode. If you are unsure, check with the datasheet or test carefully with a proper resistor in place. A reversed LED does not light, and simply blocks the current.
- **Current, not voltage, sets the brightness.** Above its forward voltage, a small increase in voltage causes a large increase in current. This is why an LED always needs a resistor in series to set the current.
- **Forward voltage varies.** Red LEDs are typically around 2 V, and blue and white LEDs are typically higher (often around 3 V). These are typical values, and the datasheet of your LED gives the actual ones.

![Connecting an LED: direct connection versus a series resistor, and the resulting circuit examples](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-03-led-with-resistor.png)

Recall the design method you already know: use KVL to find the voltage across the resistor, and Ohm's Law to find its value.

**Worked example (recalled).** 3.3 V supply, red LED with forward voltage about 2.0 V, target current about 10 mA.
V_resistor = 3.3 − 2.0 = 1.3 V, so R = 1.3 V ÷ 10 mA = 130 Ω. The nearest standard value, 150 Ω, gives I = 1.3 ÷ 150 ≈ 8.7 mA.

---

## The Capacitor: A Small Reservoir of Charge

A **capacitor** stores a small amount of electrical charge, and with it a small amount of energy, and releases it when the circuit needs it. A reasonable picture is a small water tank connected to a pipe: if the supply flow dips momentarily, the tank tops it up, and if the supply surges, the tank absorbs some of the surge.

Inside, a capacitor is two conductive plates separated by an insulating layer. The amount of charge it can store for a given voltage is its **capacitance**, measured in **farads (F)**. Real capacitors are much smaller than one farad, so you will see **microfarads (µF)**, **nanofarads (nF)** and **picofarads (pF)**.

### What Capacitors Do in Circuits

- **Smoothing and stabilising a power supply.** Many circuits, including microcontroller boards, draw current in sudden bursts. A capacitor placed close to the part supplies those bursts and keeps the supply voltage steady. You will find small capacitors near almost every chip on a board for this reason.
- **Timing and filtering.** A capacitor charges and discharges through a resistor at a predictable rate. That behaviour can create a delay, or smooth out a noisy signal.

### Charging Through a Resistor

When a capacitor is charged through a resistor, the voltage across it does not jump up instantly. It rises quickly at first, then more slowly. The speed is set by the **time constant**:

```text
time constant = R × C
```

After one time constant, the capacitor has reached about **63%** of the supply voltage. After about five time constants, it is essentially fully charged.

> **Example values.** R = 10 kΩ and C = 100 µF gives R × C = 10,000 Ω × 0.0001 F = **1 second**. The capacitor reaches roughly 63% of the supply voltage in about 1 second, and is nearly fully charged after about 5 seconds.

![The capacitor charging curve: voltage rises quickly at first, reaching about 63% after one time constant](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-04-capacitor-charging-curve.png)

Notice how this connects to what you already know: the resistor limits the current, which limits how quickly the charge can accumulate on the capacitor. A larger resistor or a larger capacitor makes the process slower.

### Polarity and Handling

Some capacitors, especially larger-value **electrolytic** capacitors, are **polarised**: they have a positive and a negative side, marked on the body, and must be connected the right way round. Connected backwards, they can overheat, leak or even burst. Ceramic capacitors of small value have no polarity. Charged capacitors can hold their voltage after the power is disconnected, so allow large capacitors to discharge before handling a circuit.

---

## The Button: A Switch You Can Press

A **button** is the simplest way for a person to give a circuit an input. Electrically, a **momentary pushbutton** is a switch that closes a path while you hold it and opens it again when you release it.

A button does not produce a voltage of its own. It only opens or closes a path. That sounds simple, but it creates a problem that matters a lot in IoT hardware, so it is worth working through carefully.

![A tactile pushbutton, its schematic symbol, and its released/pressed states](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-05-button-intro.png)

> **Practical tip.** A common four-legged tactile button has its legs connected in pairs *inside* the body. Two legs on the same side are always connected, and pressing the button connects one pair to the other. If your button seems to be permanently "on" or never works, check its legs with a multimeter's continuity setting to see which pins are connected, both pressed and released.

### Making a Button Readable

Imagine we want a circuit to *know* whether a button is pressed. The circuit needs to see a clear voltage: one value for pressed, another for released.

Suppose one side of the button is connected to ground, and the other side goes to an **input pin**, a connection that measures voltage without supplying any significant current itself. (In the next part of this reading, you will learn what such a pin belongs to. For now, think of it as a very sensitive voltmeter.)

- When the button is pressed, the pin is connected to ground, and it reads 0 V. 
- When the button is released, **the pin is connected to nothing at all**.

That second case is the problem. An input that is connected to nothing is said to be **floating**. A floating input has no defined voltage. It can pick up electrical noise from the surrounding air, your hand or nearby wires, and its reading may flicker unpredictably.

![A floating input pin's voltage over time: undefined and flickering compared with a clean pressed or released reading](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-06-floating-input.png)

The fix is to give the pin a default voltage using a resistor. This is called a **pull-up** or **pull-down** resistor:

```text
      Pull-up arrangement                 Pull-down arrangement

        3.3 V                                  3.3 V
          │                                      │
     [ R_pullup ]                            [ Button ]
          │                                      │
          ├──────► to input pin                  ├──────► to input pin
          │                                      │
     [ Button ]                            [ R_pulldown ]
          │                                      │
         GND                                    GND
```

**Pull-up arrangement**

- Button released: no path to ground, so the input pin is pulled up to the supply voltage (3.3 V) through the resistor. The pin reads **HIGH**.
- Button pressed: the pin is connected directly to ground. The pin reads **LOW**.

So with a pull-up, *pressed means LOW*. This surprises many beginners, and it is called **active-low** behaviour.

**Pull-down arrangement** is the mirror image. Released reads LOW; pressed connects the pin to 3.3 V and reads HIGH.

We used the words **HIGH** and **LOW** without defining them, so let us do that. A **digital signal** has only two meaningful states. HIGH means "the voltage is near the supply voltage" (3.3 V in a 3.3 V system), and LOW means "the voltage is near 0 V".

### A Resistor Value You Can Now Justify

Why 10 kΩ, and not 100 Ω? Work it out using what you already know. When the button is pressed in the pull-up arrangement, the resistor sits directly between 3.3 V and ground.

- Current: 3.3 V ÷ 10 kΩ = **0.33 mA**, a very small current.
- With 100 Ω instead: 3.3 V ÷ 100 Ω = **33 mA**, which wastes energy and would drain a battery for no reason.

The resistor should be large enough to waste almost no current when the button is pressed, and small enough that the input is firmly pulled to its default voltage when the button is released. Values around 10 kΩ are common. (Microcontrollers often have pull-up and pull-down resistors built in, which you can switch on from software. We will see how in a moment.)

### Contact Bounce

Mechanical contacts do not close cleanly. As the metal surfaces meet, they bounce apart and together several times in a few milliseconds before settling. A fast circuit sees that as several presses instead of one. This is called **contact bounce**, and the technique of ignoring it is called **debouncing**. It can be done in software by ignoring changes that occur too soon after the previous one, or in hardware using a resistor and capacitor, which is the same timing behaviour you met above.

![Contact bounce: a single physical press produces several electrical transitions, until debouncing cleans it into one change](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-07-contact-bounce.png)

---

## The Transistor: A Small Signal Controlling a Larger Flow

So far, every component we have discussed either limits, directs, stores or opens and closes a path by hand. The transistor does something different, and it is the most important component in modern electronics.

### The Problem It Solves

Recall from the earlier discussion of power that there are two separate checks when connecting a load: does the voltage match, and can the supply provide the current? The connections of a microcontroller that carry signals to the outside world are designed to carry small signal currents, not to power a motor or a heater. Yet a motor, a pump or a strip of bright LEDs may need much more current than such a connection can safely supply.

What we need is a way for a **small electrical signal** to **switch a much larger current** on and off, with the larger current coming from a separate power source. A **transistor** does exactly this. You can think of it as an electrically controlled switch, where a small control signal plays the role of the finger that presses the button.

> **Teaching model.** Transistors can also *amplify* signals, and they can behave as switches. In this course we focus on the switching role, which is the one most needed to connect a microcontroller to a real load.

### Terminals and Types

A transistor has three terminals. One is the **control** terminal, and the other two carry the switched current. The two families you will meet most often are:

| Type | Control terminal | Switched terminals | How it is controlled |
|---|---|---|---|
| **BJT** (bipolar junction transistor) | Base | Collector and emitter | A small **current** into the base allows a larger current from collector to emitter |
| **MOSFET** | Gate | Drain and source | A **voltage** at the gate controls the flow from drain to source, with almost no current entering the gate |

![BJT and MOSFET transistors: their terminals and how each one is controlled](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-08-bjt-vs-mosfet.png)

Each family comes in two polarities (for example, NPN and PNP for BJTs, N-channel and P-channel for MOSFETs). For switching a load to ground, which is the most common arrangement for a beginner, an **NPN** BJT or an **N-channel MOSFET** is typically used.

### The Standard Low-Side Switch

The most useful arrangement puts the load between the power supply and the transistor, and the transistor between the load and ground. This is called a **low-side switch**:

```text
      Load supply (+)
            │
        [  LOAD  ]      (motor, buzzer, relay coil, LED strip…)
            │
            ├──────── Collector / Drain
         [ Transistor ]  ◄──── [ resistor ] ◄──── control signal
            │                                       (from a microcontroller pin)
            └──────── Emitter / Source
            │
           GND  ◄────────────── shared with the microcontroller's ground
```

![The low-side switch: a small control signal at the transistor switches a larger load current to ground](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-09-lowside-switch.png)

Read it like this: when the control signal is low, the transistor is off, no current flows through the load, and it is off. When the control signal is high, the transistor turns on, and current flows from the supply through the load and the transistor to ground.

Three practical points decide whether such a circuit works:

- **A common ground.** The load's power supply and the microcontroller must share a ground connection. Without it, the control signal has no reference, and the transistor cannot tell whether it is on or off.
- **The resistor at the control terminal.** With a BJT, a resistor sets how much current flows into the base and protects the source of the control signal. MOSFETs draw almost no current at the gate, but a small resistor there is still common practice.
- **Matching the transistor to the job.** Check the transistor's maximum current and voltage against the load. Also, when the control signal comes from a 3.3 V microcontroller, a MOSFET must be a **logic-level** type, meaning one that turns fully on at that gate voltage. A standard MOSFET may turn on only partially at 3.3 V and get hot. The datasheet's gate threshold and on-resistance figures at your actual drive voltage tell you which you have.

![Why the transistor needs a common ground: without one, the control signal has no reference and the transistor cannot switch the load](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-10-common-ground.png)

### Protecting the Circuit from Motors and Coils

Motors, relay coils and solenoids contain coils of wire. A coil resists sudden changes in current. When the transistor switches the load off, the coil tries to keep the current flowing, and it can generate a brief, high voltage spike that may damage the transistor.

![What happens when a motor switches off: the coil's stored energy produces a brief, damaging voltage spike](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-11-motor-voltage-spike.png)

The remedy is a **flyback diode** (also called a freewheeling diode) placed across the load, pointing so that it normally does not conduct:

```text
      Load supply (+) ───┬───────────┐
                         │           │
                     [ Diode ]    [ LOAD ]
                  (stripe/cathode     │
                    toward +)         │
                         │           │
                         └─────┬─────┘
                               │
                     to the transistor
                     (collector / drain)
```

![The flyback diode gives the coil's current a safe loop to circulate in, protecting the transistor from the voltage spike](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-12-flyback-diode.png)

The diode's stripe (cathode) is connected towards the positive supply. During normal operation, the diode is reverse-biased and does nothing. When the transistor switches off and the coil produces a spike, the diode gives that current a safe loop to circulate in until the energy fades. This is the second protective job for a diode, mentioned earlier.

> **Assumption.** Many ready-made relay and motor-driver boards already include the transistor and the protective diode on the board, so you may not build these yourself. The principles are what matter, because they explain what those boards contain and why they behave as they do.

### Relays

A **relay** is another way to let a small signal switch a larger load. It contains a coil that becomes an electromagnet, pulling a mechanical contact closed. Relays provide electrical separation between the control side and the load side, and can switch loads a small transistor cannot. They are slower, they click, and their contacts wear out. In this course, all loads will be low-voltage, and switching household mains is outside the scope of your experiments.

---

## Combining Components into a Useful Circuit

Each component has a simple job. The skill is seeing how they combine. Consider a circuit that lights an LED while a button is pressed, using nothing but a supply, a button, a resistor and an LED, all in series:

```text
      3.3 V ──[ Button ]──[ 150 Ω ]──[ LED ]── GND
```

![What each component contributes: removing the button, resistor or LED changes the circuit's behaviour in a different way](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-13-circuit-fault-injection.png)

Every component plays its role: the button opens and closes the path, the resistor sets the current and the LED converts current into light. There is no microcontroller yet, and no program. It is a simple series circuit, and you can already analyse it: with the button pressed, the current is about 8.7 mA, and with it released, the current is zero.

Add a microcontroller and the same pieces can behave differently, because the program can decide *what a button press means*. It could light an LED, or count presses, or send a message. That difference is the value of putting a microcontroller in the loop, and we return to it shortly.

### A Quick Reference for the Components

| Component | What it does | Polarity? | Typical role in an IoT circuit | Common mistake |
|---|---|---|---|---|
| **Resistor** | Opposes current | No | Limits current, forms voltage dividers, sets pull-up and pull-down levels | Wrong value, or exceeding its power rating |
| **Diode** | Lets current flow one way | Yes (anode, cathode) | Reverse-polarity protection, absorbing voltage spikes | Connecting it backwards |
| **LED** | Diode that emits light | Yes | Indicator, simple output | No series resistor, or reversed |
| **Capacitor** | Stores small amounts of charge | Some types do | Smoothing supplies, timing, filtering | Reversing an electrolytic capacitor |
| **Button** | Opens or closes a path when pressed | No | Human input | Leaving the input floating, ignoring bounce |
| **Transistor** | Small signal switches a larger current | Yes (three terminals) | Driving motors, buzzers, relays, LED strips | No common ground, wrong terminals, unsuitable type |

---
