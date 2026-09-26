# C4 — Non-Blocking Application Logic
## Running Everything at Its Own Pace, With Nothing Waiting for Anything Else

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Firmware
**Time:** ~1.5 hours · **You will produce:** a refactored sketch running three peripherals at three different rates, with no blocking calls

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

In Part 1, `delay()` was a fine way to wait. Programs did one thing at a time. A product does several things at once, each at its own pace: the motion sensor wants attention 50 times a second, the heart-rate sensor only in short bursts, the display only when something changes. This unit shows how to run them all from one `loop()` without any of them waiting for the others, and how to turn the state diagram from C1 into code that does the same.

### What You Will Be Able to Do After This Reading

- **Explain** why `delay()` and other blocking calls break a multi-task product.
- **Implement** the `millis()` scheduling pattern so several tasks run at different rates.
- **Implement** a state machine from a C1 diagram without blocking.
- **Debounce** buttons without waiting.
- **Measure** the worst-case time of `loop()`, and identify the call that sets it.

### What Part 1 Already Covered

Part 1 introduced time-based checks: reading a sensor only when its interval had elapsed, and blinking an LED without sleeping. **What is new here** is building a whole product's firmware on that idea: several tasks at different rates, a state machine, debouncing, and a measured bound on how long each pass of `loop()` can take.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Why Blocking Breaks Products

## The Kitchen With One Cook

Imagine a single cook making tea, toast and eggs. A blocking cook puts the kettle on and stands watching it until it boils, then puts the bread in and watches the toaster, then starts the eggs. Breakfast takes the sum of every wait. A non-blocking cook starts the kettle, starts the toast, starts the eggs, and then walks round checking each one: *is the kettle done? Not yet. Is the toast done? Yes, take it out.* The waits overlap, and nothing burns.

A microcontroller running `loop()` is a single cook. Non-blocking code is the cook who keeps walking round.

The analogy stops working in one place. A real cook can glance at the kettle while buttering toast. The microcontroller cannot: while it is inside one function, even a short one, it is doing nothing else. So non-blocking code relies on every check being *quick*. A single slow function, even with no `delay()` in it, can still hold up everything else. Part 3 measures exactly that.

## What Counts as Blocking

A **blocking call** is anything that makes the program wait before it can do anything else. Some are obvious, and some are hidden inside libraries:

| Blocking call | How long it can block | Non-blocking alternative |
|---|---|---|
| `delay(ms)` | Exactly as long as you ask | Check `millis()` each pass |
| Waiting in a `while` loop for a sensor to be ready | Until the sensor responds, or forever | Check once per pass; use the sensor's interrupt |
| Reading a whole measurement at once | The whole measurement time | Read a few samples per pass |
| Connecting to WiFi and waiting | Seconds, or longer if the network is gone | Start the connection, then check its status each pass (C5b) |
| Sending a full display frame over I²C | About 25 ms on esp_watch at 400 kHz | Send only when something changed |

The last row deserves attention because it contains no `delay()` at all.

<!-- REFPRODUCT:START -->
esp_watch's author measured a full display update at about **25 ms** at 400 kHz and about **90 ms** at 100 kHz. For those milliseconds the processor is busy moving bytes, and nothing else runs.
<!-- REFPRODUCT:END -->

A motion sensor due every 20 ms will miss its slot whenever a full-screen update takes 25 ms. That is why "redraw only on change" matters for timing as well as for the bus load you calculated in B0.

---

# Part 2 — The `millis()` Pattern

## "Has My Interval Passed?"

`millis()` returns the number of milliseconds since the board started [1]. Instead of waiting, each task remembers when it last ran and asks, every pass through `loop()`, whether its interval has passed:

```cpp
unsigned long lastMotion = 0;

void loop() {
  unsigned long now = millis();
  if (now - lastMotion >= 20) {   // 20 ms since the last read?
    lastMotion = now;
    readMotion();
  }
  // ... every other task checks its own clock the same way ...
}
```

Written this way, each task is a quick check that almost always answers "not yet". A `loop()` made of such checks runs thousands of times a second, and each task runs when it is due.

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
| Motion sensor | Every 20 ms, always | Steps and shake-to-wake must never be missed |
| Heart-rate sensor | Every 40 ms, **only during a measurement burst** | Its LEDs are the biggest power draw (B1); between bursts it is off |
| Display | **Only when something shown has changed**, and never while asleep | A full frame costs about 25 ms of bus and processor time |

**Step 1: How often does each run in a typical minute awake?**

```text
Motion:  60,000 ms ÷ 20 ms          = 3,000 reads per minute
Heart:   0 per minute, except during a 10 s burst: 10,000 ÷ 40 = 250 reads
Display: once per step shown, once per screen change, a few times per burst
         → say 60–120 redraws per minute while walking
```

**Step 2: How much time does each take?** **Example values:** a motion read takes about 0.5 ms, close to the register-read time measured on the reference watch (see Part 3), and more than the 0.2 ms of pure bus time from B3's trace because of library overhead. A redraw is about 25 ms.

```text
Motion:  3,000 × 0.5 ms       = 1,500 ms per minute  (2.5%)
Display: 120 × 25 ms          = 3,000 ms per minute  (5%)
         vs redrawing every 50 ms: 1,200 × 25 ms = 30,000 ms per minute (50%)
```

**Check.** With redraw-on-change, the processor is idle over 90% of the time, which is time it could spend in light sleep. Redrawing on a fixed fast schedule would spend half of every minute pushing pixels that did not change. The numbers make the design decision for you.

The complete sketch is in [`assets/code/C4-nonblocking-watch/`](../assets/code/C4-nonblocking-watch/), using the same Wokwi wiring as B3, with a mock heart-rate sensor. It compiles for the XIAO ESP32-C3. For this exercise, "next" changes screen and "previous" starts a 10 s heart-rate measurement, shortened from the watch's real 30 s so you can test it quickly.

## Turning the State Machine Into Code

The heart of `loop()` is the state machine from C1, now combined with the tasks:

```cpp
void loop() {
  unsigned long start = micros();
  unsigned long now = millis();

  // 1. Always: sensors that must never be missed
  if (motionTask.due(now)) readMotion();

  // 2. Inputs
  bool next = btnNext.pressed(now);
  bool prev = btnPrev.pressed(now);

  // 3. State machine (from C1)
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

Notice the `dirty` flag. Anything that changes what the screen shows sets `dirty = true`: a new step on the step screen, a screen change, progress during a measurement. The display is redrawn at most once per pass, and only when needed. This one flag delivers B0's bus-load fix and this unit's timing fix together.

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
id: C4-01
caption: The non-blocking watch sketch running in Wokwi, with the worst-loop-time messages in the serial monitor
brief: Wokwi running the C4 project (same parts as B3). The display shows the "STEPS"
  screen with a large number. The MPU-6050's acceleration slider or popup open, being
  moved to simulate steps. Serial monitor at the bottom shows a few "new worst loop time:
  ... us" lines, the largest in the tens of thousands of microseconds (around a display
  update). The simulation timer running. Crop to show diagram and serial monitor together.
-->

> **Try it: Find what sets the worst case.** Run the C4 sketch in Wokwi.
> 1. **Predict.** What will the worst loop time be, roughly, and which call will cause it?
> 2. **Do.** Watch the "new worst loop time" messages as you press buttons and move the motion sensor's slider in the simulator.
> 3. **Explain.** Is the worst case close to a display update time from B0 and B3? If the simulator's number differs from the reference watch's measured 25 ms, what might Wokwi not be modelling?
>
> **Extra challenge:** Change the redraw so it happens on a fixed 50 ms schedule instead of only when `dirty`. What happens to the step count while you move the slider quickly?

---

# Part 3 — Keeping `loop()` Readable and Bounded

## Readable

A good `loop()` reads like the flowchart from C1: a short list of steps, each one a function call or a small `switch`. If `loop()` grows past a screen, move pieces into functions named for what they do: `readMotion()`, `handleButtons()`, `redraw()`. The state machine's `switch` is the one part that is allowed to be long, because each case is one box on the diagram.

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

If one call is too slow, split it. A display library that can send part of the screen, a sensor that can be read a few samples at a time, and a network connection that can be started and then checked (C5b) all turn one long call into several short ones.

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

**3. Refactor.** Replace each blocking call with a timed check, a state, or a split call. Implement your C1 state machine as a `switch`, with an `enter()` function for entry and exit actions.

**4. Add a `dirty` flag** so the display is redrawn only when its content changes.

**5. Measure.** Add the worst-loop-time check. Compare it with your fastest task's period, and record both.

**Deliverable:** your refactored sketch, running in Wokwi or compiling in PlatformIO, with three peripherals at three different rates and no blocking calls, plus a short note of your measured worst loop time. Save both in your design pack.

## Self-Check

Open your refactored sketch and answer each item Y or N.

1. The sketch contains no `delay()` calls in `loop()` or anything it calls. — Y/N
2. No `while` loop waits for hardware without a timeout. — Y/N
3. Every periodic check uses the form `now - last >= period`. — Y/N
4. At least three tasks run at three different rates. — Y/N
5. At least one task runs only in a particular state. — Y/N
6. The display is redrawn only when a `dirty` flag, or equivalent, is set. — Y/N
7. Buttons are debounced without waiting. — Y/N
8. The state machine matches your C1 diagram arrow for arrow. — Y/N
9. The worst loop time is measured and recorded, and compared with the fastest task period. — Y/N

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

**2.** Why is `if (now - last >= period)` preferred to `if (now >= last + period)`?

- A. It is faster to compute.
- B. It stays correct when `millis()` wraps round to zero after about 49.7 days, because unsigned subtraction wraps the same way the counter does.
- C. It uses less memory.
- D. They are identical in every case.

<details>
<summary>Answer</summary>

**B.** Near the wrap, `last + period` overflows to a small number and the comparison gives the wrong answer; the subtraction still gives the true elapsed time. **A** and **C** are negligible. **D** is false near the wrap point.

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

**5.** A sketch records `lastMotion = millis()` *after* calling `readMotion()`, which takes about 0.5 ms. Over a long run, what happens?

- A. Nothing.
- B. Each period stretches by the read's duration, so the effective rate is a little slower than intended and the timing drifts.
- C. The reads happen twice as often.
- D. The program crashes.

<details>
<summary>Answer</summary>

**B.** The next interval is measured from the end of the read, not its start, so every cycle is about 20.5 ms instead of 20 ms. Store `now`, taken once at the top of `loop()`, instead. **A** ignores the accumulated drift. **C** and **D** have no mechanism.

</details>

---

## What You Can Now Do, and What Comes Next

- Recognise blocking calls, including the hidden ones inside libraries.
- Run several tasks at different rates with the `millis()` pattern, correctly across rollover.
- Implement a state machine and debounced buttons that never wait.
- Measure your worst loop time and find what sets it.

The idea to carry forward: **nothing waits; everything checks.** A long job becomes a state or a series of short steps, and the display only moves bytes when something has changed.

In [C5a — Data Off the Device](C5a-data-off-the-device.md) you will get the data your tasks produce off the watch and onto a laptop: a proper serial data format, a logged session, and a live plot.

---

## References

1. Arduino. *millis()* ("Returns the number of milliseconds passed since the Arduino board began running the current program. This number will overflow (go back to zero), after approximately 50 days."). https://docs.arduino.cc/language-reference/en/functions/time/millis/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
