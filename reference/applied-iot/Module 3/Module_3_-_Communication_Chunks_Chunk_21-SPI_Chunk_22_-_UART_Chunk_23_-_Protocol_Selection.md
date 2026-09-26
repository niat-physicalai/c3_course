# Module 3 — Communication
## SPI, UART, and Choosing the Right Protocol

**Course:** Applied IoT
**Module:** 3 — Communication (continued)

---

## From One Shared Bus to Other Ways of Talking

In the previous reading, you connected an OLED display to your ESP32-S3 over **I2C**: two wires, SDA and SCL, shared by every device on the bus, with each device picked out by its own address. That is a good solution when you have several simple peripherals and want to use as few pins as possible.

But I2C is not the only way two chips talk to each other, and it is not always the best one. Some peripherals need to move data much faster than I2C comfortably allows. Others are not devices you address at all — they are just two things exchanging a stream of bytes, the way your computer talks to the ESP32-S3's serial console. This reading introduces the other two communication methods you will meet in this course: **SPI** and **UART**. Then it asks the more important question — given three ways of connecting devices, how do you decide which one to use?

```text
I2C  →  SPI  →  UART  →  Compare  →  Identify requirements  →  Select a protocol
```

Underneath all three protocols sits the same idea you have already used with I2C: **communication is an agreed set of rules**. Both sides must agree on what a HIGH or LOW pulse means, when to read it, and in what order the bits arrive. I2C, SPI and UART are three different agreements, each with its own trade-offs. Knowing the rules of a protocol matters less, in the end, than knowing *when* to reach for it.

---

## SPI: A Fast, Clocked Connection With No Addresses

### Why a Second Synchronous Protocol?

Like I2C, **SPI (Serial Peripheral Interface)** is a **synchronous** protocol: one device generates a clock signal, and both sides read and write bits in time with it, the way you read and write with I2C's SCL line. What SPI changes is the wiring and the speed. Instead of squeezing both directions of data onto a single shared wire, SPI gives each direction its own dedicated line. That extra wiring is the price SPI pays for being able to move data considerably faster than I2C, and for sending and receiving at the same time.

### The Four Signal Lines

A standard SPI connection uses four logical lines between a **controller** (traditionally called the "master") and a **peripheral** ("slave"):

| Line | Common older name | Newer name | Direction |
|---|---|---|---|
| Clock | SCK / SCLK | SCLK | Controller → peripheral |
| Controller-out, peripheral-in | MOSI | COPI | Controller → peripheral |
| Controller-in, peripheral-out | MISO | CIPO | Peripheral → controller |
| Chip Select | SS | CS | Controller → peripheral |

You will see both naming schemes in the wild. Older datasheets and a good deal of existing code still use **MOSI** and **MISO**; CircuitPython's documentation has moved toward **COPI** and **CIPO** to describe the same two lines without master/slave language. They refer to the same wires — get comfortable recognising both.

```text
   Controller (ESP32-S3)              Peripheral
   ┌──────────────┐                  ┌──────────────┐
   │          SCK ├─────────────────►│ SCK          │  clock, set by controller
   │  MOSI/COPI   ├─────────────────►│ MOSI/COPI    │  data out from controller
   │  MISO/CIPO   │◄─────────────────┤ MISO/CIPO    │  data back from peripheral
   │           CS ├─────────────────►│ CS           │  "you're selected" signal
   └──────────────┘                  └──────────────┘
```

Notice that data can travel in both directions **at the same time**, on the same clock edges. That is what it means for SPI to be **full-duplex**: while the controller is shifting a byte out on MOSI, the peripheral can be shifting a byte back on MISO, in the same instant. I2C cannot do this — only one side transmits on SDA at a time.

### Chip Select: Choosing Who Is Listening

I2C picks out a device by sending its address over the shared bus. SPI has no equivalent of an address byte. Instead, the clock, MOSI and MISO lines can be shared by several peripherals, but each peripheral gets its **own dedicated CS line**, run directly from the controller. A peripheral only pays attention to the clock and data lines while its own CS line is held in its active state — for most SPI parts, that means CS is pulled **LOW** to select the device and released HIGH to deselect it.

```text
                     SCK ──────────────┬──────────────┐
                    MOSI ──────────────┼──────────────┤
                    MISO ──────────────┼──────────────┤
                                        │              │
   Controller ── CS1 ────────────────► Peripheral 1    │
   Controller ── CS2 ─────────────────────────────────► Peripheral 2
```

Only the peripheral whose CS line is currently asserted responds; the rest ignore the shared lines entirely. This has a direct practical consequence: **the number of SPI peripherals you can wire up is limited by the number of free GPIO pins you can dedicate to CS**, not by an address space. Ten I2C sensors might share two wires; ten SPI sensors need two shared wires *plus* ten separate CS pins.

> **Predict:** If two SPI peripherals accidentally shared the same CS pin, what would you expect to see on the MISO line when the controller tried to read from just one of them?

### Setting Up SPI in CircuitPython

CircuitPython exposes SPI through the `busio.SPI` class. You build the bus from the clock, controller-out and controller-in pins, then explicitly claim the bus before configuring it:

```python
import board
import busio
import digitalio

# The shared SPI bus: clock, controller-out (MOSI/COPI), controller-in (MISO/CIPO)
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# CS is not part of busio.SPI — you drive it yourself, like any digital output
cs = digitalio.DigitalInOut(board.CHOSEN_CS_PIN)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True  # released; most peripherals select on LOW

while not spi.try_lock():
    pass
spi.configure(baudrate=1_000_000, polarity=0, phase=0)
spi.unlock()
```

A few things are worth noticing here. First, `try_lock()` and `unlock()` exist because an SPI bus can be shared by several pieces of code or several peripherals, and only one of them should be configuring and using it at any moment — locking the bus prevents two parts of a program from talking over each other. Second, **CircuitPython does not manage CS for you**. Unlike the clock and data lines, CS is just an ordinary `digitalio` output pin that your program drives low before talking to a peripheral and high afterwards:

```python
cs.value = False                 # select the peripheral
spi.write(bytes([0x01, 0x02]))   # send two bytes
cs.value = True                  # deselect it again
```

Not every GPIO pin on an ESP32-S3 board is wired to support SPI's clock or data functions, and which pins do depends on the specific board. Check the `board` module for your hardware (for example with `dir(board)`) rather than assuming a pin will work, and use whatever SPI-capable pins and CS pin your course setup specifies for the peripheral you are wiring.

### SPI Side by Side With I2C

| | I2C | SPI |
|---|---|---|
| Wires for data | 2 (SDA, SCL), shared | Typically 3 shared (SCK, MOSI, MISO) + 1 CS per peripheral |
| How a device is selected | By address, sent over the bus | By a dedicated CS line |
| Duplex | Half-duplex (one direction at a time) | Full-duplex (both directions at once) |
| Typical speed | Lower | Generally higher |
| Adding another peripheral | Usually free, if addresses don't clash | Costs one more GPIO pin (CS) |

> **Compare:** A sensor's datasheet says it needs a very high data rate and supports full-duplex transfer. Based on the table above, which protocol would you reach for first, and why?

---

## UART: Two Devices, No Shared Clock, No Bus

### An Asynchronous Protocol

I2C and SPI are both **synchronous**: one wire in the connection is a clock, so both devices always agree on the exact moment to read each bit. **UART (Universal Asynchronous Receiver/Transmitter)** drops the clock line entirely. There is no shared timing signal at all — each device keeps its own internal timing and simply agrees in advance on *how fast* to send bits. That agreement is the **baud rate**, and it is the one thing that makes an asynchronous link work without a shared clock.

```text
Synchronous (I2C, SPI):    controller sends a clock pulse ──► "read now"
Asynchronous (UART):       no clock line ──► both sides must already agree on timing
```

### TX and RX: A Point-to-Point Link

UART connects exactly two devices, using two lines:

- **TX** (transmit) on one device, wired to **RX** (receive) on the other.
- **RX** on the first device, wired to **TX** on the other.

```text
   Device A                       Device B
   ┌────────┐                    ┌────────┐
   │  TX    ├───────────────────►│  RX    │
   │  RX    │◄───────────────────┤  TX    │
   └────────┘                    └────────┘
```

Because TX and RX are separate wires, both devices can send at the same time — UART is full-duplex, like SPI. But unlike I2C and SPI, there is **no shared bus and no addressing at all**. UART is fundamentally **point-to-point**: one TX/RX pair connects exactly two devices. If you want a third device in the conversation, you need another dedicated pair of pins (or extra hardware), not another address.

This is exactly the kind of link your ESP32-S3 already uses to talk to your computer over its serial console — a point-to-point conversation between two specific devices, nothing shared.

### Baud Rate: Agreeing on Timing Instead of Sharing a Clock

**Baud rate** is the rate, in symbols per second, at which bits are sent. Both devices must be configured to the **same** baud rate, because that number is the only thing standing in for the missing clock wire. If Device A sends bits every 104 microseconds (roughly what 9600 baud implies) and Device B expects a new bit every 52 microseconds, then B will sample TX at the wrong moments and read nonsense.

```text
Matching baud rates:     A sends at 9600 baud ── B listens at 9600 baud ── data reads correctly
Mismatched baud rates:   A sends at 9600 baud ── B listens at 19200 baud ── garbled bytes
```

### UART in CircuitPython

```python
import board
import busio

uart = busio.UART(board.TX, board.RX, baudrate=9600)

uart.write(b"hello\n")

data = uart.readline()
if data is not None:
    print(data)
```

`busio.UART` takes the TX pin, the RX pin and a baud rate. `write()` sends bytes out on TX; `readline()` waits (up to a timeout) for data arriving on RX and returns it once a line is complete. As with SPI, whether a given pin on your board can act as UART TX or RX depends on that board's pin definitions — confirm the pins you need against your board's documentation rather than assuming any pin will do.

> **Experiment:** Configure two devices for UART communication, set them to the same baud rate, and confirm you can send a message and read it back correctly. Then change the baud rate on only one side and try again. What do you observe on the receiving end? Does it fail cleanly, or produce readable-looking but wrong data?

> **Troubleshoot:** If a UART link that used to work suddenly starts producing garbled text after you changed some code, what is the first setting you should check?

---

## Three Protocols, One Decision

You now have three ways to move data in and out of your ESP32-S3, each shaped by a different set of trade-offs.

| | I2C | SPI | UART |
|---|---|---|---|
| Timing | Synchronous (shared clock, SCL) | Synchronous (shared clock, SCK) | Asynchronous (agreed baud rate, no clock) |
| Topology | Shared bus | Shared clock/data lines + per-device CS | Point-to-point only |
| How a device is chosen | Address on the bus | Dedicated CS line | N/A — only two devices exist on the link |
| Duplex | Half-duplex | Full-duplex | Full-duplex |
| Wires needed for *n* peripherals | 2, regardless of *n* | 3 + *n* (one CS each) | 2 per pair of devices |
| Typical use | Several simple sensors sharing pins | High-speed peripherals: displays, SD cards, fast ADCs | A direct link to one other device: a PC, a GPS module, another microcontroller |

### Questions Worth Asking Before You Pick a Protocol

Rather than memorising this table, it helps to turn it into a short list of questions you ask about *your* system, before you ask which protocol you already know best:

- **How many devices need to be connected?** One other device points toward UART. Several sensors on a budget of pins points toward I2C. Several fast peripherals, if you have pins to spare for CS lines, points toward SPI.
- **How many GPIO pins can you spare?** I2C is the cheapest in pins as device count grows. SPI's pin cost grows with every extra peripheral. UART needs a fresh pair per additional point-to-point link.
- **How fast does the data need to move?** SPI is generally the fastest of the three. If a peripheral's datasheet demands a high data rate, that alone can rule out I2C.
- **Does the device need to be individually addressed, or is it the only thing on the line?** Addressing is I2C's job. Selection by a dedicated line is SPI's job. If there is only ever one other device, neither is necessary — that is UART's territory.
- **Do you need both directions to work simultaneously (full-duplex), or is one direction at a time acceptable?** SPI and UART both support full-duplex; I2C does not.
- **What does the peripheral itself support?** In practice, this is usually the deciding factor: a sensor or module's datasheet will tell you which protocol(s) it speaks, and you work within that rather than choosing freely.

> **Apply — Scenario 1.** You need to connect four small sensors to your ESP32-S3, and you only have a handful of spare GPIO pins. Each sensor has a distinct, factory-set address. Which protocol characteristics make one option clearly more practical here than the others?
>
> **Apply — Scenario 2.** A peripheral's datasheet specifies a high-speed synchronous interface and full-duplex transfer, and you have pins to spare. What would make you look at SPI over I2C for this peripheral, and what would you need to check before committing to it?
>
> **Apply — Scenario 3.** Two boards need to exchange short text messages, and there will never be a third device in the conversation. What about this requirement makes UART a reasonable, low-complexity choice, and what is the one setting you must make sure both sides agree on?

The point of working through problems like these is not to arrive at a single "correct" protocol chiseled in stone — several of them can often be made to work. The point is to be able to explain *why* one fits the requirements better than the others, using the actual constraints of the system: pin budget, device count, speed, topology and what the peripheral itself supports. A protocol chosen because "it's the one I know" will eventually run into a requirement it cannot meet; a protocol chosen by reading the requirements first rarely will.

---

## Bringing the Three Together

Across this module you have now built, wired and reasoned about all three of the communication methods you are likely to meet on an ESP32-S3 project: I2C's shared, addressed bus; SPI's fast, full-duplex, CS-selected lines; and UART's simple, clocked-free, point-to-point link. Each solves the same underlying problem — getting bits reliably from one chip to another — with a different balance of pins, speed, topology and complexity.

As you move into building larger systems, the recurring question is the one this reading has been pointing toward:

> What does my system actually need to communicate, and which protocol's characteristics fit those requirements — not which protocol happens to be the one I used last?

That question, asked honestly at the start of a design, will save far more debugging time than any amount of protocol trivia memorised afterward.

---

### References

1. Adafruit Learning System. *SPI* (CircuitPython learn guide covering SCK, MOSI/COPI, MISO/CIPO, CS, and full-duplex behaviour). https://learn.adafruit.com
2. CircuitPython documentation. *busio – Hardware accelerated behavior* (`busio.SPI`, `try_lock`, `configure`, `unlock`). https://docs.circuitpython.org/en/latest/shared-bindings/busio/
3. CircuitPython documentation. *busio.UART* (`busio.UART`, `write`, `readline`, baud rate configuration). https://docs.circuitpython.org/en/latest/shared-bindings/busio/
4. Adafruit Learning System. *Circuit Playground UART Serial* and related guides on point-to-point serial communication, TX/RX wiring and baud-rate matching. https://learn.adafruit.com
5. Adafruit / CircuitPython documentation. *Comparing SPI, I2C, and UART* style guidance on protocol trade-offs (pin count, addressing, duplex, speed). https://learn.adafruit.com
6. Espressif Systems. *ESP32-S3 Technical Reference* (GPIO matrix and multiple hardware SPI/UART peripheral controllers). https://www.espressif.com

> **Note.** Baud rates, CS pin names and example bytes in this reading are illustrative. Which specific GPIO pins on your ESP32-S3 board support SPI or UART functions depends on that board's own pin definitions — always confirm with your board's documentation or the `board` module (`dir(board)`) rather than assuming a pin name shown here exists on your hardware.