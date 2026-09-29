# B5 — Virtual Prototyping
## Testing the Circuit Before It Exists

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 2 — Sensing and Hardware Architecture
**Time:** ~1.5 hours · **You will produce:** a working Wokwi project link and a Falstad circuit link

---

### Your Bench Is a Browser

In Part 1 you checked a circuit by building it on a breadboard. Here nothing gets built, so you check your B3 calculations in a **simulator** instead: change a resistor and watch the edge slow down, run your firmware and read the bus traffic it produces. (esp_watch itself was tested on a real breadboard before its schematic was drawn; a simulator is the next best thing when you don't have the parts yet.)

Simulators have blind spots, and esp_watch's worst breadboard bug sits in one. This unit uses two simulators, each for what it does well, and shows where each one stops telling the truth.

### What You Will Be Able to Do After This Reading

- **Simulate** pull-up rise times and bus voltage levels in Falstad, and compare them with your B3 calculations.
- **Build** a Wokwi project that runs real firmware against your pin map, including a mock for a sensor the simulator does not have.
- **Read** an I²C trace: start, address, acknowledge, data and stop.
- **Diagnose** a failed transaction from its trace.
- **Explain** what each simulator cannot show you, and which real measurement fills the gap.

---

# Analog Behaviour in Falstad

## Two Simulators, Two Questions

| Question | Tool | Why |
|---|---|---|
| Do the voltages and edges look right? | **Falstad** Circuit Simulator [1] | Shows voltages and currents continuously; you can see an edge rise |
| Does my firmware work with my pin map and parts? | **Wokwi** [2] | Runs real Arduino code on a simulated ESP32-C3 with simulated sensors and displays |

Falstad treats every wire as a voltage that changes over time. Wokwi treats most signals as simply HIGH or LOW. (For more rigorous analog work, engineers use **LTspice**; Falstad is enough for this course.)

## Pull-up Rise Time

In B3 you calculated the range of legal pull-up values. Now watch why the upper limit exists.

When no device pulls an I²C line low, the pull-up resistor charges the bus's capacitance back up to 3.3 V. That takes time, because a resistor charging a capacitor produces a curve, not a step. The I²C specification measures the **rise time** from 30% to 70% of the supply voltage, and for a resistor charging a capacitor that works out to 0.8473 × R × C [3].

### Worked Example: Three Pull-up Values

**Assumption:** bus capacitance 50 pF, as in B3.

```text
t_r = 0.8473 × R × C

4.7 kΩ:   0.8473 × 4,700  × 50 pF = 199 ns
10 kΩ:    0.8473 × 10,000 × 50 pF = 424 ns
1.57 kΩ:  0.8473 × 1,570  × 50 pF =  67 ns   (three 4.7 kΩ pairs in parallel)
```

The fast-mode (400 kHz) limit is 300 ns, and standard mode (100 kHz) allows 1,000 ns [3].

**Check.** 4.7 kΩ passes at 400 kHz with margin. 10 kΩ breaks the 300 ns limit at 400 kHz, though the line still reaches most of the way up before the next bit, so it may *seem* to work on the bench, with less margin for noise. It passes easily at 100 kHz. 1.57 kΩ gives very fast edges, but, as B3 showed, it asks every device to sink more current. The simulator will show you all three curves side by side.

> **Try it: Watch the edge rise.** Open Falstad in your browser [1]. Build three identical circuits side by side. In each, an N-channel MOSFET connects the line to ground and acts as the open-drain device, with its gate driven by a 0–3.3 V square-wave source. Add a pull-up resistor from the line to a 3.3 V source, and a 50 pF capacitor from the line to ground. Use 4.7 kΩ, 10 kΩ and 1.57 kΩ for the three pull-ups. Add a scope to each line.
> 1. **Predict.** Which of the three will look most like a clean square wave at 400 kHz?
> 2. **Do.** Set the source to 400 kHz. Compare the rising edges on the scopes. Then change it to 100 kHz.
> 3. **Explain.** On each scope, estimate the time from 30% to 70% of 3.3 V (0.99 V to 2.31 V). Which pull-ups break the 300 ns limit? Do your times match the numbers above?
>
> **Extra challenge:** Double the capacitance to 100 pF. Which pull-ups still pass at 400 kHz?

<!-- MEDIA
type: screenshot
id: B5-01
caption: Falstad: rising edges with 4.7 kΩ, 10 kΩ and 1.57 kΩ pull-ups on a 50 pF bus at 400 kHz
brief: Falstad Circuit Simulator in a browser, full window. Three identical open-drain
  pull-up circuits side by side, each with its pull-up value labelled (4.7k, 10k, 1.57k)
  and a 50 pF capacitor to ground. Below, three scope traces stacked, same time scale,
  showing one clock period at 400 kHz. The 1.57 kΩ trace has near-square edges, the
  4.7 kΩ trace has visibly rounded but complete rises, and the 10 kΩ trace is the slowest,
  clearly rounded and only just reaching the top before it falls again. Add a horizontal marker at 70% of 3.3 V (2.31 V)
  on each scope, if Falstad allows, or annotate it afterwards.
-->

## When the Bus Sits at the Wrong Voltage

<!-- REFPRODUCT:START -->
On esp_watch's breadboard prototype, the green heart-rate module tied its I²C lines to its own 1.8 V rail. With it on the shared bus, the idle bus voltage was measured at **1.82 V**.
<!-- REFPRODUCT:END -->

Why does 1.82 V break everything? Look at what the ESP32-C3 accepts as a logic level. Its datasheet sets the **input-high threshold** at 0.75 × VDD and the **input-low threshold** at 0.25 × VDD [4]:

```text
                3.3 V ┬
                      │  HIGH: guaranteed read as 1
  0.75 × 3.3 = 2.475 V ┼─────────────────────────────
                      │
                      │  UNDEFINED: may read as 0 or 1
       measured 1.82 V ┼── ◄ esp_watch bus with the green module
                      │
  0.25 × 3.3 = 0.825 V ┼─────────────────────────────
                      │  LOW: guaranteed read as 0
                  0 V ┴
```

The idle bus sat in the **undefined** band. Sometimes a receiver read an idle line as HIGH, sometimes as LOW. That is exactly the kind of fault that produces 80% failures on one device and occasional success on another, rather than a clean "not working".

> **Teaching model.** The Try-it below treats the green module as a second pull-up to 1.8 V, fighting the 3.3 V pull-up. The real module may also clamp the line through protection diodes. The model is enough to show why the bus ends up between the two rails.

> **Try it: Two pull-ups, two rails.** In Falstad, draw one line with a 4.7 kΩ pull-up to 3.3 V and a second resistor, R_mod, pulling the same line to a 1.8 V source. Add a voltmeter on the line.
> 1. **Predict.** With R_mod = 4.7 kΩ, where will the line sit?
> 2. **Do.** Try R_mod = 4.7 kΩ, 2.2 kΩ and 1 kΩ, and read the voltage each time.
> 3. **Explain.** For which values does the line fall below 2.475 V, into the undefined band?
>
> **Extra challenge:** Show by calculation that the line drops below 2.475 V whenever R_mod is less than about 3.85 kΩ.

The fixes for a mismatched module are, in order of preference: choose a module whose bus sits at your voltage (esp_watch's black module), change the module's pull-up voltage if it has a jumper for it, or add a **bidirectional level shifter** between the two voltage domains.

## A Battery Divider's Settling Time

<!-- REFPRODUCT:START -->
esp_watch doesn't measure its battery: the XIAO board handles charging and protection, and the watch uses a protected LiPo cell. Many battery products do show a battery level, though, and they measure it with a divider.
<!-- REFPRODUCT:END -->

**Example values:** a 1 MΩ / 1 MΩ divider halves the cell voltage so the ADC can read it, and a 100 nF capacitor at the ADC pin gives the ADC a steady voltage to sample. The capacitor has a side effect you can see in Falstad: the voltage at the pin cannot change instantly. The capacitor charges through the divider's effective resistance of 500 kΩ (the two resistors in parallel):

```text
Time constant  τ = R × C = 500 kΩ × 100 nF = 0.05 s = 50 ms
Settled (about 99%) after 5τ = 250 ms
```

So a reading taken in the first 250 ms after power-up will be low. The firmware should wait before trusting the first battery reading. In Falstad, build the divider and capacitor, switch the supply on, and watch the pin voltage curve up.

## Supply Dips Under Load

A battery is not a perfect voltage source. It has **internal resistance**, so its voltage drops when current is drawn. A regulator needs its input to stay a little above its output, the **dropout voltage**, to keep regulating.

**Example values:** a small cell with 0.5 Ω internal resistance, a radio burst drawing a 300 mA peak, and a regulator needing 0.2 V of dropout.

```text
Voltage lost inside the cell: 300 mA × 0.5 Ω = 0.15 V
Input needed to hold 3.3 V:   3.3 V + 0.2 V  = 3.5 V
Cell voltage needed at rest:  3.5 V + 0.15 V = 3.65 V
```

Below about 3.65 V at rest, a radio burst pulls the regulator's input too low and the 3.3 V rail dips. If it dips far enough, the **brownout detector** resets the microcontroller (D5 covers this). The lower the cell, the more a current burst hurts.

<!-- FACT:VERIFY esp_watch — the XIAO ESP32-C3 regulator's dropout voltage and the fitted cell's internal resistance are not recorded; the numbers above are illustrative only -->

---

# Firmware and Parts in Wokwi

## Building the Virtual Watch

Wokwi simulates the ESP32-C3, the SSD1306 display, the MPU-6050 motion sensor and pushbuttons [5], including a XIAO ESP32-C3 board [2]. It runs real Arduino code, so the sketch you test here is the sketch you would flash.

A Wokwi project has three files:

- `sketch.ino`, the firmware
- `diagram.json`, the parts and wires
- `libraries.txt`, the Arduino libraries to install

The complete files for this unit are in [`assets/code/B5-wokwi-watch-sim/`](../assets/code/B5-wokwi-watch-sim/). To use them, create a new ESP32 project on wokwi.com, then replace the contents of each file with the provided version. If Wokwi reports an unknown pin name, hover over that pin in the diagram to see its exact name [6].

The wiring matches esp_watch's pin map: one shared I²C bus and two buttons, with no interrupt or battery pins.

```text
XIAO ESP32-C3 (Wokwi)            Parts
  D4 (GPIO6) SDA ───────────────  SSD1306 SDA, MPU-6050 SDA, logic analyser D0
  D5 (GPIO7) SCL ───────────────  SSD1306 SCL, MPU-6050 SCL, logic analyser D1
                                  MPU-6050 AD0 tied to GND → 0x68
  D10 (GPIO10)   ◄──────────────  "next" button to GND
  D1  (GPIO3)    ◄──────────────  "previous" button to GND
  3V3 / GND      ───────────────  all parts
```

## The Mock Sensor

Wokwi has no MAX30102 [5]. Rather than leave the heart-rate code untested, the sketch uses a **mock**: a small class with the same job as the real driver, returning made-up but realistic values.

```cpp
// Wokwi has no MAX30102. This mock stands in for it, returning a heart
// rate that drifts slowly between about 66 and 78 bpm. The rest of the
// program cannot tell the difference, so it can all be tested now.
class MockHeartRate {
public:
  bool begin() { return true; }
  int readBpm() {
    float t = millis() / 1000.0f;
    return 72 + (int)(6.0f * sinf(t / 10.0f));
  }
};
MockHeartRate heart;
```

The rest of the program only ever calls `heart.begin()` and `heart.readBpm()`. When the real sensor arrives, a real class with the same two functions replaces the mock, and nothing else changes. D0 builds on this idea.

The full sketch is about 140 lines and compiles for the XIAO ESP32-C3. Its main jobs:

- scan the I²C bus at start-up and print every address found
- show two screens (motion and heart rate), switched by the two buttons
- time every screen update and print it

Two lines are worth noticing now. `display.setTextWrap(false)` is there because esp_watch's own firmware showed garbled text during screen animations until wrapping was turned off. `I2C_CLOCK_HZ` sets the bus speed, so you can compare against the timing measured on the reference watch. It is passed to the display library as well, because that library otherwise switches the bus back to 100 kHz after every frame.

<!-- MEDIA
type: screenshot
id: B5-02
caption: The virtual watch running in Wokwi, with the serial monitor showing the bus scan and frame times
brief: Wokwi in a browser, the B5 project running. Left: diagram with the XIAO ESP32-C3,
  SSD1306 display (showing the "HEART RATE (mock)" screen with a two-digit number in
  large text), MPU-6050, two pushbuttons labelled next and previous, and the logic
  analyser, all wired. Bottom: the serial monitor showing "I2C scan:", "found
  device at 0x3C", "found device at 0x68", followed by several "screen 1 sent in ... us"
  lines. The simulation timer visible and running. No personal account details visible.
-->

> **Try it: Compare with the real watch.** Run the Wokwi project.
> 1. **Predict.** Which addresses will the bus scan find? How long will one screen update take at 400 kHz, based on B2?
> 2. **Do.** Read the scan and the "sent in" times in the serial monitor. Then change `I2C_CLOCK_HZ` to 100000 and run again.
> 3. **Explain.** The scan should find 0x3C and 0x68, but not 0x57, because the heart-rate sensor is a mock with no bus address. Compare your update times with B2's prediction (23 ms and 92 ms) and with the reference watch's measurements (about 25 ms and 90 ms). If the simulator's times differ, what does that tell you about what Wokwi models?
>
> **Extra challenge:** Change the redraw so the display is sent only when the heart-rate number actually changes. How many updates per minute does that save?

---

# Reading the Bus

## What an I²C Transaction Looks Like

The logic analyser in the Wokwi project records SDA and SCL while the simulation runs. When you stop the simulation, it saves a `.vcd` file [7]. Open it in **PulseView**, a free logic-analyser program [8], using *Import Value Change Dump data*, with a downsampling factor of about 50 for I²C [9]. Then add PulseView's I²C decoder to label each byte.

Here is one complete read of the motion sensor, annotated. The library's `imu.getEvent()` reads **14 bytes** in one go, starting at register 0x3B: six of acceleration, two of temperature and six of rotation.

```text
     START  address 0x68 + W   ACK  register 0x3B   ACK
SDA  ‾‾\_ [1101000][0]         [0]  [00111011]      [0]
SCL  ‾‾‾\_/‾\_/‾\_ ...                                 

     REPEATED START  address 0x68 + R   ACK  data × 14 (each followed by ACK, last by NACK)  STOP
SDA  ‾\_             [1101000][1]       [0]  [xxxxxxxx][0] ... [xxxxxxxx][1]                _/‾
```

Reading it left to right:

1. **START**: SDA falls while SCL is high. Every device on the bus starts listening.
2. **Address + write bit**: 0x68 in seven bits, then 0 meaning "I want to write".
3. **ACK**: the motion sensor pulls SDA low for one clock: "that's me".
4. **Register number**: 0x3B, the first acceleration register.
5. **Repeated START**, then the address again with the read bit (1).
6. **Fourteen data bytes** from the sensor. The controller acknowledges each one, except the last, which gets a **NACK** meaning "that's enough".
7. **STOP**: SDA rises while SCL is high.

### Worked Example: How Long Does One Sensor Read Take?

Count the bytes: address (1), register (1), address again (1), data (14) = 17 bytes.

```text
17 bytes × 9 clocks = 153 clocks
At 400 kHz: 153 ÷ 400,000 ≈ 0.4 ms
```

**Check.** Compare with a full display update: about 25 ms. One screen update takes as long as about 65 sensor reads. The trace confirms B2's conclusion from the other direction: on a shared bus, the display is the heavy user.

<!-- MEDIA
type: screenshot
id: B5-03
caption: PulseView decoding an I²C read of the MPU-6050, captured from the Wokwi logic analyser
brief: PulseView desktop application, light theme. Two channels, SDA and SCL, imported
  from wokwi-logic.vcd. An I2C protocol decoder added and stacked below them, showing
  coloured annotation boxes: "Start", "Address write: 68", "ACK", "Data write: 3B",
  "ACK", "Start repeat", "Address read: 68", "ACK", fourteen "Data read" boxes, "NACK", "Stop".
  Zoom so one complete transaction fills the width. Label the time scale.
-->

## When the Trace Shows a Failure

Wokwi's bus has no electrical faults, so your traces fail only for logic errors such as a wrong address. Real buses fail in three common patterns:

| What the trace shows | What it means | Likely cause |
|---|---|---|
| Address sent, then **NACK** instead of ACK | No device answered at that address | Wrong address, device unpowered, or an address pin left floating |
| Lines never return fully high between bytes | The idle level is too low | A module pulling the bus to another voltage, or too little pull-up |
| Rising edges slow and rounded, bits misread | Rise time too long | Pull-up too large or bus capacitance too high for the speed |

<!-- REFPRODUCT:START -->
esp_watch hit the first two on the bench, found with the author's `i2c_debug` sketch: a floating AD0 pin (see B1) and the 1.82 V bus above. Neither would appear in Wokwi, whose bus has no voltage levels, no floating pins and no capacitance.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/i2c-debug-output.png -->
![Output of the i2c_debug sketch on the esp_watch breadboard: bus scan, voltage check and read-failure counts per device](../reference-files/images/i2c-debug-output.png)

## What Each Simulator Cannot Tell You

| | Falstad | Wokwi |
|---|---|---|
| Shows voltage levels and edge shapes | Yes | No: signals are HIGH or LOW |
| Runs your firmware | No | Yes |
| Models your exact modules | Only if you draw their circuits | Only parts in its library; no MAX30102 |
| Shows a floating address pin | Only if you model it | No |
| Shows bus timing | As analog waveforms | Protocol timing, idealised |

esp_watch's two worst breadboard faults, a floating address pin and a module on the wrong voltage, fall *between* the two tools. Falstad shows the voltage fault only if you already suspect it and draw it; Wokwi shows neither. So next to each simulation result, write down **what the simulation did not include**, so the funded build knows what to check first.

---

# Putting It All Together

## Applying What You Have Learned

**1. Simulate your pull-ups in Falstad.** Build your bus with your chosen pull-up and estimated capacitance. Check the rise time at your bus speed. Save the circuit as a link.

**2. Check your voltage levels.** For every module on your bus, model its pull-up voltage in Falstad and confirm the idle level sits above the microcontroller's input-high threshold.

**3. Build your Wokwi project.** Start from the provided files and adapt the pin map, parts and addresses to your own design. Add a mock for every part Wokwi lacks. Confirm the bus scan finds exactly the addresses in your interface table.

**4. Capture and decode one transaction.** Record SDA and SCL, open the file in PulseView, decode it, and annotate one complete read.

**5. Write the gaps.** List what your simulations did *not* include: modules not modelled, voltages not checked, parts mocked.

**Deliverable:** add your Wokwi project link, your Falstad link, one annotated trace, and your list of gaps to your design pack as `B5-virtual-prototype.md`.

## Self-Check

Open `B5-virtual-prototype.md` and answer each item Y or N.

1. The Falstad link opens a circuit with your actual pull-up value and a stated bus capacitance. — Y/N
2. The simulated rise time is recorded and compared with the limit for your bus speed. — Y/N
3. Every module's bus voltage has been checked against the microcontroller's input-high threshold. — Y/N
4. The Wokwi link opens a project that runs without errors. — Y/N
5. The Wokwi pin map matches your B3 pin allocation exactly. — Y/N
6. The bus scan output is recorded and matches your interface table. — Y/N
7. Every part the simulator lacks has a mock with the same functions as the real driver. — Y/N
8. One decoded transaction is annotated from START to STOP. — Y/N
9. The list of gaps names every module, voltage and part the simulations did not model. — Y/N

---

## Check Your Understanding

**1.** A bus with 80 pF of capacitance runs at 400 kHz. Using t_r = 0.8473 × R × C and a limit of 300 ns, which is the largest pull-up that passes?

- A. 10 kΩ
- B. 4.7 kΩ
- C. 3.9 kΩ
- D. 2.2 kΩ

<details>
<summary>Answer</summary>

**C.** R_max = 300 ns ÷ (0.8473 × 80 pF) ≈ 4,426 Ω, so 3.9 kΩ passes with a little margin and is the largest option that does. **B**, 4.7 kΩ, gives 0.8473 × 4,700 × 80 pF ≈ 319 ns, just over the limit. **A** gives about 678 ns, more than double the limit. **D** passes easily, but it is not the largest that passes, and it asks devices to sink more current than they need to.

</details>

**2.** An ESP32-C3 at 3.3 V reads an I²C line that idles at 1.9 V. What will happen?

- A. The line reads reliably as HIGH.
- B. The line reads reliably as LOW.
- C. The level is in the undefined band between 0.825 V and 2.475 V, so reads are unreliable.
- D. The ESP32-C3 is damaged.

<details>
<summary>Answer</summary>

**C.** 1.9 V is below the input-high threshold (0.75 × 3.3 = 2.475 V) and above the input-low threshold (0.25 × 3.3 = 0.825 V), so neither reading is guaranteed. **A** and **B** each assume a guarantee that does not exist in that band. **D** is wrong; 1.9 V is well within the pin's allowed range.

</details>

**3.** A decoded trace shows `START, Address write: 68, NACK, STOP`. What is the most likely explanation?

- A. The register number was wrong.
- B. No device acknowledged address 0x68: it is missing, unpowered, or its address pin is not set as expected.
- C. The data was read successfully.
- D. The pull-ups are too small.

<details>
<summary>Answer</summary>

**B.** A NACK straight after the address means nobody answered to that address. On the reference watch, a floating AD0 pin produced exactly this, intermittently. **A** cannot be the cause, because the register number is never sent after a NACK. **C** is wrong, since no data bytes appear. **D** makes it harder for devices to pull the line low, so bits get misread; it does not cause a clean NACK straight after the address.

</details>

**4.** Which reference-watch fault could a Wokwi simulation have revealed?

- A. The green module clamping the bus to 1.82 V
- B. A floating AD0 pin making the sensor come and go
- C. Garbled text caused by text wrapping during screen animations
- D. Three modules' pull-ups in parallel

<details>
<summary>Answer</summary>

**C.** Text wrapping is firmware behaviour, and Wokwi runs the firmware and draws the display, so the garbled text would appear on the simulated screen. **A**, **B** and **D** are all analog or electrical effects: voltage levels, floating inputs and resistance. Wokwi's digital model does not include any of them.

</details>

**5.** A product measures its battery through a 1 MΩ / 1 MΩ divider with a 100 nF capacitor. Why should its firmware wait before trusting the first battery reading after power-up?

- A. The ADC needs to warm up.
- B. The capacitor charges through about 500 kΩ with a time constant of 50 ms, so the pin voltage takes around 250 ms to settle.
- C. The battery voltage changes at power-up.
- D. Readings are always wrong for the first second.

<details>
<summary>Answer</summary>

**B.** τ = 500 kΩ × 100 nF = 50 ms, and about 5τ is needed to settle, so early readings are low. **A** is not the mechanism here. **C** may be slightly true under load, but it is not why the reading is low. **D** is an arbitrary rule with no reasoning behind it.

</details>

---

## What Comes Next

"Passed in Wokwi" means the logic is right, not that the voltages are: a simulation result is only as complete as its list of gaps.

In [C0 — Form Factor and Concept](../03-form-schematic-and-pcb/C0-form-factor-and-concept.md) you will decide the product's shape and which face each part sits on, before the circuit becomes a board.

---

## References

1. Paul Falstad. *Circuit Simulator Applet*. https://www.falstad.com/circuit/
2. Wokwi. *ESP32 Simulation* (supported boards including XIAO ESP32-C3; I²C "Master only"). https://docs.wokwi.com/guides/esp32
3. NXP Semiconductors. *UM10204: I²C-bus specification and user manual* (rise-time limits and the R_p(max) = t_r / (0.8473 × C_b) relation). https://www.nxp.com/docs/en/user-guide/UM10204.pdf
4. Espressif Systems. *ESP32-C3 Series Datasheet* (DC characteristics: V_IH min 0.75 × VDD, V_IL max 0.25 × VDD). https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf
5. Wokwi. *Supported Hardware* (MPU6050, SSD1306, pushbutton; no MAX30102). https://docs.wokwi.com/getting-started/supported-hardware
6. Wokwi. *diagram.json File Format* (connection syntax `partId:pinName`; hover over a pin to see its name). https://docs.wokwi.com/diagram-format
7. Wokwi. *wokwi-logic-analyzer Reference* (8 channels, VCD recording saved when the simulation stops). https://docs.wokwi.com/parts/wokwi-logic-analyzer
8. sigrok. *PulseView* (logic analyser, oscilloscope and MSO GUI for sigrok). https://sigrok.org/wiki/PulseView
9. Wokwi. *Logic Analyzer Guide* (importing VCD into PulseView; downsampling factor 50 for I²C). https://docs.wokwi.com/guides/logic-analyzer
