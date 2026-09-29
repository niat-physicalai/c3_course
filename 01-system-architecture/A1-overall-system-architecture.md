# A1 — Overall System Architecture
## Drawing the Whole System on One Page, and Giving Every Requirement an Owner

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 1 — System Architecture
**Time:** ~1 hour · **You will produce:** a context diagram, a subsystem breakdown and a requirement allocation table

---

### A List of Requirements Is Not Yet a Design

You now have a specification: numbered requirements, each with a number and a check method. It tells you *what* the product must achieve. It does not tell you what the product is *made of*, what it talks to, or which part is responsible for which requirement.

Suppose your spec says the wearer must see how their resting heart rate changes across a semester. Where does a semester of readings live? On the watch? On a phone? On a server? Each answer produces a different product. Storing it on the watch needs memory and a way to show a graph on a tiny screen. A phone needs an app. A server needs an internet connection and somewhere to run. If nobody asks the question, the requirement simply falls through the gap. Nobody builds it, and nobody notices until the end.

This unit gives you one page that shows the whole system, and a table that makes such gaps impossible to miss.

### What You Will Be Able to Do After This Reading

- **Draw** a context diagram showing your product, everything outside it that it interacts with, and what flows between them.
- **Break down** your product into standard subsystems.
- **Allocate** every requirement from your specification to one owning subsystem, and find any requirement with no owner.
- **Decide** roughly where each piece of work happens (device, phone or server), and **predict** what the user sees when the link between them drops.
- **Estimate** how much data your product produces, and use the estimate to decide what to process on the device.

### What Part 1 Already Covered

Part 1 drew systems as a chain, for example *sensors → ESP32 → WiFi → MQTT broker → cloud → dashboard*, and asked you to keep each part testable on its own. **What is new here** is drawing an explicit boundary around *your* product, naming everything outside it, and checking in a table that every requirement belongs to a specific part of the system.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

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
     button presses, shake   │          │  time, weather, steps,
     to wake                 ▼          │  heart rate on screen
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

<!-- FACT:VERIFY esp_watch — the specific time and weather services used by watch_ui_test.ino are not recorded in REFERENCE-PRODUCT.md -->

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

> **Try it: Find the actors.** Take your A0 specification.
> 1. **Predict.** How many external actors will your context diagram have? Write down the number before you start.
> 2. **Do.** Go through the spec line by line. For each requirement, ask what outside the product is involved. Add each new actor to a list, then draw the diagram.
> 3. **Explain.** Did you find more actors than you predicted? Which requirement revealed an actor you had not thought of?
>
> **Extra challenge:** Find one arrow where you are not sure which way things flow. What question would you need to answer in your spec to settle it?

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
│  (on the XIAO), battery sense │                 antenna             │
│                                                                     │
│  ENCLOSURE: 3D-printed case, lid with 4 openings, sensor underneath │
└─────────────────────────────────────────────────────────────────────┘
   BACKEND: none of its own. Uses public time and weather services.
```
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/render-top.png -->
![esp_watch circuit board, top view: the display, motion sensor, ESP32-C3 board, buttons and power switch](../reference-files/images/render-top.png)

Look at the render and try to point at each subsystem. Sensing, processing, local UI and power are all visible. Connectivity is mostly inside the ESP32-C3 board, with the antenna on a cable. The enclosure is not on the board at all. The backend does not exist. A block diagram and a photo of a board show very different things, which is why you need the diagram.

## Allocating Every Requirement

A **requirement allocation table** lists every requirement in your spec and names the subsystem that **owns** it: the one responsible if the requirement is not met. Other subsystems may **support** it, but only one owns it.

Why only one owner? When two subsystems share a requirement equally, each assumes the other is handling it. One named owner removes that doubt.

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
| FR-04 | Wake the screen when the wrist is shaken |
| FR-05 | Show how resting heart rate has changed over the semester |
| NFR-01 | Heart rate within ±5 bpm, wearer sitting still |
| NFR-03 | ≥ 2 days between charges with usage pattern UP-1 |
| NFR-05 | Charge from a USB-C phone charger |
| NFR-07 | Total thickness ≤ 16 mm including the case |

**Step 2: Give each requirement an owner, and list its supporters.**

<!-- REFPRODUCT:START -->
| ID | Owner | Supporting | How esp_watch meets it |
|---|---|---|---|
| FR-01 | Processing | Connectivity, Local UI | Firmware keeps time; WiFi sets it once at first boot |
| FR-02 | Sensing | Processing, Local UI, Enclosure | MAX30102 on the underside; firmware calculates bpm |
| FR-03 | Sensing | Processing | MPU-6050 motion sensor; firmware counts steps |
| FR-04 | Sensing | Power, Processing | MPU-6050 stays on during sleep to detect a shake |
| FR-05 | **none** | — | **Orphan.** Nothing stores readings across a semester |
| NFR-01 | Sensing | Enclosure | Needs firm skin contact and blocked outside light |
| NFR-03 | Power | every subsystem | Sleep current dominates (see A0) |
| NFR-05 | Power | Enclosure | USB-C on the XIAO, reached from the left side of the case |
| NFR-07 | Enclosure | Sensing, Processing, Local UI, Power | Board alone is 14.044 mm high, leaving ~2 mm for the case |
<!-- REFPRODUCT:END -->

**Step 3: Look for orphans.** FR-05 has no owner. To show a semester's trend, readings must be stored for months and then displayed as a trend. esp_watch has no storage subsystem for history and no backend. The requirement is the heart of the problem statement, and nothing in the design delivers it.

There are three honest ways out:

1. **Add a backend**, such as a phone app or a server that the watch uploads to.
2. **Make processing own it**: store a few bytes per day in the watch's own memory and draw a simple trend on the display.
3. **Move it out of version 1**, and say so in the spec, accepting that version 1 only partly solves the problem.

Which is best? That depends on how much data is involved, which is the subject of Part 3.

**Step 4: Look for unused subsystems.** Connectivity supports only FR-01, setting the clock. esp_watch also fetches the weather, but no requirement in this spec asks for weather. So either a requirement is missing, or part of the connectivity work serves nothing in this problem statement.

**Check.** Count the rows: 9 requirements, 8 with owners, 1 orphan. Every subsystem except the backend appears at least once, and the backend does not exist. The table has done its job: it found one gap and one extra feature in a few minutes, before any circuit was drawn.

Look again at NFR-07. The board alone is 14.044 mm, leaving roughly 2 mm for the whole case: a lid, a base and the sensor window. That is almost certainly not enough, and the allocation table exposed it by making the enclosure the owner of a number it cannot meet. The fix belongs to sensing, processing and local UI (stack the modules differently), not to the enclosure.

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

A common belief is that sending everything to the cloud makes a product "smarter". In practice it makes the product only as reliable as its weakest link, and a hostel WiFi network is rarely the strongest link in anything.

## How Much Data?

Data volume decides whether a link is even practical, and it is easy to estimate. Here is FR-05, the semester trend, done two ways. The numbers are **example values**.

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

Now look back at the orphan. With Option B, a whole semester of history is about 20 kB. That changes the choice for FR-05: storing it on the watch itself (way out 2 in Part 2) becomes realistic, and a backend may not be needed at all for version 1. You will check the actual memory available when you choose parts.

> **Try it: Change the numbers.** Keep Option B, but the wearer now wants heart rate saved every 10 minutes, all day, instead of 5 times a day.
> 1. **Predict.** Will a semester of data still fit comfortably in about 100 kB?
> 2. **Do.** Recalculate bytes per day and per semester.
> 3. **Explain.** Was your prediction right? What does saving heart rate every 10 minutes do to battery life, going back to A0's worked example?
>
> **Extra challenge:** What if you stored only one value per day, the lowest heart rate? How many bytes is a semester now, and what information have you given up?

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

**5. Diagnose.** A classmate's allocation table has these rows. What is wrong with each?

```text
NFR-03  Battery ≥ 2 days       Owner: Power, Processing, Sensing
FR-06   Send daily summary     Owner: Connectivity   Supporting: Backend
         (no backend appears anywhere in their subsystem list)
NFR-08  Cost ≤ ₹2,500          Owner: —
```

<details>
<summary>Answer</summary>

**NFR-03** has three owners. Pick one (power, which manages the budget) and list the others as supporting. **FR-06** relies on a backend that does not exist in the design. Either add the backend as a subsystem or change where the summary goes. **NFR-08** is left unowned. Cost is a budget requirement that no single subsystem manages, so make "System" the owner and list every subsystem that spends from it as supporting.

</details>

**Deliverable:** save the context diagram, the subsystem list and the allocation table in your design pack as `A1-architecture.md`, with the diagram as an embedded image.

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

**B.** Counting steps (sensing) is only part of the requirement. Storing a week of totals and drawing a chart are separate jobs, and the table forces you to name who owns them. If nothing does, it is an orphan. **A** confuses the step count with the weekly chart. **C** assumes a connection that the context diagram says does not exist. **D** jumps to a design fix before the table has shown whether there is a problem; a simple bar chart may fit.

</details>

**2.** Which of these belongs inside the system boundary of a wrist-worn tracker?

- A. The hostel WiFi router
- B. The phone charger
- C. The firmware running on the watch
- D. A public weather service

<details>
<summary>Answer</summary>

**C.** You design and change the firmware, so it is inside. **A**, **B** and **D** exist whether or not your product does, and you cannot change them by editing your design files. They are external actors, and your design must cope with them as they are.

</details>

**3.** A watch sends every heart-rate reading to a server, and the server works out the resting-heart-rate trend. The student loses WiFi for two days. With no buffering on the watch, what happens?

- A. Nothing, because the server will fill the gap.
- B. Two days of readings are lost from the trend, although the watch still shows live heart rate.
- C. The watch stops showing heart rate.
- D. The watch stores the readings automatically.

<details>
<summary>Answer</summary>

**B.** Live heart rate runs on the device, so it keeps working, but anything that depended on the link, here the stored history, is lost unless the device buffers it. **A** is wrong because the server never received the data and cannot invent it. **C** would only happen if heart rate were calculated on the server. **D** is wrong: nothing happens automatically; storing readings is a design decision that someone must own.

</details>

**4.** Option A sends 60 kB a day of raw signal; Option B sends 169 bytes a day of results. Apart from storage, why does the difference matter for a battery-powered watch?

- A. It does not, because WiFi is fast.
- B. More data keeps the radio on for longer, and the radio is one of the most power-hungry parts.
- C. Servers charge per byte.
- D. The display cannot show 60 kB.

<details>
<summary>Answer</summary>

**B.** Radio-on time costs battery, so more bytes means a shorter battery life. **A** ignores energy; "fast" still has a cost for every second the radio is on. **C** may be true of some services, but it is not the main issue for the device. **D** confuses sending data with displaying it.

</details>

**5.** A team writes: *"NFR-07 Thickness ≤ 16 mm — Owner: Enclosure."* The circuit board with its modules is already 14.044 mm tall. What should the team conclude?

- A. The enclosure designer must make walls under 1 mm thick.
- B. Ownership is correct, but the requirement is really spent by the board stack, so sensing, processing, local UI and power must be listed as supporting and may need to change.
- C. Thickness should be owned by processing.
- D. The requirement is met, because 14.044 is less than 16.

<details>
<summary>Answer</summary>

**B.** Thickness is a budget requirement. The enclosure manages it, but the board stack spends most of it. Listing the supporting subsystems shows where the fix really lies. **A** puts an impossible load on one subsystem. **C** moves ownership without solving anything. **D** forgets that the case adds a lid, a base and a sensor window on top of the board.

</details>

**6.** Which is the best one-line reason for a connection choice?

- A. "WiFi, because the ESP32 has it."
- B. "Bluetooth, because it is modern."
- C. "BLE to a phone, because the wearer always carries one and history needs a large screen, while BLE keeps the watch's radio power low."
- D. "Both WiFi and Bluetooth, to be safe."

<details>
<summary>Answer</summary>

**C** ties the choice to the user, a requirement and a constraint. **A** confuses what is available with what is needed. **B** gives no engineering reason. **D** doubles the work and the power use without a requirement that needs both.

</details>

---

## What You Can Now Do, and What Comes Next

- Draw a context diagram that makes your product's boundary and outside world clear.
- Break a product into subsystems, each with a clear job.
- Give every requirement a single owner, and spot orphans and unused subsystems.
- Decide roughly where work happens, how much data flows, and which connection to use.

The idea to carry forward: **every requirement needs one owner, and every part of the design needs a reason to exist.** The allocation table checks both at once.

In [A2 — Operating Modes and Decisions](A2-operating-modes-and-decisions.md) you will decide how the whole system behaves over time: what it does while starting up, measuring, sleeping and failing, and how to record the big decisions you have just made so they survive.

---

## References

1. D2 model. *System context diagram* (a system shown as a box in the centre, surrounded by its users and the other systems it interacts with). https://c4model.com/diagrams/system-context
2. draw.io. *draw.io* (free, open-source diagramming application). https://www.drawio.com/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
