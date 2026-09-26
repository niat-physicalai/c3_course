# A2 — Operating Modes, Failure Behaviour and Architecture Decisions
## Deciding How the System Behaves Over Time, and Writing Down Why

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 1 — System Architecture
**Time:** ~1 hour · **You will produce:** a system state diagram, a failure mode table and three written decision records

---

### The Watch Is Not Always Doing the Same Thing

Your architecture from A1 shows *what* the system is made of. It does not show *when* each part is working. A watch spends most of the day asleep. It wakes for a few seconds when shaken, measures heart rate only when asked, and sometimes sits on a charger. Each of those situations draws a different current, shows something different on the screen, and can go wrong in a different way.

Now picture a student who takes the watch off halfway through a heart-rate reading. What should the screen say? The sensor is suddenly reading air. If nobody decided in advance, the firmware will do *something*, perhaps showing 212 bpm, perhaps freezing. Both are worse than a plain "no contact".

This unit covers three things: listing the states your system can be in, deciding what happens when something fails, and recording your big decisions so that you, and anyone after you, remember why they were made.

### What You Will Be Able to Do After This Reading

- **Draw** a system state diagram with states, the events that move between them, and what the device does in each.
- **Produce** a failure mode table that says, for each likely failure, how it is detected and what the wearer sees.
- **Choose** between graceful degradation and a hard stop for each failure, and justify the choice.
- **Decide** where health data lives and who can read it.
- **Write** an Architecture Decision Record with context, options, decision and consequences.

### What Part 1 Already Covered

Part 1 asked you to test your final project under abnormal conditions, such as unplugging a sensor or taking down the WiFi, and to check that it failed safely rather than silently. **What is new here** is deciding that behaviour *before* building, at the level of the whole system, and writing it down as states, a failure table and decision records.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## States: What Mode Is the System In?

A **state** is a mode the system stays in until something happens: asleep, awake, measuring. An **event** is the something that happens: a button press, a timeout, a low battery. A **transition** is the move from one state to another, caused by an event.

A **state diagram** shows all three. Each state is a box. Each arrow is a transition, labelled with the event that causes it. Beside each state, write what the system *does* while in it: which parts are powered, and what the screen shows.

Most wearables need these states:

| State | What the system does |
|---|---|
| Boot | Start up, check sensors, connect if needed |
| Awake (normal) | Screen on, respond to buttons |
| Measuring | Heart-rate sensor on, reading in progress |
| Asleep | Screen off, minimum power, waiting for a wake event |
| Low battery | Warn the wearer, switch off non-essential features |
| Charging | Show charge status; may run normally at the same time |
| Fault | A part has stopped working; show what still works |

Some of these are not separate modes but **overlays** that apply on top of another state. Charging is a good example: the watch can be awake *and* charging. Draw overlays as a note, not as a box, or your diagram fills up with copies of every state.

## Worked Example: The Reference Watch's States

We will reverse-engineer esp_watch's behaviour into a state diagram. Everything marked **recorded** comes from the author's description of the firmware. Everything marked **proposed** is a gap that the design has to fill.

<!-- REFPRODUCT:START -->
**What is recorded:** on first power-up the watch connects to WiFi once and fetches the time and weather, then keeps WiFi off. It has three screens, moved between with a "next" and a "previous" button. The screen turns off after 30 s with no input, and the watch sleeps. The motion sensor stays on during sleep so a shake wakes it. Heart rate is measured on request.

```text
                 power on
                    │
                    ▼
            ┌───────────────┐
            │     BOOT      │  connect WiFi once, fetch time + weather,
            └───────┬───────┘  then WiFi off                 (recorded)
                    │ done
                    ▼
            ┌───────────────┐   request HR    ┌───────────────┐
  ┌────────►│     AWAKE     │────────────────►│   MEASURING   │
  │         │ screen on,    │◄────────────────│ heart-rate    │
  │         │ 3 screens     │  result / abort │ sensor on     │
  │         └───────┬───────┘                 └───────────────┘
  │                 │ 30 s with no input              (recorded)
  │                 ▼
  │         ┌───────────────┐
  └─────────│    ASLEEP     │  screen off, motion sensor on
   shake or │               │                           (recorded)
   button   └───────────────┘

  Overlays (proposed):  battery low → LOW BATTERY
                        USB connected → CHARGING
                        sensor stops answering → FAULT
```
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — firmware behaviour on low battery, while charging, and on sensor failure is not recorded in REFERENCE-PRODUCT.md; shown here as proposed states only -->

Now walk the diagram and ask questions:

1. **What if WiFi fails at boot?** The diagram has only one arrow out of BOOT, labelled "done". A failed connection needs its own arrow, and a decision: go to AWAKE with no time shown, or retry? Nothing is recorded, so this is a gap.
2. **What if the watch is taken off during MEASURING?** The only way back is "result / abort". The design needs to say how an abort is detected (see the failure table below).
3. **What wakes the watch?** A shake or a button. Both are events the motion sensor or buttons must still detect while the rest is asleep. That is why the motion sensor stays powered, and why it appears in the sleep current in A0's battery estimate.

<!-- REFPRODUCT:START -->
The hardware already supports the proposed overlays. A voltage divider on one ADC pin exists specifically to measure the battery, because the XIAO board has no battery-measurement pin of its own. The XIAO can also run from the battery with USB connected, and its onboard charger handles charging. What is missing is a written decision about what the firmware *does* with that information.
<!-- REFPRODUCT:END -->

> **Try it: Find the missing arrows.** Take the esp_watch diagram above.
> 1. **Predict.** How many events can happen in AWAKE that the diagram does not show?
> 2. **Do.** List every event you can think of in AWAKE: button presses, timeouts, battery changes, USB, sensor errors. For each, decide which state it leads to.
> 3. **Explain.** How many were missing? Which of them would a student only discover by accident, after building?
>
> **Extra challenge:** Can a battery-low event happen in MEASURING? What should win: finishing the reading or protecting the battery?

## Failure Behaviour

Things will go wrong. The questions are *which* things, how the system notices, and what the wearer sees.

There are two broad responses. **Graceful degradation** keeps as much working as possible and says plainly what is not: *"No heart-rate signal. Is the watch on your wrist?"* A **hard stop** shuts a function down completely because continuing would be unsafe or misleading, such as refusing to run when the battery is dangerously low.

Choose graceful degradation by default. Choose a hard stop when carrying on could damage something, or would show a number the wearer might trust and act on.

A **failure mode table** records each likely failure:

<!-- REFPRODUCT:START -->
| Failure | How it is detected | What the wearer sees | Response |
|---|---|---|---|
| Watch taken off mid-reading | Heart-rate signal becomes too weak or erratic to give a result | "No contact" instead of a number | Degrade: abandon the reading |
| Battery reaches cut-off | Battery-sense voltage below a threshold | Warning, then screen off | Hard stop, before the cell is damaged |
| A sensor stops responding | A read on the I²C bus fails or times out | "--" for that value; other screens still work | Degrade: retry later |
| No WiFi at first boot | Connection times out | Time not set; a clear "no time" indicator | Degrade: everything else still works |
| Display stops updating | **Cannot be detected by writing to it** | Frozen or corrupted screen | See note below |
<!-- REFPRODUCT:END -->

The last row is a real lesson from the reference watch.

<!-- REFPRODUCT:START -->
On esp_watch's breadboard prototype, one version of the heart-rate module dragged the shared I²C bus down to 1.82 V. The motion sensor then failed 80% of its reads, and the display showed corrupted output. The firmware never reported an error for the display, because nothing is ever read back from it. A write that goes nowhere looks exactly like a write that worked. The author's rule afterwards: **judge the bus's health by a device you read from, not by the display.** In failure-table terms, the display's failure is detected indirectly, through a sensor that shares the same bus.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/breadboard.jpg -->
![esp_watch breadboard prototype, with the heart-rate module, motion sensor and display sharing one I²C bus](../reference-files/images/breadboard.jpg)

<!-- ASSET:PLACEHOLDER reference-files/images/i2c-debug-output.png -->
![Serial output from the i2c_debug sketch, showing the bus scan and per-device read-failure counts](../reference-files/images/i2c-debug-output.png)

Notice that every "how it is detected" entry needs something to exist in the design: a battery-sense pin, a timeout on bus reads, a check on signal quality. A failure you cannot detect is a failure you cannot handle, so this table also tells the hardware and firmware what they must provide.

## Where Health Data Lives

Heart rate is **health data**. Before any code exists, decide three things and write them down:

1. **Where does it live?** On the device only, on a phone, or on a server?
2. **Who can read it?** Only the wearer, or anyone who picks up the watch, joins the network, or has access to the server?
3. **Does it leave the device at all?** If so, over what, and is it protected on the way?

The safest data is data that never leaves the device. Every copy you send elsewhere is a copy you must protect. India's Digital Personal Data Protection Act, 2023 places duties on anyone who processes people's personal data, including taking reasonable security safeguards to prevent a data breach [2]. Your student project is not a commercial service, but designing as if it were is good practice, and essential if it ever becomes one.

<!-- REFPRODUCT:START -->
Going by esp_watch's intended behaviour, heart-rate readings stay on the watch. WiFi is used once, at first boot, to fetch the time and weather. That is a strong privacy position, and it came almost for free from a decision made for battery reasons. The cost is the one A1 exposed: no history leaves the device, so there is nowhere to see a semester's trend.
<!-- REFPRODUCT:END -->

## Architecture Decision Records

You have already made several big decisions: which connection to use, where data lives, what happens on failure. In three weeks you will not remember why. In three months a teammate will want to undo one of them, not knowing the reason it was made.

An **Architecture Decision Record** (ADR) is a short document recording one decision. The format comes from Michael Nygard [1] and has four main parts:

| Part | What it contains |
|---|---|
| Context | The situation and forces that made a decision necessary |
| Options considered | The realistic alternatives, including the one you rejected |
| Decision | What you chose, in one or two sentences |
| Consequences | What becomes easier, what becomes harder, and what you now must do |

Give each ADR a number and a short title, and never delete one. If you change your mind, write a new ADR that **supersedes** the old one. The history is the point.

### Worked Example: An ADR for the Reference Watch

<!-- REFPRODUCT:START -->
> **ADR-002: Use WiFi only once, at first boot**
>
> **Status:** Accepted
>
> **Context.** The watch must show the time, and the author wanted the local weather. Neither changes quickly enough to need a constant connection. Battery life is dominated by what runs all day (A0), and a radio that stays on would be one of the largest loads. The ESP32-C3 on the XIAO board has WiFi and Bluetooth built in.
>
> **Options considered.**
> 1. WiFi always on, updating regularly: always fresh, but a large and constant battery cost.
> 2. Bluetooth to a phone app: low radio power, but a phone app must be written and maintained.
> 3. WiFi once at first boot, then off: nearly free in battery terms, with no app to build.
>
> **Decision.** Option 3. Connect once at first boot, fetch the time and weather, then turn WiFi off.
>
> **Consequences.**
> - Easier: battery budget; no phone app; heart-rate data never leaves the device.
> - Harder: the time is never corrected after boot unless the watch reboots; the weather goes stale; no data can be sent off the watch later.
> - Now required: a decision on what to show if WiFi fails at boot (a gap in the state diagram); a way to enter WiFi details without editing code.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — this ADR is reconstructed from recorded behaviour; the author's actual reasons for WiFi-at-boot-only are not recorded in REFERENCE-PRODUCT.md -->

Notice what the consequences section does. It turns one decision into a list of follow-on work. The first "now required" item is exactly the missing arrow found in the state diagram, which shows how the three deliverables of this unit check one another.

Two more decisions in esp_watch are worth writing up as ADRs for practice:

<!-- REFPRODUCT:START -->
- **Modules on a carrier board, rather than chips placed directly.** The display, both sensors and the microcontroller are pre-made modules mounted on a custom board. That makes design faster and hand soldering possible, but costs board area and height: the stack is 14.044 mm.
- **Keep the MPU-6050 motion sensor**, even though the manufacturer declared it obsolete in 2023. Modules are still widely sold, but a future version will need a different sensor and new driver code.
<!-- REFPRODUCT:END -->

---

# Putting It All Together

## Applying What You Have Learned

**1. Draw your state diagram.** Start from the seven common states and remove any that do not apply. Label every arrow with its event. Beside each state, note what is powered and what the screen shows. Draw charging and similar conditions as overlays.

**2. Build your failure mode table.** Include at least these: the device removed mid-measurement, the battery at cut-off, a sensor not responding, the network unavailable. For each, fill in detection, what the user sees, and whether it degrades or stops. If you cannot say how something is detected, write down what the hardware or firmware must add.

**3. Decide where health data lives.** Answer the three questions in writing.

**4. Write three ADRs** for the three biggest decisions in your design so far. One of them must be your connection choice from A1.

**Deliverable:** save all four in your design pack as `A2-behaviour-and-decisions.md`.

## Self-Check

Open `A2-behaviour-and-decisions.md` and answer each item Y or N.

1. Every arrow in the state diagram is labelled with an event. — Y/N
2. Every state has a note of what is powered and what the screen shows. — Y/N
3. Every state has at least one way out, except a deliberate final state. — Y/N
4. The failure table includes removal mid-measurement, battery cut-off, sensor failure and no network. — Y/N
5. Every failure has a detection method, or a note of what must be added to detect it. — Y/N
6. Every failure is marked as degrade or stop. — Y/N
7. The health-data section answers where it lives, who can read it, and whether it leaves the device. — Y/N
8. There are three ADRs, each with context, at least two options, a decision and consequences. — Y/N
9. One ADR records the connection choice from A1. — Y/N

---

## Check Your Understanding

**1.** A student's state diagram has AWAKE, ASLEEP and MEASURING, plus separate boxes called AWAKE+CHARGING, ASLEEP+CHARGING and MEASURING+CHARGING. What is the better design?

- A. Keep all six boxes, because they are all real states.
- B. Draw charging as an overlay that applies to any state, and keep three boxes.
- C. Remove charging, because it is handled by hardware.
- D. Make charging a state that the device must enter before sleeping.

<details>
<summary>Answer</summary>

**B.** Charging can happen at the same time as the other states, so it is an overlay. Drawing it as copies of every state doubles the diagram and makes it easy to forget a transition. **A** is technically possible but grows badly with every new overlay. **C** is wrong because the firmware still needs to show charge status and may change its behaviour. **D** invents a restriction the wearer never asked for.

</details>

**2.** A watch shows "72 bpm" after being taken off mid-reading, because it averaged the last few values. Which response is correct?

- A. Keep it, because 72 is a normal value.
- B. Detect the loss of contact from the weak signal and show "no contact" instead of a number.
- C. Shut the watch down.
- D. Show the last good value with no warning.

<details>
<summary>Answer</summary>

**B.** This is graceful degradation: the reading cannot be trusted, so the watch says so plainly and keeps working. **A** is the most dangerous option, because a normal-looking wrong number is believed. **C** is a hard stop for a problem that endangers nothing. **D** hides the failure from the wearer.

</details>

**3.** On a shared I²C bus, a firmware engineer checks that every write to the display succeeds, and concludes the bus is healthy. Why is this not enough?

- A. Displays do not use I²C.
- B. Writing to a display gives no evidence that data arrived. A broken bus can accept writes that go nowhere, so bus health must be judged by a device you read back from.
- C. The display is on a different bus.
- D. It is enough, as long as the display shows something.

<details>
<summary>Answer</summary>

**B.** A write with no read-back cannot confirm anything. The reference watch's display showed corrupted output while reporting nothing, and the fault was only visible because the motion sensor, which *is* read from, failed 80% of its reads. **A** and **C** are factually wrong for the reference design. **D** is wrong because "something" on a display may be corrupted without the firmware knowing.

</details>

**4.** A team's ADR reads: *"Decision: use BLE."* Nothing else is written. Six weeks later a teammate proposes switching to WiFi. Which missing section would most help the team decide?

- A. The ADR's number
- B. The context and consequences, which say why BLE was chosen and what switching would give up
- C. The date
- D. The author's name

<details>
<summary>Answer</summary>

**B.** Without context and consequences, nobody can tell whether the original reasons still hold, so the teammate is arguing against nothing. **A**, **C** and **D** help with tracking, but none of them explains the decision, which is the whole point of an ADR.

</details>

**5.** A watch sends each heart-rate reading to a cloud server so a friend can view it on a website. Which design choice is weakest from a privacy point of view?

- A. Readings stay on the watch and are shown only on its screen.
- B. Readings go to the wearer's phone over an encrypted Bluetooth link.
- C. Readings go to a server over an encrypted link, and the website needs the wearer's login.
- D. Readings go to a server without encryption, and anyone with the web address can view them.

<details>
<summary>Answer</summary>

**D.** The data travels unprotected and anyone with the address can read it, which fails both "protected on the way" and "who can read it". **A** is the strongest: the data never leaves the device. **B** keeps the data close and protected. **C** sends it further, but protects it in transit and controls who can see it.

</details>

---

## What You Can Now Do, and What Comes Next

- Draw a state diagram that shows how your system behaves over a day, including overlays such as charging.
- Build a failure table that says how each failure is detected and what the wearer sees.
- Decide where health data lives and who can read it.
- Record a decision so that it can be understood, and challenged, months later.

The idea to carry forward: **every failure you cannot detect is a failure you cannot handle.** The failure table tells the hardware and firmware what they must provide.

This completes your System Architecture Document: specification, context diagram, subsystem breakdown, allocation table, state diagram, failure table and ADRs. In [B0 — Hardware Architecture](../02-hardware-electronics-design/B0-hardware-architecture.md) you will take the hardware subsystems down to the level of individual connections, the drawing a schematic is built from.

---

## References

1. Michael Nygard. *Documenting Architecture Decisions*, Cognitect blog, 15 November 2011 (the original ADR format: title, context, decision, status, consequences). https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
2. Government of India, Ministry of Law and Justice. *The Digital Personal Data Protection Act, 2023 (No. 22 of 2023)*, published by MeitY (including the obligation to take reasonable security safeguards against personal data breaches). https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
