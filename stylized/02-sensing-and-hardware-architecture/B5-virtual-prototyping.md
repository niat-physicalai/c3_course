<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">B5 — Virtual Prototyping</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Testing the Circuit Before It Exists</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 2 — Sensing and Hardware Architecture <strong>Time:</strong> ~1.5 hours · <strong>You will produce:</strong> a working Wokwi project link and a Falstad circuit link</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Your Bench Is a Browser</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In Part 1 you checked a circuit by building it on a breadboard. Here nothing gets built, so you check your B3 calculations in a <strong>simulator</strong> instead: change a resistor and watch the edge slow down, run your firmware and read the bus traffic it produces. (esp\_watch itself was tested on a real breadboard before its schematic was drawn; a simulator is the next best thing when you don't have the parts yet.)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Simulators have blind spots, and esp\_watch's worst breadboard bug sits in one. This unit uses two simulators, each for what it does well, and shows where each one stops telling the truth.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Simulate</strong> pull-up rise times and bus voltage levels in Falstad, and compare them with your B3 calculations.</li><li style="margin:6px 0;">​<strong>Build</strong> a Wokwi project that runs real firmware against your pin map, including a mock for a sensor the simulator does not have.</li><li style="margin:6px 0;">​<strong>Read</strong> an I²C trace: start, address, acknowledge, data and stop.</li><li style="margin:6px 0;">​<strong>Diagnose</strong> a failed transaction from its trace.</li><li style="margin:6px 0;">​<strong>Explain</strong> what each simulator cannot show you, and which real measurement fills the gap.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Analog Behaviour in Falstad</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Two Simulators, Two Questions</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Question</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Tool</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Do the voltages and edges look right?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Falstad</strong> Circuit Simulator [1]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shows voltages and currents continuously; you can see an edge rise</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Does my firmware work with my pin map and parts?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Wokwi</strong> [2]</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Runs real Arduino code on a simulated ESP32-C3 with simulated sensors and displays</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Falstad treats every wire as a voltage that changes over time. Wokwi treats most signals as simply HIGH or LOW. (For more rigorous analog work, engineers use <strong>LTspice</strong>; Falstad is enough for this course.)</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Pull-up Rise Time</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In B3 you calculated the range of legal pull-up values. Now watch why the upper limit exists.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">When no device pulls an I²C line low, the pull-up resistor charges the bus's capacitance back up to 3.3 V. That takes time, because a resistor charging a capacitor produces a curve, not a step. The I²C specification measures the <strong>rise time</strong> from 30% to 70% of the supply voltage, and for a resistor charging a capacitor that works out to 0.8473 × R × C [3].</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: Three Pull-up Values</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Assumption:</strong> bus capacitance 50 pF, as in B3.</div>

```text
t_r = 0.8473 × R × C

4.7 kΩ:   0.8473 × 4,700  × 50 pF = 199 ns
10 kΩ:    0.8473 × 10,000 × 50 pF = 424 ns
1.57 kΩ:  0.8473 × 1,570  × 50 pF =  67 ns   (three 4.7 kΩ pairs in parallel)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The fast-mode (400 kHz) limit is 300 ns, and standard mode (100 kHz) allows 1,000 ns [3].</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> 4.7 kΩ passes at 400 kHz with margin. 10 kΩ breaks the 300 ns limit at 400 kHz, though the line still reaches most of the way up before the next bit, so it may seem to work on the bench, with less margin for noise. It passes easily at 100 kHz. 1.57 kΩ gives very fast edges, but, as B3 showed, it asks every device to sink more current. The simulator will show you all three curves side by side.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Watch the edge rise.</div><div>Open Falstad in your browser [1]. Build three identical circuits side by side. In each, an N-channel MOSFET connects the line to ground and acts as the open-drain device, with its gate driven by a 0–3.3 V square-wave source. Add a pull-up resistor from the line to a 3.3 V source, and a 50 pF capacitor from the line to ground. Use 4.7 kΩ, 10 kΩ and 1.57 kΩ for the three pull-ups. Add a scope to each line.</div><div>1. <strong>Predict.</strong> Which of the three will look most like a clean square wave at 400 kHz?</div><div>2. <strong>Do.</strong> Set the source to 400 kHz. Compare the rising edges on the scopes. Then change it to 100 kHz.</div><div>3. <strong>Explain.</strong> On each scope, estimate the time from 30% to 70% of 3.3 V (0.99 V to 2.31 V). Which pull-ups break the 300 ns limit? Do your times match the numbers above?</div><div>​<strong>Extra challenge:</strong> Double the capacitance to 100 pF. Which pull-ups still pass at 400 kHz?</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">When the Bus Sits at the Wrong Voltage</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On esp\_watch's breadboard prototype, the green heart-rate module tied its I²C lines to its own 1.8 V rail. With it on the shared bus, the idle bus voltage was measured at <strong>1.82 V</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Why does 1.82 V break everything? Look at what the ESP32-C3 accepts as a logic level. Its datasheet sets the <strong>input-high threshold</strong> at 0.75 × VDD and the <strong>input-low threshold</strong> at 0.25 × VDD [4]:</div>

```text
                3.3 V ┬
                      │  HIGH: guaranteed read as 1
  0.75 × 3.3 = 2.475 V ┼─────────────────────────────
                      │
                      │  UNDEFINED: may read as 0 or 1
       measured 1.82 V ┼── ◄ esp_watch bus with the green module
                      │
  0.25 × 3.3 = 0.825 V ┼─────────────────────────────
                      │  LOW: guaranteed read as 0
                  0 V ┴
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The idle bus sat in the <strong>undefined</strong> band. Sometimes a receiver read an idle line as HIGH, sometimes as LOW. That is exactly the kind of fault that produces 80% failures on one device and occasional success on another, rather than a clean "not working".</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Teaching model.</div><div>The Try-it below treats the green module as a second pull-up to 1.8 V, fighting the 3.3 V pull-up. The real module may also clamp the line through protection diodes. The model is enough to show why the bus ends up between the two rails.</div></div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Two pull-ups, two rails.</div><div>In Falstad, draw one line with a 4.7 kΩ pull-up to 3.3 V and a second resistor, R\_mod, pulling the same line to a 1.8 V source. Add a voltmeter on the line.</div><div>1. <strong>Predict.</strong> With R\_mod = 4.7 kΩ, where will the line sit?</div><div>2. <strong>Do.</strong> Try R\_mod = 4.7 kΩ, 2.2 kΩ and 1 kΩ, and read the voltage each time.</div><div>3. <strong>Explain.</strong> For which values does the line fall below 2.475 V, into the undefined band?</div><div>​<strong>Extra challenge:</strong> Show by calculation that the line drops below 2.475 V whenever R\_mod is less than about 3.85 kΩ.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The fixes for a mismatched module are, in order of preference: choose a module whose bus sits at your voltage (esp\_watch's black module), change the module's pull-up voltage if it has a jumper for it, or add a <strong>bidirectional level shifter</strong> between the two voltage domains.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Battery Divider's Settling Time</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch doesn't measure its battery: the XIAO board handles charging and protection, and the watch uses a protected LiPo cell. Many battery products do show a battery level, though, and they measure it with a divider.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Example values:</strong> a 1 MΩ / 1 MΩ divider halves the cell voltage so the ADC can read it, and a 100 nF capacitor at the ADC pin gives the ADC a steady voltage to sample. The capacitor has a side effect you can see in Falstad: the voltage at the pin cannot change instantly. The capacitor charges through the divider's effective resistance of 500 kΩ (the two resistors in parallel):</div>

```text
Time constant  τ = R × C = 500 kΩ × 100 nF = 0.05 s = 50 ms
Settled (about 99%) after 5τ = 250 ms
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">So a reading taken in the first 250 ms after power-up will be low. The firmware should wait before trusting the first battery reading. In Falstad, build the divider and capacitor, switch the supply on, and watch the pin voltage curve up.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Supply Dips Under Load</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A battery is not a perfect voltage source. It has <strong>internal resistance</strong>, so its voltage drops when current is drawn. A regulator needs its input to stay a little above its output, the <strong>dropout voltage</strong>, to keep regulating.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Example values:</strong> a small cell with 0.5 Ω internal resistance, a radio burst drawing a 300 mA peak, and a regulator needing 0.2 V of dropout.</div>

```text
Voltage lost inside the cell: 300 mA × 0.5 Ω = 0.15 V
Input needed to hold 3.3 V:   3.3 V + 0.2 V  = 3.5 V
Cell voltage needed at rest:  3.5 V + 0.15 V = 3.65 V
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Below about 3.65 V at rest, a radio burst pulls the regulator's input too low and the 3.3 V rail dips. If it dips far enough, the <strong>brownout detector</strong> resets the microcontroller (D5 covers this). The lower the cell, the more a current burst hurts.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Firmware and Parts in Wokwi</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Building the Virtual Watch</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Wokwi simulates the ESP32-C3, the SSD1306 display, the MPU-6050 motion sensor and pushbuttons [5], including a XIAO ESP32-C3 board [2]. It runs real Arduino code, so the sketch you test here is the sketch you would flash.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A Wokwi project has three files:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">sketch.ino, the firmware</li><li style="margin:6px 0;">diagram.json, the parts and wires</li><li style="margin:6px 0;">libraries.txt, the Arduino libraries to install</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The complete files for this unit are in <a href="../assets/code/B5-wokwi-watch-sim/">assets/code/B5-wokwi-watch-sim/</a>. To use them, create a new ESP32 project on wokwi.com, then replace the contents of each file with the provided version. If Wokwi reports an unknown pin name, hover over that pin in the diagram to see its exact name [6].</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The wiring matches esp\_watch's pin map: one shared I²C bus and two buttons, with no interrupt or battery pins.</div>

```text
XIAO ESP32-C3 (Wokwi)            Parts
  D4 SDA ───────────────────────  SSD1306 SDA, MPU-6050 SDA, logic analyser D0
  D5 SCL ───────────────────────  SSD1306 SCL, MPU-6050 SCL, logic analyser D1
                                  MPU-6050 AD0 tied to GND → 0x68
  D10    ◄──────────────────────  "next" button to GND
  D9     ◄──────────────────────  "previous" button to GND
  3V3 / GND ────────────────────  all parts
```

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Mock Sensor</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Wokwi has no MAX30102 [5]. Rather than leave the heart-rate code untested, the sketch uses a <strong>mock</strong>: a small class with the same job as the real driver, returning made-up but realistic values.</div>

```cpp
// Wokwi has no MAX30102. This mock stands in for it, returning a heart
// rate that drifts slowly between about 66 and 78 bpm. The rest of the
// program cannot tell the difference, so it can all be tested now.
class MockHeartRate {
public:
  bool begin() { return true; }
  int readBpm() {
    float t = millis() / 1000.0f;
    return 72 + (int)(6.0f * sinf(t / 10.0f));
  }
};
MockHeartRate heart;
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The rest of the program only ever calls heart.begin() and heart.readBpm(). When the real sensor arrives, a real class with the same two functions replaces the mock, and nothing else changes. D0 builds on this idea.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The full sketch is about 140 lines and compiles for the XIAO ESP32-C3. Its main jobs:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">scan the I²C bus at start-up and print every address found</li><li style="margin:6px 0;">show two screens (motion and heart rate), switched by the two buttons</li><li style="margin:6px 0;">time every screen update and print it</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Two lines are worth noticing now. display.setTextWrap(false) is there because esp\_watch's own firmware showed garbled text during screen animations until wrapping was turned off. I2C\_CLOCK\_HZ sets the bus speed, so you can compare against the timing measured on the reference watch. It is passed to the display library as well, because that library otherwise switches the bus back to 100 kHz after every frame.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Compare with the real watch.</div><div>Run the Wokwi project.</div><div>1. <strong>Predict.</strong> Which addresses will the bus scan find? How long will one screen update take at 400 kHz, based on B2?</div><div>2. <strong>Do.</strong> Read the scan and the "sent in" times in the serial monitor. Then change I2C\_CLOCK\_HZ to 100000 and run again.</div><div>3. <strong>Explain.</strong> The scan should find 0x3C and 0x68, but not 0x57, because the heart-rate sensor is a mock with no bus address. Compare your update times with B2's prediction (23 ms and 92 ms) and with the reference watch's measurements (about 25 ms and 90 ms). If the simulator's times differ, what does that tell you about what Wokwi models?</div><div>​<strong>Extra challenge:</strong> Change the redraw so the display is sent only when the heart-rate number actually changes. How many updates per minute does that save?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Reading the Bus</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What an I²C Transaction Looks Like</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The logic analyser in the Wokwi project records SDA and SCL while the simulation runs. When you stop the simulation, it saves a .vcd file [7]. Open it in <strong>PulseView</strong>, a free logic-analyser program [8], using Import Value Change Dump data, with a downsampling factor of about 50 for I²C [9]. Then add PulseView's I²C decoder to label each byte.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Here is one complete read of the motion sensor, annotated. The library's imu.getEvent() reads <strong>14 bytes</strong> in one go, starting at register 0x3B: six of acceleration, two of temperature and six of rotation.</div>

```text
     START  address 0x68 + W   ACK  register 0x3B   ACK
SDA  ‾‾\_ [1101000][0]         [0]  [00111011]      [0]
SCL  ‾‾‾\_/‾\_/‾\_ ...                                 

     REPEATED START  address 0x68 + R   ACK  data × 14 (each followed by ACK, last by NACK)  STOP
SDA  ‾\_             [1101000][1]       [0]  [xxxxxxxx][0] ... [xxxxxxxx][1]                _/‾
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Reading it left to right:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>START</strong>: SDA falls while SCL is high. Every device on the bus starts listening.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Address + write bit</strong>: 0x68 in seven bits, then 0 meaning "I want to write".</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>ACK</strong>: the motion sensor pulls SDA low for one clock: "that's me".</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Register number</strong>: 0x3B, the first acceleration register.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Repeated START</strong>, then the address again with the read bit (1).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. <strong>Fourteen data bytes</strong> from the sensor. The controller acknowledges each one, except the last, which gets a <strong>NACK</strong> meaning "that's enough".</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. <strong>STOP</strong>: SDA rises while SCL is high.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: How Long Does One Sensor Read Take?</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Count the bytes: address (1), register (1), address again (1), data (14) = 17 bytes.</div>

```text
17 bytes × 9 clocks = 153 clocks
At 400 kHz: 153 ÷ 400,000 ≈ 0.4 ms
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> Compare with a full display update: about 25 ms. One screen update takes as long as about 65 sensor reads. The trace confirms B2's conclusion from the other direction: on a shared bus, the display is the heavy user.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">When the Trace Shows a Failure</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Wokwi's bus has no electrical faults, so your traces fail only for logic errors such as a wrong address. Real buses fail in three common patterns:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What the trace shows</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it means</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Likely cause</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Address sent, then <strong>NACK</strong> instead of ACK</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No device answered at that address</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Wrong address, device unpowered, or an address pin left floating</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Lines never return fully high between bytes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The idle level is too low</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A module pulling the bus to another voltage, or too little pull-up</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Rising edges slow and rounded, bits misread</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Rise time too long</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pull-up too large or bus capacitance too high for the speed</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch hit the first two on the bench, found with the author's i2c\_debug sketch: a floating AD0 pin (see B1) and the 1.82 V bus above. Neither would appear in Wokwi, whose bus has no voltage levels, no floating pins and no capacitance.</div>

<div style="text-align:center;margin:16px 0;"><img src="../reference-files/images/i2c-debug-output.png" alt="Output of the i2c_debug sketch on the esp_watch breadboard: bus scan, voltage check and read-failure counts per device" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Output of the i2c\_debug sketch on the esp\_watch breadboard: bus scan, voltage check and read-failure counts per device</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Each Simulator Cannot Tell You</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;"></th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Falstad</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Wokwi</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shows voltage levels and edge shapes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No: signals are HIGH or LOW</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Runs your firmware</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Yes</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Models your exact modules</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Only if you draw their circuits</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Only parts in its library; no MAX30102</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shows a floating address pin</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Only if you model it</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Shows bus timing</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">As analog waveforms</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Protocol timing, idealised</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's two worst breadboard faults, a floating address pin and a module on the wrong voltage, fall between the two tools. Falstad shows the voltage fault only if you already suspect it and draw it; Wokwi shows neither. So next to each simulation result, write down <strong>what the simulation did not include</strong>, so the funded build knows what to check first.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Simulate your pull-ups in Falstad.</strong> Build your bus with your chosen pull-up and estimated capacitance. Check the rise time at your bus speed. Save the circuit as a link.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Check your voltage levels.</strong> For every module on your bus, model its pull-up voltage in Falstad and confirm the idle level sits above the microcontroller's input-high threshold.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Build your Wokwi project.</strong> Start from the provided files and adapt the pin map, parts and addresses to your own design. Add a mock for every part Wokwi lacks. Confirm the bus scan finds exactly the addresses in your interface table.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Capture and decode one transaction.</strong> Record SDA and SCL, open the file in PulseView, decode it, and annotate one complete read.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Write the gaps.</strong> List what your simulations did not include: modules not modelled, voltages not checked, parts mocked.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> add your Wokwi project link, your Falstad link, one annotated trace, and your list of gaps to your design pack as B5-virtual-prototype.md.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open B5-virtual-prototype.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The Falstad link opens a circuit with your actual pull-up value and a stated bus capacitance. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. The simulated rise time is recorded and compared with the limit for your bus speed. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every module's bus voltage has been checked against the microcontroller's input-high threshold. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. The Wokwi link opens a project that runs without errors. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The Wokwi pin map matches your B3 pin allocation exactly. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. The bus scan output is recorded and matches your interface table. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Every part the simulator lacks has a mock with the same functions as the real driver. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. One decoded transaction is annotated from START to STOP. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. The list of gaps names every module, voltage and part the simulations did not model. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A bus with 80 pF of capacitance runs at 400 kHz. Using t\_r = 0.8473 × R × C and a limit of 300 ns, which is the largest pull-up that passes?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. 10 kΩ</li><li style="margin:6px 0;">B. 4.7 kΩ</li><li style="margin:6px 0;">C. 3.9 kΩ</li><li style="margin:6px 0;">D. 2.2 kΩ</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> R\_max = 300 ns ÷ (0.8473 × 80 pF) ≈ 4,426 Ω, so 3.9 kΩ passes with a little margin and is the largest option that does. <strong>B</strong>, 4.7 kΩ, gives 0.8473 × 4,700 × 80 pF ≈ 319 ns, just over the limit. <strong>A</strong> gives about 678 ns, more than double the limit. <strong>D</strong> passes easily, but it is not the largest that passes, and it asks devices to sink more current than they need to.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> An ESP32-C3 at 3.3 V reads an I²C line that idles at 1.9 V. What will happen?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The line reads reliably as HIGH.</li><li style="margin:6px 0;">B. The line reads reliably as LOW.</li><li style="margin:6px 0;">C. The level is in the undefined band between 0.825 V and 2.475 V, so reads are unreliable.</li><li style="margin:6px 0;">D. The ESP32-C3 is damaged.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> 1.9 V is below the input-high threshold (0.75 × 3.3 = 2.475 V) and above the input-low threshold (0.25 × 3.3 = 0.825 V), so neither reading is guaranteed. <strong>A</strong> and <strong>B</strong> each assume a guarantee that does not exist in that band. <strong>D</strong> is wrong; 1.9 V is well within the pin's allowed range.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A decoded trace shows START, Address write: 68, NACK, STOP. What is the most likely explanation?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The register number was wrong.</li><li style="margin:6px 0;">B. No device acknowledged address 0x68: it is missing, unpowered, or its address pin is not set as expected.</li><li style="margin:6px 0;">C. The data was read successfully.</li><li style="margin:6px 0;">D. The pull-ups are too small.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A NACK straight after the address means nobody answered to that address. On the reference watch, a floating AD0 pin produced exactly this, intermittently. <strong>A</strong> cannot be the cause, because the register number is never sent after a NACK. <strong>C</strong> is wrong, since no data bytes appear. <strong>D</strong> makes it harder for devices to pull the line low, so bits get misread; it does not cause a clean NACK straight after the address.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Which reference-watch fault could a Wokwi simulation have revealed?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The green module clamping the bus to 1.82 V</li><li style="margin:6px 0;">B. A floating AD0 pin making the sensor come and go</li><li style="margin:6px 0;">C. Garbled text caused by text wrapping during screen animations</li><li style="margin:6px 0;">D. Three modules' pull-ups in parallel</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Text wrapping is firmware behaviour, and Wokwi runs the firmware and draws the display, so the garbled text would appear on the simulated screen. <strong>A</strong>, <strong>B</strong> and <strong>D</strong> are all analog or electrical effects: voltage levels, floating inputs and resistance. Wokwi's digital model does not include any of them.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A product measures its battery through a 1 MΩ / 1 MΩ divider with a 100 nF capacitor. Why should its firmware wait before trusting the first battery reading after power-up?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The ADC needs to warm up.</li><li style="margin:6px 0;">B. The capacitor charges through about 500 kΩ with a time constant of 50 ms, so the pin voltage takes around 250 ms to settle.</li><li style="margin:6px 0;">C. The battery voltage changes at power-up.</li><li style="margin:6px 0;">D. Readings are always wrong for the first second.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> τ = 500 kΩ × 100 nF = 50 ms, and about 5τ is needed to settle, so early readings are low. <strong>A</strong> is not the mechanism here. <strong>C</strong> may be slightly true under load, but it is not why the reading is low. <strong>D</strong> is an arbitrary rule with no reasoning behind it.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">"Passed in Wokwi" means the logic is right, not that the voltages are: a simulation result is only as complete as its list of gaps.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="../03-form-schematic-and-pcb/C0-form-factor-and-concept.md">C0 — Form Factor and Concept</a> you will decide the product's shape and which face each part sits on, before the circuit becomes a board.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Paul Falstad. Circuit Simulator Applet. https://www.falstad.com/circuit/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Wokwi. ESP32 Simulation (supported boards including XIAO ESP32-C3; I²C "Master only"). https://docs.wokwi.com/guides/esp32</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. NXP Semiconductors. UM10204: I²C-bus specification and user manual (rise-time limits and the R\_p(max) = t\_r / (0.8473 × C\_b) relation). https://www.nxp.com/docs/en/user-guide/UM10204.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Espressif Systems. ESP32-C3 Series Datasheet (DC characteristics: V\_IH min 0.75 × VDD, V\_IL max 0.25 × VDD). https://www.espressif.com/sites/default/files/documentation/esp32-c3\_datasheet\_en.pdf</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Wokwi. Supported Hardware (MPU6050, SSD1306, pushbutton; no MAX30102). https://docs.wokwi.com/getting-started/supported-hardware</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Wokwi. diagram.json File Format (connection syntax partId:pinName; hover over a pin to see its name). https://docs.wokwi.com/diagram-format</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Wokwi. wokwi-logic-analyzer Reference (8 channels, VCD recording saved when the simulation stops). https://docs.wokwi.com/parts/wokwi-logic-analyzer</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. sigrok. PulseView (logic analyser, oscilloscope and MSO GUI for sigrok). https://sigrok.org/wiki/PulseView</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. Wokwi. Logic Analyzer Guide (importing VCD into PulseView; downsampling factor 50 for I²C). https://docs.wokwi.com/guides/logic-analyzer</div>
