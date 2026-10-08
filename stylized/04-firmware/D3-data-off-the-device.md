<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">D3 — Data Off the Device: Serial Format, Logging and Live Plotting</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Designing the Stream Before You Print Anything</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 4 — Firmware <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a serial protocol document, a logged CSV session, and a screenshot of a live plot</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">"Heart rate is 72!" Is Not Data</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Most students' first serial output looks like this:</div>

```text
Starting...
Sensor ok
Heart rate is 72!
steps: 1043   hr=73
Reading... done
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">It is fine for a human watching the monitor. It is useless for anything else. A program cannot reliably pull the numbers out, because the wording changes from line to line. Nobody knows the units. There is no timestamp, so you cannot tell whether readings arrived 20 ms or 20 seconds apart. And the debug messages are mixed in with the data.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The moment you want to plot a signal, save a session to compare later, or check a sensor against a reference, you need a <strong>serial data format</strong>: a stream designed as carefully as a file format, and documented so that someone else can read it. This unit designs one, logs it to a file on your laptop, and plots it live, including a raw optical heart-rate signal, which looks like nothing at all until you filter it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Design</strong> a serial data format with a header, a fixed field order and units declared once.</li><li style="margin:6px 0;">​<strong>Calculate</strong> whether a stream fits within a serial link's baud rate.</li><li style="margin:6px 0;">​<strong>Log</strong> a session to a CSV file and <strong>plot</strong> it live with a provided Python script.</li><li style="margin:6px 0;">​<strong>Explain</strong> why a raw PPG signal must be filtered before a heartbeat can be seen.</li><li style="margin:6px 0;">​<strong>Write</strong> a serial protocol document that another person could use to parse your stream.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 used Serial.print() for debugging and JSON for network messages. Here the serial port becomes a documented data channel.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Serial Monitor and Serial Plotter</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The Arduino IDE gives you two built-in views of the serial port. The <strong>Serial Monitor</strong> shows text exactly as it arrives. The <strong>Serial Plotter</strong> draws numbers as a graph, one sample per line, with several values per line separated by a delimiter such as a space [1]. Check the tool's page for its exact rules, including how to label each value.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The plotter is good for a quick look. It cannot save a session, apply a filter, or compare a run with yesterday's. For those you need your own format and your own script.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Designing a Serial Data Format</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Follow these rules and any program, spreadsheet or teammate can read your stream:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>One record per line.</strong> Each line is one sample, ending in a newline.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>A fixed field order.</strong> The same columns, in the same order, on every line.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>A header that names each field and its unit, once.</strong> Units in the header, not repeated on every line.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>A version line.</strong> When the format changes, the version changes, so old logs are not misread.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Everything that is not data starts with #.</strong> Debug messages, start-up notes and errors can still be printed, and a parser simply skips them.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. <strong>A timestamp on every line</strong>, from millis(), so gaps and rates are visible.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">CSV or JSON Lines?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two formats are common:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;"></th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">CSV lines</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Newline-delimited JSON</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Example line</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">1520,50213,2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">{"t\_ms":1520,"ppg":50213,"steps":2}</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Bytes per sample</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Small</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">About 2–3 times larger</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Field names</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Once, in the header</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">On every line</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Adding a field later</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Changes the column order; bump the version</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Old parsers can ignore the new key</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Opens directly in a spreadsheet</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Matches your network payloads (D4)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For a fast sensor stream going to a laptop, CSV is usually the better choice: small, and it opens straight into a spreadsheet. For occasional structured messages, JSON lines are easier to extend. This unit uses CSV.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is the stream this unit's firmware produces:</div>

```text
# esp_watch_stream v1
t_ms,ppg_counts,steps
1520,50213,2
1540,50251,2
1560,50198,2
```

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Will the Stream Fit?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A serial link has a fixed capacity, set by its <strong>baud rate</strong>. With the common 8-N-1 setting, each byte takes 10 bits on the wire: a start bit, 8 data bits and a stop bit.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 1: Bytes per line.</strong> A typical line, 1520,50213,2 plus the newline characters, is about 14 characters. Allow for larger values later in a session (a seven-digit timestamp, more steps): <strong>assume 22 bytes per line.</strong></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Step 2: Lines per second.</strong> 50 samples a second.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 3: Bits per second needed.</div>

```text
22 bytes × 50 lines × 10 bits = 11,000 bits per second
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Step 4: Compare with the link.</div>

```text
At 115,200 baud: 11,000 ÷ 115,200 = 9.5% of capacity
At 9,600 baud:   11,000 ÷ 9,600   = 115%, so it does not fit
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> At 115,200 baud there is plenty of room. At 9,600, a common default in older examples, the stream is bigger than the link. The output buffer fills, Serial.print() waits for space, and the non-blocking timing from D2 breaks. This applies to a UART link, as in Wokwi or on a board with a USB-to-serial chip. The XIAO ESP32-C3's native USB port ignores the baud setting. The same line as JSON would be about 40 bytes, 20,000 bits per second: still fine at 115,200, but worth checking every time you add fields.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Firmware Side</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The provided sketch <a href="../assets/code/D3-serial-stream/sketch.ino">assets/code/D3-serial-stream/sketch.ino</a> prints the header once, then one CSV line every 20 ms, using the millis() pattern from D2. It runs on any ESP32 or in Wokwi. Because Wokwi has no MAX30102, the PPG value is synthetic: a large, slowly drifting level with a small pulse on top, plus noise, which is what a real optical signal looks like.</div>

```cpp
long syntheticPpg(unsigned long t_ms) {
  float t = t_ms / 1000.0f;
  float drift = 2000.0f * sinf(2.0f * PI * 0.05f * t);      // slow drift
  float pulse = 150.0f * sinf(2.0f * PI * 1.2f * t);        // 72 bpm
  float noise = random(-40, 41);
  return 50000L + (long)(drift + pulse + noise);
}
```

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>Real PPG signals are messier than this: their pulse shape is not a sine wave, and motion adds large, irregular disturbances. The model keeps the one feature that matters here: a small pulse riding on a large, wandering level.</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Logging and Plotting on the Laptop</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The provided script <a href="../assets/code/D3-plot-serial.py">assets/code/D3-plot-serial.py</a> does three jobs: it reads the stream, saves every line to a timestamped CSV file, and plots the data live. It needs Python with two packages, installed with pip install pyserial matplotlib.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">It reads from any of three sources:</div>

```text
python3 D3-plot-serial.py COM5                      # a board on a Windows serial port
python3 D3-plot-serial.py /dev/ttyUSB0              # a board on Linux or macOS
python3 D3-plot-serial.py rfc2217://localhost:4000  # the simulated board in Wokwi for VS Code
python3 D3-plot-serial.py --replay session.csv      # a saved session, no hardware at all
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The third line works because Wokwi for VS Code can forward the simulated serial port over the network, and pyserial can open it like a real port [2]. Add rfc2217ServerPort = 4000 to the project's wokwi.toml to turn it on. The last line needs nothing but a saved file, so you can practise plotting and filtering with any log, including one a classmate sends you.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two details in the script follow the format rules. It skips any line starting with # or t\_ms, so the header and debug messages never reach the plot. And it skips any line it cannot parse instead of crashing, because a real serial stream will occasionally deliver half a line.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Why Raw PPG Looks Like Nothing</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Plot the raw signal and you see a line that wanders slowly up and down, with, if you look carefully, a tiny ripple. The heartbeat is the ripple.</div>

```text
Raw PPG level:   about 50,000 counts
Slow drift:      ± 2,000 counts   (breathing, pressure, movement)
Pulse:           ±   150 counts   (the heartbeat)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The pulse is less than a tenth of the drift, so on a graph scaled to fit the drift it is almost flat. To see it, remove the slow part. The script uses the simplest possible method: it keeps a <strong>moving average</strong> of the last 25 samples (half a second), treats that as the slowly changing <strong>baseline</strong>, and plots each sample minus the baseline. The average follows the drift, which changes over many seconds, but cannot keep up with each beat. Subtracting it removes most of the drift and leaves the pulse.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>Subtracting a moving average is a crude high-pass filter. Real heart-rate algorithms use better filters, and also reject motion, but the principle is the same: separate the fast pulse from the slow level.</div></div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Tune the filter.</div><div>Run the script in replay mode on a logged session.</div><div>1. <strong>Predict.</strong> What will the bottom plot look like if SMOOTH is 5 samples (0.1 s)? If it is 250 (5 s)?</div><div>2. <strong>Do.</strong> Change SMOOTH to each value and run it again.</div><div>3. <strong>Explain.</strong> At 5, what happened to the pulse itself? At 250, what came back into the plot? Why does the best value depend on the heart rate you expect?</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Serial Protocol Document</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Write down your format so that someone else could write a parser without asking you anything. Keep it short:</div>

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

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The range column deserves care. It tells a parser what counts as a damaged line, and it records limits that are easy to forget, such as millis() wrapping.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The ppg\_counts range comes from the MAX30102 datasheet: its ADC resolution is 15 to 18 bits, set by the LED pulse width, and FIFO data is always left-justified in an 18-bit field, so values run from 0 to 262,143 [3].</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Design your format.</strong> List every value your product streams, with type, unit and range. Choose CSV or JSON lines and say why. Add a version line and a header.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Check the bandwidth.</strong> Calculate your stream's bits per second and the percentage of your baud rate.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Stream it.</strong> Adapt the provided sketch to print your format, using a mock for any sensor you do not have.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Log a session.</strong> Record at least 60 seconds with the provided script, from Wokwi, from hardware if you have it, or by saving the simulator's serial output to a file.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Plot it.</strong> Take a screenshot of the live or replayed plot, with at least one signal filtered.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> your serial protocol document, the logged CSV file and the plot screenshot, saved in your design pack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your protocol document and CSV file and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The stream starts with a version line and a header naming every field. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every field's unit is stated once, in the header or the protocol document. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every data line has a timestamp. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every non-data line starts with #. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The protocol document states the baud rate, sample rate and bandwidth used. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The protocol document gives a range for every field. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. The logged CSV covers at least 60 seconds. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The plot screenshot shows at least one filtered signal. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A stream sends 30-byte lines 100 times a second at 115,200 baud, 8-N-1. What fraction of the link does it use?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. About 2.6%</li><li style="margin:6px 0;">B. About 21%</li><li style="margin:6px 0;">C. About 26%</li><li style="margin:6px 0;">D. It does not fit.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> 30 bytes × 100 × 10 bits = 30,000 bits per second, and 30,000 ÷ 115,200 ≈ 26%. <strong>B</strong> uses 8 bits per byte, forgetting the start and stop bits. <strong>A</strong> is ten times too small. <strong>D</strong> is wrong: 26% fits comfortably.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A student's firmware prints Heart rate: 72 bpm on some lines and steps=1043 on others. Their Python parser crashes. What is the root cause?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Python cannot read serial data.</li><li style="margin:6px 0;">B. There is no fixed format: fields, order and wording change from line to line, so no parser can rely on them.</li><li style="margin:6px 0;">C. The baud rate is too low.</li><li style="margin:6px 0;">D. The heart rate is too high.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A stream meant for programs needs one record per line with fixed fields. <strong>A</strong> is false; pyserial reads it fine. <strong>C</strong> would garble characters, not change the wording. <strong>D</strong> is irrelevant.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A raw PPG plot looks like a slowly wandering line with no visible heartbeat. What is the best explanation?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The sensor is broken.</li><li style="margin:6px 0;">B. The pulse is small compared with the slow drift, so it is hidden at this scale; subtracting a moving baseline reveals it.</li><li style="margin:6px 0;">C. The sample rate is too high.</li><li style="margin:6px 0;">D. The heart has stopped.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A PPG pulse is a small ripple on a large, drifting level, and the drift dominates the plot's scale. <strong>A</strong> jumps to a conclusion before processing the data. <strong>C</strong> is not the issue; a higher rate shows the pulse better, not worse. <strong>D</strong> is not a serious engineering explanation.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Your protocol document says lines starting with # are comments. Mid-session, the firmware must report that the IMU has stopped responding. A teammate writes a parser from your document alone. What should the firmware print?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. IMU lost</li><li style="margin:6px 0;">B. # ERR imu not responding</li><li style="margin:6px 0;">C. 1520,50213,-1</li><li style="margin:6px 0;">D. ERROR,IMU,0</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> According to the document, only a # line is a comment, so the parser skips it and keeps going. <strong>A</strong> and <strong>D</strong> look like damaged data rows that the parser may reject or crash on. <strong>C</strong> disguises an error as a valid-looking step count.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> The firmware's stream needs 11,000 bits per second, but the UART is set to 9,600 baud. The sketch uses the non-blocking millis() pattern throughout. What happens?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing; non-blocking code is unaffected.</li><li style="margin:6px 0;">B. The output buffer fills and Serial.print() waits for space, so the loop stalls and the careful timing breaks.</li><li style="margin:6px 0;">C. The extra data is compressed automatically.</li><li style="margin:6px 0;">D. The baud rate adjusts itself.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> When more data is printed than the link can send, the print call must wait, which makes it a blocking call in disguise. <strong>A</strong> overlooks that printing itself can block. <strong>C</strong> and <strong>D</strong> do not happen.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="D4-connectivity-and-persistence.md">D4 — Connectivity and Persistence</a> you will send the same data over the network to a dashboard, keep working when the network disappears, and store settings that survive a power cycle.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Arduino. Using the Serial Plotter Tool (Arduino IDE 2: data format, delimiters and labels). https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-serial-plotter/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Wokwi. Configuring Your Project (wokwi.toml) (serial port forwarding with rfc2217ServerPort, and connecting with PySerial's serial\_for\_url). https://docs.wokwi.com/vscode/project-config</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Analog Devices. MAX30102 datasheet (ADC resolution 15–18 bits set by LED\_PW; FIFO data left-justified with the MSB in bit 17). https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
