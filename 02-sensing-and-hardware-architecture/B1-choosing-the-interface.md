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

The honest answer is "it depends", and this unit is about what it depends on. Part 1 taught you how I²C, SPI and UART work. This unit is about *choosing* between them for a real product: counting pins, estimating data rates, thinking about how many devices share a connection, and knowing how each choice fails. By the end you will be able to answer the display question for esp_watch, and write a justified choice for every peripheral in your own design.

### What You Will Be Able to Do After This Reading

- **Compare** I²C, SPI, UART, analog and pulse interfaces on pins, speed, device count, distance and failure modes.
- **Calculate** how long a transfer takes on each interface, and what that means for a shared bus.
- **Select** an interface for each peripheral, and **justify** it from your pin budget and data rates.
- **Diagnose** the common interface faults: wrong pull-ups, address clashes, baud mismatches and a missing common ground.

### What Part 1 Already Covered

Part 1's communication readings explained I²C addressing and scanning, SPI's separate chip-select lines, UART's point-to-point link and baud rate, and compared the three for a few scenarios. **What is new here** is making that choice under real constraints: a full pin budget, a shared bus with a measured load, and a written justification for every peripheral that someone else can check.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

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
esp_watch uses 7 of the XIAO's 11 pins. The 4 left are GPIO8 and GPIO9 (strapping pins, which must be high at reset) and D6 and D7 (the UART, useful for debugging). The display's four or five SPI lines would all have to come from those four pins. Moving the display off I²C frees nothing, because the two sensors still need the I²C pins.
<!-- REFPRODUCT:END -->

The budget cannot pay without using strapping pins for outputs that could hold them low at reset, or giving up the debug UART.

**Step 4: Is there a cheaper fix for the real problem?** The real problem was bus *time*, not bus speed. Redrawing the display only when something changes removes most of its bus use (B2 and D2 show how). That costs no pins and no hardware.

**Check.** SPI is faster, but esp_watch cannot afford the pins, and the problem it would solve has a free firmware fix. **Conclusion: keep the display on I²C and redraw on change.** For a product with a bigger microcontroller, or animations that genuinely need 30 frames a second, the answer could reasonably be the opposite. Writing down the reasoning, not just the result, is what lets someone make that call later.

> **Try it: Would SPI win here?** A different product uses an ESP32 module with 10 spare pins and a 128 × 64 display that must animate at 30 frames a second, while two sensors each need 1,000 bytes a second.
> 1. **Predict.** I²C or SPI for the display?
> 2. **Do.** Work out the I²C bus use at 400 kHz for 30 full frames a second (use 25 ms per frame), plus the sensors (9 clocks per byte). Then check whether SPI fits the pin budget.
> 3. **Explain.** Which constraint decided it this time: pins, bus time, or something else?

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
| MAX30102 heart rate | I²C (0x57) + open-drain interrupt | Only I²C is offered [2]; the interrupt says when samples are ready, so the firmware does not have to poll | Module's pull-up voltage (the green module's 1.8 V problem) |
| MPU-6050 motion | I²C (0x68) + interrupt | I²C is what the module exposes; data rate is tiny; interrupt allows shake-to-wake | AD0 must be tied to a defined level |
| SSD1306 display | I²C (0x3C) | Pin budget; redraw-on-change solves the bus-time problem | Writes cannot confirm the bus works |
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
esp_watch's bench testing produced three of these, all measured with the author's `i2c_debug` sketch:

- **Floating address pin**: with the motion sensor's AD0 unconnected, it appeared and disappeared between scans, with 6% to 80% of reads failing.
- **Too many pull-ups**: three modules' pull-ups in parallel, about 1.5 kΩ, made 400 kHz unreliable.
- **Floating analog inputs**: unconnected ADC pins read **142 mV**. That was not a bus voltage, just an artefact of an input connected to nothing. It is a useful reminder that an analog reading from a floating pin looks like data.

And one fault that fits no row of the table: a write-only device hid a broken bus. The display kept accepting data while the bus was clamped to 1.82 V, and showed corrupted output without any error, because nothing is ever read back from it. The author's rule: **judge the bus by a device you read from.**
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

**3. Check your busiest connection.** Estimate its load at your chosen speed: bytes per second × about 10 bits per byte ÷ bus speed. If it is over about 50%, record your fix.

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

**2.** A GPS module sends location data over UART. The serial output shows random characters. What is the most likely cause?

- A. Missing pull-up resistors
- B. A baud-rate mismatch between the module and the microcontroller
- C. An address clash
- D. The GPS has no signal

<details>
<summary>Answer</summary>

**B.** Characters arrive but decode wrongly, which is the signature of the two sides timing their bits differently. **A** applies to I²C, not UART. **C** has no meaning on a point-to-point UART. **D** would produce valid messages reporting no position, not random characters.

</details>

**3.** Why is a write-only device a poor choice for checking whether a shared bus is healthy?

- A. Write-only devices are slower.
- B. Writes succeed or fail silently from the firmware's point of view, so a broken bus can look healthy; only a device you read from can confirm the data got through.
- C. Write-only devices use more power.
- D. They cannot be on I²C.

<details>
<summary>Answer</summary>

**B.** The reference watch's display showed corrupted output on a broken bus while the firmware saw no error, because nothing was ever read back. **A** and **C** are not the issue. **D** is false: the SSD1306 is write-only in SPI mode, and on I²C the firmware still only ever writes to it.

</details>

**4.** An unconnected ADC pin reads about 140 mV. What should you conclude?

- A. The pin is measuring a real voltage on the board.
- B. The pin is floating; the value is an artefact, not a measurement.
- C. The ADC is broken.
- D. The bus is running at 140 mV.

<details>
<summary>Answer</summary>

**B.** An input connected to nothing reads whatever charge and noise happen to be on it. esp_watch's floating ADC pins read 142 mV. **A** mistakes an artefact for data. **C** is unlikely; the ADC is doing what it should with a floating input. **D** confuses an analog pin with the I²C bus.

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

## What You Can Now Do, and What Comes Next

- Compare interfaces on pins, speed, sharing, distance and failure modes.
- Decide an interface per peripheral from your pin budget and data rates, and write down why.
- Recognise the common interface faults from their symptoms.
- Pick a read-back device to judge a bus's health.

The idea to carry forward: **on a small board, pins are the scarcest resource, and a firmware fix is cheaper than a wiring change.** Check the pin budget before you reach for a faster interface.

In [B2 — Hardware Architecture](B2-hardware-architecture.md) you will turn your sensors and interfaces into a block diagram and an interface table, the drawing a schematic is built from.

---

## References

1. Solomon Systech. *SSD1306 datasheet*, hosted by Adafruit (4-wire SPI pins SCLK, SDIN, CS#, D/C#, RES#; SPI clock cycle time minimum 100 ns; "Under serial mode, only write operations are allowed"; I²C addresses 0111100/0111101). https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf
2. Analog Devices. *MAX30102 datasheet* (I²C interface; open-drain interrupt). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
3. Espressif Systems. *ESP32-C3 Series Datasheet* (connectivity interfaces: two UARTs, three SPI, one I²C; I²C standard mode 100 kbit/s and fast mode 400 kbit/s). https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
