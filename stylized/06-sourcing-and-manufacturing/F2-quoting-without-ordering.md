<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">F2 — Quoting Without Ordering</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Real Checks, Real Quotes, and What One Unit Costs</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 6 — Sourcing and Manufacturing Handoff <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> DFM report screenshots, a resolved-issues list and a cost model at 1 and 10 units</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Stop One Click Before You Pay</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">You have a fabrication zip (F1), a costed BOM (F0) and a sliced enclosure (E5). The last step before a real build is to find out what a manufacturer thinks of your files, and what it would charge. Fab houses do this for free: upload a zip, and within minutes you get an automated design check and an instant price. You do not have to order.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit walks you through that process right up to checkout, and then uses the numbers to answer the question every funding panel will ask: <strong>what does one unit cost?</strong> The answer depends on how many you make, and a simple cost model shows why.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Upload</strong> a fabrication zip to a fab house, and <strong>read</strong> its automated DFM report.</li><li style="margin:6px 0;">​<strong>Resolve</strong> DFM findings in KiCad, and record what you changed.</li><li style="margin:6px 0;">​<strong>Obtain</strong> a board quote and an enclosure quote, and <strong>identify</strong> every charge between the listed price and the landed cost.</li><li style="margin:6px 0;">​<strong>Build</strong> a unit-cost model at 1 and 10 units, separating one-off costs from per-unit costs.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 did not cover manufacturing costs. <strong>Everything here is new.</strong></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Uploading and Checking</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Most board fabricators accept a Gerber zip on their website and show a quote straight away. For example, JLCPCB advertises prototype boards from $2 [1], and PCB Power, an Indian fabricator, offers an instant free quote and a free DFM check [2]. Try at least two, one international and one Indian, because delivery time, shipping and taxes often decide more than the board price does.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>DFM</strong> (design for manufacturability) checks look at your files the way the fabricator's own engineers would: tracks and gaps too small for their process, holes too close to an edge, missing layers, a board outline that is not closed. Some are run automatically on upload, and JLCPCB also offers a free, web-based DFM tool, JLCDFM [3].</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Reading a DFM Report</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A DFM report usually sorts findings by severity. Treat them like ERC and DRC results:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Severity</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What to do</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Error</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fix it in KiCad, re-export, re-upload. Never order with an unresolved error.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Warning</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Understand it. Fix it if it matters; if you accept it, write down why.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Information</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Read it. Often explains how the fab will interpret something.</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Fix findings <strong>in KiCad</strong>, not by editing the Gerbers. The Gerbers are generated from the board; if you change the files by hand, the next export silently undoes your fix.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch passed KiCad's DRC with zero errors, with its constraints set to JLCPCB's two-layer minimums (C3). Its JLCPCB order went through and the boards were delivered; its DFM report is shown below.</div>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/DFM_check.png" alt="JLCDFM report for esp_watch&#x27;s board: findings grouped by layer on the left, the board on the right" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">JLCDFM report for esp\_watch's board: findings grouped by layer on the left, the board on the right</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Resolved-Issues List</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Record every finding and what you did about it:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">#</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Finding</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Severity</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Cause</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Action</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Re-checked</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">e.g. Silkscreen text overlaps a pad</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Warning</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reference label placed on the pad</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Moved the label in KiCad</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes, gone</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">e.g. Annular ring below minimum on one via</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Error</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Via size smaller than the default rule</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Changed via to the default class</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes, gone</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Reading the Quote</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A quote has a headline price and a list of options: quantity, board thickness, finish, colour, copper weight, delivery speed. Change one at a time and watch the price. You will usually find that a few options, such as an unusual colour or a faster build, change the price a lot, and the rest barely matter.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Then follow the money to your door. The headline price is not what you pay. F0 showed how shipping, customs duty and GST are added to imported goods. For a board order, list every charge:</div>

```text
Board price (quoted)
+ Shipping (chosen method)
+ Customs duty (on value + shipping)
+ GST (on value + shipping + duty)
+ Any handling or clearance fee
= Landed cost
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's real order, 5 boards from JLCPCB:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Line</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Cost</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Board fabrication (5 boards)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">$4.00</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shipping (DHL Express)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">$24.68</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Quoted total</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>$28.68</strong></td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Discount</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">−$10.00</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Paid</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>$18.68</strong></td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Shipping cost six times as much as the boards themselves: the headline board price was the smallest line on the bill. The quote promised a 2-day build and 2–5 business days of shipping. (Customs duty and GST were not recorded.)</div>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/JLCPCB_quote.png" alt="JLCPCB&#x27;s online quote for esp_watch&#x27;s board: 5 two-layer boards at $4.00, with a shipping estimate" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">JLCPCB's online quote for esp\_watch's board: 5 two-layer boards at $4.00, with a shipping estimate</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Quoting the Enclosure</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Do the same for the case. Upload the lid and base (STL or 3MF) to an online 3D printing service, choose a material close to your E1 decision, and record the price, material, lead time and delivery. Compare it with your E5 estimate: the service's price includes machine time, labour and profit, not just the few rupees of filament.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Unit-Cost Model</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">One-Off Costs and Per-Unit Costs</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every product cost splits into two kinds:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>One-off costs</strong>, also called <strong>NRE</strong> (non-recurring engineering) and <strong>tooling</strong>: paid once, whatever the quantity. A test fixture, a solder-paste stencil, or (at volume) a mould.</li><li style="margin:6px 0;">​<strong>Per-unit costs</strong>: paid again for every unit. Parts, the board, the case, assembly time, test time.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The cost of one unit at quantity N is:</div>

```text
unit cost = (one-off costs ÷ N) + per-unit costs at quantity N
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two things change with quantity. The one-off costs are shared across more units, and the per-unit costs themselves usually fall, through price breaks and cheaper processes.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: esp\_watch at 1 and 10</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;background:#fef2f2;border-left:4px solid #dc2626;border-radius:6px;padding:8px 14px;color:#991b1b;">​<strong>All figures are example values</strong>, chosen to show the structure. The modules are B4's Robu prices; everything else is illustrative. Replace every number with your own quotes.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 1: List the per-unit costs.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Per unit (₹)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">1</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">10</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modules (B4: ₹1,416 at 1)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1,416</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1,416</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Small parts: buttons, switch, resistors, headers</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">150</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">120</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery (300 mAh protected cell)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">350</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">350</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Circuit board (at 1 unit, the whole 5-board minimum order lands on one watch)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">750</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">150</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Enclosure, printed by a service</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">300</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">250</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hand assembly: 30 min at ₹200/h</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">100</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">100</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Per-unit total</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>3,066</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>2,386</strong></td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 2: List the one-off costs.</strong> A simple programming and test fixture: ₹5,000. For a single prototype you might skip it (₹0).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 3: Unit cost.</div>

```text
1 unit, no fixture:   0 ÷ 1      + 3,066 = ₹3,066
10 units, fixture:    5,000 ÷ 10 + 2,386 = 500 + 2,386 = ₹2,886
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> At 10 units the fixture adds ₹500 to each unit, but the unit cost still falls, because the minimum board order no longer lands on one watch. One-off costs, and minimum orders that behave like them, dominate at small quantities. At hundreds of units they shrink to almost nothing per unit.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Upload and check.</strong> Upload your F1 zip to at least one fab house, and run a DFM check. Screenshot the report.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Resolve the findings</strong> in KiCad, re-export, re-check, and complete the resolved-issues list.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Get the quotes.</strong> A board quote at your prototype quantity from two suppliers, and an enclosure quote from a printing service. Record every charge to the landed cost. Stop at checkout.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Build the cost model.</strong> One-off and per-unit costs, at 1 and 10 units, with the source of every number: a quote, a listing with its date, or a labelled assumption.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> DFM report screenshots, the resolved-issues list, the quotes with landed costs, and the cost model at 1 and 10 units (spreadsheet), saved in your design pack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. At least one DFM report is saved as a screenshot. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every DFM error was fixed in KiCad and re-checked. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every accepted DFM warning has a written reason. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. There are board quotes from at least two suppliers. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every quote is followed through to a landed cost. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The cost model separates one-off and per-unit costs. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Unit cost is calculated at 1 and 10. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Every number in the model has a source or is labelled as an assumption. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A DFM report flags an annular ring below the fab's minimum. What is the right fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Edit the drill file by hand to make the hole smaller.</li><li style="margin:6px 0;">B. Change the via or pad size in KiCad, re-run DRC, re-export and re-upload.</li><li style="margin:6px 0;">C. Ignore it; the fab will adjust it.</li><li style="margin:6px 0;">D. Choose a different fab without checking.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Fix the design, then regenerate the files, so the fix survives the next export. <strong>A</strong> is undone at the next export and bypasses your own checks. <strong>C</strong> hands a decision to someone who does not know your intent. <strong>D</strong> may move the problem without solving it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> One-off costs are ₹50,000 and per-unit costs ₹1,000. What is the unit cost at 100 units?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. ₹1,000</li><li style="margin:6px 0;">B. ₹1,500</li><li style="margin:6px 0;">C. ₹5,000</li><li style="margin:6px 0;">D. ₹51,000</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> 50,000 ÷ 100 + 1,000 = ₹1,500. <strong>A</strong> ignores the one-off costs. <strong>C</strong> is the one-off cost spread over only 10 units, plus nothing. <strong>D</strong> puts the whole one-off cost on a single unit.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A student's cost model shows ₹3,200 for one unit and ₹3,450 each for ten, even though parts are slightly cheaper at ten. What most likely explains the higher unit cost at ten?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Parts cost more in bulk.</li><li style="margin:6px 0;">B. A one-off cost, such as a test fixture, is shared across only ten units and adds more per unit than the price breaks save.</li><li style="margin:6px 0;">C. The model is wrong; unit cost always falls with quantity.</li><li style="margin:6px 0;">D. Shipping is only charged on larger orders.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> One-off costs divided over a small quantity can outweigh small price breaks. <strong>A</strong> is backwards. <strong>C</strong> ignores one-off costs. <strong>D</strong> is false: shipping applies to every order.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A board quote shows $2 for 5 boards. Why is that not the cost of the boards?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The quote is in dollars.</li><li style="margin:6px 0;">B. Shipping, customs duty, GST and any clearance fees are added between the quote and your door.</li><li style="margin:6px 0;">C. The fab will change the price later.</li><li style="margin:6px 0;">D. Boards are sold in tens.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The landed cost includes everything to your door, as F0 showed, and on a small order these extra charges can be several times the board price. <strong>A</strong> is a conversion, not the missing cost. <strong>C</strong> and <strong>D</strong> are not the reason.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> You need 2 boards. The fab's minimum order is 5, with a landed cost of ₹750. What board cost goes in your cost model?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. ₹150 per board, because 750 ÷ 5 = 150</li><li style="margin:6px 0;">B. ₹375 per board: the whole ₹750 spread over the 2 boards you use, with the quote's source and date noted</li><li style="margin:6px 0;">C. Zero, because boards are cheap</li><li style="margin:6px 0;">D. The per-board price at 1,000 units</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> You pay for the whole minimum order, so its landed cost falls on the boards you use. <strong>A</strong> spreads the cost over three boards you will not use. <strong>C</strong> ignores a real cost. <strong>D</strong> is a quantity you will not buy.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The idea to carry forward: <strong>unit cost is a function of quantity.</strong> Always say at what quantity when you quote a cost.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="../07-capstone/G-capstone-design-pack.md">G — Capstone</a> you will assemble everything you have produced into a single Design Pack, review it against a rubric, and compare it, honestly, with the reference watch.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. JLCPCB. PCB Prototype and PCB Fabrication Manufacturer ("Instant online PCB quote, get PCBs for only $2"; online Gerber viewer). https://jlcpcb.com/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. PCB Power. PCB Manufacturer in India (instant free quote; free DFM check). https://www.pcbpower.com/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. JLCDFM. Free Online PCB DFM Tool (web-based DFM analysis). https://jlcdfm.com/</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
