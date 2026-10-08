# Programming Your First Microcontroller: ESP32-S3 and CircuitPython

## From Understanding a Microcontroller to Programming One

In the previous reading, you learned what a microcontroller is: a small computer on a chip, with a processor, memory and peripherals, whose **GPIO pins** connect software to the electrical world. You saw a short program that read a button and lit an LED, but it was only a sketch. It contained placeholders where real pin names should be, and there was no board to run it on.

This reading closes that gap. By the end of it, you will have connected a real board to your computer, run a program on it, talked to it interactively, made a pin switch an LED on and off, changed the program and watched the behaviour change, and worked out what to do when something does not work.

The path we will follow is:

```text
Microcontroller → ESP32-S3 board → Pins → CircuitPython → Editor (IDE) → REPL → First program → Modify → Observe → Debug
```

We start with the hardware, because you cannot program something you cannot identify. Then we look at the software that lets you program it, and at how your code actually reaches the chip. Finally, we put everything together in a few small programs.

### What You Will Be Able to Do After This Reading

- Identify the ESP32-S3 as the microcontroller platform used in this course, and explain the role of a development board.
- Identify the main features of your board and describe the purpose of its important pins at a high level.
- Explain what CircuitPython is, and how it is used to program the board.
- Describe how the editor (IDE), your code, the board and the physical hardware relate to one another.
- Explain what the REPL is, and when it is useful.
- Write and run a basic CircuitPython program, modify it and observe the change.
- Build and run a simple LED-blink circuit in the **Wokwi** simulator, using **Arduino C/C++**, and explain how each step parallels the real-hardware CircuitPython workflow.
- Troubleshoot common first-run problems in a systematic order.

> **How to read the labels in this material.** As before:
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. Real parts vary, and the datasheet or documentation of your actual board always wins.
> - **Assumption** — something this reading assumes because it depends on your specific hardware or course setup.

> **Assumptions about your setup.**
> - **Board.** Development boards built around the ESP32-S3 differ from one another. Where this reading needs a concrete example of a board, it uses Espressif's **ESP32-S3-DevKitC-1**, whose documentation is public. Your board may be a different one. Its own documentation and pinout diagram are the final authority on where things are and what they are called.
> - **Editor.** The course setup specifies which editor (IDE) you will use. Rather than guess, this reading describes what an editor *does* in the CircuitPython workflow, and leaves menu-level details to your course's setup instructions.
> - **CircuitPython on the board.** If the course has already installed CircuitPython on your board, you can skip the firmware installation overview. If not, the overview explains what installing it involves, and your setup instructions give the exact steps.
> - **Pin numbers.** This reading gives no pin numbers to wire to. You will discover the right names for *your* board using the board's documentation and CircuitPython itself.

> **Two ways to practise, and three environments to keep straight.** Every hands-on activity in this module has a simulation version, done first in the free browser-based simulator **Wokwi**, and a real-hardware version, done on your physical board. This reading walks through both: the simulation first, later in this reading, and then the real-hardware workflow that makes up most of the reading: **ESP32-S3 with CircuitPython**, the programming environment used throughout this course. The Wokwi simulation uses a different combination on purpose: an **ESP32-S3** board simulated in Wokwi, programmed in **Arduino C/C++**. This is not a simplification or a mistake — Wokwi's CircuitPython simulation only covers a different board family, so the practical simulation track uses Arduino C/C++ instead, on the same ESP32-S3 chip. The underlying ideas (firmware, GPIO, a program that runs continuously, reading inputs and driving outputs) are identical either way; only the syntax changes, as you will see when you build the same simple LED circuit both ways. Keep three things distinct as you go through this course:
>
> - **Conceptual / real-hardware programming environment (this reading):** ESP32-S3 + CircuitPython.
> - **Wokwi simulation environment (covered later in this reading):** ESP32-S3 + Arduino C/C++.
> - **Physical hardware in your kit:** an ESP32 board supplied with your course kit. It may not be the exact same board used in Wokwi, but the core ideas — GPIO, digital signals, firmware, the programming workflow — carry over regardless of the exact board.

![CircuitPython on real hardware and Arduino C/C++ in Wokwi both target the same ESP32-S3 GPIO and concepts](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_testing_1/niat_coding_questions/rm3-01-circuitpython-vs-arduino-wokwi.png)

---

# The ESP32-S3 Board

## From a Chip to a Development Board

### The ESP32-S3 in an IoT System

The microcontroller you will use throughout this course is the **ESP32-S3**, made by Espressif Systems. In terms of the loop you know so well, it fills the middle box:

```text
Sensor  ──►  ESP32-S3  ──►  Actuator
```

Inside, according to Espressif's documentation, it has a dual-core processor running at up to 240 MHz, 512 KB of on-chip SRAM, 45 programmable GPIOs and a range of peripherals. It also has built-in Wi-Fi and Bluetooth Low Energy. In an IoT system, this means one chip can take on the **Compute** role and also the **Communicate** stage of the journey. For now, we focus on the first: reading inputs, running a program and driving outputs. Communication comes later in the course.

![The ESP32-S3 module on a development board, showing its GPIO pin headers, Wi-Fi/Bluetooth radio and USB connection](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_testing_1/niat_coding_questions/rm3-02-meet-the-esp32-s3.png)

### Chip, Module and Development Board

The ESP32-S3 is a small silicon chip, and you cannot easily wire anything to it directly. In practice, you will meet it in three forms, and knowing which is which avoids a lot of confusion:

```text
┌──────────────────────────── Development board ────────────────────────────┐
│                                                                           │
│   USB connection(s)     Power regulator      Buttons     LED(s)   Pin      │
│                                                                   headers │
│          ┌──────────────── Module ────────────────┐                       │
│          │  ESP32-S3 chip + flash memory + antenna │                       │
│          └─────────────────────────────────────────┘                       │
└───────────────────────────────────────────────────────────────────────────┘
```

- The **chip** is the ESP32-S3 itself.
- A **module** is the chip mounted with the parts it needs to operate, such as flash memory for storing programs and an antenna for Wi-Fi and Bluetooth, on a small board. Espressif's ESP32-S3-WROOM-1 is an example.
- A **development board** takes a module and adds everything you need to *use* it: a USB connection to a computer, a circuit that converts the 5 V from USB into the 3.3 V the chip needs, buttons for resetting and starting up, an indicator light or two and **pin headers**, rows of pins that bring the chip's connections out to where you can plug in jumper wires or a breadboard.

Why does a development board exist? Because the bare chip is tiny and has no convenient way to power it or load programs onto it. A development board turns it into something a student can plug in and program in minutes.

> **Assumption.** In the example board used in this reading, Espressif's ESP32-S3-DevKitC-1, the board carries an ESP32-S3 module and brings most of the module's I/O pins out to pin headers on both sides, so it can be used with jumper wires or plugged into a breadboard. Boards from other makers follow the same general idea, but their layouts differ.

![Side by side: the bare ESP32-S3 chip, the module built around it, and a complete development board](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_testing_1/niat_coding_questions/rm3-03-chip-module-dev-board.png)

### Getting to Know Your Board

Pick up your board and look at it. Nearly every ESP32-S3 development board has the same kinds of features, even if they are in different places:

| Feature | What it does | What to check on your board |
|---|---|---|
| **USB connector(s)** | Powers the board and connects it to your computer for programming and communication | How many USB connectors are there, and how are they labelled? |
| **Power indicator LED** | Lights up when the board is powered | Does it light when you plug the board in? |
| **BOOT button** | Used, together with RESET, to put the chip into a special mode for loading firmware | Where is it, and what is it labelled? |
| **RESET (or EN) button** | Restarts the chip | Where is it? |
| **Pin headers** | Bring the chip's pins out for wiring | Are the pins labelled? Which rows are power, ground and GPIO? |
| **On-board LED(s)** | Indicators driven by the chip | Does your board have one? Is it a plain LED or a special type? |
| **The module and antenna** | The chip, its memory and its wireless antenna | Keep the antenna area clear of metal and wires |

A few facts about the example board, from Espressif's documentation, illustrate what to look for:

- It has **two USB Type-C connectors**: one connected to a USB-to-UART bridge chip (Espressif calls it the "USB-to-UART port") and one connected to the ESP32-S3's own **native USB** interface (the "ESP32-S3 USB port"). Espressif's documentation describes both as able to power the board.
- Holding **BOOT** and then pressing **RESET** starts the firmware download mode.
- It has an **addressable RGB LED**, driven from a single pin. Which pin depends on the board revision: Espressif states that the initial revision uses GPIO48 and version 1.1 uses GPIO38.

That last point is a good example of why board documentation matters. The pin that drives the on-board LED is different on two versions of the same board. It is also a warning that an "addressable" LED is not a simple LED you can switch on with a plain HIGH or LOW. It needs special handling, which we leave for later. That is why the LED experiments in this reading use an external LED with a resistor, which you already know how to wire.

## Pins: The Board's Connection to the Physical World

In the previous reading, you learned that GPIO pins are where software meets the electrical world. Now you have a board with actual pins in front of you. Let us sort them.

### Kinds of Pins

Not all pins on the header do the same job. At a beginner level, you can sort them into a few groups:

| Kind of pin | What it does | Typical labels |
|---|---|---|
| **Power output pins** | Provide a supply voltage you can use to power small components | 3V3 (3.3 V), 5V |
| **Ground pins** | The common reference (0 V) for all voltages, to which every circuit must return | GND, G |
| **GPIO pins** | Pins your program can set as inputs or outputs | Numbers or names such as IO followed by a number, depending on the board |
| **Control pins** | Reset or enable the chip | EN, RST |
| **Special-purpose pins** | Used by the chip for internal jobs such as USB, memory or start-up configuration | Varies by board; the pinout diagram flags them |

Some of these are worth a closer look.

- **Power pins.** The 3V3 pin provides 3.3 V, the voltage the chip and its signals run on. Espressif describes the board as powered either through its USB connector(s), or through the 5V and GND pins, or through the 3V3 and GND pins, and these ways are alternatives to each other. Connecting several power sources at once is a mistake. Everything you learned about safety and polarity applies to these pins.
- **Ground pins.** There are usually several. They are all the same electrical point, and any of them can be used as the return path of your circuits. Recall that the load and the microcontroller must share a ground.
- **GPIO pins.** These are the pins you will program. Remember the logic-level rule from before: the chip works with **3.3 V** signals, so never connect a 5 V signal to a GPIO pin without checking that it is safe.
- **Special-purpose pins.** Some pins have jobs that are fixed or that are used when the chip starts up. On the ESP32-S3, for example, Espressif's design documentation refers to **strapping pins**, whose voltage levels at start-up help configure the chip. CircuitPython's documentation also notes that the ESP32-S3's native USB connection uses two GPIO pins internally (GPIO19 and GPIO20 for USB data). Others may be connected to on-board parts or to the module's internal memory on some board variants.

> **Teaching model.** For a beginner, the rule is simple: **treat a pin as free for your experiments only if your board's documentation shows it as a general-purpose pin with no special role.** Pins marked for USB, start-up configuration, on-board features or memory should be left alone until you know why you need them.

### Three Names for the Same Pin

One more thing tends to confuse beginners. The same physical pin can be referred to in **three different ways**:

1. **The label printed on the board** (the silkscreen next to the pin).
2. **The chip's GPIO number**, as used in the chip's datasheet.
3. **The name CircuitPython uses in code**, which comes from the CircuitPython definition for your specific board.

These are related but not always identical, and they depend on the board. This is why you should not copy a pin name from a tutorial written for a different board. You will find out how to discover the correct CircuitPython names for your board by asking CircuitPython itself, a little later in this reading.

### Choosing a Pin for Your First Experiment

When you choose a pin for your first LED, work through this short checklist:

1. Look at your board's **pinout diagram**. Choose a pin that is a plain general-purpose pin with no special function marked on it.
2. Avoid the pins used for USB, start-up configuration, on-board LEDs and buttons, and internal memory.
3. Later, confirm that CircuitPython actually has a name for that pin on your board.
4. Note the **nearest ground pin**, so the return wire is short.

If you are unsure, ask your instructor, or read your board's documentation before wiring.

---

# CircuitPython

## What CircuitPython Is

### Firmware and Your Program

Your board can do nothing on its own until it has software inside it. There is a distinction that beginners often miss, and it makes everything else in this reading easier to understand.

**Firmware** is software that is stored permanently in the microcontroller's flash memory and runs directly on the hardware. It is what starts running when the chip is powered on, and it provides the basic behaviour of the device.

**CircuitPython** is firmware. When installed, it turns your ESP32-S3 into a device that can read and run **Python** programs. It includes:

- an **interpreter**, which reads your Python program and carries it out, line by line,
- **built-in libraries** for controlling hardware, such as the modules that control pins,
- and a way for the board to appear to your computer as a small USB drive, so you can copy code onto it.

This gives us a picture of layers:

```text
┌───────────────────────────────────────┐
│  YOUR PROGRAM  (code.py)              │   you write and change this often
├───────────────────────────────────────┤
│  CircuitPython libraries              │   digitalio, board, time …
│  (built-in modules)                   │
├───────────────────────────────────────┤
│  CircuitPython FIRMWARE               │   installed once (and updated rarely)
│  (interpreter + hardware support)     │
├───────────────────────────────────────┤
│  ESP32-S3 HARDWARE                    │   processor, memory, GPIO pins
└───────────────────────────────────────┘
```

Two different things can therefore be "loaded onto the board", and they are very different in how often you do them:

- **Installing CircuitPython** (the firmware) is done once, when you set up the board. It replaces what was on the board before.
- **Writing your program** (a Python file) is what you do all the time. It sits on top of the firmware and is easy to change.

Keeping these apart will save you from a common misunderstanding, namely that you have to "flash" the board every time you change a line of code. With CircuitPython you don't.

![Firmware versus your program: firmware is the foundation, installed once and rarely changed; your program is the set of instructions, changed frequently](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_testing_1/niat_coding_questions/rm3-04-firmware-vs-your-program.png)

### Choosing CircuitPython for This Course

There are several ways to program an ESP32-S3: with C or C++ (for example using Espressif's own framework or the Arduino environment), with MicroPython or with CircuitPython. This course uses **CircuitPython**, and it is worth understanding the reasons, including the trade-offs.

**What makes it a good fit for learning:**

- **It is Python.** CircuitPython is almost completely compatible with Python, and simply adds hardware support. If you have programmed before, the structure of a program (variables, loops, conditions) will feel familiar.
- **Fast feedback.** You save a file and the board runs it immediately. There is no separate compile-and-upload step to wait for.
- **Interactive.** The REPL, which you will meet shortly, lets you type a command and see the result at once. That makes it excellent for exploring hardware.
- **A consistent way to control hardware.** Modules such as `digitalio` give a uniform way to work with pins, and there is a large collection of ready-made libraries for sensors and other devices, which later modules will use.
- **The board is a drive.** Your code is just a file you copy to a drive, which is easy to understand.

**The trade-offs:**

- Because a Python program is interpreted, it generally runs slower and uses more memory than the equivalent compiled C or C++ program. For the tasks in this course, that is rarely a problem. For extremely timing-critical or memory-tight applications, other tools are sometimes preferred.

**A note on look-alikes.** CircuitPython is based on **MicroPython**, and the two look very similar. But they are different projects with differences in their hardware libraries. An example you find online written for MicroPython, or for Arduino, may not work in CircuitPython. When you search for help, look for CircuitPython specifically, and check that an example is meant for it before copying anything.

## How Code Reaches the Board

### The CIRCUITPY Drive and code.py

Here is what makes the CircuitPython workflow so approachable. When a board with CircuitPython is connected to your computer through the appropriate USB connection, it shows up as a small USB drive named **CIRCUITPY**. You can open it like any other drive.

On that drive, a few file names have special meaning:

- **`code.py`** is your main program. After the board starts up (and after `boot.py`, if there is one), CircuitPython looks for this file and runs it.
- **`boot.py`** (optional) holds one-time setup that runs before everything else at start-up. You will not need it in this reading.
- **A `lib` folder** holds extra libraries that programs can import. Later modules will use it.

Then comes the feature that makes experimentation quick: **auto-reload**. Whenever a file on the CIRCUITPY drive is saved, CircuitPython restarts and runs `code.py` again straight away. You edit, save and see the result.

> **Important.** The name matters. A program saved as anything other than `code.py` (for example, `Code.txt`, `code.py.txt` or `my_program.py`) in the wrong place will not be run automatically. Many "my program does nothing" problems come down to file name or file location.

### The Role of the IDE

An **IDE**, or *integrated development environment*, is the software in which you write and manage your code. For CircuitPython, the editor does three jobs:

1. **Editing.** You write and change your Python code, with helpful features such as colouring and error hints.
2. **Transferring.** It saves your code to the `code.py` file on the CIRCUITPY drive, which is how the code reaches the board.
3. **Connecting to the board.** Many editors that are used with CircuitPython also provide a **serial console** and **REPL** panel, where you can see what your program prints and type commands directly to the board.

Because the board looks like a USB drive, a plain text editor can technically be used to edit `code.py`. But editors designed for CircuitPython, such as Mu and Thonny (both of which are commonly used with CircuitPython boards), combine editing with the serial console in one place, which is why they are popular for beginners. The course setup names the editor you will use.

So the relationship among the pieces is this:

```text
  Editor (IDE)  ──save code.py──►  CIRCUITPY drive  ──►  CircuitPython on the ESP32-S3  ──►  pins  ──►  LED / circuit
       ▲                                                              │
       └────────────  serial console: print() output, REPL  ◄─────────┘
```

Your code travels **forward** through the drive to the board and out through its pins, and information travels **back** through the serial connection as printed messages and REPL responses.

### Putting CircuitPython on a Board

> **Assumption.** Your course setup may deliver boards with CircuitPython already installed, in which case you can skip to the next section. This part explains the idea so you understand what is going on if you need to do it.

Installing CircuitPython means writing the **firmware** into the board's flash memory. You do this using the official CircuitPython download page, which has a separate download for each supported board. Two points matter:

- **Choose the build that matches your board exactly.** The download page lists boards by name, including several variants of the ESP32-S3-DevKitC-1 that differ in their memory. The wrong build may not work or may waste memory. If you are unsure which one you have, look at the markings on the board or its documentation.
- **There are two common routes.** The chip has a built-in **ROM bootloader**, a tiny program permanently inside the chip that can accept new firmware. You start it by holding the BOOT button, pressing and releasing RESET and then releasing BOOT. A tool such as Adafruit's browser-based WebSerial ESPTool or `esptool` can then write the CircuitPython firmware. Alternatively, some setups use a **UF2 bootloader** (on Espressif boards it is called TinyUF2), which lets you install CircuitPython by dragging a file onto a drive.

Two cautions from the CircuitPython download pages are worth remembering. **Installing a bootloader or new firmware can erase what is on the board**, so save any files you want to keep first. And a **charge-only USB cable** cannot carry data: use a cable that supports data.

---

# Simulating Your First Program in Wokwi

## Why Simulate Before You Wire Anything

As the callout at the start of this reading mentioned, every hands-on activity in this course has a simulation version as well as a real-hardware version. **Wokwi** is the simulator this course uses: a free, browser-based ESP32 simulator that runs entirely on the page, with no installation. You write code in your browser, wire a virtual circuit and press a button to see it run — LEDs, buttons, buzzers, sensors and more all behave the way the real components would. Running the circuit in simulation first lets you build, test and debug an idea safely, before you touch a real board and real wires.

> **Two ways to practise, revisited.** The simulation track uses an **ESP32-S3** board simulated in Wokwi, programmed in **Arduino C/C++**, while the rest of this reading uses the same ESP32-S3 chip with **CircuitPython** on real hardware. The two use different languages because Wokwi's CircuitPython simulation covers a different board family, so the simulation track uses Arduino C/C++ instead. The underlying ideas — GPIO, a program that runs continuously, driving an output pin — are identical either way; only the syntax changes, as the worked example below shows.

## Building the Circuit in Wokwi

Follow these steps to build and run your first simulated program.

1. **Open Wokwi.** Go to `https://wokwi.com/esp32` in your browser. No account or installation is needed to try it.
2. **Select the ESP32-S3 starter template.** Wokwi offers starter templates for several boards, including plain ESP32, ESP32-S2 and ESP32-S3. Choose the **ESP32-S3** template, since that is the chip this course uses.
3. **Add an LED and a resistor.** From Wokwi's parts panel, add an LED and a resistor to the workspace alongside the ESP32-S3 board.
4. **Set the resistor value to 220 Ω.** Click the resistor and set its **Resistance** property to **220 Ω**. This plays the same role as the resistor you have already met elsewhere in this reading: it limits the current through the LED so it lights safely.
5. **Build the circuit.** Wire the parts together: connect one leg of the resistor to a GPIO pin (this reading uses **pin 20** on the simulated board), and the other leg of the resistor to the LED's anode. Connect the LED's cathode to a **GND** pin.

![Wiring an LED and a 220 ohm resistor to GPIO 20 on the Wokwi ESP32-S3 board](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_testing_1/niat_coding_questions/rm3-06-wokwi-esp32s3-led-wiring.png)

This is the same circuit shape you already know from elsewhere in this reading: **GPIO pin → resistor → LED → GND**. Only the values and the tool have changed — you are building the identical idea in a simulator instead of on a breadboard.

6. **Start the simulation.** Click the green play button. The simulator begins running whatever program is loaded, and the circuit becomes "live": the LED will light if the program drives its pin HIGH.

## The Arduino C/C++ Program

7. **Run the Arduino C/C++ blink program.** Replace the sketch in the code editor with the following program, then start (or restart) the simulation:

```cpp
void setup() {
  pinMode(20, OUTPUT);
}

void loop() {
  digitalWrite(20, HIGH);
  delay(500);
  digitalWrite(20, LOW);
  delay(500);
}
```

This is Arduino C/C++, not CircuitPython, but the shape of the program should feel familiar. Here is how each part connects to the hardware:

- `void setup()` runs once, when the program starts. `pinMode(20, OUTPUT)` tells the chip that pin 20 will *drive* a signal — the same "GPIO as output" idea you meet again later in this reading, just written as a function call instead of an assignment.
- `void loop()` runs over and over, forever, which is Arduino C/C++'s equivalent of CircuitPython's `while True:`.
- `digitalWrite(20, HIGH)` sets pin 20 HIGH, about 3.3 V, so current flows through the resistor and LED and it lights.
- `delay(500)` pauses for 500 milliseconds, half a second — the same pause you will later write as `time.sleep(0.5)` in CircuitPython.
- `digitalWrite(20, LOW)` sets the pin LOW, about 0 V, and the current stops.

> **Assumption.** Pin 20 is specific to the simulated ESP32-S3-WROOM-1 board in Wokwi's ESP32-S3 starter template, matching the circuit wired in Step 5. It is not a claim about any real board's pin numbering — as elsewhere in this reading, the pin you use on a real board depends on that board's own documentation.

## Explaining the Flow

8. **Explain the flow.** With the simulation running, you should see the LED blink on and off every half second. Nothing about this is magic: it is a chain of cause and effect, the same one you will trace again later in this reading with real hardware:

```text
Program → ESP32-S3 → GPIO HIGH/LOW → Electrical signal → LED ON/OFF
```

Read it as a chain: your `digitalWrite()` call becomes an instruction the ESP32-S3 carries out, which sets the GPIO pin HIGH or LOW, which is an electrical signal, which drives current through the resistor and LED, which the LED turns into light.

---

# Your First Programs

## Connecting the Board and Checking That It Is Alive

Before writing any code, confirm that the pieces of the chain (computer, cable, board, CircuitPython) are all working. This is a procedure where the order matters:

1. **Use a USB cable that carries data.** Some cables only charge devices and have no data lines. A charge-only cable is one of the most common reasons a board does not appear.
2. **Connect the board to the correct USB connector.** CircuitPython's CIRCUITPY drive is provided through the chip's own **native USB** interface. On a board with two USB connectors, such as the example board, that is normally the one Espressif's documentation calls the "ESP32-S3 USB" port, not the USB-to-UART port. CircuitPython's documentation notes that on some ESP32-S3 boards the USB connector may or may not be wired to native USB, so confirm which connector your course setup expects.
3. **Look for signs of power.** A power indicator LED should light.
4. **Look for the drive.** A new drive named **CIRCUITPY** should appear on your computer within a few seconds.
5. **Open your editor** and connect it to the board's serial console, following your course setup instructions.

When the serial console connects, you will typically see messages from CircuitPython. The exact text varies with the version, but you may see something like this:

```text
Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
code.py output:
...
Code done running.
Press any key to enter the REPL. Use CTRL-D to reload.
```

Each message tells you something. "Auto-reload is on" means saving a file will restart your program. "Code done running" means `code.py` ran to its end, or was empty. "Press any key to enter the REPL" is the invitation to the next section.

## The REPL: Talking to the Board Directly

So far, the workflow has been *write a file, save it, watch it run*. There is another way to work that is often better for exploring: the **REPL**.

**REPL** stands for **Read–Eval–Print Loop**. It is a prompt where you type one line of Python, the board **reads** it, **evaluates** it (carries it out), **prints** the result and then waits for your next line. The prompt looks like this:

```text
>>>
```

Imagine the difference between writing a letter and having a conversation. A program in `code.py` is a letter, complete and sent in one go. The REPL is a conversation: you say something, the board answers and you decide what to say next.

### Getting In and Out

You reach the REPL through the **serial console** of your editor:

1. Connect to the serial console.
2. Press **Ctrl+C**. If a program is running, it stops, and you see a message such as "Press any key to enter the REPL".
3. Press any key. You see the `>>>` prompt.
4. To leave, press **Ctrl+D**. This reloads the board and runs your program again.

> **Note.** In current versions of CircuitPython, the REPL starts as a fresh session. Variables from `code.py` are not available in it, so things you create in the REPL are your own, and they disappear when the board reloads.

### First Conversations

Try these in the REPL:

```text
>>> print("Hello, board!")
Hello, board!
>>> 6 * 7
42
>>> import board
>>> dir(board)
```

The first two lines show that the REPL evaluates ordinary Python. The last line is more interesting. `board` is a module built into CircuitPython, and it holds the **names of the pins and other board-specific things for your particular board**. The function `dir()` lists what is inside it. The output is a list of names, and it will be different for different boards.

This answers the question left open earlier, about the third name for a pin. The names in this list are the names CircuitPython uses for the pins on **your** board. You will typically find that they include names for the GPIO pins, and possibly names for special things such as an on-board LED, buses or the board's identity. Comparing this list with your board's pinout diagram tells you what to write in your code. (On many Espressif boards, the GPIO names begin with the letters IO followed by a number, but check the output for your own board and do not assume.)

### When the REPL Is the Right Tool

The REPL is good for:

- **Quick experiments.** Try a single line before putting it in a program.
- **Discovering what is available.** As with `dir(board)`, you can explore instead of guessing.
- **Testing hardware.** Change a pin's state and see the physical effect instantly.
- **Debugging.** Check a value or test a piece of code when something is not behaving.

It is *not* the place for your finished program. Nothing typed in the REPL is saved, and when the board restarts it is gone. The workflow to remember is: **explore in the REPL, then put the working code in `code.py`.**

## Your First Program

Now we write a real program. The first one needs no wiring at all, so you can check the whole chain from editor to board before adding any hardware.

### Hello from the Board

Open `code.py` on the CIRCUITPY drive in your editor, replace its contents with the following and save:

```python
import time

print("Hello from my ESP32-S3!")

count = 0
while True:
    print("Loop number", count)
    count = count + 1
    time.sleep(1)
```

Because auto-reload is on, the board should restart and run this as soon as the save is complete. Look at the serial console. You should see the greeting, followed by a new line every second.

Here is what each part does:

- `import time` gives the program access to the `time` module, which includes `sleep`.
- `print(...)` sends text to the serial console. This is your window into what the program is doing. Recall that the board has no screen of its own.
- `count = 0` creates a variable that lives in the board's working memory (its RAM).
- `while True:` repeats the indented lines forever. A microcontroller program typically runs continuously.
- `time.sleep(1)` pauses for one second. Without it, the loop would run as fast as the processor allows and flood the console.

This program does not touch any pin, yet it demonstrates the full path: you wrote code in an editor, saving it put it on the board's drive, the firmware interpreted it and the result came back over the serial connection.

## Making a Pin Do Something: Blinking an External LED

Now we connect the program to the physical world, using the GPIO ideas from the previous reading: a program sets a pin HIGH or LOW, and an LED circuit responds.

### Building the Circuit

You already know this circuit: a GPIO pin drives current through a resistor and an LED to ground.

```text
    GPIO pin ──[ Resistor ]──►|── GND pin
                              LED
                       (anode)   (cathode)
```

Use the resistor value you calculated earlier for a 3.3 V supply, or one from your kit that gives a safe current.

> **Example values.** With a 3.3 V output, a red LED with a forward voltage of about 2.0 V and a 330 Ω resistor, the current is about (3.3 − 2.0) ÷ 330 ≈ 4 mA. With 150 Ω it would be about 8.7 mA. Check your own LED and resistor, and never connect an LED to a pin without a resistor.

Build it in this order, keeping to the safety habits from earlier:

1. **Disconnect the board's USB cable** so the board is unpowered while you wire.
2. **Connect the resistor** to the GPIO pin you chose from the pinout diagram.
3. **Connect the LED's anode** (the longer leg, in the usual convention) to the other end of the resistor, and the **cathode** to a **GND** pin.
4. **Check the wiring** against the diagram before applying power. Is the LED the right way round? Is the resistor in series?
5. **Reconnect USB.**

Notice that the circuit uses the board's **ground pin** as the return path. The LED circuit and the chip must share a ground, exactly as you saw earlier.

### The Program

Replace the contents of `code.py` with this program:

```python
import time
import board
import digitalio

# Replace CHOSEN_PIN with the name you found using dir(board)
LED_PIN = board.CHOSEN_PIN

led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    print("LED on")
    time.sleep(0.5)

    led.value = False
    print("LED off")
    time.sleep(0.5)
```

> **Assumption.** `board.CHOSEN_PIN` is a placeholder. Until you replace `CHOSEN_PIN` with a real pin name from your own board's `dir(board)` list, the program will stop with an error. That is deliberate, and it gives you a chance to see what a CircuitPython error looks like. We deal with errors shortly.

What is this program trying to accomplish? It repeatedly turns the LED on for half a second, then off for half a second. Here is how each part connects to the hardware:

- `import board` and `import digitalio` bring in the modules for pin names and for digital pin control. You met `digitalio` in the previous reading.
- `LED_PIN = board.CHOSEN_PIN` refers to the physical pin by the name CircuitPython gives it on your board.
- `digitalio.DigitalInOut(LED_PIN)` gives the program control of that pin.
- `led.direction = digitalio.Direction.OUTPUT` tells the chip that this pin will *drive* a signal instead of reading one. This is the "GPIO as output" idea, now in real code.
- `led.value = True` sets the pin HIGH, about 3.3 V, so current flows through the resistor and LED, and the LED lights.
- `led.value = False` sets it LOW, about 0 V, so the current stops.

Follow the signal path: a line of Python → the firmware → the GPIO peripheral → a voltage on the pin → a current through the resistor and LED → light. This is the same chain of "forms of a signal" you traced in the previous reading, and now you are making it happen.

![The signal path from your program to the physical LED: the program sets the GPIO pin HIGH or LOW, which drives the electrical signal that switches the LED on and off](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_testing_1/niat_coding_questions/rm3-05-signal-path-gpio-to-led.png)

### Modify and Observe

Now change the program and see how the behaviour changes. As always, predict first.

- Make the LED stay on for 2 seconds and off for 0.2 seconds.
- Make it blink twice quickly, then pause for a second, and repeat.
- Remove the `print` lines. Does the LED behaviour change? Does the console?
- What happens if you make both `time.sleep` calls very short, such as `0.001`? What do you see, and why do you think that happens?

**Stretch: a button as an input.** If you have a button and want to try more, reuse the sketch from the previous reading, with real pin names in place of the placeholders. Wire a button between a chosen pin and ground, use `Pull.UP` on the input and let the LED follow the button. Reading inputs is explored in more depth in later modules. Here, it is a chance to see that the code you read before actually works.

## Using the REPL to Control the LED

The REPL lets you do the same thing interactively. With the LED circuit wired, stop the program (Ctrl+C), enter the REPL, and type:

```text
>>> import board
>>> import digitalio
>>> led = digitalio.DigitalInOut(board.CHOSEN_PIN)
>>> led.direction = digitalio.Direction.OUTPUT
>>> led.value = True
>>> led.value = False
```

(Replace `CHOSEN_PIN` with your pin name.) After you press Enter on `led.value = True`, the LED lights *immediately*. After `led.value = False`, it goes out. No file, no saving, no restart: you are talking directly to the pin.

This is a very useful debugging technique. If your program does not light the LED, you can test the *circuit* on its own in the REPL. If the LED lights when you set the value in the REPL, the circuit and pin are fine and the problem is in your program. If it does not, the problem is in the wiring or components.

## When Something Does Not Work

Every engineer's first attempt at a new platform includes failures. That is normal, and learning to diagnose them is a skill worth as much as writing the code. The habits from earlier still apply: **Predict → Measure → Explain**, and working in a fixed order from the most likely, easiest-to-check cause to the least.

### A Troubleshooting Order for the Board

```text
Power ─► Cable & port ─► Board detected ─► CircuitPython running ─► File (name, place, saved) ─► Program errors ─► Wiring & pin ─► Expected behaviour
```

For hardware problems, the general method is **Observe → Isolate → Measure → Hypothesize → Test → Fix → Verify**. Observe exactly what you see. Isolate which link of the chain the problem is in. Measure or check to find out. Form a hypothesis, test it with one change, fix and confirm that it worked.

### Common First-Run Problems

| What you observe | Likely causes | What to check |
|---|---|---|
| **No power light, board not detected at all** | Charge-only cable, faulty cable or port, board not powered | Try a different data cable and a different USB port. Confirm that the power LED lights. |
| **Power LED on, but no CIRCUITPY drive** | Wrong USB connector (for example, the USB-to-UART one), CircuitPython not installed or not running, board in a special start-up mode | Try the other connector. Press RESET. Confirm from your setup instructions that CircuitPython is installed. |
| **CIRCUITPY drive appears, but nothing happens** | Program not saved, file not named `code.py`, file in the wrong place, hidden extension such as `code.py.txt`, program has finished | Check that the file is named exactly `code.py`, is at the top level of the drive and has been saved. Look at the serial console for messages. |
| **Serial console shows an error message** | Syntax error, typo in a name, wrong pin name | Read the error message (see below). |
| **Program runs and prints, but the LED does not light** | Wrong pin name or pin choice, LED reversed, resistor or ground not connected, LED or resistor faulty | Use the REPL to set the pin HIGH. Measure the voltage on the pin. Check the LED's direction and the ground connection. |
| **Program restarts by itself unexpectedly** | Something else is writing to the CIRCUITPY drive, and each write triggers auto-reload | Close backup, anti-virus or disk-checking utilities that might be touching the drive. |
| **Message about "safe mode"** | The board did not start normally, or RESET was pressed at a particular moment during start-up | Read the message. Pressing RESET again, or unplugging and reconnecting the board, typically returns to normal mode. |

> **Note.** A common cause of confusion is a serial console panel that is too small: error messages can scroll out of view. Check that you can see the whole output before concluding that "nothing happened".

### Reading an Error Message

When CircuitPython hits a problem in your program, it prints a **traceback** on the serial console. It looks intimidating, but it is a set of clues. The key rule is: **read from the bottom up**.

```text
code.py output:
Traceback (most recent call last):
  File "code.py", line 6, in <module>
AttributeError: 'module' object has no attribute 'CHOSEN_PIN'
```

- The **last line** says what kind of error it is and gives a short description. Here, an `AttributeError` means the program asked the `board` module for something that does not exist. This is exactly what happens if you forget to replace the placeholder `CHOSEN_PIN` with a real name.
- The line above it says **where**: file `code.py`, line 6.

A **syntax error** looks slightly different, and means Python could not even understand the line:

```text
  File "code.py", line 9
SyntaxError: invalid syntax
```

Typical causes are a missing colon after `while True`, an unclosed bracket, or a misspelt word. The line number is where Python noticed the problem, and the actual mistake is sometimes on the line just before it.

> **Assumption.** The precise wording of messages can vary between CircuitPython versions, but the structure (an error type, a description and a line number) stays the same.

### Debugging Step by Step

Suppose the LED does not blink. Work through the chain in order, and stop as soon as you find the break:

1. **Is the board powered and detected?** Power LED on? CIRCUITPY visible?
2. **Is the program actually running?** Is there output in the serial console? Any error?
3. **Is the file in the right place with the right name?** `code.py`, top level, saved.
4. **Does the pin change state?** Use the REPL, or a multimeter, to see whether the pin's voltage changes. If it does, the software is doing its part.
5. **Is the circuit correct?** LED orientation, resistor, ground connection.
6. **Is the pin choice suitable?** Check the pinout again for any special function.

Every step is a *measurement or observation*, not a guess. That is what makes this fast.

---

# What You Can Now Do, and What Comes Next

You started this reading with a microcontroller as an idea. You can now work with one as an object.

- You can identify the **ESP32-S3** as the course platform, and explain how a **development board** turns a chip into something you can plug in and use.
- You can find the important features of your board and tell power, ground, GPIO and special-purpose pins apart, and you know to check your board's documentation before choosing a pin.
- You understand that **CircuitPython** is firmware that lets the board run Python, that your program lives in `code.py` on the **CIRCUITPY** drive and that the **editor** connects your code, the board and the serial console.
- You can use the **REPL** for interactive experiments and for discovering your board's pin names.
- You have run a program, changed it and observed the effect, connected a pin to an LED circuit and worked through a fixed order when something went wrong.
- You have built and run the same LED-blink idea twice: once simulated in **Wokwi** with **Arduino C/C++**, and once on real hardware with **CircuitPython** — and you can explain why the signal path (program → chip → GPIO → electrical signal → LED) is the same in both.

The mental model to carry forward is this: **you write Python in an editor, it reaches the board through the CIRCUITPY drive, the CircuitPython firmware carries it out, and the GPIO pins turn your instructions into voltages that drive real circuits.** The serial console and REPL carry information back.

This is the point where the course shifts from understanding how systems work to building them. In the modules ahead, you will go deeper into digital inputs and outputs, read analog signals, control actuators with varying power, communicate with sensors and other devices, and eventually connect your boards to networks and the cloud. Every one of those steps uses the workflow you have just practised: write code, save it, observe, predict, measure, explain and debug.

---

## References

1. Espressif Systems. *ESP32-S3-DevKitC-1 User Guide (v1.1)* (board components, USB ports, power options, BOOT and RESET, RGB LED GPIO by revision). https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html
2. Espressif Systems. *ESP32-S3 Series Datasheet* (processor, memory, peripherals). https://documentation.espressif.com/esp32-s3_datasheet_en.pdf
3. Espressif Systems. *ESP32-S3 Hardware Design Guidelines* (3.3 V supply, strapping pins). https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32s3/index.html
4. CircuitPython. *ESP32-S3-DevKitC-1 download page* (firmware builds per board, ROM bootloader entry with BOOT and RESET, TinyUF2, data-cable note). https://circuitpython.org/board/espressif_esp32s3_devkitc_1_n8r2/
5. CircuitPython documentation. *Espressif port* (native USB connection on the ESP32-S3, serial console and REPL). https://docs.circuitpython.org/en/latest/ports/espressif/README.html
6. Adafruit Learning System. *Welcome to CircuitPython: The REPL* (Ctrl+C, Ctrl+D, entering and leaving the REPL). https://learn.adafruit.com/welcome-to-circuitpython/the-repl
7. Adafruit Learning System. *Welcome to CircuitPython: Troubleshooting* (auto-reload, safe mode, serial console output). https://learn.adafruit.com/welcome-to-circuitpython/troubleshooting
8. Adafruit Learning System. *CircuitPython Pins and Modules* (the `board` module and `dir(board)`). https://learn.adafruit.com/adafruit-qt-py/circuitpython-pins-and-modules
9. Adafruit Learning System. *CircuitPython Digital In & Out* (`digitalio`, `Direction`, `Pull`, `value`). https://learn.adafruit.com/adafruit-grand-central/circuitpython-digital-in-out
10. Adafruit. *CircuitPython project README* (relationship to MicroPython, `code.py` on the CIRCUITPY drive, auto-reload). https://github.com/adafruit/circuitpython
11. Wokwi. *Wokwi for ESP32* (browser-based ESP32/ESP32-S3 simulator, starter templates, wiring and running a simulation). https://wokwi.com/esp32
12. Arduino. *Language Reference* (`pinMode`, `digitalWrite`, `delay`, and the `setup()`/`loop()` structure). https://www.arduino.cc/reference/en/

> **Note.** Example values, such as LED forward voltage and resistor values, are illustrative. Board-specific details (pin names, which USB connector to use, the on-board LED) depend on your board. Always confirm them with your board's own documentation.
