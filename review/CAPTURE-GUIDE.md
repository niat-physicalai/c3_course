# Capture guide: how to make the remaining screenshots

Written 2026-10-07 in answer to the questions in the "reference" column of `ASSETS-TODO.md`. Each section says **what the image is for**, **what to run**, and **what to capture**. Save each file as `assets/<area>/<ID>.png` (or `.gif`) and put the path in the reference column; Claude then embeds it.

All code lives in this repo under `assets/code/`. Wokwi needs no account for a quick run: open https://wokwi.com, start a new **ESP32-C3** project, then replace its files with the ones named below.

---

## Section 2 items

### B4-02 — Parametric search on LCSC

**What it is for.** B4 teaches students to search a distributor *by specification* instead of by name. The screenshot shows the filter panel doing that work.

**Steps.**
1. Open https://www.lcsc.com and search `MAX30102`.
2. On the results page, use the left filter panel: tick **In Stock**, and tick the manufacturer (Analog Devices / Maxim).
3. Capture the full browser window with the filter panel, the result list, the stock column and the price-break column (1+, 10+, …) all visible. Make sure you are logged out or the account name is hidden.

### B5-01 — Falstad: pull-up resistor vs rise time

**What it is for.** B5 explains that a bigger pull-up resistor makes the I²C line rise more slowly. One picture of three traces shows it at once.

**Steps.**
1. Open https://www.falstad.com/circuit/circuitjs.html. Choose **File → New Blank Circuit**.
2. Build one stage: a 3.3 V source (**Draw → Inputs and Sources → Add DC Voltage Source**) → a resistor → a node → a 50 pF capacitor to ground. At the node, add a switch to ground (**Draw → Passive Components → Add Switch**). The switch stands in for the chip pulling the line low.
3. Copy the stage twice. Set the three resistors to **1.57k**, **4.7k** and **10k** (double-click a resistor to edit it). Set every capacitor to **50p**.
4. Right-click each capacitor's top node → **View in Scope**. Three scopes appear at the bottom.
5. Set the simulation speed low and click each switch open and closed a few times, so each scope shows a rise. Pause and capture the whole window.
6. Simpler alternative if this takes long: capture only one stage, and change the resistor between three captures; Claude will combine them.

### B5-02 — The virtual watch running in Wokwi

**Code.** `assets/code/B5-wokwi-watch-sim/` — copy `sketch.ino` and `diagram.json` into the Wokwi project, and add the libraries listed in `libraries.txt` (Wokwi's **Library Manager** tab, the `+` button).

**Steps.** Press the green play button. Wait for the display to show a screen, then press the "next" button once.

**Capture.** The whole browser window: the wired parts on the left, the display showing a screen, and the serial monitor at the bottom with the `I2C scan:` lines (`found device at 0x3C`, `0x68`) and a few `screen … sent in … us` lines.

### B5-03 — PulseView decoding an I²C read

**What it is for.** Students cannot own a logic analyser, so this shows what one sees on the I²C bus.

**Steps.**
1. Run the B5 project above for about 2 seconds, then stop it. The diagram already has a logic analyser on SDA and SCL. When the simulation stops, Wokwi downloads `wokwi-logic.vcd`.
2. Install PulseView (free, https://sigrok.org/wiki/Downloads).
3. In PulseView: **Open → Import Value Change Dump data**, choose the `.vcd` file. Two channels appear.
4. Click **Add protocol decoder** (the yellow-green icon), choose **I²C**, and set SCL and SDA to the matching channels.
5. Zoom until one whole transaction (Start … Stop) fills the width. Capture the window.

### C0-01 — Concept sketch

**What it is.** A rough hand drawing of the finished product, done **before** the PCB: what goes where, and why.

**"Constraint labelled" means** writing on the sketch the reason each thing is where it is. For esp_watch, for example:
- "display faces up"
- "heart-rate sensor on the skin side"
- "USB-C on the left, away from the skin"
- "buttons on the right edge"
- "battery stands on end behind the display"
- "about 18 mm thick in total"

**Steps.** On plain paper, draw a top view and a side view of the watch, roughly to scale with a ruler, then add those labels with arrows. Photograph it flat, in good light.

### D1-01 — State diagram in Mermaid

**Code.** Paste this into https://mermaid.live (left pane), and capture the split view:

```text
stateDiagram-v2
    [*] --> Boot
    Boot --> Awake : done
    Awake --> Measuring : request HR
    Measuring --> Awake : result / abort
    Awake --> Asleep : 30 s no input
    Asleep --> Awake : button
```

### D1-02 — The state machine running

**What it is.** Not esp_watch's own code. It is the small teaching sketch that turns D1's diagram into code; the screenshot proves each arrow in the diagram happens.

**Code.** `assets/code/D1-state-machine.ino`, pasted into a new Wokwi ESP32-C3 project (no parts needed).

**Steps.** Start it. In the serial monitor input box, type `h` (Enter), then `r` (Enter). Wait 30 seconds without typing. Then type `b` (Enter).

**Capture.** The serial output showing `BOOT -> AWAKE`, `AWAKE -> MEASURING`, `MEASURING -> AWAKE`, `AWAKE -> ASLEEP` and `ASLEEP -> AWAKE`, with their entry and exit lines.

### D2-01 — Non-blocking watch in Wokwi

**Code.** `assets/code/D2-nonblocking-watch/` (`sketch.ino`, `diagram.json`, `libraries.txt`), set up as in B5-02.

**Steps.** Start it. Click the MPU-6050 in the diagram and move its acceleration sliders up and down a few times, to fake steps.

**Capture.** The diagram with the display and the slider pop-up, plus the serial monitor showing a few `new worst loop time: … us` lines.

### D3-01 and D3-02 — Streaming data to a live plot

**Code.** `assets/code/D3-serial-stream/sketch.ino` (on the device) and `assets/code/D3-plot-serial.py` (on the laptop).

**Easiest route (real XIAO, no Wokwi):**
1. Flash `D3-serial-stream/sketch.ino` to the XIAO with the Arduino IDE or PlatformIO. Close the serial monitor.
2. Install Python packages once: `pip install pyserial matplotlib`.
3. Run `python3 D3-plot-serial.py /dev/ttyACM0` (Linux; on Windows use the COM port, e.g. `COM5`).
4. Let it run about 10 seconds. Capture the plot window (**D3-01**) with the terminal beside it showing the command.

**D3-02 (Wokwi for VS Code route).** Only needed if you want to show the simulator route. Install the **Wokwi Simulator** extension in VS Code, create `wokwi.toml` in the sketch folder with `rfc2217ServerPort = 4000`, start the simulator, then run `python3 D3-plot-serial.py rfc2217://localhost:4000`. Capture VS Code with the simulator tab, `wokwi.toml` and the terminal. If you skip this route, tell Claude and the D3-02 slot will be removed.

### D4-01 — Dashboard

**Code.** `assets/code/D4-connected-watch/` in Wokwi (it uses WiFi `Wokwi-GUEST` and the public broker `test.mosquitto.org`).

**Steps.** Start the simulation and wait for `# MQTT: online` in the serial monitor. Point any MQTT dashboard at `test.mosquitto.org`, port 1883, and subscribe to `c3course/#` (the watch publishes on `c3course/<device id>/data` and `/status`): the Part 1 dashboard platform, or the free **MQTT Explorer** app. Stop the simulation for a minute and restart it, so the chart shows a gap.

**Capture.** A tile with the step count, the online/offline status, and a chart with the gap. D4-02 (MQTT Explorer) is postponed by the author until the v2 firmware.

### D5-01 — Crash report decoded

**Not a compiler error.** It is a **runtime crash** on the real XIAO, and PlatformIO decoding it into a file name and line number.

**Code.** In a PlatformIO project for the XIAO ESP32-C3, add to `platformio.ini`:

```ini
monitor_filters = esp32_exception_decoder
build_type = debug
```

and use this `src/main.cpp`:

```cpp
#include <Arduino.h>

struct Sensor { int value; };
Sensor *sensor = nullptr;          // never set: a deliberate bug

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("about to read through a null pointer");
}

void loop() {
  Serial.println(sensor->value);   // crashes here
  delay(1000);
}
```

**Steps.** Upload, then open the PlatformIO serial monitor.

**Capture.** VS Code showing the `Guru Meditation Error … Load access fault` line, the register dump (`MEPC`, `MTVAL`), the decoded backtrace naming `loop` and the line in `main.cpp`, and the `monitor_filters` line in `platformio.ini`.

### D5-02 — Watchdog reset

**Code.** `assets/code/D5-robust-basics.ino` in a Wokwi ESP32-C3 project, or on the real XIAO.

**Steps.** Start it. After a few normal lines, type `h` (Enter). Wait about 5 seconds.

**Capture.** The serial output with `reset reason: power on`, the `simulating a hang` line, the reboot, and `reset reason: task watchdog`.

### E1-01 — Four filament finishes

The photo shows how matte, silk, translucent and black filament look and photograph. You don't need to print anything. One image showing these finishes side by side, from a filament maker's product page or a review, is enough. Note where it came from so a credit line can be added.

### F0-01 — MPU-6050 marked Obsolete

**What it is for.** F0 teaches checking the **chip's** lifecycle on the manufacturer's site. A module listing never shows it. You are right that the module is still easy to buy. The screenshot shows why that can't be taken for granted: the chip on it is already obsolete.

**Steps.** Search "MPU-6050 TDK InvenSense" and open TDK's product page. Capture the part number heading with the status (Obsolete) and the recommended alternate.

### F0-02 — Reading a distributor listing

**Yes, electronic components.** Open the LCSC (or Mouser India) page for **MAX30102EFD+T**, the bare heart-rate chip, and capture the product information area: part number, stock, price breaks, minimum order and datasheet link. Claude adds numbered callouts.

---

## Section 6 items

### C2-W06 — Calibrated photo of the MAX30102 module

**What it is for.** C2's worked example measures the module from a photo, using its own edge pads as the ruler. The image shows that measurement.

**Steps.**
1. Put the black MAX30102 module flat on plain white paper, sensor side up, in good even light.
2. Hold the phone **directly above** it, about 15–20 cm away, parallel to the table (not at an angle), and take the photo. Zoom in rather than moving closer, so the edges stay straight.
3. Send that plain photo. Claude adds the overlay: the 62.2 px pad pitch, the 20.2 × 15.6 mm body, the sensor outline, pin 1 and the 24.5 px/mm scale.


### C1-W11 — Annotate Schematic

This is **not** the Place Text tool. It is the button in the **top** toolbar whose icon shows `R??` above `R42`; **Tools → Annotate Schematic** also opens it. It opens a dialog that numbers every symbol (U1, SW1, SW2 …). Capture that dialog with its default options. Don't press **Annotate** on the real project.

### Moved rows (C1-01, C1-02, C2-01 … E2-03)

Nothing to capture for these. They were old slots replaced by the step-by-step slots in §6 (for example, C2-01 became C2-W06). Capture the §6 IDs instead.
