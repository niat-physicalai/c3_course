# B1 — Talking to Sensors: Choosing the Interface
## Picking I²C, SPI, UART or Analog for Each Part, and Saying Why

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 2 — Sensing and Hardware Architecture
**Time:** ~1 hour · **You will produce:** an interface comparison table and a justified interface choice for each peripheral

---

### The Display Is Using Most of the Bus. Should It Move?

<!-- REFPRODUCT:START -->
esp_watch's display, redrawn 30 times a second over I²C at 400 kHz, would take about 75% of the bus (you will check that sum yourself in B2), leaving the two sensors to share the rest. You can buy the same 0.96-inch SSD1306 display in a version with an SPI connection. SPI is much faster. Should esp_watch have used it?
<!-- REFPRODUCT:END -->

### What You Will Be Able to Do After This Reading

- **Compare** I²C, SPI, UART, analog and pulse interfaces on pins, speed, device count, distance and failure modes.
- **Calculate** how long a transfer takes on each interface, and what that means for a shared bus.
- **Select** an interface for each peripheral, and **justify** it from your pin budget and data rates.
- **Diagnose** the common interface faults: wrong pull-ups, address clashes, baud mismatches and a missing common ground.

### What Part 1 Already Covered

Part 1 taught how I²C, SPI and UART work. Here you choose between them under a full pin budget, and write down a reason for each choice.

---

## The Interfaces Side by Side

| | I²C | SPI | UART | Analog (ADC) | Pulse / one-wire |
|---|---|---|---|---|---|
| Wires (plus ground) | 2, shared by all devices | 3 shared + 1 chip select per device | 2 per device (TX, RX) | 1 per signal | 1 per device |
| Devices per connection | Many, by address | Many, by chip select | One | One | One (or a few, for one-wire buses) |
| Typical speed | 100 or 400 kHz | Several MHz | 9,600 to 115,200 baud is common | Limited by the ADC and filtering | Depends on the protocol |
| Needs pull-ups | Yes | No | No | No | Often |
| Can read back from the device | Yes | Usually; some devices are write-only | Yes | — | Yes |
| Typical distance | Centimetres, on one board | Centimetres | Metres | Short; noise-sensitive | Varies |
| Typical parts | Sensors, small displays, clocks | Fast displays, memory, fast sensors | GPS, modems, self-contained modules | Potentiometers, simple light or temperature sensors, battery sense | Some temperature sensors, ultrasonic distance |

> **Teaching model.** These are typical values to help you compare, not limits. Some I²C devices run faster, some UARTs much faster, and an analog signal's usable speed depends on the sensor as much as the ADC. The datasheets of your actual parts decide.

Three ideas from this table matter more than the rest.

**Pins cost more than speed on a small board.** esp_watch uses every pin it can safely spare (B3 builds its full pin budget). An interface that needs four pins where another needs zero extra is often decided by the pin budget before speed even comes into it.

**Sharing is both the strength and the weakness of a bus.** I²C lets many devices share two wires, but they then share the bus time, the pull-ups and the fate of the bus: one faulty device can stop all of them.

**Some interfaces cannot read back.** The SSD1306 datasheet states that in its serial (SPI) mode "only write operations are allowed" [1]. That matches a lesson esp_watch learned the hard way (below): if you can only write to a device, you cannot use it to check that the connection works.

## Worked Example: Should esp_watch's Display Move to SPI?

**Step 1: What does SPI need?** In 4-wire SPI mode the SSD1306 uses a clock (SCLK), data in (SDIN), chip select (CS#) and data/command select (D/C#), plus a reset line (RES#) [1]. That is 4 to 5 microcontroller pins, depending on whether reset is tied to the microcontroller or wired separately.

**Step 2: How fast would it be?** The datasheet's minimum clock cycle for SPI is 100 ns [1], so up to 10 MHz.

```text
One full screen: 1,024 bytes × 8 bits = 8,192 bits
At 10 MHz: 8,192 ÷ 10,000,000 = 0.82 ms
On I²C at 400 kHz (measured on esp_watch): about 25 ms
```

SPI would be about 30 times faster, and it would take the display off the I²C bus entirely, leaving the sensors the whole of it.

**Step 3: Can the pin budget pay for it?**

<!-- REFPRODUCT:START -->
esp_watch uses only 4 of the XIAO's 11 pins: SDA, SCL and the two buttons. Neither sensor's interrupt is wired, and there is no battery-sense pin. So pins are free, but look at which ones: GPIO4 and GPIO5 are clear, GPIO2, GPIO8 and GPIO9 are strapping pins that must be high at reset, and GPIO20/21 are the UART used for debugging. Four or five SPI lines would need at least one strapping pin or the debug UART.
<!-- REFPRODUCT:END -->

So the budget *can* pay, but only by driving strapping pins (which must not be held low at reset) or giving up the debug UART. Possible, with care.

**Step 4: Is there a cheaper fix for the real problem?** The real problem was bus *time*, not bus speed. Redrawing the display only when something changes removes most of its bus use (B2 and D2 show how). That costs no pins and no hardware.

**Check.** SPI is faster and esp_watch could just about find the pins, but the problem it would solve has a free firmware fix. **Conclusion: keep the display on I²C and redraw on change.** For a product with a bigger microcontroller, or animations that genuinely need 30 frames a second, the answer could reasonably be the opposite. Writing down the reasoning, not just the result, is what lets someone make that call later.

## Choosing, Peripheral by Peripheral

For each peripheral, ask these questions in order:

1. **What does the part offer?** Many sensors only have one interface. If so, the choice is made, and your job is to fit it in.
2. **How many pins can you spend?** Count your MCU's free pins now; B3 turns this into a full pin budget.
3. **How much data, how often?** Estimate bytes per second: bytes per reading × readings per second.
4. **How many devices will share the connection?** Check addresses on I²C, chip selects on SPI.
5. **How far does the signal travel?** Across a 38 mm board, anything works. Down a cable, UART or a differential interface may be needed.
6. **How does it fail, and can you detect it?** A2's failure table needs an answer for each.

<!-- REFPRODUCT:START -->
esp_watch's choices, justified:

| Peripheral | Interface | Why | Watch out for |
|---|---|---|---|
| MAX30102 heart rate | I²C (0x57) | Only I²C is offered [2]. The module also has an interrupt pin, but esp_watch leaves it unconnected and polls the sensor | Module's pull-up voltage (the green module's 1.8 V problem) |
| MPU-6050 motion | I²C (0x68) | I²C is what the module exposes and the data rate is tiny; its interrupt pin is left unconnected | AD0 must be tied to a defined level |
| SSD1306 display | I²C (0x3C) | Shares the bus with no extra pins; redrawing only on change would fix the bus-time problem | Writes cannot confirm the bus works |
| Buttons | Digital input, internal pull-up | Simplest possible, one pin each | Switch bounce |
| Battery | Analog (ADC1) through a divider | A voltage is exactly what needs measuring | Chip-to-chip ADC variation; settling time |
<!-- REFPRODUCT:END -->

One point about the ESP32-C3 makes the I²C column worth thinking about. Its datasheet lists a single I²C interface [3]. Everything on esp_watch's I²C bus shares one controller, so a second I²C bus, a common fix for address clashes or overloaded buses on larger chips, is not a simple option here.

<!-- MEDIA
type: diagram
id: B1-01
caption: The same display, wired two ways: I²C (2 shared wires) versus 4-wire SPI (4–5 dedicated wires)
brief: A clean side-by-side wiring diagram. Left panel "I²C": XIAO ESP32-C3 with SDA and
  SCL lines running to a shared bus that also serves two sensor boxes and the display;
  one pull-up pair shown; label "2 pins, shared". Right panel "SPI": the same XIAO with
  SCLK, SDIN, CS, D/C and RES lines running only to the display, and the sensors still on
  a separate I²C pair; label "I²C 2 pins + SPI 4–5 pins". Colour-code shared versus
  dedicated wires. Show the XIAO's free-pin count under each panel (4 left vs 0 or −1).
  Flat vector style.
-->

## When Interfaces Fail

Most interface faults come down to a handful of causes. Learn to recognise them from their symptoms:

| Symptom | Likely cause | How to confirm |
|---|---|---|
| I²C device missing from a scan, or appearing and disappearing | Address pin floating; device unpowered; wrong address | Scan repeatedly; check how the address pin is set |
| Two devices "on" one address, garbled reads | Address clash | Scan with one device removed; check both datasheets |
| I²C works at 100 kHz, fails at 400 kHz | Pull-ups too weak for the capacitance, or too many in parallel | Calculate rise time (taught in B3; simulated in B5) |
| UART output is random characters | Baud-rate mismatch | Try the other side's rate; check both settings |
| UART silent | TX connected to TX instead of RX | Swap the two lines |
| Everything behaves oddly, readings drift | Missing common ground between two powered boards | Check a ground wire joins every board |
| SPI device ignores commands | Chip select not driven, or wrong SPI mode | Check chip select goes low during a transfer |
| Analog reading jumps around | Floating input, or a high-impedance source without a capacitor | Check the source; add filtering |

<!-- REFPRODUCT:START -->
esp_watch's bench testing with the author's `i2c_debug` sketch <!-- ASSET:PLACEHOLDER reference-files/firmware/i2c_debug/i2c_debug.ino --> produced two of these:

- **Floating address pin**: with the motion sensor's AD0 unconnected, it appeared and disappeared between scans, with 6% to 80% of reads failing.
- **Floating analog inputs**: unconnected ADC pins read **142 mV**. That was not a bus voltage, just an artefact of an input connected to nothing. It is a useful reminder that an analog reading from a floating pin looks like data.

One fault fits no row: a write-only display can hide a broken bus, because nothing is read back from it (the full story is in D5). The author's rule: **judge the bus by a device you read from.**
<!-- REFPRODUCT:END -->

> **Try it: Read the symptoms.** For each report, name the most likely cause and the one check you would make first.
> 1. **Predict.** Before reading the table again, guess each cause.
> 2. **Do.** (a) "The GPS module prints `ÿÿÿ` characters." (b) "The pressure sensor shows up in the scan at 0x76 on some boots and not others." (c) "My two sensors both answer at 0x68 and the readings make no sense." (d) "The sensor board works on the bench but gives drifting readings when powered from a separate battery pack."
> 3. **Explain.** Which of these could you catch in Wokwi, and which only on real hardware?

<details>
<summary>Answer</summary>

(a) Baud-rate mismatch: check both baud settings. (b) Floating address pin: check how the address pin is tied. (c) Address clash: check whether either device has an alternative address. (d) Missing common ground between the two supplies: check that a ground wire joins them. Wokwi could catch (a), since both baud rates are set in code you can see, and (c), since two parts with one address appear in the simulator's bus. (b) and (d) are electrical effects that Wokwi's digital model does not include.

</details>

---

# Putting It All Together

## Applying What You Have Learned

**1. Build your interface comparison table.** For each interface your parts could use, fill in pins, device count, speed, pull-ups, read-back and main failure mode, from your parts' datasheets rather than the typical values above.

**2. Justify each peripheral.** One row per peripheral: interface, the reason in terms of pins, data rate and sharing, and what to watch out for. Where a part offers only one interface, say so.

**3. Check your busiest connection.** Estimate its load at your chosen speed: bytes per second × bits per byte ÷ bus speed. Use 9 for I²C and 10 for UART. If the load is over about 50%, record your fix.

**4. Plan for failure.** For each interface, write how the firmware will detect a fault, linking back to your A2 failure table. For any write-only device, name the device on the same bus you will use to check the bus's health.

**Deliverable:** add the comparison table and per-peripheral justifications to your design pack as `B1-interfaces.md`.

## Self-Check

Open `B1-interfaces.md` and answer each item Y or N.

1. Every peripheral has an interface and a written reason. — Y/N
2. Every reason refers to at least one of: pins, data rate, device count, distance, or what the part offers. — Y/N
3. The total pin use fits within your MCU's free pins. — Y/N
4. Every I²C device has an address and a note of how it is set. — Y/N
5. No two devices on one bus share an address. — Y/N
6. The busiest connection has a load estimate at its chosen speed. — Y/N
7. Every interface has a detection method for faults. — Y/N
8. Every write-only device has a named read-back device on the same bus for health checks. — Y/N

---

## Check Your Understanding

**1.** A watch has two spare GPIO pins. Its display is on I²C and uses 70% of the bus through constant redraws. What is the best first step?

- A. Move the display to SPI.
- B. Redraw the display only when its content changes.
- C. Add a second I²C controller.
- D. Lower the bus speed to 100 kHz.

<details>
<summary>Answer</summary>

**B.** It removes most of the load with no pins or hardware. **A** needs 4 to 5 pins, and there are only 2. **C** is not available on a chip with a single I²C interface, such as the ESP32-C3. **D** makes every transfer four times longer, which makes the load worse.

</details>

**2.** Two SPI devices share SCLK, MOSI and MISO. Reading device A works alone, but returns garbage once device B is connected. B's chip-select pin is not connected to anything. What is the most likely cause?

- A. B's chip select floats low, so B drives MISO at the same time as A.
- B. SCLK has no pull-up resistor.
- C. A and B have the same address.
- D. A baud-rate mismatch between A and the microcontroller.

<details>
<summary>Answer</summary>

**A.** Any SPI device whose chip select is low drives the shared MISO line. A floating chip select lets B answer over A. **B**: SPI lines need no pull-ups. **C** and **D** are I²C and UART faults, not SPI ones.

</details>
**3.** An I²C bus carries a write-only display and a temperature sensor. Your firmware checks the bus once a minute. Which check can detect a broken bus?

- A. Confirm the last display write returned no error.
- B. Read the sensor's ID register and compare it with the datasheet value.
- C. Confirm the display still shows text.
- D. Count how many display writes were sent.

<details>
<summary>Answer</summary>

**B.** Only a read proves that data came back across the bus. **A** and **D** can pass on a broken bus: esp_watch's display accepted writes while showing corrupted output. **C** needs a person watching, and corrupted output can still look like text.

</details>
**4.** Before wiring a battery divider to an ADC pin, you print that pin's reading and see about 140 mV. What should you conclude?

- A. The pin is measuring a real voltage on the board.
- B. The pin is floating; the value is a false reading, not a measurement.
- C. The ADC is broken.
- D. The battery is almost flat.

<details>
<summary>Answer</summary>

**B.** An input connected to nothing reads whatever charge and noise are on it. esp_watch's floating ADC pins read 142 mV. **A** and **D** treat the number as data, but nothing is connected yet. **C** is unlikely: the ADC is behaving normally for a floating input.

</details>
**5.** A sensor offers both I²C and SPI. The product has plenty of spare pins, the sensor needs 20 kB per second, and the I²C bus already carries a display. Which choice is best supported?

- A. I²C, because it uses fewer wires.
- B. SPI, because pins are available, the data rate is high, and it keeps the load off the already busy I²C bus.
- C. UART, because it is simplest.
- D. Analog, because it needs only one pin.

<details>
<summary>Answer</summary>

**B.** 20 kB per second is 180,000 I²C clocks per second, nearly half of a 400 kHz bus by itself. With pins to spare, SPI takes that load away. **A** optimises the wrong constraint here. **C** is not offered by the sensor. **D** does not apply to a digital sensor.

</details>

---

## What Comes Next

In [B2 — Hardware Architecture](B2-hardware-architecture.md) you will turn your sensors and interfaces into a block diagram and an interface table, the drawing a schematic is built from.

---

## References

1. Solomon Systech. *SSD1306 datasheet*, hosted by Adafruit (4-wire SPI pins SCLK, SDIN, CS#, D/C#, RES#; SPI clock cycle time minimum 100 ns; "Under serial mode, only write operations are allowed"; I²C addresses 0111100/0111101). https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf
2. Analog Devices. *MAX30102 datasheet* (I²C interface; open-drain interrupt). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
3. Espressif Systems. *ESP32-C3 Series Datasheet* (connectivity interfaces: two UARTs, three SPI, one I²C; I²C standard mode 100 kbit/s and fast mode 400 kbit/s). https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
