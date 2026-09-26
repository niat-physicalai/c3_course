# Module 3 — Communication
## From GPIO to I2C: Talking to Intelligent Peripherals

**Course:** Applied IoT
**Module:** 3 — Communication

---

## From Controlling Pins to Talking to Devices

In the last two modules, every physical thing you connected to your ESP32-S3 spoke a very simple language. A button was either pressed or not pressed. An LED was either on or off. A potentiometer's wiper sat somewhere between 0 V and the supply voltage, and the ADC turned that into a single number. In every case, one pin carried one piece of information, and your program read or set that pin directly.

That simplicity is also a limit. Many of the components you will want to use in an IoT project are not simple two-state or single-voltage devices. A small screen, a real-time clock, an environmental sensor with multiple internal settings, a motion sensor with configurable sensitivity — these are small computers in their own right, each with internal memory, multiple functions and settings, and data to send back that is more than a single bit or a single voltage. You cannot wire a screen's entire image to one GPIO pin. You need a way to send it *structured* information: which pixel, which letter, which command.

This reading is about that jump: from **controlling** a pin to **communicating** with a device. It introduces the idea of a communication protocol in general, then focuses on one specific, very common protocol — **I2C** — and uses it to do something genuinely useful: display live sensor readings on a small OLED screen.

```text
Digital I/O, Analog I/O  →  Communication protocols  →  I2C  →  OLED display
   (M1, M2)                  (this reading)              (this reading)
```

## Why GPIO Alone Is Not Enough

Think about what a single GPIO pin can actually express. As a digital output, it can be HIGH or LOW — one bit. As a digital input, it can report HIGH or LOW back — again, one bit. As an analog input, it can report a voltage as a number, but that number describes only one physical quantity, sampled at one moment, on one pin.

Now consider an OLED display. To show even a short piece of text, the display needs to know *which* pixels to turn on, in *which* rows and columns, matching the shapes of specific letters, and it needs this information updated every time the text changes. That is thousands of bits of structured information, not one bit or one voltage. Wiring a separate GPIO pin to every pixel would need far more pins than any microcontroller has, and would still not tell the display *when* a new pixel value applies or *which pixel* is being set.

The same problem, on a smaller scale, applies to many everyday sensors. A humidity and pressure sensor might need to be told which internal setting to use before it takes a reading, and then asked, separately, for the temperature, the humidity and the pressure it just measured. A single digital or analog pin cannot carry "please give me the humidity reading" as a distinct request from "please give me the pressure reading."

Devices like this are sometimes called **intelligent peripherals**: chips with their own internal logic, memory and multiple addressable functions, as opposed to a passive component like an LED or a resistor. Talking to an intelligent peripheral requires more than setting a pin HIGH or LOW. Both sides — your microcontroller and the peripheral chip — need to agree on how information is packaged, in what order, and how each side knows when a message starts, what it means and when it ends.

That agreement is a **communication protocol**.

## What a Communication Protocol Actually Is

A communication protocol is a shared set of rules that both sides of a conversation follow, so that a stream of electrical signals can be turned back into meaningful information. A protocol typically settles questions such as:

- How is a single **bit** represented electrically, and how is its timing marked?
- How are bits grouped into **bytes** or **messages**?
- If several devices share the same wires, how does a message say **which device** it is for?
- How does a receiver know a message has **started** and **finished**?
- What happens if something goes wrong, and how are **errors** detected?

You already use protocols without thinking about them: when two people agree that a nod means "yes" and a shake of the head means "no," they have agreed on a tiny protocol. Electrical communication protocols do the same job, but far more precisely and far faster, because the "conversation" happens in millionths of a second and must be repeatable, exactly the same way, millions of times a day.

For IoT systems specifically, protocols are what let a small, cheap microcontroller work with sensors, displays, memory chips and other microcontrollers that were designed independently, by different manufacturers, often without ever being tested together. As long as both sides implement the same protocol correctly, they can talk.

## Serial and Parallel Communication, Briefly

Before looking at a specific protocol, it helps to understand one basic design choice every protocol designer faces: how many wires to use.

**Parallel communication** sends several bits at the same time, each bit on its own wire. If you want to send one byte (8 bits), you could use 8 wires, and transmit the whole byte in a single tick. This can be fast, but it does not scale well: more bits means more wires, more pins used on both chips and more opportunities for the signals on different wires to arrive very slightly out of step with each other as the connection gets longer or faster.

**Serial communication** sends bits one after another, over one wire (or a very small number of wires). It is slower per "tick," because only one bit moves at a time, but it needs far fewer physical connections, and it keeps working reliably over longer distances and higher speeds than parallel wiring typically allows.

```text
Parallel (illustration only):        Serial (illustration only):
  Wire 1: 1                            Wire: 1 → 0 → 1 → 1 → ...
  Wire 2: 0        (all bits
  Wire 3: 1        at once)
  Wire 4: 1
```

Almost every protocol you are likely to meet when connecting a microcontroller to a sensor, display or memory chip — **I2C**, **SPI** and **UART** — is a serial protocol. That is why serial communication is worth understanding clearly now: the rest of this module, and the next one, builds directly on it.

## Introducing I2C

**I2C** (pronounced "eye-squared-C," short for **Inter-Integrated Circuit**) is one of the most common serial protocols used to connect a microcontroller to nearby peripheral chips: displays, sensors, real-time clocks, memory chips and more. Its defining feature is that it needs only **two wires**, no matter how many devices are attached to it.

Those two wires are:

- **SDA — Serial Data.** This wire carries the actual bits being exchanged, in both directions.
- **SCL — Serial Clock.** This wire carries a timing signal, generated by the controller, that tells every device exactly when to read or write a bit on SDA.

```text
        SDA  ───────────────────────────────────
                    (data, both directions)

        SCL  ───────────────────────────────────
                    (clock, one direction: from the controller)
```

The clock line solves a problem you may not have thought about yet: how does a receiver know *when* to look at the data line? In parallel communication with a separate clock wire, and in I2C, the clock line answers that question directly — each clock pulse marks the moment a bit on SDA should be read. Without a shared clock, both sides would need to somehow agree on timing in advance and never drift out of sync, which is difficult over long, slow communications and is one of the practical reasons I2C carries its own clock.

### Controller and Peripheral

I2C connects devices with two different roles.

- The **controller** (the ESP32-S3, in this course) is the device that starts every conversation. It drives the clock line, decides when a transaction begins, and chooses which peripheral it wants to talk to.
- A **peripheral** is a device that listens for its turn, and responds only when the controller addresses it directly. A peripheral never starts a conversation on its own.

You may see older material use the terms "master" and "slave" for these same two roles; current documentation and specifications use **controller** and **peripheral** (or **target**), which is the terminology this course uses.

This is a genuinely different relationship from a GPIO pin. With GPIO, your program directly forces a voltage, or directly reads one, at every instant. With I2C, your program issues a structured *request* — "peripheral at this address, here is a command" or "peripheral at this address, send me data" — and the protocol layer (handled for you by CircuitPython) takes care of putting that request onto SDA and SCL correctly, bit by bit, with the right timing.

## Sharing One Bus Among Many Devices

The real payoff of I2C's two-wire design appears when you need more than one peripheral. Every I2C device on the same bus connects to the *same* SDA wire and the *same* SCL wire:

```text
                 3.3 V
                   │
          ┌────────┼────────┐
          │        │        │
     [ pull-up ] [ pull-up ]
          │        │
  SDA ────┴────────┴─────────────┬──────────┬───────────
  SCL ──────────────┬────────────┼──────────┼───────────
                     │            │          │
               ┌─────┴───┐  ┌─────┴───┐ ┌────┴────┐
               │Controller│  │  OLED   │ │ Sensor  │
               │ (ESP32-S3)  │(address)│ │(address)│
               └──────────┘  └─────────┘ └─────────┘
```

Because I2C peripherals only ever *pull the lines low*, and never actively drive them high, both SDA and SCL need **pull-up resistors** to hold them at the supply voltage when nothing is being sent — the same pull-up idea you met with buttons in Module 2, applied here to a shared bus. Many small I2C breakout boards, including common OLED modules, already include these pull-up resistors on the board itself, which is one reason they are simple to wire.

With only two shared wires, though, a new question appears immediately: if the controller sends a bit on SDA, how does it make sure only the *intended* peripheral responds, and not all of them at once?

## I2C Addresses

The answer is **addressing**. Every I2C peripheral has a **device address**, usually a 7-bit number (from 0 up to 127), and the controller includes that address as the very first thing it sends in a transaction. Every peripheral on the bus "hears" the address, but only the one that recognizes its own address responds; the rest stay silent.

This is the key idea that makes a shared two-wire bus work at all: **the wires are shared, but the conversations are not.** The controller can talk to a display at one address, then a sensor at a different address, over the same two physical wires, one transaction at a time.

A device's address is usually fixed by its manufacturer, though some breakout boards let you change it slightly, for example with a solder jumper or an address pin, precisely so that two identical devices can share a bus without conflicting.

### What Happens with a Conflict

If two devices on the same bus are set to the *same* address, the controller has no way to tell them apart. When it addresses that number, both devices may try to respond at once, and the result is unreliable: garbled data, a device that never seems to answer correctly, or unpredictable behavior that is hard to reproduce. This is a genuinely common real-world bug, and it is one reason experienced builders check device addresses *before* wiring up multiple similar peripherals.

### Finding Out What Is Actually on the Bus: Address Scanning

Because you should never simply assume a device's address — datasheets sometimes disagree with what is printed on a board, and some modules can be configured differently — the practical way to find out is to ask the bus directly. This is called **address scanning**: the controller tries every possible address in turn and notes which ones get a response.

In CircuitPython, the `busio.I2C` object provides exactly this as a built-in method, `scan()`. Because the I2C bus is a shared resource that other parts of your program (or other libraries) might also want to use, CircuitPython requires you to explicitly **lock** the bus before scanning it, and **unlock** it afterward:

```python
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass

try:
    found = i2c.scan()
    print("I2C addresses found:", [hex(addr) for addr in found])
finally:
    i2c.unlock()
```

Notice that the pins are given as `board.SCL` and `board.SDA`, not as specific GPIO numbers. CircuitPython's `board` module maps these names to whichever physical pins your ESP32-S3 board actually uses for I2C, so the same code works regardless of the exact pin numbers underneath — you should always use `board.SCL` / `board.SDA` (or the convenience function `board.I2C()`, which returns a ready-made shared bus) rather than hardcoding pin numbers.

Running this scan should print a short list of hexadecimal numbers — the addresses of whatever I2C devices are wired up and powered. If the list is empty, something is wrong with the wiring or the device is not powered; if it contains an address you did not expect, that is useful information too.

> **Before you scan:** connect only SDA to SDA, SCL to SCL, and provide power (usually 3.3 V) and ground to your I2C peripheral. Reversing SDA and SCL is a very easy mistake to make and usually shows up as an empty scan.

## The OLED Display as an I2C Peripheral

A small monochrome **OLED display** is a good first I2C peripheral to work with because it gives you an immediate, visible result, and because it is a genuine example of the kind of "intelligent" peripheral that motivated this whole reading: it has internal memory holding the image, and it needs structured commands, not a single voltage, to display anything useful.

Most small I2C OLED modules you will meet are built around a display driver chip called the **SSD1306**. On the bus, the OLED behaves exactly like the peripheral described above: it has a device address (commonly **0x3C**, though some modules use **0x3D**), and it does nothing until the controller addresses it and sends it commands or pixel data.

> **Do not assume the address.** Whether your particular OLED module answers at 0x3C or 0x3D depends on the specific board. Always confirm it with an address scan, as shown above, rather than typing in a value from memory.

Once addressed, the OLED accepts two broad kinds of messages from the controller: **commands**, which configure things like the display's memory addressing mode, and **data**, which is the actual pixel content to show. CircuitPython libraries handle the details of formatting these commands and data correctly; your job is to call functions like "write this text" and "show it," and the library takes care of turning that into the right sequence of I2C messages.

## Initializing and Using the OLED in CircuitPython

The `adafruit_ssd1306` library provides a simple, framebuffer-style way to work with SSD1306 OLEDs: you draw into an in-memory picture of the screen, then send that whole picture to the display at once.

```python
import board
import busio
import adafruit_ssd1306

i2c = board.I2C()          # uses the board's default SCL/SDA pins

# Width, height and address depend on your specific module.
# Confirm the resolution in your module's documentation, and
# confirm the address with an I2C scan before hardcoding it here.
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)                    # clear the display buffer (all pixels off)
oled.text("Hello, IoT!", 0, 0, 1)   # draw text into the buffer
oled.show()                     # push the buffer to the physical screen
```

A few details are worth noticing, because they tell you something about how the display actually works:

- `oled.fill(0)` and `oled.text(...)` only change a **buffer in memory** — nothing on the physical screen changes yet. This mirrors the idea of structured communication: the controller prepares a complete picture before sending it, rather than updating individual pixels one at a time over the bus.
- `oled.show()` is the step that actually sends the buffer to the display over I2C. If you forget to call it, your changes never appear.
- The width and height (`128, 64` above) must match your actual module. Some OLEDs are 128×32 pixels rather than 128×64; check your module's documentation, because passing the wrong size will make the display behave strangely even if the wiring is correct.

You will also see a newer library, `adafruit_displayio_ssd1306`, which integrates with CircuitPython's more general `displayio` graphics system. Both libraries talk to the same SSD1306 chip over the same I2C bus; they simply offer different ways of describing what to draw. This reading uses the simpler, text-focused approach, since the goal here is to understand I2C communication through a working display, not to master graphics programming.

## Building the Sensor → I2C → OLED System

The real point of adding a display is not to show a fixed string — it is to make the *invisible* readings from your sensors visible, without needing a serial console. This closes the loop you have been building since Module 2: a sensor produces a number, your program processes it, and now an actuator-like output — the OLED — presents it directly to a person.

```text
Sensor  ──►  ESP32-S3 (CircuitPython)  ──►  I2C bus (SDA/SCL)  ──►  OLED
(e.g. reading            (reads the sensor,                    (displays the
 temperature)             formats a string)                     text on screen)
```

A minimal version, reusing a sensor reading from Module 2 (adjust to whichever sensor and reading you already have working), might look like this:

```python
import time
import board
import adafruit_ssd1306
# ... plus whatever import your sensor from Module 2 needs

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

while True:
    reading = read_my_sensor()          # from your Module 2 code
    oled.fill(0)
    oled.text("Sensor reading:", 0, 0, 1)
    oled.text(str(reading), 0, 16, 1)
    oled.show()
    time.sleep(1)
```

Notice that this program uses the **same I2C bus object**, `i2c`, that a sensor library might also need, if your chosen sensor happens to be an I2C device itself rather than a digital or analog one. This is exactly the situation the shared-bus idea was built for: several devices, one pair of wires, each reached by its own address. If your sensor is analog or a simple digital sensor from Module 2, it uses its own pin as before, and only the OLED uses I2C — which is a perfectly reasonable first system, and a good one to get working before adding a second I2C device to the same bus.

**Try it and observe:** what happens if you remove the `oled.show()` call? What happens if you call `oled.fill(0)` but never draw new text before showing it again? Predicting the answer, and then checking it, is a fast way to build an accurate mental model of what the buffer-then-show pattern is actually doing.

## Troubleshooting I2C and OLED Problems

Because I2C hides a lot of detail behind a simple-looking API, when something goes wrong the symptoms can look mysterious. The table below connects common symptoms to their usual causes, in roughly the order you should check them.

| Symptom | Likely cause | What to check |
|---|---|---|
| `i2c.scan()` returns an empty list | Wiring problem, or device unpowered | Confirm SDA↔SDA and SCL↔SCL (not swapped), confirm power and ground are connected, confirm the device has a power indicator if it has one |
| Scan finds a device, but the OLED constructor fails | Wrong address used in code | Use the address from your own scan, not an assumed value; try both 0x3C and 0x3D if unsure |
| Scan finds a device, but nothing appears on screen | Wrong width/height passed to the library, or `show()` never called | Check the module's actual pixel resolution; make sure `oled.show()` runs after each change |
| Program raises an error mentioning the I2C bus being "in use" or locked | Bus locked by a previous `try_lock()` that was never unlocked, or multiple `busio.I2C` objects created | Prefer `board.I2C()` for a single shared bus object; always `unlock()` after a manual scan |
| Import error for the OLED library | Library not installed on the CIRCUITPY drive | Confirm the required `.mpy` library file is present in your `lib` folder |
| Bus works with one device, breaks when a second I2C device is added | Address conflict between the two devices | Scan again with both devices connected; if the addresses match, check for an address-select jumper or pin on one of them |

The general troubleshooting habit from earlier modules still applies here: **predict → measure → explain**. Before changing code at random, predict what a working scan or a working display should show, run the scan or the program, compare the actual result to your prediction, and use the difference to decide what to check next.

## Where This Leaves You

You now have a second way for your ESP32-S3 to reach the physical world, alongside plain digital and analog I/O: a genuine communication protocol, carried over two shared wires, that lets the controller address specific peripherals, request specific data and send structured information such as a full screen of text. You have seen why this was necessary — GPIO pins simply cannot express the structured, multi-device conversations that intelligent peripherals need — and you have used address scanning as a concrete, practical way to find out exactly what is on a bus rather than guessing.

I2C is only one member of a small family of serial protocols used constantly in embedded and IoT systems. The next reading in this module introduces **SPI** and **UART**, two other serial protocols with different trade-offs — more wires but often higher speed, or a very simple point-to-point link with no addressing at all — and looks at how to choose between I2C, SPI and UART for a given peripheral. Everything you have just learned about serial communication, controllers, and structured messages carries forward directly into that comparison.

---

### References

1. NXP Semiconductors. *I2C-bus specification and user manual* (SDA/SCL, controller–peripheral terminology, addressing). https://www.nxp.com/docs/en/user-guide/UM10204.pdf
2. CircuitPython documentation. *busio – Bus protocol support* (`busio.I2C`, `try_lock`, `unlock`, `scan`). https://docs.circuitpython.org/en/latest/shared-bindings/busio/index.html
3. CircuitPython documentation. *board – Board-specific pin definitions* (`board.SCL`, `board.SDA`, `board.I2C()`). https://docs.circuitpython.org/en/latest/shared-bindings/board/index.html
4. Adafruit CircuitPython SSD1306 library documentation (`adafruit_ssd1306`, `fill`, `text`, `show`). https://docs.circuitpython.org/projects/ssd1306/en/latest/
5. Adafruit CircuitPython displayio SSD1306 library documentation (alternative `displayio`-based approach). https://docs.circuitpython.org/projects/displayio-ssd1306/en/latest/
6. Solomon Systech. *SSD1306 OLED driver datasheet* (I2C and SPI interface, command/data model). Distributed by display module manufacturers.

> **Note.** I2C addresses (including 0x3C and 0x3D for OLED modules), display resolutions and pin names are examples and depend on your specific hardware. Always confirm a device's address with an I2C scan rather than assuming one, and confirm pin names, display resolution and required libraries against your own board's and module's documentation.