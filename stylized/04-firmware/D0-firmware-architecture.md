<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">D0 — Firmware Architecture</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Structuring the Code So a Sensor Swap Stays a Small Job</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 4 — Firmware <strong>Time:</strong> ~1.5 hours · <strong>You will produce:</strong> a firmware architecture diagram and a module responsibility table</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Sensor Will Change. Will the Code Survive It?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's motion sensor, the MPU-6050, is obsolete (F0 tells that story). esp\_watch keeps it, because modules are still easy to buy.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Suppose the sensor ever had to be replaced. A new sensor has different registers, a different identity value and different start-up steps. How much of the firmware would have to change?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">That depends entirely on how the firmware is organised. If register addresses are scattered through one long sketch, mixed in with step counting, screen drawing and button handling, the swap touches everything, and every change risks breaking something unrelated. If all the sensor-specific code lives in one small file behind a fixed interface, the swap touches that file and nothing else.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit is about the second kind of firmware: <strong>layered</strong>, split into modules with one job each, with every board-specific number in one place. You will design that structure before writing the code, so that the code has somewhere sensible to go.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Separate</strong> firmware into driver, service and application layers, and <strong>state</strong> what each may and may not know.</li><li style="margin:6px 0;">​<strong>Define</strong> an interface that lets one sensor driver replace another without changing the code above it.</li><li style="margin:6px 0;">​<strong>Organise</strong> code into header and source files, one module per job, with a single configuration header.</li><li style="margin:6px 0;">​<strong>Produce</strong> a firmware architecture diagram and a module responsibility table for your own product.</li><li style="margin:6px 0;">​<strong>Identify</strong> a layering violation from a file's list of includes.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 taught Arduino C++ in single sketches. New here: splitting a whole product's firmware into layers and modules.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — Three Layers</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Who Knows What</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Split the firmware into three <strong>layers</strong>, each allowed to know about the one below it and nothing above:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Layer</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Its job</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">It knows about</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">It must not know about</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Application</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Decide what the product does and when: states, screens, responses to buttons</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Services and interfaces</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Registers, pins, bus addresses</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Services</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Turn raw data into useful information: steps, heart rate, battery percentage</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Driver interfaces</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Which chip produced the data; what is on screen</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Drivers</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Talk to one piece of hardware: registers, pins, timing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The hardware and the bus</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Why the data is wanted</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Below the drivers sits the platform: the Arduino core, the Wire library for I²C, and the ESP32 itself.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Reference Watch, Layered</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is one way to layer esp\_watch's firmware. Its recorded features are three screens with animations, two buttons, step counting, heart rate, and a WiFi fetch of time and weather at first boot.</div>

```text
┌──────────────────────────── APPLICATION ─────────────────────────────┐
│  Screen manager: 3 screens, next / previous, animations              │
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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Notice two things. The display and buttons have drivers but no service, because there is nothing to calculate: the application uses them directly through their drivers. And the time-and-weather service is the only module that knows WiFi exists.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Separation of Concerns</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The layers give you one rule. A second rule works sideways, between modules in the same layer: <strong>each module has one concern and does not reach into another's.</strong></div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">Sensor code does not know about WiFi.</li><li style="margin:6px 0;">Network code does not know about the display.</li><li style="margin:6px 0;">The step counter does not know what screen is showing.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A useful test: if I deleted this module, which other modules would stop compiling? The answer should be only the modules that genuinely use it, and they should use it through its header, never by touching its variables.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — Interfaces: How a Swap Stays Small</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Interface Is the Contract</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">An <strong>interface</strong> is a promise about what a module offers, without saying how. In C++ you write it as a class with only <strong>virtual</strong> functions and no data. Any driver that fills in those functions can be used wherever the interface is expected.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is a motion-sensor interface that names no chip at all:</div>

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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two design choices in this small file matter:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Units are fixed in the interface</strong>: metres per second squared, not raw sensor counts. Every chip reports raw values on a different scale, so converting in the driver keeps that difference out of every layer above.</li><li style="margin:6px 0;">​<strong>read reports failure.</strong> It returns false when the bus read fails, instead of returning zeros that look like real data. A2's failure table depends on the firmware knowing a read failed.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Driver: The Only File That Knows Registers</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The MPU-6050 driver fills in the interface. It is the only place in the firmware with the chip's register addresses: 0x3B for the first acceleration byte, 0x6B for power management, 0x75 for its identity register [2].</div>

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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Write the driver for the part you actually have. A genuine MPU-6050 reads <strong>0x68</strong> [2], but esp\_watch's clone reads <strong>0x70</strong> (see B1). A strict check would refuse to start, so this driver accepts both and reports the clone. The driver above accepts both and reports the clone, so the behaviour is deliberate and visible.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The last line matters too. The chip powers up asleep, with its power register at 0x40 [2], so the driver must wake it. That detail belongs in the driver and nowhere else.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Mock: Same Interface, No Hardware</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">In B5 you met a mock heart-rate sensor. With an interface in place, a mock motion sensor is just another class that fills in the same two functions:</div>

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

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The application chooses which one to use in a single line, driven by a setting in the configuration header:</div>

```cpp
MotionSensor &motion = USE_MOCK_MOTION ? static_cast<MotionSensor &>(mockMotion)
                                       : static_cast<MotionSensor &>(realMotion);
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Everything above that line, including the step counter, runs unchanged on real hardware, in a simulator, or with no sensor at all.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The complete example is a small PlatformIO project in <a href="../assets/code/D0-layered-firmware/">assets/code/D0-layered-firmware/</a>, with a configuration header, the interface, the MPU-6050 driver, the mock, a step-counter service and an application main.cpp. It compiles for the XIAO ESP32-C3 in both real and mock modes.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: What Does the Sensor Swap Touch?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Suppose version 2 replaces the MPU-6050 with the ICM-42670-P. Compare the work in two firmware structures.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Structure A: one sketch.</strong> Register reads for the motion sensor appear in setup() (wake-up), in the step-counting code, in the motion screen, and in a debug screen. Unit conversion is done in two places with a hard-coded 16384.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Structure B: layered, as above.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: List what could differ between the chips.</strong> TDK does not guarantee the two are interchangeable [1], so assume the register addresses, identity value, wake-up sequence and raw-to-units scale all differ.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 2: Find every place each difference lives.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Difference</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Structure A: places to edit</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Structure B: places to edit</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Register addresses</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">wake-up, step code, motion screen, debug screen</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mpu6050\_motion.cpp only</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Identity check</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">setup()</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">driver only</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Wake-up sequence</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">setup()</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">driver only</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Scale to m/s²</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">two conversions</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">driver only</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Step counting logic</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">mixed in with register reads, must be re-checked</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">unchanged</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 3: Count.</strong> Structure A needs edits in four or more functions spread across the sketch, and every one of them also contains unrelated logic that could break. Structure B needs one new driver file, say icm42670\_motion.cpp, filling in the same begin() and read(), plus a changed #include and object line in main.cpp to create it instead.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> In Structure B, the step counter and every screen are untouched, and the mock still works for testing them. The swap has become a <strong>driver</strong> job, which is exactly the claim the layering makes. What it cannot remove is the testing: the new driver must still be checked against real hardware, because the interface promises the shape of the data, not its correctness.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The ICM-42670-P's own register map, identity value and I²C address are in its datasheet, DS-000451, linked from TDK's product page [4].</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>​<strong>Try it: Run the architecture without hardware.</strong> Open the D0 example in PlatformIO (VS Code), or copy its files into a multi-file Wokwi project.</div><div>1. <strong>Predict.</strong> With USE\_MOCK\_MOTION = true, roughly how many steps should be counted per minute, given the mock "walks" at 2 steps per second?</div><div>2. <strong>Do.</strong> Build and run it, and read the serial output for a minute.</div><div>3. <strong>Explain.</strong> Does the count match your prediction? If not, look at the thresholds in step\_counter.cpp: what does the mock's acceleration swing between, and does it cross both thresholds every cycle?</div><div>​<strong>Extra challenge:</strong> Change only the mock so it "walks" at 1 step per second. Which files did you have to touch? Which did you not?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 3 — Files, Modules and One Configuration Header</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Header and Source</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each module is two files:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A <strong>header</strong> (.h) says what the module offers: its class, its functions, its types. Other modules include it.</li><li style="margin:6px 0;">A <strong>source</strong> file (.cpp) says how: the function bodies, private constants, register addresses. Nothing else includes it.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The header is the module's public face, and it should stay small. The register addresses in the example live in the .cpp file, inside an unnamed namespace, so no other file can even see them.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">One Module per Job</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Give each driver, service and application piece its own pair of files. A small watch firmware might look like this:</div>

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

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Configuration Header</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Put <strong>every board-specific number</strong> in one header: pin numbers, bus addresses, clock speeds, timings and feature switches. Nothing else in the firmware should contain a raw pin number.</div>

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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">When the board changes, this is the first file you open. When a reviewer wants to check the firmware against the B3 pin map, this is the only file they need.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Pitfalls When You Split the Code</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's author hit three build problems when moving the firmware to PlatformIO:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Symptom</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Cause</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Fix</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">'Serial' was not declared</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">PlatformIO compiles .cpp files as plain C++, without the Arduino IDE's automatic include</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Add #include &lt;Arduino.h&gt; at the top of every .cpp file that uses Arduino functions</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">multiple definition of setup() and loop()</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Two sketches in src/ are compiled into one program</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Keep one program per environment, using build\_src\_filter in platformio.ini [3]</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">'WxType' does not name a type</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The Arduino IDE inserts function prototypes above the first function, before your enum is declared</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Declare enums used as return types before any function, or move them into a header</td></tr></tbody></table>

<div style="text-align:center;margin:16px 0;"><img src="../assets/platformio/D0-01.png" alt="esp_watch&#x27;s PlatformIO project in VS Code: platformio.ini with one environment per program, each selected with build_src_filter" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch's PlatformIO project in VS Code: platformio.ini with one environment per program, each selected with build\_src\_filter</div></div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Find the layering violation.</div><div>Here are the #include lines at the top of four files in a classmate's project:</div><div>text</div><div>step\_counter.cpp: #include "step\_counter.h" #include "mpu6050\_motion.h"</div><div>screen\_manager.cpp: #include "step\_counter.h" #include "display.h"</div><div>weather.cpp: #include "weather.h" #include "display.h"</div><div>mpu6050\_motion.cpp: #include &lt;Arduino.h&gt; #include "mpu6050\_motion.h"</div><div>1. <strong>Predict.</strong> Which two files break the rules?</div><div>2. <strong>Do.</strong> For each include, name the layer of the including file and of the included file. Mark any include that goes to a specific chip from a service, or sideways into another concern.</div><div>3. <strong>Explain.</strong> What should each violating file include instead?</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>step\_counter.cpp</strong> is a service including a specific chip's driver. It should include only motion\_sensor.h, the interface, so it works with any sensor or mock. <strong>weather.cpp</strong> is a network service including the display: network code must not know about the screen. It should return the weather to the application, which decides how to show it. The other two are fine: the screen manager is application code using a service and a driver, and the driver includes its own header and the platform.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Module Responsibility Table</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The deliverable for this unit is a table with one row per module, which makes the architecture checkable:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Module</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Layer</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Responsibility (one sentence)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Depends on</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Must not know about</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">config.h</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Holds every pin, address, timing and switch</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">nothing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MotionSensor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Interface</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Promises acceleration in m/s², with failure reported</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">nothing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">any chip</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Mpu6050Motion</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Driver</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reads acceleration from an MPU-6050 over I²C</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Wire, MotionSensor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">steps, screens</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">StepCounter</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Service</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Counts steps from acceleration</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MotionSensor types</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">which chip; the display</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">main.cpp</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Application</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Schedules reads and reports steps</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">all of the above</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">registers</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The "must not know about" column is the one that catches problems. If anyone writes code that needs something from that column, the architecture is being broken, and the table makes it visible in review.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Draw your layers.</strong> Using your A1 subsystems and B2 block diagram, list every driver your hardware needs, every service that turns data into information, and the application pieces from your A2 state diagram. Draw them as a layered diagram.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Define one interface.</strong> For the part in your design most likely to change (check its lifecycle from B4), write the interface header: functions, units, and how failure is reported.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Write your configuration header.</strong> Transcribe every pin, address and timing from B3. No raw numbers anywhere else.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Build the module responsibility table.</strong> One row per module, with the "must not know about" column filled in.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Swap test on paper.</strong> For the part from step 2, list every file a replacement would touch. If it is more than the new driver and the application lines that create it, find what leaked upwards.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> save the architecture diagram and module responsibility table in your design pack as D0-firmware-architecture.md, with your interface header and configuration header attached. Commit the PlatformIO project to your design pack's repository, leaving out its .pio/ build folder (<a href="../01-system-architecture/REF-version-control.md">Version Control</a>, Step 4).</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open D0-firmware-architecture.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The diagram shows three layers, and every arrow points downwards. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every hardware part in your B2 block diagram has a driver. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. At least one interface header exists, with units stated. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. The interface's read function can report failure. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The configuration header contains every pin number in your B3 pin map. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. No module other than config.h contains a raw pin number or bus address. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Every module in the table has a one-sentence responsibility. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Every module has its "must not know about" column filled in. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. Your swap test lists only the new driver and the application lines that create it. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A step counter calls mpu.getAccelX() directly on an MPU-6050 library object. Version 2 changes the sensor. What is the main architectural problem?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The function name is too long.</li><li style="margin:6px 0;">B. The service depends on a specific chip, so changing the chip means changing the step counter as well as the driver.</li><li style="margin:6px 0;">C. The step counter should read registers itself.</li><li style="margin:6px 0;">D. There is no problem as long as the new library has the same function name.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A service that names a chip cannot outlive that chip. Depending on an interface instead keeps the change inside the driver. <strong>A</strong> is cosmetic. <strong>C</strong> makes things worse, pushing register knowledge up into the service. <strong>D</strong> hopes for a coincidence; different libraries rarely match, and even if they did, units and failure behaviour may not.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A driver's read() returns zeros when the I²C read fails. Why is this a poor design?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Zeros use more memory.</li><li style="margin:6px 0;">B. The layers above cannot tell "no motion" from "the read failed", so failures are silently treated as real data.</li><li style="margin:6px 0;">C. Drivers should never fail.</li><li style="margin:6px 0;">D. It makes the code run slower.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A failed read must be visible, or the failure table from A2 cannot be implemented: the watch would count zero steps instead of reporting a sensor fault. <strong>A</strong> and <strong>D</strong> are not meaningful effects. <strong>C</strong> is unrealistic: buses fail, and the reference watch's breadboard saw read failures of up to 80%.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> Where should the I²C clock speed and the motion sensor's address be defined?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. In the motion-sensor driver's source file</li><li style="margin:6px 0;">B. In the configuration header, and passed into the driver</li><li style="margin:6px 0;">C. In the application's loop()</li><li style="margin:6px 0;">D. Wherever they are first needed</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Board-specific numbers belong in one place, so a board change means editing one file, and a reviewer can check them against the pin map in one place. <strong>A</strong> hides a board decision inside a driver. <strong>C</strong> buries it in timing logic. <strong>D</strong> is how the same number ends up in three places with two different values.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A PlatformIO build fails with 'Serial' was not declared in this scope in sensor.cpp, although the same code worked in the Arduino IDE. What is the fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Rename the file to sensor.ino.</li><li style="margin:6px 0;">B. Add #include &lt;Arduino.h&gt; at the top of sensor.cpp.</li><li style="margin:6px 0;">C. Declare Serial as a global variable.</li><li style="margin:6px 0;">D. Move all code back into one file.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The Arduino IDE adds that include automatically to sketches; PlatformIO compiles .cpp files as plain C++, so you must add it. <strong>A</strong> fights the build system. <strong>C</strong> would create a second, broken Serial. <strong>D</strong> gives up the structure to avoid a one-line fix.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A weather module calls display.print() to show the forecast directly. Which rule does this break, and what is the better design?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. No rule; it saves code.</li><li style="margin:6px 0;">B. Separation of concerns: network code should return the forecast, and the application should decide whether and how to display it.</li><li style="margin:6px 0;">C. The weather module should draw the whole screen.</li><li style="margin:6px 0;">D. The display should fetch the weather itself.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Once the weather module knows about the display, changing screens or display hardware means changing network code too. <strong>A</strong> saves a line and costs flexibility. <strong>C</strong> makes the problem bigger. <strong>D</strong> moves the same tangle in the opposite direction.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="D1-flowcharts-and-state-diagrams.md">D1 — Flowcharts and State Diagrams</a> you will design the application layer's behaviour before writing it: the main loop as a flowchart, the device as a state machine, and the conversations between modules as sequence diagrams.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. TDK. MPU-6050 detailed information (product status "Obsolete"; recommended alternate ICM-42670-P, "Interchangeability is not guaranteed"). https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part\_no=MPU-6050</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. InvenSense. MPU-6000 and MPU-6050 Register Map and Descriptions, RM-MPU-6000A-00 (ACCEL\_XOUT\_H 0x3B; PWR\_MGMT\_1 0x6B, reset value 0x40; WHO\_AM\_I 0x75, default 0x68; ±2 g sensitivity 16384 LSB/g), hosted by SparkFun. https://cdn.sparkfun.com/datasheets/Sensors/Accelerometers/RM-MPU-6000A.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. PlatformIO. build\_src\_filter (choosing which source files are included in a build). https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build\_src\_filter.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. TDK InvenSense. ICM-42670-P product page (datasheet DS-000451). https://invensense.tdk.com/products/motion-tracking/6-axis/icm-42670-p/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
