<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 3 — Three Rough Decisions</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The architecture needs three decisions early, even if they are only rough. You will refine each one later in the course.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Where Does the Work Happen?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">For each job your product does, decide roughly where it runs: on the <strong>device</strong>, on a <strong>phone</strong>, or on a <strong>server</strong>. Then ask the question that matters most: what does the wearer see when the link between them drops?</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Work done on…</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Strengths</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">When the link drops</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Device only</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Works anywhere, no dependence on others</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Nothing changes</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Phone</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Big screen, easy graphs, more memory</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Watch keeps working; the history on the phone stops updating</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Server</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Data survives a lost phone; can be seen anywhere</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Watch and phone must buffer until the link returns, or data is lost</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The rule of thumb: <strong>anything the wearer needs at the moment belongs on the device.</strong> Heart rate on request, the time and the step count must still work in a basement lab with no signal. Only work that can wait, such as long-term history, should depend on a link.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">How Much Data?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Data volume decides whether a link is even practical, and it is easy to estimate. Here is FR-04, the semester trend, done two ways. The numbers are <strong>example values</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Option A: Send the raw optical signal and let the server work out heart rate.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Assumption:</strong> the sensor is read 100 times a second, and each reading takes 4 bytes.</div>

```text
One 30 s reading:   100 samples/s × 4 bytes × 30 s  = 12,000 bytes
Per day (5 readings): 12,000 × 5                     = 60,000 bytes  (60 kB)
Per semester (120 days): 60,000 × 120               = 7,200,000 bytes (7.2 MB)
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;font-weight:700;">Option B: Work out heart rate on the watch, and keep only the results.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Assumption:</strong> each result is 1 byte of heart rate plus a 4-byte timestamp. Steps are saved once an hour as 2 bytes plus a 4-byte timestamp.</div>

```text
Heart rate:  5 results × 5 bytes          =   25 bytes/day
Steps:      24 hours  × 6 bytes           =  144 bytes/day
Per day:                                    169 bytes
Per semester: 169 × 120                   = 20,280 bytes (about 20 kB)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> 7,200,000 ÷ 20,280 ≈ 355. Option A produces about 355 times more data for the same answer. More data means the radio stays on longer, and in A0 you saw how much battery life depends on what runs for long periods.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Now look back at the orphan. With Option B, a whole semester of history is about 20 kB. That changes the choice for FR-04: storing it on the watch itself (way out 2 in Part 2) becomes realistic, and a backend may not be needed at all for version 1. You will check the actual memory available when you choose parts.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Which Connection?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Choose the product's route to the outside world, and write down a one-line reason. For a wearable the realistic choices are:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Route</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Suits</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Watch out for</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>No connection</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Everything needed is on the device</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No history beyond what the watch stores</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Bluetooth Low Energy to a phone</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Frequent small updates; the phone relays to the internet</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">You must build, or depend on, a phone app</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>WiFi direct to the internet</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Occasional larger transfers, with no phone</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Higher power while connected; campus networks often need a browser login page that a watch cannot complete</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">You will choose protocols and payloads properly in the firmware module. For now, one line is enough, such as: "BLE to a phone, because history needs a big screen and the wearer always carries a phone."</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch chose WiFi, used once at first boot, and then off. The reason is simple: it only needs the time and the weather, and a single short connection costs almost nothing in the battery budget. The trade-off is that it depends on a WiFi network the watch can join without a login page, and it cannot send anything later without turning WiFi back on. For the hostel problem statement, with its semester history, that choice would need revisiting.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Draw your context diagram.</strong> Use your A0 spec. One box for your product, every external actor, every arrow labelled with what flows. Save it as an image in your design pack.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Break down your product.</strong> List your subsystems using the seven as a starting point. For each, write one sentence describing its job. Mark any you merged or added, and say why.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Allocate every requirement.</strong> Build the table: ID, owner, supporting subsystems, and a short note on how it is met. Then:</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">List every orphan and choose one of the three ways out for each.</li><li style="margin:6px 0;">List every subsystem that owns or supports nothing, and say whether a requirement is missing or the subsystem is unnecessary.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Make the three rough decisions.</strong> For each main job, write where it runs and what the wearer sees when the link drops. Estimate your daily and total data volume, showing each step. Choose a connection route in one line.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> save the context diagram, the subsystem list, the allocation table and your three rough decisions in your design pack as A1-architecture.md, with the diagram as an embedded image.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open A1-architecture.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The context diagram has exactly one box for your product. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every arrow in the context diagram is labelled with what flows. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every actor mentioned in your A0 spec appears in the context diagram. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every subsystem has a one-sentence job description. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every requirement ID from A0 appears in the allocation table. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Every requirement has exactly one owner, or is marked as an orphan. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. Every orphan has a chosen way out written next to it. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. Every subsystem appears in the allocation table at least once, or has a note explaining why not. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. Your data estimate shows bytes per day and total, with every step. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">10. Your connection route has a one-line reason. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A student's watch must "show weekly step totals as a bar chart". Their context diagram has no phone and no server, and their watch display is 128 × 64 pixels. What is the most useful thing the allocation table will reveal?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing, because step counting is owned by sensing.</li><li style="margin:6px 0;">B. Whether a small display can show the chart, and where a week of data is stored, which may reveal a missing owner.</li><li style="margin:6px 0;">C. That the requirement belongs to connectivity.</li><li style="margin:6px 0;">D. That the display must be replaced with a larger one.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Counting steps is only part of it. Storing a week of totals and drawing the chart are separate jobs that need owners, or they are orphans. <strong>A</strong> ignores the chart. <strong>C</strong> assumes a connection the diagram rules out. <strong>D</strong> fixes a problem not yet shown; a simple bar chart may fit.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A watch sends every heart-rate reading to a server, and the server works out the resting-heart-rate trend. The student loses WiFi for two days. With no buffering on the watch, what happens?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Nothing, because the server will fill the gap.</li><li style="margin:6px 0;">B. Two days of readings are lost from the trend, although the watch still shows live heart rate.</li><li style="margin:6px 0;">C. The watch stops showing heart rate.</li><li style="margin:6px 0;">D. The watch stores the readings automatically.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Live heart rate runs on the device and keeps working; history that depends on the link is lost without buffering. <strong>A</strong>: the server never received the data. <strong>C</strong> would need heart rate calculated on the server. <strong>D</strong>: nothing is stored automatically; buffering is a design decision someone must own.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> Option A sends 60 kB a day of raw signal; Option B sends 169 bytes a day of results. Apart from storage, why does the difference matter for a battery-powered watch?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. It does not, because WiFi is fast.</li><li style="margin:6px 0;">B. More data keeps the radio on for longer, and the radio is one of the most power-hungry parts.</li><li style="margin:6px 0;">C. Servers charge per byte.</li><li style="margin:6px 0;">D. The display cannot show 60 kB.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Radio-on time costs battery, so more bytes means a shorter battery life. <strong>A</strong> ignores energy; "fast" still has a cost for every second the radio is on. <strong>C</strong> may be true of some services, but it is not the main issue for the device. <strong>D</strong> confuses sending data with displaying it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A team writes: "NFR-07 Thickness ≤ 16 mm — Owner: Enclosure." The circuit board with its modules is already 14.044 mm tall. What should the team conclude?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. The enclosure designer must make walls under 1 mm thick.</li><li style="margin:6px 0;">B. Ownership is correct, but the requirement is really spent by the board stack, so sensing, processing, local UI and power must be listed as supporting and may need to change.</li><li style="margin:6px 0;">C. Thickness should be owned by processing.</li><li style="margin:6px 0;">D. The requirement is met, because 14.044 is less than 16.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Thickness is a budget requirement. The enclosure manages it, but the board stack spends most of it. Listing the supporting subsystems shows where the fix really lies. <strong>A</strong> puts an impossible load on one subsystem. <strong>C</strong> moves ownership without solving anything. <strong>D</strong> forgets that the case adds a lid, a base and a sensor window on top of the board.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> Which is the best one-line reason for a connection choice?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. "WiFi, because the ESP32 has it."</li><li style="margin:6px 0;">B. "Bluetooth, because it is modern."</li><li style="margin:6px 0;">C. "BLE to a phone, because the wearer always carries one and history needs a large screen, while BLE keeps the watch's radio power low."</li><li style="margin:6px 0;">D. "Both WiFi and Bluetooth, to be safe."</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C</strong> ties the choice to the user, a requirement and a constraint. <strong>A</strong> confuses what is available with what is needed. <strong>B</strong> gives no engineering reason. <strong>D</strong> doubles the work and the power use without a requirement that needs both.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="A2-operating-modes-and-decisions.md">A2 — Operating Modes and Decisions</a> you will decide how the whole system behaves over time: what it does while starting up, measuring, sleeping and failing, and how to record the big decisions you have just made so they survive.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. C4 model. System context diagram (a system shown as a box in the centre, surrounded by its users and the other systems it interacts with). https://c4model.com/diagrams/system-context</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. draw.io. draw.io (free, open-source diagramming application). https://www.drawio.com/</div>
