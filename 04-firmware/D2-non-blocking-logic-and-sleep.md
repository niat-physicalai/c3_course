# D2 — Non-Blocking Logic and Sleep Modes
## Running Everything at Its Own Pace, and Sleeping When There Is Nothing to Do

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Firmware
**Time:** ~2 hours · **You will produce:** a refactored sketch running three peripherals at three different rates, with no blocking calls, that sleeps when idle and wakes on a button

---

### One `delay()` Is Enough to Break a Watch

Here is a heart-rate function that looks perfectly reasonable:

```cpp
// BROKEN: blocks for the whole measurement.
int measureHeartRate() {
  heartSensorOn();
  delay(10000);            // collect samples for 10 s
  int bpm = calculateBpm();
  heartSensorOff();
  return bpm;
}
```

While that `delay()` runs, nothing else happens. The motion sensor is not read, so steps taken during those 10 seconds are lost. Button presses are not seen. The screen timeout does not count. If the wearer presses "cancel" because the watch is off their wrist, the watch ignores them until the time is up. On its own each problem is small. Together they are why a product built from `delay()` feels broken even when each feature works in isolation.

Part 1 used `delay()` and simple time checks for programs that did one thing. A product does several things at once, each at its own pace. The motion sensor needs reading 50 times a second, the heart-rate sensor only in short bursts, the display only when something changes. This unit runs them all from one `loop()`, with your D1 state machine, and puts the watch to sleep when idle.

### What You Will Be Able to Do After This Reading

- **Explain** why `delay()` and other blocking calls break a multi-task product.
- **Implement** the `millis()` scheduling pattern so several tasks run at different rates.
- **Implement** a state machine from a D1 diagram without blocking.
- **Debounce** buttons without waiting.
- **Measure** the worst-case time of `loop()`, and identify the call that sets it.
- **Choose** between modem sleep, light sleep and deep sleep for each idle period of your product, and **implement** the one you chose with a wake-up source.

---

# Part 1 — Why Blocking Breaks Products

Non-blocking code works only if every check is quick. One slow function, even with no `delay()` in it, holds up everything else.

## What Counts as Blocking

A **blocking call** is anything that makes the program wait before it can do anything else. Some are obvious, and some are hidden inside libraries:

| Blocking call | How long it can block | Non-blocking alternative |
|---|---|---|
| `delay(ms)` | Exactly as long as you ask | Check `millis()` each pass |
| Waiting in a `while` loop for a sensor to be ready | Until the sensor responds, or forever | Check once per pass; use the sensor's interrupt |
| Reading a whole measurement at once | The whole measurement time | Read a few samples per pass |
| Connecting to WiFi and waiting | Seconds, or longer if the network is gone | Start the connection, then check its status each pass (D4) |
| Sending a full display frame over I²C | About 25 ms on esp_watch at 400 kHz | Send only when something changed |

The last row deserves attention because it contains no `delay()` at all.

<!-- REFPRODUCT:START -->
esp_watch's author measured a full display update at about **25 ms** at 400 kHz and about **90 ms** at 100 kHz. For those milliseconds the processor is busy moving bytes, and nothing else runs.
<!-- REFPRODUCT:END -->

A motion sensor due every 20 ms will miss its slot whenever a full-screen update takes 25 ms. That is why "redraw only on change" matters for timing as well as for the bus load you calculated in B2.

---

# Part 2 — The `millis()` Pattern

## "Has My Interval Passed?"

`millis()` returns the milliseconds since the board started [1]. As in Part 1, each task stores when it last ran and checks, on every pass through `loop()`, whether its interval has passed. Each check almost always answers "not yet", so `loop()` runs thousands of times a second.

### Why `now - last >= period`, and Not `now >= last + period`

`millis()` is stored in an `unsigned long`, 32 bits on the ESP32. It counts up to 4,294,967,295 and then wraps back to zero:

```text
2^32 ms = 4,294,967,296 ms ÷ 1000 ÷ 60 ÷ 60 ÷ 24 ≈ 49.7 days
```

A watch left running for 50 days will see `millis()` wrap. Suppose a task ran at `last` = 4,294,967,290, with a 20 ms period:

```text
Addition form:     last + period = 4,294,967,310, which does not fit, so it wraps to 14.
                   One millisecond later, now = 4,294,967,291, and "now >= 14" is TRUE.
                   The task fires on every pass until the counter wraps: far too often.

Subtraction form:  now − last is computed with the same wrap-around.
                   At now = 4,294,967,291: difference = 1   → not yet.
                   At now = 14 (after the wrap): difference = 20 → due, exactly on time.
```

Unsigned subtraction wraps the same way the counter does, so `now - last` is always the true elapsed time. **Always write the subtraction form.**

## A Small Helper

When there are several periodic tasks, a tiny structure keeps them readable:

```cpp
struct Every {
  unsigned long period, last;
  bool due(unsigned long now) {
    if (now - last >= period) {   // safe across millis() rollover
      last = now;
      return true;
    }
    return false;
  }
};
Every motionTask{20, 0};   // 50 times a second
Every heartTask{40, 0};    // 25 times a second, during a measurement

void loop() {
  unsigned long now = millis();
  if (motionTask.due(now)) readMotion();
  // ...
}
```

## Worked Example: Three Peripherals, Three Rates

Here is the plan for a watch with a motion sensor, a heart-rate sensor and a display, before any code:

| Task | When it runs | Why that rate |
|---|---|---|
| Motion sensor | Every 20 ms, always | Steps must never be missed |
| Heart-rate sensor | Every 40 ms, **only during a measurement burst** | Measuring draws more than screen-on in the modelled budget (~44 mA vs ~36 mA, B3); between bursts the sensor is off |
| Display | **Only when something shown has changed**, and never while asleep | A full frame costs about 25 ms of bus and processor time |

**Step 1: How often does each run in a typical minute awake?**

```text
Motion:  60,000 ms ÷ 20 ms          = 3,000 reads per minute
Heart:   0 per minute, except during a 10 s burst: 10,000 ÷ 40 = 250 reads
Display: once per step shown, once per screen change, a few times per burst
         → say 60–120 redraws per minute while walking
```

**Step 2: How much time does each take?** **Example values:** a motion read takes about 0.5 ms, close to the register-read time measured on the reference watch (see Part 3), and more than the 0.4 ms of pure bus time from B5's trace because of library overhead. A redraw is about 25 ms.

```text
Motion:  3,000 × 0.5 ms       = 1,500 ms per minute  (2.5%)
Display: 120 × 25 ms          = 3,000 ms per minute  (5%)
         vs redrawing every 50 ms: 1,200 × 25 ms = 30,000 ms per minute (50%)
```

**Check.** With redraw-on-change, the processor is idle over 90% of the time, which is time it could spend in light sleep. Redrawing on a fixed fast schedule would spend half of every minute pushing pixels that did not change. The numbers make the design decision for you.

The complete sketch is in [`assets/code/D2-nonblocking-watch/`](../assets/code/D2-nonblocking-watch/), using the same Wokwi wiring as B5, with a mock heart-rate sensor. It compiles for the XIAO ESP32-C3. For this exercise, "next" changes screen and "previous" starts a 10 s heart-rate measurement, shortened from the 30 s assumed in B3's budget so you can test it quickly.

## Turning the State Machine Into Code

The heart of `loop()` is the state machine from D1, now combined with the tasks:

```cpp
void loop() {
  unsigned long start = micros();
  unsigned long now = millis();

  // 1. Always: sensors that must never be missed
  if (motionTask.due(now)) readMotion();

  // 2. Inputs
  bool next = btnNext.pressed(now);
  bool prev = btnPrev.pressed(now);

  // 3. State machine (from D1)
  switch (state) {
    case State::Awake:
      if (next) { screen = (screen + 1) % 2; lastInput = now; dirty = true; }
      if (prev) enter(State::Measuring, now);
      else if (now - lastInput >= SCREEN_TIMEOUT_MS) enter(State::Asleep, now);
      break;
    case State::Measuring:
      if (heartTask.due(now)) { samples++; if (samples % 25 == 0) dirty = true; }
      if (now - measureStart >= MEASURE_TIME_MS) {
        bpm = mockBpm(now);
        screen = 1;
        enter(State::Awake, now);
      }
      break;
    case State::Asleep:
      if (next || prev) enter(State::Awake, now);  // shake-to-wake would go here too
      break;
  }

  // 4. Display: only when something changed, and never while asleep
  if (dirty && state != State::Asleep) redraw();

  // 5. Keep an eye on the longest pass through loop()
  unsigned long took = micros() - start;
  if (took > worstLoopUs) {
    worstLoopUs = took;
    Serial.printf("new worst loop time: %lu us\n", worstLoopUs);
  }
}
```

Compare this with the broken function at the start. The measurement still lasts 10 seconds, but it no longer *blocks* for 10 seconds. It is a state, MEASURING, which the loop passes through thousands of times, reading a sample when one is due. Meanwhile the motion sensor keeps counting steps and the buttons keep working.

Notice the `dirty` flag. Anything that changes what the screen shows sets `dirty = true`: a new step on the step screen, a screen change, progress during a measurement. The display is redrawn at most once per pass, and only when needed. This one flag delivers B2's bus-load fix and this unit's timing fix together.

## Debouncing Without Waiting

A mechanical button does not switch cleanly. For a few milliseconds its contacts **bounce**, flickering between open and closed. Read it naively and one press counts as several. The common beginner fix, `delay(50)` after detecting a press, is blocking.

The non-blocking version remembers when the reading last changed, and only accepts it once it has been steady for a set time:

```cpp
struct Button {
  int pin;
  bool stable, lastRaw;
  unsigned long changedAt;
  bool pressed(unsigned long now) {           // true once per press
    bool raw = digitalRead(pin);
    if (raw != lastRaw) { lastRaw = raw; changedAt = now; }
    if (now - changedAt >= DEBOUNCE_MS && raw != stable) {
      stable = raw;
      return stable == LOW;
    }
    return false;
  }
};
```

It is the same idea as `Every`: a quick check each pass, with time measured rather than waited for.

<!-- MEDIA
type: screenshot
id: D2-01
caption: The non-blocking watch sketch running in Wokwi, with the worst-loop-time messages in the serial monitor
brief: Wokwi running the D2 project (same parts as B5). The display shows the "STEPS"
  screen with a large number. The MPU-6050's acceleration slider or popup open, being
  moved to simulate steps. Serial monitor at the bottom shows a few "new worst loop time:
  ... us" lines, the largest in the tens of thousands of microseconds (around a display
  update). The simulation timer running. Crop to show diagram and serial monitor together.
-->

> **Try it.** Run the D2 sketch in Wokwi, press the buttons and move the motion sensor's slider. Which call sets the worst loop time? How close is it to the reference watch's measured 25 ms display update?

---

# Part 3 — Keeping `loop()` Readable and Bounded

## Readable

A good `loop()` reads like the flowchart from D1: a short list of steps, each one a function call or a small `switch`. If `loop()` grows past a screen, move pieces into functions named for what they do: `readMotion()`, `handleButtons()`, `redraw()`. The state machine's `switch` is the one part that is allowed to be long, because each case is one box on the diagram.

## Bounded

A **bounded** loop has a known worst-case time for one pass. That number matters because it is the longest any task can be kept waiting. If the worst pass is 25 ms and the motion sensor wants a read every 20 ms, one read will occasionally be late.

Measure it, as the example does with `micros()`, and compare it with your fastest task's period:

| Worst loop time | Fastest task period | Verdict |
|---|---|---|
| Well under the period | 20 ms | Fine |
| Close to the period | 20 ms | Occasional late reads; check whether it matters |
| Over the period | 20 ms | Reads will be missed; find and split the slow call |

<!-- REFPRODUCT:START -->
On esp_watch the obvious candidate for the worst case is a full display update: about 25 ms at 400 kHz. The author also measured that a loop of 200 register reads takes 92 to 101 ms, about 0.5 ms per read. That is the scale of a single sensor transaction: small, but not zero, and worth knowing when you add up everything one pass might do.
<!-- REFPRODUCT:END -->

If one call is too slow, split it. A display library that can send part of the screen, a sensor that can be read a few samples at a time, and a network connection that can be started and then checked (D4) all turn one long call into several short ones.

---

# Part 4 — Sleeping When There Is Nothing to Do

## Why Sleep Matters More Than Anything Else on a Watch

A non-blocking loop runs thousands of times a second, and almost every pass answers "not yet". That is fine for timing, but the chip is fully awake the whole time, drawing current to do nothing.

<!-- REFPRODUCT:START -->
B3's budget (modelled, not measured) plans for the reference watch to sleep about 23.5 hours a day, with sleep taking roughly 60–80% of its daily charge. Today's firmware never sleeps: the watch is always on, which is why a sleep mode is the first thing worth adding. How well a watch sleeps matters more than the screen or the heart-rate sensor.
<!-- REFPRODUCT:END -->

So the most useful battery decision in your firmware is: **when nothing needs doing, which sleep mode, and what wakes it up?**

## The Sleep Modes, in Plain Terms

The ESP32-C3 has three sleep modes [3]. | Mode | What switches off | What is kept | How it wakes | After waking |
|---|---|---|---|---|
| **Active** | Nothing | Everything | — | — |
| **Modem sleep** | Only the WiFi/BLE radio, between the moments it is needed | Everything; your code keeps running | Automatic | The CPU never stopped |
| **Light sleep** | The CPU and most clocks pause | All RAM and variables | Timer, a GPIO pin (e.g. a button), UART | In about a millisecond, code **continues from the next line** |
| **Deep sleep** | Almost everything, including the main RAM | Only a small RTC memory (a few KB) | Timer, or GPIO0–GPIO5 only on the C3 | A **restart**: `setup()` runs again, and ordinary variables are gone |

Seeed's published figures for the XIAO ESP32-C3 on its own give the scale [2]:

| Mode | XIAO ESP32-C3 (Seeed) |
|---|---|
| Active | below 75 mA |
| Modem sleep | below 25 mA |
| Light sleep | below 4 mA |
| Deep sleep | about 43 µA |

Each step down saves current, from tens of mA awake to tens of µA in deep sleep, and costs something: a slower wake-up, or losing what was in memory.

> **What about "ultra-low-power" or "hibernation" modes?** Some chips go further. The original ESP32 has a hibernation mode, and the ESP32-S3 has a tiny extra processor (the ULP) that can watch a sensor while the main CPU sleeps. **The ESP32-C3 has neither.** Deep sleep is the lowest it goes. Below that the only step is **off**, meaning the battery is disconnected. On the reference watch that is what the slide switch does.

## Which One, When

| Situation | Use | Why |
|---|---|---|
| WiFi connected, device mostly waiting for data | **Modem sleep** | It is on by default when the ESP32 is connected to WiFi, so there is nothing to do except not turn it off |
| Screen off, but the user may press a button any second, and you must keep counting (steps, a timer) | **Light sleep** | Wakes instantly and keeps every variable |
| Nothing to do for minutes or hours, and little to remember (a sensor node reading every 15 min) | **Deep sleep** | Lowest current. The restart is acceptable because there is little state to lose. |
| Stored in a drawer, shipped, or not used for days | **Off** (power switch) | Nothing is cheaper than zero |

A watch sits in the light-sleep row: after the screen timeout it must still wake the moment a button is pressed, and it must not forget today's step count. A deep-sleep watch would reboot on every glance, and a reboot shows as a delay before the screen appears.

## The Chip Is Not the Whole Board

The 43 µA figure is for the XIAO alone. Your board's sleep current is the chip **plus everything else still powered**: the display, the sensors, the pull-ups and any divider. A display left on, or a sensor left sampling, can easily draw more than a sleeping chip. So "going to sleep" is a checklist:

1. Turn the display off (the SSD1306 has a display-off command).
2. Put each sensor in its own low-power or shutdown mode, unless it is the one that wakes you.
3. Only then put the chip to sleep.

<!-- PLACEHOLDER:FEATURE sleep / shake-to-wake — if esp_watch adds shake-to-wake, note here that the motion sensor stays on during sleep and adds to sleep current -->

## How To: Light Sleep With a Button Wake-Up

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

In the state machine, the ASLEEP state's entry action calls `goToLightSleep()`. When it returns, the watch is awake again. The next pass of `loop()` sees the button and changes state as normal.

## How To: Deep Sleep With a Timer or Pin Wake-Up

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

Two things catch students out:

- **Deep sleep is a reboot.** Anything you need afterwards must be in `RTC_DATA_ATTR` variables or saved to flash (D4).
- **On the ESP32-C3, only GPIO0–GPIO5 can wake the chip from deep sleep.** On the XIAO that means D0–D3 only. A button on any other pin cannot. Check this against your pin map from B3 before choosing deep sleep.

<!-- FACT:VERIFY GPIO0–GPIO5 as the ESP32-C3's deep-sleep wake-capable (RTC-domain) pins — confirm against the ESP32-C3 datasheet's RTC GPIO table; ESP-IDF sleep_modes page only says "RTC domain" -->

<!-- REFPRODUCT:START -->
If esp_watch adds sleep later: its buttons are on D10 and D9, and neither is one of the XIAO's deep-sleep wake pins (D0–D3), so neither could wake the watch from deep sleep. Light sleep, which can wake on any pin, would suit it; deep sleep would need one button moved to D0–D3 in a v2.
<!-- REFPRODUCT:END -->

## Worked Example: What a Better Sleep Would Buy

**Example values.** Take the reference watch's modelled day: 15.0 mAh for the screen and 1.8 mAh for heart-rate readings, plus 23.5 h of sleep.

```text
Sleep at 3 mA (modelled, high):   23.5 h × 3 mA   = 70.5 mAh → day total ≈ 87 mAh
Sleep at 1 mA (modelled, low):    23.5 h × 1 mA   = 23.5 mAh → day total ≈ 40 mAh
Sleep at 0.2 mA (example only):   23.5 h × 0.2 mA =  4.7 mAh → day total ≈ 22 mAh
```

**Check.** Going from 3 mA to 1 mA of sleep current roughly doubles the battery life. None of the awake-time savings in Part 2 comes close. That is why the sleep checklist, meaning display off, sensors down, then chip, is worth more than any other optimisation in this unit.

## Spot the Bug

Each of these compiles and seems to work in a quick test. Find what is wrong.

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

<details>
<summary>Answer</summary>

**Version A** has three defects. `delay(200)` blocks for every press, freezing the motion reads and everything else. `redraw()` runs on every pass, sending a full frame (about 25 ms) continuously, so the motion task will often be late. And `lastMotion = millis()` after `readMotion()` records the time *after* the read, so each period stretches by the read's duration and the rate slowly drifts. Store `now` at the start instead.

**Version B** uses `now >= lastMotion + 20`, which misbehaves when `millis()` wraps after about 49.7 days. Use `now - lastMotion >= 20`. It is otherwise correct.

</details>

---

# Putting It All Together

## Applying What You Have Learned

**1. Find the blocking calls.** Search your current sketch for `delay(`, `while (` loops that wait on hardware, and any library call you know takes more than a few milliseconds. List each with its worst-case time.

**2. Plan the tasks.** Make a table like the worked example: every task, its rate, and why. Mark which run always and which only in certain states.

**3. Refactor.** Replace each blocking call with a timed check, a state, or a split call. Implement your D1 state machine as a `switch`, with an `enter()` function for entry and exit actions.

**4. Add a `dirty` flag** so the display is redrawn only when its content changes.

**5. Measure.** Add the worst-loop-time check. Compare it with your fastest task's period, and record both.

**6. Choose and add sleep.** For each idle period in your state diagram, pick modem, light or deep sleep (or off) from the "Which one, when" table and write one line saying why. Implement the ASLEEP state with your chosen mode and a button wake-up. In Wokwi, or from the serial log, confirm the sketch enters ASLEEP after the timeout and wakes on the button. <!-- FACT:VERIFY Wokwi support for esp_light_sleep_start() and GPIO light-sleep wake-up on the XIAO ESP32-C3 -->

**Deliverable:** your refactored sketch, running in Wokwi or compiling in PlatformIO, with three peripherals at three different rates, no blocking calls, and a sleep state with a wake-up. Add a short note with your measured worst loop time and your sleep-mode choice with its reason. Save both in your design pack.

## Self-Check

Open your refactored sketch and answer each item Y or N.

1. The sketch contains no `delay()` calls in `loop()` or anything it calls. — Y/N
2. No `while` loop waits for hardware without a timeout. — Y/N
3. Every periodic check uses the form `now - last >= period`. — Y/N
4. At least three tasks run at three different rates. — Y/N
5. At least one task runs only in a particular state. — Y/N
6. The display is redrawn only when a `dirty` flag, or equivalent, is set. — Y/N
7. Buttons are debounced without waiting. — Y/N
8. The state machine matches your D1 diagram arrow for arrow. — Y/N
9. The worst loop time is measured and recorded, and compared with the fastest task period. — Y/N
10. The sleep state names one sleep mode and at least one wake-up source. — Y/N
11. The display is turned off before the chip sleeps. — Y/N
12. If deep sleep is used, the wake pin is one of GPIO0–GPIO5, and anything needed after waking is in `RTC_DATA_ATTR` or flash. — Y/N

---

## Check Your Understanding

**1.** A watch reads its motion sensor every 20 ms and redraws the full display every pass through `loop()`. Each redraw takes about 25 ms. What happens to the motion reads?

- A. Nothing; they are on their own timer.
- B. They run late, because each pass takes at least 25 ms, so the 20 ms timer is always overdue and reads happen roughly every 25 ms instead.
- C. They stop completely.
- D. They speed up.

<details>
<summary>Answer</summary>

**B.** A timer check can only run when `loop()` reaches it. If every pass includes a 25 ms redraw, reads happen at most once per pass. **A** misunderstands non-blocking timing: the timer does not interrupt a running function. **C** is too strong; the reads still happen, just late. **D** has no mechanism.

</details>

**2.** A sensor node wakes from deep sleep every 15 minutes, sends one reading, and must report how many readings it has sent since power-on. Where should the counter live?

- A. An ordinary global variable.
- B. A global variable marked `RTC_DATA_ATTR`.
- C. A local variable in `setup()`.
- D. Nowhere; deep sleep erases everything.

<details>
<summary>Answer</summary>

**B.** RTC memory stays powered in deep sleep, so the counter survives each wake. **A** and **C** live in main RAM, which is lost: waking reruns `setup()` and both restart at 0. **D** is too strong, because the small RTC memory is kept.

</details>
**3.** A student debounces a button with `delay(50)` after each press. What is the main problem?

- A. 50 ms is too short to debounce.
- B. Every press freezes the whole program for 50 ms, so other tasks, such as sensor reads, miss their slots.
- C. `delay()` uses too much power.
- D. Nothing, because 50 ms is very short.

<details>
<summary>Answer</summary>

**B.** Any `delay()` in `loop()` stops every task. On a watch reading motion every 20 ms, 50 ms loses two or three reads per press. **A** is usually untrue; 50 ms debounces most buttons. **C** is not the main issue. **D** ignores that other tasks run on shorter periods than 50 ms.

</details>

**4.** A heart-rate measurement takes 10 seconds. What is the non-blocking way to implement it?

- A. Call `delay(10000)` inside a separate function.
- B. Make MEASURING a state: record the start time on entry, read a sample whenever one is due, and leave the state when 10 s have passed.
- C. Measure for 1 second instead.
- D. Run the measurement in `setup()`.

<details>
<summary>Answer</summary>

**B.** The measurement becomes a state the loop passes through, so everything else keeps running. **A** still blocks, just from another function. **C** changes the requirement to hide the problem. **D** runs it only once, at start-up, and still blocks.

</details>

**5.** A watch must wake instantly when a button is pressed and must not lose today's step count. Its button is on XIAO pin D10. Which sleep mode fits between uses?

- A. Deep sleep, because it uses the least current.
- B. Light sleep, because it wakes in about a millisecond, keeps every variable, and can wake from any GPIO.
- C. Modem sleep, because it switches the radio off.
- D. No sleep, because sleeping would lose the step count.

<details>
<summary>Answer</summary>

**B.** Light sleep keeps RAM and resumes where it stopped. **A** fails twice: deep sleep reboots and loses ordinary variables, and D10 cannot wake it. **C** leaves the CPU running and saves little. **D** is wrong because light sleep keeps the count.

</details>

## What Comes Next

**Next:** [D3 — Data Off the Device](D3-data-off-the-device.md): a serial data format, a logged session and a live plot.

---

## References

1. Arduino. *millis()* ("Returns the number of milliseconds passed since the Arduino board began running the current program. This number will overflow (go back to zero), after approximately 50 days."). https://docs.arduino.cc/language-reference/en/functions/time/millis/
2. Seeed Studio. *Getting Started with Seeed Studio XIAO ESP32C3* (current by mode). https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/
3. Espressif Systems. *ESP-IDF Programming Guide (ESP32-C3): Sleep Modes* (light sleep keeps state; deep sleep powers off most RAM; deep-sleep GPIO wake-up only from RTC-domain pins). https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/system/sleep_modes.html

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
