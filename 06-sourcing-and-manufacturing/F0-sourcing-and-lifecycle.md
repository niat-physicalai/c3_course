# E0 — Sourcing Components, and the Lifecycle Trap
## Buying Parts That Exist Today, Will Exist Tomorrow, and Cost What You Think

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 5 — Sourcing and Manufacturing Handoff
**Time:** ~1 hour · **You will produce:** a fully costed BOM with part numbers, links, lifecycle status and unit price at 1, 10 and 100

---

### A Part You Can Buy Today Can Still Be a Problem

<!-- REFPRODUCT:START -->
Search any Indian electronics shop for an MPU-6050 motion-sensor module and you will find it, cheap and ready to ship. Search the manufacturer's website and you will find something else: TDK lists the MPU-6050 as **Obsolete**, and names the ICM-42670-P as its recommended alternate, with the warning that interchangeability is not guaranteed [1]. The reference watch uses the MPU-6050 anyway, and the author records it as a known issue.
<!-- REFPRODUCT:END -->

Both facts are true at once. That is the **lifecycle trap**: a part can be easy to buy today and still be a risk to a product that must be built again next year. This unit teaches you to read a part's real status, to find it at the right supplier for your quantity, and to turn a list of parts into a BOM with honest costs, including the customs, GST and shipping that students usually forget until the parcel arrives.

### What You Will Be Able to Do After This Reading

- **Find** parts with parametric search, and **compare** Indian suppliers with international distributors.
- **Read** a stock listing: minimum order, lead time, price breaks and lifecycle status.
- **Explain** why an obsolete chip can stay on sale for years, and **plan** for its replacement.
- **Calculate** a landed cost, including shipping, customs duty and GST.
- **Produce** a fully costed BOM at quantities of 1, 10 and 100.

### What Part 1 Already Covered

Part 1 had you buy or receive a kit, and you may have ordered a module or two. **What is new here** is buying for a product: choosing suppliers by quantity, checking lifecycle, and costing every line, including the taxes and fees that only appear at checkout or on delivery.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## Where to Buy

| Supplier type | Examples | Best for | Watch out for |
|---|---|---|---|
| Indian shops | Robu, Robocraze, Sunrom | Modules and small quantities, fast delivery, prices in rupees including GST | Stock changes daily; few manufacturer part numbers; no lifecycle information |
| Indian arms of global distributors | Element14 India, Mouser India, DigiKey India | Genuine parts with full manufacturer part numbers, datasheets and lifecycle status | Import terms, delivery charges below a threshold |
| Direct from Asian distributors | LCSC | Low prices on passives and ICs, especially in tens or hundreds | You pay duties and taxes on arrival |

B2 found that on one day, three of esp_watch's four modules were out of stock at one Indian shop. A BOM with a single supplier per line is fragile. Give every active part a **second source**: another shop, another distributor, or an equivalent part.

## Reading a Stock Listing

Every distributor listing contains the same information, if you know where to look:

| Field | Meaning | Why it matters |
|---|---|---|
| **Manufacturer part number (MPN)** | The exact part, including package and options | "MAX30102" is a family; `MAX30102EFD+T` is a specific part on tape and reel |
| **Stock** | How many are available now | Zero stock means waiting |
| **Lead time** | How long until more arrive, if out of stock | Can be weeks or months |
| **MOQ** | Minimum order quantity | You may have to buy 10 to get 1 |
| **Price breaks** | Unit price at different quantities | Changes which option is cheapest |
| **Lifecycle status** | Where the part is in its life | Decides whether you can build it again |

Price breaks are worth reading carefully. On LCSC, the bare MAX30102 chip was listed at $14.73 each at 1, $14.15 at 10 and $13.15 at 30 [2]. The price falls with quantity, but even at 30 it is still well above a complete ₹179 module (B2). Price breaks change comparisons between chips; they rarely overturn a module-versus-chip decision at student quantities.

<!-- MEDIA
type: screenshot
id: E0-02
caption: Reading a distributor listing: MPN, stock, price breaks and lifecycle in one view
brief: Browser screenshot of a distributor product page (LCSC or Mouser India) for the
  MAX30102EFD+T. Annotate with numbered callouts: 1 the full manufacturer part number,
  2 stock quantity, 3 the price-break table (1+, 10+, 30+ or similar), 4 minimum order
  quantity, 5 lifecycle or product status field (if shown), 6 datasheet link. Crop to the
  product information area. No account or cart details visible.
-->

## Lifecycle Status

Manufacturers and distributors describe a part's stage of life with a few common labels:

| Status | Meaning | What to do |
|---|---|---|
| **Active** | In production, recommended | Use it |
| **NRND** | Not recommended for new designs; still made for existing customers | Avoid in a new design unless there is no alternative |
| **EOL** | End of life announced; a **last-time buy** date is usually given | Buy your lifetime needs before the date, or redesign |
| **Obsolete** | No longer made | Buy remaining stock knowingly, and plan a replacement |

Two cautions. First, **distributors can label the same part differently**, because each updates its database on its own schedule, and some list their remaining stock of a part the manufacturer has already discontinued. Always check the **manufacturer's own product page** as well. Second, a module listing almost never shows lifecycle at all. The chip on it has a status; the module does not tell you.

<!-- MEDIA
type: screenshot
id: E0-01
caption: The manufacturer's product page for the MPU-6050: status Obsolete, with its recommended alternate
brief: Browser screenshot of TDK's product detail page for the MPU-6050, cropped to the
  status area: "Product Status: Obsolete" and "Recommended Alternate Part No.: ICM-42670-P
  (Interchangeability is not guaranteed.)" clearly visible, with the part number heading.
  Highlight the status line in a box. No cookie banners.
-->

## The Case Study: Why an Obsolete Chip Stays on Sale

<!-- REFPRODUCT:START -->
The MPU-6050 is obsolete, according to its manufacturer [1], and the author records the discontinuation notice as TDK PCN-000614, July 2023. Yet in September 2026 the module was still listed by an Indian shop at ₹159 (B2). How?
<!-- REFPRODUCT:END -->

<!-- LINK:VERIFY  want: "TDK product change notice PCN-000614 announcing MPU-6050 discontinuation"  search: "TDK InvenSense PCN-000614 MPU-6050" -->

Three things keep an obsolete chip on sale:

1. **Last-time buys.** Before production stops, module makers and distributors buy large quantities to keep selling for years.
2. **Distributor stock.** Parts already on shelves are sold until they run out.
3. **Copies.** When a popular chip is widely used, other manufacturers may make compatible or look-alike parts. esp_watch's own motion sensor reports itself as a clone.

For a student project, that is fine: you can still buy the module. For a product, ask what happens in **year three**. The stock runs out, the price rises, or the next batch contains a different chip that behaves slightly differently. At that point you must switch to a successor, and the successor is rarely a drop-in.

**Swapping the chip is a firmware job, too.** The recommended alternate is not guaranteed to be interchangeable [1], and it has a different register map. That is exactly the situation C0's layered firmware prepares for: if the MPU-6050's registers live only in one driver file behind a `MotionSensor` interface, the swap is a new driver and one line of the application. If they are scattered through the code, it is a rewrite. The hardware may also change: a different module, different pins, a different footprint.

> **Try it: Check your riskiest part.** Take the active part in your BOM you are least sure about.
> 1. **Predict.** What lifecycle status will the manufacturer give it?
> 2. **Do.** Find the manufacturer's product page and two distributor listings. Record the status each gives, and the date.
> 3. **Explain.** Do they agree? If not, which do you trust, and what is your plan if the part becomes unavailable in year three?

---

## Landed Cost: The Price You Actually Pay

The price on a listing is rarely what you pay. The **landed cost** includes shipping, customs duty, GST and any handling fees. How they are charged depends on the supplier's terms:

| Supplier (India) | Terms | What it means |
|---|---|---|
| Indian shop | Price in rupees, GST included | What you see is close to what you pay, plus delivery |
| Mouser India, GST business invoice | DDP, with GST added at checkout; duty and customs fees paid by Mouser [3] | Known cost at checkout |
| Mouser India, standard invoice | FCA; duty, customs fees and taxes collected at delivery [3] | You pay extra when the parcel arrives |
| DigiKey India | CPT; duty, customs and tax due at delivery; free delivery at ₹7,000 or more, ₹1,200 below [4] | Small orders carry a large delivery charge, and taxes are paid on arrival |
| LCSC | Customer pays any government or customs charges at the destination [5] | Budget for duty and GST on top of the order |

### Worked Example: Landed Cost of an Import

A small order of passives and switches from an international distributor, paid on delivery.

**Assumptions** (check the current rates for your parts' customs classification before relying on them):

- Order value: $30 (about ₹2,640 at **₹88 per dollar**)
- Shipping: $10 (₹880)
- Basic customs duty: **10%** of the value plus shipping
- GST: **18%** on the value plus shipping plus duty

<!-- LINK:VERIFY  want: "Official Indian customs tariff and GST rate for electronic components (HS 8532/8533/8536/8541/8542)"  search: "CBIC customs tariff India HS 8536 basic customs duty and IGST rate" -->

**Step 1: Value for duty.**

```text
Goods + shipping = ₹2,640 + ₹880 = ₹3,520
```

**Step 2: Customs duty.**

```text
10% × ₹3,520 = ₹352
```

**Step 3: GST on everything so far.**

```text
18% × (₹3,520 + ₹352) = 18% × ₹3,872 = ₹697
```

**Step 4: Landed cost.**

```text
₹3,520 + ₹352 + ₹697 = ₹4,569
Compared with the goods alone (₹2,640): 73% more
```

**Check.** On a small order, shipping and taxes almost doubled the cost. The fix is not to avoid imports, but to **batch** them: order everything at once, above free-delivery thresholds, and compare the landed cost with an Indian shop's GST-inclusive price before deciding. The rates above are illustrative; the method, applying duty and GST to value plus shipping, is the part to keep.

---

## The Fully Costed BOM

Now put it all together. The deliverable BOM has these columns:

| Column | Example |
|---|---|
| Reference | U3 |
| Description | 6-axis motion sensor module, I²C, 3.3 V |
| Manufacturer and MPN (chip) | TDK MPU-6050 (on module) |
| Supplier and link | Robu, product page |
| Second source | Another shop, or an alternative module |
| Lifecycle (manufacturer page, date) | Obsolete, 25 Sep 2026 |
| Unit price at 1 / 10 / 100 | ₹159 / ₹159 / ask |
| Landed? | Yes (GST-inclusive Indian listing) |
| Notes | Clone chip on esp_watch's module; replacement plan in C0 |

<!-- REFPRODUCT:START -->
esp_watch's main modules, with prices from B2 (Robu, 24 September 2026, including GST):

| Ref | Part | Supplier | Price at 1 | Lifecycle of the chip | Risk |
|---|---|---|---|---|---|
| U1 | Seeed Studio XIAO ESP32-C3 | Robu | ₹849 | Module: check Seeed | Out of stock that day |
| U2 | MAX30102 module (black) | Robu | ₹179 | Chip: check Analog Devices | Module variant matters (1.8 V vs 3.3 V) |
| U3 | MPU-6050 module | Robu | ₹159 | **Obsolete** [1] | Replacement needs a new driver |
| U4 | SSD1306 0.96" OLED, I²C | Robu | ₹229 | Check the controller's maker | Pin order varies by seller |
<!-- REFPRODUCT:END -->

Indian shop listings rarely show price breaks, so the 10 and 100 columns often need a quote, or a distributor listing for comparison. Where you cannot find a price, write "quote needed" rather than guessing.

---

# Putting It All Together

## Applying What You Have Learned

**1. Complete every BOM line.** Start from your B2 preliminary BOM. For each line: MPN, supplier and link, second source, and the date checked.

**2. Record lifecycle.** For every active part, check the manufacturer's page and at least one distributor. Record both, and flag any disagreement.

**3. Price at 1, 10 and 100.** Use price breaks where listed; write "quote needed" where not.

**4. Calculate landed cost** for any imported line, stating your assumed duty rate, GST rate and exchange rate.

**5. Plan for your riskiest part.** One paragraph: what happens if it disappears in year three, and what changes in hardware and firmware.

**Deliverable:** the fully costed BOM (spreadsheet), with the lifecycle column and the risk paragraph, saved in your design pack.

## Self-Check

Open your costed BOM and answer each item Y or N.

1. Every active part has a manufacturer part number. — Y/N
2. Every line has a supplier link and the date checked. — Y/N
3. Every active part has a second source. — Y/N
4. Every active part's lifecycle is taken from the manufacturer's page. — Y/N
5. Any disagreement between sources on lifecycle is noted. — Y/N
6. Prices at 1, 10 and 100 are filled in, or marked "quote needed". — Y/N
7. Imported lines include shipping, duty and GST, with stated rates. — Y/N
8. The riskiest part has a written replacement plan covering hardware and firmware. — Y/N

---

## Check Your Understanding

**1.** A module is in stock at several Indian shops, but the chip on it is listed as Obsolete by its manufacturer. What is the right conclusion?

- A. The chip is fine, since it is in stock.
- B. It can be used knowingly for a prototype, but a product needs a replacement plan, because stock will eventually run out or change.
- C. It must never be used.
- D. The manufacturer's page must be wrong.

<details>
<summary>Answer</summary>

**B.** Availability today and lifecycle are different questions. **A** confuses them. **C** is too strong for a student build. **D** dismisses the most authoritative source.

</details>

**2.** Two distributors show different lifecycle statuses for the same part. What should you do?

- A. Use the more optimistic one.
- B. Check the manufacturer's own product page and record the date, since distributor databases update on different schedules.
- C. Average them.
- D. Ignore lifecycle.

<details>
<summary>Answer</summary>

**B.** The manufacturer is the source; distributors copy it at different times. **A** picks the answer you want. **C** has no meaning. **D** is how products get stranded.

</details>

**3.** A $30 order with $10 shipping arrives with 10% duty and 18% GST applied to value plus shipping plus duty, at ₹88 per dollar. Roughly what is the landed cost?

- A. ₹2,640
- B. ₹3,520
- C. About ₹4,570
- D. About ₹6,000

<details>
<summary>Answer</summary>

**C.** ₹3,520 + ₹352 duty + ₹697 GST ≈ ₹4,569. **A** is the goods only. **B** adds shipping but no taxes. **D** has no consistent basis.

</details>

**4.** Why is replacing an obsolete sensor with its recommended alternate usually a firmware job as well as a hardware one?

- A. The new sensor needs a new programming language.
- B. The alternate has a different register map and start-up sequence, so the driver must change; interchangeability is not guaranteed.
- C. Firmware must always be rewritten when any part changes.
- D. It is not; recommended alternates are drop-in replacements.

<details>
<summary>Answer</summary>

**B.** Different registers need a different driver, which C0's layering keeps contained. **A** is false. **C** is too broad; a resistor change needs no firmware. **D** contradicts the manufacturer's own warning.

</details>

**5.** DigiKey India charges ₹1,200 delivery below ₹7,000 and collects duty and tax on delivery. You need parts worth ₹1,500. What is the most sensible approach?

- A. Order now; delivery charges do not matter.
- B. Compare the landed cost with a GST-inclusive Indian listing, or batch with other parts to pass the threshold.
- C. Always use DigiKey.
- D. Never import.

<details>
<summary>Answer</summary>

**B.** ₹1,200 delivery on ₹1,500 of parts, plus taxes on arrival, may make an Indian shop cheaper; batching changes the maths. **A** ignores a charge nearly as large as the order. **C** and **D** are rules that ignore the numbers.

</details>

---

## What You Can Now Do, and What Comes Next

- Choose suppliers by quantity, and give every part a second source.
- Read listings for stock, lead time, price breaks and lifecycle.
- Explain the lifecycle trap and plan a replacement, in hardware and firmware.
- Cost a BOM honestly, including the charges that arrive after checkout.

The idea to carry forward: **in stock today is not the same as available for the product's life.** Check the manufacturer, date everything, and plan for your riskiest part.

In [E1 — The PCB Manufacturing Package](E1-pcb-manufacturing-package.md) you will produce the files a board fabricator needs, and learn what every file in that package is for.

---

## References

1. TDK. *MPU-6050 detailed information* (product status Obsolete; recommended alternate ICM-42670-P, "Interchangeability is not guaranteed"). https://product.tdk.com/en/search/sensor/mortion-inertial/imu/info?part_no=MPU-6050
2. LCSC. *MAX30102EFD+T* (price breaks at 1+, 10+ and 30+). https://www.lcsc.com/product-detail/C6454833.html
3. Mouser Electronics India. *Sales Terms and Conditions* (DDP with GST at checkout for GST business invoices, duty and customs paid by Mouser; FCA for standard invoices, duty, customs and taxes collected at delivery). https://www.mouser.in/saleterms/
4. DigiKey India. *Delivery Time and Cost* (free delivery on orders of ₹7,000 or more, ₹1,200 below; CPT, duty, customs and tax due at delivery). https://www.digikey.in/en/help-support/delivery-information/delivery-time-and-cost
5. LCSC. *Customs Duties and Taxes* ("Customers are expected to pay any amount charged by the government or customs at the destination"). https://www.lcsc.com/help-center/shipping-delivering/customs-duties-taxes

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
