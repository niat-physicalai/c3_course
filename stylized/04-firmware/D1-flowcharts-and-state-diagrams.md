<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">D1 — Design Before Code: Flowcharts and State Diagrams</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Drawing the Behaviour First, So the Code Has Something to Match</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 4 — Firmware <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a main-loop flowchart and a device state diagram</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">"It Mostly Works" Is a Design Problem</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Most student firmware grows like this. You get the display working. You add a button, with an if. You add the heart-rate reading, with another if and a flag. The screen should turn off after 30 seconds, so there is a timer and another flag. Then pressing the button while measuring does something strange, so you add a check for that. After a week, loop() is 200 lines of nested conditions, and nobody, including you, can say what the watch will do if the wearer shakes it during a measurement while the battery is low.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit turns your A2 state list into a <strong>flowchart</strong> and a <strong>state diagram</strong> in standard notation. You draw and review them before coding, then check the code against them.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Draw</strong> a flowchart for procedural logic with standard symbols, clear decisions and a readable loop.</li><li style="margin:6px 0;">​<strong>Produce</strong> a state diagram with states, events, transitions, and entry and exit actions.</li><li style="margin:6px 0;">​<strong>Review</strong> a diagram for missing transitions and unhandled events before any code exists.</li><li style="margin:6px 0;">​<strong>Trace</strong> each transition in a state diagram to a line of code, and find the ones that are missing.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — Flowcharts</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">When to Use One</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>flowchart</strong> shows a procedure: a sequence of steps with decisions and loops, run from start to finish. Use it for logic that happens in order: the main loop, a start-up sequence, a calibration routine, a retry with backoff.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Do not use a flowchart for behaviour that depends on history, meaning "what happens next depends on what mode we are in". That is a state diagram's job (Part 2). Trying to show modes in a flowchart is how you get a chart of crossing arrows and flags.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Symbols</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A handful of shapes covers almost every firmware flowchart:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Shape</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Meaning</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Example</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Rounded rectangle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Start or end</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Start, Return</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Rectangle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A process step</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Read motion sensor</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Diamond</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A decision with labelled exits</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Time to redraw? Yes / No</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Parallelogram</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Input or output</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Print steps to Serial</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Small circle</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connector to another part of the chart</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Keep these rules and the chart stays readable:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Every diamond has exactly two exits, both labelled</strong>, usually Yes and No.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Flow goes top to bottom</strong>, with loops returning up one side, not across the middle.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>One idea per box.</strong> "Read sensor, update steps and redraw" is three boxes.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>No box without an exit</strong>, except End.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: A Main Loop That Does Three Things at Different Rates</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A watch reads the motion sensor 50 times a second, redraws the screen once a second, and checks the buttons every pass. Here is its main loop, designed before any code:</div>

```text
          ┌───────────┐
          │   Start   │
          └─────┬─────┘
                ▼
       ┌────────────────┐
       │ Set up bus,    │
       │ sensors, display│
       └────────┬───────┘
                ▼
       ┌────────────────┐◄──────────────────────────────┐
       │ now = millis() │                               │
       └────────┬───────┘                               │
                ▼                                       │
         ◇ 20 ms since      ◇── No ──┐                  │
           last motion read?         │                  │
                │ Yes                │                  │
                ▼                    │                  │
       ┌────────────────┐            │                  │
       │ Read motion,   │            │                  │
       │ update steps   │            │                  │
       └────────┬───────┘            │                  │
                ▼◄───────────────────┘                  │
         ◇ Button pressed? ◇── No ──┐                   │
                │ Yes               │                   │
                ▼                   │                   │
       ┌────────────────┐           │                   │
       │ Change screen  │           │                   │
       └────────┬───────┘           │                   │
                ▼◄──────────────────┘                   │
         ◇ 1 s since      ◇── No ──────────────────────►┤
           last redraw?                                 │
                │ Yes                                   │
                ▼                                       │
       ┌────────────────┐                               │
       │ Redraw screen  │───────────────────────────────┘
       └────────────────┘
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check the chart against the rules.</strong> Every diamond has two labelled exits. Every path returns to the top. Nothing in the loop waits: each diamond checks the clock and moves on. That last property is the one D2 builds its whole approach on, and you can see it here before a line of code exists.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Spot the anti-pattern.</strong> Suppose the redraw box instead said "Redraw screen, then wait 1 s". The chart would still be valid, but during that wait no motion reads happen and no button presses are noticed. The flowchart makes the problem visible as a box that takes a long time, sitting on a path everything else must pass through.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — State Diagrams</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">States, Events, Transitions and Actions</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>state diagram</strong> shows behaviour that depends on the current mode. You met its parts in A2. Here is the complete notation:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Element</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Meaning</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Drawn as</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>State</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A mode the device stays in until something happens</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Rounded box</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Initial state</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Where the machine starts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Filled dot with an arrow</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Event</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Something that happens: a press, a timeout, a result</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Label on an arrow</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Guard</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A condition that must also be true</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">[in square brackets] after the event</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Transition</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The move from one state to another</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Arrow</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Entry action</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Done once, every time the state is entered</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">entry / action inside the box</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Exit action</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Done once, every time the state is left</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">exit / action inside the box</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Entry and exit actions are what make state diagrams tidy. "Turn the display off" does not need to appear on every arrow into ASLEEP. It is written once, as ASLEEP's entry action, and it happens however the watch got there.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: esp\_watch as a State Machine</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is esp\_watch's recorded behaviour from A2 (BOOT, AWAKE, MEASURING), redrawn with entry and exit actions. One state is added that esp\_watch does not have yet: <strong>ASLEEP</strong>, entered after 30 s with no input and left on a button press. It shows how a timeout and a wake-up are drawn. The entry and exit actions, the abort path and ASLEEP are this unit's design choices, not recorded firmware.</div>

```text
      ●
      │
      ▼
┌──────────────────────────┐
│ BOOT                     │
│ entry / connect WiFi,    │
│   fetch time + weather,  │
│   WiFi off               │
└────────────┬─────────────┘
             │ done
             ▼
┌──────────────────────────┐   request HR      ┌──────────────────────────┐
│ AWAKE                    │──────────────────►│ MEASURING                │
│ entry / display on,      │                   │ entry / sensor LEDs on   │
│   restart 30 s timer     │◄──────────────────│ exit  / sensor LEDs off  │
│ button / change screen,  │  result or abort  └──────────────────────────┘
│   restart timer          │
└──────┬───────────▲───────┘
       │ 30 s      │ button
       │ no input  │
       ▼           │
┌──────────────────┴───────┐
│ ASLEEP                   │
│ entry / display off      │
│                          │
└──────────────────────────┘
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Notice the line inside AWAKE: button / change screen, restart timer. That is an <strong>internal transition</strong>: an event handled without leaving the state, so AWAKE's entry action does not run again. Drawing it this way stops you writing a pointless "leave AWAKE and come back" in code.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Reviewing the Diagram Before Coding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A state diagram is cheap to review, and review is where it earns its keep. Ask the same three questions of every state:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Every event, every state.</strong> For each event the device can receive, what happens in this state? If the answer is "nothing", say so deliberately.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Every way out.</strong> Can the device always leave this state? A state with no exit is a trap.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Every entry and exit.</strong> Is anything switched on in the entry action and never switched off?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Run question 1 on MEASURING for three of its events:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Event in MEASURING</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Diagram says</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Decision needed</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Button</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Nothing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Abort the reading, or ignore it?</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">30 s timeout</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Nothing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Should a long reading keep the screen on?</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Result</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">→ AWAKE</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Covered</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two gaps, found in five minutes, with no code written. Each one is a decision that the firmware would otherwise make by accident.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">From Diagram to Code</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A state diagram translates into code almost mechanically: an enum listing the states, a switch on the current state, and one function that performs every transition so that exit and entry actions are never forgotten. The complete sketch is in <a href="../assets/code/D1-state-machine.ino">assets/code/D1-state-machine.ino</a>. It takes events typed into the Serial Monitor, so it runs on any ESP32 or in Wokwi.</div>

```cpp
void enter(State next) {
  // Exit actions
  if (state == State::Measuring) Serial.println("  exit: heart-rate LEDs off");
  if (state == State::Asleep)    Serial.println("  exit: display on");

  Serial.printf("%s -> %s\n", name(state), name(next));
  state = next;
  lastInput = millis();

  // Entry actions
  if (state == State::Measuring) Serial.println("  entry: heart-rate LEDs on");
  if (state == State::Asleep)    Serial.println("  entry: display off");
}

void loop() {
  int c = Serial.available() ? Serial.read() : -1;

  switch (state) {
    case State::Boot:
      break;  // left in setup()
    case State::Awake:
      if (c == 'h') enter(State::Measuring);
      else if (c == 'b') lastInput = millis();          // stays AWAKE, timer restarts
      else if (millis() - lastInput >= SCREEN_TIMEOUT_MS) enter(State::Asleep);
      break;
    case State::Measuring:
      if (c == 'r') enter(State::Awake);                // result / abort
      break;
    case State::Asleep:
      if (c == 'b') enter(State::Awake);                // button
      break;
  }
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The check: <strong>every arrow in the diagram is exactly one enter(...) call, and every enter(...) call is an arrow.</strong> The diagram has five arrows between states. The full sketch has five enter calls: four in loop() above and one in setup(), which the excerpt omits. The internal transition (button in AWAKE) is a timer restart, not an enter, which also matches.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Declare the enum at the top of the file, before any function, or the Arduino IDE fails with "does not name a type" (see D0's error table).</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>​<strong>Try it: Diff the code against the diagram.</strong> Run the sketch in Wokwi or on any ESP32, and type events into the Serial Monitor.</div><div>1. <strong>Predict.</strong> What will the sketch print if you type h then b while measuring?</div><div>2. <strong>Do.</strong> Try it, then try h followed by waiting 30 s.</div><div>3. <strong>Explain.</strong> Both are gaps from the MEASURING event table above. Which behaviour did the code choose by default? Is that the behaviour you would have chosen?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">For Reference: Sequence Diagrams</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A third notation, the <strong>sequence diagram</strong>, shows several modules exchanging messages over time, with time running downwards. You won't need one for your deliverable, but you will meet them in datasheets and documentation. Here is heart rate on request, using the layers from D0:</div>

```text
 Wearer      Application        HeartRate        MAX30102 driver
   │ press button │   service         │                  │
   │─────────────►│ start()          │                  │
   │              │─────────────────►│ enable LEDs      │
   │              │                  │─────────────────►│
   │              │   ... repeated while measuring ...   │
   │              │                  │ readSamples()    │
   │              │                  │─────────────────►│
   │              │  bpm, or         │◄- - - - - - - - -│
   │              │  "no contact"    │                  │
   │ show result  │◄- - - - - - - - -│                  │
   │◄- - - - - - -│ stop()           │ disable LEDs     │
   │              │─────────────────►│─────────────────►│
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Solid arrows are calls; dashed arrows are replies. Notice that the application never talks to the driver directly, which is the D0 layering made visible.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Diagrams as Text</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">You can draw these diagrams in draw.io, or write them as <strong>text</strong> using Mermaid, which turns a short description into a diagram [1]. Text diagrams live alongside your code, show changes clearly in version control, and can be pasted into the Mermaid Live Editor to view [2]. Here is esp\_watch's state diagram in Mermaid:</div>

```text
stateDiagram-v2
    [*] --> Boot
    Boot --> Awake : done
    Awake --> Measuring : request HR
    Measuring --> Awake : result / abort
    Awake --> Asleep : 30 s no input
    Asleep --> Awake : button
```

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Discipline: Draw, Review, Then Code</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The diagrams only help if they come first and stay true. Work in this order:</div>

```text
Draw  ──►  Review  ──►  Code  ──►  Diff code against diagram
  ▲           │                          │
  └── fix ────┘◄──────── mismatch ───────┘
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Draw</strong> the flowchart and state diagram.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Review</strong> them with the three state questions and the event table. Fix the diagram, not the code.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Code</strong> from the diagram, one state or one message at a time.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Diff</strong>: count arrows against enter calls. Every mismatch is either a missing piece of code or a missing piece of design. Decide which, and fix it in the right place.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Diagrams go out of date only when behaviour is changed in code alone. Change the diagram first and it stays true.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Flowchart your main loop.</strong> Show every task, its rate, and the decision that triggers it. Check that no box waits.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Draw your device state diagram.</strong> Start from A2. Add entry and exit actions, guards where needed, and internal transitions. Draw charging and similar conditions as overlays.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Fill the event table.</strong> States as rows, every event as columns, every cell decided. Resolve every blank in the diagram.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> save your flowchart, state diagram and event table in your design pack as D1-behaviour-design.md. Text diagrams (Mermaid) or images are both acceptable.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open D1-behaviour-design.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every diamond in the flowchart has two labelled exits. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. No flowchart box waits or delays. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. The state diagram has an initial state. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every state has at least one way out, or is a deliberate final state. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every state that switches something on in its entry action switches it off in its exit action. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The event table has no blank cells. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Every arrow is labelled with an event. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Every task in the flowchart shows the rate or event that triggers it. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A student's flowchart for "heart-rate measurement mode" has diamonds labelled "Is mode HR?", "Was the button pressed while in HR?" and "Was the previous mode sleep?". What is the best advice?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Add more diamonds to cover every case.</li><li style="margin:6px 0;">B. This behaviour depends on the current mode, so it belongs in a state diagram, not a flowchart.</li><li style="margin:6px 0;">C. Replace the diamonds with rectangles.</li><li style="margin:6px 0;">D. Merge the diamonds into one.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Questions about the current or previous mode are the sign of state-dependent behaviour. A state diagram represents modes directly, without flags and nested checks. <strong>A</strong> makes the tangle bigger. <strong>C</strong> breaks the notation, since decisions must be diamonds. <strong>D</strong> hides the complexity rather than removing it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> In a state diagram, "turn the display off" appears on all three arrows leading into ASLEEP. What is the better notation?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Leave it on the arrows.</li><li style="margin:6px 0;">B. Make it ASLEEP's entry action, so it happens however the device arrives.</li><li style="margin:6px 0;">C. Make it AWAKE's entry action.</li><li style="margin:6px 0;">D. Put it in a separate flowchart.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> An entry action is written once and runs on every arrival, so a fourth arrow added later cannot forget it. <strong>A</strong> works until someone adds an arrow without the action. <strong>C</strong> puts the action in the wrong state. <strong>D</strong> separates the behaviour from the state it belongs to.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A diagram shows five arrows between states. The code has four calls to enter(...). What should you do first?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Delete an arrow from the diagram.</li><li style="margin:6px 0;">B. Find the arrow with no matching enter call, and decide whether the code is missing a transition or the design was wrong.</li><li style="margin:6px 0;">C. Add an extra enter call anywhere.</li><li style="margin:6px 0;">D. Nothing; one mismatch is acceptable.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A mismatch is information: either a transition was never implemented, or the diagram shows something the product should not do. Deciding which, and fixing it in the right place, is the whole point of the diff. <strong>A</strong> and <strong>C</strong> force the counts to match without understanding why they did not. <strong>D</strong> accepts an unknown behaviour into the product.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> In MEASURING, pressing the button is not shown on the diagram. The code ignores it. Which is true?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The design is complete, because the code handles it.</li><li style="margin:6px 0;">B. The behaviour was decided by accident. The event table should record whether ignoring the button is the intended behaviour.</li><li style="margin:6px 0;">C. Buttons cannot be pressed during measurement.</li><li style="margin:6px 0;">D. The button should always go to ASLEEP.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Ignoring may well be right, but it should be a decision, written in the event table, not a side effect of which if statements happen to exist. <strong>A</strong> mistakes "the code does something" for "the design says what should happen". <strong>C</strong> is false. <strong>D</strong> is one possible decision, stated without any reasoning.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> Which situation is best shown as a sequence diagram rather than a state diagram?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The watch's modes: awake, asleep, measuring</li><li style="margin:6px 0;">B. The order of calls between the application, a WiFi service, the router and a weather server at first boot, including what happens if the server does not reply</li><li style="margin:6px 0;">C. Whether the watch is charging</li><li style="margin:6px 0;">D. The decision to redraw the screen once a second</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> It is a conversation between several participants in a specific order, with a failure alternative, which is exactly what a sequence diagram shows. <strong>A</strong> is the classic state diagram. <strong>C</strong> is an overlay on a state diagram. <strong>D</strong> is a flowchart decision in the main loop.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="D2-non-blocking-logic-and-sleep.md">D2 — Non-Blocking Logic and Sleep Modes</a> you will turn this state diagram into code that runs every task at its own rate, and sleeps when there is nothing to do.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Mermaid. State diagrams (stateDiagram-v2 syntax). https://mermaid.js.org/syntax/stateDiagram.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Mermaid. Mermaid Live Editor (online editor that renders Mermaid text as diagrams). https://mermaid.live/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
