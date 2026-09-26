# C5a — Data Off the Device: Serial Format, Logging and Live Plotting
## Designing the Stream Before You Print Anything

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 3 — Firmware
**Time:** ~1 hour · **You will produce:** a serial protocol document, a logged CSV session, and a screenshot of a live plot

---

### "Heart rate is 72!" Is Not Data

Most students' first serial output looks like this:

```text
Starting...
Sensor ok
Heart rate is 72!
steps: 1043   hr=73
Reading... done
```

It is fine for a human watching the monitor. It is useless for anything else. A program cannot reliably pull the numbers out, because the wording changes from line to line. Nobody knows the units. There is no timestamp, so you cannot tell whether readings arrived 20 ms or 20 seconds apart. And the debug messages are mixed in with the data.

The moment you want to plot a signal, save a session to compare later, or check a sensor against a reference, you need a **serial data format**: a stream designed as carefully as a file format, and documented so that someone else can read it. This unit designs one, logs it to a file on your laptop, and plots it live, including a raw optical heart-rate signal, which looks like nothing at all until you filter it.

### What You Will Be Able to Do After This Reading

- **Design** a serial data format with a header, a fixed field order and units declared once.
- **Calculate** whether a stream fits within a serial link's baud rate.
- **Log** a session to a CSV file and **plot** it live with a provided Python script.
- **Explain** why a raw PPG signal must be filtered before a heartbeat can be seen.
- **Write** a serial protocol document that another person could use to parse your stream.

### What Part 1 Already Covered

Part 1 used `Serial.print()` for debugging and structured data as JSON for sending over the network. **What is new here** is treating the serial port as a proper data channel: a versioned, documented format, a bandwidth check, logging to a file, and a laptop-side script that reads and plots the stream.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

## Serial Monitor and Serial Plotter

The Arduino IDE gives you two built-in views of the serial port. The **Serial Monitor** shows text exactly as it arrives. The **Serial Plotter** draws numbers as a graph, one sample per line, with several values per line separated by a delimiter such as a space [1]. Check the tool's page for its exact rules, including how to label each value.

The plotter is good for a quick look. It cannot save a session, apply a filter, or compare a run with yesterday's. For those you need your own format and your own script.

## Designing a Serial Data Format

Follow these rules and any program, spreadsheet or teammate can read your stream:

1. **One record per line.** Each line is one sample, ending in a newline.
2. **A fixed field order.** The same columns, in the same order, on every line.
3. **A header that names each field and its unit, once.** Units in the header, not repeated on every line.
4. **A version line.** When the format changes, the version changes, so old logs are not misread.
5. **Everything that is not data starts with `#`.** Debug messages, start-up notes and errors can still be printed, and a parser simply skips them.
6. **A timestamp on every line**, from `millis()`, so gaps and rates are visible.

### CSV or JSON Lines?

Two formats are common:

| | CSV lines | Newline-delimited JSON |
|---|---|---|
| Example line | `1520,50213,2` | `{"t_ms":1520,"ppg":50213,"steps":2}` |
| Bytes per sample | Small | About 2–3 times larger |
| Field names | Once, in the header | On every line |
| Adding a field later | Changes the column order; bump the version | Old parsers can ignore the new key |
| Opens directly in a spreadsheet | Yes | No |
| Matches your network payloads (C5b) | No | Yes |

For a fast sensor stream going to a laptop, CSV is usually the better choice: small, and it opens straight into a spreadsheet. For occasional structured messages, JSON lines are easier to extend. This unit uses CSV.

Here is the stream this unit's firmware produces:

```text
# esp_watch_stream v1
t_ms,ppg_counts,steps
1520,50213,2
1540,50251,2
1560,50198,2
```

### Worked Example: Will the Stream Fit?

A serial link has a fixed capacity, set by its **baud rate**. With the common 8-N-1 setting, each byte takes 10 bits on the wire: a start bit, 8 data bits and a stop bit.

**Step 1: Bytes per line.** A typical line, `1520,50213,2` plus the newline characters, is about 14 characters. Allow for larger values later in a session (a seven-digit timestamp, more steps): **assume 22 bytes per line.**

**Step 2: Lines per second.** 50 samples a second.

**Step 3: Bits per second needed.**

```text
22 bytes × 50 lines × 10 bits = 11,000 bits per second
```

**Step 4: Compare with the link.**

```text
At 115,200 baud: 11,000 ÷ 115,200 = 9.5% of capacity
At 9,600 baud:   11,000 ÷ 9,600   = 115%, so it does not fit
```

**Check.** At 115,200 baud there is plenty of room, even for extra columns. At 9,600, a common default in older examples, the stream is larger than the link, so the serial buffer fills, the sketch stalls inside `Serial.print()` waiting for space, and your careful non-blocking timing from C4 quietly breaks. The same line as JSON would be about 40 bytes, 20,000 bits per second: still fine at 115,200, but worth checking every time you add fields.

> **Try it: Size your own stream.** Write one example line of your product's serial format.
> 1. **Predict.** Will it fit at 115,200 baud at your highest sample rate?
> 2. **Do.** Count the bytes in your longest realistic line, multiply by lines per second and by 10.
> 3. **Explain.** What percentage of the link does it use? What would you drop, or slow down, if it did not fit?

## The Firmware Side

The provided sketch [`assets/code/C5a-serial-stream/sketch.ino`](../assets/code/C5a-serial-stream/sketch.ino) prints the header once, then one CSV line every 20 ms, using the `millis()` pattern from C4. It runs on any ESP32 or in Wokwi. Because Wokwi has no MAX30102, the PPG value is synthetic: a large, slowly drifting level with a small pulse on top, plus noise, which is what a real optical signal looks like.

```cpp
long syntheticPpg(unsigned long t_ms) {
  float t = t_ms / 1000.0f;
  float drift = 2000.0f * sinf(2.0f * PI * 0.05f * t);      // slow drift
  float pulse = 150.0f * sinf(2.0f * PI * 1.2f * t);        // 72 bpm
  float noise = random(-40, 41);
  return 50000L + (long)(drift + pulse + noise);
}
```

> **Teaching model.** Real PPG signals are messier than this: their pulse shape is not a sine wave, and motion adds large, irregular disturbances. The model keeps the one feature that matters here: a small pulse riding on a large, wandering level.

## Logging and Plotting on the Laptop

The provided script [`assets/code/C5a-plot-serial.py`](../assets/code/C5a-plot-serial.py) does three jobs: it reads the stream, saves every line to a timestamped CSV file, and plots the data live. It needs Python with two packages, installed with `pip install pyserial matplotlib`.

It reads from any of three sources:

```text
python3 C5a-plot-serial.py COM5                      # a board on a Windows serial port
python3 C5a-plot-serial.py /dev/ttyUSB0              # a board on Linux or macOS
python3 C5a-plot-serial.py rfc2217://localhost:4000  # the simulated board in Wokwi for VS Code
python3 C5a-plot-serial.py --replay session.csv      # a saved session, no hardware at all
```

The third line works because Wokwi for VS Code can forward the simulated serial port over the network, and pyserial can open it like a real port [2]. Add `rfc2217ServerPort = 4000` to the project's `wokwi.toml` to turn it on. The last line needs nothing but a saved file, so you can practise plotting and filtering with any log, including one a classmate sends you.

<!-- MEDIA
type: screenshot
id: C5a-02
caption: Wokwi for VS Code forwarding the simulated serial port to the plotting script
brief: VS Code with the Wokwi simulator tab open, running the C5a-serial-stream sketch on
  an ESP32-C3 (serial output lines of CSV visible in the Wokwi terminal). In the editor,
  wokwi.toml open with the line rfc2217ServerPort = 4000 highlighted. An integrated
  terminal below running "python3 C5a-plot-serial.py rfc2217://localhost:4000", with the
  matplotlib window partly visible beside VS Code. Light theme.
-->

Two details in the script follow the format rules. It skips any line starting with `#` or `t_ms`, so the header and debug messages never reach the plot. And it skips any line it cannot parse instead of crashing, because a real serial stream will occasionally deliver half a line.

<!-- MEDIA
type: screenshot
id: C5a-01
caption: The live plot: raw PPG on top, filtered below, where the heartbeat finally appears
brief: The matplotlib window produced by C5a-plot-serial.py in replay or live mode, about
  10 seconds of data. Top panel "raw PPG (counts)": a slowly wandering line between about
  49,000 and 52,000 with tiny ripples barely visible. Bottom panel "raw minus baseline":
  a clear repeating wave, about 12 cycles across the window, swinging roughly ±300. Axis
  labels readable. A terminal beside it showing the command used and the name of the
  session CSV file written.
-->

## Why Raw PPG Looks Like Nothing

Plot the raw signal and you see a line that wanders slowly up and down, with, if you look carefully, a tiny ripple. The heartbeat is the ripple.

```text
Raw PPG level:   about 50,000 counts
Slow drift:      ± 2,000 counts   (breathing, pressure, movement)
Pulse:           ±   150 counts   (the heartbeat)
```

The pulse is less than a tenth of the drift, so on a graph scaled to fit the drift it is almost flat. To see it, remove the slow part. The script uses the simplest possible method: it keeps a **moving average** of the last 25 samples (half a second), treats that as the slowly changing **baseline**, and plots each sample minus the baseline. Anything slower than about half a second is subtracted away. The heartbeat, which repeats faster than that, is left.

> **Teaching model.** Subtracting a moving average is a crude high-pass filter. Real heart-rate algorithms use better filters, and also reject motion, but the principle is the same: separate the fast pulse from the slow level.

This is why the raw PPG waveform is a good first thing to plot. It teaches you, visually and in about a minute, that raw sensor data often needs processing before it means anything, and that the processing has to be designed.

> **Try it: Tune the filter.** Run the script in replay mode on a logged session.
> 1. **Predict.** What will the bottom plot look like if `SMOOTH` is 5 samples (0.1 s)? If it is 250 (5 s)?
> 2. **Do.** Change `SMOOTH` to each value and run it again.
> 3. **Explain.** At 5, what happened to the pulse itself? At 250, what came back into the plot? Why does the best value depend on the heart rate you expect?

## The Serial Protocol Document

Write down your format so that someone else could write a parser without asking you anything. Keep it short:

```markdown
# Serial protocol — <product> — esp_watch_stream v1

Link: USB serial, 115,200 baud, 8-N-1
Rate: one data line every 20 ms (50 per second)
Line ending: CR LF

Lines starting with # are comments (version, debug, errors). Ignore them.
The first non-comment line is the header.

| Column | Type | Unit | Range | Meaning |
|---|---|---|---|---|
| t_ms | integer | ms | 0 to 4,294,967,295 (wraps after ~49.7 days) | millis() at the sample |
| ppg_counts | integer | ADC counts | 0 to 262,143 | raw PPG reading |
| steps | integer | steps | 0 upwards | total since boot |

Bandwidth: longest line ~22 bytes → ~11,000 bit/s, about 9.5% of the link.
Changes from the previous version: none (first version).
```

The range column deserves care. It tells a parser what counts as a damaged line, and it records limits that are easy to forget, such as `millis()` wrapping.

The `ppg_counts` range comes from the MAX30102 datasheet: its ADC resolution is 15 to 18 bits, set by the LED pulse width, and FIFO data is always left-justified in an 18-bit field, so values run from 0 to 262,143 [3].

---

# Putting It All Together

## Applying What You Have Learned

**1. Design your format.** List every value your product streams, with type, unit and range. Choose CSV or JSON lines and say why. Add a version line and a header.

**2. Check the bandwidth.** Calculate your stream's bits per second and the percentage of your baud rate.

**3. Stream it.** Adapt the provided sketch to print your format, using a mock for any sensor you do not have.

**4. Log a session.** Record at least 60 seconds with the provided script, from Wokwi, from hardware if you have it, or by saving the simulator's serial output to a file.

**5. Plot it.** Take a screenshot of the live or replayed plot, with at least one signal filtered.

**Deliverable:** your serial protocol document, the logged CSV file and the plot screenshot, saved in your design pack.

## Self-Check

Open your protocol document and CSV file and answer each item Y or N.

1. The stream starts with a version line and a header naming every field. — Y/N
2. Every field's unit is stated once, in the header or the protocol document. — Y/N
3. Every data line has a timestamp. — Y/N
4. Every non-data line starts with `#`. — Y/N
5. The protocol document states the baud rate, sample rate and bandwidth used. — Y/N
6. The protocol document gives a range for every field. — Y/N
7. The logged CSV covers at least 60 seconds. — Y/N
8. The plot screenshot shows at least one filtered signal. — Y/N

---

## Check Your Understanding

**1.** A stream sends 30-byte lines 100 times a second at 115,200 baud, 8-N-1. What fraction of the link does it use?

- A. About 2.6%
- B. About 21%
- C. About 26%
- D. It does not fit.

<details>
<summary>Answer</summary>

**C.** 30 bytes × 100 × 10 bits = 30,000 bits per second, and 30,000 ÷ 115,200 ≈ 26%. **B** uses 8 bits per byte, forgetting the start and stop bits. **A** is ten times too small. **D** is wrong: 26% fits comfortably.

</details>

**2.** A student's firmware prints `Heart rate: 72 bpm` on some lines and `steps=1043` on others. Their Python parser crashes. What is the root cause?

- A. Python cannot read serial data.
- B. There is no fixed format: fields, order and wording change from line to line, so no parser can rely on them.
- C. The baud rate is too low.
- D. The heart rate is too high.

<details>
<summary>Answer</summary>

**B.** A stream meant for programs needs one record per line with fixed fields. **A** is false; pyserial reads it fine. **C** would garble characters, not change the wording. **D** is irrelevant.

</details>

**3.** A raw PPG plot looks like a slowly wandering line with no visible heartbeat. What is the best explanation?

- A. The sensor is broken.
- B. The pulse is small compared with the slow drift, so it is hidden at this scale; subtracting a moving baseline reveals it.
- C. The sample rate is too high.
- D. The heart has stopped.

<details>
<summary>Answer</summary>

**B.** A PPG pulse is a small ripple on a large, drifting level, and the drift dominates the plot's scale. **A** jumps to a conclusion before processing the data. **C** is not the issue; a higher rate shows the pulse better, not worse. **D** is not a serious engineering explanation.

</details>

**4.** Why should debug messages in a data stream start with `#`?

- A. It makes them print faster.
- B. A parser can skip them reliably, so debug output can stay in the firmware without corrupting the data.
- C. The Serial Monitor requires it.
- D. It saves memory.

<details>
<summary>Answer</summary>

**B.** A simple, documented rule separates data from everything else. **A** and **D** are not effects of the prefix. **C** is false; the Serial Monitor shows any text.

</details>

**5.** The firmware's stream needs 11,000 bits per second, but the serial port is set to 9,600 baud. The sketch uses the non-blocking `millis()` pattern throughout. What happens?

- A. Nothing; non-blocking code is unaffected.
- B. The output buffer fills and `Serial.print()` waits for space, so the loop stalls and the careful timing breaks.
- C. The extra data is compressed automatically.
- D. The baud rate adjusts itself.

<details>
<summary>Answer</summary>

**B.** When more data is printed than the link can send, the print call must wait, which makes it a blocking call in disguise. **A** overlooks that printing itself can block. **C** and **D** do not happen.

</details>

---

## What You Can Now Do, and What Comes Next

- Design a documented serial data format with a version, a header and units.
- Check a stream against the link's capacity before it becomes a hidden stall.
- Log sessions to a file and plot them live or from a replay.
- Filter a raw signal enough to see what it contains.

The idea to carry forward: **design the stream like a file format, because that is what it becomes the moment you save it.**

In [C5b — Connectivity and Persistence](C5b-connectivity-and-persistence.md) you will send the same data over the network to a dashboard, keep working when the network disappears, and store settings that survive a power cycle.

---

## References

1. Arduino. *Using the Serial Plotter Tool* (Arduino IDE 2: data format, delimiters and labels). https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-serial-plotter/
2. Wokwi. *Configuring Your Project (wokwi.toml)* (serial port forwarding with `rfc2217ServerPort`, and connecting with PySerial's `serial_for_url`). https://docs.wokwi.com/vscode/project-config
3. Analog Devices. *MAX30102 datasheet* (ADC resolution 15–18 bits set by LED_PW; FIFO data left-justified with the MSB in bit 17). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
