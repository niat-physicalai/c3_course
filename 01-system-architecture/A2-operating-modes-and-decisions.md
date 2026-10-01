# A2 — Operating Modes, Failure Behaviour and Decisions
## Deciding How the System Behaves Over Time, and Writing Down Why

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 1 — System Architecture
**Time:** ~1 hour · **You will produce:** a system state diagram, a failure mode table and two decision notes

---

### The Watch Is Not Always Doing the Same Thing

Your architecture from A1 shows *what* the system is made of. It does not show *when* each part is working. A watch spends most of the day asleep. It wakes for a few seconds when shaken, measures heart rate only when asked, and sometimes sits on a charger. Each of those situations draws a different current, shows something different on the screen, and can go wrong in a different way.

Now picture a student who takes the watch off halfway through a heart-rate reading. What should the screen say? The sensor is suddenly reading air. If nobody decided in advance, the firmware will do *something*, perhaps showing 212 bpm, perhaps freezing. Both are worse than a plain "no contact".

This unit covers three things: listing the states your system can be in, deciding what happens when something fails, and writing down your big decisions so you can explain them later.

### What You Will Be Able to Do After This Reading

- **Draw** a system state diagram with states, the events that move between them, and what the device does in each.
- **Produce** a failure mode table that says, for each likely failure, how it is detected and what the wearer sees.
- **Choose** between graceful degradation and a hard stop for each failure, and justify the choice.
- **Decide** where health data lives and who can read it.
- **Write** a short decision note: the choice, the options, why, and what it costs.

Part 1 had you test a finished project by unplugging sensors or WiFi. Here you decide that behaviour *before* building.

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
**What is recorded:** on first power-up the watch connects to WiFi once and fetches the time and weather, then keeps WiFi off. It has three screens, moved between with a "next" and a "previous" button. Heart rate is measured on request. The watch is **always on**: it has no sleep state.

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
            │     AWAKE     │────────────────►│   MEASURING   │
            │ screen on,    │◄────────────────│ heart-rate    │
            │ 3 screens     │  result / abort │ sensor on     │
            └───────────────┘                 └───────────────┘
                                                      (recorded)

  Overlays (proposed):  battery low → LOW BATTERY
                        USB connected → CHARGING
                        sensor stops answering → FAULT
```
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — firmware behaviour on low battery, while charging, and on sensor failure is not recorded in REFERENCE-PRODUCT.md; shown here as proposed states only -->
<!-- PLACEHOLDER:FEATURE sleep / shake-to-wake — if added, an ASLEEP state goes here: AWAKE → ASLEEP after a timeout, ASLEEP → AWAKE on shake or button -->

Now walk the diagram and ask questions:

1. **What if WiFi fails at boot?** The diagram has only one arrow out of BOOT, labelled "done". A failed connection needs its own arrow, and a decision: go to AWAKE with no time shown, or retry? Nothing is recorded, so this is a gap.
2. **What if the watch is taken off during MEASURING?** The only way back is "result / abort". The design needs to say how an abort is detected (see the failure table below).
3. **What happens when nobody is using it?** Nothing: the watch stays awake with the screen on, which costs battery all day. A sleep state, and something to wake it, is the obvious next addition. D2 teaches the sleep modes you would use.

<!-- REFPRODUCT:START -->
Not every proposed overlay fits esp_watch's hardware. The XIAO charges the cell on board and can run from the battery with USB connected, and the watch uses a protected cell that cuts itself off when flat. But the XIAO has no battery-measurement pin and esp_watch adds none, so the firmware cannot see the battery level. A LOW BATTERY state would first need a divider on an ADC pin. Writing that down is exactly what the state diagram is for.
<!-- REFPRODUCT:END -->

## Failure Behaviour

Things will go wrong. The questions are *which* things, how the system notices, and what the wearer sees.

There are two broad responses. **Graceful degradation** keeps as much working as possible and says plainly what is not: *"No heart-rate signal. Is the watch on your wrist?"* A **hard stop** shuts a function down completely because continuing would be unsafe or misleading, such as refusing to run when the battery is dangerously low.

Choose graceful degradation by default. Choose a hard stop when carrying on could damage something, or would show a number the wearer might trust and act on.

A **failure mode table** records each likely failure. Here is a **proposed** table for esp_watch. Only the display row describes recorded behaviour; the rest is not recorded.

<!-- REFPRODUCT:START -->
| Failure | How it is detected | What the wearer sees | Response |
|---|---|---|---|
| Watch taken off mid-reading | Heart-rate signal becomes too weak or erratic to give a result | "No contact" instead of a number | Degrade: abandon the reading |
| Battery reaches cut-off | Not detectable: esp_watch has no battery measurement | Screen goes dark with no warning | Hard stop by the protected cell's own cut-off |
| A sensor stops responding | A read on the I²C bus fails or times out | "--" for that value; other screens still work | Degrade: retry later |
| No WiFi at first boot | Connection times out | Time not set; a clear "no time" indicator | Degrade: everything else still works |
| Display stops updating | **Cannot be detected by writing to it** | Frozen or corrupted screen | See note below |
<!-- REFPRODUCT:END -->

The last row is a real lesson from the reference watch.

<!-- REFPRODUCT:START -->
On esp_watch's breadboard, a faulty heart-rate module corrupted the shared I²C bus. The display showed garbage, but the firmware reported nothing, because nothing is read back from a display (full story in B3 and D5). **Judge bus health by a device you read from.** So the display's failure is detected indirectly, through a sensor on the same bus.
<!-- REFPRODUCT:END -->

<!-- ASSET: public repo asset/breadboard/photo_9.jpeg -->
![esp_watch breadboard prototype, with the heart-rate module, motion sensor and display sharing one I²C bus](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/breadboard/photo_9.jpeg)

<!-- ASSET:PLACEHOLDER reference-files/images/i2c-debug-output.png -->
![Serial output from the i2c_debug sketch, showing the bus scan and per-device read-failure counts](../reference-files/images/i2c-debug-output.png)

Notice that every "how it is detected" entry needs something to exist in the design: a timeout on bus reads, a check on signal quality. The battery row shows the other side: esp_watch has no battery-sense pin, so it cannot warn before cut-off. A failure you cannot detect is a failure you cannot handle, so this table also tells the hardware and firmware what they must provide.

## Where Health Data Lives

Heart rate is **health data**. Before any code exists, decide three things and write them down:

1. **Where does it live?** On the device only, on a phone, or on a server?
2. **Who can read it?** Only the wearer, or anyone who picks up the watch, joins the network, or has access to the server?
3. **Does it leave the device at all?** If so, over what, and is it protected on the way?

The safest data is data that never leaves the device. Every copy you send elsewhere is a copy you must protect. India's Digital Personal Data Protection Act, 2023 places duties on anyone who processes people's personal data, including taking reasonable security safeguards to prevent a data breach [1]. Your student project is not a commercial service, but designing as if it were is good practice, and essential if it ever becomes one.

<!-- REFPRODUCT:START -->
Going by esp_watch's intended behaviour, heart-rate readings stay on the watch. WiFi is used once, at first boot, to fetch the time and weather. That is a strong privacy position, and it comes as a side effect of keeping WiFi off. The cost is the one A1 exposed: no history leaves the device, so there is nowhere to see a semester's trend.
<!-- REFPRODUCT:END -->

## Writing Down Your Decisions

You have already made several big decisions: which connection to use, where data lives, what happens on failure. In three weeks you will not remember why, and when someone reviews your design pack they will ask.

A **decision note** records one decision in four short parts:

| Part | What it contains |
|---|---|
| Decision | What you chose, in one sentence |
| Options considered | The realistic alternatives, including the ones you rejected |
| Why | The reason this option won, tied to a requirement from A0 |
| What it costs | What becomes harder, and any follow-on work it creates |

If you change your mind later, write a new note that says which one it replaces. Don't delete the old note: the reasoning is still useful.

### Worked Example: A Reconstructed Decision Note for the Reference Watch

The author's actual reasons are not recorded, so this note is rebuilt from the watch's behaviour.

<!-- REFPRODUCT:START -->
> **Decision: use WiFi only once, at first boot.**
>
> **Options considered.** (1) WiFi always on: always fresh, but a large, constant battery cost. (2) Bluetooth to a phone app: low radio power, but a phone app to write. (3) WiFi once at first boot, then off.
>
> **Why.** The watch needs the time and the weather, and neither changes fast enough to need a constant connection. Battery life is dominated by what runs all day (A0), so option 3 is nearly free in battery terms and needs no app.
>
> **What it costs.** The time is never corrected after boot, the weather goes stale, and heart-rate data never leaves the watch. It also creates work: a decision on what to show if WiFi fails at boot (a gap in the state diagram), and a way to enter WiFi details without editing code.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — this note is reconstructed from recorded behaviour; the author's actual reasons for WiFi-at-boot-only are not recorded in REFERENCE-PRODUCT.md -->

The "what it costs" part is the useful one. It turns one decision into a list of follow-on work, and its first item is exactly the missing arrow found in the state diagram.

---

# Putting It All Together

## Applying What You Have Learned

**1. Draw your state diagram.** Start from the seven common states and remove any that do not apply. Label every arrow with its event. Beside each state, note what is powered and what the screen shows. Draw charging and similar conditions as overlays.

**2. Build your failure mode table.** Include at least these: the device removed mid-measurement, the battery at cut-off, a sensor not responding, the network unavailable. For each, fill in detection, what the user sees, and whether it degrades or stops. If you cannot say how something is detected, write down what the hardware or firmware must add.

**3. Decide where health data lives.** Answer the three questions in writing.

**4. Write two decision notes** for the two biggest decisions in your design so far. One of them must be your connection choice from A1.

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
8. There are two decision notes, each with the decision, at least two options, a reason and a cost. — Y/N
9. One note records the connection choice from A1. — Y/N

---

## Check Your Understanding

**1.** A student's state diagram has AWAKE, ASLEEP and MEASURING, plus separate boxes called AWAKE+CHARGING, ASLEEP+CHARGING and MEASURING+CHARGING. What is the better design?

- A. Keep all six boxes, because they are all real states.
- B. Draw charging as an overlay that applies to any state, and keep three boxes.
- C. Remove charging, because it is handled by hardware.
- D. Make charging a state that the device must enter before sleeping.

<details>
<summary>Answer</summary>

**B.** Charging happens alongside other states, so it is an overlay. Copying every state doubles the diagram and invites missed transitions. **A** grows worse with each new overlay. **C** is wrong: firmware must still show charge status. **D** invents a restriction nobody asked for.

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

- A. It is enough, because the display is the busiest device on the bus.
- B. Display writes are never read back, so a broken bus can look healthy. Check a device you read from.
- C. It is enough if the bus runs at 100 kHz instead of 400 kHz.
- D. It is enough, as long as the display shows something.

<details>
<summary>Answer</summary>

**B.** A write with no read-back confirms nothing, so a corrupted bus can look fine from the display side. Read a register from a sensor on the same bus. **A** and **C** do not change what the check can see. **D** fails because the screen can show corrupted output without the firmware knowing.

</details>
**4.** A student's decision note reads: *"Decision: use BLE."* Nothing else is written. Six weeks later they wonder whether to switch to WiFi. Which missing part would help most?

- A. A number for the note
- B. The "why" and "what it costs", which say why BLE was chosen and what switching would give up
- C. The date
- D. The student's name

<details>
<summary>Answer</summary>

**B.** Without the reason and the cost, nobody can tell whether the original reasons still hold. **A**, **C** and **D** help with tracking, but none explains the decision, which is the whole point of the note.

</details>

**5.** Four students decide where their watch's heart-rate readings go. Which design is weakest on privacy?

- A. Readings stay on the watch and are shown only on its screen.
- B. Readings go to the wearer's phone over an encrypted Bluetooth link.
- C. Readings go to a server over an encrypted link, and the website needs the wearer's login.
- D. Readings go to a server without encryption, and anyone with the web address can view them.

<details>
<summary>Answer</summary>

**D.** The data travels unprotected and anyone with the address can read it, which fails both "protected on the way" and "who can read it". **A** is the strongest: the data never leaves the device. **B** keeps the data close and protected. **C** sends it further, but protects it in transit and controls who can see it.

</details>

---

## What Comes Next

This completes your System Architecture Document: specification, context diagram, subsystem breakdown, allocation table, state diagram, failure table and decision notes. In [B0 — Choosing the Right Sensor](../02-sensing-and-hardware-architecture/B0-choosing-sensors.md) you will decide what your product must sense, and with which sensor, before any circuit is drawn.

---

## References

1. Government of India, Ministry of Law and Justice. *The Digital Personal Data Protection Act, 2023 (No. 22 of 2023)*, published by MeitY (including the obligation to take reasonable security safeguards against personal data breaches). https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
