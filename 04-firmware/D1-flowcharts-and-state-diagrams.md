# D1 — Design Before Code: Flowcharts and State Diagrams
## Drawing the Behaviour First, So the Code Has Something to Match

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Firmware
**Time:** ~1 hour · **You will produce:** a main-loop flowchart and a device state diagram

---

### "It Mostly Works" Is a Design Problem

Most student firmware grows like this. You get the display working. You add a button, with an `if`. You add the heart-rate reading, with another `if` and a flag. The screen should turn off after 30 seconds, so there is a timer and another flag. Then pressing the button while measuring does something strange, so you add a check for that. After a week, `loop()` is 200 lines of nested conditions, and nobody, including you, can say what the watch will do if the wearer shakes it during a measurement while the battery is low.

The code is not wrong so much as undesigned. Nobody decided the behaviour before writing it, so the behaviour is whatever the code happens to do.

In A2 you listed your product's states and failures. This unit turns that list into two precise diagrams, a **flowchart** and a **state diagram**, using notation standard enough that anyone can review them. Then comes the discipline that makes them worth drawing: draw it, review it, *then* write the code, and check the code against the drawing.

### What You Will Be Able to Do After This Reading

- **Draw** a flowchart for procedural logic with standard symbols, clear decisions and a readable loop.
- **Produce** a state diagram with states, events, transitions, and entry and exit actions.
- **Review** a diagram for missing transitions and unhandled events before any code exists.
- **Trace** each transition in a state diagram to a line of code, and find the ones that are missing.

### What Part 1 Already Covered

Part 1 introduced flowcharts informally and had you write `if` statements, loops and functions in Arduino C++. **What is new here** is using two standard design notations deliberately: drawing behaviour before coding it, reviewing the drawing for gaps, and then checking the code against it line by line.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — Flowcharts

## When to Use One

A **flowchart** shows a *procedure*: a sequence of steps with decisions and loops, run from start to finish. Use it for logic that happens in order: the main loop, a start-up sequence, a calibration routine, a retry with backoff.

Do not use a flowchart for behaviour that depends on history, meaning "what happens next depends on what mode we are in". That is a state diagram's job (Part 2). Trying to show modes in a flowchart is how you get a chart of crossing arrows and flags.

## The Symbols

A handful of shapes covers almost every firmware flowchart:

| Shape | Meaning | Example |
|---|---|---|
| Rounded rectangle | Start or end | `Start`, `Return` |
| Rectangle | A process step | `Read motion sensor` |
| Diamond | A decision with labelled exits | `Time to redraw?` Yes / No |
| Parallelogram | Input or output | `Print steps to Serial` |
| Small circle | Connector to another part of the chart | `A` |

Keep these rules and the chart stays readable:

1. **Every diamond has exactly two exits, both labelled**, usually *Yes* and *No*.
2. **Flow goes top to bottom**, with loops returning up one side, not across the middle.
3. **One idea per box.** "Read sensor, update steps and redraw" is three boxes.
4. **No box without an exit**, except End.

## Worked Example: A Main Loop That Does Three Things at Different Rates

A watch reads the motion sensor 50 times a second, redraws the screen once a second, and checks the buttons every pass. Here is its main loop, designed before any code:

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

**Check the chart against the rules.** Every diamond has two labelled exits. Every path returns to the top. Nothing in the loop waits: each diamond checks the clock and moves on. That last property is the one D2 builds its whole approach on, and you can see it here before a line of code exists.

**Spot the anti-pattern.** Suppose the redraw box instead said *"Redraw screen, then wait 1 s"*. The chart would still be valid, but during that wait no motion reads happen and no button presses are noticed. The flowchart makes the problem visible as a box that takes a long time, sitting on a path everything else must pass through.

---

# Part 2 — State Diagrams

## States, Events, Transitions and Actions

A **state diagram** shows behaviour that depends on the current mode. You met its parts in A2. Here is the complete notation:

| Element | Meaning | Drawn as |
|---|---|---|
| **State** | A mode the device stays in until something happens | Rounded box |
| **Initial state** | Where the machine starts | Filled dot with an arrow |
| **Event** | Something that happens: a press, a timeout, a result | Label on an arrow |
| **Guard** | A condition that must also be true | `[in square brackets]` after the event |
| **Transition** | The move from one state to another | Arrow |
| **Entry action** | Done once, every time the state is entered | `entry / action` inside the box |
| **Exit action** | Done once, every time the state is left | `exit / action` inside the box |

Entry and exit actions are what make state diagrams tidy. "Turn the display off" does not need to appear on every arrow into ASLEEP. It is written once, as ASLEEP's entry action, and it happens however the watch got there.

## Worked Example: esp_watch as a State Machine

<!-- REFPRODUCT:START -->
Start from the recorded behaviour of esp_watch (from A2): one WiFi fetch at first boot, three screens, a 30 s screen timeout into sleep, the motion sensor left on so a shake wakes the watch, and heart rate measured on request.

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
       │ 30 s      │ shake or button
       │ no input  │
       ▼           │
┌──────────────────┴───────┐
│ ASLEEP                   │
│ entry / display off,     │
│   motion wake on         │
└──────────────────────────┘
```
<!-- REFPRODUCT:END -->

Notice the line inside AWAKE: `button / change screen, restart timer`. That is an **internal transition**: an event handled *without* leaving the state, so AWAKE's entry action does not run again. Drawing it this way stops you writing a pointless "leave AWAKE and come back" in code.

## Reviewing the Diagram Before Coding

A state diagram is cheap to review, and review is where it earns its keep. Ask the same three questions of every state:

1. **Every event, every state.** For each event the device can receive, what happens in this state? If the answer is "nothing", say so deliberately.
2. **Every way out.** Can the device always leave this state? A state with no exit is a trap.
3. **Every entry and exit.** Is anything switched on in the entry action and never switched off?

Run question 1 on MEASURING. The events are: button, shake, 30 s timeout, request HR, result, battery low, USB connected.

| Event in MEASURING | Diagram says | Decision needed |
|---|---|---|
| Button | Nothing | Abort the reading, or ignore it? |
| Shake | Nothing | Probably ignore; it would spoil the reading anyway |
| 30 s timeout | Nothing | Should a long reading keep the screen on? |
| Battery low | Nothing | Finish or abort? (A2's failure table) |
| Result | → AWAKE | Covered |

Four gaps, found in five minutes, with no code written. Each one is a decision that the firmware would otherwise make by accident.

<!-- FACT:VERIFY esp_watch — how watch_ui_test.ino handles button presses, timeouts and low battery during a heart-rate measurement is not recorded in REFERENCE-PRODUCT.md -->

> **Try it: The event table.** Take your own A2 state diagram.
> 1. **Predict.** How many state-and-event combinations will have no defined behaviour?
> 2. **Do.** Make a table with your states as rows and every event as columns. Fill each cell with the target state, an internal action, or "ignored (deliberate)". Leave a cell blank only if you genuinely have not decided.
> 3. **Explain.** How many blanks were there? Which of them could cause a visible bug?
>
> **Extra challenge:** Add "sensor stops responding" as an event. Which states need a transition to a FAULT state, and what does FAULT's entry action show?

## From Diagram to Code

A state diagram translates into code almost mechanically: an `enum` listing the states, a `switch` on the current state, and one function that performs every transition so that exit and entry actions are never forgotten. The complete sketch is in [`assets/code/D1-state-machine.ino`](../assets/code/D1-state-machine.ino). It takes events typed into the Serial Monitor, so it runs on any ESP32 or in Wokwi.

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
  if (state == State::Asleep)    Serial.println("  entry: display off, motion wake on");
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
      if (c == 's' || c == 'b') enter(State::Awake);    // shake or button
      break;
  }
}
```

Now the check from the verification stack becomes simple: **every arrow in the diagram should appear as exactly one `enter(...)` call, and every `enter(...)` call should be an arrow in the diagram.** Count them. The diagram has five arrows between states (BOOT→AWAKE, AWAKE→MEASURING, MEASURING→AWAKE, AWAKE→ASLEEP, ASLEEP→AWAKE) and the code has five `enter` calls, one of them in `setup()`. The internal transition (button in AWAKE) appears as a timer restart, not as an `enter`, which matches the diagram too.

<!-- REFPRODUCT:START -->
Notice where the `enum` sits: at the top of the file, before any function. esp_watch's author hit the Arduino IDE error `'WxType' does not name a type` because the IDE inserts function prototypes above the first function, and an `enum` declared later is not yet known there. Declaring enums first avoids it.
<!-- REFPRODUCT:END -->

> **Try it: Diff the code against the diagram.** Run the sketch in Wokwi or on any ESP32, and type events into the Serial Monitor.
> 1. **Predict.** What will the sketch print if you type `h` then `b` while measuring?
> 2. **Do.** Try it, then try `h` followed by waiting 30 s.
> 3. **Explain.** Both are gaps from the MEASURING event table above. Which behaviour did the code choose by default? Is that the behaviour you would have chosen?

<!-- MEDIA
type: screenshot
id: D1-02
caption: The state-machine sketch running, with each transition printed in the Serial Monitor
brief: Wokwi (or the Arduino IDE Serial Monitor) running D1-state-machine.ino on an ESP32-C3.
  The serial output shows, in order: "BOOT: connect WiFi once, fetch time and weather, WiFi
  off", "BOOT -> AWAKE", then after typing h: "AWAKE -> MEASURING" and "entry: heart-rate
  LEDs on", then after typing r: "exit: heart-rate LEDs off", "MEASURING -> AWAKE", then
  after a 30 s wait: "AWAKE -> ASLEEP" and "entry: display off, motion wake on", then after
  typing s: "exit: display on", "ASLEEP -> AWAKE". The input box with a typed character
  visible. Crop to the serial output.
-->

---

## For Reference: Sequence Diagrams

A third notation, the **sequence diagram**, shows *several* modules exchanging messages over time, with time running downwards. You won't need one for your deliverable, but you will meet them in datasheets and documentation. Here is heart rate on request, using the layers from D0:

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

Solid arrows are calls; dashed arrows are replies. Notice that the application never talks to the driver directly, which is the D0 layering made visible.

## Diagrams as Text

You can draw these diagrams in draw.io, or write them as **text** using Mermaid, which turns a short description into a diagram [1]. Text diagrams live alongside your code, show changes clearly in version control, and can be pasted into the Mermaid Live Editor to view [2]. Here is esp_watch's state diagram in Mermaid:

```text
stateDiagram-v2
    [*] --> Boot
    Boot --> Awake : done
    Awake --> Measuring : request HR
    Measuring --> Awake : result / abort
    Awake --> Asleep : 30 s no input
    Asleep --> Awake : shake or button
```

<!-- MEDIA
type: screenshot
id: D1-01
caption: esp_watch's state diagram rendered in the Mermaid Live Editor
brief: mermaid.live in a browser, split view. Left pane: the stateDiagram-v2 text from
  the reading (Boot, Awake, Measuring, Asleep with the five labelled transitions).
  Right pane: the rendered diagram, with the start dot, four rounded state boxes and
  labelled arrows. No account or advertising banner visible if possible. Light theme.
-->

## The Discipline: Draw, Review, Then Code

The diagrams only help if they come first and stay true. Work in this order:

```text
Draw  ──►  Review  ──►  Code  ──►  Diff code against diagram
  ▲           │                          │
  └── fix ────┘◄──────── mismatch ───────┘
```

1. **Draw** the flowchart and state diagram.
2. **Review** them with the three state questions and the event table. Fix the diagram, not the code.
3. **Code** from the diagram, one state or one message at a time.
4. **Diff**: count arrows against `enter` calls. Every mismatch is either a missing piece of code or a missing piece of design. Decide which, and fix it in the right place.

A common belief is that diagrams go out of date the moment coding starts, so they are not worth maintaining. They go out of date when changes are made in code only. If a behaviour change starts with the diagram, the diagram stays true, and it becomes the fastest way for anyone, including a reviewer of your design pack, to understand the firmware.

---

# Putting It All Together

## Applying What You Have Learned

**1. Flowchart your main loop.** Show every task, its rate, and the decision that triggers it. Check that no box waits.

**2. Draw your device state diagram.** Start from A2. Add entry and exit actions, guards where needed, and internal transitions. Draw charging and similar conditions as overlays.

**3. Fill the event table.** States as rows, every event as columns, every cell decided. Resolve every blank in the diagram.

**4. Diagnose.** A classmate's state diagram has a state CHARGING with arrows in from AWAKE and ASLEEP, and no arrows out. What is wrong, and what are two ways to fix it?

<details>
<summary>Answer</summary>

CHARGING is a **trap**: once entered, the device can never leave, even after USB is unplugged. Either add an exit transition ("USB removed → previous state", which needs the previous state remembered), or, better for a watch that works while charging, draw charging as an **overlay** that applies on top of AWAKE and ASLEEP rather than a separate state.

</details>

**Deliverable:** save your flowchart, state diagram and event table in your design pack as `D1-behaviour-design.md`. Text diagrams (Mermaid) or images are both acceptable.

## Self-Check

Open `D1-behaviour-design.md` and answer each item Y or N.

1. Every diamond in the flowchart has two labelled exits. — Y/N
2. No flowchart box waits or delays. — Y/N
3. The state diagram has an initial state. — Y/N
4. Every state has at least one way out, or is a deliberate final state. — Y/N
5. Every state that switches something on in its entry action switches it off in its exit action. — Y/N
6. The event table has no blank cells. — Y/N
7. Every arrow is labelled with an event. — Y/N
8. Every task in the flowchart shows the rate or event that triggers it. — Y/N

---

## Check Your Understanding

**1.** A student's flowchart for "heart-rate measurement mode" has diamonds labelled "Is mode HR?", "Was the button pressed while in HR?" and "Was the previous mode sleep?". What is the best advice?

- A. Add more diamonds to cover every case.
- B. This behaviour depends on the current mode, so it belongs in a state diagram, not a flowchart.
- C. Replace the diamonds with rectangles.
- D. Merge the diamonds into one.

<details>
<summary>Answer</summary>

**B.** Questions about the current or previous mode are the sign of state-dependent behaviour. A state diagram represents modes directly, without flags and nested checks. **A** makes the tangle bigger. **C** breaks the notation, since decisions must be diamonds. **D** hides the complexity rather than removing it.

</details>

**2.** In a state diagram, "turn the display off" appears on all three arrows leading into ASLEEP. What is the better notation?

- A. Leave it on the arrows.
- B. Make it ASLEEP's entry action, so it happens however the device arrives.
- C. Make it AWAKE's entry action.
- D. Put it in a separate flowchart.

<details>
<summary>Answer</summary>

**B.** An entry action is written once and runs on every arrival, so a fourth arrow added later cannot forget it. **A** works until someone adds an arrow without the action. **C** puts the action in the wrong state. **D** separates the behaviour from the state it belongs to.

</details>

**3.** A diagram shows five arrows between states. The code has four calls to `enter(...)`. What should you do first?

- A. Delete an arrow from the diagram.
- B. Find the arrow with no matching `enter` call, and decide whether the code is missing a transition or the design was wrong.
- C. Add an extra `enter` call anywhere.
- D. Nothing; one mismatch is acceptable.

<details>
<summary>Answer</summary>

**B.** A mismatch is information: either a transition was never implemented, or the diagram shows something the product should not do. Deciding which, and fixing it in the right place, is the whole point of the diff. **A** and **C** force the counts to match without understanding why they did not. **D** accepts an unknown behaviour into the product.

</details>

**4.** In MEASURING, pressing the button is not shown on the diagram. The code ignores it. Which is true?

- A. The design is complete, because the code handles it.
- B. The behaviour was decided by accident. The event table should record whether ignoring the button is the intended behaviour.
- C. Buttons cannot be pressed during measurement.
- D. The button should always go to ASLEEP.

<details>
<summary>Answer</summary>

**B.** Ignoring may well be right, but it should be a decision, written in the event table, not a side effect of which `if` statements happen to exist. **A** mistakes "the code does something" for "the design says what should happen". **C** is false. **D** is one possible decision, stated without any reasoning.

</details>

**5.** Which situation is best shown as a sequence diagram rather than a state diagram?

- A. The watch's modes: awake, asleep, measuring
- B. The order of calls between the application, a WiFi service, the router and a weather server at first boot, including what happens if the server does not reply
- C. Whether the watch is charging
- D. The decision to redraw the screen once a second

<details>
<summary>Answer</summary>

**B.** It is a conversation between several participants in a specific order, with a failure alternative, which is exactly what a sequence diagram shows. **A** is the classic state diagram. **C** is an overlay on a state diagram. **D** is a flowchart decision in the main loop.

</details>

---

## What You Can Now Do, and What Comes Next

- Draw flowcharts for procedures and state diagrams for modes, and know which to use.
- Use entry, exit and internal transitions to keep a state diagram small and correct.
- Find gaps with an event table before they become bugs.
- Check code against a diagram arrow by arrow.

The idea to carry forward: **if a behaviour is not in the diagram, it was decided by accident.** The event table turns every accident into a decision.

In [D2 — Non-Blocking Logic and Sleep Modes](D2-non-blocking-logic-and-sleep.md) you will turn this state diagram into code that runs every task at its own rate, and sleeps when there is nothing to do.

---

## References

1. Mermaid. *State diagrams* (stateDiagram-v2 syntax). https://mermaid.js.org/syntax/stateDiagram.html
2. Mermaid. *Mermaid Live Editor* (online editor that renders Mermaid text as diagrams). https://mermaid.live/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
