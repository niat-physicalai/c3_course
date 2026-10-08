<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">D2 — Non-Blocking Logic and Sleep Modes</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Running Everything at Its Own Pace, and Sleeping When There Is Nothing to Do</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 4 — Firmware <strong>Time:</strong> ~2 hours · <strong>You will produce:</strong> a refactored sketch running three peripherals at three different rates, with no blocking calls, that sleeps when idle and wakes on a button</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">One delay() Is Enough to Break a Watch</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is a heart-rate function that looks perfectly reasonable:</div>

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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">While that delay() runs, nothing else happens. The motion sensor is not read, so steps taken during those 10 seconds are lost. Button presses are not seen. The screen timeout does not count. If the wearer presses "cancel" because the watch is off their wrist, the watch ignores them until the time is up. On its own each problem is small. Together they are why a product built from delay() feels broken even when each feature works in isolation.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 used delay() and simple time checks for programs that did one thing. A product does several things at once, each at its own pace. The motion sensor needs reading 50 times a second, the heart-rate sensor only in short bursts, the display only when something changes. This unit runs them all from one loop(), with your D1 state machine, and puts the watch to sleep when idle.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Explain</strong> why delay() and other blocking calls break a multi-task product.</li><li style="margin:6px 0;">​<strong>Implement</strong> the millis() scheduling pattern so several tasks run at different rates.</li><li style="margin:6px 0;">​<strong>Implement</strong> a state machine from a D1 diagram without blocking.</li><li style="margin:6px 0;">​<strong>Debounce</strong> buttons without waiting.</li><li style="margin:6px 0;">​<strong>Measure</strong> the worst-case time of loop(), and identify the call that sets it.</li><li style="margin:6px 0;">​<strong>Choose</strong> between modem sleep, light sleep and deep sleep for each idle period of your product, and <strong>implement</strong> the one you chose with a wake-up source.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — Why Blocking Breaks Products</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Non-blocking code works only if every check is quick. One slow function, even with no delay() in it, holds up everything else.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Counts as Blocking</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>blocking call</strong> is anything that makes the program wait before it can do anything else. Some are obvious, and some are hidden inside libraries:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Blocking call</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How long it can block</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Non-blocking alternative</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">delay(ms)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Exactly as long as you ask</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check millis() each pass</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Waiting in a while loop for a sensor to be ready</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Until the sensor responds, or forever</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check once per pass; use the sensor's interrupt</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reading a whole measurement at once</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The whole measurement time</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Read a few samples per pass</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connecting to WiFi and waiting</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Seconds, or longer if the network is gone</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Start the connection, then check its status each pass (D4)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Sending a full display frame over I²C</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">About 25 ms on esp\_watch at 400 kHz</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Send only when something changed</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The last row deserves attention because it contains no delay() at all.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's author measured a full display update at about <strong>25 ms</strong> at 400 kHz and about <strong>90 ms</strong> at 100 kHz. For those milliseconds the processor is busy moving bytes, and nothing else runs.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A motion sensor due every 20 ms will miss its slot whenever a full-screen update takes 25 ms. That is why "redraw only on change" matters for timing as well as for the bus load you calculated in B2.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — The millis() Pattern</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">"Has My Interval Passed?"</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">millis() returns the milliseconds since the board started [1]. As in Part 1, each task stores when it last ran and checks, on every pass through loop(), whether its interval has passed. Each check almost always answers "not yet", so loop() runs thousands of times a second.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Why now - last &gt;= period, and Not now &gt;= last + period</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">millis() is stored in an unsigned long, 32 bits on the ESP32. It counts up to 4,294,967,295 and then wraps back to zero:</div>

```text
2^32 ms = 4,294,967,296 ms ÷ 1000 ÷ 60 ÷ 60 ÷ 24 ≈ 49.7 days
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A watch left running for 50 days will see millis() wrap. Suppose a task ran at last = 4,294,967,290, with a 20 ms period:</div>

```text
Addition form:     last + period = 4,294,967,310, which does not fit, so it wraps to 14.
                   One millisecond later, now = 4,294,967,291, and "now >= 14" is TRUE.
                   The task fires on every pass until the counter wraps: far too often.

Subtraction form:  now − last is computed with the same wrap-around.
                   At now = 4,294,967,291: difference = 1   → not yet.
                   At now = 14 (after the wrap): difference = 20 → due, exactly on time.
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Unsigned subtraction wraps the same way the counter does, so now - last is always the true elapsed time. <strong>Always write the subtraction form.</strong></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Small Helper</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">When there are several periodic tasks, a tiny structure keeps them readable:</div>

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

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Three Peripherals, Three Rates</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Here is the plan for a watch with a motion sensor, a heart-rate sensor and a display, before any code:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Task</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">When it runs</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why that rate</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Motion sensor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every 20 ms, always</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Steps must never be missed</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate sensor</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every 40 ms, <strong>only during a measurement burst</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Measuring draws more than screen-on in the modelled budget (~44 mA vs ~36 mA, B3); between bursts the sensor is off</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Display</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Only when something shown has changed</strong>, and never while asleep</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A full frame costs about 25 ms of bus and processor time</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 1: How often does each run in a typical minute awake?</div>

```text
Motion:  60,000 ms ÷ 20 ms          = 3,000 reads per minute
Heart:   0 per minute, except during a 10 s burst: 10,000 ÷ 40 = 250 reads
Display: once per step shown, once per screen change, a few times per burst
         → say 60–120 redraws per minute while walking
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: How much time does each take?</strong> <strong>Example values:</strong> a motion read takes about 0.5 ms, close to the register-read time measured on the reference watch (see Part 3), and more than the 0.4 ms of pure bus time from B5's trace because of library overhead. A redraw is about 25 ms.</div>

```text
Motion:  3,000 × 0.5 ms       = 1,500 ms per minute  (2.5%)
Display: 120 × 25 ms          = 3,000 ms per minute  (5%)
         vs redrawing every 50 ms: 1,200 × 25 ms = 30,000 ms per minute (50%)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> With redraw-on-change, the processor is idle over 90% of the time, which is time it could spend in light sleep. Redrawing on a fixed fast schedule would spend half of every minute pushing pixels that did not change. The numbers make the design decision for you.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The complete sketch is in <a href="../assets/code/D2-nonblocking-watch/">assets/code/D2-nonblocking-watch/</a>, using the same Wokwi wiring as B5, with a mock heart-rate sensor. It compiles for the XIAO ESP32-C3. For this exercise, "next" changes screen and "previous" starts a 10 s heart-rate measurement, shortened from the 30 s assumed in B3's budget so you can test it quickly.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Turning the State Machine Into Code</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The heart of loop() is the state machine from D1, now combined with the tasks:</div>

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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Compare this with the broken function at the start. The measurement still lasts 10 seconds, but it no longer blocks for 10 seconds. It is a state, MEASURING, which the loop passes through thousands of times, reading a sample when one is due. Meanwhile the motion sensor keeps counting steps and the buttons keep working.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Notice the dirty flag. Anything that changes what the screen shows sets dirty = true: a new step on the step screen, a screen change, progress during a measurement. The display is redrawn at most once per pass, and only when needed. This one flag delivers B2's bus-load fix and this unit's timing fix together.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Debouncing Without Waiting</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A mechanical button does not switch cleanly. For a few milliseconds its contacts <strong>bounce</strong>, flickering between open and closed. Read it naively and one press counts as several. The common beginner fix, delay(50) after detecting a press, is blocking.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The non-blocking version remembers when the reading last changed, and only accepts it once it has been steady for a set time:</div>

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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">It is the same idea as Every: a quick check each pass, with time measured rather than waited for.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it.</div><div>Run the D2 sketch in Wokwi, press the buttons and move the motion sensor's slider. Which call sets the worst loop time? How close is it to the reference watch's measured 25 ms display update?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 3 — Keeping loop() Readable and Bounded</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Readable</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A good loop() reads like the flowchart from D1: a short list of steps, each one a function call or a small switch. If loop() grows past a screen, move pieces into functions named for what they do: readMotion(), handleButtons(), redraw(). The state machine's switch is the one part that is allowed to be long, because each case is one box on the diagram.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Bounded</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>bounded</strong> loop has a known worst-case time for one pass. That number matters because it is the longest any task can be kept waiting. If the worst pass is 25 ms and the motion sensor wants a read every 20 ms, one read will occasionally be late.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Measure it, as the example does with micros(), and compare it with your fastest task's period:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Worst loop time</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Fastest task period</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Verdict</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Well under the period</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">20 ms</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fine</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Close to the period</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">20 ms</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Occasional late reads; check whether it matters</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Over the period</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">20 ms</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reads will be missed; find and split the slow call</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On esp\_watch the obvious candidate for the worst case is a full display update: about 25 ms at 400 kHz. The author also measured that a loop of 200 register reads takes 92 to 101 ms, about 0.5 ms per read. That is the scale of a single sensor transaction: small, but not zero, and worth knowing when you add up everything one pass might do.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">If one call is too slow, split it. A display library that can send part of the screen, a sensor that can be read a few samples at a time, and a network connection that can be started and then checked (D4) all turn one long call into several short ones.</div>

---

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:center;line-height:1.7;"><div style="font-weight:700;color:#1e40af;">This cookbook will be continued in Part 2.</div></div>
