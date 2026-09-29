# D5 — Debugging and Robustness
## Making Failures Visible, Understandable and Recoverable

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Firmware
**Time:** ~1 hour · **You will produce:** a completed "spot the bug" exercise set

---

### "It Just Restarts Sometimes"

Every embedded project reaches this stage. The watch works, then one day it resets on its own. Or the screen goes blank and stays blank. Or it freezes until someone presses reset. "It just restarts sometimes" is not a bug report. It is the sound of firmware that cannot tell you what went wrong.

<!-- REFPRODUCT:START -->
Not every apparent crash is a crash. During esp_watch's development the screen went blank after 15 seconds with no button wired, and it looked exactly like the watch had died. It was the screen-sleep timeout doing its job. The fix, for testing, was to set the timeout to zero. The lesson is to find out *what* happened before deciding *why*.
<!-- REFPRODUCT:END -->

This unit gives you the tools to find out: logging that is useful rather than noisy, reading the ESP32's crash report, recognising the four failures that account for most real-world trouble, and the defensive habits, such as a watchdog, timeouts and retries, that turn a hang into a recovery.

### What You Will Be Able to Do After This Reading

- **Use** log levels so that serial output helps rather than floods.
- **Read** an ESP32 crash report, and **decode** its backtrace to a line of code.
- **Diagnose** the four common failures: brownout, stack overflow, watchdog reset and a blocking network call.
- **Apply** a hardware watchdog, and timeouts and retries on every bus and network operation.
- **Identify** the defect in a broken sketch from its symptoms.

### What Part 1 Already Covered

Part 1 taught serial-monitor debugging and systematic troubleshooting: isolate one layer at a time, change one thing at a time. **What is new here** is debugging a device that must run unattended: structured log levels, reading a crash dump, recognising reset reasons, and code that recovers by itself when something external fails.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## Logging With Levels

`Serial.println("here")` scattered through code works for five minutes. After that there is too much output to read, and you delete it all just before you need it again. **Log levels** fix this. Every message gets a level, and one setting decides which levels are printed:

| Level | Use for | Example |
|---|---|---|
| Error | Something failed and a feature is not working | "motion sensor not answering" |
| Warning | Something unexpected, but the device carried on | "WiFi retry 3, waiting 8 s" |
| Info | Normal milestones worth knowing | "boot, reset reason: brownout" |
| Debug | Detail for chasing a specific problem | "attempt 2 failed" |

Normally you run at *Info*: quiet unless something notable happens. When chasing a bug, switch to *Debug* for the module involved, then switch back. The messages stay in the code, ready for next time.

The provided sketch [`assets/code/D5-robust-basics.ino`](../assets/code/D5-robust-basics.ino) defines four macros that add the level and the function name to every line, and start it with `#` so it never corrupts a data stream (D3):

```cpp
#define LOG(lvl, tag, fmt, ...) \
  do { if ((lvl) <= LOG_LEVEL) Serial.printf("# [%s] %s: " fmt "\n", tag, __func__, ##__VA_ARGS__); } while (0)
#define LOGE(fmt, ...) LOG(LVL_ERROR, "E", fmt, ##__VA_ARGS__)
#define LOGW(fmt, ...) LOG(LVL_WARN,  "W", fmt, ##__VA_ARGS__)
```

A line of output then reads `# [W] loop: motion sensor not answering (3 failures)`, which tells you how serious it is, where it came from and what happened.

## The First Thing to Log: Why Did I Restart?

The ESP32 records why it last reset, and `esp_reset_reason()` returns it. Log it at every boot:

```cpp
esp_reset_reason_t why = esp_reset_reason();
LOGI("boot, reset reason: %s", resetReasonName(why));
if (why == ESP_RST_BROWNOUT) LOGW("last reset was a brownout: check battery and current peaks");
```

This single line turns "it restarts sometimes" into "it restarted because of a brownout" or "because of the task watchdog", which points directly at one of the four failures below.

## Reading a Crash Report

When the ESP32-C3 hits a fatal error, such as reading through a null pointer, its **panic handler** prints a report and restarts [1]. The report starts like this:

```text
Guru Meditation Error: Core 0 panic'ed (Load access fault). Exception was unhandled.

Core  0 register dump:
MEPC    : 0x42006686  RA      : 0x42006692  SP      : 0x3fc8f2f0  ...
...
MCAUSE  : 0x00000005  MTVAL   : 0x00000000
```

Three parts matter:

1. **The cause, in brackets.** Here, *Load access fault*: the program tried to read from an invalid address.
2. **`MTVAL`**, the address that was accessed. Espressif's guide explains that if it is zero, the program most likely dereferenced a null pointer; if it is close to zero, it probably accessed a member of a structure through a null pointer [1].
3. **`MEPC`** and the **backtrace**: the address of the instruction that failed, and the chain of calls that led there.

The addresses mean nothing on their own. A **decoder** turns them into function names and line numbers using the compiled program. Espressif's own monitor does this automatically [1], and PlatformIO's serial monitor has an `esp32_exception_decoder` filter that does the same [2]. Add `monitor_filters = esp32_exception_decoder` to `platformio.ini`, and the backtrace arrives as something like:

```text
0x42006686 in bar (ptr=0x0) at src/main.cpp:18
#1  0x42006692 in foo () at src/main.cpp:22
#2  0x420066ac in loop () at src/main.cpp:28
```

Read the top line first: that is where it failed. The lines below show how it got there.

<!-- MEDIA
type: screenshot
id: D5-01
caption: A crash report decoded by PlatformIO's exception decoder
brief: VS Code with the PlatformIO serial monitor open, showing a real ESP32-C3 panic from a
  deliberately broken sketch that dereferences a null pointer. Visible: the "Guru Meditation
  Error ... (Load access fault)" line, the register dump with MEPC and MTVAL (0x00000000)
  highlighted, and below it the decoded backtrace lines naming the function and the line
  in main.cpp. platformio.ini visible in an editor tab with "monitor_filters =
  esp32_exception_decoder" highlighted.
-->

---

## The Four Things That Actually Go Wrong

Most unexplained resets and freezes on a small connected device come from four causes. Learn their symptoms.

| Failure | What it is | What you see | Typical cause |
|---|---|---|---|
| **Brownout** | The supply voltage drops below a safe level, and the chip resets itself [1] | "Brownout detector was triggered", often cut short; reset reason *brownout* | Weak battery plus a current peak, typically WiFi transmitting |
| **Stack overflow** | A function uses more stack memory than its task has | "Stack protection fault" or similar panic [1] | Large local arrays, deep recursion |
| **Watchdog reset** | Code stopped returning to the scheduler for too long | Reset reason *task watchdog* or *interrupt watchdog* | A loop waiting for hardware with no timeout |
| **Blocking network call** | The program waits on the network with no limit | Freeze, often followed by a watchdog reset | Connecting or requesting with no timeout |

### Brownout

<!-- REFPRODUCT:START -->
B5 showed how a battery's internal resistance makes its voltage dip during a current burst, and esp_watch's modelled WiFi burst is about 100 mA against a few milliamps asleep. A cell that looks fine at rest can dip far enough during a WiFi connection to trip the brownout detector. The symptom is a reset exactly when WiFi starts, more often as the battery runs down.
<!-- REFPRODUCT:END -->

The fix is not in the firmware alone: check the battery voltage before heavy operations (B3's battery sense), avoid starting WiFi on a low battery, and give the regulator enough input headroom. Never simply disable the brownout detector to "fix" the resets. It exists to stop the chip running on a supply too low for it to work correctly.

### Stack Overflow

Each task has a fixed amount of **stack** memory for its local variables and function calls. A large local array, such as a 16 kB buffer declared inside a function, can use it up in one go. The ESP32-C3 has a hardware stack guard that catches this and reports a "Stack protection fault" [1]. Move large buffers to global or `static` storage, and avoid recursion.

### Watchdog Reset

A **watchdog** is a timer that resets the chip unless the program checks in regularly. If your code gets stuck, the watchdog notices and restarts the device, which is far better than a watch that is frozen until its battery dies.

```cpp
// Watchdog: if loop() stops coming back for WDT_TIMEOUT_S, the chip resets.
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  esp_task_wdt_config_t cfg = {WDT_TIMEOUT_S * 1000, 0, true};
  esp_task_wdt_reconfigure(&cfg);
#else
  esp_task_wdt_init(WDT_TIMEOUT_S, true);
#endif
  esp_task_wdt_add(NULL);                      // watch this task (loop)

void loop() {
  esp_task_wdt_reset();                        // "I'm still alive"
  // ...
}
```

The two branches exist because the watchdog API changed between versions of the ESP32 Arduino core. The sketch was compiled with core 2.0.17. The version-3 branch follows the newer ESP-IDF 5 interface.

Choose the timeout from your worst loop time (D2): long enough never to trigger in normal operation, short enough that a hang is caught quickly. Seconds, not milliseconds.

A watchdog is not a fix. It turns a hang into a reset, and the reset reason tells you it happened. You still have to find the loop that got stuck.

> **Try it: Trigger the watchdog.** Run the D5 sketch on a board or in Wokwi.
> 1. **Predict.** What will the next boot's reset reason be after you type `h`?
> 2. **Do.** Type `h` into the serial monitor to start an endless loop. Wait, and read the next boot message.
> 3. **Explain.** How long did it take to reset? What would the watch have done without the watchdog?

<!-- MEDIA
type: screenshot
id: D5-02
caption: The watchdog at work: a simulated hang, a reset, and the reason logged on the next boot
brief: Serial monitor (Wokwi or Arduino IDE) running D5-robust-basics.ino on an ESP32-C3.
  Lines visible in order: "# [I] setup: boot, reset reason: power on", a few normal lines,
  "# [E] loop: simulating a hang" after typing h, a gap of about 5 seconds, the ESP32 boot
  messages, then "# [I] setup: boot, reset reason: task watchdog". Highlight the two
  reset-reason lines. Crop to the serial output.
-->

### Blocking Network Call

D4 made the connection non-blocking. The same rule applies to every network operation: an HTTP request, a DNS lookup, a TLS handshake. Every one needs a **timeout**, and failure must lead to a retry with backoff, not a wait.

## Defensive Coding Around Every External Dependency

Anything outside your code can fail: a sensor, the bus, the network, the server. For each one, answer three questions:

1. **How long will I wait?** Set a timeout. The ESP32 `Wire` library defaults to 50 ms per I²C transaction, and `Wire.setTimeOut()` changes it.
2. **How many times will I try?** Retry a small, fixed number of times.
3. **What happens if it still fails?** Report it, degrade gracefully (A2), and try again later.

```cpp
// Read one register, with a bounded number of retries. Never hangs:
// Wire has its own timeout, and we give up after RETRIES attempts.
bool readRegister(uint8_t addr, uint8_t reg, uint8_t &value) {
  const int RETRIES = 3;
  for (int attempt = 1; attempt <= RETRIES; attempt++) {
    Wire.beginTransmission(addr);
    Wire.write(reg);
    if (Wire.endTransmission(false) == 0 && Wire.requestFrom(addr, (uint8_t)1) == 1) {
      value = Wire.read();
      return true;
    }
    LOGD("attempt %d failed", attempt);
  }
  return false;
}
```

<!-- REFPRODUCT:START -->
The reference watch's bench testing shows why the failure path matters. With the motion sensor's AD0 pin floating, between 6% and 80% of reads failed, and the sensor came and went between scans. Firmware that assumed every read succeeded would have produced nonsense step counts with no warning. Firmware that counts failures and logs a warning makes the fault visible on the first day.
<!-- REFPRODUCT:END -->

---

# Putting It All Together

## Applying What You Have Learned: Spot the Bug

This exercise set is your deliverable. For each sketch fragment, name the defect, the symptom it would produce, and the fix. Write your answers before opening each solution.

**Bug 1.**

```cpp
void loop() {
  while (!imuDataReady()) { }      // wait for the sensor
  readImu();
}
```

<details>
<summary>Diagnosis</summary>

The `while` loop waits for hardware with **no timeout**. If the sensor stops responding, the loop never exits, the watchdog resets the chip (or, without a watchdog, the watch freezes). Fix: check `imuDataReady()` once per pass and read when it is true; count how long it has been false and report a fault after a limit.

</details>

**Bug 2.**

```cpp
void logSession() {
  char buffer[20000];              // hold a whole session
  // ... fill and send buffer ...
}
```

<details>
<summary>Diagnosis</summary>

A 20 kB **local** array lives on the task's stack, which is far smaller, so this is a **stack overflow**, reported as a stack protection fault. Fix: make the buffer `static` or global, or stream the data in small pieces.

</details>

**Bug 3.** The watch resets every time it connects to WiFi, but only after it has been off the charger for a few hours. The reset reason is *brownout*.

<details>
<summary>Diagnosis</summary>

The WiFi current burst pulls a partly discharged cell's voltage below the brownout threshold. It is a power problem that shows up in firmware. Fix: read the battery voltage before starting WiFi and skip or postpone the connection below a threshold; review the power path's headroom (B3, B5). Do not disable the brownout detector.

</details>

**Bug 4.**

```cpp
void loop() {
  http.begin(client, "http://example.com/weather");
  int code = http.GET();           // no timeout set
  // ...
}
```

<details>
<summary>Diagnosis</summary>

A **blocking network call** in `loop()`, repeated every pass, with no timeout. When the network is slow or absent, the loop stalls for as long as the call waits. Fix: set a timeout on the request, run it only when due (for example once per hour, as esp_watch fetches weather only at boot), and use the backoff pattern from D4 on failure.

</details>

**Bug 5.** A crash report shows `Load access fault` with `MTVAL : 0x00000008`.

<details>
<summary>Diagnosis</summary>

`MTVAL` holds the address that was accessed. A value close to zero means the program most likely accessed a **member of a structure through a null pointer**, at an offset of 8 bytes [1]. Fix: decode the backtrace to find the line, and check that the pointer is valid before using it, for example a driver object that failed to initialise.

</details>

**Bug 6.**

```cpp
bool ok = display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
// ok is never checked; later:
if (busLooksHealthy()) { ... }     // implemented as "last display write succeeded"
```

<details>
<summary>Diagnosis</summary>

Two problems. The start-up result is ignored, so a missing display goes unreported. And bus health is judged by **display writes**, which cannot detect a broken bus, since nothing is read back. This is exactly the trap esp_watch fell into when the green heart-rate module clamped the bus. Fix: check `begin()`'s result and log it; judge bus health by a device you read from, such as the motion sensor's identity register.

</details>

## Self-Check

Open your exercise answers and your own sketch, and answer each item Y or N.

1. Every one of the six bugs has a defect, a symptom and a fix written. — Y/N
2. Your sketch logs the reset reason at every boot. — Y/N
3. Your log messages use at least three levels, set by one setting. — Y/N
4. Every log message starts with `#`, so it cannot corrupt a data stream. — Y/N
5. Your sketch enables a watchdog and resets it in `loop()`. — Y/N
6. Every I²C transaction has a timeout and a bounded number of retries. — Y/N
7. Every network operation has a timeout. — Y/N
8. No local variable in your sketch is larger than about 1 kB. — Y/N

---

## Check Your Understanding

**1.** A device resets only when WiFi starts, and more often as the battery runs down. What is the most likely cause?

- A. A stack overflow in the WiFi library
- B. A brownout: the WiFi current burst drops a weakening battery below the safe voltage
- C. A watchdog timeout
- D. A null pointer

<details>
<summary>Answer</summary>

**B.** The link to both WiFi start-up and battery level points to supply voltage. Logging the reset reason would confirm *brownout*. **A** would not depend on the battery level. **C** would show a watchdog reset reason and would be linked to a hang, not to battery level. **D** would crash regardless of the battery.

</details>

**2.** What does a watchdog do for a device that occasionally gets stuck?

- A. Prevents the code from getting stuck.
- B. Resets the device when the code stops checking in, turning a permanent freeze into a recovery, and records the reason.
- C. Finds the bug automatically.
- D. Speeds up the loop.

<details>
<summary>Answer</summary>

**B.** It limits the damage and leaves evidence. **A** and **C** overstate it: the code still gets stuck, and you still have to find why. **D** is unrelated.

</details>

**3.** A crash report's backtrace is a list of hexadecimal addresses. What turns it into something useful?

- A. Converting the addresses to decimal
- B. A decoder, such as PlatformIO's `esp32_exception_decoder` filter, which maps addresses to function names and line numbers using the compiled program
- C. Restarting the device
- D. Increasing the baud rate

<details>
<summary>Answer</summary>

**B.** The addresses only have meaning together with the program that produced them. **A** changes the notation, not the meaning. **C** and **D** do not interpret anything.

</details>

**4.** Why start every log message with `#`?

- A. It is required by the ESP32.
- B. Parsers of the data stream (D3) skip lines starting with `#`, so logging never corrupts recorded data.
- C. It makes the log shorter.
- D. It makes the device run faster.

<details>
<summary>Answer</summary>

**B.** It keeps the debug channel and the data channel separable on the same serial port. **A**, **C** and **D** are not true.

</details>

**5.** A screen goes blank after 15 seconds during testing, and a student starts reading crash reports. What should they check first?

- A. The stack size
- B. Whether the device actually reset (for example, a new boot message), because a blank screen may be a designed behaviour, such as a screen timeout
- C. The brownout threshold
- D. The WiFi password

<details>
<summary>Answer</summary>

**B.** First establish *what* happened. The reference watch's "crash" was its screen-sleep timeout. **A**, **C** and **D** assume a fault that has not been shown to exist.

</details>

---

## What You Can Now Do, and What Comes Next

- Log with levels and record the reason for every reset.
- Read a crash report and decode it to a line of code.
- Recognise brownout, stack overflow, watchdog reset and blocking calls from their symptoms.
- Wrap every external dependency in a timeout, a bounded retry and a failure path.

The idea to carry forward: **every failure should leave evidence.** A reset reason, a log line and a counter are what turn "it restarts sometimes" into a bug you can fix.

[D6 — Going Further](D6-going-further.md) is a short reading-only tour of topics beyond this course: over-the-air updates, FreeRTOS tasks, ESP-IDF, secure MQTT, BLE, deep sleep and testing embedded code.

---

## References

1. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): Fatal Errors* (panic handler output, register dump with MEPC and MTVAL, backtrace decoding, brownout detector message, hardware stack guard "Stack protection fault"). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-guides/fatal-errors.html
2. PlatformIO. *pio device monitor* (`esp32_exception_decoder` filter, "decodes crash exception"). https://docs.platformio.org/en/latest/core/userguide/device/cmd_monitor.html

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
