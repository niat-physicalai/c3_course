<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">D5 — Debugging and Robustness</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Making Failures Visible, Understandable and Recoverable</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 4 — Firmware <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a completed "spot the bug" exercise set</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">"It Just Restarts Sometimes"</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The watch works, then one day it resets on its own, or its screen goes blank, or it freezes. "It just restarts sometimes" is not a bug report.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Not every apparent crash is a crash. During esp\_watch's development the screen went blank after 15 seconds with no button wired, and it looked exactly like the watch had died. It was the screen-sleep timeout doing its job. The fix, for testing, was to set the timeout to zero. The lesson is to find out what happened before deciding why.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Use</strong> log levels so that serial output helps rather than floods.</li><li style="margin:6px 0;">​<strong>Read</strong> an ESP32 crash report, and <strong>decode</strong> its backtrace to a line of code.</li><li style="margin:6px 0;">​<strong>Diagnose</strong> the four common failures: brownout, stack overflow, watchdog reset and a blocking network call.</li><li style="margin:6px 0;">​<strong>Apply</strong> a hardware watchdog, and timeouts and retries on every bus and network operation.</li><li style="margin:6px 0;">​<strong>Identify</strong> the defect in a broken sketch from its symptoms.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 taught serial-monitor debugging. This unit is about debugging a device that must run unattended.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Logging With Levels</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Serial.println("here") scattered through code works for five minutes. After that there is too much output to read, and you delete it all just before you need it again. <strong>Log levels</strong> fix this. Every message gets a level, and one setting decides which levels are printed:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Level</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Use for</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Example</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Error</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Something failed and a feature is not working</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"motion sensor not answering"</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Warning</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Something unexpected, but the device carried on</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"WiFi retry 3, waiting 8 s"</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Info</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Normal milestones worth knowing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"boot, reset reason: brownout"</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Debug</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Detail for chasing a specific problem</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"attempt 2 failed"</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Normally you run at Info: quiet unless something notable happens. When chasing a bug, switch to Debug for the module involved, then switch back. The messages stay in the code, ready for next time.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The provided sketch <a href="../assets/code/D5-robust-basics.ino">assets/code/D5-robust-basics.ino</a> defines four macros that add the level and the function name to every line, and start it with # so it never corrupts a data stream (D3):</div>

```cpp
#define LOG(lvl, tag, fmt, ...) \
  do { if ((lvl) <= LOG_LEVEL) Serial.printf("# [%s] %s: " fmt "\n", tag, __func__, ##__VA_ARGS__); } while (0)
#define LOGE(fmt, ...) LOG(LVL_ERROR, "E", fmt, ##__VA_ARGS__)
#define LOGW(fmt, ...) LOG(LVL_WARN,  "W", fmt, ##__VA_ARGS__)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A line of output then reads # [W] loop: motion sensor not answering (3 failures), which tells you how serious it is, where it came from and what happened.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The First Thing to Log: Why Did I Restart?</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The ESP32 records why it last reset, and esp\_reset\_reason() returns it. Log it at every boot:</div>

```cpp
esp_reset_reason_t why = esp_reset_reason();
LOGI("boot, reset reason: %s", resetReasonName(why));
if (why == ESP_RST_BROWNOUT) LOGW("last reset was a brownout: check battery and current peaks");
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This single line turns "it restarts sometimes" into "it restarted because of a brownout" or "because of the task watchdog", which points directly at one of the four failures below.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Reading a Crash Report</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">When the ESP32-C3 hits a fatal error, such as reading through a null pointer, its <strong>panic handler</strong> prints a report and restarts [1]. The report starts like this:</div>

```text
Guru Meditation Error: Core 0 panic'ed (Load access fault). Exception was unhandled.

Core  0 register dump:
MEPC    : 0x42006686  RA      : 0x42006692  SP      : 0x3fc8f2f0  ...
...
MCAUSE  : 0x00000005  MTVAL   : 0x00000000
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Three parts matter:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>The cause, in brackets.</strong> Here, Load access fault: the program tried to read from an invalid address.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>MTVAL</strong>, the address that was accessed. Espressif's guide explains that if it is zero, the program most likely dereferenced a null pointer; if it is close to zero, it probably accessed a member of a structure through a null pointer [1].</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>MEPC</strong> and the <strong>stack dump</strong>: MEPC is the address of the instruction that failed. The stack dump is raw memory from which a decoder rebuilds the chain of calls, called the backtrace.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The addresses mean nothing on their own. A <strong>decoder</strong> turns them into function names and line numbers using the compiled program. Espressif's own monitor does this automatically [1], and PlatformIO's serial monitor has an esp32\_exception\_decoder filter that does the same [2]. Add monitor\_filters = esp32\_exception\_decoder to platformio.ini, and the backtrace arrives as something like:</div>

```text
0x42006686 in bar (ptr=0x0) at src/main.cpp:18
#1  0x42006692 in foo () at src/main.cpp:22
#2  0x420066ac in loop () at src/main.cpp:28
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Read the top line first: that is where it failed. The lines below show how it got there.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Four Things That Actually Go Wrong</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Most unexplained resets and freezes on a small connected device come from four causes. Learn their symptoms.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Failure</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it is</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What you see</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Typical cause</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Brownout</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The supply voltage drops below a safe level, and the chip resets itself [1]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Brownout detector was triggered", often cut short; reset reason brownout</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Weak battery plus a current peak, typically WiFi transmitting</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Stack overflow</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A function uses more stack memory than its task has</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"Stack protection fault" or similar panic [1]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Large local arrays, deep recursion</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Watchdog reset</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Code stopped returning to the scheduler for too long</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reset reason task watchdog or interrupt watchdog</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A loop waiting for hardware with no timeout</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Blocking network call</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The program waits on the network with no limit</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Freeze, often followed by a watchdog reset</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connecting or requesting with no timeout</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Brownout</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">B5 showed how a battery's internal resistance makes its voltage dip during a current burst, and esp\_watch's modelled WiFi burst is about 100 mA against a few milliamps asleep. A cell that looks fine at rest can dip far enough during a WiFi connection to trip the brownout detector. The symptom is a reset exactly when WiFi starts, more often as the battery runs down.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The fix is not in the firmware alone: if your design measures the battery (B3 shows how), check it before heavy operations and avoid starting WiFi on a low battery; and give the regulator enough input headroom. Never simply disable the brownout detector to "fix" the resets. It exists to stop the chip running on a supply too low for it to work correctly.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Stack Overflow</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each task has a fixed amount of <strong>stack</strong> memory for its local variables and function calls. A large local array, such as a 16 kB buffer declared inside a function, can use it up in one go. The ESP32-C3 has a hardware stack guard that catches this and reports a "Stack protection fault" [1]. Move large buffers to global or static storage, and avoid recursion.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Watchdog Reset</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A <strong>watchdog</strong> is a timer that resets the chip unless the program checks in regularly. If your code gets stuck, the watchdog notices and restarts the device, which is far better than a watch that is frozen until its battery dies.</div>

```cpp
```cpp
void setup() {
  // ...
  // Watchdog: if loop() stops coming back for WDT_TIMEOUT_S, the chip resets.
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  esp_task_wdt_config_t cfg = {WDT_TIMEOUT_S * 1000, 0, true};
  esp_task_wdt_reconfigure(&cfg);
#else
  esp_task_wdt_init(WDT_TIMEOUT_S, true);
#endif
  esp_task_wdt_add(NULL);                      // watch this task (loop)
}
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">void loop() { esp\_task\_wdt\_reset(); // "I'm still alive" // ... }</div>

```

The two branches exist because the watchdog API changed in version 3 of the ESP32 Arduino core.

Choose the timeout from your worst loop time (D2): long enough never to trigger in normal operation, short enough that a hang is caught quickly. Seconds, not milliseconds.

A watchdog is not a fix. It turns a hang into a reset, and the reset reason tells you it happened. You still have to find the loop that got stuck.

> **Try it: Trigger the watchdog.** Run the D5 sketch in Wokwi.
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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The reference watch's floating AD0 pin (B1) made reads fail at random. Firmware that counts failed reads and logs a warning shows a fault like this on the first day.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned: Spot the Bug</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This exercise set is your deliverable. For each sketch fragment, name the defect, the symptom it would produce, and the fix. Write your answers before opening each solution.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Bug 1.</div>

```cpp
void loop() {
  while (!imuDataReady()) { }      // wait for the sensor
  readImu();
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Diagnosis</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The while loop waits for hardware with <strong>no timeout</strong>. If the sensor stops responding, the loop never exits, the watchdog resets the chip (or, without a watchdog, the watch freezes). Fix: check imuDataReady() once per pass and read when it is true; count how long it has been false and report a fault after a limit.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Bug 2.</div>

```cpp
void logSession() {
  char buffer[20000];              // hold a whole session
  // ... fill and send buffer ...
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Diagnosis</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A 20 kB <strong>local</strong> array lives on the task's stack, which is far smaller, so this is a <strong>stack overflow</strong>, reported as a stack protection fault. Fix: make the buffer static or global, or stream the data in small pieces.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Bug 3.</strong> The watch resets every time it connects to WiFi, but only after it has been off the charger for a few hours. The reset reason is brownout.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Diagnosis</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The WiFi current burst pulls a partly discharged cell's voltage below the brownout threshold. It is a power problem that shows up in firmware. Fix: read the battery voltage before starting WiFi and skip or postpone the connection below a threshold; review the power path's headroom (B3, B5). Do not disable the brownout detector.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Bug 4.</div>

```cpp
void loop() {
  http.begin(client, "http://example.com/weather");
  `  int code = http.GET();           // default timeout, called every pass`
And in the Bug 4 diagnosis, replace "A **blocking network call** in `loop()`, repeated every pass, with no timeout. When the network is slow or absent, the loop stalls for as long as the call waits. Fix: set a timeout on the request, run it only when due (for example once per hour, as esp_watch fetches weather only at boot), and use the backoff pattern from D4 on failure." with:
"A **blocking network call** in `loop()`, repeated every pass. `HTTPClient`'s default timeout is several seconds, so a slow network stalls every pass for that long. Fix: set a short timeout, run the request only when it is due (esp_watch fetches weather once, at boot), and use D4's backoff on failure."
  // ...
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Diagnosis</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>blocking network call</strong> in loop(), repeated every pass, with no timeout. When the network is slow or absent, the loop stalls for as long as the call waits. Fix: set a timeout on the request, run it only when due (for example once per hour, as esp\_watch fetches weather only at boot), and use the backoff pattern from D4 on failure.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Bug 5.</strong> A crash report shows Load access fault with MTVAL : 0x00000008.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Diagnosis</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">MTVAL holds the address that was accessed. A value close to zero means the program most likely accessed a <strong>member of a structure through a null pointer</strong>, at an offset of 8 bytes [1]. Fix: decode the backtrace to find the line, and check that the pointer is valid before using it, for example a driver object that failed to initialise.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Bug 6.</div>

```cpp
bool ok = display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
// ok is never checked; later:
if (busLooksHealthy()) { ... }     // implemented as "last display write succeeded"
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Diagnosis</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two problems. The start-up result is ignored, so a missing display goes unreported. And bus health is judged by <strong>display writes</strong>, which cannot detect a broken bus, since nothing is read back. This is exactly the trap esp\_watch fell into when the green heart-rate module clamped the bus. Fix: check begin()'s result and log it; judge bus health by a device you read from, such as the motion sensor's identity register.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your exercise answers and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every one of the six bugs has a defect, a symptom and a fix written. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Your fix for Bug 1 ends the wait after a set time or number of checks. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Your fix for Bug 2 takes the buffer off the stack (static, global, or streamed in pieces). — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Your answer to Bug 3 adds a battery check before WiFi and does not disable the brownout detector. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Your fix for Bug 4 sets a timeout and runs the request only when it is due. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Your answer to Bug 5 says what a MTVAL value close to zero points to. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Your fix for Bug 6 judges bus health by reading from a device, not by writing to the display. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. You wrote each answer before opening its diagnosis. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A device resets only when WiFi starts, and more often as the battery runs down. What is the most likely cause?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A stack overflow in the WiFi library</li><li style="margin:6px 0;">B. A brownout: the WiFi current burst drops a weakening battery below the safe voltage</li><li style="margin:6px 0;">C. A watchdog timeout</li><li style="margin:6px 0;">D. A null pointer</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The link to both WiFi start-up and battery level points to supply voltage. Logging the reset reason would confirm brownout. <strong>A</strong> would not depend on the battery level. <strong>C</strong> would show a watchdog reset reason and would be linked to a hang, not to battery level. <strong>D</strong> would crash regardless of the battery.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> Your watch used to freeze overnight. After you add a watchdog, it restarts instead, and the next boot logs task watchdog. What is true now?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The bug is fixed.</li><li style="margin:6px 0;">B. Some code still runs longer than the watchdog timeout without returning. You must find that loop.</li><li style="margin:6px 0;">C. The battery is causing brownouts.</li><li style="margin:6px 0;">D. A function is overflowing its stack.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The watchdog turns a freeze into a reset and leaves evidence, but the stuck code is still there. <strong>A</strong> confuses recovery with a fix. <strong>C</strong> and <strong>D</strong> would log brownout or a panic, not task watchdog.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A crash report's backtrace is a list of hexadecimal addresses. What turns it into something useful?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Converting the addresses to decimal</li><li style="margin:6px 0;">B. A decoder, such as PlatformIO's esp32\_exception\_decoder filter, which maps addresses to function names and line numbers using the compiled program</li><li style="margin:6px 0;">C. Restarting the device</li><li style="margin:6px 0;">D. Increasing the baud rate</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The addresses only have meaning together with the program that produced them. <strong>A</strong> changes the notation, not the meaning. <strong>C</strong> and <strong>D</strong> do not interpret anything.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Your D3 plotting script crashes when it reaches [W] loop: motion sensor not answering. What is the smallest fix that keeps the log message?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Lower the baud rate.</li><li style="margin:6px 0;">B. Start every log line with #, so the parser skips it.</li><li style="margin:6px 0;">C. Set LOG\_LEVEL to Debug.</li><li style="margin:6px 0;">D. Remove the [W] tag.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> D3's parser skips lines starting with #, so logs and data can share one serial port. <strong>A</strong> changes nothing about the content. <strong>C</strong> prints more log lines, not fewer. <strong>D</strong> leaves a line that is still not data.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A screen goes blank after 15 seconds during testing, and a student starts reading crash reports. What should they check first?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The stack size</li><li style="margin:6px 0;">B. Whether the device actually reset (for example, a new boot message), because a blank screen may be a designed behaviour, such as a screen timeout</li><li style="margin:6px 0;">C. The brownout threshold</li><li style="margin:6px 0;">D. The WiFi password</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> First establish what happened. The reference watch's "crash" was its screen-sleep timeout. <strong>A</strong>, <strong>C</strong> and <strong>D</strong> assume a fault that has not been shown to exist.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<a href="D6-going-further.md">D6 — Going Further</a> is a short reading-only tour of topics beyond this course: over-the-air updates, FreeRTOS tasks, ESP-IDF, secure MQTT, BLE, deep sleep and testing embedded code.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Espressif Systems. ESP-IDF Programming Guide (ESP32-C3): Fatal Errors (panic handler output, register dump with MEPC and MTVAL, backtrace decoding, brownout detector message, hardware stack guard "Stack protection fault"). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-guides/fatal-errors.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. PlatformIO. pio device monitor (esp32\_exception\_decoder filter, "decodes crash exception"). https://docs.platformio.org/en/latest/core/userguide/device/cmd\_monitor.html</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
