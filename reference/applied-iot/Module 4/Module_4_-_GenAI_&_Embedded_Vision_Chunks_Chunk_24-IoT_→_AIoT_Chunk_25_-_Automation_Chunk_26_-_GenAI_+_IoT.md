# Module 4 — GenAI & Embedded Vision
## From IoT to AIoT: Adding an Interpretation Layer to Your System

**Course:** Applied IoT
**Module:** 4 — GenAI & Embedded Vision

---

## Where This Reading Picks Up

Across the previous modules, you built a complete loop: a sensor produced a reading, the ESP32-S3 read it through digital or analog inputs, your CircuitPython program made a decision, and an actuator or output responded. That decision was always written by you, in advance, as a fixed rule: *if the button is pressed, toggle the LED; if the LDR reading falls below a threshold, turn on the light; if the temperature exceeds a value, sound the buzzer.*

This kind of system is powerful, predictable and still the backbone of most real IoT deployments. But it has a hard limit: it can only do exactly what its rules describe. It cannot notice a pattern its designer did not anticipate, and it cannot explain a reading in plain language. This reading introduces the layer that sits on top of a conventional IoT system to address that limit — a layer built from **automation platforms** and **AI services** — and shows how the two combine into what is generally called **AIoT**.

The path this reading follows is:

```text
Traditional IoT → Rule-based automation → Workflow automation → AI integration → LLM API → AIoT workflow
```

By the end, you will understand where an AI component fits inside an IoT pipeline, how an automation platform such as **n8n** connects a device event to that AI component, and how to reason about when AI genuinely adds value and when a simple rule is the better engineering choice. It is worth saying plainly, before going further: **AI does not replace the sensor, the microcontroller or the actuator.** It is an additional computational stage that helps interpret what the sensing system already produces.

---

## From Rule-Based Systems to Intelligent Systems

Every rule-based system you have built so far follows the same shape: a condition, checked against a fixed threshold, that triggers a fixed response.

```text
if temperature > 30:
    send_alert()
```

This is deterministic: given the same input, it always produces the same output, and you can predict its behaviour completely just by reading the code. That predictability is a genuine strength — for safety-relevant decisions, you usually *want* a system to behave exactly the same way every time.

The limitation appears when the situation is not well described by a single threshold. Consider a room where temperature and humidity are both being logged. A temperature of 29 °C might be unremarkable on its own, but combined with rapidly rising humidity and a time of day when the room is normally empty, it might indicate something worth a human's attention — a window left open, a fault in a cooling unit, an early sign of condensation risk. Writing a rule that captures all of these combinations, and phrasing the resulting message usefully for a person, becomes difficult very quickly.

This is the gap that an **AI-assisted decision layer** is designed to fill. Instead of a fixed threshold, the raw sensor readings are handed to a model that can:

- weigh several variables together rather than checking them one at a time,
- generalise beyond conditions the original programmer explicitly anticipated,
- produce a natural-language explanation rather than a bare true/false signal.

The trade-off is equally important. A rule-based check is deterministic and auditable. An AI-based interpretation is **probabilistic** — it can phrase the same underlying situation differently each time, and, more seriously, it can be confidently wrong. Holding both of these facts at once, rather than treating AI as a strict upgrade, is the mindset this module is trying to build.

> **Prediction.** Before reading further, think about a sensor system you have already built in this course. Is there a decision in it that would benefit from being reasoned about "in combination" rather than by a single threshold? Is there a decision where you would *not* want that flexibility, because you need the same input to always produce the same output?

---

## Where AI Fits in an IoT Pipeline

It helps to place AI explicitly inside the pipeline you already know, rather than treating it as a separate, unrelated system.

```text
Sensing (ESP32-S3 + sensor)
        │
        ▼
Data transmission / automation layer  (e.g. n8n)
        │
        ▼
AI / ML processing or interpretation  (e.g. an LLM API)
        │
        ▼
Action / response  (notification, log entry, actuator command)
```

The sensing stage does not change at all — it is still the ESP32-S3, CircuitPython and the sensors you have already used. What changes is what happens to the data *after* it leaves the device. In a purely rule-based system, that data goes straight into a condition check written in your firmware. In an AIoT system, an extra interpretive stage is inserted before the final action.

AI can occupy this stage in more than one place, depending on how the system is designed:

- **On the device itself (edge inference).** A small model runs directly on the microcontroller or a nearby edge computer. This keeps data local and can work without an internet connection, but it is constrained by the very limited memory and processing power of a microcontroller like the ESP32-S3.
- **In the automation/orchestration layer.** The device sends its reading to a workflow platform, which decides what to do with it, including whether to call out to an AI service. This is the arrangement this reading focuses on, because it keeps the device simple and puts the more demanding computation where there is more capacity for it.
- **As a cloud-based API call.** The actual "thinking" happens on a remote server operated by an AI provider, reached over the internet through an API. The device or the automation layer sends data to it and receives an interpretation back.

For this course, the practical arrangement is the second and third combined: the **ESP32-S3 senses**, **n8n automates and orchestrates**, and an **LLM API interprets**. Keeping these three roles distinct in your head — device, automation platform, external AI service — will make the rest of this reading, and your own workflow design, much easier to reason about.

---

## Automation: Turning an Event Into a Response

Before adding AI to the picture, it is worth being precise about what "automation" means, because the vocabulary carries over directly into how n8n workflows are built.

An **event** is something that happens and is worth noticing: a sensor reading arrives, a value crosses a limit, a button is pressed. A **trigger** is the mechanism that starts a workflow in response to that event — it could be an incoming HTTP request, a scheduled check every few minutes, or a message arriving on a communication channel. A **condition** is a rule evaluated against the event data to decide whether to continue (for example, "is the temperature above 30 °C?"). An **action** is the resulting operation once the condition is satisfied: sending a notification, writing a log entry, calling another service, or commanding an actuator.

```text
Event  →  Trigger  →  Condition  →  Action
(sensor reading)   (starts the workflow)   (decide whether to proceed)   (notify / actuate / log)
```

This same pattern underlies both traditional automation and AI-assisted automation. The difference between them is what happens at the "condition" or "process" step: a fixed rule evaluates it in traditional automation, while an AI model interprets it in AI-assisted automation. Everything else — the event arriving, the trigger firing, the eventual action — stays conceptually the same.

An important design principle follows directly from this: **the IoT device's job is to sense and transmit data reliably. The logic — whether rule-based or AI-assisted — belongs in the automation layer or the external service, not necessarily inside the microcontroller's firmware.** Keeping this separation clean is what allows you to change a decision rule, or swap a threshold check for an AI call, without touching the code running on the ESP32-S3 at all.

---

## n8n as the Automation Layer

**n8n** is a workflow automation platform. Instead of writing a full backend program to receive, process and forward data, you assemble a workflow visually from connected **nodes**, where each node performs one step: receiving data, transforming it, checking a condition, calling an external service, or sending a message.

Two trigger types matter most for the workflow you will build in this module:

- A **Webhook trigger** gives your workflow a unique URL. When something sends an HTTP request to that URL, the workflow starts, and the request's data becomes available to the following nodes. This is exactly how your ESP32-S3 will start a workflow: by sending an HTTP request to it.
- A **Schedule trigger** starts a workflow at fixed time intervals instead of in response to an external request, useful for periodic checks rather than event-driven ones.

Once a workflow has started, an **HTTP Request node** lets it call out to another API — including an LLM API — by sending a request and capturing the response, and passing that response along to the next node in the workflow (for example, one that sends a notification).

```text
[Webhook Trigger] → [Condition check] → [HTTP Request: call LLM API] → [Send notification]
```

A detail worth remembering from the very start: **API keys and other secrets are never placed directly inside a workflow's visible nodes.** n8n keeps this kind of information in a separate credentials store, referenced by the node rather than written into it. This mirrors a rule you will also apply on the device side.

Because n8n is under active development, the exact names of nodes, the options available on them and the details of the interface can change between versions. Treat the node names above as a description of the role each step plays, and confirm the current interface against your own installation when you build the workflow.

---

## Connecting the ESP32-S3 to n8n

The ESP32-S3 is not designed to sit and wait for incoming requests the way a server does. Instead, the natural direction of communication is for the **device to reach out** to n8n's webhook whenever it has something to report. That means the device makes an **outbound HTTP request**, in the same way a browser requests a web page, except that here it is sending a small JSON payload of sensor data rather than asking for one.

CircuitPython on the ESP32-S3 provides this capability through its built-in `wifi` module for the network connection, `socketpool` for the underlying sockets, and Adafruit's `adafruit_requests` library for a familiar, higher-level way of making HTTP requests.

```python
import wifi
import socketpool
import ssl
import adafruit_requests
import os
import json

# Wi-Fi credentials and the n8n webhook URL are read from settings.toml,
# never written directly into this file.
wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

webhook_url = os.getenv("N8N_WEBHOOK_URL")

payload = {
    "temperature_c": 29.4,
    "humidity_pct": 68,
}

response = requests.post(webhook_url, json=payload)
print("n8n responded:", response.status_code)
response.close()
```

A few things are worth noticing about this code, because they connect directly to habits you should already be building.

The Wi-Fi credentials and the webhook URL never appear as text inside the script. They are read with `os.getenv(...)`, which pulls them from a settings file kept outside the program itself. This is the same principle as keeping secrets out of an n8n workflow: **credentials belong in a separate, protected location, never inside code or configuration that might be shared, copied or version-controlled.**

The payload is a small Python dictionary of **structured data** — a temperature and a humidity value, each clearly labelled. This is deliberate. The device's job stops at reporting a clean, structured measurement. What happens to that measurement — whether it is checked against a threshold, forwarded to an AI service, or both — is entirely the automation layer's responsibility, not the firmware's.

> **Observe.** If you run a version of this code and watch the n8n workflow's execution log, you can see the exact JSON payload arrive at the webhook. Compare it against what your program sent. This is a useful debugging habit for the rest of this module: when a workflow does not behave as expected, check first whether the data that arrived matches the data you believe you sent.

---

## The API Mental Model, Before Adding an LLM

Before bringing a language model into the picture, it is worth being explicit about what an **API** is, at the level this course needs.

An API (Application Programming Interface) is a defined way for one piece of software to ask another piece of software to do something, without needing to know how that other software works internally. The pattern is always the same three-part shape:

```text
Request  →  API  →  Response
(you send structured data)   (the service processes it)   (you receive structured data back)
```

You have already used this pattern, perhaps without naming it: sending an HTTP POST request to an n8n webhook and getting a status code back *is* an API interaction. An LLM API works on exactly the same shape — you send a request, usually as JSON, and you receive a response, also usually as JSON, containing the result. What differs is *what* is inside the request and the response, and that is the subject of the next section.

---

## GenAI + IoT: Sending Sensor Data to an LLM

A **Large Language Model (LLM)** is designed to work with natural language: it takes text in and produces text out. A raw sensor reading like `29.4` is not, by itself, something an LLM can meaningfully "understand" — it is just a number. The useful step in an AIoT workflow is turning structured sensor data into a **natural-language prompt** before it is sent to the model.

```text
Structured sensor data          →   Natural-language prompt              →   LLM API
{"temperature_c": 29.4,             "The temperature is 29.4°C and              (generates a
 "humidity_pct": 68}                 humidity is 68%. Is this               response)
                                     unusual for an indoor room,
                                     and should anyone be alerted?"
```

Inside an n8n workflow, this is typically done with a node that builds a short piece of text from the incoming JSON fields, and then an HTTP Request node sends that text to the LLM API's endpoint. The response that comes back is natural-language text — for example, a short explanation and recommendation — which can then be forwarded to a notification node (an email, a chat message, a log entry) as a **human-readable alert**.

The exact request format, endpoint address and authentication method depend entirely on which LLM provider your course setup uses, and these details change over time as providers update their APIs. For that reason, this reading does not specify a particular provider's request format — you should build your workflow against whatever provider and documentation your course setup specifies, keeping the provider itself a configurable detail of the workflow rather than something hardcoded into your thinking about the pattern.

What *is* stable, regardless of provider, is the role the LLM step plays in the pipeline: it takes a natural-language description of a situation and returns a natural-language interpretation of it. The rest of the workflow — the trigger, the JSON handling, the eventual notification — stays exactly the pattern you have already learned.

Putting the whole pipeline together, one full AIoT workflow for this module might look like this:

```text
ESP32-S3 reads temperature & humidity
        │  (HTTP POST, JSON payload)
        ▼
n8n Webhook Trigger receives the event
        │
        ▼
n8n builds a natural-language prompt from the JSON fields
        │
        ▼
n8n HTTP Request node calls the LLM API
        │
        ▼
n8n receives the LLM's natural-language response
        │
        ▼
n8n sends a human-readable alert (notification, log, message)
```

> **Apply.** Sketch this same pipeline for a different sensor condition than temperature and humidity — for instance, a light level from an LDR, or a distance reading. What would the natural-language prompt say? What kind of response would be useful to a person receiving the alert?

---

## Why AI Output Needs a Human in the Loop

An LLM's response is generated, not looked up. It is built by predicting plausible text, which means it can be genuinely useful and, at the same time, occasionally confident and wrong — a well-documented behaviour usually called **hallucination**. A response that reads fluently and sounds authoritative is not automatically a response that is factually correct.

This matters directly for an AIoT workflow. If an LLM interprets a sensor pattern as "this indicates a cooling system fault," that sentence is a **generated interpretation**, not a verified diagnosis. Treating it as ground truth — especially if it were wired directly into an automatic, irreversible action — would be a design mistake.

A few practical safeguards follow from this, and they are worth building into any AIoT workflow you design in this module and beyond:

- Prefer **low-risk actions** for AI-generated output, such as notifications a person reviews, rather than direct, irreversible control of an actuator.
- Keep the **raw sensor data and the AI's interpretation both visible**, so a person can check the AI's reasoning against the actual numbers rather than trusting the summary blindly.
- Treat AI-generated text as a **draft or recommendation**, phrased that way in the notification itself ("Possible concern, please review" rather than "Fault detected").

This is not a reason to avoid AI in an IoT system — it is a reason to place it deliberately, at the stage where a wrong or oddly phrased answer causes the least harm, with a human positioned to catch it before anything irreversible happens. This idea will be developed further later in the course when reliability is treated as a topic in its own right; for now, the key habit is simply not to let a fluent sentence stand in for a checked fact.

---

## Choosing Between a Rule and an AI Call

With both approaches now on the table, it is worth comparing them directly, because a working AIoT system usually mixes the two rather than replacing one with the other.

| Situation | Rule-based check | AI-assisted interpretation |
|---|---|---|
| Behaviour needs to be identical every time | Well suited — deterministic | Poorly suited — output can vary |
| A single, clear threshold defines the condition | Well suited, and cheaper/faster | Unnecessary overhead |
| Several variables interact in ways hard to encode as one rule | Becomes complex and brittle | Well suited |
| A human-readable explanation is the goal, not just a flag | Requires manually written messages | Well suited |
| The action is safety-critical or irreversible | Preferred, for predictability | Needs strong human oversight if used at all |
| Network/API access may be unavailable | Works offline, on the device | Depends on connectivity to the AI service |

A well-designed AIoT workflow typically keeps a simple rule-based condition as the trigger for whether to *involve* AI at all (for example, only calling the LLM when a temperature is already outside a normal range), and reserves the AI step for producing the interpretation or explanation once that condition is met. This keeps the deterministic, auditable part of the system doing what it does best, and uses the generative part only where flexibility and natural language genuinely add value.

---

## Bringing It Together

The system you are building in this module does not discard anything from earlier ones. The ESP32-S3 still senses; CircuitPython still reads the sensor and sends the data onward; the physical loop of Sense → Compute → Actuate is still there. What has been added is a second computational stage, sitting between the device and the final action, made up of an automation platform that recognises events and manages workflows, and an AI service that can turn a structured reading into an interpreted, natural-language response.

Understanding AIoT, in the sense this reading has built it, means being able to point to each of these stages separately — sensing, automation, AI interpretation, action — and to say plainly what each one is responsible for, and what it is not. That separation is also what will let you debug the system later: if an alert never arrives, you will know to check whether the device sent the request, whether n8n's trigger fired, whether the LLM call succeeded, or whether the notification step failed, rather than treating the whole pipeline as one opaque block.

---

## References

1. n8n. *Official Documentation* (workflow concepts, Webhook trigger, HTTP Request node, credentials management). https://docs.n8n.io
2. CircuitPython documentation. *wifi – WiFi driver* and *socketpool – Socket pool support*. https://docs.circuitpython.org/en/latest/shared-bindings/wifi/ and https://docs.circuitpython.org/en/latest/shared-bindings/socketpool/
3. Adafruit Learning System. *CircuitPython Requests* (`adafruit_requests`, making HTTP requests over Wi-Fi from an ESP32-S3). https://learn.adafruit.com/adafruit-circuitpython-requests
4. Adafruit CircuitPython documentation. *Settings and secrets via `settings.toml`* (keeping Wi-Fi credentials and other secrets out of source code). https://docs.circuitpython.org
5. General IoT automation and event-driven architecture principles (event, trigger, condition, action pattern); widely established software design concepts rather than a single citation.
6. General synthesis from widely recognized IoT/AI systems literature on the concept and architecture of AIoT; no single canonical standard defines the term.
7. General AI reliability and safety literature on generative model limitations, including hallucination and the need for human oversight in AI-assisted decision pipelines.

> **Note.** The exact LLM provider, request format and endpoint used in your hands-on workflow depend on the service specified in your course setup, and this reading deliberately avoids assuming one. Node names and interface details in n8n may change between versions; confirm them against your own installation. Never place API keys, Wi-Fi passwords or webhook URLs directly inside source code or a visible workflow node — keep them in your device's settings file and n8n's credentials store respectively.