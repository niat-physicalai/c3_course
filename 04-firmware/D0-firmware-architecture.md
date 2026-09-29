# D0 — Firmware Architecture
## Structuring the Code So a Sensor Swap Stays a Small Job

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Firmware
**Time:** ~1.5 hours · **You will produce:** a firmware architecture diagram and a module responsibility table

---

### The Sensor Will Change. Will the Code Survive It?

<!-- REFPRODUCT:START -->
esp_watch's motion sensor, the MPU-6050, is obsolete (F0 tells that story). esp_watch keeps it, because modules are still easy to buy.
<!-- REFPRODUCT:END -->

Suppose the sensor ever had to be replaced. A new sensor has different registers, a different identity value and different start-up steps. How much of the firmware would have to change?

That depends entirely on how the firmware is organised. If register addresses are scattered through one long sketch, mixed in with step counting, screen drawing and button handling, the swap touches everything, and every change risks breaking something unrelated. If all the sensor-specific code lives in one small file behind a fixed interface, the swap touches that file and nothing else.

This unit is about the second kind of firmware: **layered**, split into modules with one job each, with every board-specific number in one place. You will design that structure before writing the code, so that the code has somewhere sensible to go.

### What You Will Be Able to Do After This Reading

- **Separate** firmware into driver, service and application layers, and **state** what each may and may not know.
- **Define** an interface that lets one sensor driver replace another without changing the code above it.
- **Organise** code into header and source files, one module per job, with a single configuration header.
- **Produce** a firmware architecture diagram and a module responsibility table for your own product.
- **Identify** a layering violation from a file's list of includes.

### What Part 1 Already Covered

Part 1 taught Arduino C++ in single sketches. New here: splitting a whole product's firmware into layers and modules.

---

# Part 1 — Three Layers

## Who Knows What

Split the firmware into three **layers**, each allowed to know about the one below it and nothing above:

| Layer | Its job | It knows about | It must not know about |
|---|---|---|---|
| **Application** | Decide what the product does and when: states, screens, responses to buttons | Services and interfaces | Registers, pins, bus addresses |
| **Services** | Turn raw data into useful information: steps, heart rate, battery percentage | Driver interfaces | Which chip produced the data; what is on screen |
| **Drivers** | Talk to one piece of hardware: registers, pins, timing | The hardware and the bus | Why the data is wanted |

Below the drivers sits the platform: the Arduino core, the `Wire` library for I²C, and the ESP32 itself.

## The Reference Watch, Layered

<!-- REFPRODUCT:START -->
Here is one way to layer esp_watch's firmware. Its recorded features are three screens with animations, two buttons, step counting, heart rate, and a WiFi fetch of time and weather at first boot.

```text
┌──────────────────────────── APPLICATION ─────────────────────────────┐
│  Screen manager: 3 screens, next / previous, animations              │
│  Power manager: 30 s timeout → sleep, shake → wake                   │
└───────┬──────────────┬───────────────┬───────────────────────────────┘
        │              │               │
┌───────▼──────┐ ┌─────▼───────┐ ┌─────▼─────────────┐
│ Step counter │ │ Heart-rate  │ │ Time and weather  │  SERVICES
│              │ │ calculator  │ │ (WiFi, once)      │
└───────┬──────┘ └─────┬───────┘ └─────┬─────────────┘
        │              │               │
┌───────▼──────┐ ┌─────▼───────┐ ┌─────▼──────┐ ┌───────────┐ ┌─────────┐
│ MotionSensor │ │ HeartSensor │ │ WiFi       │ │ Display   │ │ Buttons │ DRIVERS
│ (MPU-6050)   │ │ (MAX30102)  │ │            │ │ (SSD1306) │ │         │
└───────┬──────┘ └─────┬───────┘ └────────────┘ └─────┬─────┘ └─────────┘
        └──────────────┴────── I²C bus (Wire) ────────┘       PLATFORM: Arduino core
```
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — the actual file and module structure of watch_ui_test.ino is not recorded in REFERENCE-PRODUCT.md; the layering above is a proposed structure, not a description of the author's code -->

Notice two things. The display and buttons have drivers but no service, because there is nothing to calculate: the application uses them directly through their drivers. And the time-and-weather service is the *only* module that knows WiFi exists.

## Separation of Concerns

The layers give you one rule. A second rule works sideways, between modules in the same layer: **each module has one concern and does not reach into another's.**

- Sensor code does not know about WiFi.
- Network code does not know about the display.
- The step counter does not know what screen is showing.

A useful test: *if I deleted this module, which other modules would stop compiling?* The answer should be only the modules that genuinely use it, and they should use it through its header, never by touching its variables.

---

# Part 2 — Interfaces: How a Swap Stays Small

## The Interface Is the Contract

An **interface** is a promise about what a module offers, without saying how. In C++ you write it as a class with only **virtual** functions and no data. Any driver that fills in those functions can be used wherever the interface is expected.

Here is a motion-sensor interface that names no chip at all:

```cpp
// motion_sensor.h — what the rest of the firmware knows about a motion sensor.
// Nothing here names a chip. Any driver that fills in these two functions
// can replace any other.
#pragma once

struct Accel {
  float x, y, z;   // metres per second squared
};

class MotionSensor {
public:
  virtual ~MotionSensor() {}
  virtual bool begin() = 0;
  virtual bool read(Accel &out) = 0;   // false if the read failed
};
```

Two design choices in this small file matter:

- **Units are fixed in the interface**: metres per second squared, not raw sensor counts. Every chip reports raw values on a different scale, so converting in the driver keeps that difference out of every layer above.
- **`read` reports failure.** It returns `false` when the bus read fails, instead of returning zeros that look like real data. A2's failure table depends on the firmware *knowing* a read failed.

## The Driver: The Only File That Knows Registers

The MPU-6050 driver fills in the interface. It is the only place in the firmware with the chip's register addresses: `0x3B` for the first acceleration byte, `0x6B` for power management, `0x75` for its identity register [2].

```cpp
bool Mpu6050Motion::begin() {
  bus_.beginTransmission(addr_);
  bus_.write(REG_WHO_AM_I);
  if (bus_.endTransmission(false) != 0) return false;
  if (bus_.requestFrom(addr_, (uint8_t)1) != 1) return false;
  uint8_t id = bus_.read();
  // A genuine MPU-6050 answers 0x68. Clone chips answer other values
  // (esp_watch's reads 0x70) and still work, so accept both, and report it.
  if (id != 0x68 && id != 0x70) return false;
  if (id != 0x68) Serial.printf("MPU-6050 WHO_AM_I = 0x%02X (clone)\n", id);
  return writeReg(REG_PWR_MGMT_1, 0x00);   // clear SLEEP: start measuring
}
```

<!-- REFPRODUCT:START -->
Write the driver for the part you actually have. A genuine MPU-6050 reads **0x68** [2], but esp_watch's clone reads **0x70** (see B1). A strict check would refuse to start, so this driver accepts both and reports the clone. The driver above accepts both and reports the clone, so the behaviour is deliberate and visible.
<!-- REFPRODUCT:END -->

The last line matters too. The chip powers up asleep, with its power register at 0x40 [2], so the driver must wake it. That detail belongs in the driver and nowhere else.

## The Mock: Same Interface, No Hardware

In B5 you met a mock heart-rate sensor. With an interface in place, a mock motion sensor is just another class that fills in the same two functions:

```cpp
class MockMotion : public MotionSensor {
public:
  bool begin() override { return true; }
  bool read(Accel &out) override {
    float t = millis() / 1000.0f;
    out.x = 0.5f * sinf(t);
    out.y = 0.3f;
    out.z = 9.81f + 3.0f * sinf(2.0f * PI * 2.0f * t);   // "walking" at 2 steps/s
    return true;
  }
};
```

The application chooses which one to use in a single line, driven by a setting in the configuration header:

```cpp
MotionSensor &motion = USE_MOCK_MOTION ? static_cast<MotionSensor &>(mockMotion)
                                       : static_cast<MotionSensor &>(realMotion);
```

Everything above that line, including the step counter, runs unchanged on real hardware, in a simulator, or with no sensor at all.

The complete example is a small PlatformIO project in [`assets/code/D0-layered-firmware/`](../assets/code/D0-layered-firmware/), with a configuration header, the interface, the MPU-6050 driver, the mock, a step-counter service and an application `main.cpp`. It compiles for the XIAO ESP32-C3 in both real and mock modes.

### Worked Example: What Does the Sensor Swap Touch?

Suppose version 2 replaces the MPU-6050 with the ICM-42670-P. Compare the work in two firmware structures.

**Structure A: one sketch.** Register reads for the motion sensor appear in `setup()` (wake-up), in the step-counting code, in the shake-to-wake code, and in a debug screen. Unit conversion is done in two places with a hard-coded 16384.

**Structure B: layered, as above.**

**Step 1: List what could differ between the chips.** TDK does not guarantee the two are interchangeable [1], so assume the register addresses, identity value, wake-up sequence and raw-to-units scale all differ.

**Step 2: Find every place each difference lives.**

| Difference | Structure A: places to edit | Structure B: places to edit |
|---|---|---|
| Register addresses | wake-up, step code, shake code, debug screen | `mpu6050_motion.cpp` only |
| Identity check | `setup()` | driver only |
| Wake-up sequence | `setup()` | driver only |
| Scale to m/s² | two conversions | driver only |
| Step counting logic | mixed in with register reads, must be re-checked | unchanged |

**Step 3: Count.** Structure A needs edits in four or more functions spread across the sketch, and every one of them also contains unrelated logic that could break. Structure B needs one new driver file, say `icm42670_motion.cpp`, filling in the same `begin()` and `read()`, plus a changed `#include` and object line in `main.cpp` to create it instead.

**Check.** In Structure B, the step counter, the shake-to-wake logic and every screen are untouched, and the mock still works for testing them. The swap has become a **driver** job, which is exactly the claim the layering makes. What it cannot remove is the testing: the new driver must still be checked against real hardware, because the interface promises the *shape* of the data, not its correctness.

<!-- LINK:VERIFY  want: "TDK ICM-42670-P datasheet (register map, WHO_AM_I value, I2C address)"  search: "TDK ICM-42670-P datasheet DS-000451" -->

> **Try it: Run the architecture without hardware.** Open the D0 example in PlatformIO (VS Code), or copy its files into a multi-file Wokwi project.
> 1. **Predict.** With `USE_MOCK_MOTION = true`, roughly how many steps should be counted per minute, given the mock "walks" at 2 steps per second?
> 2. **Do.** Build and run it, and read the serial output for a minute.
> 3. **Explain.** Does the count match your prediction? If not, look at the thresholds in `step_counter.cpp`: what does the mock's acceleration swing between, and does it cross both thresholds every cycle?
>
> **Extra challenge:** Change only the mock so it "walks" at 1 step per second. Which files did you have to touch? Which did you not?

---

# Part 3 — Files, Modules and One Configuration Header

## Header and Source

Each module is two files:

- A **header** (`.h`) says *what* the module offers: its class, its functions, its types. Other modules include it.
- A **source** file (`.cpp`) says *how*: the function bodies, private constants, register addresses. Nothing else includes it.

The header is the module's public face, and it should stay small. The register addresses in the example live in the `.cpp` file, inside an unnamed namespace, so no other file can even see them.

## One Module per Job

Give each driver, service and application piece its own pair of files. A small watch firmware might look like this:

```text
include/
  config.h              pins, addresses, timings, feature switches
  motion_sensor.h       interface
  mpu6050_motion.h      driver
  mock_motion.h         test stand-in
  step_counter.h        service
src/
  mpu6050_motion.cpp
  step_counter.cpp
  main.cpp              application
platformio.ini
```

<!-- MEDIA
type: screenshot
id: D0-01
caption: The layered example project open in VS Code with PlatformIO
brief: VS Code with the PlatformIO extension, the D0-layered-firmware folder open. Explorer
  panel on the left showing include/ (config.h, motion_sensor.h, mpu6050_motion.h,
  mock_motion.h, step_counter.h), src/ (main.cpp, mpu6050_motion.cpp, step_counter.cpp)
  and platformio.ini. Editor showing motion_sensor.h. The PlatformIO status bar visible
  at the bottom with the build (tick) button. Terminal panel showing a successful build
  ending in "[SUCCESS]". Light theme.
-->

## The Configuration Header

Put **every board-specific number** in one header: pin numbers, bus addresses, clock speeds, timings and feature switches. Nothing else in the firmware should contain a raw pin number.

```cpp
// config.h — every board-specific number lives here, and only here.
#pragma once
#include <stdint.h>

// Pin map (from B3)
constexpr int PIN_SDA = 6;   // D4
constexpr int PIN_SCL = 7;   // D5

// I2C
constexpr uint32_t I2C_CLOCK_HZ = 400000;
constexpr uint8_t  ADDR_IMU     = 0x68;   // MPU-6050, AD0 tied to GND

// Timing
constexpr uint32_t MOTION_PERIOD_MS = 20;    // 50 samples per second
constexpr uint32_t REPORT_PERIOD_MS = 1000;

// Set to true to run without hardware (for example in a simulator).
constexpr bool USE_MOCK_MOTION = false;
```

When the board changes, this is the first file you open. When a reviewer wants to check the firmware against the B3 pin map, this is the only file they need.

## Pitfalls When You Split the Code

<!-- REFPRODUCT:START -->
esp_watch's author hit two build problems when moving the firmware to PlatformIO:

| Symptom | Cause | Fix |
|---|---|---|
| `'Serial' was not declared` | PlatformIO compiles `.cpp` files as plain C++, without the Arduino IDE's automatic include | Add `#include <Arduino.h>` at the top of every `.cpp` file that uses Arduino functions |
| `multiple definition of setup()` and `loop()` | Two sketches in `src/` are compiled into one program | Keep one program per environment, using `build_src_filter` in `platformio.ini` [3] |

| Symptom | Cause | Fix |
|---|---|---|
| `'Serial' was not declared` | PlatformIO compiles `.cpp` files as plain C++, without the Arduino IDE's automatic include | Add `#include <Arduino.h>` at the top of every `.cpp` file that uses Arduino functions |
| `multiple definition of setup()` and `loop()` | Two sketches in `src/` are compiled into one program | Keep one program per environment, using `build_src_filter` in `platformio.ini` [3] |
| `'WxType' does not name a type` | The Arduino IDE inserts function prototypes above the first function, before your `enum` is declared | Declare enums used as return types before any function, or move them into a header |
<!-- REFPRODUCT:END -->

> **Try it: Find the layering violation.** Here are the `#include` lines at the top of four files in a classmate's project:
>
> ```text
> step_counter.cpp:    #include "step_counter.h"   #include "mpu6050_motion.h"
> screen_manager.cpp:  #include "step_counter.h"   #include "display.h"
> weather.cpp:         #include "weather.h"        #include "display.h"
> mpu6050_motion.cpp:  #include <Arduino.h>        #include "mpu6050_motion.h"
> ```
>
> 1. **Predict.** Which two files break the rules?
> 2. **Do.** For each include, name the layer of the including file and of the included file. Mark any include that goes to a specific chip from a service, or sideways into another concern.
> 3. **Explain.** What should each violating file include instead?

<details>
<summary>Answer</summary>

**`step_counter.cpp`** is a service including a specific chip's driver. It should include only `motion_sensor.h`, the interface, so it works with any sensor or mock. **`weather.cpp`** is a network service including the display: network code must not know about the screen. It should return the weather to the application, which decides how to show it. The other two are fine: the screen manager is application code using a service and a driver, and the driver includes its own header and the platform.

</details>

## The Module Responsibility Table

The deliverable for this unit is a table with one row per module, which makes the architecture checkable:

| Module | Layer | Responsibility (one sentence) | Depends on | Must not know about |
|---|---|---|---|---|
| `config.h` | — | Holds every pin, address, timing and switch | nothing | — |
| `MotionSensor` | Interface | Promises acceleration in m/s², with failure reported | nothing | any chip |
| `Mpu6050Motion` | Driver | Reads acceleration from an MPU-6050 over I²C | `Wire`, `MotionSensor` | steps, screens |
| `StepCounter` | Service | Counts steps from acceleration | `MotionSensor` types | which chip; the display |
| `main.cpp` | Application | Schedules reads and reports steps | all of the above | registers |

The "must not know about" column is the one that catches problems. If anyone writes code that needs something from that column, the architecture is being broken, and the table makes it visible in review.

---

# Putting It All Together

## Applying What You Have Learned

**1. Draw your layers.** Using your A1 subsystems and B2 block diagram, list every driver your hardware needs, every service that turns data into information, and the application pieces from your A2 state diagram. Draw them as a layered diagram.

**2. Define one interface.** For the part in your design most likely to change (check its lifecycle from B4), write the interface header: functions, units, and how failure is reported.

**3. Write your configuration header.** Transcribe every pin, address and timing from B3. No raw numbers anywhere else.

**4. Build the module responsibility table.** One row per module, with the "must not know about" column filled in.

**5. Swap test on paper.** For the part from step 2, list every file a replacement would touch. If it is more than the new driver and the application lines that create it, find what leaked upwards.

**Deliverable:** save the architecture diagram and module responsibility table in your design pack as `D0-firmware-architecture.md`, with your interface header and configuration header attached.

## Self-Check

Open `D0-firmware-architecture.md` and answer each item Y or N.

1. The diagram shows three layers, and every arrow points downwards. — Y/N
2. Every hardware part in your B2 block diagram has a driver. — Y/N
3. At least one interface header exists, with units stated. — Y/N
4. The interface's read function can report failure. — Y/N
5. The configuration header contains every pin number in your B3 pin map. — Y/N
6. No module other than `config.h` contains a raw pin number or bus address. — Y/N
7. Every module in the table has a one-sentence responsibility. — Y/N
8. Every module has its "must not know about" column filled in. — Y/N
9. Your swap test lists only the new driver and the application lines that create it. — Y/N

---

## Check Your Understanding

**1.** A step counter calls `mpu.getAccelX()` directly on an MPU-6050 library object. Version 2 changes the sensor. What is the main architectural problem?

- A. The function name is too long.
- B. The service depends on a specific chip, so changing the chip means changing the step counter as well as the driver.
- C. The step counter should read registers itself.
- D. There is no problem as long as the new library has the same function name.

<details>
<summary>Answer</summary>

**B.** A service that names a chip cannot outlive that chip. Depending on an interface instead keeps the change inside the driver. **A** is cosmetic. **C** makes things worse, pushing register knowledge up into the service. **D** hopes for a coincidence; different libraries rarely match, and even if they did, units and failure behaviour may not.

</details>

**2.** A driver's `read()` returns zeros when the I²C read fails. Why is this a poor design?

- A. Zeros use more memory.
- B. The layers above cannot tell "no motion" from "the read failed", so failures are silently treated as real data.
- C. Drivers should never fail.
- D. It makes the code run slower.

<details>
<summary>Answer</summary>

**B.** A failed read must be visible, or the failure table from A2 cannot be implemented: the watch would count zero steps instead of reporting a sensor fault. **A** and **D** are not meaningful effects. **C** is unrealistic: buses fail, and the reference watch's breadboard saw read failures of up to 80%.

</details>

**3.** Where should the I²C clock speed and the motion sensor's address be defined?

- A. In the motion-sensor driver's source file
- B. In the configuration header, and passed into the driver
- C. In the application's `loop()`
- D. Wherever they are first needed

<details>
<summary>Answer</summary>

**B.** Board-specific numbers belong in one place, so a board change means editing one file, and a reviewer can check them against the pin map in one place. **A** hides a board decision inside a driver. **C** buries it in timing logic. **D** is how the same number ends up in three places with two different values.

</details>

**4.** A PlatformIO build fails with `'Serial' was not declared in this scope` in `sensor.cpp`, although the same code worked in the Arduino IDE. What is the fix?

- A. Rename the file to `sensor.ino`.
- B. Add `#include <Arduino.h>` at the top of `sensor.cpp`.
- C. Declare `Serial` as a global variable.
- D. Move all code back into one file.

<details>
<summary>Answer</summary>

**B.** The Arduino IDE adds that include automatically to sketches; PlatformIO compiles `.cpp` files as plain C++, so you must add it. **A** fights the build system. **C** would create a second, broken `Serial`. **D** gives up the structure to avoid a one-line fix.

</details>

**5.** A weather module calls `display.print()` to show the forecast directly. Which rule does this break, and what is the better design?

- A. No rule; it saves code.
- B. Separation of concerns: network code should return the forecast, and the application should decide whether and how to display it.
- C. The weather module should draw the whole screen.
- D. The display should fetch the weather itself.

<details>
<summary>Answer</summary>

**B.** Once the weather module knows about the display, changing screens or display hardware means changing network code too. **A** saves a line and costs flexibility. **C** makes the problem bigger. **D** moves the same tangle in the opposite direction.

</details>

---

## What Comes Next

In [D1 — Flowcharts and State Diagrams](D1-flowcharts-and-state-diagrams.md) you will design the application layer's behaviour before writing it: the main loop as a flowchart, the device as a state machine, and the conversations between modules as sequence diagrams.

---

## References

1. TDK. *MPU-6050 detailed information* (product status "Obsolete"; recommended alternate ICM-42670-P, "Interchangeability is not guaranteed"). https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part_no=MPU-6050
2. InvenSense. *MPU-6000 and MPU-6050 Register Map and Descriptions*, RM-MPU-6000A-00 (ACCEL_XOUT_H 0x3B; PWR_MGMT_1 0x6B, reset value 0x40; WHO_AM_I 0x75, default 0x68; ±2 g sensitivity 16384 LSB/g), hosted by SparkFun. https://cdn.sparkfun.com/datasheets/Sensors/Accelerometers/RM-MPU-6000A.pdf
3. PlatformIO. *build_src_filter* (choosing which source files are included in a build). https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_src_filter.html

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
