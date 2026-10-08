# Module 5 — Cloud IoT
## From a Standalone Device to a Connected System

**Course:** Applied IoT
**Module:** 5 — Cloud IoT

---

## Leaving the Workbench

Across Modules 1 to 4, your ESP32-S3 has been a self-contained little world. It read a button, watched a light-dependent resistor, listened through a microphone, and drove an LED or a buzzer. Every loop of `Sense → Compute → Actuate` started and finished on the same board, on your desk, with nothing beyond a few wires involved.

That is a complete and useful pattern, but it stops at the edge of the breadboard. A real IoT deployment rarely lives alone. A soil-moisture sensor in a field is only useful if a farmer, an app or an automated valve somewhere else finds out what it measured. A wearable device is only useful if the reading eventually reaches a phone, a server or a dashboard, often far from where the sensing happened.

This module adds the missing piece: **communication beyond the board**. The progression is:

```text
ESP32-S3  →  Wi-Fi  →  HTTP  →  (limits of HTTP)  →  Publish/Subscribe  →  MQTT Broker  →  Topics  →  Multiple Devices
```

By the end, you will have taken a device that only spoke to itself and turned it into one node in a small network of things, exchanging data with a server and with other devices through a broker.

---

## Connectivity: Putting Your ESP32-S3 on a Network

### Local Wires vs a Network

Every sensor and actuator you have used so far was connected by a **direct wire**: a GPIO pin, a specific voltage, a specific pin name in your code. That kind of connection only works between things that are physically near each other and wired on purpose.

A **network** connection is different. Instead of a dedicated wire between two known points, your device joins a shared communication medium and reaches other devices by *address*, not by wire. Two ideas sit underneath almost everything in this module:

- **Local network.** A group of devices (your ESP32-S3, your laptop, your Wi-Fi router) that can reach each other directly, usually inside one home, lab or building.
- **The Internet.** A much larger network of networks. Your local network reaches the Internet through a **router**, which forwards traffic between your local devices and the outside world.

An IoT device can be useful on a local network alone (for example, talking only to a phone in the same room), but most of the systems this module builds assume the device can also reach a server or a broker somewhere else, through the Internet.

### Wi-Fi as the Connection Layer

The ESP32-S3 you have been using has built-in **Wi-Fi** hardware, and CircuitPython exposes it through a module simply called `wifi`. Wi-Fi is the *radio link* between your board and a nearby access point (typically your router). It is the first hop of every network connection this module uses; HTTP and MQTT both travel over it, but neither of them cares how the bits got as far as the router. Wi-Fi's job ends there.

Connecting is a small number of steps, and CircuitPython keeps them close to plain English:

```python
import os
import wifi

ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")

print("Connecting to", ssid, "...")
wifi.radio.connect(ssid, password)
print("Connected. IP address:", wifi.radio.ipv4_address)
```

Two details matter here.

**Credentials never live in the code.** `os.getenv(...)` reads values from a settings file (conventionally `settings.toml`) that stays on the device but is kept out of anything you might share or commit to version control. This is not a stylistic preference: a Wi-Fi password hardcoded into a script that gets copied, shared or pushed to a public repository is a password given away.

**`wifi.radio.connect()` blocks until it succeeds or fails.** Your program pauses at that line until the board has joined the network or CircuitPython raises an exception because the password was wrong, the network was out of range, or the connection timed out. This is a useful debugging signal by itself: if your program never reaches the `print` line after `connect()`, the problem is at the Wi-Fi link, before HTTP or MQTT even enter the picture.

### Proving the Connection Actually Happened

A board that "looks" connected and a board that *is* connected are not the same thing. Two pieces of information let you check:

- **`wifi.radio.ipv4_address`** — the address your router assigned to the board. If this exists, your board has joined the local network.
- **`wifi.radio.ap_info`** — details about the access point it joined (on boards and CircuitPython versions where this is available), useful for confirming signal strength or which network you actually landed on if more than one is in range.

> **Prediction.** Before running the connection code, guess what happens if the SSID is correct but the password is wrong. Then try it (or check the documentation for your CircuitPython version) and see whether your guess matches what actually happens.

Having an IP address on the local network is necessary, but it is not the same as reaching the Internet — that additionally depends on your router and its connection to the wider network. For everything in this module, having an IP address is the signal that Wi-Fi has done its job and it is safe to move up a layer.

```text
ESP32-S3  ──Wi-Fi──►  Router / Access Point  ──►  Local network  ──►  Internet  ──►  Server / Broker
```

---

## HTTP: Asking a Server for Something

### The Client-Server Mental Model

Once your board is on a network, it needs something to talk *to*. The simplest and most familiar pattern is the one behind almost every website you have ever opened: **client and server**.

- A **server** is a program, usually running continuously somewhere else, that waits for requests and responds to them.
- A **client** is a program that initiates contact, sends a request, and waits for a reply.

Your ESP32-S3, in this pattern, is the client. It is not waiting for the world to talk to it; it reaches out.

**HTTP** (HyperText Transfer Protocol) is the language most clients and servers use to have that conversation. It follows a strict rhythm:

```text
Client                          Server
  │──── request ────────────────►│
  │                               │  (server processes the request)
  │◄──── response ────────────────│
```

A **request** names an action and a target: "GET the current price" or "POST this temperature reading." A **response** carries back a **status code**, a short number that summarises what happened, and usually a **body** with the actual content, often written in a format called JSON.

| HTTP method | Intent | Typical IoT use |
|---|---|---|
| `GET` | Retrieve something | Fetch a configuration value or a forecast |
| `POST` | Send/create something | Send a new sensor reading |
| `PUT` | Replace/update something | Overwrite a stored value with a new one |

| Status code range | Meaning |
|---|---|
| `2xx` | Success — the server did what was asked |
| `4xx` | Client error — the request itself was wrong (bad address, bad data) |
| `5xx` | Server error — something failed on the server's side |

### Sending Sensor Data with `adafruit_requests`

CircuitPython does not include a general-purpose networking library the way desktop Python does. Instead, the `adafruit_requests` library provides an HTTP client modeled closely on Python's familiar `requests` library, built on top of the networking pieces CircuitPython already gives you: `socketpool` for raw network sockets, and `ssl` if the address you are contacting uses HTTPS.

```python
import os
import ssl
import wifi
import socketpool
import adafruit_requests

wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

url = os.getenv("HTTP_ENDPOINT")   # provided by your course environment
reading = {"temperature_c": 23.4}

response = requests.post(url, json=reading)
print("Status:", response.status_code)
print("Body:", response.text)
```

A few things to notice, connecting the code to the model above:

- `socketpool.SocketPool(wifi.radio)` is the bridge between the Wi-Fi connection you already made and the networking library. Nothing above this line changes if you later switch from HTTP to MQTT; only what happens *after* the pool is created changes.
- `requests.post(url, json=reading)` is the request: method `POST`, target `url`, body `reading` (automatically encoded as JSON).
- `response.status_code` and `response.text` are the two halves of the response you actually look at: did it succeed, and what did the server say back.

> **Note.** The exact way `adafruit_requests.Session` is constructed has changed between library versions. Confirm the pattern against the version of the library bundled with your course setup before relying on this exact code. Never invent an endpoint address, an API key or a broker address — use the one specified by your course environment.

> **Modify and observe.** Change the value in `reading`, or add a second field such as `"humidity": 55`, and send it again. Look at what the server sends back each time. Does the status code change if you send a badly formed request, for example a string where a number is expected? This is exactly the kind of controlled poking that reveals what a server actually checks.

### Where HTTP Leaves You

HTTP gives you a clean, well-understood way to send a single reading and get a single answer back. That is genuinely enough for many small projects: log a temperature every ten minutes, fetch a setting once at startup. The next section asks what breaks when the system grows.

---

## Why MQTT: When Asking Isn't Enough

### The Cost of Always Having to Ask

HTTP is a **pull** protocol at heart: nothing happens until the client asks. Imagine a monitoring dashboard that wants to know the temperature from ten sensors, updated every second. With HTTP, the only way to stay current is to keep asking, over and over — this is called **polling**. Each request opens a connection, sends bytes, waits for a reply and closes again, even if the temperature has not changed at all since the last check.

That has real costs as a system grows:

- **Wasted requests.** Most polls return "nothing new," but the network and both endpoints paid the cost of a full request-response cycle anyway.
- **Tight coupling.** The client has to know exactly which server, at exactly which address, holds the data it wants. If ten devices need to reach ten other devices this way, you are close to building ten separate point-to-point relationships.
- **Awkward fan-out.** If five different applications all want the same sensor reading, either the sensor answers five separate requests, or something in the middle has to re-distribute the data. HTTP alone does not solve that.

### Push Instead of Pull

The alternative is to flip who acts first. In a **push** or **event-driven** model, the data source announces new information as soon as it has it, and anyone interested simply receives it — no repeated asking required.

```text
Pull (HTTP):   Client asks → Server answers → Client asks again → Server answers again → …
Push (events): Something happens → interested parties are told, once, when it happens
```

### Publish/Subscribe, at the Idea Level

The specific push pattern this module builds on is **publish/subscribe**. Instead of a client addressing a specific server, a **publisher** announces information under a named channel, and any number of **subscribers** who have expressed interest in that channel receive it automatically. Publishers and subscribers never need to know about each other directly; a piece of intermediary infrastructure handles the delivery.

This is a genuine shift in mental model, not just a different set of function calls:

| | HTTP | Publish/Subscribe |
|---|---|---|
| Who acts first | The client, every time it wants data | The publisher, once, when it has new data |
| Relationship | Client knows the server's address | Publisher and subscriber don't need to know each other |
| Fan-out to many receivers | Awkward — server must be asked repeatedly, once per client | Natural — many subscribers receive the same publication |
| Typical use | One-off request, configuration fetch, simple data submission | Ongoing streams of sensor data, frequent updates, many devices |

MQTT (Message Queuing Telemetry Transport) is the specific protocol this module uses to put publish/subscribe into practice. It was designed with constrained devices and unreliable networks in mind, which is part of why it fits small microcontrollers like the ESP32-S3 so well: it is intentionally lighter than repeatedly opening HTTP connections.

---

## MQTT: Broker, Publisher, Subscriber, Topic

### The Three Roles

MQTT organizes communication around a small number of ideas, and it is worth being precise about each one before writing any code.

- **Broker.** A server that sits in the middle of everything. It never generates data itself; its whole job is to receive messages from publishers and deliver them to the right subscribers.
- **Publisher.** Any device or program that sends a message. In this course, that will usually be your ESP32-S3 sending a sensor reading.
- **Subscriber.** Any device or program that has told the broker it wants messages from a particular channel. That could be another ESP32-S3, a laptop script, or a dashboard.
- **Topic.** The named channel a message is published to and a subscriber listens on, written as a short path such as `classroom/deskA/temperature`.

A single device is often both a publisher and a subscriber at once — for example, sending its own sensor readings while also listening for a command topic that tells it what to do.

```text
   Publisher(s)                    Broker                    Subscriber(s)
  ┌───────────┐               ┌─────────────┐               ┌─────────────┐
  │ Device A  │──publish────►│             │───deliver────►│ Monitor      │
  │ (sensor)  │               │   MQTT      │               │ (dashboard)  │
  └───────────┘               │   Broker    │               └─────────────┘
                                │             │───deliver────►┌─────────────┐
                                └─────────────┘               │ Another     │
                                                               │ subscriber  │
                                                               └─────────────┘
```

Neither device in this diagram knows the other's address, or even that the other exists. Both only know the broker's address and the topic name. That decoupling is the entire point: you can add a second, third or tenth subscriber to the same topic without changing anything on the publishing device at all.

### Topics Are Just Structured Names

A topic is a plain string, with `/` used to express levels, much like a file path: `home/livingroom/temperature`. Subscribers do not have to match a topic exactly — MQTT defines two wildcards for subscriptions:

- `+` matches exactly one level: `home/+/temperature` matches `home/livingroom/temperature` and `home/kitchen/temperature`.
- `#` matches everything below that point: `home/#` matches every topic anywhere under `home/`.

Wildcards only apply to *subscribing*; a publisher always publishes to one specific, fully written topic.

### Connecting, Publishing and Subscribing in CircuitPython

CircuitPython's MQTT support comes from the `adafruit_minimqtt` library, built on the same `socketpool` you already used for HTTP. The overall shape of an MQTT program is different from the HTTP examples above: instead of a single request and a single response, the program sets up a persistent relationship with the broker and then keeps checking in on it.

```python
import os
import wifi
import socketpool
from adafruit_minimqtt import adafruit_minimqtt as MQTT

wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
pool = socketpool.SocketPool(wifi.radio)

def on_message(client, topic, message):
    print("Received on", topic, ":", message)

mqtt_client = MQTT.MQTT(
    broker=os.getenv("MQTT_BROKER"),   # given by your course environment
    port=int(os.getenv("MQTT_PORT")),
    socket_pool=pool,
)
mqtt_client.on_message = on_message

mqtt_client.connect()
mqtt_client.subscribe("classroom/deskA/temperature")

mqtt_client.publish("classroom/deskA/temperature", "23.4")

while True:
    mqtt_client.loop()
```

Reading this against the diagram above:

- `mqtt_client.connect()` is the moment your device joins the broker, the same way `wifi.radio.connect()` joined the Wi-Fi network — a separate, earlier step.
- `subscribe(...)` registers interest in a topic. From this point on, any message published to that topic (by *any* publisher, including this same device) will trigger `on_message`.
- `publish(...)` sends a message under a topic name. It does not need to know who, if anyone, is listening.
- `mqtt_client.loop()` has to run repeatedly. Unlike the one-shot HTTP request, MQTT messages can arrive at any time, and `loop()` is what actually checks the network and calls `on_message` when something is waiting.

> **Assumption.** The broker address, port and any authentication must come from your course's specified broker, never invented. Whether that broker needs a username, password or TLS (`ssl_context`) depends entirely on that broker's configuration — confirm it before writing connection code, rather than assuming a plain, unauthenticated connection.

> **Observe.** Publish a message from your board, and watch it appear in `on_message` on the *same* board, since it is subscribed to the topic it just published to. Then try publishing from a second device or a second running program, subscribed to the same topic, and watch the message arrive there too — with no direct connection between the two publishers at all.

### Tracing a Message End to End

It is worth walking through the full path a single reading takes, since every idea above eventually collapses into this sequence:

1. A sensor device measures something (say, temperature) and calls `mqtt_client.publish("classroom/deskA/temperature", "23.4")`.
2. The message travels over Wi-Fi, then the local network, to the broker's address.
3. The broker looks at the topic name and checks which currently-connected clients are subscribed to it (exactly, or through a wildcard).
4. The broker delivers a copy of the message to each matching subscriber.
5. Each subscriber's `on_message` callback fires the next time it calls `loop()`, with the topic and the payload.

Notice that the publishing device never learns who received the message, or how many subscribers there were. That is not a limitation to work around — it is the design.

---

## Multi-device MQTT: From One Link to a Small Network

### Many Publishers, One Topic

Because the broker mediates everything, nothing stops several devices from publishing to the same topic. If Device A and Device B both publish to `classroom/temperature`, a subscriber to that topic receives both streams, mixed together, in the order the broker delivers them.

```text
Device A ──┐
Device B ──┼──► MQTT Broker ──► Subscriber(s)
Device C ──┘
```

This is powerful, but it introduces a question the single-device examples above never had to answer: **if three devices publish to the same topic, how does a subscriber know which reading came from which device?**

MQTT itself does not attach an identity to a message. If that distinction matters, you have to build it in yourself, in one of two ways:

- **Put the identity in the payload.** Instead of publishing `"23.4"`, publish something like `{"device": "deskA", "temperature_c": 23.4}`, so the subscriber can read the source out of the message body.
- **Put the identity in the topic.** Give each device its own topic, such as `classroom/deskA/temperature` and `classroom/deskB/temperature`, and let a subscriber use a wildcard (`classroom/+/temperature`) to receive from all of them while still knowing, from the topic each message arrived on, which device it came from.

Both are valid engineering choices with a real trade-off: a shared topic with an identity field is simpler to subscribe to (one subscription covers everyone), while per-device topics make it trivial to subscribe to just one device, at the cost of a slightly longer topic name for each one.

> **Engineering decision.** If you were building a classroom system with fifteen desks, each reporting temperature and light level, would you design one topic per desk, one topic per measurement type, or one topic for everything with identifying fields in the payload? There is no single correct answer — the right choice depends on how subscribers will want to filter the data.

### Separating Data from Commands

A pattern worth adopting early: keep the topics that carry **sensor data** (device → broker → monitor) visually and structurally separate from topics that carry **commands** (application → broker → device), even though both are ordinary MQTT topics under the hood.

```text
classroom/deskA/temperature      ← sensor data, published by the device
classroom/deskA/command          ← commands, published by a controller, subscribed to by the device
```

A device that is a publisher on its own data topic is often, at the same time, a subscriber on its own command topic — for example, listening for `"ON"` or `"OFF"` to control an LED. This is where the "publisher and subscriber roles can both live on the same device" idea from earlier stops being abstract: the device runs both `publish()` calls (for its readings) and an `on_message` handler (for incoming commands) in the same `loop()`.

### Building the System in Stages

The practical path to a working multi-device setup mirrors how the ideas were introduced:

1. **One publisher, one subscriber, one topic.** Get a single sensor device publishing readings, and a single separate client (which could be a laptop script) subscribed and printing what arrives. Confirm the basic path works before adding complexity.
2. **Sensor Device → Broker → Monitoring Device.** Give the topic a meaningful name, publish real sensor readings instead of test text, and check the values arriving at the subscriber match what the sensor reports locally.
3. **Multiple publishers, shared or per-device topics.** Add a second and third publishing device. Decide, deliberately, whether they share a topic (with identity in the payload) or use separate topics (with a wildcard subscription), and observe how the subscriber's incoming messages change.
4. **Multiple subscribers.** Add a second subscriber to the same topic — perhaps a script that logs to a file, alongside one that only prints to the console — and confirm both receive every message independently.
5. **Command topics.** Add a topic a device subscribes to, and publish a command to it from another client, watching the device react.

> **Debug tip.** If a subscriber never receives anything, check each layer in order: is the device connected to Wi-Fi (does it have an IP address)? Is it connected to the broker? Is it subscribed to the *exact* topic string the publisher is using (a stray character or a different case will not match)? Is `loop()` actually being called repeatedly? Most "nothing arrived" problems are a mismatch at one of these steps, not a broken broker.

---

## HTTP and MQTT, Side by Side

Both protocols now sit in your toolkit, and choosing between them is itself a skill worth naming explicitly.

| | HTTP | MQTT |
|---|---|---|
| Who initiates | The client, each time | The publisher, when it has news |
| Relationship | Client must know the server's address | Publisher and subscriber only know the broker |
| Best suited to | One-off requests, occasional data submission, fetching a resource | Ongoing streams, many devices, many interested parties |
| Core roles | Client, server | Publisher, subscriber, broker |
| Addressing | A specific URL | A topic, potentially matched by wildcards |

A single real system is often not "HTTP or MQTT" but both, used for what each is good at: MQTT for constant device-to-device and device-to-broker traffic, HTTP for occasional one-off exchanges such as fetching a configuration or reporting to a service that only understands HTTP.

---

### References

1. Adafruit CircuitPython Core Documentation. *wifi — Native networking support* (`wifi.radio.connect`, `ipv4_address`, `ap_info`). https://docs.circuitpython.org/en/latest/shared-bindings/wifi/
2. Adafruit CircuitPython Core Documentation. *socketpool — Socket pool support* (`SocketPool`, used by `adafruit_requests` and `adafruit_minimqtt`). https://docs.circuitpython.org/en/latest/shared-bindings/socketpool/
3. Adafruit CircuitPython Learn Guide. *CircuitPython Requests Library* (`adafruit_requests`, HTTP GET/POST, JSON responses). https://learn.adafruit.com/adafruit-circuitpython-requests
4. Adafruit CircuitPython Learn Guide. *Basics of MQTT* (`adafruit_minimqtt`, connecting to a broker, `publish`, `subscribe`, `on_message`, `loop`). https://learn.adafruit.com/mqtt-in-circuitpython
5. OASIS. *MQTT Version 3.1.1 / 5.0 Specification* (broker/publisher/subscriber roles, topics, wildcards, Quality of Service). https://mqtt.org
6. Adafruit CircuitPython Core Documentation. *os — Miscellaneous operating system interfaces* (`os.getenv`, reading settings from `settings.toml`). https://docs.circuitpython.org/en/latest/shared-bindings/os/

> **Note.** Broker addresses, ports, endpoint URLs and credentials in this reading are placeholders read from your course environment (through `os.getenv`) and must never be replaced with invented values in your own code. Exact constructor arguments for `adafruit_requests.Session` and `adafruit_minimqtt.MQTT` can differ between library versions — confirm both against the versions installed for this course before you rely on the examples above. Sensor values used to illustrate publishing and posting are example values only.