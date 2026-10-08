<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">D4 — Connectivity and Persistence: Network, Dashboard and Settings That Survive</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">A Device That Keeps Working When the Network Does Not</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 4 — Firmware <strong>Time:</strong> ~1 hour · <strong>You will produce:</strong> a device publishing to a dashboard, and configuration that survives a power cycle</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Hostel WiFi Will Go Down</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1's WiFi examples connected in setup() and published in loop(). On a desk with a good router, that works. Now picture the same code on a student's wrist. The hostel WiFi drops at 11 pm. The student walks from the library to the mess, out of range for ten minutes. The router restarts after a power cut. Each time, a simple sketch either freezes in its wait-for-WiFi loop, loses every reading taken while offline, or never reconnects until someone presses reset.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">And the WiFi password is typed into the source code. To use the watch on a different network, someone has to edit the firmware and flash it again.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Implement</strong> a non-blocking WiFi and MQTT connection with reconnection and exponential backoff.</li><li style="margin:6px 0;">​<strong>Write</strong> a payload contract, and choose between HTTP POST and MQTT publish for your product.</li><li style="margin:6px 0;">​<strong>Specify</strong> what a device dashboard should show: live value, history, status and last-seen time.</li><li style="margin:6px 0;">​<strong>Store</strong> credentials and calibration in non-volatile storage, with a factory reset.</li></ul>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Part 1 Already Covered</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 covered WiFi, HTTP, MQTT, JSON and dashboards. This unit makes them survive real conditions.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 1 — A Connection That Never Blocks</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Connecting as a State Machine</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The simple approach waits:</div>

```cpp
// BLOCKING: nothing else runs until WiFi connects, which may be never.
WiFi.begin(ssid, pass);
while (WiFi.status() != WL_CONNECTED) {
  delay(500);
}
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The non-blocking approach treats the network as a <strong>state machine</strong>, exactly like the device states in D1 and D2. It starts a connection, then checks on it each pass:</div>

```text
        ┌──────────┐  retry time reached   ┌──────────────────┐
        │   IDLE   │──────────────────────►│ WIFI CONNECTING  │
        └──────────┘                       │ (check status    │
            ▲  ▲                           │  each pass)      │
            │  │ timeout (15 s):           └───┬──────────────┘
            │  └── schedule retry ◄────────────┤ connected
            │                                  ▼
            │  MQTT connect failed:     ┌──────────────────┐
            ├── schedule retry ◄────────│ WIFI UP          │
            │                           │ (connect broker) │
            │                           └───┬──────────────┘
            │                               │ connected
            │  WiFi or broker lost:         ▼
            └── schedule retry ◄────  ┌──────────────────┐
                                      │ ONLINE           │
                                      │ publish          │
                                      └──────────────────┘
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The complete sketch is in <a href="../assets/code/D4-connected-watch/">assets/code/D4-connected-watch/</a>. It runs in Wokwi, whose simulated ESP32 joins a virtual access point called Wokwi-GUEST with no password [1], and it compiles for the XIAO ESP32-C3. Here is its network state machine:</div>

```cpp
void serviceNetwork(unsigned long now) {
  switch (netState) {
    case Net::Idle:
      if ((long)(now - retryAt) >= 0) {
        Serial.printf("# WiFi: connecting to %s\n", ssid.c_str());
        if (ssid == "Wokwi-GUEST") WiFi.begin(ssid.c_str(), pass.c_str(), 6);
        else WiFi.begin(ssid.c_str(), pass.c_str());
        netState = Net::WifiConnecting;
        netSince = now;
      }
      break;
    case Net::WifiConnecting:                  // check, never wait
      if (WiFi.status() == WL_CONNECTED) { netState = Net::WifiUp; }
      else if (now - netSince >= WIFI_TIMEOUT_MS) { WiFi.disconnect(); scheduleRetry(now, "WiFi timeout"); }
      break;
    case Net::WifiUp:
      // Note: connect() blocks while the TCP connection opens (normally well
      // under a second). Backoff keeps these attempts rare when the broker is down.
      if (mqtt.connect(deviceId.c_str(), topicStatus.c_str(), 1, true, "offline")) {
        mqtt.publish(topicStatus.c_str(), "online", true);
        Serial.println("# MQTT: online");
        backoff = BACKOFF_MIN_MS;
        netState = Net::Online;
      } else {
        scheduleRetry(now, "MQTT connect failed");
      }
      break;
    // ... ONLINE: see Part 2
  }
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">One exception: mqtt.connect() waits while it opens the connection to the broker. Backoff limits this to one short wait a minute when the broker is down.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Exponential Backoff</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">When a connection fails, retrying immediately is the worst option. If the router has just rebooted, a hundred devices hammering it at once keep it busy. If the broker is down for an hour, retrying every pass wastes battery for an hour.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Exponential backoff</strong> doubles the wait after each failure, up to a limit, and resets when a connection succeeds:</div>

```text
Attempt:  1     2     3     4      5      6      7      8 ...
Wait:     1 s   2 s   4 s   8 s    16 s   32 s   60 s   60 s (capped)
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The sketch also adds a little <strong>jitter</strong>, a random extra of up to 20%, so that many devices that lost the network at the same moment do not all retry at the same moment:</div>

```cpp
void scheduleRetry(unsigned long now, const char *why) {
  unsigned long jitter = random(0, backoff / 5 + 1);
  retryAt = now + backoff + jitter;
  Serial.printf("# %s; retry in %lu ms\n", why, backoff + jitter);
  backoff = min(backoff * 2, BACKOFF_MAX_MS);
  netState = Net::Idle;
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Notice the # at the start of each debug message. It follows the serial format rule from D3, so these messages never corrupt a data log.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Worked Example: What Does an Hour Offline Cost?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Assumption:</strong> each failed attempt costs 15 s of WiFi searching, the timeout, at about 100 mA (esp\_watch's modelled WiFi burst figure, a model rather than a measurement).</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 1: Retry every 1 s, no backoff.</strong> Each attempt is 15 s of searching plus a 1 s wait, so the radio is searching about 94% of the time.</div>

```text
3,600 s × (15 ÷ 16) = 3,375 s searching
3,375 s × 100 mA ÷ 3,600 = 93.8 mAh
```

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">​<strong>Step 2: Exponential backoff, capped at 60 s.</strong> After the first few minutes, each cycle is 15 s searching plus about 60 s waiting.</div>

```text
Searching fraction ≈ 15 ÷ 75 = 20%
3,600 s × 20% = 720 s searching
720 s × 100 mA ÷ 3,600 = 20 mAh
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Check.</strong> An hour without a network costs about 94 mAh with naive retries, more than an entire day's budget from A0's worked example, and about 20 mAh with backoff. A longer cap cuts it further. For a watch that only needs to sync occasionally, a cap of several minutes is reasonable, and that choice belongs in your A2 failure table.</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Watch it recover.</div><div>Run the D4 project in Wokwi.</div><div>1. <strong>Predict.</strong> What will the serial monitor show if WiFi is unavailable?</div><div>2. <strong>Do.</strong> Type wifi WrongNetwork x into the serial monitor. The sketch saves a network that does not exist and restarts. Watch the retry messages, then type reset to restore Wokwi-GUEST.</div><div>3. <strong>Explain.</strong> Do the waits double? At what wait do they stop growing, and why?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 2 — What Gets Sent, and Where</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Going further: offline buffering.</div><div>Readings taken while the network is down are lost unless the device stores them and sends them later. The D4 sketch keeps a small <strong>ring buffer</strong> in RAM for this, and its comments explain how it works. You don't need to design one for this course.</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">The Payload Contract</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">A <strong>payload contract</strong> is a written agreement between the device and whatever receives its data: exactly which fields each message contains, their types and units, and what happens when the format changes. It is the network version of D3's serial protocol document.</div>

```json
{"v":1,"device":"watch-a1b2c3","t_ms":125000,"steps":208,"hr_bpm":73,"batt_v":3.9,"buffered":0}
```

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Field</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Type</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Unit</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Meaning</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">v</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">integer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Contract version; increase it when fields change</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">device</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">string</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Unique device name, from the chip's MAC address</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">t\_ms</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">integer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ms</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Device time when the reading was taken</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">steps</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">integer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">steps</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Total since boot</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">hr\_bpm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">integer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">bpm</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Last heart-rate result</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">batt\_v</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">number</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">V</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Battery voltage</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">buffered</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">integer</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">readings</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How many readings are still waiting to be sent (from the sketch's offline buffer)</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The t\_ms field records the device's own clock, which restarts at every boot. A dashboard that needs real dates should use the time the message arrived, or the device must set its clock from the network, as esp\_watch does at first boot. Write down which one your contract uses.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">HTTP POST or MQTT Publish?</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Part 1 taught both, and A1 already chose your connection route. The short version: <strong>HTTP POST</strong> suits occasional uploads to a web API, because each request opens its own connection. <strong>MQTT</strong> suits frequent small readings and many listeners, because the connection stays open and each message is small. Use whichever A1 chose, and write one line saying why.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The sketch uses MQTT with a <strong>last will</strong>: when it connects, it tells the broker "if I disappear, publish offline on my status topic". Then it publishes online itself. A dashboard subscribed to the status topic always knows the device's state, even if the device lost power without saying goodbye.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch uses neither for readings. It uses WiFi once, at first boot, to fetch the time and weather, and no readings leave the watch (A2's decision note). A version that kept a semester's history would need one of the two, and a new decision note.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The sketch publishes to test.mosquitto.org, a free public broker whose own page warns "anybody could be listening" [2]. Use it only for test data. To watch your messages arrive, subscribe with a desktop client such as MQTT Explorer [3], or with the dashboard tool from Part 1.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What a Good Device Dashboard Shows</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A dashboard for a device, as opposed to one for the data, answers four questions at a glance:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Question</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Shown as</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What is the value now?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The latest reading, large, with its unit</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">How has it changed?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A history chart over a sensible window</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Is the device alive?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Online or offline, from the status topic</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">When did we last hear from it?</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Last-seen time, and how long ago</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The last row catches the most common confusion. A chart that simply stops updating looks exactly like a device whose values have not changed. "Last seen 3 hours ago" removes the doubt.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Part 3 — Settings That Survive a Power Cycle</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Why Hard-Coded Credentials Are a Dead End</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A WiFi name and password in the source code has three problems. Changing network means reflashing. Anyone with the code, including anyone who sees your repository, has the password. And every device built from that code has the same credentials.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The ESP32 has a small area of flash set aside for <strong>non-volatile storage</strong> (NVS). The Arduino <strong>Preferences</strong> library stores named values there, and they survive restarts and power loss [4]. Values are grouped under a <strong>namespace</strong>, a short name for your application's settings.</div>

```cpp
void loadSettings() {
  prefs.begin("watch", true);                  // read-only
  ssid = prefs.getString("ssid", "Wokwi-GUEST");
  pass = prefs.getString("pass", "");
  prefs.end();
}
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The second argument to getString is the <strong>default</strong> used when nothing has been saved yet, so a brand-new device still starts sensibly.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The same storage suits <strong>calibration</strong> values: a battery ADC correction factor from B3, a step-counter threshold tuned to one wearer. Anything that differs per device and must survive a restart belongs here, not in the code.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;background:#fef2f2;border-left:4px solid #dc2626;border-radius:6px;padding:8px 14px;color:#991b1b;">Two cautions. Flash has a limited number of write cycles, so save settings when they change, never on every pass of loop(). And NVS is not encrypted by default, so a determined person with the device could read the stored password. That is acceptable for a student prototype, and worth a line in your A2 privacy notes.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Getting Settings In: Provisioning</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Provisioning</strong> is how a new device receives its settings. The sketch uses the simplest method that works on a laptop: type wifi &lt;ssid&gt; &lt;password&gt; into the serial monitor, and it saves them and restarts.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Real products often use a <strong>captive portal</strong> instead: the device opens its own access point and a web page where you pick a network (the WiFiManager library does this [5]). You do not need one here.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Factory Reset</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every device that stores settings needs a way back to a clean state: a new owner, a wrong password, a corrupted setting. The sketch offers two: type reset, or hold the "next" button for 5 seconds. Both call prefs.clear(), which deletes every key in the namespace [4], and restart.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">The button hold is checked without waiting, using the same pattern as D2:</div>

```cpp
if (digitalRead(PIN_BTN_NEXT) == LOW) {
  if (pressedSince == 0) pressedSince = now;
  else if (now - pressedSince >= RESET_HOLD_MS) factoryReset();
} else {
  pressedSince = 0;
}
```

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Try it: Survive a power cycle.</div><div>In Wokwi, run the D4 project.</div><div>1. <strong>Predict.</strong> If you save new WiFi details with the wifi command, will they still be there after the chip restarts?</div><div>2. <strong>Do.</strong> Type wifi MyTest x. The sketch saves it and restarts itself. Read the first "connecting to" line. Then hold the button for 5 seconds and read it again.</div><div>3. <strong>Explain.</strong> Did the setting survive the restart? What did the reset do?</div></div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Putting It All Together</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1. Write your payload contract.</strong> Every field, with type, unit and meaning, plus a version field and a note on how time is handled.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2. Choose HTTP or MQTT</strong> for your product, with a one-line reason, and add it to your A2 decision notes if it changes an earlier decision.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3. Make the connection robust.</strong> Adapt the D4 sketch: non-blocking connection, and backoff with a cap you have chosen.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4. Publish to a dashboard.</strong> Use the Part 1 dashboard platform, or MQTT Explorer, and show the four things: value, history, status and last seen.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5. Move settings into NVS.</strong> WiFi credentials and at least one calibration value. Add a factory reset.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> a working device (Wokwi or hardware) publishing to a dashboard, with a screenshot; your payload contract; and evidence that a setting survives a restart. Save them in your design pack.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your sketch, contract and screenshots and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. No while loop waits for WiFi or the broker to connect. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Reconnection uses exponential backoff with a stated cap. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. The choice of HTTP or MQTT is written down with a one-line reason. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. The payload contract lists every field with type and unit, and has a version. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The dashboard shows the current value, history, online status and last-seen time. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. No WiFi password appears in the source code. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. At least one setting is stored in NVS and survives a restart. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. A factory reset exists and clears the stored settings. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> A device retries its WiFi connection every second, with each attempt searching for 15 s. The network is down for an hour. What is the best improvement?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Retry every 0.5 s to reconnect faster.</li><li style="margin:6px 0;">B. Use exponential backoff with a cap, so failed attempts become rarer and the radio searches a small fraction of the time.</li><li style="margin:6px 0;">C. Give up permanently after three failures.</li><li style="margin:6px 0;">D. Increase the timeout to 60 s.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> It keeps reconnecting, but cuts the radio's searching time from almost all of the hour to about a fifth or less. <strong>A</strong> wastes even more energy. <strong>C</strong> leaves the device offline until someone restarts it. <strong>D</strong> makes each failed attempt longer, which makes things worse.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A dashboard chart of steps stopped moving two hours ago. What single addition would tell the viewer whether the wearer has simply been sitting still?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A bigger chart</li><li style="margin:6px 0;">B. A "last seen" time and online status from the device</li><li style="margin:6px 0;">C. More decimal places</li><li style="margin:6px 0;">D. A colour change</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> If the device was last seen seconds ago, the flat chart is real; if hours ago, the device is offline. <strong>A</strong>, <strong>C</strong> and <strong>D</strong> make the chart easier to read without answering the question.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> A watch's battery is pulled out. An hour later its dashboard, subscribed to the status topic, still shows "online". What was missing when the watch connected to the broker?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. TLS encryption</li><li style="margin:6px 0;">B. A last will of "offline" on the status topic, which the broker publishes when the device's connection drops</li><li style="margin:6px 0;">C. A retained "online" message</li><li style="margin:6px 0;">D. A shorter payload</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> A device that loses power cannot announce it, so the broker announces it on the device's behalf. <strong>A</strong> protects the data but says nothing about whether the device is there. <strong>C</strong> makes things worse, because the stale "online" stays. <strong>D</strong> has no effect on status.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Where should a step-counter threshold tuned for one particular wearer be stored?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. In the source code, as a constant.</li><li style="margin:6px 0;">B. In non-volatile storage (Preferences), with a sensible default, because it differs per device and must survive restarts.</li><li style="margin:6px 0;">C. In a RAM variable only.</li><li style="margin:6px 0;">D. On the dashboard.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Per-device values that must persist belong in NVS. <strong>A</strong> gives every device the same value and needs a reflash to change it. <strong>C</strong> is lost at every restart. <strong>D</strong> makes the watch depend on the network for its own basic function.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A plant-watering sensor sends one small reading every 10 seconds, and three different apps want to receive it. Which fits better?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. HTTP POST, because it is simpler to debug</li><li style="margin:6px 0;">B. MQTT publish, because the connection stays open, each message is small, and any number of subscribers can listen</li><li style="margin:6px 0;">C. Neither; send email instead</li><li style="margin:6px 0;">D. HTTP GET</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Frequent small readings with several listeners are what MQTT is built for. <strong>A</strong> works but opens a connection per reading and needs a server endpoint per listener. <strong>C</strong> is not a data protocol for devices. <strong>D</strong> fetches data rather than sending it.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The idea to carry forward: <strong>assume the network is absent, and treat its presence as a bonus.</strong> Everything the wearer needs works without it; everything that uses it survives losing it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">In <a href="D5-debugging-and-robustness.md">D5 — Debugging and Robustness</a> you will look at the failures that are not network failures: crashes, resets, stack overflows and stuck buses, and how to make each one visible and recoverable.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Wokwi. ESP32 WiFi Networking (the virtual Wokwi-GUEST access point, no password, channel 6; public gateway for outgoing connections). https://docs.wokwi.com/guides/esp32-wifi</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Eclipse Mosquitto. test.mosquitto.org (public test broker; port 1883 unencrypted and unauthenticated; "Please don't publish anything sensitive, anybody could be listening"). https://test.mosquitto.org/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. MQTT Explorer. MQTT Explorer (free desktop MQTT client showing a structured topic tree). http://mqtt-explorer.com/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Espressif Systems. Arduino-ESP32: Preferences (stores data in NVS, retained across restarts and power loss; begin, putString, clear). https://docs.espressif.com/projects/arduino-esp32/en/latest/api/preferences.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. tzapu. WiFiManager (WiFi connection manager with a web captive-portal configuration, for ESP8266 and ESP32 Arduino). https://github.com/tzapu/wifimanager</div>

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:justify;line-height:1.7;"><div style="font-weight:700;margin-bottom:3px;color:#1e40af;">Note on numbers.</div><div>Component values, prices and specifications in this reading are example values chosen for clear calculation. Always confirm against the datasheet or supplier listing for the part you are actually using.</div></div>
