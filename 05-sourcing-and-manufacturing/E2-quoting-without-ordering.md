# E2 — Quoting Without Ordering
## Real Checks, Real Quotes, and What One Unit Costs at 10, 100 and 1,000

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Sourcing and Manufacturing Handoff
**Time:** ~1 hour · **You will produce:** DFM report screenshots, a resolved-issues list and a three-tier cost model

---

### Stop One Click Before You Pay

You have a fabrication zip (E1), a costed BOM (E0) and a sliced enclosure (D5). The last step before a real build is to find out what a manufacturer thinks of your files, and what it would charge. Fab houses do this for free: upload a zip, and within minutes you get an automated design check and an instant price. You do not have to order.

This unit walks you through that process right up to checkout, and then uses the numbers to answer the question every funding panel will ask: **what does one unit cost?** The answer is different at 10, 100 and 1,000 units, sometimes surprisingly so, and a cost model shows why.

### What You Will Be Able to Do After This Reading

- **Upload** a fabrication zip to a fab house, and **read** its automated DFM report.
- **Resolve** DFM findings in KiCad, and record what you changed.
- **Obtain** a board quote and an enclosure quote, and **identify** every charge between the listed price and the landed cost.
- **Build** a unit-cost model at 10, 100 and 1,000 units, separating one-off costs from per-unit costs.
- **Find** the quantity at which a mould becomes cheaper than printing.

### What Part 1 Already Covered

Part 1 did not cover manufacturing costs. **Everything here is new.**

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## Uploading and Checking

Most board fabricators accept a Gerber zip on their website and show a quote straight away. For example, JLCPCB advertises prototype boards from $2 [1], and PCB Power, an Indian fabricator, offers an instant free quote and a free DFM check [2]. Try at least two, one international and one Indian, because delivery time, shipping and taxes often decide more than the board price does.

**DFM** (design for manufacturability) checks look at your files the way the fabricator's own engineers would: tracks and gaps too small for their process, holes too close to an edge, missing layers, a board outline that is not closed. Some are run automatically on upload, and JLCPCB also offers a free, web-based DFM tool, JLCDFM [3].

### Reading a DFM Report

A DFM report usually sorts findings by severity. Treat them like ERC and DRC results:

| Severity | What to do |
|---|---|
| **Error** | Fix it in KiCad, re-export, re-upload. Never order with an unresolved error. |
| **Warning** | Understand it. Fix it if it matters; if you accept it, write down why. |
| **Information** | Read it. Often explains how the fab will interpret something. |

Fix findings **in KiCad**, not by editing the Gerbers. The Gerbers are generated from the board; if you change the files by hand, the next export silently undoes your fix.

<!-- REFPRODUCT:START -->
esp_watch passed KiCad's DRC with zero errors, and its constraints were set tighter than the fab's published minimums (B5). Its JLCPCB order has been placed and is at fabrication; the DFM feedback from that order is not yet available, and screenshots of it will be added as course assets when it completes.
<!-- REFPRODUCT:END -->

<!-- ASSET:PLACEHOLDER reference-files/images/jlcpcb-dfm.png -->

<!-- MEDIA
type: screenshot
id: E2-01
caption: A fab house's automated DFM report for a small two-layer board
brief: Browser screenshot of a DFM result page (JLCDFM or a fab's upload checker) for a
  small two-layer board. A list of findings on the left grouped by severity (e.g. one
  warning "silkscreen overlaps pad", one information item "board outline detected"), and
  a board render on the right with the warning location highlighted. Crop to the report
  and render; no account details.
-->

### The Resolved-Issues List

Record every finding and what you did about it:

| # | Finding | Severity | Cause | Action | Re-checked |
|---|---|---|---|---|---|
| 1 | *e.g.* Silkscreen text overlaps a pad | Warning | Reference label placed on the pad | Moved the label in KiCad | Yes, gone |
| 2 | *e.g.* Annular ring below minimum on one via | Error | Via size smaller than the default rule | Changed via to the default class | Yes, gone |

## Reading the Quote

A quote has a headline price and a list of options: quantity, board thickness, finish, colour, copper weight, delivery speed. Change one at a time and watch the price. You will usually find that a few options, such as an unusual colour or a faster build, change the price a lot, and the rest barely matter.

Then follow the money to your door. The headline price is not what you pay. E0 showed how shipping, customs duty and GST are added to imported goods. For a board order, list every charge:

```text
Board price (quoted)
+ Shipping (chosen method)
+ Customs duty (on value + shipping)
+ GST (on value + shipping + duty)
+ Any handling or clearance fee
= Landed cost
```

<!-- REFPRODUCT:START -->
esp_watch's real order will give the course a true comparison: what was quoted, what it cost once shipping, customs and GST were added, and how long delivery actually took against the estimate. Until the order completes, those figures are a **placeholder**.
<!-- REFPRODUCT:END -->

<!-- FACT:VERIFY esp_watch — JLCPCB order quantity, options, quoted and landed cost, and quoted versus actual lead time are placeholders until the order completes (REFERENCE-PRODUCT.md §6) -->

<!-- ASSET:PLACEHOLDER reference-files/images/jlcpcb-order.png -->

## Quoting the Enclosure

Do the same for the case. Upload the lid and base (STL or 3MF) to an online 3D printing service, choose a material close to your D3 decision, and record the price, material, lead time and delivery. Compare it with your D5 estimate: the service's price includes machine time, labour and profit, not just the few rupees of filament.

> **Try it: Find the expensive option.** On one fab house's quote page, with your own zip uploaded:
> 1. **Predict.** Which option will change the price the most: quantity 5 to 10, board colour, surface finish, or delivery speed?
> 2. **Do.** Change each one alone, note the price, and change it back.
> 3. **Explain.** Which mattered most? Which option would you choose for a first prototype, and why?

---

## The Unit-Cost Model

### One-Off Costs and Per-Unit Costs

Every product cost splits into two kinds:

- **One-off costs**, also called **NRE** (non-recurring engineering) and **tooling**: paid once, whatever the quantity. A mould, a solder-paste stencil, a test fixture, certification.
- **Per-unit costs**: paid again for every unit. Parts, the board, the case, assembly time, test time.

The cost of one unit at quantity *N* is:

```text
unit cost = (one-off costs ÷ N) + per-unit costs at quantity N
```

Two things change with quantity. The one-off costs are shared across more units, and the per-unit costs themselves usually fall, through price breaks and cheaper processes.

### Worked Example: esp_watch at 10, 100 and 1,000

**All figures are example values**, chosen to show the structure. The modules are B2's Robu prices; everything else, including the discounts, is illustrative. Replace every number with your own quotes.

**Step 1: List the per-unit costs at each quantity.**

| Per unit (₹) | 10 | 100 | 1,000 |
|---|---|---|---|
| Modules (B2: ₹1,416 at 1; assume 10% off at 100, 20% at 1,000) | 1,416 | 1,274 | 1,133 |
| Small parts: buttons, switch, resistors, headers | 120 | 100 | 80 |
| Battery (placeholder cell) | 350 | 300 | 250 |
| Circuit board | 150 | 60 | 25 |
| Enclosure, printed by a service | 250 | 200 | 200 |
| Hand assembly: 30 min at ₹200/h | 100 | 100 | 100 |
| Test and programming: 10 min at ₹200/h | 33 | 33 | 33 |
| **Per-unit total** | **2,419** | **2,067** | **1,821** |

**Step 2: List the one-off costs.** A simple programming and test fixture: ₹5,000.

**Step 3: Unit cost with a printed case.**

```text
10 units:    5,000 ÷ 10    + 2,419 = 500 + 2,419 = ₹2,919
100 units:   5,000 ÷ 100   + 2,067 =  50 + 2,067 = ₹2,117
1,000 units: 5,000 ÷ 1,000 + 1,821 =   5 + 1,821 = ₹1,826
```

**Step 4: What if the case were moulded at 1,000?** Assume a mould costing ₹3,00,000, and a moulded case at ₹30 each.

```text
Per-unit total: 1,821 − 200 (printed) + 30 (moulded) = ₹1,651
Unit cost: (5,000 + 3,00,000) ÷ 1,000 + 1,651 = 305 + 1,651 = ₹1,956
```

At 1,000 units, the moulded case is **more** expensive per unit than the printed one: ₹1,956 against ₹1,826.

**Step 5: Where does moulding break even?** The mould pays for itself when the saving per case, ₹200 − ₹30 = ₹170, has covered its cost:

```text
3,00,000 ÷ 170 ≈ 1,765 units
```

**Check.** Below about 1,800 units, printing wins on cost in this model; above it, moulding does. But cost is not the only limit. Printing 1,000 cases at D5's 1 h 45 min each is 1,750 hours of printer time, and hand assembly at 30 minutes each is 500 hours of someone's work. At volume, **time and capacity** become as important as rupees, and that, together with the surface finish and accuracy of moulded parts (D3), is why commercial watch cases are moulded long before the pure cost crossover.

<!-- MEDIA
type: diagram
id: E2-02
caption: Unit cost against quantity: printed case versus moulded case
brief: A simple line chart, quantity on a logarithmic x axis from 10 to 10,000, unit cost
  in rupees on the y axis. Two lines from the worked example's model: "printed case" and
  "moulded case (₹3,00,000 mould)". The moulded line starts very high and falls steeply;
  the printed line falls gently and flattens. Mark the crossover at about 1,765 units with
  a dotted vertical line labelled "break-even". Label both axes; note "example values".
-->

> **Try it: Move the break-even.** Using the worked example's model:
> 1. **Predict.** If a cheaper aluminium mould cost ₹1,50,000 instead of ₹3,00,000, where would the break-even move?
> 2. **Do.** Recalculate it.
> 3. **Explain.** What other cost in the model would you most want a real quote for before deciding, and why?

---

# Putting It All Together

## Applying What You Have Learned

**1. Upload and check.** Upload your E1 zip to at least one fab house, and run a DFM check. Screenshot the report.

**2. Resolve the findings** in KiCad, re-export, re-check, and complete the resolved-issues list.

**3. Get the quotes.** A board quote at your prototype quantity from two suppliers, and an enclosure quote from a printing service. Record every charge to the landed cost. Stop at checkout.

**4. Build the cost model.** One-off and per-unit costs, at 10, 100 and 1,000 units, with the source of every number: a quote, a listing with its date, or a labelled assumption.

**5. Decide the case process** for each quantity, with the break-even calculation.

**Deliverable:** DFM report screenshots, the resolved-issues list, the quotes with landed costs, and the three-tier cost model (spreadsheet), saved in your design pack.

## Self-Check

1. At least one DFM report is saved as a screenshot. — Y/N
2. Every DFM error was fixed in KiCad and re-checked. — Y/N
3. Every accepted DFM warning has a written reason. — Y/N
4. There are board quotes from at least two suppliers. — Y/N
5. Every quote is followed through to a landed cost. — Y/N
6. The cost model separates one-off and per-unit costs. — Y/N
7. Unit cost is calculated at 10, 100 and 1,000. — Y/N
8. Every number in the model has a source or is labelled as an assumption. — Y/N
9. The case process decision includes a break-even calculation. — Y/N

---

## Check Your Understanding

**1.** A DFM report flags an annular ring below the fab's minimum. What is the right fix?

- A. Edit the drill file by hand to make the hole smaller.
- B. Change the via or pad size in KiCad, re-run DRC, re-export and re-upload.
- C. Ignore it; the fab will adjust it.
- D. Choose a different fab without checking.

<details>
<summary>Answer</summary>

**B.** Fix the design, then regenerate the files, so the fix survives the next export. **A** is undone at the next export and bypasses your own checks. **C** hands a decision to someone who does not know your intent. **D** may move the problem without solving it.

</details>

**2.** One-off costs are ₹50,000 and per-unit costs ₹1,000. What is the unit cost at 100 units?

- A. ₹1,000
- B. ₹1,500
- C. ₹5,000
- D. ₹51,000

<details>
<summary>Answer</summary>

**B.** 50,000 ÷ 100 + 1,000 = ₹1,500. **A** ignores the one-off costs. **C** is the one-off cost spread over only 10 units, plus nothing. **D** puts the whole one-off cost on a single unit.

</details>

**3.** A mould costs ₹3,00,000 and saves ₹170 per case compared with printing. Roughly how many cases must be made before the mould pays for itself?

- A. About 170
- B. About 1,765
- C. About 3,000
- D. About 17,650

<details>
<summary>Answer</summary>

**B.** 3,00,000 ÷ 170 ≈ 1,765. **A** confuses the saving with the quantity. **C** divides by 100. **D** is ten times too many.

</details>

**4.** A board quote shows $2 for 5 boards. Why is that not the cost of the boards?

- A. The quote is in dollars.
- B. Shipping, customs duty, GST and any clearance fees are added between the quote and your door.
- C. The fab will change the price later.
- D. Boards are sold in tens.

<details>
<summary>Answer</summary>

**B.** The landed cost includes everything to your door, as E0 showed, and on a small order these extra charges can be several times the board price. **A** is a conversion, not the missing cost. **C** and **D** are not the reason.

</details>

**5.** At 1,000 units, the cost model shows printing slightly cheaper than moulding per unit. Why might a company choose moulding anyway?

- A. Moulding is always cheaper.
- B. Printing 1,000 cases takes well over a thousand printer-hours, and moulded parts are more accurate and better finished; capacity and quality matter as well as cost.
- C. Printed cases cannot hold electronics.
- D. The model must be wrong.

<details>
<summary>Answer</summary>

**B.** Cost is only one input. Time, capacity, consistency and finish all favour moulding as volume grows. **A** contradicts the model. **C** is false. **D** assumes the model is wrong rather than incomplete.

</details>

---

## What You Can Now Do, and What Comes Next

- Use a fab house's free checks and quotes without ordering.
- Resolve DFM findings at the source, and record them.
- Follow a quote to its landed cost.
- Build a cost model that shows how the unit cost changes with quantity, and where a process changes.

The idea to carry forward: **unit cost is a function of quantity.** Always say *at what quantity* when you quote a cost.

In [F — Capstone](../06-capstone/F-capstone-design-pack.md) you will assemble everything you have produced into a single Design Pack, review it against a rubric, and compare it, honestly, with the reference watch.

---

## References

1. JLCPCB. *PCB Prototype and PCB Fabrication Manufacturer* ("Instant online PCB quote, get PCBs for only $2"; online Gerber viewer). https://jlcpcb.com/
2. PCB Power. *PCB Manufacturer in India* (instant free quote; free DFM check). https://www.pcbpower.com/
3. JLCDFM. *Free Online PCB DFM Tool* (web-based DFM analysis). https://jlcdfm.com/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
