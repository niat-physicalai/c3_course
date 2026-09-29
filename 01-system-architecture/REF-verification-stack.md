<!-- ASSIGNABLE: verification-stack · home: 01-system-architecture -->

# The Verification Stack
## How to Know Your Design Is Right When Nothing Gets Built

**Course:** C3 — From Problem Statement to Manufacturable Design
**Type:** Reference page. Keep it open throughout the course; it is not a timed unit.

---

### Why This Page Exists

In Part 1, you knew a circuit worked because the LED lit up or the sensor printed a sensible number. In this course nothing is built until the funded build. So for each stage of the design, this page names the check that gives a clear pass or fail. Run it before you call the work done.

## The Full Table

```
| Question | Tool that answers it | What "pass" looks like |
|---|---|---|
| Is every requirement checkable? | Your specification | Every requirement has an ID, a number and a test method |
| Is my architecture coherent? |
``` Requirement allocation table | Every requirement goes to a part of the system, and every part of the system serves at least one requirement |
| Did I pick the right sensor? | Sensor selection matrix | Each rejected option has a written reason, and each chosen sensor has a stated way it can fail |
| Will this part still exist in three years? | Lifecycle status on two distributors plus the manufacturer's page | "Active" in all three places, or a written plan if it is not |
| Does my circuit logic work? | Wokwi, which runs real Arduino code on a simulated ESP32 [1] | The expected serial output appears, and the displays and buttons behave as designed |
| Does my analog or power circuit behave? | Falstad Circuit Simulator for intuition [3], LTspice for accuracy [4] | Voltages and currents stay inside the datasheet limits |
| Is my schematic self-consistent? | KiCad Electrical Rules Check (ERC) | Zero errors |
| Is my symbol right? | Comparing each pin against the datasheet's pin table | Every pin number, name and electrical type matches |
| Is my footprint right? | Pad pitch, pad size, outline and pin 1 checked against the manufacturer's drawing | All four match, and are written down |
| Is my board manufacturable? | KiCad Design Rules Check (DRC) [5], then the fab house's automated DFM report | Zero DRC errors; every DFM warning fixed or explained |
| Does the board fit the enclosure? | CAD interference detection using the real board model | No overlaps, and clearance around tall parts |
| Will the enclosure print? | Slicer preview | No unsupported overhangs or adhesion warnings you have not dealt with |
| Does my firmware match my design? | Comparing code transitions against your state diagram | Every arrow in the diagram exists in code, and nothing extra |
| Are my choices sound? | Comparing with the reference watch, including its mistakes | Every difference is either justified or taught you something |

The last row matters most in a course with no instructor. Whenever your design differs from the reference watch, you must be able to say why. Sometimes your reason will be better than the reference's. The reference watch is the course author's own work, not a polished commercial product, and it has known flaws that you are encouraged to criticise.

## What a Pass Does Not Tell You

Every tool on this page has limits. Two catch students out more than any others.

**A clean DRC means "can be made", not "will work".** The design rules check confirms that tracks are wide enough, gaps are big enough and every pad is connected as the schematic says. It cannot know that you connected a sensor to the wrong pin in the schematic, or that the heart-rate sensor faces away from the wrist. A board can pass DRC perfectly and still be useless.

**Simulators do not model everything.** Wokwi simulates the ESP32-C3, the MPU-6050 motion sensor, the SSD1306 display, pushbuttons and slide switches, but it has no MAX30102 heart-rate sensor [2]. The fix is a **mock sensor**: a small piece of code that stands in for the real sensor and returns made-up but realistic readings. Your application code cannot tell the difference, so you can still test everything around the sensor. You write one in B5 and reuse it in the firmware module.

Simulators also idealise. Wokwi's I²C bus, for example, runs the ESP32 only as the controller on the bus [1], and no simulator reproduces a badly soldered joint, a weak battery or a noisy wrist. Treat a simulator pass as "my logic is right", not "my product works".

<!-- REFPRODUCT:START -->
The reference watch shows why both warnings matter. On the breadboard, one heart-rate module broke the shared I²C bus. No DRC or simulator would have caught it (full story in B3; why the display hid it in D5). That is why this page never says "verified" when it means "simulated".
<!-- REFPRODUCT:END -->

## How to Use This Page

When you finish any piece of work in the course:

1. Find its row in the table above.
2. Run the check it names.
3. Record the result in your design pack: the check, the date and the verdict. If you accepted a warning, write down why.

By the end of the course, that record shows a reviewer that every part of your design has been checked by something other than your own confidence.

---

## References

1. Wokwi. *ESP32 Simulation* (supported ESP32 variants and the simulation-features table, including I²C as "Master only"). https://docs.wokwi.com/guides/esp32
2. Wokwi. *Supported Hardware* (full list of simulated parts, including MPU6050 and SSD1306). https://docs.wokwi.com/getting-started/supported-hardware
3. Paul Falstad. *Circuit Simulator Applet* (interactive, browser-based circuit simulator). https://www.falstad.com/circuit/
4. Analog Devices. *LTspice* (free SPICE simulator, schematic capture and waveform viewer). https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html
5. KiCad. *PCB Editor documentation, version 9.0* (the Design Rules Checker section). https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html
