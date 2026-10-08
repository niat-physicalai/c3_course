# From the Physical World to Your First IoT System

### Welcome to Applied IoT

If you can write programs, you already know how to make a computer follow instructions. This course is about what happens when those instructions leave the screen: when a program can **notice** something in the real world, **decide** what to do about it and **change** something in the real world as a result.

That is the heart of the **Internet of Things (IoT)**. A street light that turns on at dusk, an irrigation system that waters a field only when the soil is dry, a wearable band that warns you about an unusual heart rate: each of these is software working together with physical hardware, and usually with a network as well. Put simply, IoT is about giving physical things the ability to **sense**, to **act** and to **share information**.

### Software on a Screen vs Software in the World

Most software you have written so far lives entirely inside a computer. Its inputs are data (keystrokes, files, network messages) and its outputs are data (text, pixels, files). If something goes wrong, you get an error message.

An IoT system is different in three ways:

- **Its inputs are physical.** Light, temperature, motion, moisture, sound and distance are not numbers until something converts them into numbers.
- **Its outputs are physical.** A program cannot switch on a lamp or turn a motor by itself. Something has to deliver real electrical power to that lamp or motor.
- **It usually talks to other systems.** Devices share what they sense, and can be monitored or controlled from somewhere else.

These differences change how you have to think. Real hardware is noisy, it can be wired incorrectly, it drifts, it overheats and its battery runs out. A large part of becoming an IoT engineer is learning to reason about the physical side, not just the code.

### The Building Blocks That Connect Software to the World

A program running on a processor can only deal with electrical signals. To connect it to the physical world, we need a short chain of parts, each with a clear job:

```text
Sensor → Microcontroller → Actuator
```

- A **sensor** converts a physical condition (light, temperature, distance…) into an electrical signal.
- A **microcontroller** is a tiny computer on a single chip. It reads those signals, runs your program and produces electrical outputs. In this course, that role is played by the **ESP32-S3**.
- An **actuator** converts electrical signals and energy into a physical effect: light, motion, sound or heat.

Joining these parts together is the job of **electronics**: supplying each part with the right power, shaping signals so they can be read, and protecting components from damage. Each part is introduced properly in the pages and modules ahead.

### The Journey of This Course

Across the course, you will gradually build connected physical systems. It helps to see the whole path from the start:

```text
Sense → Compute → Actuate → Communicate → Understand → Automate
```

- **Sense** — measure the physical world.
- **Compute** — decide what to do, using a program on a microcontroller.
- **Actuate** — change the physical world.
- **Communicate** — share data and receive commands over a network.
- **Understand** — make sense of collected data, using analysis, AI and vision.
- **Automate** — let systems make decisions and act reliably, on their own.

You do not need to memorise this list. Think of it as a map. Each stage builds on the one before it, and you will visit each one properly in the modules ahead.

### Begin with Electricity and Circuits

Every stage on that map rests on the same foundation: **electrical behaviour**. Sensors produce voltages. Microcontrollers run on voltages and currents. Actuators need power. If you understand only enough electronics to copy a wiring diagram, you can build something that works once, but you cannot explain why it works, why it fails, or why a small change destroyed a component.

So we begin here:

> Before we can build connected physical systems, we first need to understand what is happening underneath them.

This reading has three main sections. **Understanding IoT Systems** looks at IoT systems as a whole: the loop of sensing, computing and acting that every physical system follows. **The Electrical Foundation** builds the electrical knowledge that makes that loop work. **Building Safely and Thinking Like an Engineer** teaches you to work safely with circuits and to think like an engineer when they do not behave as expected.

### Learning Outcomes

By the end of this Reading Material, you will be able to:

- Explain how a physical system **senses**, **computes** and **acts**, using real IoT systems as examples.
- Describe how Physical AI, IoT and AIoT relate to each other, and where each one adds something new.
- Explain **voltage, current and resistance**, and use **Ohm's Law** and **power** to predict what a simple circuit will do.
- Analyse **series** and **parallel** circuits, and use **KVL** and **KCL** to check your reasoning.
- Work with low-voltage circuits **safely**, and troubleshoot them in a systematic order instead of guessing.

> **How to read the labels in this material.** Three kinds of statements appear here, and it helps to know which is which.
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. Real parts vary, and the **datasheet** (the manufacturer's official specification document for a part) always wins.
> - **Assumption** — something this reading assumes because the course kit or later units will define it precisely.

# Understanding IoT Systems

## From Software to the Physical World

Think about a street light that turns itself on at dusk. Nobody walks up to it and presses a switch. Nobody tells it that evening has arrived. Yet at roughly the right moment, it responds.

For that to work, several things must be true inside the device:

1. Something must **notice** that the light level has dropped.
2. Something must **decide** that "dark enough" has been reached.
3. Something must **switch the lamp on**.

Nothing about this is magic, and none of it is limited to street lights. A phone that rotates its screen, an air conditioner that holds 24 °C, a warehouse robot that stops before hitting a person and a smartwatch that warns you about an unusual heart rate all follow the same underlying pattern.

Before we look at how such a system is built, it helps to understand what changes when a program has to deal with the real world.

### When Software Has to Touch the World

![Traditional software versus physical computing: input, processing and output on each side](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-02-physical-computing-overview.png)

Most programming you have done so far lives entirely inside a computer. A variable holds a number, a function returns a value, and if something goes wrong you get an error message. The inputs and outputs are data.

**Physical computing** is what we call the practice of building systems where computation is connected to the physical world through hardware. The inputs are real quantities such as light, temperature, motion or pressure. The outputs are real effects such as a lamp turning on, a motor turning or a buzzer sounding.

> **Teaching model.** "Physical computing" is used here as an umbrella idea: *hardware that lets a program observe and change something physical.* Different textbooks draw the boundary slightly differently, but this working definition is enough for the course.

Moving from data to the physical world changes the rules of the game. It is worth being aware of these changes early, because they explain many of the design decisions you will meet later.

- **The world is noisy.** A temperature sensor does not report the "true" temperature. It reports a value affected by the sensor's accuracy, electrical noise and where it was placed.
- **Time matters.** A web page that loads 200 ms late is a minor annoyance. A robot that reacts 200 ms late may already have hit the obstacle.
- **Actions have consequences.** A wrong line of code in an app can be undone. A motor that has already moved a robot arm cannot be undone.
- **Hardware fails in ways software does not.** Wires come loose, batteries run down, components overheat.
- **Energy is limited.** Every sensor, processor and motor draws power, and that power comes from a battery or a supply with limits.

Keep these five points in mind. You will see them again in the electrical sections of this module, because a large share of "the program is wrong" problems in physical systems are actually "the circuit is wrong" problems.

### The Sense → Compute → Actuate Loop

![The Sense, Compute, Actuate loop illustrated with a street light](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-03-sense-compute-actuate.png)

The differences listed above may make physical systems sound chaotic. Yet almost all of them, from a street light to a warehouse robot, are organised around the same small loop.

Every system we have mentioned so far can be described by one small loop:

```text
        Physical World
         │          ▲
         ▼          │
       SENSE     ACTUATE
         │          ▲
         ▼          │
         └─ COMPUTE ┘
```

Read it in a straight line as **Sense → Compute → Actuate**, and remember that the last arrow feeds back into the physical world. This is the central mental model of the course, and we will keep coming back to it.

| Stage | What it does | What goes in | What comes out | Example |
|---|---|---|---|---|
| **Sense** | Converts a physical quantity into an electrical signal | Light, heat, sound, motion, pressure, distance… | A voltage (or another electrical signal) | A light sensor, a temperature sensor |
| **Compute** | Interprets the signal and decides what to do | The sensor signal, converted to a number | A decision, and a command | A microcontroller running a program |
| **Actuate** | Converts a command into a physical effect | An electrical signal and electrical power | Light, motion, sound, heat… | An LED, a motor, a buzzer, a heater |

Two details in that table deserve a closer look.

First, the **sensor's job is translation**. Software cannot read "brightness". A sensor turns brightness into something electrical, usually a **voltage** that changes as the brightness changes. (Voltage is a measure of electrical "push", which we will explain properly in the Electrical Foundation section.) The microcontroller then turns that voltage into a number it can work with. So the real path of information looks like this:

```text
Light level → Sensor circuit → Voltage → Number in the program → Decision → Electrical output → Lamp
```

Second, the **actuator needs power, not just a command**. A small signal can *tell* a motor to move, but it cannot *move* it. Turning a decision into a physical effect takes real electrical energy. You will see, when we reach power, why this makes actuators special.

#### The Street Light, Step by Step

Here is the street light written as the loop, using simple pseudo-code so we are not tied to a particular language yet:

```text
every 100 milliseconds:
    brightness = read_light_sensor()       # SENSE:   a number from 0 (dark) to 100 (bright)

    if brightness < 30:                    # COMPUTE: compare against a threshold
        lamp = ON
    else:
        lamp = OFF                         # ACTUATE: drive the lamp
```

> **Example values.** The 0–100 scale, the threshold of 30 and the 100 ms interval are chosen only for illustration.

This is only a few lines, but it already raises real engineering questions:

- **What happens when the brightness hovers around 30?** The reading fluctuates a little because of noise, so the lamp may flicker on and off. Engineers often solve this by using two thresholds, one to switch on and a lower one to switch off. This idea is called *hysteresis*. Could you modify the program to use it?
- **What if the lamp's own light reaches the sensor?** The lamp turns on, the sensor sees more light, the program decides it is bright and turns the lamp off, and now it is dark again. Where would you place the sensor to avoid this?
- **What if the sensor fails and always reads 0?** The lamp would stay on all day. Is that acceptable? What would a safer design do?

Notice that none of these questions is about the definition of "sense", "compute" or "actuate". They are about *how well the loop behaves in the real world*, and that is the kind of thinking this course is trying to build.

#### Closing the Loop

The street light has an interesting property. What the lamp does (making light) *can* affect what the sensor sees. When the action of a system affects what it senses next, we say the loop is **closed**. A thermostat is a clearer example: cooling the room changes the temperature that the sensor reads, which changes the next decision.

Compare that with a simple timer that turns a lamp on at 6:30 pm every day. It never looks at the world, so it cannot notice a cloudy afternoon or a power cut. It is an **open-loop** system. Closed-loop systems can react to what is actually happening, which is a large part of why they feel "smart".

### From a Standalone System to an IoT System

![A smart device that works on its own compared with an IoT device that also communicates over a network](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-05-standalone-vs-iot-device.png)

So far, our street light does everything by itself: sensing, deciding and switching all happen inside the device. A small computer built into a device to carry out one dedicated job like this is called an **embedded system**. On its own, an embedded system is self-contained. It does not share what it knows, and it does not listen for instructions from outside.

Now suppose the street light also reports its state to a control room and can be switched off remotely during maintenance. It now does something new: it **shares information and can be influenced from far away**. That is the step from a standalone system to an IoT system.

The **Internet of Things (IoT)** is formally described by the International Telecommunication Union (ITU) as a global infrastructure that connects physical and virtual "things" so they can offer advanced services, building on existing and evolving communication technologies. Put simply for our purposes:

> **IoT = things that can sense and/or act, plus the ability to communicate over a network, plus the data and services built on that communication.**

A useful test is this. Take the smart street light and remove its network connection. If it still turns on at dusk, its core was an embedded system all along, with a network added on top. The network is what upgrades it to IoT, because the network is what lets data leave the device and commands arrive.

#### What Connectivity Changes

Connecting devices allows things a single device cannot do:

- **Remote monitoring** — checking the state of a pump or a sensor from anywhere.
- **Remote control** — switching a device, or updating its behaviour, without visiting it.
- **Collecting data at scale** — one soil sensor tells you about one field corner, but a hundred sensors tell you about a whole farm.
- **Coordination** — devices adjusting to each other, for example lights in a neighbourhood dimming together.

#### The Loop Can Be Spread Across Places

In a simple device, sensing, computing and actuating happen in the same box. In an IoT system, they can happen in different places. The computing might happen on a nearby computer (the **edge**) or on powerful remote servers reached over the internet (the **cloud**):

```text
[ Device A: SENSE ] ──network──► [ Edge or Cloud: COMPUTE ] ──network──► [ Device B: ACTUATE ]
```

This flexibility comes with trade-offs, and it is a good moment to think like an engineer:

| Where the computing happens | Advantages | Trade-offs |
|---|---|---|
| **On the device** | Fast response, works without a network, less data sent | Limited processing power and memory |
| **Nearby (edge)** | Faster than the cloud, more power than a small device | Needs extra hardware and setup |
| **In the cloud** | Very large computing power, easy to update, sees data from many devices | Depends on the network, adds delay, raises privacy and cost considerations |

Ask yourself: *what should happen to an automatic door sensor if the Wi-Fi drops?* If the answer is "it must still open", then the safety-critical decision belongs on the device, and the network is just an extra.

> **Scope note.** The details of networking, protocols and cloud platforms belong to later units. For now, just remember that **IoT adds communication to the sense → compute → actuate loop.**

### Adding Intelligence: AIoT and Physical AI

The street light's decision rule ("if brightness is below 30, switch on") was written by a person. This works well when the situation is simple and predictable. It works poorly when the situation is complicated. Imagine writing an exact rule to decide whether a fruit on a conveyor belt is ripe, using only a camera image, or whether a machine's vibration pattern means a bearing is about to fail.

For problems like these, the compute stage can use **artificial intelligence**: models that have learned patterns from data instead of following rules that a person wrote out one by one.

#### AIoT

**AIoT (Artificial Intelligence of Things)** refers to combining AI with IoT. Connected devices that used to only collect and forward data can now also interpret it: recognising patterns, detecting anomalies and making decisions. AIoT systems often run the AI model *on or near the device* (this is called **edge AI**), which reduces delay and reduces the amount of data that must be sent to the cloud.

> **Assumption.** In this course, "AI" in an AIoT context mainly means a trained model used inside the compute stage. How such models are built and deployed is covered in later modules.

#### Physical AI

**Physical AI** refers to AI systems that can perceive the real world, reason about it and take physical action. It typically brings together AI models, sensors such as cameras, control systems and actuators, so that the system can adapt when conditions change. Robots, autonomous vehicles, drones and smart factory machines are the standard examples.

What separates Physical AI from an AI model running on a website is the **loop**. A chatbot's output is text on a screen. A Physical AI system's output changes the physical world, and the physical world's response becomes its next input. That closed loop, with all the noise, delay and risk we discussed earlier, is what makes Physical AI both powerful and difficult.

#### How These Ideas Fit Together

```text
Physical computing   →   Hardware lets a program sense and act on the physical world
        │
        ▼
      IoT            →   Adds communication: data leaves the device, commands arrive
        │
        ▼
     AIoT            →   Adds AI in the compute stage of connected devices
        │
        ▼
  Physical AI        →   AI-driven perception, reasoning and action in the physical world
                         (robots, autonomous machines, smart factories…)
```

> **Teaching model.** These layers overlap heavily and different sources draw the lines differently. A warehouse robot can be described as Physical AI, as AIoT and as an IoT system at the same time, depending on which aspect you are discussing. Do not spend energy arguing about which label is "correct." Ask instead **what the system senses, how it decides and what it changes**. That question always has a clear answer, and it is the one this course cares about.

### Seeing the Pattern in Real Systems

Because the sense → compute → actuate pattern is so general, it appears across industries. The table below shows a few examples. Read across each row to see the loop.

| Domain | Example system | Senses | Computes | Actuates |
|---|---|---|---|---|
| **Agriculture** | Automatic irrigation | Soil moisture, weather | Is the soil too dry? Is rain expected? | Opens a valve, starts a pump |
| **Smart home** | Air conditioner or thermostat | Room temperature, occupancy | Compare against the target, decide cooling level | Compressor and fan speed |
| **Healthcare** | Wearable health band | Heart rate, motion | Detect abnormal patterns | Vibrates, sends an alert |
| **Industry** | Machine health monitoring | Vibration, temperature | Detect early signs of failure | Raises an alert, slows or stops the machine |
| **Logistics** | Warehouse robot | Camera, distance sensors | Recognise obstacles and choose a path | Motors steer and stop the robot |
| **Smart cities** | Adaptive street lighting or traffic signals | Light level, vehicle flow | Decide brightness or signal timing | Lamps, traffic lights |
| **Vehicles** | Automatic emergency braking | Radar, camera | Estimate collision risk | Brake system |

Two observations will help you when you analyse systems yourself.

**Actuation does not always mean motion.** In the wearable example, the "action" is a vibration and a message. In many industrial systems, the action is an alert to a person. When a human is part of the loop, we call it a *human-in-the-loop* system. That is still the same pattern, but the final "actuator" is a person who takes the physical action.

**The loop can be small or large.** The street light is one small loop. A smart city is thousands of such loops that also exchange information with each other.

#### A Method for Analysing a Real System

Throughout this module you will be asked to analyse real IoT systems. Here is a set of questions that works for almost any system. Answer them in order:

1. **Goal.** What is the system trying to achieve, and for whom?
2. **Sense.** What physical quantities does it measure? What kind of sensor might do that?
3. **Compute.** What decisions does it make? Are they simple rules or do they seem to require AI? Where might the computing happen: on the device, at the edge or in the cloud?
4. **Actuate.** What physical effect does it produce? Is a person part of the loop?
5. **Loop.** Is it open-loop or closed-loop? Does the action change what is sensed next?
6. **Communicate.** What data leaves the device, and what commands arrive? Which parts still work if the network is lost?
7. **Constraints.** What limits it: power source, cost, response time, safety, environment?
8. **Failure.** What happens if a sensor lies, a wire breaks or the network drops? Is the failure safe?

Practise this on a system you see every day. For instance, try the lift in your building, a smart meter, a ride-hailing app's vehicle tracking or a digital attendance device. You will find you can describe it in a few minutes, and you will also notice how much of what you described depends on **electrical signals**. That observation leads directly into the electrical foundation you need next.

---

# The Electrical Foundation

So far we have described IoT systems by what they sense, decide and do. Now we can look at what physically carries out each of those steps. Return to the loop and look at each arrow:

```text
Physical quantity ──► [ Sensor ] ──► electrical signal ──► [ Microcontroller ] ──► electrical signal + power ──► [ Actuator ] ──► Physical effect
```

- The **sensor** outputs an electrical signal. Usually that signal is a *voltage*.
- The **microcontroller** (the small computer that runs your program) runs on electrical power and represents information as voltage levels.
- The **actuator** needs electrical *power*: a certain voltage and a certain amount of current.

If you understand electricity only as "it makes things work", you can copy circuits from a diagram but you cannot tell why one works, why another fails or why a third one damages a component. If you understand it as *quantities that can be predicted and measured*, you can reason about a circuit before you build it, and you can find faults after you build it.

That is what this part is for. We will build the electrical foundation step by step: first the three basic quantities, then the rule that connects them, then how components behave when they are connected together. Along the way we will practise the habit of predicting what a circuit will do before we build it.

### Voltage, Current, and Resistance

Every circuit, from a single LED to the inside of a microcontroller board, can be described using three quantities. Before any formula, we need an intuition for each one, and the easiest place to start is the basic idea of a circuit.

#### Charge and the Idea of a Complete Loop

![A simple circuit: a source, a resistor and an LED forming a complete path](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-14-simple-circuit-loop.png)

All matter contains electric charge. In metals such as copper, some charges (electrons) are free to move. When they move in an organised way, we have an **electric current**. For that to happen, two things must exist:

1. Something that *pushes* the charges: a **source** such as a battery, a USB port or a power supply.
2. A **complete, closed path** for them to travel around: a **circuit**.

If the path is broken anywhere, nothing flows. The word "circuit" literally means a path that goes round and returns to where it started. A **switch** is simply a device that deliberately opens or closes this path.

A minimal circuit looks like this:

```text
        ┌──────[ Resistor ]──────[ LED ]──────┐
        │                                     │
      ( + )                                   │
     Supply                                   │
      ( − )                                   │
        │                                     │
        └─────────────────────────────────────┘
```

The supply pushes, the path is closed, and the LED and resistor are the "loads", the parts that use the electrical energy. (An **LED**, or light-emitting diode, is a small light source that glows when current flows through it in the right direction.)

Three quantities describe almost everything that matters in a simple circuit. It is worth building an intuition for each before using any formula.

#### Voltage — the "push"

**Voltage** is the difference in electrical potential energy, per unit of charge, between two points. In everyday terms, it is the electrical "push" available to move charge. Its unit is the **volt (V)**.

Three points about voltage matter more than they first appear.

- **Voltage is always between two points.** Saying "the voltage is 5 V" is incomplete. It should be "5 V *between* this point and that point". In most circuits we pick one point as a reference, called **ground (GND)**, and treat it as 0 V. Other voltages are then measured relative to it.
- **Voltage can exist without any current.** A battery sitting on a table has a voltage between its terminals even though nothing is flowing. The push is available; no path lets it act.
- **A voltage is measured *across* a component.** To measure it, you touch the two probes of the meter to the two ends of the component, in parallel with it.

Typical values you will meet in this course: a AA cell has a nominal 1.5 V; a USB port supplies nominally 5 V; and many modern microcontroller boards, including the ESP32 family from Espressif, operate their chips at 3.3 V.

> **Assumption.** The exact supply voltage and signal levels of your course hardware will be specified when the microcontroller is introduced. Always confirm them from the board's documentation before connecting anything.

#### Current — the "flow"

**Current** is the rate at which charge flows past a point. Its unit is the **ampere (A)**, where 1 A means one coulomb of charge passing per second. In electronics we usually work in **milliamperes (mA)**, where 1 A = 1000 mA.

- **Current is measured *through* a component.** To measure it, the meter must be placed *in the path*, in series, so that the current flows through the meter.
- **Direction convention.** By historical convention, current is drawn as flowing from the positive terminal, around the circuit, to the negative terminal. (The actual electrons in a metal move the opposite way, but the convention works perfectly well for analysis. We will always use the conventional direction.)
- **Current is not "used up".** A very common misconception is that the LED "consumes" current, so less current comes back than went in. In a simple loop, the current is the same at every point. What the LED converts into light and heat is *energy*, not charge.

#### Resistance — the "opposition"

**Resistance** describes how strongly a component opposes current flow. Its unit is the **ohm (Ω)**, and you will constantly see **kilo-ohms (kΩ = 1000 Ω)** and **mega-ohms (MΩ = 1,000,000 Ω)**.

- A **conductor**, such as copper wire, has very low resistance.
- An **insulator**, such as the plastic covering a wire, has extremely high resistance.
- A **resistor** is a component made to have a specific, known resistance, so that we can control how much current flows. In IoT circuits, resistors have two everyday jobs: **protecting components** by limiting current (as we will do with an LED) and **shaping signals** (as we will do with a voltage divider).

Resistors are marked with coloured bands that encode their value, and you can also measure their value with a **multimeter** (a handheld instrument that measures voltage, current and resistance) set to measure resistance, with the resistor removed from any powered circuit.

Resistance matters for IoT in a way that is easy to miss: **many sensors are simply components whose resistance changes with the physical world.** A light-dependent resistor's resistance falls as light increases. A thermistor's resistance changes with temperature. The voltage divider, later in this part, shows how that changing resistance becomes a changing voltage, which is exactly the "translation" performed by the sense stage.

#### A Water Analogy, and Where It Stops Working

| Water in pipes | Electricity in a circuit |
|---|---|
| Pressure difference | Voltage |
| Flow rate | Current |
| A narrow section of pipe | Resistance |
| A closed loop of pipe with a pump | A circuit with a source |

> **Teaching model.** This analogy helps build intuition: more pressure gives more flow, and a narrower pipe gives less flow. But it is only an analogy. A cut water pipe leaks onto the floor; a cut wire simply stops the current. Use the analogy to get a first feeling, then rely on the actual rules.

#### Direct and Alternating Current

Current can flow in two broad ways. In **direct current (DC)**, it flows in one direction all the time. Batteries and USB supplies provide DC, and every circuit in this course uses DC. In **alternating current (AC)**, the direction of flow reverses repeatedly. The electricity from a wall socket is AC; in India it completes 50 cycles every second (50 Hz). The rules in this part (Ohm's Law, series and parallel behaviour, Kirchhoff's laws and power) are described here for DC circuits.

### Ohm's Law

![Ohm's Law: V equals I times R, with a worked example and the cover-the-one-you-want triangle](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-16-ohms-law.png)

Now that we have met all three quantities, the natural question is how they relate to each other. Voltage, current and resistance are not independent. Think of voltage as the push, resistance as the opposition, and current as the result:

```text
Voltage (push) ──► [ Resistance (opposition) ] ──► Current (result)
```

For a resistor, the exact link between them is called **Ohm's Law**:

```text
V = I × R
```

where **V** is the voltage across the resistor (volts), **I** is the current through it (amperes) and **R** is its resistance (ohms). Rearranged:

```text
I = V ÷ R          R = V ÷ I
```

Read the middle form as a sentence: *the current through a resistor is the voltage across it divided by its resistance.* More voltage means more current; more resistance means less current.

A handy shortcut: when the voltage is in **volts** and the resistance is in **kilo-ohms**, the answer is in **milliamperes**. For example, 5 V ÷ 1 kΩ = 5 mA.

#### Feeling the Law with Numbers

Suppose a 5 V supply is connected across a single resistor. What happens to the current as we change the resistor?

| Resistance | Current (I = V / R) |
|---|---|
| 2 kΩ | 2.5 mA |
| 1 kΩ | 5 mA |
| 500 Ω | 10 mA |
| 100 Ω | 50 mA |

Look at the pattern instead of just the numbers. When the resistance is halved, the current doubles. Current and resistance are **inversely related** for a fixed voltage. And when the voltage doubles across the same resistor, the current doubles too.

A resistor does not "draw" a fixed current by itself. The current is the *result* of two things: how much voltage is applied and how much the resistor resists. Change either, and the current changes.

#### Where Ohm's Law Applies, and Where It Needs Care

![The LED problem: connecting an LED directly to a supply versus through a resistor](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-18-led-problem.png)

Ohm's Law describes **resistors** (and any component that behaves like one) very well. Not every component behaves that way. An LED is a good example: below a certain voltage it hardly conducts at all, and above it the current rises extremely steeply for a small increase in voltage. If you connect an LED straight across a supply with nothing to limit the current, it can be damaged in an instant.

That is why LEDs are almost always used **with a series resistor**. The resistor, which does follow Ohm's Law, sets the current. We will work through this design once we have one more tool, Kirchhoff's Voltage Law.

#### Open Circuits and Short Circuits

Ohm's Law also explains two extreme situations that you will meet often when debugging.

- **Open circuit.** The path is broken, so the resistance is effectively infinite, and the current is (almost) zero. A broken wire, a loose connection or an open switch all produce an open circuit.
- **Short circuit.** A path with almost no resistance connects two points that should not be connected directly, for example the two terminals of a supply. With R close to zero, I = V / R becomes very large, limited only by the source and the wires. That can cause overheating, damaged components and in serious cases fire.

```text
Open circuit:   R → very large   ⟹   I ≈ 0
Short circuit:  R → very small   ⟹   I → very large  (dangerous)
```

### Series Circuits

Ohm's Law describes a single resistor. Real circuits contain several components, so the next question is what changes when they are connected together. The simplest arrangement is a chain.

When components are connected **end to end** so that there is only one path, they are in **series**.

```text
        ┌────[ R1 ]────[ R2 ]────┐
        │                        │
      ( + )  5 V                 │
      ( − )                      │
        └────────────────────────┘
```

Three rules describe a series circuit:

1. **The same current flows through every component.** There is only one path, so charge has nowhere else to go.
2. **The total resistance is the sum:** R_total = R1 + R2 + …
3. **The supply voltage is shared between the components.** The voltages across the components add up to the supply voltage.

#### A Worked Example

Let R1 = 1 kΩ and R2 = 4 kΩ, connected to 5 V.

- Total resistance: 1 kΩ + 4 kΩ = **5 kΩ**
- Current (Ohm's Law): 5 V ÷ 5 kΩ = **1 mA**, the same through both resistors.
- Voltage across R1: 1 mA × 1 kΩ = **1 V**
- Voltage across R2: 1 mA × 4 kΩ = **4 V**
- Check: 1 V + 4 V = 5 V ✓

Notice that the **larger resistor takes the larger share of the voltage**. Keep this in mind, because it leads to one of the most useful ideas in sensor circuits, which we will meet shortly.

#### When a Series Circuit Breaks

Because there is only one path, **an open circuit anywhere stops the current everywhere**. In old-style decorative light strings wired in series, one burnt-out bulb turned the whole string off, and finding it meant testing bulb after bulb. Series circuits are ideal when you *want* the same current through everything (as in the voltage divider we meet shortly), and a poor choice when you want each part to work independently.

### Parallel Circuits

So far, the current has had only one route to follow. What if it has several?

When components are connected **side by side**, so that each one connects across the same two points, they are in **parallel**.

```text
        ┌─────────┬─────────┐
        │         │         │
      ( + )     [ R1 ]    [ R2 ]
      ( − )       │         │
        └─────────┴─────────┘
```

The rules mirror those of series circuits, but with the roles swapped:

1. **The same voltage appears across every branch.**
2. **The total current is the sum of the branch currents.**
3. **The total resistance is *smaller* than the smallest branch.**

For two resistors:

```text
R_total = (R1 × R2) ÷ (R1 + R2)
```

and for identical resistors, R_total = R ÷ (number of resistors).

#### A Worked Example

Two 100 Ω resistors are connected in parallel across 5 V.

- Each branch has 5 V across it, so each carries 5 V ÷ 100 Ω = **50 mA**.
- The total current from the supply is 50 mA + 50 mA = **100 mA**.
- The equivalent resistance is 5 V ÷ 100 mA = **50 Ω**, which matches 100 ÷ 2.

The result may feel strange at first: **adding a resistor made the total resistance go down.** The reason is that each new branch is a *new path*, and more paths make it easier, not harder, for current to flow overall. It is like opening extra checkout counters in a shop.

#### Parallel Circuits in IoT Hardware

- **Shared supply lines (power rails).** On a breadboard (a reusable board with holes for building circuits without soldering) or a circuit board, sensors, LEDs and other parts are usually connected across the *same* supply voltage. That is a parallel arrangement, and it is why each part gets its full rated voltage.
- **Independence.** If one branch opens, the others keep working. This is why the appliances in a home are wired in parallel.
- **Growing load.** Every extra branch increases the total current drawn from the supply. If you add enough sensors and actuators to the same supply, the total current may exceed what the supply can provide, and then its voltage sags or it overheats. We return to this when we look at power.

#### Series and Parallel Side by Side

![Series and parallel circuits compared side by side](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-21-series-vs-parallel.png)

| | Series | Parallel |
|---|---|---|
| **Paths for the current** | One | Several |
| **Current** | Same through every component | Splits among the branches; branch currents add up to the total |
| **Voltage** | Shared between components; the parts add up to the supply | Same across every branch |
| **Total resistance** | The sum, so larger than any single resistor | Smaller than the smallest branch |
| **If one part opens** | Everything stops | The other branches keep working |
| **Typical use in IoT hardware** | Current-limiting resistor with an LED; voltage dividers | Power rails; several devices sharing one supply |

#### Series-Parallel Circuits

Real circuits mix both patterns. A reliable way to analyse them is to **simplify step by step**: replace each parallel group with its single equivalent resistance, then replace series parts with their sum, until you have one resistance. Compute the current. Then work backwards, using the current to find the voltage across each part. The worked example in the discussion of Kirchhoff's laws demonstrates this.

### Voltage Dividers and Sensor Applications

A series circuit shares its voltage between components in proportion to their resistances. That simple fact, combined with sensors whose resistance changes, gives one of the most useful tricks in IoT hardware.

Suppose you connect two resistors in series and look at the voltage at the point *between* them:

```text
 3.3 V ───┬───
          │
        [ R_top ]
          │
          ├────────  V_out
          │
        [ R_bottom ]
          │
 GND ─────┴───
```

Since the current is the same in both and the voltage shares in proportion to resistance, the output is:

```text
V_out = V_in × R_bottom ÷ (R_top + R_bottom)
```

This arrangement is called a **voltage divider**. It is one of the most important small circuits in IoT, because it turns a **change in resistance into a change in voltage**.

Suppose R_top is a light-dependent resistor (LDR) and R_bottom is a fixed 10 kΩ resistor, powered from 3.3 V.

> **Example values.** The LDR resistances below are illustrative. A real LDR's values come from its datasheet.

| Condition | LDR resistance | V_out |
|---|---|---|
| Bright light | 1 kΩ | 3.3 × 10 / (1 + 10) = **3.0 V** |
| Darkness | 100 kΩ | 3.3 × 10 / (100 + 10) = **0.3 V** |

Light has become a voltage: high when bright, low when dark. This is the *sense* stage of the street light we started with. A microcontroller can now read this voltage and turn it into the number that the program compares with a threshold. (How that voltage-to-number conversion works is a topic for a later module.) The same idea works for any sensor whose resistance changes with a physical condition, such as a thermistor that changes with temperature.

**Think about it:** what would happen to V_out if you swapped the positions of the LDR and the fixed resistor? Predict the direction of the change before you work it out.

### Kirchhoff's Laws: KVL and KCL

Series and parallel rules are convenient, but they describe only two specific arrangements. It would be useful to have rules that work for *any* circuit.

Fortunately, the series and parallel rules are really consequences of two more basic ideas that hold for any circuit, however complicated. These are the Kirchhoff laws.

#### KVL — Kirchhoff's Voltage Law

![KVL: does the loop balance? The voltages around a closed loop sum to zero](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-23-kvl.png)

> **Around any closed loop, the voltage rises from sources equal the voltage drops across components.** Equivalently, if you add up all the voltages around a closed loop (rises positive, drops negative), you get zero.

Intuition: imagine a walk through hills that returns to its starting point. However much you climbed, you must have descended exactly as much, or you would not be back at the same height. In a circuit, the source "lifts" the electrical potential and the components let it "fall" back.

```text
Around the loop:   +5 V (source rise)   −1 V (drop)   −4 V (drop)   =   0
```

KVL is why the series example worked: 5 V (source) = 1 V + 4 V (drops).

#### KCL — Kirchhoff's Current Law

![KCL: does the junction balance? Current entering equals current leaving](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-24-kcl.png)

> **At any junction (node), the total current flowing in equals the total current flowing out.**

Intuition: charge does not pile up or vanish at a junction, just as water arriving at a pipe junction has to leave through the branches. 

```text
            ┌── 13.3 mA ──►
 20 mA ───► ●
            └──  6.7 mA ──►        20 = 13.3 + 6.7
```

KCL is why the parallel example worked: 100 mA leaving the supply splits into 50 mA + 50 mA and rejoins.

#### Using Both Together: A Worked Example

Here is a mixed circuit. R1 is in series with a parallel pair, R2 and R3, powered from 6 V.

```text
           node A                        node B
   ┌──[ R1 = 100 Ω ]──●──┬──[ R2 = 300 Ω ]──┬──●──┐
   │                     │                  │     │
 ( + ) 6 V               └──[ R3 = 600 Ω ]──┘     │
 ( − )                                            │
   └──────────────────────────────────────────────┘
```

**Step 1 — Simplify the parallel pair.**
R2 ∥ R3 = (300 × 600) ÷ (300 + 600) = **200 Ω**

**Step 2 — Total resistance.**
R_total = 100 + 200 = **300 Ω**

**Step 3 — Total current.**
I = 6 V ÷ 300 Ω = **20 mA**, and this is the current through R1.

**Step 4 — Voltage across each part.**
V across R1 = 20 mA × 100 Ω = **2 V**
V across the parallel pair = 20 mA × 200 Ω = **4 V**

**Step 5 — Branch currents.**
Through R2 = 4 V ÷ 300 Ω ≈ **13.3 mA**
Through R3 = 4 V ÷ 600 Ω ≈ **6.7 mA**

**Step 6 — Check your work with the laws.**
- KVL: 6 V = 2 V + 4 V ✓
- KCL at node A: 20 mA = 13.3 mA + 6.7 mA ✓

That last step is the real value of KVL and KCL. They give you **independent ways to check your own answers**. If your numbers fail these checks, you have made an error somewhere. The same idea works on a real circuit: if your measurements do not obey KVL and KCL, something is wrong with a connection, a component or the measurement itself.

#### Worked Example: Sizing a Resistor for an LED

![Why the resistor matters: it drops the extra voltage and limits the current to a safe value](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-25-why-resistor-matters.png)

Now we can return to the LED, which does not obey Ohm's Law by itself. The trick is that the *resistor* does, and KVL tells us what voltage the resistor must carry.

> **Example values.** Assume a red LED with a forward voltage of about 2.0 V and a desired current of about 10 mA, powered from 3.3 V. Real LEDs differ by colour and part number, so always check the datasheet for the LED you use.

**KVL around the loop:** supply = V_resistor + V_LED, so
V_resistor = 3.3 V − 2.0 V = **1.3 V**

**Ohm's Law for the resistor:**
R = V ÷ I = 1.3 V ÷ 10 mA = **130 Ω**

Resistors come only in standard values, and 130 Ω is not one of the common ones. A nearby standard value is 150 Ω. With that value:
I = 1.3 V ÷ 150 Ω ≈ **8.7 mA**

This is slightly less than 10 mA, so the LED will be very slightly dimmer, which is perfectly acceptable. Would it also have been acceptable to pick 120 Ω? Work out what current you would get, and decide which choice you would make and why.

Now try changing the situation in your head. If the same LED is powered from 5 V instead of 3.3 V, the resistor must carry more voltage. What resistor value would you need to keep the current near 10 mA?

---
