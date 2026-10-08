<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">A2 — Operating Modes, Failure Behaviour and Decisions</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Deciding How the System Behaves Over Time, and Writing Down Why</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 1 — System Architecture <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a system state diagram, a failure mode table and two decision notes</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Watch Is Not Always Doing the Same Thing</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Your architecture from A1 shows what the system is made of. It does not show when each part is working. A watch spends most of the day asleep. It wakes for a few seconds when shaken, measures heart rate only when asked, and sometimes sits on a charger. Each of those situations draws a different current, shows something different on the screen, and can go wrong in a different way.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Now picture a student who takes the watch off halfway through a heart-rate reading. What should the screen say? The sensor is suddenly reading air. If nobody decided in advance, the firmware will do something, perhaps showing 212 bpm, perhaps freezing. Both are worse than a plain "no contact".</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit covers three things: listing the states your system can be in, deciding what happens when something fails, and writing down your big decisions so you can explain them later.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Draw</strong> a system state diagram with states, the events that move between them, and what the device does in each.</li><li style="margin:6px 0;">​<strong>Produce</strong> a failure mode table that says, for each likely failure, how it is detected and what the wearer sees.</li><li style="margin:6px 0;">​<strong>Choose</strong> between graceful degradation and a hard stop for each failure, and justify the choice.</li><li style="margin:6px 0;">​<strong>Decide</strong> where health data lives and who can read it.</li><li style="margin:6px 0;">​<strong>Write</strong> a short decision note: the choice, the options, why, and what it costs.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 had you test a finished project by unplugging sensors or WiFi. Here you decide that behaviour before building.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">States: What Mode Is the System In?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>state</strong> is a mode the system stays in until something happens: asleep, awake, measuring. An <strong>event</strong> is the something that happens: a button press, a timeout, a low battery. A <strong>transition</strong> is the move from one state to another, caused by an event.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>state diagram</strong> shows all three. Each state is a box. Each arrow is a transition, labelled with the event that causes it. Beside each state, write what the system does while in it: which parts are powered, and what the screen shows.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Most wearables need these states:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">State</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What the system does</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Boot</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Start up, check sensors, connect if needed</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Awake (normal)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Screen on, respond to buttons</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Measuring</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate sensor on, reading in progress</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Asleep</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Screen off, minimum power, waiting for a wake event</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Low battery</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Warn the wearer, switch off non-essential features</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Charging</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Show charge status; may run normally at the same time</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fault</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A part has stopped working; show what still works</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Some of these are not separate modes but <strong>overlays</strong> that apply on top of another state. Charging is a good example: the watch can be awake and charging. Draw overlays as a note, not as a box, or your diagram fills up with copies of every state.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: The Reference Watch's States</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">We will reverse-engineer esp\_watch's behaviour into a state diagram. Everything marked <strong>recorded</strong> comes from the author's description of the firmware. Everything marked <strong>proposed</strong> is a gap that the design has to fill.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>What is recorded:</strong> on first power-up the watch connects to WiFi once and fetches the time and weather, then keeps WiFi off. It has three screens, moved between with a "next" and a "previous" button. Heart rate is measured on request. The watch is <strong>always on</strong>: it has no sleep state.</div>

```text
                 power on
                    │
                    ▼
            ┌───────────────┐
            │     BOOT      │  connect WiFi once, fetch time + weather,
            └───────┬───────┘  then WiFi off                 (recorded)
                    │ done
                    ▼
            ┌───────────────┐   request HR    ┌───────────────┐
            │     AWAKE     │────────────────►│   MEASURING   │
            │ screen on,    │◄────────────────│ heart-rate    │
            │ 3 screens     │  result / abort │ sensor on     │
            └───────────────┘                 └───────────────┘
                                                      (recorded)

  Overlays (proposed):  battery low → LOW BATTERY
                        USB connected → CHARGING
                        sensor stops answering → FAULT
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Now walk the diagram and ask questions:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>What if WiFi fails at boot?</strong> The diagram has only one arrow out of BOOT, labelled "done". A failed connection needs its own arrow, and a decision: go to AWAKE with no time shown, or retry? Nothing is recorded, so this is a gap.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>What if the watch is taken off during MEASURING?</strong> The only way back is "result / abort". The design needs to say how an abort is detected (see the failure table below).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>What happens when nobody is using it?</strong> Nothing: the watch stays awake with the screen on, which costs battery all day. A sleep state, and something to wake it, is the obvious next addition. D2 teaches the sleep modes you would use.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Not every proposed overlay fits esp\_watch's hardware. The XIAO charges the cell on board and can run from the battery with USB connected, and the watch uses a protected cell that cuts itself off when flat. But the XIAO has no battery-measurement pin and esp\_watch adds none, so the firmware cannot see the battery level. A LOW BATTERY state would first need a divider on an ADC pin. Writing that down is exactly what the state diagram is for.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Failure Behaviour</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Things will go wrong. The questions are which things, how the system notices, and what the wearer sees.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">There are two broad responses. <strong>Graceful degradation</strong> keeps as much working as possible and says plainly what is not: "No heart-rate signal. Is the watch on your wrist?" A <strong>hard stop</strong> shuts a function down completely because continuing would be unsafe or misleading, such as refusing to run when the battery is dangerously low.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Choose graceful degradation by default. Choose a hard stop when carrying on could damage something, or would show a number the wearer might trust and act on.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>failure mode table</strong> records each likely failure. Here is a <strong>proposed</strong> table for esp\_watch. Only the display row describes recorded behaviour; the rest is not recorded.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Failure</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">How it is detected</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What the wearer sees</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Response</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Watch taken off mid-reading</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Heart-rate signal becomes too weak or erratic to give a result</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"No contact" instead of a number</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Degrade: abandon the reading</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery reaches cut-off</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Not detectable: esp\_watch has no battery measurement</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Screen goes dark with no warning</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Hard stop by the protected cell's own cut-off</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A sensor stops responding</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A read on the I²C bus fails or times out</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">"--" for that value; other screens still work</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Degrade: retry later</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No WiFi at first boot</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connection times out</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Time not set; a clear "no time" indicator</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Degrade: everything else still works</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Display stops updating</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Cannot be detected by writing to it</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Frozen or corrupted screen</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">See note below</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The last row is a real lesson from the reference watch.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">On esp\_watch's breadboard, a faulty heart-rate module corrupted the shared I²C bus. The display showed garbage, but the firmware reported nothing, because nothing is read back from a display (full story in B3 and D5). <strong>Judge bus health by a device you read from.</strong> So the display's failure is detected indirectly, through a sensor on the same bus.</div>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/breadboard/photo_9.jpeg" alt="esp_watch breadboard prototype, with the heart-rate module, motion sensor and display sharing one I²C bus" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch breadboard prototype, with the heart-rate module, motion sensor and display sharing one I²C bus</div></div>

<div style="text-align:center;margin:16px 0;"><img src="../reference-files/images/i2c-debug-output.png" alt="Serial output from the i2c_debug sketch, showing the bus scan and per-device read-failure counts" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Serial output from the i2c\_debug sketch, showing the bus scan and per-device read-failure counts</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Notice that every "how it is detected" entry needs something to exist in the design: a timeout on bus reads, a check on signal quality. The battery row shows the other side: esp\_watch has no battery-sense pin, so it cannot warn before cut-off. A failure you cannot detect is a failure you cannot handle, so this table also tells the hardware and firmware what they must provide.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Where Health Data Lives</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Heart rate is <strong>health data</strong>. Before any code exists, decide three things and write them down:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Where does it live?</strong> On the device only, on a phone, or on a server?</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Who can read it?</strong> Only the wearer, or anyone who picks up the watch, joins the network, or has access to the server?</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Does it leave the device at all?</strong> If so, over what, and is it protected on the way?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The safest data is data that never leaves the device. Every copy you send elsewhere is a copy you must protect. India's Digital Personal Data Protection Act, 2023 places duties on anyone who processes people's personal data, including taking reasonable security safeguards to prevent a data breach [1]. Your student project is not a commercial service, but designing as if it were is good practice, and essential if it ever becomes one.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Going by esp\_watch's intended behaviour, heart-rate readings stay on the watch. WiFi is used once, at first boot, to fetch the time and weather. That is a strong privacy position, and it comes as a side effect of keeping WiFi off. The cost is the one A1 exposed: no history leaves the device, so there is nowhere to see a semester's trend.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Writing Down Your Decisions</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">You have already made several big decisions: which connection to use, where data lives, what happens on failure. In three weeks you will not remember why, and when someone reviews your design pack they will ask.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A <strong>decision note</strong> records one decision in four short parts:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Part</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What it contains</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Decision</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What you chose, in one sentence</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Options considered</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The realistic alternatives, including the ones you rejected</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Why</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The reason this option won, tied to a requirement from A0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What it costs</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What becomes harder, and any follow-on work it creates</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">If you change your mind later, write a new note that says which one it replaces. Don't delete the old note: the reasoning is still useful.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: A Reconstructed Decision Note for the Reference Watch</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The author's actual reasons are not recorded, so this note is rebuilt from the watch's behaviour.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note</div><div>​<strong>Decision: use WiFi only once, at first boot.</strong></div><div>​<strong>Options considered.</strong> (1) WiFi always on: always fresh, but a large, constant battery cost. (2) Bluetooth to a phone app: low radio power, but a phone app to write. (3) WiFi once at first boot, then off.</div><div>​<strong>Why.</strong> The watch needs the time and the weather, and neither changes fast enough to need a constant connection. Battery life is dominated by what runs all day (A0), so option 3 is nearly free in battery terms and needs no app.</div><div>​<strong>What it costs.</strong> The time is never corrected after boot, the weather goes stale, and heart-rate data never leaves the watch. It also creates work: a decision on what to show if WiFi fails at boot (a gap in the state diagram), and a way to enter WiFi details without editing code.</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The "what it costs" part is the useful one. It turns one decision into a list of follow-on work, and its first item is exactly the missing arrow found in the state diagram.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Draw your state diagram.</strong> Start from the seven common states and remove any that do not apply. Label every arrow with its event. Beside each state, note what is powered and what the screen shows. Draw charging and similar conditions as overlays.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Build your failure mode table.</strong> Include at least these: the device removed mid-measurement, the battery at cut-off, a sensor not responding, the network unavailable. For each, fill in detection, what the user sees, and whether it degrades or stops. If you cannot say how something is detected, write down what the hardware or firmware must add.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Decide where health data lives.</strong> Answer the three questions in writing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Write two decision notes</strong> for the two biggest decisions in your design so far. One of them must be your connection choice from A1.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> save all four in your design pack as A2-behaviour-and-decisions.md.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open A2-behaviour-and-decisions.md and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Every arrow in the state diagram is labelled with an event. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every state has a note of what is powered and what the screen shows. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every state has at least one way out, except a deliberate final state. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. The failure table includes removal mid-measurement, battery cut-off, sensor failure and no network. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. Every failure has a detection method, or a note of what must be added to detect it. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Every failure is marked as degrade or stop. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. The health-data section answers where it lives, who can read it, and whether it leaves the device. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. There are two decision notes, each with the decision, at least two options, a reason and a cost. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">9. One note records the connection choice from A1. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A student's state diagram has AWAKE, ASLEEP and MEASURING, plus separate boxes called AWAKE+CHARGING, ASLEEP+CHARGING and MEASURING+CHARGING. What is the better design?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Keep all six boxes, because they are all real states.</li><li style="margin:6px 0;">B. Draw charging as an overlay that applies to any state, and keep three boxes.</li><li style="margin:6px 0;">C. Remove charging, because it is handled by hardware.</li><li style="margin:6px 0;">D. Make charging a state that the device must enter before sleeping.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Charging happens alongside other states, so it is an overlay. Copying every state doubles the diagram and invites missed transitions. <strong>A</strong> grows worse with each new overlay. <strong>C</strong> is wrong: firmware must still show charge status. <strong>D</strong> invents a restriction nobody asked for.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A watch shows "72 bpm" after being taken off mid-reading, because it averaged the last few values. Which response is correct?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Keep it, because 72 is a normal value.</li><li style="margin:6px 0;">B. Detect the loss of contact from the weak signal and show "no contact" instead of a number.</li><li style="margin:6px 0;">C. Shut the watch down.</li><li style="margin:6px 0;">D. Show the last good value with no warning.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> This is graceful degradation: the reading cannot be trusted, so the watch says so plainly and keeps working. <strong>A</strong> is the most dangerous option, because a normal-looking wrong number is believed. <strong>C</strong> is a hard stop for a problem that endangers nothing. <strong>D</strong> hides the failure from the wearer.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> On a shared I²C bus, a firmware engineer checks that every write to the display succeeds, and concludes the bus is healthy. Why is this not enough?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. It is enough, because the display is the busiest device on the bus.</li><li style="margin:6px 0;">B. Display writes are never read back, so a broken bus can look healthy. Check a device you read from.</li><li style="margin:6px 0;">C. It is enough if the bus runs at 100 kHz instead of 400 kHz.</li><li style="margin:6px 0;">D. It is enough, as long as the display shows something.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A write with no read-back confirms nothing, so a corrupted bus can look fine from the display side. Read a register from a sensor on the same bus. <strong>A</strong> and <strong>C</strong> do not change what the check can see. <strong>D</strong> fails because the screen can show corrupted output without the firmware knowing.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> A student's decision note reads: "Decision: use BLE." Nothing else is written. Six weeks later they wonder whether to switch to WiFi. Which missing part would help most?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A number for the note</li><li style="margin:6px 0;">B. The "why" and "what it costs", which say why BLE was chosen and what switching would give up</li><li style="margin:6px 0;">C. The date</li><li style="margin:6px 0;">D. The student's name</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Without the reason and the cost, nobody can tell whether the original reasons still hold. <strong>A</strong>, <strong>C</strong> and <strong>D</strong> help with tracking, but none explains the decision, which is the whole point of the note.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> Four students decide where their watch's heart-rate readings go. Which design is weakest on privacy?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Readings stay on the watch and are shown only on its screen.</li><li style="margin:6px 0;">B. Readings go to the wearer's phone over an encrypted Bluetooth link.</li><li style="margin:6px 0;">C. Readings go to a server over an encrypted link, and the website needs the wearer's login.</li><li style="margin:6px 0;">D. Readings go to a server without encryption, and anyone with the web address can view them.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> The data travels unprotected and anyone with the address can read it, which fails both "protected on the way" and "who can read it". <strong>A</strong> is the strongest: the data never leaves the device. <strong>B</strong> keeps the data close and protected. <strong>C</strong> sends it further, but protects it in transit and controls who can see it.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This completes your System Architecture Document: specification, context diagram, subsystem breakdown, allocation table, state diagram, failure table and decision notes. In <a href="../02-sensing-and-hardware-architecture/B0-choosing-sensors.md">B0 — Choosing the Right Sensor</a> you will decide what your product must sense, and with which sensor, before any circuit is drawn.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Government of India, Ministry of Law and Justice. The Digital Personal Data Protection Act, 2023 (No. 22 of 2023), published by MeitY (including the obligation to take reasonable security safeguards against personal data breaches). https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
