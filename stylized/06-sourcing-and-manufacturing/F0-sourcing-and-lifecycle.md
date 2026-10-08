<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">F0 — Sourcing Components, and the Lifecycle Trap</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Buying Parts That Exist Today, Will Exist Tomorrow, and Cost What You Think</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 6 — Sourcing and Manufacturing Handoff <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a fully costed BOM with part numbers, links, lifecycle status and unit price at 1 and 10</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Part You Can Buy Today Can Still Be a Problem</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Search an Indian electronics shop for an MPU-6050 motion-sensor module and you will find it listed, for about ₹159. Search the manufacturer's website and you will find something else: TDK lists the MPU-6050 as <strong>Obsolete</strong>, and names the ICM-42670-P as its recommended alternate, with the warning that interchangeability is not guaranteed [1]. The reference watch uses the MPU-6050 anyway, and the author records it as a known issue.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">That is the <strong>lifecycle trap</strong>: a part can be easy to buy today and still be a risk to a product that must be built again next year.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Find</strong> parts with parametric search, and <strong>compare</strong> Indian suppliers with international distributors.</li><li style="margin:6px 0;">​<strong>Read</strong> a stock listing: minimum order, lead time, price breaks and lifecycle status.</li><li style="margin:6px 0;">​<strong>Explain</strong> why an obsolete chip can stay on sale for years, and <strong>plan</strong> for its replacement.</li><li style="margin:6px 0;">​<strong>Calculate</strong> a landed cost, including shipping, customs duty and GST.</li><li style="margin:6px 0;">​<strong>Produce</strong> a fully costed BOM at quantities of 1 and 10.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Where to Buy</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Supplier type</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Examples</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Best for</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Watch out for</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Indian shops</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Robu, Robocraze, Sunrom</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modules and small quantities, fast delivery, prices in rupees including GST</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Stock changes daily; few manufacturer part numbers; no lifecycle information</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Indian arms of global distributors</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Element14 India, Mouser India, DigiKey India</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Genuine parts with full manufacturer part numbers, datasheets and lifecycle status</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Import terms, delivery charges below a threshold</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Direct from Asian distributors</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">LCSC</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Low prices on passives and ICs, especially in tens or hundreds</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">You pay duties and taxes on arrival</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">B4 found that on one day, three of esp\_watch's four modules were out of stock at one Indian shop. A BOM with a single supplier per line is fragile. Give every active part a <strong>second source</strong>: another shop, another distributor, or an equivalent part.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Reading a Stock Listing</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every distributor listing contains the same information, if you know where to look:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Field</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Meaning</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why it matters</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Manufacturer part number (MPN)</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The exact part, including package and options</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"MAX30102" is a family; MAX30102EFD+T is a specific part on tape and reel</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Stock</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How many are available now</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Zero stock means waiting</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Lead time</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How long until more arrive, if out of stock</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Can be weeks or months</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>MOQ</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Minimum order quantity</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">You may have to buy 10 to get 1</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Price breaks</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Unit price at different quantities</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Changes which option is cheapest</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Lifecycle status</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Where the part is in its life</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Decides whether you can build it again</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Price breaks lower the unit price as quantity rises. B4 showed they rarely change a module-versus-chip decision at student quantities.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Lifecycle Status</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Manufacturers and distributors describe a part's stage of life with a few common labels:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Status</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Meaning</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What to do</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Active</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">In production, recommended</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Use it</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>NRND</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Not recommended for new designs; still made for existing customers</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Avoid in a new design unless there is no alternative</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>EOL</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">End of life announced; a <strong>last-time buy</strong> date is usually given</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Buy your lifetime needs before the date, or redesign</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Obsolete</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No longer made</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Buy remaining stock knowingly, and plan a replacement</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two cautions. First, <strong>distributors can label the same part differently</strong>, because each updates its database on its own schedule, and some list their remaining stock of a part the manufacturer has already discontinued. Always check the <strong>manufacturer's own product page</strong> as well. Second, a module listing almost never shows lifecycle at all. The chip on it has a status; the module does not tell you.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Case Study: Why an Obsolete Chip Stays on Sale</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">TDK announced the MPU-6050's discontinuation in July 2023 (notice PCN-000614). Three years later the module is still listed in Indian shops.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Three things keep an obsolete chip on sale:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Last-time buys.</strong> Before production stops, module makers and distributors buy large quantities to keep selling for years.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Distributor stock.</strong> Parts already on shelves are sold until they run out.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Copies.</strong> When a popular chip is widely used, other manufacturers may make compatible or look-alike parts. esp\_watch's own motion sensor reports itself as a clone.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For a student project, that is fine: you can still buy the module. For a product, ask what happens in <strong>year three</strong>. The stock runs out, the price rises, or the next batch contains a different chip that behaves slightly differently. At that point you must switch to a successor, and the successor is rarely a drop-in.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Swapping the chip is a firmware job, too.</strong> The recommended alternate is not guaranteed to be interchangeable [1], and it has a different register map. That is exactly the situation D0's layered firmware prepares for: if the MPU-6050's registers live only in one driver file behind a MotionSensor interface, the swap is a new driver and one line of the application. If they are scattered through the code, it is a rewrite. The hardware may also change: a different module, different pins, a different footprint.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Landed Cost: The Price You Actually Pay</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The price on a listing is rarely what you pay. The <strong>landed cost</strong> includes shipping, customs duty, GST and any handling fees. How they are charged depends on the supplier's terms:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Supplier (India)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How taxes are charged</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it means</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Indian shop</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Price in rupees, GST included</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What you see is close to what you pay, plus delivery</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Mouser India, GST business invoice</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">GST added at checkout; Mouser pays duty and customs fees [3]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Known cost at checkout</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Mouser India, standard invoice</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Duty, customs fees and taxes collected at delivery [3]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">You pay extra when the parcel arrives</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">DigiKey India</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Duty, customs and tax due at delivery; free delivery at ₹7,000 or more, ₹1,200 below [4]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Small orders carry a large delivery charge, and taxes are paid on arrival</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">LCSC</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Customer pays any government or customs charges at the destination [5]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Budget for duty and GST on top of the order</td></tr></tbody></table>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Landed Cost of an Import</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A small order of passives and switches from an international distributor, paid on delivery.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Assumptions</strong> (check the current rates for your parts' customs classification before relying on them):</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">Order value: $30 (about ₹2,640 at <strong>₹88 per dollar</strong>)</li><li style="margin:6px 0;">Shipping: $10 (₹880)</li><li style="margin:6px 0;">Basic customs duty: <strong>10%</strong> of the value plus shipping</li><li style="margin:6px 0;">GST: <strong>18%</strong> on the value plus shipping plus duty</li></ul>

```text
Step 1  Value for duty   goods + shipping         ₹2,640 + ₹880          = ₹3,520
Step 2  Customs duty     10% of value              10% × ₹3,520           = ₹352
Step 3  GST              18% of value + duty       18% × ₹3,872           = ₹697
Step 4  Landed cost      value + duty + GST        ₹3,520 + ₹352 + ₹697   = ₹4,569
        73% more than the goods alone (₹2,640)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> On a small order, shipping and taxes added 73% to the cost. So <strong>batch</strong> imports: order everything at once, pass free-delivery thresholds, and compare the landed cost with an Indian shop's GST-inclusive price.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Fully Costed BOM</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Now put it all together. The deliverable BOM has these columns:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Column</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Example</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Reference</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U3</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Description</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">6-axis motion sensor module, I²C, 3.3 V</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Manufacturer and MPN (chip)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">TDK MPU-6050 (on module)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Supplier and link</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Robu, product page</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Second source</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Another shop, or an alternative module</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lifecycle (manufacturer page, date)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Obsolete, 25 Sep 2026</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Unit price at 1 / 10</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">₹159 / quote needed</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Landed?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes (GST-inclusive Indian listing)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Notes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Clone chip on esp\_watch's module; replacement plan in D0</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's main modules, with prices from B4 (Robu, 24 September 2026, including GST):</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Ref</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Part</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Supplier</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Price at 1</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Lifecycle of the chip</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Risk</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Seeed Studio XIAO ESP32-C3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Robu</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">₹849</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Module: check Seeed</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Out of stock on 24 Sep</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MAX30102 module (black)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Robu</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">₹179</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Chip: check Analog Devices</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Out of stock on 24 Sep; module variant matters (1.8 V vs 3.3 V)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MPU-6050 module</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Robu</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">₹159</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Obsolete</strong> [1]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Out of stock on 24 Sep; replacement needs a new driver</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U4</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SSD1306 0.96" OLED, I²C</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Robu</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">₹229</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check the controller's maker</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pin order varies by seller</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Indian shop listings rarely show price breaks, so the 10 column often needs a quote, or a distributor listing for comparison. Where you cannot find a price, write "quote needed" rather than guessing.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Complete every BOM line.</strong> Start from your B4 preliminary BOM. For each line: MPN, supplier and link, second source, and the date checked.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Record lifecycle.</strong> For every active part, check the manufacturer's page and at least one distributor. Record both, and flag any disagreement.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Price at 1 and 10.</strong> Use price breaks where listed; write "quote needed" where not.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Calculate landed cost</strong> for any imported line, stating your assumed duty rate, GST rate and exchange rate.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Plan for your riskiest part.</strong> One paragraph: what happens if it disappears in year three, and what changes in hardware and firmware.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> the fully costed BOM (spreadsheet), with the lifecycle column and the risk paragraph, saved in your design pack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your costed BOM and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every active part has a manufacturer part number. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every line has a supplier link and the date checked. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every active part has a second source. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every active part's lifecycle is taken from the manufacturer's page. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Any disagreement between sources on lifecycle is noted. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Prices at 1 and 10 are filled in, or marked "quote needed". — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Imported lines include shipping, duty and GST, with stated rates. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The riskiest part has a written replacement plan covering hardware and firmware. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A module is in stock at several Indian shops, but the chip on it is listed as Obsolete by its manufacturer. What is the right conclusion?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The chip is fine, since it is in stock.</li><li style="margin:6px 0;">B. It can be used knowingly for a prototype, but a product needs a replacement plan, because stock will eventually run out or change.</li><li style="margin:6px 0;">C. It must never be used.</li><li style="margin:6px 0;">D. The manufacturer's page must be wrong.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Availability today and lifecycle are different questions. <strong>A</strong> confuses them. <strong>C</strong> is too strong for a student build. <strong>D</strong> dismisses the most authoritative source.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> Mouser lists a sensor as Active and LCSC lists it as Obsolete. On 25 Sep 2026 the manufacturer's page says "Not recommended for new designs". What goes in your BOM's lifecycle column?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Active, because one distributor still stocks it.</li><li style="margin:6px 0;">B. Not recommended for new designs (manufacturer, 25 Sep 2026), with the distributor disagreement noted.</li><li style="margin:6px 0;">C. Obsolete, because the most cautious label is safest.</li><li style="margin:6px 0;">D. Leave it blank until the distributors agree.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer: <strong>B.</strong> The manufacturer is the source; distributors copy it at different times. <strong>A</strong> picks the answer you want. <strong>C</strong> records a status the maker has not given. <strong>D</strong> may never resolve and hides a known risk.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> The manufacturer is the source; distributors copy it at different times. <strong>A</strong> picks the answer you want. <strong>C</strong> has no meaning. <strong>D</strong> is how products get stranded.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A $50 order with $10 shipping arrives with 10% duty on value plus shipping, and 18% GST on value plus shipping plus duty, at ₹88 per dollar. Roughly what is the landed cost?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. ₹4,400</li><li style="margin:6px 0;">B. ₹5,280</li><li style="margin:6px 0;">C. About ₹6,760</li><li style="margin:6px 0;">D. About ₹6,850</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer: <strong>D.</strong> Value ₹4,400 + ₹880 = ₹5,280; duty ₹528; GST 18% × ₹5,808 = ₹1,045; total ≈ ₹6,853. <strong>A</strong> is goods only. <strong>B</strong> leaves out taxes. <strong>C</strong> leaves duty out of the GST base.</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. ₹2,640</li><li style="margin:6px 0;">B. ₹3,520</li><li style="margin:6px 0;">C. About ₹4,570</li><li style="margin:6px 0;">D. About ₹6,000</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> ₹3,520 + ₹352 duty + ₹697 GST ≈ ₹4,569. <strong>A</strong> is the goods only. <strong>B</strong> adds shipping but no taxes. <strong>D</strong> has no consistent basis.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Why is replacing an obsolete sensor with its recommended alternate usually a firmware job as well as a hardware one?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The new sensor needs a new programming language.</li><li style="margin:6px 0;">B. The alternate has a different register map and start-up sequence, so the driver must change; interchangeability is not guaranteed.</li><li style="margin:6px 0;">C. Firmware must always be rewritten when any part changes.</li><li style="margin:6px 0;">D. It is not; recommended alternates are drop-in replacements.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Different registers need a different driver, which D0's layering keeps contained. <strong>A</strong> is false. <strong>C</strong> is too broad; a resistor change needs no firmware. <strong>D</strong> contradicts the manufacturer's own warning.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> DigiKey India charges ₹1,200 delivery below ₹7,000 and collects duty and tax on delivery. You need parts worth ₹1,500. What is the most sensible approach?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Order now; delivery charges do not matter.</li><li style="margin:6px 0;">B. Compare the landed cost with a GST-inclusive Indian listing, or batch with other parts to pass the threshold.</li><li style="margin:6px 0;">C. Always use DigiKey.</li><li style="margin:6px 0;">D. Never import.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> ₹1,200 delivery on ₹1,500 of parts, plus taxes on arrival, may make an Indian shop cheaper; batching changes the maths. <strong>A</strong> ignores a charge nearly as large as the order. <strong>C</strong> and <strong>D</strong> are rules that ignore the numbers.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="F1-pcb-manufacturing-package.md">F1 — The PCB Manufacturing Package</a> you will produce the files a board fabricator needs, and learn what every file in that package is for.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. TDK. MPU-6050 detailed information (product status Obsolete; recommended alternate ICM-42670-P, "Interchangeability is not guaranteed"). https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part\_no=MPU-6050</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. LCSC. MAX30102EFD+T (price breaks at 1+, 10+ and 30+). https://www.lcsc.com/product-detail/C6454833.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Mouser Electronics India. Sales Terms and Conditions (DDP with GST at checkout for GST business invoices, duty and customs paid by Mouser; FCA for standard invoices, duty, customs and taxes collected at delivery). https://www.mouser.in/saleterms/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. DigiKey India. Delivery Time and Cost (free delivery on orders of ₹7,000 or more, ₹1,200 below; CPT, duty, customs and tax due at delivery). https://www.digikey.in/en/help-support/delivery-information/delivery-time-and-cost</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. LCSC. Customs Duties and Taxes ("Customers are expected to pay any amount charged by the government or customs at the destination"). https://www.lcsc.com/help-center/shipping-delivering/customs-duties-taxes</div>
