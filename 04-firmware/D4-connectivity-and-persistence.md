# D4 — Connectivity and Persistence: Network, Dashboard and Settings That Survive
## A Device That Keeps Working When the Network Does Not

**Course:** C3 — From Problem Statement to Manufacturable Design
**Module:** 4 — Firmware
**Time:** ~1 hour · **You will produce:** a device publishing to a dashboard, and configuration that survives a power cycle

---

### Hostel WiFi Will Go Down

Part 1's WiFi examples connected in `setup()` and published in `loop()`. On a desk with a good router, that works. Now picture the same code on a student's wrist. The hostel WiFi drops at 11 pm. The student walks from the library to the mess, out of range for ten minutes. The router restarts after a power cut. Each time, a simple sketch either freezes inside `WiFi.begin()`, loses every reading taken while offline, or never reconnects until someone presses reset.

And the WiFi password is typed into the source code. To use the watch on a different network, someone has to edit the firmware and flash it again.

This unit makes the connection **robust**: it connects without blocking, notices when the link drops, and reconnects with increasing delays. It defines what each message contains in a written **payload contract**, shows what a device dashboard should display, and moves settings out of the code into storage that survives a power cycle.

### What You Will Be Able to Do After This Reading

- **Implement** a non-blocking WiFi and MQTT connection with reconnection and exponential backoff.
- **Write** a payload contract, and choose between HTTP POST and MQTT publish for your product.
- **Specify** what a device dashboard should show: live value, history, status and last-seen time.
- **Store** credentials and calibration in non-volatile storage, with a factory reset.

### What Part 1 Already Covered

Part 1 connected an ESP32 to WiFi, called a REST API over HTTP, published over MQTT with a structured JSON payload, and built a cloud dashboard. It also warned against putting credentials in code. **What is new here** is making all of that survive real conditions: no blocking, automatic reconnection, a written contract for every message, and settings stored outside the code.

> **How to read the labels in this material.**
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. The datasheet always wins.
> - **Assumption** — something this reading assumes because your tools or kit will define it precisely.

---

# Part 1 — A Connection That Never Blocks

## Connecting as a State Machine

The simple approach waits:

```cpp
// BLOCKING: nothing else runs until WiFi connects, which may be never.
WiFi.begin(ssid, pass);
while (WiFi.status() != WL_CONNECTED) {
  delay(500);
}
```

The non-blocking approach treats the network as a **state machine**, exactly like the device states in D1 and D2. It starts a connection, then *checks* on it each pass:

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

The complete sketch is in [`assets/code/D4-connected-watch/`](../assets/code/D4-connected-watch/). It runs in Wokwi, whose simulated ESP32 joins a virtual access point called `Wokwi-GUEST` with no password [1], and it compiles for the XIAO ESP32-C3. Here is its network state machine:

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

Be honest about the one exception. The MQTT library's `connect()` does wait while it opens a network connection to the broker. On a working network that is short; on a broken one it can take longer. The design limits the damage rather than pretending it away: connection attempts happen only when the backoff timer allows, so a dead broker costs one short wait every minute, not every pass.

## Exponential Backoff

When a connection fails, retrying immediately is the worst option. If the router has just rebooted, a hundred devices hammering it at once keep it busy. If the broker is down for an hour, retrying every pass wastes battery for an hour.

**Exponential backoff** doubles the wait after each failure, up to a limit, and resets when a connection succeeds:

```text
Attempt:  1     2     3     4      5      6      7      8 ...
Wait:     1 s   2 s   4 s   8 s    16 s   32 s   60 s   60 s (capped)
```

The sketch also adds a little **jitter**, a random extra of up to 20%, so that many devices that lost the network at the same moment do not all retry at the same moment:

```cpp
void scheduleRetry(unsigned long now, const char *why) {
  unsigned long jitter = random(0, backoff / 5 + 1);
  retryAt = now + backoff + jitter;
  Serial.printf("# %s; retry in %lu ms\n", why, backoff + jitter);
  backoff = min(backoff * 2, BACKOFF_MAX_MS);
  netState = Net::Idle;
}
```

Notice the `#` at the start of each debug message. It follows the serial format rule from D3, so these messages never corrupt a data log.

### Worked Example: What Does an Hour Offline Cost?

**Assumption:** each failed attempt costs 15 s of WiFi searching, the timeout, at about 100 mA (esp_watch's modelled WiFi burst figure, a model rather than a measurement).

**Step 1: Retry every 1 s, no backoff.** Each attempt is 15 s of searching plus a 1 s wait, so the radio is searching about 94% of the time.

```text
3,600 s × (15 ÷ 16) = 3,375 s searching
3,375 s × 100 mA ÷ 3,600 = 93.8 mAh
```

**Step 2: Exponential backoff, capped at 60 s.** After the first few minutes, each cycle is 15 s searching plus about 60 s waiting.

```text
Searching fraction ≈ 15 ÷ 75 = 20%
3,600 s × 20% = 720 s searching
720 s × 100 mA ÷ 3,600 = 20 mAh
```

**Check.** An hour without a network costs about 94 mAh with naive retries, more than an entire day's budget from A0's worked example, and about 20 mAh with backoff. A longer cap cuts it further. For a watch that only needs to sync occasionally, a cap of several minutes is reasonable, and that choice belongs in your A2 failure table.

> **Try it: Watch it recover.** Run the D4 project in Wokwi.
> 1. **Predict.** What will the serial monitor show if WiFi is unavailable?
> 2. **Do.** In Wokwi, stop the simulation, open the WiFi part's settings (or type `wifi WrongNetwork x` into the serial monitor to save a network that does not exist), and restart. Watch the retry messages. Then type `reset` to restore the default.
> 3. **Explain.** Do the waits double? How long does it take to come back once the network returns?

---

# Part 2 — What Gets Sent, and Where

> **Going further: offline buffering.** Readings taken while the network is down are lost unless the device stores them and sends them later. The D4 sketch keeps a small **ring buffer** in RAM for this, and its comments explain how it works. You don't need to design one for this course.

## The Payload Contract

A **payload contract** is a written agreement between the device and whatever receives its data: exactly which fields each message contains, their types and units, and what happens when the format changes. It is the network version of D3's serial protocol document.

```json
{"v":1,"device":"watch-a1b2c3","t_ms":125000,"steps":208,"hr_bpm":73,"batt_v":3.9,"buffered":0}
```

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `v` | integer | — | Contract version; increase it when fields change |
| `device` | string | — | Unique device name, from the chip's MAC address |
| `t_ms` | integer | ms | Device time when the reading was taken |
| `steps` | integer | steps | Total since boot |
| `hr_bpm` | integer | bpm | Last heart-rate result |
| `batt_v` | number | V | Battery voltage |
| `buffered` | integer | readings | How many readings are still waiting to be sent (from the sketch's offline buffer) |

The `t_ms` field records the device's own clock, which restarts at every boot. A dashboard that needs real dates should use the time the message arrived, or the device must set its clock from the network, as esp_watch does at first boot. Write down which one your contract uses.

## HTTP POST or MQTT Publish?

Part 1 taught both, and A1 already chose your connection route. The short version: **HTTP POST** suits occasional uploads to a web API, because each request opens its own connection. **MQTT** suits frequent small readings and many listeners, because the connection stays open and each message is small. Use whichever A1 chose, and write one line saying why.

The sketch uses MQTT with a **last will**: when it connects, it tells the broker "if I disappear, publish `offline` on my status topic". Then it publishes `online` itself. A dashboard subscribed to the status topic always knows the device's state, even if the device lost power without saying goodbye.

<!-- REFPRODUCT:START -->
esp_watch uses neither for readings. It uses WiFi once, at first boot, to fetch the time and the weather, and sends nothing. That was the decision note in A2, chosen for battery life and privacy. A version of the watch that solved the hostel problem statement's semester history would need one of the two, and the choice would go in a new decision note.
<!-- REFPRODUCT:END -->

The sketch publishes to `test.mosquitto.org`, a free public broker whose own page warns "anybody could be listening" [2]. Use it only for test data. To watch your messages arrive, subscribe with a desktop client such as MQTT Explorer [3], or with the dashboard tool from Part 1.

## What a Good Device Dashboard Shows

A dashboard for a device, as opposed to one for the data, answers four questions at a glance:

| Question | Shown as |
|---|---|
| What is the value now? | The latest reading, large, with its unit |
| How has it changed? | A history chart over a sensible window |
| Is the device alive? | Online or offline, from the status topic |
| When did we last hear from it? | Last-seen time, and how long ago |

The last row catches the most common confusion. A chart that simply stops updating looks exactly like a device whose values have not changed. "Last seen 3 hours ago" removes the doubt.

<!-- MEDIA
type: screenshot
id: D4-01
caption: A device dashboard answering the four questions: value now, history, status, last seen
brief: A simple dashboard (the Part 1 dashboard platform, or any MQTT dashboard tool) for
  one simulated watch. Top left: a large tile "Steps 208". Top right: a status badge
  "online" in green with "last seen 12 s ago" beneath. Below: a line chart of steps over
  the last 30 minutes, with a visible flat gap where the device was offline and then a
  quick catch-up when it reconnected.
  Clean, readable, no personal account details.
-->

<!-- MEDIA
type: screenshot
id: D4-02
caption: MQTT Explorer subscribed to the simulated watch's topics
brief: MQTT Explorer desktop app connected to test.mosquitto.org, with the topic tree
  expanded to c3course/watch-xxxxxx/, showing "status = online" and "data" with the latest
  JSON payload displayed in the right panel, formatted. The message history panel shows
  several recent payloads. Light theme.
-->

---

# Part 3 — Settings That Survive a Power Cycle

## Why Hard-Coded Credentials Are a Dead End

A WiFi name and password in the source code has three problems. Changing network means reflashing. Anyone with the code, including anyone who sees your repository, has the password. And every device built from that code has the same credentials.

The ESP32 has a small area of flash set aside for **non-volatile storage** (NVS). The Arduino **Preferences** library stores named values there, and they survive restarts and power loss [4]. Values are grouped under a **namespace**, a short name for your application's settings.

```cpp
void loadSettings() {
  prefs.begin("watch", true);                  // read-only
  ssid = prefs.getString("ssid", "Wokwi-GUEST");
  pass = prefs.getString("pass", "");
  prefs.end();
}
```

The second argument to `getString` is the **default** used when nothing has been saved yet, so a brand-new device still starts sensibly.

The same storage suits **calibration** values: a battery ADC correction factor from B3, a step-counter threshold tuned to one wearer. Anything that differs per device and must survive a restart belongs here, not in the code.

Two cautions. Flash has a limited number of write cycles, so save settings when they change, never on every pass of `loop()`. And NVS is not encrypted by default, so a determined person with the device could read the stored password. That is acceptable for a student prototype, and worth a line in your A2 privacy notes.

## Getting Settings In: Provisioning

**Provisioning** is how a new device receives its settings. The sketch uses the simplest method that works on a laptop: type `wifi <ssid> <password>` into the serial monitor, and it saves them and restarts.

Real products use a **captive portal**: with no saved network, the device starts its own WiFi access point; you join it from a phone, a web page opens, and you choose your network there. The widely used open-source WiFiManager library implements this for ESP32 [5]. You do not need to build one in this course. Know that it exists, and design your settings so a portal could fill them in later.

## Factory Reset

Every device that stores settings needs a way back to a clean state: a new owner, a wrong password, a corrupted setting. The sketch offers two: type `reset`, or hold the "next" button for 5 seconds. Both call `prefs.clear()`, which deletes every key in the namespace [4], and restart.

The button hold is checked without waiting, using the same pattern as D2:

```cpp
if (digitalRead(PIN_BTN_NEXT) == LOW) {
  if (pressedSince == 0) pressedSince = now;
  else if (now - pressedSince >= RESET_HOLD_MS) factoryReset();
} else {
  pressedSince = 0;
}
```

> **Try it: Survive a power cycle.** In Wokwi, run the D4 project.
> 1. **Predict.** If you save new WiFi details with the `wifi` command and then stop and restart the simulation, will they still be there?
> 2. **Do.** Save a network name, restart the simulation, and read the first "connecting to" message. Then hold the button for 5 seconds.
> 3. **Explain.** Did the setting survive a simulated restart? What did the reset do? Note: whether Wokwi keeps flash between separate simulation runs depends on the tool, so if it does not, explain what you would expect on real hardware and why.

<!-- FACT:VERIFY whether Wokwi preserves NVS/flash contents between stopping and restarting a simulation was not confirmed; the Try-it asks students to observe and explain either outcome -->

---

# Putting It All Together

## Applying What You Have Learned

**1. Write your payload contract.** Every field, with type, unit and meaning, plus a version field and a note on how time is handled.

**2. Choose HTTP or MQTT** for your product, with a one-line reason, and add it to your A2 decision notes if it changes an earlier decision.

**3. Make the connection robust.** Adapt the D4 sketch: non-blocking connection, and backoff with a cap you have chosen.

**4. Publish to a dashboard.** Use the Part 1 dashboard platform, or MQTT Explorer, and show the four things: value, history, status and last seen.

**5. Move settings into NVS.** WiFi credentials and at least one calibration value. Add a factory reset.

**Deliverable:** a working device (Wokwi or hardware) publishing to a dashboard, with a screenshot; your payload contract; and evidence that a setting survives a restart. Save them in your design pack.

## Self-Check

Open your sketch, contract and screenshots and answer each item Y or N.

1. No `while` loop waits for WiFi or the broker to connect. — Y/N
2. Reconnection uses exponential backoff with a stated cap. — Y/N
3. The choice of HTTP or MQTT is written down with a one-line reason. — Y/N
4. The payload contract lists every field with type and unit, and has a version. — Y/N
5. The dashboard shows the current value, history, online status and last-seen time. — Y/N
6. No WiFi password appears in the source code. — Y/N
7. At least one setting is stored in NVS and survives a restart. — Y/N
8. A factory reset exists and clears the stored settings. — Y/N

---

## Check Your Understanding

**1.** A device retries its WiFi connection every second, with each attempt searching for 15 s. The network is down for an hour. What is the best improvement?

- A. Retry every 0.5 s to reconnect faster.
- B. Use exponential backoff with a cap, so failed attempts become rarer and the radio searches a small fraction of the time.
- C. Give up permanently after three failures.
- D. Increase the timeout to 60 s.

<details>
<summary>Answer</summary>

**B.** It keeps reconnecting, but cuts the radio's searching time from almost all of the hour to about a fifth or less. **A** wastes even more energy. **C** leaves the device offline until someone restarts it. **D** makes each failed attempt longer, which makes things worse.

</details>

**2.** A dashboard chart of steps stopped moving two hours ago. What single addition would tell the viewer whether the wearer has simply been sitting still?

- A. A bigger chart
- B. A "last seen" time and online status from the device
- C. More decimal places
- D. A colour change

<details>
<summary>Answer</summary>

**B.** If the device was last seen seconds ago, the flat chart is real; if hours ago, the device is offline. **A**, **C** and **D** make the chart easier to read without answering the question.

</details>

**3.** Why is MQTT's "last will" useful for a device dashboard?

- A. It encrypts the connection.
- B. The broker publishes the device's "offline" message automatically if the device disappears, so the dashboard knows even after a sudden power loss.
- C. It stores readings while the device is offline.
- D. It makes messages smaller.

<details>
<summary>Answer</summary>

**B.** A device that loses power cannot announce it, but the broker can on its behalf. **A** is TLS's job. **C** is not something the broker does. **D** is not what it does.

</details>

**4.** Where should a step-counter threshold tuned for one particular wearer be stored?

- A. In the source code, as a constant.
- B. In non-volatile storage (Preferences), with a sensible default, because it differs per device and must survive restarts.
- C. In a RAM variable only.
- D. On the dashboard.

<details>
<summary>Answer</summary>

**B.** Per-device values that must persist belong in NVS. **A** gives every device the same value and needs a reflash to change it. **C** is lost at every restart. **D** makes the watch depend on the network for its own basic function.

</details>

**5.** A plant-watering sensor sends one small reading every 10 seconds, and three different apps want to receive it. Which fits better?

- A. HTTP POST, because it is simpler to debug
- B. MQTT publish, because the connection stays open, each message is small, and any number of subscribers can listen
- C. Neither; send email instead
- D. HTTP GET

<details>
<summary>Answer</summary>

**B.** Frequent small readings with several listeners are what MQTT is built for. **A** works but opens a connection per reading and needs a server endpoint per listener. **C** is not a data protocol for devices. **D** fetches data rather than sending it.

</details>

---

## What You Can Now Do, and What Comes Next

- Build a connection that never waits for long, reconnects with backoff, and costs little battery when the network is gone.
- Write a payload contract and choose between HTTP and MQTT with a reason.
- Show a device's health honestly on a dashboard.
- Keep settings out of the code, with provisioning and a factory reset.

The idea to carry forward: **assume the network is absent, and treat its presence as a bonus.** Everything the wearer needs works without it; everything that uses it survives losing it.

In [D5 — Debugging and Robustness](D5-debugging-and-robustness.md) you will look at the failures that are not network failures: crashes, resets, stack overflows and stuck buses, and how to make each one visible and recoverable.

---

## References

1. Wokwi. *ESP32 WiFi Networking* (the virtual `Wokwi-GUEST` access point, no password, channel 6; public gateway for outgoing connections). https://docs.wokwi.com/guides/esp32-wifi
2. Eclipse Mosquitto. *test.mosquitto.org* (public test broker; port 1883 unencrypted and unauthenticated; "Please don't publish anything sensitive, anybody could be listening"). https://test.mosquitto.org/
3. MQTT Explorer. *MQTT Explorer* (free desktop MQTT client showing a structured topic tree). http://mqtt-explorer.com/
4. Espressif Systems. *Arduino-ESP32: Preferences* (stores data in NVS, retained across restarts and power loss; `begin`, `putString`, `clear`). https://docs.espressif.com/projects/arduino-esp32/en/latest/api/preferences.html
5. tzapu. *WiFiManager* (WiFi connection manager with a web captive-portal configuration, for ESP8266 and ESP32 Arduino). https://github.com/tzapu/wifimanager

> **Note on numbers.** Component values, prices and specifications in this reading are
> example values chosen for clear calculation. Always confirm against the datasheet or
> supplier listing for the part you are actually using.
