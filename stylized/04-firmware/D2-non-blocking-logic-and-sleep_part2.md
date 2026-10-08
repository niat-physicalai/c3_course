<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 4 — Sleeping When There Is Nothing to Do</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Why Sleep Matters More Than Anything Else on a Watch</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A non-blocking loop runs thousands of times a second, and almost every pass answers "not yet". That is fine for timing, but the chip is fully awake the whole time, drawing current to do nothing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">B3's budget (modelled, not measured) plans for the reference watch to sleep about 23.5 hours a day, with sleep taking roughly 60–80% of its daily charge. Today's firmware never sleeps: the watch is always on, which is why a sleep mode is the first thing worth adding. How well a watch sleeps matters more than the screen or the heart-rate sensor.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">So the most useful battery decision in your firmware is: <strong>when nothing needs doing, which sleep mode, and what wakes it up?</strong></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Sleep Modes, in Plain Terms</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">The ESP32-C3 has three sleep modes [3].</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Mode</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What switches off</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What is kept</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How it wakes</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">After waking</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Active</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Nothing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Everything</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Modem sleep</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Only the WiFi/BLE radio, between the moments it is needed</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Everything; your code keeps running</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Automatic</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The CPU never stopped</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Light sleep</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The CPU and most clocks pause</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">All RAM and variables</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Timer, a GPIO pin (e.g. a button), UART</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">In about a millisecond, code <strong>continues from the next line</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Deep sleep</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Almost everything, including the main RAM</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Only a small RTC memory (a few KB)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Timer, or GPIO0–GPIO5 only on the C3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A <strong>restart</strong>: setup() runs again, and ordinary variables are gone</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;"></td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Seeed's published figures for the XIAO ESP32-C3 on its own give the scale [2]:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Mode</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">XIAO ESP32-C3 (Seeed)</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Active</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">below 75 mA</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modem sleep</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">below 25 mA</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Light sleep</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">below 4 mA</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Deep sleep</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">about 43 µA</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each step down saves current, from tens of mA awake to tens of µA in deep sleep, and costs something: a slower wake-up, or losing what was in memory.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>​<strong>What about "ultra-low-power" or "hibernation" modes?</strong> Some chips go further. The original ESP32 has a hibernation mode, and the ESP32-S3 has a tiny extra processor (the ULP) that can watch a sensor while the main CPU sleeps. <strong>The ESP32-C3 has neither.</strong> Deep sleep is the lowest it goes. Below that the only step is <strong>off</strong>, meaning the battery is disconnected. On the reference watch that is what the slide switch does.</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Which One, When</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Situation</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Use</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">WiFi connected, device mostly waiting for data</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Modem sleep</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">It is on by default when the ESP32 is connected to WiFi, so there is nothing to do except not turn it off</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Screen off, but the user may press a button any second, and you must keep counting (steps, a timer)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Light sleep</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Wakes instantly and keeps every variable</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Nothing to do for minutes or hours, and little to remember (a sensor node reading every 15 min)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Deep sleep</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lowest current. The restart is acceptable because there is little state to lose.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Stored in a drawer, shipped, or not used for days</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Off</strong> (power switch)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Nothing is cheaper than zero</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A watch sits in the light-sleep row: after the screen timeout it must still wake the moment a button is pressed, and it must not forget today's step count. A deep-sleep watch would reboot on every glance, and a reboot shows as a delay before the screen appears.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Chip Is Not the Whole Board</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The 43 µA figure is for the XIAO alone. Your board's sleep current is the chip <strong>plus everything else still powered</strong>: the display, the sensors, the pull-ups and any divider. A display left on, or a sensor left sampling, can easily draw more than a sleeping chip. So "going to sleep" is a checklist:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Turn the display off (the SSD1306 has a display-off command).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Put each sensor in its own low-power or shutdown mode, unless it is the one that wakes you.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Only then put the chip to sleep.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">How To: Light Sleep With a Button Wake-Up</div>

```cpp
#include "esp_sleep.h"
#include "driver/gpio.h"

const int BTN_NEXT = 10;   // XIAO D10, button to GND with internal pull-up

void goToLightSleep() {
  display.ssd1306_command(SSD1306_DISPLAYOFF);         // 1. display off
  // 2. put sensors you don't need into low-power mode here

  gpio_wakeup_enable((gpio_num_t)BTN_NEXT, GPIO_INTR_LOW_LEVEL);  // pressed = LOW
  esp_sleep_enable_gpio_wakeup();

  esp_light_sleep_start();                             // 3. the chip pauses HERE...

  // ...and continues HERE after waking, with every variable intact.
  // enter(State::Awake) turns the display back on.
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In the state machine, the ASLEEP state's entry action calls goToLightSleep(). When it returns, the watch is awake again. The next pass of loop() sees the button and changes state as normal.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">How To: Deep Sleep With a Timer or Pin Wake-Up</div>

```cpp
#include "esp_sleep.h"

RTC_DATA_ATTR uint32_t bootCount = 0;   // kept in RTC memory: survives deep sleep
uint32_t ordinaryCounter = 0;           // lost: back to 0 after every wake

void setup() {
  Serial.begin(115200);
  bootCount++;
  if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_TIMER) {
    Serial.println("Woke on the timer");
  } else if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_GPIO) {
    Serial.println("Woke on a pin");
  }
  Serial.printf("Boot number %lu\n", (unsigned long)bootCount);

  // ... read the sensor, send the reading ...

  esp_deep_sleep_enable_gpio_wakeup(1ULL << 3, ESP_GPIO_WAKEUP_GPIO_LOW);  // GPIO3 = XIAO D1; only GPIO0–5 work
  esp_sleep_enable_timer_wakeup(15ULL * 60 * 1000000);                      // or every 15 minutes
  esp_deep_sleep_start();   // never returns: the next code to run is setup()
}

void loop() {}              // never reached in this pattern
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two things catch students out:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Deep sleep is a reboot.</strong> Anything you need afterwards must be in RTC\_DATA\_ATTR variables or saved to flash (D4).</li><li style="margin:6px 0;">​<strong>On the ESP32-C3, only GPIO0–GPIO5 can wake the chip from deep sleep.</strong> On the XIAO that means D0–D3 only. A button on any other pin cannot. Check this against your pin map from B3 before choosing deep sleep.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">If esp\_watch adds sleep later: its buttons are on D10 and D9, and neither is one of the XIAO's deep-sleep wake pins (D0–D3), so neither could wake the watch from deep sleep. Light sleep, which can wake on any pin, would suit it; deep sleep would need one button moved to D0–D3 in a v2.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: What a Better Sleep Would Buy</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Example values.</strong> Take the reference watch's modelled day: 15.0 mAh for the screen and 1.8 mAh for heart-rate readings, plus 23.5 h of sleep.</div>

```text
Sleep at 3 mA (modelled, high):   23.5 h × 3 mA   = 70.5 mAh → day total ≈ 87 mAh
Sleep at 1 mA (modelled, low):    23.5 h × 1 mA   = 23.5 mAh → day total ≈ 40 mAh
Sleep at 0.2 mA (example only):   23.5 h × 0.2 mA =  4.7 mAh → day total ≈ 22 mAh
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Going from 3 mA to 1 mA of sleep current roughly doubles the battery life. None of the awake-time savings in Part 2 comes close. That is why the sleep checklist, meaning display off, sensors down, then chip, is worth more than any other optimisation in this unit.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Spot the Bug</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Each of these compiles and seems to work in a quick test. Find what is wrong.</div>

```cpp
// Version A
void loop() {
  if (millis() - lastMotion >= 20) {
    readMotion();
    lastMotion = millis();
  }
  if (buttonPressed()) {
    screen++;
    delay(200);   // debounce
  }
  redraw();
}
```

```cpp
// Version B
void loop() {
  unsigned long now = millis();
  if (now >= lastMotion + 20) { lastMotion = now; readMotion(); }
  if (dirty) redraw();
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Version A</strong> has three defects. delay(200) blocks for every press, freezing the motion reads and everything else. redraw() runs on every pass, sending a full frame (about 25 ms) continuously, so the motion task will often be late. And lastMotion = millis() after readMotion() records the time after the read, so each period stretches by the read's duration and the rate slowly drifts. Store now at the start instead.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Version B</strong> uses now &gt;= lastMotion + 20, which misbehaves when millis() wraps after about 49.7 days. Use now - lastMotion &gt;= 20. It is otherwise correct.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Find the blocking calls.</strong> Search your current sketch for delay(, while ( loops that wait on hardware, and any library call you know takes more than a few milliseconds. List each with its worst-case time.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Plan the tasks.</strong> Make a table like the worked example: every task, its rate, and why. Mark which run always and which only in certain states.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Refactor.</strong> Replace each blocking call with a timed check, a state, or a split call. Implement your D1 state machine as a switch, with an enter() function for entry and exit actions.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Add a dirty flag</strong> so the display is redrawn only when its content changes.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Measure.</strong> Add the worst-loop-time check. Compare it with your fastest task's period, and record both.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6. Choose and add sleep.</strong> For each idle period in your state diagram, pick modem, light or deep sleep (or off) from the "Which one, when" table and write one line saying why. Implement the ASLEEP state with your chosen mode and a button wake-up. In Wokwi, or from the serial log, confirm the sketch enters ASLEEP after the timeout and wakes on the button.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> your refactored sketch, running in Wokwi or compiling in PlatformIO, with three peripherals at three different rates, no blocking calls, and a sleep state with a wake-up. Add a short note with your measured worst loop time and your sleep-mode choice with its reason. Save both in your design pack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your refactored sketch and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The sketch contains no delay() calls in loop() or anything it calls. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. No while loop waits for hardware without a timeout. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every periodic check uses the form now - last &gt;= period. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. At least three tasks run at three different rates. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. At least one task runs only in a particular state. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The display is redrawn only when a dirty flag, or equivalent, is set. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Buttons are debounced without waiting. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The state machine matches your D1 diagram arrow for arrow. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. The worst loop time is measured and recorded, and compared with the fastest task period. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">10. The sleep state names one sleep mode and at least one wake-up source. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">11. The display is turned off before the chip sleeps. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">12. If deep sleep is used, the wake pin is one of GPIO0–GPIO5, and anything needed after waking is in RTC\_DATA\_ATTR or flash. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A watch reads its motion sensor every 20 ms and redraws the full display every pass through loop(). Each redraw takes about 25 ms. What happens to the motion reads?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing; they are on their own timer.</li><li style="margin:6px 0;">B. They run late, because each pass takes at least 25 ms, so the 20 ms timer is always overdue and reads happen roughly every 25 ms instead.</li><li style="margin:6px 0;">C. They stop completely.</li><li style="margin:6px 0;">D. They speed up.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A timer check can only run when loop() reaches it. If every pass includes a 25 ms redraw, reads happen at most once per pass. <strong>A</strong> misunderstands non-blocking timing: the timer does not interrupt a running function. <strong>C</strong> is too strong; the reads still happen, just late. <strong>D</strong> has no mechanism.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A sensor node wakes from deep sleep every 15 minutes, sends one reading, and must report how many readings it has sent since power-on. Where should the counter live?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. An ordinary global variable.</li><li style="margin:6px 0;">B. A global variable marked RTC\_DATA\_ATTR.</li><li style="margin:6px 0;">C. A local variable in setup().</li><li style="margin:6px 0;">D. Nowhere; deep sleep erases everything.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> RTC memory stays powered in deep sleep, so the counter survives each wake. <strong>A</strong> and <strong>C</strong> live in main RAM, which is lost: waking reruns setup() and both restart at 0. <strong>D</strong> is too strong, because the small RTC memory is kept.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A student debounces a button with delay(50) after each press. What is the main problem?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 50 ms is too short to debounce.</li><li style="margin:6px 0;">B. Every press freezes the whole program for 50 ms, so other tasks, such as sensor reads, miss their slots.</li><li style="margin:6px 0;">C. delay() uses too much power.</li><li style="margin:6px 0;">D. Nothing, because 50 ms is very short.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Any delay() in loop() stops every task. On a watch reading motion every 20 ms, 50 ms loses two or three reads per press. <strong>A</strong> is usually untrue; 50 ms debounces most buttons. <strong>C</strong> is not the main issue. <strong>D</strong> ignores that other tasks run on shorter periods than 50 ms.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A heart-rate measurement takes 10 seconds. What is the non-blocking way to implement it?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Call delay(10000) inside a separate function.</li><li style="margin:6px 0;">B. Make MEASURING a state: record the start time on entry, read a sample whenever one is due, and leave the state when 10 s have passed.</li><li style="margin:6px 0;">C. Measure for 1 second instead.</li><li style="margin:6px 0;">D. Run the measurement in setup().</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The measurement becomes a state the loop passes through, so everything else keeps running. <strong>A</strong> still blocks, just from another function. <strong>C</strong> changes the requirement to hide the problem. <strong>D</strong> runs it only once, at start-up, and still blocks.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A watch must wake instantly when a button is pressed and must not lose today's step count. Its button is on XIAO pin D10. Which sleep mode fits between uses?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Deep sleep, because it uses the least current.</li><li style="margin:6px 0;">B. Light sleep, because it wakes in about a millisecond, keeps every variable, and can wake from any GPIO.</li><li style="margin:6px 0;">C. Modem sleep, because it switches the radio off.</li><li style="margin:6px 0;">D. No sleep, because sleeping would lose the step count.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Light sleep keeps RAM and resumes where it stopped. <strong>A</strong> fails twice: deep sleep reboots and loses ordinary variables, and D10 cannot wake it. <strong>C</strong> leaves the CPU running and saves little. <strong>D</strong> is wrong because light sleep keeps the count.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Next:</strong> <a href="D3-data-off-the-device.md">D3 — Data Off the Device</a>: a serial data format, a logged session and a live plot.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Arduino. millis() ("Returns the number of milliseconds passed since the Arduino board began running the current program. This number will overflow (go back to zero), after approximately 50 days."). https://docs.arduino.cc/language-reference/en/functions/time/millis/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Seeed Studio. Getting Started with Seeed Studio XIAO ESP32C3 (current by mode). https://wiki.seeedstudio.com/XIAO\_ESP32C3\_Getting\_Started/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Espressif Systems. ESP-IDF Programming Guide (ESP32-C3): Sleep Modes (light sleep keeps state; deep sleep powers off most RAM; deep-sleep GPIO wake-up only from RTC-domain pins). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/sleep\_modes.html</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
