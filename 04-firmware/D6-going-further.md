# D6 — Going Further (Reading Only)
## Six Topics Beyond This Course, and When You Would Need Them

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Firmware
**Time:** ~30 minutes · **You will produce:** answers to the check questions at the end

---

### What a Product Needs After Version 1

Your firmware does what version 1 needs. A product that ships to hundreds of people, lasts for years or handles private data will need more. You will not build these six topics here. You only need to recognise when your product needs one.

### What You Will Be Able to Do After This Reading

- **Recognise** which of these six topics a given product requirement calls for.
- **Explain** each topic's main benefit and its main cost in one or two sentences.

---

## 1. Over-the-Air (OTA) Updates

**What it is.** The device downloads new firmware over the network and installs it itself. ESP-IDF's OTA system stores the new firmware alongside the running one, tracks which version is valid, and can **roll back** to the previous version if the new one fails to start properly [1].

**When you need it.** As soon as devices are in other people's hands. Without OTA, every bug fix means collecting devices and plugging them into a laptop.

**The cost.** Twice the flash space for firmware, a secure way to deliver updates, and a plan for what happens when an update fails halfway, for example on a flat battery.

## 2. FreeRTOS Tasks and Queues

**What it is.** The ESP32's software already runs on **FreeRTOS**, a small real-time operating system [2]. Instead of one `loop()` checking every task in turn (D2), you can create separate **tasks** that each run their own loop, and pass data between them through **queues**.

**When you need it.** When jobs genuinely need to run independently: for example, a network task that may wait for seconds should not hold up a sensor task that must run every 20 ms.

**The cost.** New kinds of bugs: two tasks using the same variable at once, a task starving another of processor time, stack sizes to choose for each task. D2's single-loop approach avoids all of these, which is why it is the right place to start.

## 3. ESP-IDF Instead of Arduino

**What it is.** **ESP-IDF** is Espressif's own development framework, which the Arduino core for ESP32 is built on top of [3]. It gives direct access to every chip feature and configuration option.

**When you need it.** When you need something the Arduino layer hides or does not expose, such as fine control of power management, security features, or build configuration.

**The cost.** More setup, more code for simple things, and fewer beginner-friendly libraries. Many products stay on Arduino successfully; some move to ESP-IDF once they need its control.

## 4. MQTT With TLS

**What it is.** The D4 sketch sends MQTT unencrypted on port 1883, and the public test broker warns that "anybody could be listening" [4]. **TLS** encrypts the connection, and certificates prove the broker, and optionally the device, are who they claim to be. The same test broker offers encrypted ports, such as 8883, for practice [4].

**When you need it.** Whenever the data is private, such as heart rate (A2), or whenever someone could send your device a malicious command.

**The cost.** More memory and processing, certificates to install and eventually renew, and more time connecting, which matters for battery life.

## 5. BLE as an Alternative to WiFi

**What it is.** **Bluetooth Low Energy** connects the watch to a phone nearby, and the phone relays data to the internet if needed. The ESP32-C3 supports it alongside WiFi.

**When you need it.** For a wearable that syncs often with a phone the wearer always carries (A1's connection choice). BLE generally uses less power than WiFi for small, frequent transfers, and it does not need the wearer's WiFi password.

**The cost.** A phone app, which is a second product to design, build and maintain.

<!-- REFPRODUCT:START -->
Which radio uses less power depends on how often and how much the device sends. Your B3 current budget answers that.
<!-- REFPRODUCT:END -->

> **Sleep modes are no longer here.** Modem, light and deep sleep are core to battery life, so they are taught in [D2 — Non-Blocking Logic and Sleep Modes](D2-non-blocking-logic-and-sleep.md), Part 4.

## 6. Unit Testing Embedded Code

**What it is.** Small automated tests that check one function at a time, such as "does the step counter count 10 steps from this recorded acceleration data?". PlatformIO can run the same tests on your laptop (**native**) or on a real board [5].

**When you need it.** As soon as you change code that already works. A test catches the change that quietly breaks step counting before anyone wears the watch.

**The cost.** Writing the tests, and designing code that can be tested. D0's layers and B5's mock sensor class help here: a step counter that depends only on an interface can be tested on a laptop with recorded data and no hardware at all.

<!-- REFPRODUCT:START -->
The reference watch's firmware (`esp_watch.ino` in the repository's Arduino-IDE folder, with a PlatformIO version alongside) covers three screens, animations, two buttons, steps, heart rate and a WiFi weather fetch. The topics above describe where such a sketch goes next: structured into modules (D0), then tested, secured and made updatable.
<!-- REFPRODUCT:END -->

<!-- ASSET: public repo firmware/Arduino-IDE/esp_watch.ino -->

---

# Putting It All Together

## Applying What You Have Learned

For your own product, pick the **two** topics above that version 2 would need first. For each, write one sentence naming the requirement that calls for it, and one sentence naming its main cost. Add both to your capstone's "what I would change in v2" page.

## Self-Check

1. You picked exactly two topics. — Y/N
2. Each topic names a requirement from your A0 spec that calls for it. — Y/N
3. Each topic names its main cost in one sentence. — Y/N
4. Neither topic is something your version 1 already needs to work. — Y/N
5. Both are added to your capstone's "what I would change in v2" page. — Y/N
6. Each cost sentence names a concrete cost, such as flash, memory, battery, a phone app or new bugs, not just "more complexity". — Y/N
7. You answered all five check questions before opening any answer. — Y/N
8. You scored at least 4 out of 5 on the check questions. — Y/N

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

**4.** A wearable sends step counts every few minutes to a phone the wearer always carries. The hostel WiFi needs a login page. Which option fits best, and what does it cost?

- A. WiFi with MQTT; no extra cost
- B. BLE to the phone; a phone app to design, build and maintain
- C. BLE to the phone; twice the flash space
- D. ESP-IDF instead of Arduino; more setup

<details>
<summary>Answer</summary>

**B.** BLE suits frequent small transfers to a nearby phone and needs no WiFi password. Its main cost is the phone app. **A** fails at the login page. **C** gives OTA's cost. **D** does not choose a radio.

</details>

**5.** You want to test your step counter on your laptop against recorded accelerometer data, with no board attached. What must be true of the step-counting code?

- A. It reads samples by calling `Wire` directly.
- B. It gets samples through an interface, so a test can feed it recorded data.
- C. It runs in its own FreeRTOS task.
- D. It is built with ESP-IDF.

<details>
<summary>Answer</summary>

**B.** A service that depends only on an interface can be given a mock or recorded data. **A** ties the code to real hardware. **C** and **D** do not affect whether the code can run without a board.

</details>

---

## What Comes Next

This completes the firmware module. Module 5 turns to the enclosure, starting with [E0 — Parametric CAD Fundamentals](../05-mechanical-3d-design/E0-parametric-cad-fundamentals.md).

---

## References

1. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): Over The Air Updates (OTA)* (OTA data partition, safe update mode, application rollback). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/ota.html
2. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): FreeRTOS Overview*. https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/freertos.html
3. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): Get Started*. https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/index.html
4. Eclipse Mosquitto. *test.mosquitto.org* (port 1883 unencrypted; 8883 encrypted; "anybody could be listening"). https://test.mosquitto.org/
5. PlatformIO. *Unit Testing* (run the same tests on the host machine or on boards). https://docs.platformio.org/en/latest/advanced/unit-testing/index.html
