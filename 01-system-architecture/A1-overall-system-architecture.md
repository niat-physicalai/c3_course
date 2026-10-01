# A1 — Overall System Architecture
## Drawing the Whole System on One Page, and Giving Every Requirement an Owner

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 1 — System Architecture
**Time:** ~1 hour · **You will produce:** a context diagram, a subsystem breakdown and a requirement allocation table

---

### A List of Requirements Is Not Yet a Design

You now have a specification: numbered requirements, each with a number and a check method. It tells you *what* the product must achieve. It does not tell you what the product is *made of*, what it talks to, or which part is responsible for which requirement.

Suppose your spec asks for a semester of resting heart rate. Does that history live on the watch, a phone or a server? Each answer is a different product. If nobody asks, the requirement falls through the gap and nobody builds it.

This unit gives you one page that shows the whole system, and a table that makes such gaps impossible to miss.

### What You Will Be Able to Do After This Reading

- **Draw** a context diagram showing your product, everything outside it that it interacts with, and what flows between them.
- **Break down** your product into standard subsystems.
- **Allocate** every requirement from your specification to one owning subsystem, and find any requirement with no owner.
- **Decide** roughly where each piece of work happens (device, phone or server), and **predict** what the user sees when the link between them drops.
- **Estimate** how much data your product produces, and use the estimate to decide what to process on the device.

### What Part 1 Already Covered

Part 1 drew systems as a chain (*sensors → ESP32 → WiFi → MQTT → cloud → dashboard*). New here: a boundary around your product, and a table giving every requirement an owner.

---

# Part 1 — Drawing the Boundary

## Inside and Outside

Every product has a **system boundary**: a line with everything you design and build on the inside, and everything you do not control on the outside.

The outside matters as much as the inside. Your watch does not design the wearer's wrist, the hostel WiFi router or the phone charger, but it depends on all of them. Each is an **external actor**: a person or system outside the boundary that your product exchanges something with. That something might be information, energy or physical contact.

A useful test: *could I change it by editing my design files?* If yes, it is inside. If no, it is outside, and your design must cope with whatever it does.

For a wrist-worn device, the external actors usually include:

| External actor | What crosses the boundary |
|---|---|
| The wearer | Button presses and wrist movement in; displayed information out |
| The wearer's skin | Pulse signal and motion in; pressure and heat both ways |
| A charger | Electrical energy in |
| A WiFi router | Network traffic both ways |
| A phone | Data both ways, if the product uses one |
| An internet service | Time, weather or stored history, if the product uses one |

A common mistake is to treat the phone or the server as "part of my product" without saying so. If your requirement needs an app, that app is either inside the boundary (you must design it) or outside it (someone else's app you depend on). Both are allowed. Leaving it unstated is not.

## The Context Diagram

A **context diagram** shows your product as a single box in the centre, surrounded by its external actors, with labelled arrows for what flows between them [1]. It shows nothing inside the box yet. Its only job is to make the boundary and the outside world visible on one page.

Four rules keep it useful:

1. **One box for your product.** Do not draw its insides here.
2. **Every actor from your spec appears.** If the spec mentions charging, a charger appears.
3. **Every arrow is labelled with *what* flows**, such as "heart-rate reading" or "5 V charging power", not *how* it travels.
4. **Arrow direction means something.** Draw a two-way arrow only if things genuinely flow both ways.

<!-- REFPRODUCT:START -->
Here is the context diagram for the reference watch, **esp_watch**. When first switched on, it connects to WiFi once to fetch the time and the weather, then keeps WiFi off. It charges over USB-C, and its heart-rate sensor on the underside of the board reads the pulse through the skin.

```text
                         ┌──────────────────┐
                         │      Wearer      │
                         └───┬──────────▲───┘
     button presses          │          │  time, weather, steps,
                             ▼          │  heart rate on screen
┌──────────────┐     ┌──────────────────┴─┐     ┌──────────────┐
│ USB charger  │────►│                    │◄───►│ WiFi router  │
└──────────────┘     │     esp_watch      │     └──────┬───────┘
 charging power      │                    │  once, at  │ internet
                     └─────────▲──────────┘  first boot▼
                               │              ┌───────────────────┐
                 pulse, motion │              │ Time and weather  │
                         ┌─────┴──────┐       │ services          │
                         │ Wrist/skin │       └───────────────────┘
                         └────────────┘
```
<!-- REFPRODUCT:END -->

<!-- REFPRODUCT:START -->
At first boot esp_watch sets its clock (shown in IST) and fetches the current temperature and weather code from the free **Open-Meteo** forecast API, then turns WiFi off.
<!-- REFPRODUCT:END -->

Notice what is *not* in this diagram: there is no phone and no server that stores the wearer's data. That is a design decision, and in Part 2 you will see what it costs.

You can draw your own diagram on paper and photograph it, or use a free tool such as draw.io [2].

<!-- MEDIA
type: screenshot
id: A1-01
caption: A context diagram for a wrist-worn tracker, drawn in draw.io
brief: draw.io open in a browser, full window, blank canvas with the "General" shape
  library visible on the left. In the centre, a single rounded rectangle labelled
  "Hostel activity watch". Around it, five rectangles: "Wearer", "Wrist / skin",
  "USB charger", "Phone app", "Cloud history service". Labelled arrows between the
  centre box and each actor: "button presses" (in), "heart rate, steps on screen" (out),
  "pulse, motion" (in from wrist), "charging power" (in), "daily summary" (out to
  phone), "semester history" (phone to cloud). The arrow label text box is being
  edited, with the cursor visible, to show how labels are added. Light theme, no
  personal account details visible.
-->

---

# Part 2 — Splitting the Inside into Subsystems

## Seven Standard Subsystems

Now open the box. A **subsystem** is a part of the product with a clear job, one you could describe in a sentence and hand to a single person. Most connected devices can be split into the same seven:

| Subsystem | Its job | Typical contents in a wearable |
|---|---|---|
| Sensing | Turn physical quantities into signals | Heart-rate sensor, motion sensor |
| Processing | Run the firmware and make decisions | Microcontroller |
| Power | Store, charge, regulate and switch energy | Battery, charger, regulator, power switch |
| Connectivity | Exchange data with the outside | WiFi or Bluetooth radio and antenna |
| Local user interface | Let the wearer see and control it | Display, buttons |
| Enclosure | Hold, protect and present everything | Case, strap, sensor window |
| Backend | Store and process data away from the device | Phone app, server, cloud database |

> **Teaching model.** These seven are a starting point, not a law. A product with a motor would add an "actuation" subsystem. A very simple product might merge connectivity into processing. Use the list to make sure nothing is forgotten, then adjust it to fit your product.

Two of these are regularly forgotten. The **enclosure** is treated as "the box it goes in later", yet it decides whether the heart-rate sensor touches the skin. The **backend** is forgotten because it is not on the circuit board. If a requirement needs data to outlive the device, or to be seen somewhere other than the wrist, a backend exists whether you drew it or not.

## The Reference Watch, Broken Down

<!-- REFPRODUCT:START -->
Here is esp_watch split into the seven subsystems:

```text
┌──────────────────────────── esp_watch ─────────────────────────────┐
│                                                                     │
│  SENSING                 PROCESSING              LOCAL UI           │
│  MAX30102 heart rate ──► XIAO ESP32-C3 ────────► SSD1306 display    │
│  MPU-6050 motion ──────► (firmware)    ◄──────── 2 buttons          │
│        (shared I²C bus)       │                                     │
│                               │                                     │
│  POWER                        │                 CONNECTIVITY        │
│  LiPo cell ─► slide switch ─► │ ◄─────────────► WiFi radio on the   │
│  charger + 3.3 V regulator    │                 XIAO, external      │
│  (on the XIAO); protected cell│                 antenna             │
│                                                                     │
│  ENCLOSURE: 3D-printed case, lid with 4 openings, sensor underneath │
└─────────────────────────────────────────────────────────────────────┘
   BACKEND: none of its own. Uses public time and weather services.
```
<!-- REFPRODUCT:END -->

<!-- ASSET: public repo asset/pcb/pcb_top.png -->
![esp_watch circuit board, top view: the display, motion sensor, ESP32-C3 board, buttons and power switch](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/pcb_top.png)

In the render you can see sensing, processing, local UI and power. Connectivity is mostly inside the ESP32-C3 board, with the antenna on a cable. The enclosure and backend do not appear, so a photo cannot replace the diagram.

## Allocating Every Requirement

A **requirement allocation table** lists every requirement in your spec and names the subsystem that **owns** it: the one responsible if the requirement is not met. Other subsystems may **support** it, but only one owns it.

If two subsystems share a requirement equally, each assumes the other is handling it.

Three situations need special handling:

- **Budget requirements.** Battery life, cost, weight and thickness are not delivered by one subsystem; every subsystem uses up part of the budget. Give the owner role to the subsystem that manages the budget (power for battery life, enclosure for thickness), or to "System" when no single subsystem does, as with cost. List every subsystem that draws on it as supporting.
- **Orphans.** A requirement that no subsystem can own is an **orphaned requirement**. It will not be built unless you add a subsystem, change the requirement, or move it out of version 1.
- **Unused subsystems.** A subsystem that owns or supports no requirement is either serving a requirement you forgot to write, or it is unnecessary. Either way, write down which.

## Worked Example: Holding esp_watch Against a Problem Statement

We will test esp_watch against the hostel problem statement from A0: *"Hostel students cannot easily see how active they are, or how their resting heart rate changes through a semester."* esp_watch was not designed for this exact statement, so this is a fair test of what the method reveals.

**Step 1: List the requirements.** These are **example values**, a short spec for the problem statement:

| ID | Requirement |
|---|---|
| FR-01 | Show the time of day |
| FR-02 | Show heart rate on request, 40–180 bpm |
| FR-03 | Count steps during the day |
<!-- PLACEHOLDER:FEATURE shake-to-wake — | FR-xx | Wake the screen when the wrist is shaken | -->
| FR-04 | Show how resting heart rate has changed over the semester |
| NFR-01 | Heart rate within ±5 bpm, wearer sitting still |
| NFR-03 | ≥ 2 days between charges with usage pattern UP-1 |
| NFR-04 | Charge from a USB-C phone charger |
| NFR-07 | Total thickness ≤ 16 mm including the case |

**Step 2: Give each requirement an owner, and list its supporters.**

<!-- REFPRODUCT:START -->
| ID | Owner | Supporting | How esp_watch meets it |
|---|---|---|---|
| FR-01 | Processing | Connectivity, Local UI | Firmware keeps time; WiFi sets it once at first boot |
| FR-02 | Sensing | Processing, Local UI, Enclosure | MAX30102 on the underside; firmware calculates bpm |
| FR-03 | Sensing | Processing | MPU-6050 motion sensor; firmware counts steps |
| FR-04 | **none** | — | **Orphan.** Nothing stores readings across a semester |
| NFR-01 | Sensing | Enclosure | Needs firm skin contact and blocked outside light |
| NFR-03 | Power | every subsystem | Sleep current dominates (see A0) |
| NFR-04 | Power | Enclosure | USB-C on the XIAO, reached from the left side of the case |
| NFR-07 | Enclosure | Sensing, Processing, Local UI, Power | Board alone is 14.044 mm high, leaving ~2 mm for the case |
<!-- REFPRODUCT:END -->

**Step 3: Look for orphans.** FR-04 has no owner. To show a semester's trend, readings must be stored for months and then displayed as a trend. esp_watch has no storage subsystem for history and no backend. The requirement is the heart of the problem statement, and nothing in the design delivers it.

There are three honest ways out:

1. **Add a backend**, such as a phone app or a server that the watch uploads to.
2. **Make processing own it**: store a few bytes per day in the watch's own memory and draw a simple trend on the display.
3. **Move it out of version 1**, and say so in the spec, accepting that version 1 only partly solves the problem.

The best choice depends on how much data is involved (Part 3).

**Step 4: Look for unused subsystems.** Connectivity supports only FR-01, setting the clock. esp_watch also fetches the weather, but no requirement in this spec asks for weather. So either a requirement is missing, or part of the connectivity work serves nothing in this problem statement.

**Check.** 9 requirements: 8 with owners, 1 orphan. Every existing subsystem appears at least once.

NFR-07 is also in trouble. The board stack leaves about 2 mm for the whole case (E2 covers the stack). The enclosure owns a number it cannot meet, so the fix lies with the subsystems that spend the budget.

---

# Part 3 — Three Rough Decisions

The architecture needs three decisions early, even if they are only rough. You will refine each one later in the course.

## Where Does the Work Happen?

For each job your product does, decide roughly where it runs: on the **device**, on a **phone**, or on a **server**. Then ask the question that matters most: *what does the wearer see when the link between them drops?*

| Work done on… | Strengths | When the link drops |
|---|---|---|
| Device only | Works anywhere, no dependence on others | Nothing changes |
| Phone | Big screen, easy graphs, more memory | Watch keeps working; the history on the phone stops updating |
| Server | Data survives a lost phone; can be seen anywhere | Watch and phone must buffer until the link returns, or data is lost |

The rule of thumb: **anything the wearer needs at the moment belongs on the device.** Heart rate on request, the time and the step count must still work in a basement lab with no signal. Only work that can wait, such as long-term history, should depend on a link.

## How Much Data?

Data volume decides whether a link is even practical, and it is easy to estimate. Here is FR-04, the semester trend, done two ways. The numbers are **example values**.

**Option A: Send the raw optical signal and let the server work out heart rate.**

**Assumption:** the sensor is read 100 times a second, and each reading takes 4 bytes.

```text
One 30 s reading:   100 samples/s × 4 bytes × 30 s  = 12,000 bytes
Per day (5 readings): 12,000 × 5                     = 60,000 bytes  (60 kB)
Per semester (120 days): 60,000 × 120               = 7,200,000 bytes (7.2 MB)
```

**Option B: Work out heart rate on the watch, and keep only the results.**

**Assumption:** each result is 1 byte of heart rate plus a 4-byte timestamp. Steps are saved once an hour as 2 bytes plus a 4-byte timestamp.

```text
Heart rate:  5 results × 5 bytes          =   25 bytes/day
Steps:      24 hours  × 6 bytes           =  144 bytes/day
Per day:                                    169 bytes
Per semester: 169 × 120                   = 20,280 bytes (about 20 kB)
```

**Check.** 7,200,000 ÷ 20,280 ≈ 355. Option A produces about 355 times more data for the same answer. More data means the radio stays on longer, and in A0 you saw how much battery life depends on what runs for long periods.

Now look back at the orphan. With Option B, a whole semester of history is about 20 kB. That changes the choice for FR-04: storing it on the watch itself (way out 2 in Part 2) becomes realistic, and a backend may not be needed at all for version 1. You will check the actual memory available when you choose parts.

## Which Connection?

Choose the product's route to the outside world, and write down a one-line reason. For a wearable the realistic choices are:

| Route | Suits | Watch out for |
|---|---|---|
| **No connection** | Everything needed is on the device | No history beyond what the watch stores |
| **Bluetooth Low Energy to a phone** | Frequent small updates; the phone relays to the internet | You must build, or depend on, a phone app |
| **WiFi direct to the internet** | Occasional larger transfers, with no phone | Higher power while connected; campus networks often need a browser login page that a watch cannot complete |

You will choose protocols and payloads properly in the firmware module. For now, one line is enough, such as: *"BLE to a phone, because history needs a big screen and the wearer always carries a phone."*

<!-- REFPRODUCT:START -->
esp_watch chose WiFi, used once at first boot, and then off. The reason is simple: it only needs the time and the weather, and a single short connection costs almost nothing in the battery budget. The trade-off is that it depends on a WiFi network the watch can join without a login page, and it cannot send anything later without turning WiFi back on. For the hostel problem statement, with its semester history, that choice would need revisiting.
<!-- REFPRODUCT:END -->

---

# Putting It All Together

## Applying What You Have Learned

**1. Draw your context diagram.** Use your A0 spec. One box for your product, every external actor, every arrow labelled with what flows. Save it as an image in your design pack.

**2. Break down your product.** List your subsystems using the seven as a starting point. For each, write one sentence describing its job. Mark any you merged or added, and say why.

**3. Allocate every requirement.** Build the table: ID, owner, supporting subsystems, and a short note on how it is met. Then:
- List every orphan and choose one of the three ways out for each.
- List every subsystem that owns or supports nothing, and say whether a requirement is missing or the subsystem is unnecessary.

**4. Make the three rough decisions.** For each main job, write where it runs and what the wearer sees when the link drops. Estimate your daily and total data volume, showing each step. Choose a connection route in one line.

**Deliverable:** save the context diagram, the subsystem list, the allocation table and your three rough decisions in your design pack as `A1-architecture.md`, with the diagram as an embedded image.

## Self-Check

Open `A1-architecture.md` and answer each item Y or N.

1. The context diagram has exactly one box for your product. — Y/N
2. Every arrow in the context diagram is labelled with what flows. — Y/N
3. Every actor mentioned in your A0 spec appears in the context diagram. — Y/N
4. Every subsystem has a one-sentence job description. — Y/N
5. Every requirement ID from A0 appears in the allocation table. — Y/N
6. Every requirement has exactly one owner, or is marked as an orphan. — Y/N
7. Every orphan has a chosen way out written next to it. — Y/N
8. Every subsystem appears in the allocation table at least once, or has a note explaining why not. — Y/N
9. Your data estimate shows bytes per day and total, with every step. — Y/N
10. Your connection route has a one-line reason. — Y/N

---

## Check Your Understanding

**1.** A student's watch must "show weekly step totals as a bar chart". Their context diagram has no phone and no server, and their watch display is 128 × 64 pixels. What is the most useful thing the allocation table will reveal?

- A. Nothing, because step counting is owned by sensing.
- B. Whether a small display can show the chart, and where a week of data is stored, which may reveal a missing owner.
- C. That the requirement belongs to connectivity.
- D. That the display must be replaced with a larger one.

<details>
<summary>Answer</summary>

**B.** Counting steps is only part of it. Storing a week of totals and drawing the chart are separate jobs that need owners, or they are orphans. **A** ignores the chart. **C** assumes a connection the diagram rules out. **D** fixes a problem not yet shown; a simple bar chart may fit.

</details>

**2.** A watch sends every heart-rate reading to a server, and the server works out the resting-heart-rate trend. The student loses WiFi for two days. With no buffering on the watch, what happens?

- A. Nothing, because the server will fill the gap.
- B. Two days of readings are lost from the trend, although the watch still shows live heart rate.
- C. The watch stops showing heart rate.
- D. The watch stores the readings automatically.

<details>
<summary>Answer</summary>

**B.** Live heart rate runs on the device and keeps working; history that depends on the link is lost without buffering. **A**: the server never received the data. **C** would need heart rate calculated on the server. **D**: nothing is stored automatically; buffering is a design decision someone must own.

</details>

**3.** Option A sends 60 kB a day of raw signal; Option B sends 169 bytes a day of results. Apart from storage, why does the difference matter for a battery-powered watch?

- A. It does not, because WiFi is fast.
- B. More data keeps the radio on for longer, and the radio is one of the most power-hungry parts.
- C. Servers charge per byte.
- D. The display cannot show 60 kB.

<details>
<summary>Answer</summary>

**B.** Radio-on time costs battery, so more bytes means a shorter battery life. **A** ignores energy; "fast" still has a cost for every second the radio is on. **C** may be true of some services, but it is not the main issue for the device. **D** confuses sending data with displaying it.

</details>

**4.** A team writes: *"NFR-07 Thickness ≤ 16 mm — Owner: Enclosure."* The circuit board with its modules is already 14.044 mm tall. What should the team conclude?

- A. The enclosure designer must make walls under 1 mm thick.
- B. Ownership is correct, but the requirement is really spent by the board stack, so sensing, processing, local UI and power must be listed as supporting and may need to change.
- C. Thickness should be owned by processing.
- D. The requirement is met, because 14.044 is less than 16.

<details>
<summary>Answer</summary>

**B.** Thickness is a budget requirement. The enclosure manages it, but the board stack spends most of it. Listing the supporting subsystems shows where the fix really lies. **A** puts an impossible load on one subsystem. **C** moves ownership without solving anything. **D** forgets that the case adds a lid, a base and a sensor window on top of the board.

</details>

**5.** Which is the best one-line reason for a connection choice?

- A. "WiFi, because the ESP32 has it."
- B. "Bluetooth, because it is modern."
- C. "BLE to a phone, because the wearer always carries one and history needs a large screen, while BLE keeps the watch's radio power low."
- D. "Both WiFi and Bluetooth, to be safe."

<details>
<summary>Answer</summary>

**C** ties the choice to the user, a requirement and a constraint. **A** confuses what is available with what is needed. **B** gives no engineering reason. **D** doubles the work and the power use without a requirement that needs both.

</details>

---

## What Comes Next

In [A2 — Operating Modes and Decisions](A2-operating-modes-and-decisions.md) you will decide how the whole system behaves over time: what it does while starting up, measuring, sleeping and failing, and how to record the big decisions you have just made so they survive.

---

## References

1. C4 model. *System context diagram* (a system shown as a box in the centre, surrounded by its users and the other systems it interacts with). https://c4model.com/diagrams/system-context
2. draw.io. *draw.io* (free, open-source diagramming application). https://www.drawio.com/

