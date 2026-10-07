# F2 — Quoting Without Ordering
## Real Checks, Real Quotes, and What One Unit Costs

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 6 — Sourcing and Manufacturing Handoff
**Time:** ~1 hour · **You will produce:** DFM report screenshots, a resolved-issues list and a cost model at 1 and 10 units

---

### Stop One Click Before You Pay

You have a fabrication zip (F1), a costed BOM (F0) and a sliced enclosure (E5). The last step before a real build is to find out what a manufacturer thinks of your files, and what it would charge. Fab houses do this for free: upload a zip, and within minutes you get an automated design check and an instant price. You do not have to order.

This unit walks you through that process right up to checkout, and then uses the numbers to answer the question every funding panel will ask: **what does one unit cost?** The answer depends on how many you make, and a simple cost model shows why.

### What You Will Be Able to Do After This Reading

- **Upload** a fabrication zip to a fab house, and **read** its automated DFM report.
- **Resolve** DFM findings in KiCad, and record what you changed.
- **Obtain** a board quote and an enclosure quote, and **identify** every charge between the listed price and the landed cost.
- **Build** a unit-cost model at 1 and 10 units, separating one-off costs from per-unit costs.

### What Part 1 Already Covered

Part 1 did not cover manufacturing costs. **Everything here is new.**

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
esp_watch passed KiCad's DRC with zero errors, with its constraints set to JLCPCB's two-layer minimums (C3). Its JLCPCB order went through and the boards were delivered; its DFM report is shown below.
<!-- REFPRODUCT:END -->

![JLCDFM report for esp_watch's board: findings grouped by layer on the left, the board on the right](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/DFM_check.png)

### The Resolved-Issues List

Record every finding and what you did about it:

| # | Finding | Severity | Cause | Action | Re-checked |
|---|---|---|---|---|---|
| 1 | *e.g.* Silkscreen text overlaps a pad | Warning | Reference label placed on the pad | Moved the label in KiCad | Yes, gone |
| 2 | *e.g.* Annular ring below minimum on one via | Error | Via size smaller than the default rule | Changed via to the default class | Yes, gone |

## Reading the Quote

A quote has a headline price and a list of options: quantity, board thickness, finish, colour, copper weight, delivery speed. Change one at a time and watch the price. You will usually find that a few options, such as an unusual colour or a faster build, change the price a lot, and the rest barely matter.

Then follow the money to your door. The headline price is not what you pay. F0 showed how shipping, customs duty and GST are added to imported goods. For a board order, list every charge:

```text
Board price (quoted)
+ Shipping (chosen method)
+ Customs duty (on value + shipping)
+ GST (on value + shipping + duty)
+ Any handling or clearance fee
= Landed cost
```

<!-- REFPRODUCT:START -->
esp_watch's real order, 5 boards from JLCPCB:

| Line | Cost |
|---|---|
| Board fabrication (5 boards) | $4.00 |
| Shipping (DHL Express) | $24.68 |
| **Quoted total** | **$28.68** |
| Discount | −$10.00 |
| **Paid** | **$18.68** |

Shipping cost six times as much as the boards themselves: the headline board price was the smallest line on the bill. The quote promised a 2-day build and 2–5 business days of shipping. (Customs duty and GST were not recorded.)
<!-- REFPRODUCT:END -->

![JLCPCB's online quote for esp_watch's board: 5 two-layer boards at $4.00, with a shipping estimate](https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/JLCPCB_quote.png)

## Quoting the Enclosure

Do the same for the case. Upload the lid and base (STL or 3MF) to an online 3D printing service, choose a material close to your E1 decision, and record the price, material, lead time and delivery. Compare it with your E5 estimate: the service's price includes machine time, labour and profit, not just the few rupees of filament.

---

## The Unit-Cost Model

### One-Off Costs and Per-Unit Costs

Every product cost splits into two kinds:

- **One-off costs**, also called **NRE** (non-recurring engineering) and **tooling**: paid once, whatever the quantity. A test fixture, a solder-paste stencil, or (at volume) a mould.
- **Per-unit costs**: paid again for every unit. Parts, the board, the case, assembly time, test time.

The cost of one unit at quantity *N* is:

```text
unit cost = (one-off costs ÷ N) + per-unit costs at quantity N
```

Two things change with quantity. The one-off costs are shared across more units, and the per-unit costs themselves usually fall, through price breaks and cheaper processes.

### Worked Example: esp_watch at 1 and 10

**All figures are example values**, chosen to show the structure. The modules are B4's Robu prices; everything else is illustrative. Replace every number with your own quotes.

**Step 1: List the per-unit costs.**

| Per unit (₹) | 1 | 10 |
|---|---|---|
| Modules (B4: ₹1,416 at 1) | 1,416 | 1,416 |
| Small parts: buttons, switch, resistors, headers | 150 | 120 |
| Battery (300 mAh protected cell) | 350 | 350 |
| Circuit board (at 1 unit, the whole 5-board minimum order lands on one watch) | 750 | 150 |
| Enclosure, printed by a service | 300 | 250 |
| Hand assembly: 30 min at ₹200/h | 100 | 100 |
| **Per-unit total** | **3,066** | **2,386** |

**Step 2: List the one-off costs.** A simple programming and test fixture: ₹5,000. For a single prototype you might skip it (₹0).

**Step 3: Unit cost.**

```text
1 unit, no fixture:   0 ÷ 1      + 3,066 = ₹3,066
10 units, fixture:    5,000 ÷ 10 + 2,386 = 500 + 2,386 = ₹2,886
```

**Check.** At 10 units the fixture adds ₹500 to each unit, but the unit cost still falls, because the minimum board order no longer lands on one watch. One-off costs, and minimum orders that behave like them, dominate at small quantities. At hundreds of units they shrink to almost nothing per unit.

---

# Putting It All Together

## Applying What You Have Learned

**1. Upload and check.** Upload your F1 zip to at least one fab house, and run a DFM check. Screenshot the report.

**2. Resolve the findings** in KiCad, re-export, re-check, and complete the resolved-issues list.

**3. Get the quotes.** A board quote at your prototype quantity from two suppliers, and an enclosure quote from a printing service. Record every charge to the landed cost. Stop at checkout.

**4. Build the cost model.** One-off and per-unit costs, at 1 and 10 units, with the source of every number: a quote, a listing with its date, or a labelled assumption.

**Deliverable:** DFM report screenshots, the resolved-issues list, the quotes with landed costs, and the cost model at 1 and 10 units (spreadsheet), saved in your design pack.

## Self-Check

1. At least one DFM report is saved as a screenshot. — Y/N
2. Every DFM error was fixed in KiCad and re-checked. — Y/N
3. Every accepted DFM warning has a written reason. — Y/N
4. There are board quotes from at least two suppliers. — Y/N
5. Every quote is followed through to a landed cost. — Y/N
6. The cost model separates one-off and per-unit costs. — Y/N
7. Unit cost is calculated at 1 and 10. — Y/N
8. Every number in the model has a source or is labelled as an assumption. — Y/N

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

**3.** A student's cost model shows ₹3,200 for one unit and ₹3,450 each for ten, even though parts are slightly cheaper at ten. What most likely explains the higher unit cost at ten?

- A. Parts cost more in bulk.
- B. A one-off cost, such as a test fixture, is shared across only ten units and adds more per unit than the price breaks save.
- C. The model is wrong; unit cost always falls with quantity.
- D. Shipping is only charged on larger orders.

<details>
<summary>Answer</summary>

**B.** One-off costs divided over a small quantity can outweigh small price breaks. **A** is backwards. **C** ignores one-off costs. **D** is false: shipping applies to every order.

</details>

**4.** A board quote shows $2 for 5 boards. Why is that not the cost of the boards?

- A. The quote is in dollars.
- B. Shipping, customs duty, GST and any clearance fees are added between the quote and your door.
- C. The fab will change the price later.
- D. Boards are sold in tens.

<details>
<summary>Answer</summary>

**B.** The landed cost includes everything to your door, as F0 showed, and on a small order these extra charges can be several times the board price. **A** is a conversion, not the missing cost. **C** and **D** are not the reason.

</details>

**5.** You need 2 boards. The fab's minimum order is 5, with a landed cost of ₹750. What board cost goes in your cost model?

- A. ₹150 per board, because 750 ÷ 5 = 150
- B. ₹375 per board: the whole ₹750 spread over the 2 boards you use, with the quote's source and date noted
- C. Zero, because boards are cheap
- D. The per-board price at 1,000 units

<details>
<summary>Answer</summary>

**B.** You pay for the whole minimum order, so its landed cost falls on the boards you use. **A** spreads the cost over three boards you will not use. **C** ignores a real cost. **D** is a quantity you will not buy.

</details>

---

## What Comes Next

The idea to carry forward: **unit cost is a function of quantity.** Always say *at what quantity* when you quote a cost.

In [G — Capstone](../07-capstone/G-capstone-design-pack.md) you will assemble everything you have produced into a single Design Pack, review it against a rubric, and compare it, honestly, with the reference watch.

---

## References

1. JLCPCB. *PCB Prototype and PCB Fabrication Manufacturer* ("Instant online PCB quote, get PCBs for only $2"; online Gerber viewer). https://jlcpcb.com/
2. PCB Power. *PCB Manufacturer in India* (instant free quote; free DFM check). https://www.pcbpower.com/
3. JLCDFM. *Free Online PCB DFM Tool* (web-based DFM analysis). https://jlcdfm.com/

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
