# C7 — Going Further (Reading Only)
## Seven Topics Beyond This Course, and When You Would Need Them

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Firmware
**Time:** ~30 minutes · **You will produce:** answers to the check questions at the end

---

### What a Product Needs After Version 1

The firmware you have designed does what version 1 needs. A product that ships to hundreds of people, lasts for years, or handles private data will need more. This short reading introduces seven topics, one page's worth each. You will not build any of them in this course. The goal is to recognise when your product needs one, and where to start reading.

### What You Will Be Able to Do After This Reading

- **Recognise** which of these seven topics a given product requirement calls for.
- **Explain** each topic's main benefit and its main cost in one or two sentences.

### What Part 1 Already Covered

Part 1 introduced MQTT, cloud connectivity and working with the ESP32 in Arduino C++. **What is new here** is a map of the next layer: how professional firmware is updated, organised, secured, powered down and tested.

---

## 1. Over-the-Air (OTA) Updates

**What it is.** The device downloads new firmware over the network and installs it itself. ESP-IDF's OTA system stores the new firmware alongside the running one, tracks which version is valid, and can **roll back** to the previous version if the new one fails to start properly [1].

**When you need it.** As soon as devices are in other people's hands. Without OTA, every bug fix means collecting devices and plugging them into a laptop.

**The cost.** Twice the flash space for firmware, a secure way to deliver updates, and a plan for what happens when an update fails halfway, for example on a flat battery.

## 2. FreeRTOS Tasks and Queues

**What it is.** The ESP32's software already runs on **FreeRTOS**, a small real-time operating system [2]. Instead of one `loop()` checking every task in turn (C4), you can create separate **tasks** that each run their own loop, and pass data between them through **queues**.

**When you need it.** When jobs genuinely need to run independently: for example, a network task that may wait for seconds should not hold up a sensor task that must run every 20 ms.

**The cost.** New kinds of bugs: two tasks using the same variable at once, a task starving another of processor time, stack sizes to choose for each task. C4's single-loop approach avoids all of these, which is why it is the right place to start.

## 3. ESP-IDF Instead of Arduino

**What it is.** **ESP-IDF** is Espressif's own development framework, which the Arduino core for ESP32 is built on top of [3]. It gives direct access to every chip feature and configuration option.

**When you need it.** When you need something the Arduino layer hides or does not expose, such as fine control of power management, security features, or build configuration.

**The cost.** More setup, more code for simple things, and fewer beginner-friendly libraries. Many products stay on Arduino successfully; some move to ESP-IDF once they need its control.

## 4. MQTT With TLS

**What it is.** The C5b sketch sends MQTT unencrypted on port 1883, and the public test broker warns that "anybody could be listening" [4]. **TLS** encrypts the connection, and certificates prove the broker, and optionally the device, are who they claim to be. The same test broker offers encrypted ports, such as 8883, for practice [4].

**When you need it.** Whenever the data is private, such as heart rate (A2), or whenever someone could send your device a malicious command.

**The cost.** More memory and processing, certificates to install and eventually renew, and more time connecting, which matters for battery life.

## 5. BLE as an Alternative to WiFi

**What it is.** **Bluetooth Low Energy** connects the watch to a phone nearby, and the phone relays data to the internet if needed. The ESP32-C3 supports it alongside WiFi.

**When you need it.** For a wearable that syncs often with a phone the wearer always carries (A1's connection choice). BLE generally uses less power than WiFi for small, frequent transfers, and it does not need the wearer's WiFi password.

**The cost.** A phone app, which is a second product to design, build and maintain.

<!-- REFPRODUCT:START -->
Seeed's figures for the XIAO ESP32-C3 show the trade-off is not simple: they list light sleep at about 4 mA with WiFi enabled and about 10 mA with BLE enabled [5]. The right choice depends on how often and how much the device sends, which is exactly what your B1 current budget exists to answer.
<!-- REFPRODUCT:END -->

## 6. Deep Sleep and Duty Cycling

**What it is.** In **light sleep**, the processor pauses and resumes where it left off. In **deep sleep**, almost everything is powered off, including most RAM, and the chip restarts from the beginning when it wakes [6].

**When you need it.** When the battery budget is dominated by sleep current, which A0 and B1 showed is the case for esp_watch.

<!-- REFPRODUCT:START -->
Seeed lists the XIAO ESP32-C3's deep-sleep current at about 44 µA, against about 4 mA in light sleep [5], roughly 90 times less. esp_watch sleeps with its motion sensor on so that a shake can wake it. For deep sleep to work that way, the motion sensor's interrupt must be connected to a pin that can wake the chip from deep sleep. Espressif's documentation says only pins in the chip's RTC power domain can do this, and refers to the datasheet for the exact list [6]. Whether esp_watch's motion interrupt on GPIO5 qualifies is the first thing a version 2 would need to check.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY whether GPIO5 on the ESP32-C3 is in the VDD3P3_RTC domain and can wake the chip from deep sleep was not confirmed from the datasheet -->

<!-- MEDIA
type: diagram
id: C7-01
caption: Active, light sleep and deep sleep on the XIAO ESP32-C3: what stays on, and roughly what it costs
brief: A three-column comparison graphic. Column 1 "Active": CPU, RAM, radio all shown on;
  "< 75 mA (Seeed)". Column 2 "Light sleep": CPU paused (state kept), RAM kept, radio off
  or idle; "~4 mA with WiFi (Seeed)". Column 3 "Deep sleep": CPU, most RAM and peripherals
  off, only the RTC section on; "~44 µA (Seeed)"; a note "wakes by restarting". Use a
  logarithmic bar under each column to show the current difference. Mark all figures
  "Seeed's published figures for the board".
-->

**The cost.** Everything in RAM is lost on each wake, so state must be saved first, and waking takes longer than resuming from light sleep.

## 7. Unit Testing Embedded Code

**What it is.** Small automated tests that check one function at a time, such as "does the step counter count 10 steps from this recorded acceleration data?". PlatformIO can run the same tests on your laptop (**native**) or on a real board [7].

**When you need it.** As soon as you change code that already works. A test catches the change that quietly breaks step counting before anyone wears the watch.

**The cost.** Writing the tests, and designing code that can be tested. C0's layers and C3's mocks help here: a step counter that depends only on an interface can be tested on a laptop with recorded data and no hardware at all.

<!-- REFPRODUCT:START -->
The reference watch's firmware, `watch_ui_test.ino`, is a single test sketch covering three screens, animations, two buttons, steps, heart rate and a WiFi weather fetch. The topics above describe where such a sketch goes next: structured into modules (C0), then tested, secured and made updatable.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/firmware/watch_ui_test/watch_ui_test.ino -->

---

# Putting It All Together

## Applying What You Have Learned

For your own product, pick the **two** topics above that version 2 would need first. For each, write one sentence naming the requirement that calls for it, and one sentence naming its main cost. Add both to your capstone's "what I would change in v2" page.

---

## Check Your Understanding

**1.** A watch will be given to 200 students for a semester. A bug is found in week 3. Which topic would have made fixing it simplest?

- A. BLE
- B. Over-the-air updates
- C. Deep sleep
- D. Unit testing

<details>
<summary>Answer</summary>

**B.** OTA delivers the fix to every device without collecting them. **D** might have caught the bug earlier, but it does not help once devices are deployed. **A** and **C** are unrelated to updating firmware.

</details>

**2.** A network request sometimes waits for several seconds, and the motion sensor must still be read every 20 ms. Which approach separates the two most cleanly?

- A. A longer watchdog timeout
- B. Running the network work in its own FreeRTOS task, passing results through a queue
- C. Reading the sensor less often
- D. Using deep sleep

<details>
<summary>Answer</summary>

**B.** Separate tasks let the slow job wait without holding up the fast one. **A** hides the symptom. **C** changes the requirement. **D** stops everything.

</details>

**3.** A watch sends heart-rate readings to a cloud broker. Which topic addresses the privacy risk?

- A. MQTT with TLS
- B. FreeRTOS
- C. ESP-IDF
- D. Unit testing

<details>
<summary>Answer</summary>

**A.** TLS encrypts the data in transit and verifies the broker. **B**, **C** and **D** do not protect the data on the network.

</details>

**4.** A design wants to use deep sleep and wake on a wrist shake. What must be checked first?

- A. That the display supports deep sleep
- B. That the motion sensor's interrupt is on a pin able to wake the chip from deep sleep
- C. That WiFi is disabled
- D. That the I²C bus runs at 400 kHz

<details>
<summary>Answer</summary>

**B.** Only certain pins can wake the chip from deep sleep. If the interrupt is on the wrong one, shake-to-wake cannot work, whatever the firmware does. **A**, **C** and **D** do not determine whether the chip can wake.

</details>

**5.** Why do C0's interfaces and mocks make unit testing easier?

- A. They make the code run faster.
- B. A service that depends only on an interface can be tested on a laptop with a mock or recorded data, with no hardware.
- C. They remove the need for tests.
- D. They reduce flash use.

<details>
<summary>Answer</summary>

**B.** Testability is one of the main payoffs of layering. **A** and **D** are not effects of interfaces. **C** is backwards: interfaces make tests possible, not unnecessary.

</details>

---

## What You Can Now Do, and What Comes Next

- Recognise when a product needs OTA, tasks, ESP-IDF, TLS, BLE, deep sleep or tests.
- Weigh each one's benefit against its cost.

The idea to carry forward: **each of these topics solves a problem version 1 does not yet have.** Add them when a requirement calls for one, not before.

This completes the firmware module. Module 4 turns to the physical product, starting with [D0 — Form Factor and Concept](../04-mechanical-3d-design/D0-form-factor-and-concept.md).

---

## References

1. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): Over The Air Updates (OTA)* (OTA data partition, safe update mode, application rollback). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/ota.html
2. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): FreeRTOS Overview*. https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/freertos.html
3. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): Get Started*. https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/index.html
4. Eclipse Mosquitto. *test.mosquitto.org* (port 1883 unencrypted; 8883 encrypted; "anybody could be listening"). https://test.mosquitto.org/
5. Seeed Studio. *Getting Started with Seeed Studio XIAO ESP32C3* (deep sleep about 44 µA; light sleep about 4 mA with WiFi and 10 mA with BLE). https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/
6. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): Sleep Modes* (light sleep preserves state; deep sleep powers off most RAM; deep-sleep GPIO wake-up only from pins in the VDD3P3_RTC domain). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/sleep_modes.html
7. PlatformIO. *Unit Testing* (run the same tests on the host machine or on boards). https://docs.platformio.org/en/latest/advanced/unit-testing/index.html
