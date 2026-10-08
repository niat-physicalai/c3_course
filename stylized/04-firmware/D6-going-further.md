<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">D6 — Going Further (Reading Only)</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Six Topics Beyond This Course, and When You Would Need Them</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 4 — Firmware <strong>Time:</strong> ~30 minutes · <strong>You will produce:</strong> answers to the check questions at the end</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What a Product Needs After Version 1</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Your firmware does what version 1 needs. A product that ships to hundreds of people, lasts for years or handles private data will need more. You will not build these six topics here. You only need to recognise when your product needs one.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Recognise</strong> which of these six topics a given product requirement calls for.</li><li style="margin:6px 0;">​<strong>Explain</strong> each topic's main benefit and its main cost in one or two sentences.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">1. Over-the-Air (OTA) Updates</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>What it is.</strong> The device downloads new firmware over the network and installs it itself. ESP-IDF's OTA system stores the new firmware alongside the running one, tracks which version is valid, and can <strong>roll back</strong> to the previous version if the new one fails to start properly [1].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>When you need it.</strong> As soon as devices are in other people's hands. Without OTA, every bug fix means collecting devices and plugging them into a laptop.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The cost.</strong> Twice the flash space for firmware, a secure way to deliver updates, and a plan for what happens when an update fails halfway, for example on a flat battery.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">2. FreeRTOS Tasks and Queues</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>What it is.</strong> The ESP32's software already runs on <strong>FreeRTOS</strong>, a small real-time operating system [2]. Instead of one loop() checking every task in turn (D2), you can create separate <strong>tasks</strong> that each run their own loop, and pass data between them through <strong>queues</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>When you need it.</strong> When jobs genuinely need to run independently: for example, a network task that may wait for seconds should not hold up a sensor task that must run every 20 ms.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The cost.</strong> New kinds of bugs: two tasks using the same variable at once, a task starving another of processor time, stack sizes to choose for each task. D2's single-loop approach avoids all of these, which is why it is the right place to start.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">3. ESP-IDF Instead of Arduino</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>What it is.</strong> <strong>ESP-IDF</strong> is Espressif's own development framework, which the Arduino core for ESP32 is built on top of [3]. It gives direct access to every chip feature and configuration option.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>When you need it.</strong> When you need something the Arduino layer hides or does not expose, such as fine control of power management, security features, or build configuration.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The cost.</strong> More setup, more code for simple things, and fewer beginner-friendly libraries. Many products stay on Arduino successfully; some move to ESP-IDF once they need its control.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">4. MQTT With TLS</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>What it is.</strong> The D4 sketch sends MQTT unencrypted on port 1883, and the public test broker warns that "anybody could be listening" [4]. <strong>TLS</strong> encrypts the connection, and certificates prove the broker, and optionally the device, are who they claim to be. The same test broker offers encrypted ports, such as 8883, for practice [4].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>When you need it.</strong> Whenever the data is private, such as heart rate (A2), or whenever someone could send your device a malicious command.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The cost.</strong> More memory and processing, certificates to install and eventually renew, and more time connecting, which matters for battery life.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">5. BLE as an Alternative to WiFi</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>What it is.</strong> <strong>Bluetooth Low Energy</strong> connects the watch to a phone nearby, and the phone relays data to the internet if needed. The ESP32-C3 supports it alongside WiFi.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>When you need it.</strong> For a wearable that syncs often with a phone the wearer always carries (A1's connection choice). BLE generally uses less power than WiFi for small, frequent transfers, and it does not need the wearer's WiFi password.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The cost.</strong> A phone app, which is a second product to design, build and maintain.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Which radio uses less power depends on how often and how much the device sends. Your B3 current budget answers that.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Sleep modes are no longer here.</div><div>Modem, light and deep sleep are core to battery life, so they are taught in <a href="D2-non-blocking-logic-and-sleep.md">D2 — Non-Blocking Logic and Sleep Modes</a>, Part 4.</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">6. Unit Testing Embedded Code</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>What it is.</strong> Small automated tests that check one function at a time, such as "does the step counter count 10 steps from this recorded acceleration data?". PlatformIO can run the same tests on your laptop (<strong>native</strong>) or on a real board [5].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>When you need it.</strong> As soon as you change code that already works. A test catches the change that quietly breaks step counting before anyone wears the watch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The cost.</strong> Writing the tests, and designing code that can be tested. D0's layers and B5's mock sensor class help here: a step counter that depends only on an interface can be tested on a laptop with recorded data and no hardware at all.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The reference watch's firmware (esp\_watch.ino in the repository's Arduino-IDE folder, with a PlatformIO version alongside) covers three screens, animations, two buttons, steps, heart rate and a WiFi weather fetch. The topics above describe where such a sketch goes next: structured into modules (D0), then tested, secured and made updatable.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For your own product, pick the <strong>two</strong> topics above that version 2 would need first. For each, write one sentence naming the requirement that calls for it, and one sentence naming its main cost. Add both to your capstone's "what I would change in v2" page.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. You picked exactly two topics. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Each topic names a requirement from your A0 spec that calls for it. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Each topic names its main cost in one sentence. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Neither topic is something your version 1 already needs to work. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Both are added to your capstone's "what I would change in v2" page. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Each cost sentence names a concrete cost, such as flash, memory, battery, a phone app or new bugs, not just "more complexity". — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. You answered all five check questions before opening any answer. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. You scored at least 4 out of 5 on the check questions. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A watch will be given to 200 students for a semester. A bug is found in week 3. Which topic would have made fixing it simplest?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. BLE</li><li style="margin:6px 0;">B. Over-the-air updates</li><li style="margin:6px 0;">C. Deep sleep</li><li style="margin:6px 0;">D. Unit testing</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> OTA delivers the fix to every device without collecting them. <strong>D</strong> might have caught the bug earlier, but it does not help once devices are deployed. <strong>A</strong> and <strong>C</strong> are unrelated to updating firmware.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A network request sometimes waits for several seconds, and the motion sensor must still be read every 20 ms. Which approach separates the two most cleanly?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A longer watchdog timeout</li><li style="margin:6px 0;">B. Running the network work in its own FreeRTOS task, passing results through a queue</li><li style="margin:6px 0;">C. Reading the sensor less often</li><li style="margin:6px 0;">D. Using deep sleep</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Separate tasks let the slow job wait without holding up the fast one. <strong>A</strong> hides the symptom. <strong>C</strong> changes the requirement. <strong>D</strong> stops everything.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A watch sends heart-rate readings to a cloud broker. Which topic addresses the privacy risk?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. MQTT with TLS</li><li style="margin:6px 0;">B. FreeRTOS</li><li style="margin:6px 0;">C. ESP-IDF</li><li style="margin:6px 0;">D. Unit testing</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> TLS encrypts the data in transit and verifies the broker. <strong>B</strong>, <strong>C</strong> and <strong>D</strong> do not protect the data on the network.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A wearable sends step counts every few minutes to a phone the wearer always carries. The hostel WiFi needs a login page. Which option fits best, and what does it cost?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. WiFi with MQTT; no extra cost</li><li style="margin:6px 0;">B. BLE to the phone; a phone app to design, build and maintain</li><li style="margin:6px 0;">C. BLE to the phone; twice the flash space</li><li style="margin:6px 0;">D. ESP-IDF instead of Arduino; more setup</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> BLE suits frequent small transfers to a nearby phone and needs no WiFi password. Its main cost is the phone app. <strong>A</strong> fails at the login page. <strong>C</strong> gives OTA's cost. <strong>D</strong> does not choose a radio.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> You want to test your step counter on your laptop against recorded accelerometer data, with no board attached. What must be true of the step-counting code?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. It reads samples by calling Wire directly.</li><li style="margin:6px 0;">B. It gets samples through an interface, so a test can feed it recorded data.</li><li style="margin:6px 0;">C. It runs in its own FreeRTOS task.</li><li style="margin:6px 0;">D. It is built with ESP-IDF.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A service that depends only on an interface can be given a mock or recorded data. <strong>A</strong> ties the code to real hardware. <strong>C</strong> and <strong>D</strong> do not affect whether the code can run without a board.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This completes the firmware module. Module 5 turns to the enclosure, starting with <a href="../05-mechanical-3d-design/E0-parametric-cad-fundamentals.md">E0 — Parametric CAD Fundamentals</a>.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Espressif Systems. ESP-IDF Programming Guide (ESP32-C3): Over The Air Updates (OTA) (OTA data partition, safe update mode, application rollback). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/ota.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Espressif Systems. ESP-IDF Programming Guide (ESP32-C3): FreeRTOS Overview. https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/freertos.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Espressif Systems. ESP-IDF Programming Guide (ESP32-C3): Get Started. https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/index.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Eclipse Mosquitto. test.mosquitto.org (port 1883 unencrypted; 8883 encrypted; "anybody could be listening"). https://test.mosquitto.org/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. PlatformIO. Unit Testing (run the same tests on the host machine or on boards). https://docs.platformio.org/en/latest/advanced/unit-testing/index.html</div>
