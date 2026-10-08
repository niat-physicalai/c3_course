# Crux — module 02: Sensing & Hardware Architecture

## B0 — Common Sensors, and Choosing the Right One for the Job
- Seven families; know what each *actually* measures and how it fails (PIR misses a still person, gyros drift, gas sensors drift…). (B0#seven-families)
- Measurand vs proxy: an accelerometer measures acceleration, a PPG measures reflected light; write down when each proxy lies. (B0#sensing-is-measuring-a-stand-in)
- Nine questions in order; the last — false positive or false negative, which is costlier — changes decisions most. (B0#the-questions-in-order)
- Heart rate from one wrist, passively: ECG (deliberate action), chest strap (user tolerance), piezo (placement) rejected; PPG kept with motion, fit, light weaknesses; activity error ~30% higher, signal crossover. (B0#worked-example-1-heart-rate-from-a-wrist-without-the-wearer-doing-anything)
- Conveyor: break-beam enough for counting, hopeless for caps; the cap check's false negative reaches a customer. (B0#worked-example-2-three-sensing-jobs-in-one-machine)
- Selection matrix: one row per quantity, with a rejected alternative and why. (B0#the-matrix)
- Images: B0-01.svg (PPG and where it goes wrong) → proxy point; B0-02.svg (conveyor) → costlier-error point.

## B1 — Talking to Sensors: Choosing the Interface
- I²C / SPI / UART / analog / pulse compared on wires, devices, speed, pull-ups, read-back, distance. (B1#the-interfaces-side-by-side)
- Pins cost more than speed on a small board; a shared bus shares time, pull-ups and fate; some interfaces cannot read back. (B1#the-interfaces-side-by-side)
- Display to SPI? ~30× faster but 4–5 pins (strapping or debug UART); real problem is bus time → redraw on change. (B1#worked-example-should-espwatchs-display-move-to-spi)
- Per peripheral: what the part offers, pins, data, sharing, distance, failure; ESP32-C3 has one I²C controller. (B1#choosing-peripheral-by-peripheral)
- Faults by symptom: floating address pin, address clash, baud mismatch, missing common ground; floating ADC reads 142 mV; judge the bus by a device you read from. (B1#when-interfaces-fail)
- Images: B1-01.svg (display on I²C vs SPI) → SPI decision.

## B2 — Hardware Architecture and Block Diagram
- Block diagram: one box per part, every connection incl. power/ground, labelled lines, shared bus drawn shared; it is what the schematic is checked against. (B2#what-a-hardware-block-diagram-shows)
- Interface table columns: signal, from→to, type, voltage, direction, data rate, notes. (B2#the-interface-table)
- esp_watch: XIAO + three modules on one I²C bus (0x3C, 0x68, 0x57), buttons D10/D9, SW3, protected LiPo. (B2#the-block-diagram, B2#the-interface-table-1)
- Full screen 1,024 bytes × 9 clocks → 23 ms predicted / ~25 ms measured at 400 kHz; 30 redraws/s = 75% of bus; sensors ~2% → redraw on change. (B2#worked-example-predicting-a-display-update)
- Record I²C line voltage, how the address is set, the chip's supply limits. (B2#what-the-reference-watch-learned-the-hard-way)
- Images: Schematic.png (remote) — not used; Claude-made block diagram instead.

## B3 — Electrical Architecture: MCU, Power, Buses and Pins
- MCU class from flash/RAM, pins (+20%), radio, module vs bare chip; a pre-certified module saves most radio approval work. (B3#what-do-you-actually-need, B3#module-or-bare-chip)
- Power tree: source → conversion → switch → load; SW3 off + USB = runs but cannot charge; no divider = no battery level. (B3#the-power-tree)
- Current budget per mode (modelled): continuous HR 5.5 h; every 10 min 1.8–2.7 days; on demand 2.7–6.0 days. (B3#worked-example-hours-or-days-duty-cycling-the-heart-rate-sensor)
- Modules carry their own decoupling; protection table. (B3#decoupling-and-protection)
- Pull-ups: R_min 967 Ω, R_max 7,081 Ω at 400 kHz/50 pF; 3 pairs 1.57 kΩ (2.1 mA), 4 pairs 1.18 kΩ (2.8 mA); count before adding. (B3#sizing-pull-up-resistors, B3#worked-example-how-many-pull-ups-is-too-many)
- Strapping pins D0/D8/D9 high at reset; idle-low interrupt off them; analog on ADC1 (D0–D2). (B3#not-all-pins-are-equal, B3#worked-example-espwatchs-pin-map)
- Images: B3-01.png (spreadsheet, too dense for a slide) → chart instead; B3-02.svg (pin map; labels overlap when rasterised) → Claude-made pin map.

## B4 — Component Selection: Modules or Discrete ICs?
- Module vs discrete IC trade-offs; decide per part: fit, assembly, application circuit, quantity. esp_watch: modules for every active part, hence thick. (B4#what-you-gain-and-what-you-give-up, B4#deciding-per-part)
- Absolute maximum = damage limit; recommended = guaranteed to work. MAX30102 VDD 1.7–2.0 V, abs max 2.2 V → needs 1.8 V and 3.3 V. (B4#absolute-maximum-vs-recommended-operating-conditions)
- A module's listing is not the chip's datasheet: green module 1.8 V pull-ups, black 3.3 V. (B4#the-modules-listing-is-not-the-chips-datasheet)
- Weighted matrix: green 11 (disqualified), black 18, bare chip 12. (B4#worked-example-three-ways-to-measure-heart-rate)
- Stock at more than one supplier, price at 1 and 10, lifecycle; preliminary BOM ₹1,416 main modules. (B4#parametric-search-and-stock, B4#the-preliminary-bom)
- Images: pcb_front.png (B4#deciding-per-part) → assets/slides/02/esp_watch-pcb_front.png.

## B5 — Virtual Prototyping
- Falstad = voltages and edges; Wokwi = firmware with pin map. (B5#two-simulators-two-questions)
- t_r = 0.8473 × R × C: 4.7 kΩ 199 ns, 10 kΩ 424 ns, 1.57 kΩ 67 ns vs 300 ns limit. (B5#worked-example-three-pull-up-values)
- 1.82 V idle bus sits in the undefined band (0.825–2.475 V); fixes: matching module, jumper, level shifter. (B5#when-the-bus-sits-at-the-wrong-voltage)
- Divider τ = 50 ms, settle 250 ms; supply dips under a radio burst. (B5#a-battery-dividers-settling-time, B5#supply-dips-under-load)
- Mock sensor with the same functions as the real driver. (B5#the-mock-sensor)
- I²C trace START → STOP; 17 bytes ≈ 0.4 ms. (B5#what-an-i²c-transaction-looks-like)
- Write down what each simulation did not include. (B5#what-each-simulator-cannot-tell-you)
- Images: i2c-debug-output.png is MISSING; Claude-made trace diagram instead.
