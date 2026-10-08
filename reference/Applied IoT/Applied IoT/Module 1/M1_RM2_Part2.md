# From Components to a Microcontroller-Controlled System (continued from Part 1)

> *This is Part 2 of the RM2 reading material. Part 1 covered Electronic Components: the resistor, diode, LED, capacitor, button and transistor. This part continues with Sensors and Actuators, and The Microcontroller (processing, memory, peripherals and GPIO).*

---

# Sensors and Actuators

## Inputs and Outputs in a Physical Computing System

Now step back from individual components and look at a whole system. Every physical computing system has parts that bring information *in* and parts that send effects *out*. We use the words **input** and **output** for these, and it is important to notice **from whose point of view** they are defined: the **microcontroller's**.

- An **input** is anything that sends information *into* the microcontroller: a button, a light sensor, a temperature sensor.
- An **output** is anything the microcontroller sends signals *out* to: an LED, a buzzer, a motor.

In terms of our loop:

```text
Physical world ──► SENSOR ──► [ INPUT ] ──► MICROCONTROLLER ──► [ OUTPUT ] ──► ACTUATOR ──► Physical world
```

![Inputs bring the world in as sensor signals; outputs send the microcontroller's decisions out to actuators](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-14-inputs-outputs.png)

A person can be part of the loop too. A button is an input operated by a person, and a display is an output read by a person.

## Sensors: Turning the Physical World into Signals

A **sensor** converts a physical quantity, such as light, temperature, distance, motion or moisture, into an electrical signal that a circuit can work with. You have already met the idea: the LDR and fixed resistor in a voltage divider *is* a light sensor, because it turns brightness into a voltage.

### Three Kinds of Sensor Output

It helps to sort sensors by what they hand to the microcontroller, because that decides how the microcontroller has to read them.

```text
Digital (two states):       ─────┐        ┌─────        HIGH
                                 └────────┘             LOW

Analog (any value in a      ╭──╮      ╭──╮
range):                   ──╯  ╰──────╯  ╰──
```

| Output type | What the signal looks like | Examples | What it means for the microcontroller |
|---|---|---|---|
| **Digital (on/off)** | Only two levels: HIGH or LOW | Button, tilt switch, magnetic door switch, many motion-sensor modules | Read directly as HIGH or LOW |
| **Analog** | A voltage that varies smoothly over a range | LDR or thermistor in a voltage divider, potentiometer, many simple temperature sensors | Measure the voltage and convert it to a number (this is the job of an **ADC**, an analog-to-digital converter, which we look at soon) |
| **Digital data** | The sensor contains its own electronics, and sends its measurement as a numerical message | Many temperature, humidity, pressure and motion sensors | The microcontroller receives numbers through a communication interface such as **I2C** or **SPI** (introduced in later modules) |

![Three concrete sensors, one for each output type: a button (digital), an LDR (analog) and a temperature/humidity module (digital data)](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-15-three-sensor-types.png)

The first two kinds are close to the raw physical signal. The third does more of the work inside the sensor, and is common in modern IoT sensor modules.

> **Assumption.** Whether a particular sensor module is analog, digital or a data-sending type depends on the module. Always check the datasheet or the module's documentation.

### What to Know About Any Sensor

Whatever the sensor, a handful of questions help you understand what you are dealing with:

- **What does it measure?** (Light, temperature, distance…)
- **What range can it measure, and how precisely?** A sensor that measures 0 to 50 °C is not suitable for a freezer.
- **What signal does it output?** (Digital, analog, or data.)
- **What supply voltage does it need, and how much current does it draw?**
- **How fast does it respond?** Some sensors take seconds to settle.

Also remember a lesson from the start of this module: **a sensor never reports the "true" value.** Its reading is affected by accuracy, noise, placement and the environment. A temperature sensor placed next to a warm chip may measure the chip's warmth instead of the room's.

### Some Common Sensors

> **Teaching model.** The output types in this table are typical. Individual modules vary.

| Physical quantity | Typical sensors | Typical output |
|---|---|---|
| Light level | LDR in a voltage divider, light-sensor modules | Analog voltage, or digital data |
| Temperature | Thermistor in a voltage divider, temperature-sensor modules | Analog voltage, or digital data |
| Motion or presence | PIR (passive infrared) motion sensor modules | Often a digital HIGH/LOW signal |
| Distance | Ultrasonic distance sensors, infrared proximity sensors | Pulse timing, digital data or analog voltage, depending on the module |
| Soil moisture | Resistive or capacitive moisture probes | Analog voltage |
| Human input | Button, potentiometer (a knob) | Digital or analog |

## Actuators: Turning Decisions into Physical Effects

An **actuator** does the opposite of a sensor. It converts electrical energy into a physical effect: light, motion, sound, heat or a change in flow. A sensor gathers information and needs very little power. An actuator *does something in the world* and often needs substantial power.

```text
Sensor:     physical condition ──► electrical signal      (small power)
Actuator:   electrical signal + power ──► physical effect (often larger power)
```

### Common Actuators and How They Are Driven

| Actuator | Physical effect | How it is usually driven from a microcontroller |
|---|---|---|
| **LED** | Light | Directly from an output connection, through a series resistor, for a small indicator LED |
| **Buzzer** | Sound | Directly for a very small buzzer, or through a transistor for a louder one (see the note below) |
| **DC motor** | Rotation | Through a transistor or a motor-driver module, with a protective diode |
| **Servo motor** | Rotation to a chosen angle | A control signal to the servo, plus a separate power supply for it (control signals are covered in a later module) |
| **Relay** | Switches another circuit | Through a transistor, or via a relay module |
| **Solenoid valve or pump** | Controls the flow of liquid | Through a transistor with a protective diode, or via a driver module |
| **Display** | Shows text or graphics | Through a communication interface (later module) |

The pattern is consistent: the microcontroller provides a **small control signal**, and anything that needs real power gets it from a **separate supply**, switched by a transistor or a driver. That is the reason for the transistor discussion earlier.

> **Note: Two kinds of buzzer.** An **active buzzer** contains its own oscillator: apply a steady voltage and it makes a fixed tone. A **passive buzzer** has no oscillator, and needs a changing signal from the microcontroller to produce a tone, whose pitch is set by the signal's frequency. They can look identical from outside, and they need different control. If a buzzer stays silent on a steady voltage, ask which type you have.

### Is an LED a Sensor or an Actuator?

An LED that lights up to show a status is an **output**, because it is driven by the microcontroller and produces a physical effect (light). It therefore counts as a simple actuator. The boundary is not sharp: some engineers would call it an "indicator" and reserve "actuator" for parts that move or switch things. For this course, the working test is simple. **Does it push something out into the physical world? Then it is on the output side.**

## The Signal Path: Sensor → Microcontroller → Actuator

Now we can trace a complete path through a system, using the loop you already know with real components in each box. Consider an **automatic night light**: a lamp that comes on when the room gets dark.

```text
Room brightness
     │
     ▼
[ LDR + fixed resistor ]     SENSOR: brightness → voltage (voltage divider)
     │  varying voltage
     ▼
[ Microcontroller input ]    INPUT: voltage → number
     │
     ▼
[ Program compares with threshold, decides "dark" or "bright" ]    COMPUTE
     │
     ▼
[ Microcontroller output ]   OUTPUT: decision → HIGH or LOW signal
     │
     ▼
[ Resistor + LED ]           ACTUATOR: signal + power → light
     │
     ▼
Light in the room
```

![The complete signal path of the automatic night light: brightness in, light out, step by step](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-16-signal-path-nightlight.png)

Follow the *form* of the signal at each hop: brightness (physical) → a resistance change → a voltage → a number in a program → a decision → a voltage on a pin → a current through an LED → light (physical). Being able to name the form of the signal at every hop is exactly the skill of **analysing a signal path**.

### What the Microcontroller Adds

A fair question to ask here: could you build a night light without a microcontroller? Yes. A simple circuit with an LDR and a transistor can switch a lamp on when it gets dark. For a single, unchanging job, that is perfectly good engineering.

A microcontroller earns its place when the behaviour needs to be *programmable*:

- **Changeable decisions.** Change the threshold, add a delay or add a second sensor by changing the program instead of rebuilding the circuit.
- **Combining inputs.** Decide based on several sensors at once, such as light *and* time *and* motion.
- **Memory and timing.** Remember what happened earlier, and act after a delay.
- **Communication.** Share readings or receive commands over a network, which is what turns a device into an IoT device.

The microcontroller sits between the inputs and outputs because it is the one part that can **interpret** signals and **decide** what to do, and can be reprogrammed without changing the wiring.

### A Second Example: Automatic Plant Watering

Here is a longer chain, in which nearly every component from this reading has a job.

```text
Soil moisture ─► [ Moisture sensor ] ─► analog voltage ─► [ Microcontroller ] ─► control signal
                                                                                     │
                                                                                     ▼
                            Water flow ◄─ [ Pump ] ◄─ [ Transistor switch + flyback diode ] ◄─ separate pump supply
```

![The plant-watering signal path: soil moisture sensor, microcontroller decision, transistor switch and pump, end to end](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-17-plant-watering-path.png)

- The **sensor** turns soil moisture into a voltage.
- The **microcontroller** reads that voltage, compares it with a "too dry" threshold and decides when to water.
- The **transistor** lets the microcontroller's small control signal switch the pump's larger current.
- The **flyback diode** protects the transistor from the pump motor's voltage spike.
- The **separate supply** provides the pump's power, sharing a ground with the microcontroller.
- Resistors appear throughout: in the sensor's divider, at the transistor's control terminal and possibly as pull-ups on inputs.

## Matching Sensors and Actuators to Applications

Choosing parts is an engineering decision, not a search for "the best sensor". A helpful way to decide is to work from the application towards the part.

1. **Define the physical quantity and the behaviour needed.** What must be measured or changed? How accurately, how fast and over what range?
2. **Consider the environment.** Will it be wet, hot, dusty, outdoors, in sunlight or moving?
3. **Check the electrical fit.** Does the part's supply voltage match your system? What signal does it use? Can the microcontroller supply the current, or does the part need a transistor or driver?
4. **Consider trade-offs.** Cost, availability, size, power consumption and ease of use.

**Worked example: measuring the distance to an object.** Compare two common approaches.

- An **ultrasonic distance sensor** measures the time taken for a sound pulse to bounce back. It typically measures distances of up to a few metres, but soft or angled surfaces can reflect poorly and give unreliable readings.
- An **infrared proximity sensor** detects reflected infrared light. It suits short distances, but its reading depends on the colour and reflectivity of the target and on ambient light.

![Ultrasonic versus infrared distance sensing: longer range and wide beam versus short, precise detection](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-18-ultrasonic-vs-infrared.png)

Neither is "better". For detecting a person approaching a door from a few metres away, ultrasonic suits better. For detecting whether an object is on a conveyor at a few centimetres, infrared may be enough and cheaper. The right question is always: *which one suits this application, and why?*

**Another example: alerting someone to a door left open.** A magnetic door switch produces a simple digital signal, an LED gives a visible status and a buzzer gives an audible alert. A distance sensor or camera *could* detect the open door, but they would be more expensive and complex than the problem needs. Simpler is often better.

---

# The Microcontroller

## The Small Computer Inside the Loop

Every system in this reading has a decision-maker in the middle. It reads signals from inputs, runs your program and drives outputs. That is the **microcontroller**.

A **microcontroller** is a small computer built onto a single chip, designed to *control* things. It combines, in one package:

- a **processor**, which runs the instructions of your program,
- **memory**, which holds the program and the data it works with, and
- **peripherals**, which are hardware blocks that connect the chip to the outside world, including the pins that let it read and drive electrical signals.

A laptop or a phone is also a computer, and it also has a processor and memory. But they are designed for a different purpose, and the differences explain a lot about how microcontrollers are used.

### A Microcontroller and a General-Purpose Computer

| | General-purpose computer (laptop, phone) | Microcontroller |
|---|---|---|
| **Purpose** | Do many different things, chosen by the user | Do one dedicated control job, repeatedly |
| **Software** | An operating system runs many programs at once | Typically runs one program, starting as soon as power is applied |
| **Memory** | Gigabytes | Kilobytes to a few megabytes on the chip (external memory can sometimes be added) |
| **Connection to the physical world** | Through USB, screens and other standard interfaces | Directly, through pins that read and drive electrical signals |
| **Power use** | Watts | Can be designed for very low power, suiting battery-operated devices |
| **Cost and size** | Higher, larger | Low, tiny |

> **Teaching model.** The line between the two is blurring. Microcontrollers are getting more capable, and some single-board computers can also control pins. But the description above captures the design idea: a microcontroller is built to sit inside a device and control it.

Microcontrollers are everywhere: in washing machines, remote controls, electric toothbrushes and car door-lock systems. It is not unusual for a car to contain dozens.

### The Chip and the Development Board

The word "microcontroller" is used for a few related things, and it helps to separate them:

- The **chip** is the silicon device itself.
- A **development board** is a small circuit board that carries the chip plus the supporting parts it needs: a USB connection for programming, a power circuit, and pin connections you can wire to.
- The **pins** of the board are what you connect components to.

![A development board's parts: the chip, the power regulator, the USB connection, buttons and the pin headers](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-19-development-board.png)

The chip used in this course, the **ESP32-S3**, is a good illustration of how far microcontrollers have advanced. According to Espressif's documentation, it has a dual-core processor running at up to 240 MHz, 512 KB of on-chip SRAM, 45 programmable GPIOs and a range of peripherals. It also includes built-in Wi-Fi and Bluetooth Low Energy, which is why it is well suited to IoT: the "Communicate" stage of the journey comes built in. Chips like this that integrate a processor, memory, peripherals and a radio are often called a **system on a chip (SoC)**.

> **Assumption.** These figures describe the ESP32-S3 chip. The number of pins actually available, and the amount of external flash or extra memory, depend on the specific development board. Check the documentation of the board you have.

## Inside a Microcontroller: Processing, Memory and Peripherals

We can sketch the inside of a microcontroller as three cooperating parts:

```text
┌──────────────────────────── Microcontroller chip ─────────────────────────────┐
│                                                                               │
│   PROCESSOR (CPU)          MEMORY                    PERIPHERALS              │
│   runs the program's       - program storage         hardware blocks for      │
│   instructions, one        - working memory          input, output, timing    │
│   step at a time                                     and communication        │
│                                                                               │
└───────────▲───────────────────────────────────────────────────┬───────────────┘
            │ signals in                                        │ signals out
       sensors, buttons                                  LEDs, transistors, motors…
```

![Inside a microcontroller chip: the processor, memory and peripherals working together](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-20-inside-the-chip.png)

### Processing

The **processor** (CPU) follows your program's instructions one after another, extremely quickly. It does arithmetic, compares values, makes decisions and moves data around. Its speed is measured by its **clock frequency**, in megahertz (MHz): one MHz means a million clock ticks per second. Faster clocks let a processor do more work per second, at the cost of higher power consumption.

For the tasks in this course, you will rarely worry about processor speed. What matters is the idea: the processor is where the "Compute" in Sense → Compute → Actuate takes place. It reads a value, compares it with a threshold and decides what to do.

### Memory

A microcontroller uses two kinds of memory, and the difference between them is worth understanding:

- **Program memory** holds your program. It is **non-volatile**, meaning it keeps its contents when power is removed. In most microcontrollers, this is **flash** memory. This is why a device runs its program again as soon as it is powered on.
- **Working memory** (RAM) holds the values your program is using right now: variables, sensor readings, intermediate results. It is **volatile**, meaning it loses its contents when power is removed.

An everyday parallel: the program is like a recipe book kept on a shelf, and working memory is the scratch paper you use while cooking. The recipe book stays; the scratch paper is thrown away at the end.

![Flash memory as the recipe book that survives power loss, and RAM as the scratch paper that is cleared when power is removed](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-21-memory-analogy.png)

Memory on a microcontroller is limited, and that shapes how you write programs. Where a laptop has gigabytes, a microcontroller has memory measured in kilobytes or megabytes, so programs need to be economical.

### Peripherals

A processor alone cannot read a voltage or drive a pin. **Peripherals** are dedicated hardware blocks that do those jobs alongside the processor. Some tasks need precise timing or repetitive work, and it is more efficient to hand them to specialised hardware, which leaves the processor free for decisions.

Here are the peripherals you will meet in this course. For now, treat this table as a map: each will be covered properly when you need it.

| Peripheral | What it does | Where it appears in your systems |
|---|---|---|
| **GPIO** (general-purpose input/output) | Lets a pin read a HIGH/LOW signal or drive one | Buttons, LEDs, digital sensors, switching transistors |
| **ADC** (analog-to-digital converter) | Measures a voltage and converts it into a number | Reading analog sensors such as an LDR divider |
| **PWM** (pulse-width modulation) | Produces a rapidly switching signal whose on-time can be adjusted | Dimming an LED, controlling motor speed, driving servos |
| **Timers** | Count time precisely | Delays, scheduling, measuring pulses |
| **Communication interfaces** (I2C, SPI, UART) | Exchange data with other chips and sensor modules | Digital-data sensors, displays |
| **Wireless (Wi-Fi, Bluetooth)** | Communicates without wires | The "Communicate" stage of an IoT system |

Espressif lists 45 programmable GPIOs, SPI, I2S, I2C, PWM, ADC and UART among the ESP32-S3's peripherals, among others.

## GPIO: Where Software Meets the Electrical World

Of all the peripherals, one is the most important for what we are doing: **GPIO**. It is the point where a line of code becomes an electrical signal, and the reverse.

**GPIO** stands for **general-purpose input/output**. Each **GPIO pin** is a connection that your program can configure to act as either an input or an output. "General-purpose" means the pin is not permanently fixed to one job; software decides.

![One GPIO pin, two jobs: as an output the pin speaks (drives a signal), as an input the pin listens (reads a signal)](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-22-gpio-input-output.png)

### A Pin as an Output

When a pin is configured as an **output**, your program can set it to **HIGH** or **LOW**:

- **HIGH**: the pin drives a voltage near the chip's supply voltage. On a 3.3 V board, that is roughly 3.3 V.
- **LOW**: the pin is at roughly 0 V.

That is how a program turns on an LED. Setting the pin HIGH makes a current flow through the series resistor and LED to ground. Setting it LOW stops the current.

```text
Program:  led.value = True
              │
              ▼
        GPIO pin driven HIGH  (about 3.3 V)
              │
              ▼
        current through resistor and LED
              │
              ▼
           light
```

![From one line of code to light: setting the pin HIGH drives current through the resistor and LED](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-23-code-to-light.png)

An output pin is a signal source, not a power supply. It can drive a small load such as an indicator LED through a resistor, but not a motor or a pump. For that, the pin drives a transistor, as you saw earlier. The exact limits for your board are in its documentation.

### A Pin as an Input

When configured as an **input**, the pin measures the voltage applied to it and reports HIGH or LOW to the program. Here, the button circuit from earlier comes to life: the pin sits at the junction of the button and the pull-up resistor, and the program reads whether it sees HIGH (released) or LOW (pressed).

Microcontrollers usually include **built-in pull-up and pull-down resistors** that software can switch on for an input pin. This means a button can often be connected between a pin and ground with no external resistor. Using an internal pull-up, the pin reads HIGH when the button is released and LOW when it is pressed. You have now seen how *all* of this works, with no magic: the internal pull-up is the same pull-up resistor from the button circuit, placed inside the chip.

### Logic Levels

The HIGH and LOW levels a microcontroller expects belong to its **logic level**. Espressif recommends a 3.3 V supply for the ESP32-S3, and the chip works with 3.3 V signals. Connecting a 5 V signal directly to an input pin designed for 3.3 V can damage it. This is why "check the voltage before connecting" is a rule you learned in the safety discussion. If a sensor or module runs at 5 V, its documentation will tell you whether its signal is safe for a 3.3 V input.

### Pins Are Not All Alike

It is tempting to think all pins are interchangeable. They are not entirely. Some pins are also connected to on-board features. Others have special roles when the chip starts up. Espressif calls these **strapping pins**. Others support specific peripherals. This is why this reading does not give you any pin numbers: **the pin you should use depends on your board, so always check its pinout diagram and documentation** before wiring.

### From Code to Behaviour: A First Look

In CircuitPython, the language used in this course, a program controls a pin through a small set of tools. Here is a short sketch that ties everything in this section together. It lights an LED while a button is pressed.

> **Assumption.** This is an illustrative sketch, not a program to run yet. `LED_PIN` and `BUTTON_PIN` stand in for the board pins to which you have connected the LED circuit and the button. The real names come from your board's documentation. Setting up the board and running programs is covered when you first work with the hardware.

```python
import digitalio

# LED_PIN and BUTTON_PIN stand for the pins you wired the parts to.
# The real pin names come from your board's documentation.

led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT       # this pin drives the LED circuit

button = digitalio.DigitalInOut(BUTTON_PIN)
button.direction = digitalio.Direction.INPUT     # this pin reads the button
button.pull = digitalio.Pull.UP                  # switch on the internal pull-up resistor

while True:
    if button.value == False:                    # LOW means the button is pressed
        led.value = True                         # drive the pin HIGH: LED on
    else:
        led.value = False                        # drive the pin LOW: LED off
```

What is this program trying to accomplish? It repeatedly reads the button and copies its state to the LED. Here is how the code connects to the physical circuit:

- `DigitalInOut(...)` gives the program a handle on one GPIO pin.
- `Direction.OUTPUT` and `Direction.INPUT` set the pin's role: whether the program drives it or reads it.
- `Pull.UP` switches on the pull-up resistor inside the chip, so the pin reads HIGH (`True`) while the button is released.
- Because of that pull-up, a pressed button reads LOW, which is why the test is `button.value == False`. This is the active-low behaviour from earlier, now visible in code.
- `led.value = True` sets the pin HIGH, and current flows through the resistor and LED.

### When an Output Does Not Behave

Suppose the LED does not light when the program says it should. Reason your way toward the cause in the order in which failures are most likely and easiest to check:

```text
Is the program running?  ─►  Does the pin change state?  ─►  Is the wiring right?  ─►  Is the component OK?  ─►  Is the power/ground right?
```

![A debugging checklist for a silent LED: is the code changing, is the pin changing, is the wiring, component and power all correct](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_qa_testing/niat_coding_questions/rm2-24-debug-led-checklist.png)

1. **Is the program actually running, and does it reach the line that sets the pin?** Add a way to confirm it, such as printing a message.
2. **Does the pin change state?** Measure the voltage on the pin with a multimeter while the program toggles it. If the voltage changes, the software side is doing its job. If it does not, the problem is in the software or in the pin's configuration.
3. **Is the wiring correct?** Is the resistor in series? Is the LED in the right direction? Is the circuit complete back to ground?
4. **Is the component healthy?** Try a different LED or resistor.
5. **Are power and ground connected?**

The same order works for an input: is the program reading the pin, does the pin's voltage change when the button is pressed, is the input floating, is the pull-up configured?

This is the Predict → Measure → Explain habit applied to a system in which software and hardware both play a part: the multimeter tells you which side of the boundary the problem is on.

## The Loop Revisited: Mapping Sense → Compute → Actuate onto Hardware

We can now say precisely what happens inside a microcontroller-based system at each stage of the loop you learned at the start of this module:

| Stage | What happens | Hardware involved |
|---|---|---|
| **Sense** | A sensor turns a physical condition into an electrical signal, which reaches the microcontroller | Sensor and any supporting components (such as a voltage divider) |
| **Input** | The microcontroller reads that signal | A GPIO input pin (for HIGH/LOW signals) or an ADC (for analog voltages) |
| **Compute** | The program processes the reading and decides what to do | Processor and memory |
| **Output** | The microcontroller sets a signal to command the actuator | A GPIO output pin (or PWM for adjustable control) |
| **Actuate** | The actuator turns the command and power into a physical effect | LED, buzzer, transistor-driven motor or pump, and so on |

The night light from earlier is now fully explained: the LDR divider and ADC bring brightness in as a number, the processor compares it with a threshold and a GPIO output drives the LED.

---

# What You Can Now Do, and What Comes Next

You began this reading with three boxes: a sensor, a microcontroller and an actuator. You can now open each one.

- You know the **components** that make up circuits and what each one does: the resistor limits current, the diode and LED conduct one way, the capacitor stores and smooths, the button opens and closes a path and the transistor lets a small signal switch a large current.
- You can tell **sensors** from **actuators**, identify the inputs and outputs of a system, trace a signal from a physical condition to a physical effect and choose suitable parts for simple applications.
- You understand what a **microcontroller** is, how it differs from a general-purpose computer, what its processor, memory and peripherals do, and how **GPIO** connects software to the electrical world.

The mental model to carry forward is this: **a microcontroller-based IoT system is a physical system in which sensors bring the world in as electrical signals, a program running on a small computer decides what to do, and actuators turn those decisions back into physical effects, with components shaping and protecting the signals along the way.**

The next stage of the course moves from understanding to doing. You will set up the ESP32-S3 with CircuitPython, write your first programs and use the GPIO ideas from this reading to read buttons and drive LEDs on real hardware. When you do, the sketch you saw here will stop being an illustration and become something you can run, change and debug.

---

## References

1. Espressif Systems. *ESP32-S3 Series Datasheet* (processor, memory, peripherals). https://documentation.espressif.com/esp32-s3_datasheet_en.pdf
2. Espressif Systems. *ESP32-S3 Wi-Fi & Bluetooth 5 SoC* (product overview: cores, memory, 45 programmable GPIOs, peripherals). https://www.espressif.com/en/products/socs/esp32-s3
3. Espressif Systems. *ESP32-S3 Hardware Design Guidelines* (recommended 3.3 V supply, strapping pins, GPIO). https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32s3/index.html
4. Adafruit Learning System. *CircuitPython Digital In & Out* (`digitalio`, `Direction`, `Pull`, reading a button and driving an LED). https://learn.adafruit.com/adafruit-grand-central/circuitpython-digital-in-out
5. Adafruit Learning System. *Arduino to CircuitPython: Digital In & Out* (configuring pins as inputs and outputs). https://learn.adafruit.com/arduino-to-circuitpython/digital-in-out
6. ROHM Semiconductor. *Low-Side Switch Design: NPN Transistor Circuit Design* (low-side switching, base resistor, flyback diode for inductive loads). https://techweb.rohm.com/product/transistors-diodes/transistors/23727/
7. EmbeddedRelated. *Transistor* (BJT versus MOSFET switching, logic-level gate drive at 3.3 V, flyback diode). https://embeddedrelated.com/glossary/transistor
8. For the fundamental behaviour of resistors, diodes, LEDs, capacitors and transistors, and for the reading of resistor colour codes, this material follows standard introductory electronics practice. Component values are **example values**; always confirm against the datasheet of the actual part.
