# Module 4 — GenAI & Embedded Vision
## Seeing the World: Cameras, Vision AI and Reliable Automated Decisions

**Course:** Applied IoT
**Module:** 4 — GenAI & Embedded Vision

---

## From Automated Decisions to Automated Sight

Across this course you have built a consistent pattern: a sensor produces a number, your program interprets it, and an actuator or notification responds. A potentiometer produces a voltage. A DHT11 produces a temperature and a humidity. Even when you brought in an LLM to help decide what an alert should say, the input to that decision was still a small, structured piece of data — a temperature, a distance, a motion flag.

This reading introduces a sensor that breaks that pattern completely: the **camera**. A camera does not hand your program a single number. It hands your program a picture — tens of thousands of pixel values with no built-in meaning. Getting from that picture to a decision your system can act on requires several new stages, and each stage introduces its own kind of uncertainty.

The path for this reading is:

```text
Camera → Image capture → JPEG encoding → Send to Vision AI → Interpretation → Validation → Decision → Action
```

By the end, you will understand not just how to get a picture out of a camera and a sentence out of an AI model, but how to build a system around that AI model that does not simply trust it blindly — because unlike every sensor you have used so far, a vision AI model has no datasheet, no accuracy tolerance and no guarantee that the same picture will always produce the same answer.

---

## Part 1 — Embedded Vision: The Camera as an IoT Sensor

### A Sensor That Doesn't Return a Number

Think back to how you read the sensors earlier in this course. A digital sensor gave you `True` or `False`. An analog sensor gave you a single integer from the ADC. Even a more complex sensor like the DHT11 gave you exactly two numbers. In every case, the sensor did the hard part — turning a physical effect into a clean, structured value — and your program only had to read it.

A camera is different. What it produces is a **two-dimensional array of pixel data**: a grid of brightness or colour values, one for every point in the image, with no built-in interpretation of what any of it means. A pixel value of 200 does not tell you "there is a person here" the way a `True` from a button tells you "the button is pressed." The structure a normal sensor gives you for free — this number *is* the light level, this number *is* the temperature — simply does not exist for an image. Turning pixels into meaning is a whole additional step, one this reading spends most of its time on.

This is the first big idea of **embedded vision**: using a camera as a sensor inside an embedded system, where the "reading" is not a value but a scene, and where extracting anything useful from that scene takes real processing, either on the device, in the cloud, or (as you will see) with the help of an AI model.

### The Image Acquisition Pipeline

Before any interpretation can happen, the image has to be captured and made available to your program. A camera sensor sits at the front of a short pipeline:

```text
Sensor exposure  →  Raw pixel capture  →  (optional) on-sensor compression  →  Frame buffer in memory  →  Available to your program
```

- **Exposure.** The camera's sensor chip is briefly exposed to light, much like exposing a strip of film, and converts the light hitting each of its tiny elements into an electrical value.
- **Raw pixel capture.** Those values are read out row by row into a buffer of pixel data.
- **On-sensor compression (optional).** Many camera sensor chips used in embedded systems, such as the OmniVision OV2640 and OV5640 families commonly paired with ESP32-S3 boards, include a hardware JPEG encoder built into the sensor itself. This means the microcontroller does not always have to compress the image in software — the sensor can hand over an already-compressed JPEG frame.
- **Frame buffer.** The finished frame, whether raw pixel data or JPEG, is placed into memory where your CircuitPython program can access it.

> **Board dependency.** Not every ESP32-S3 board has a camera. Camera capability depends on the specific board having a compatible sensor wired to the ESP32-S3's camera interface. Which sensor chip your board uses, what resolutions and formats it supports, and how it is wired are all specific to your actual hardware — always confirm these against your board's documentation rather than assuming they match another board.

### Capturing a Frame in CircuitPython

CircuitPython provides a module specifically for this kind of camera hardware, called `espcamera`, for use on ESP32/ESP32-S3 boards that have a camera sensor connected. The shape of the code, in outline, looks like this:

```python
import board
import espcamera

camera = espcamera.Camera(
    data_pins=board.CAMERA_DATA,          # names are board-specific
    pixel_clock_pin=board.CAMERA_PCLK,
    vsync_pin=board.CAMERA_VSYNC,
    href_pin=board.CAMERA_HREF,
    pixel_format=espcamera.PixelFormat.JPEG,
    frame_size=espcamera.FrameSize.QVGA,
)

frame = camera.take(1)   # capture one frame
```

Do not treat the pin names above as universal — `board.CAMERA_DATA` and similar names exist only if your specific board defines them, and the exact set of parameters you need depends on your sensor and board wiring. What matters conceptually is the pattern: you configure the camera once (telling it what format and size of image you want), and then you call a method to `take()` a frame, which becomes available in memory as a sequence of bytes, ready for the next stage of the pipeline.

**Prediction check.** If `pixel_format` is set to `JPEG`, is the microcontroller or the camera sensor doing the compression work? What would change if you set it to a raw pixel format instead?

---

## Part 2 — From Pixels to a File: JPEG and Image Data

### Why Compress at All

A single uncompressed frame from a camera can easily be hundreds of kilobytes, even at a modest resolution — far larger than the sensor readings you have worked with, which fit in a few bytes. An ESP32-S3 has limited memory, and sending a full uncompressed image over Wi-Fi would be slow and would strain both the microcontroller's memory and the network connection. Something has to shrink that data before it goes anywhere.

### JPEG in the Pipeline

**JPEG** is a widely used, lossy image compression standard. "Lossy" means it does not preserve the image perfectly — it discards some detail that the human eye is unlikely to notice, in exchange for a much smaller file. A photograph that might be several hundred kilobytes uncompressed can often shrink to a few tens of kilobytes as a JPEG, while still looking essentially the same to a viewer.

JPEG is the natural choice for an embedded vision pipeline for a few concrete reasons:

- **The sensor may do the work for you.** As mentioned above, many camera sensor chips include hardware JPEG encoding, so the compression happens without spending microcontroller cycles on it.
- **Smaller size means less memory and less bandwidth.** A compressed frame is easier to hold in the ESP32-S3's memory and far faster to transmit over a network connection.
- **It is a nearly universal format.** Web APIs, cloud AI services and ordinary image viewers all accept JPEG without any special handling.

The trade-off is quality. JPEG compression has a quality setting: a lower quality setting produces a smaller file but discards more detail. For most embedded vision purposes this is a reasonable trade, but it is worth remembering when the next stage of your pipeline is an AI model trying to interpret the picture — a heavily compressed, blurry image gives the model less to work with, exactly like handing a person a low-resolution photo and asking them to describe it.

> **Assumption.** Exact JPEG quality settings available through your board's camera library, and whether they are adjustable from CircuitPython, depend on your specific sensor and library version. Confirm against your camera library's documentation before relying on a particular setting.

With a captured, JPEG-encoded frame sitting in memory, you now have something you can actually send somewhere — which is exactly what the next stage of the pipeline does.

---

## Part 3 — Vision AI: Asking a Model What It Sees

### Multimodal AI

You have already used an LLM API earlier in this module to help generate or interpret text-based alerts. A **vision-capable LLM**, sometimes called a **multimodal model**, extends the same idea to images: it can accept a picture as input, alongside or instead of text, and produce a natural-language response about what the picture shows. You are not writing code that detects edges or shapes yourself — you are asking a trained model to describe or answer a question about the image, the same way you might ask a person "what do you see in this photo?"

### Getting the Image to the Model

An AI service running in the cloud cannot directly reach into your microcontroller's memory. The image has to be transmitted, and the common pattern for doing this is:

```text
JPEG bytes  →  Base64-encode  →  Embed in an HTTP request (e.g. JSON body or data URI)  →  Send to the AI API
```

**Base64** is a way of representing binary data (like JPEG bytes) as plain text, using only printable characters. This matters because many web APIs expect their request bodies to be text-based JSON, not raw binary, so the image is converted to a text-safe form before being placed inside the request. CircuitPython provides a `binascii` module with functions for exactly this kind of conversion:

```python
import binascii

jpeg_bytes = bytes(frame)
encoded_image = binascii.b2a_base64(jpeg_bytes)
```

The resulting text can then be placed into an HTTP request to a vision AI API, using the same kind of `adafruit_requests`-based networking you have used for other LLM and automation calls earlier in this module. The exact request format — whether the image goes into a JSON field, a data URI, or elsewhere — depends entirely on which AI service you are using, so this must be confirmed against that service's own documentation. What stays constant across services is the underlying idea: **the image travels as encoded text inside a normal web request, not as a special "image protocol."**

> **Keep credentials out of your code.** Whatever service you send images to will require an API key. As with the LLM APIs you used earlier in this module, that key must never be hard-coded into a script you might share or commit — keep it in a place your code reads at runtime, separate from the source itself.

### What "Understanding" Means Here

On the receiving end, the AI service decodes your image and passes it through a trained model — commonly built around a vision transformer or a convolutional neural network — that turns the picture into internal feature representations. From those, the model generates a natural-language answer to whatever question you asked about the image. It is worth being precise about what is happening: the model is not running a fixed formula on the pixels the way a traditional image-processing algorithm (edge detection, thresholding, colour matching) does. A traditional algorithm is deterministic — given the same image and the same parameters, it produces the same output every time. A vision-capable LLM's response is generated **probabilistically** — it is inferring a plausible answer, and asking the same question about the same image twice will not always guarantee the exact same wording, or even the exact same conclusion.

This is the key distinction to hold onto for the rest of this reading:

| | Structured sensor data (e.g. temperature) | Image data sent to Vision AI |
|---|---|---|
| Form | A single number or short set of numbers | A large, unstructured grid of pixel values |
| Meaning | Built in, defined by the sensor's calibration | Requires interpretation — no meaning until processed |
| How it is produced | Fixed physical measurement, within known accuracy | AI-generated answer, produced probabilistically |
| Repeatability | Same conditions → same reading, within tolerance | Same image → not guaranteed to give an identical answer |

A temperature sensor's number is precise and low-bandwidth, with an unambiguous meaning stated on a datasheet. An image is exactly the opposite: high-bandwidth, unstructured, and meaningless until something — traditional code or an AI model — interprets it. That difference is the reason the next part of this reading exists.

---

## Part 4 — AI Reliability: Trusting an Uncertain Sensor

### Why AI Output Is Not a Measurement

Every sensor you have used so far came with an implicit contract: a stated accuracy, a known range, a documented behaviour under known conditions. Even when a reading was imperfect, you could reason about *how* imperfect it was likely to be, because a datasheet told you.

A vision AI model's response has no such contract. It is generated text, produced by a model that is, at its core, predicting a plausible answer rather than computing a guaranteed one. This produces a well-known and well-documented limitation of generative AI systems: **hallucination**, where a model states something confidently and fluently that is simply wrong. Unless the specific AI service you are using explicitly returns some kind of confidence or similarity score, a plain natural-language answer carries no calibrated indication of how sure the model actually is.

This leads to a rule worth treating as strict as the one you learned about raw sensor readings earlier in this course:

> **An AI-generated interpretation of an image is not a measurement. It is a probabilistic guess, and it must be treated that way in your system's design.**

### Where Vision AI Goes Wrong

Vision AI errors tend to come from a small set of recurring causes, most of which you can influence:

- **Poor image quality** — heavy JPEG compression, low resolution, motion blur or poor lighting all give the model less to work with.
- **Poor framing** — an object partially out of frame, or at an odd angle, is harder to identify correctly.
- **Objects underrepresented in training** — a model trained mostly on everyday photographs may struggle with unusual objects, uncommon angles, or specialised equipment.
- **Vague or ambiguous prompts** — asking "what is in this picture?" invites a broad, less useful answer compared with a specific question like "is there a person standing in the doorway?"

**Troubleshooting thought.** If a vision AI system in the field starts giving noticeably worse answers than it did during testing, what would you check first: the prompt you are sending, the camera's exposure and framing, or the network connection? Which of these would you check *first*, and why?

### Designing Safeguards Around AI-Generated Decisions

Because AI output cannot be trusted the way a calibrated sensor reading can, a system that lets AI output influence anything physical needs a **validation step** between "the AI said X" and "the system does Y." A few practical strategies, often used together:

- **Cross-check against another sensor.** If the AI reports "motion detected in the image" and a separate PIR or ultrasonic sensor also indicates something nearby, the agreement between two independent sources is far more trustworthy than either alone.
- **Require a minimum match in the response.** Rather than acting on any AI reply, check that the reply contains a clear, expected keyword or phrase before treating it as a positive result, and treat an unclear reply as "no result" rather than guessing.
- **Human-in-the-loop confirmation.** For consequential actions — unlocking something, shutting down equipment, sending an urgent alert — route the AI's interpretation to a person for a final confirmation before the action executes, rather than letting the AI trigger the action directly.

This is the same idea you have already met with rule-based automation and AI-assisted decision-making earlier in the course, pushed one step further: the less deterministic and less bounded the input, the more deliberate the validation around it needs to be.

---

## Part 5 — Integration: Building the End-to-End AIoT Pipeline

### Separating the Stages

Bringing a camera and an AI model into an IoT system multiplies the number of things that can go wrong, which makes it more important, not less, to keep the pipeline's stages clearly separated:

```text
1. Image capture        (ESP32-S3 + camera)
2. Image encoding        (JPEG, in the sensor or on the microcontroller)
3. Network transfer      (HTTP request to an automation layer or AI API)
4. AI inference          (vision-capable model produces an interpretation)
5. Decision logic         (validation, combining sources)
6. Action                 (notification, actuator, or automation)
```

Keeping these separate means you can test and debug each one independently. If the system misbehaves, you can ask exactly where: did the camera capture a usable image? Did the request reach the AI service? Did the AI's answer get parsed correctly? Did the decision logic apply the validation you intended? This mirrors the same debugging discipline you have used throughout the course, applied to a longer chain.

### Combining Camera + Sensor Before Deciding

A recurring, useful pattern in vision-based IoT applications is to **not rely on the camera alone**. Combining the AI's interpretation of an image with an independent sensor reading — a motion sensor, a door contact, a temperature threshold — gives you two largely independent pieces of evidence. If they agree, you can act with more confidence. If they disagree, that disagreement itself is useful information: it tells you the situation needs a closer look rather than an automatic response.

### An Example System

A representative structure for this kind of integrated system, using the tools you have already worked with across this course, looks like this:

```text
Camera + Sensor  →  ESP32-S3 (CircuitPython)  →  Vision AI API  →  n8n workflow  →  Notification / Action
```

The ESP32-S3 captures an image and reads a sensor value, sends the image to a vision AI service for interpretation, and passes the result — along with the sensor reading — into an **n8n** workflow. n8n, which you have already used for automation earlier in this course, is well suited to the decision and action stages here: it can apply conditional logic to the combined information, and route the outcome to a notification service (email, Telegram, or similar) or another automated action, without you having to write that orchestration logic on the microcontroller itself.

### Designing the Decision Logic

The decision stage is where validation actually happens in code. Here is the shape of that logic, written to make the validation step explicit rather than acting on the AI's answer alone:

```python
image_bytes = capture_and_encode_image()          # Part 1 and Part 2
ai_reply = ask_vision_ai(image_bytes, question="Is there a package on the doorstep?")

motion_detected = motion_sensor.value             # an independent sensor reading

if "yes" in ai_reply.lower() and motion_detected:
    trigger_action()          # both sources agree — act
elif "yes" in ai_reply.lower() and not motion_detected:
    log_for_review(ai_reply)  # AI says yes, sensor disagrees — do not act automatically
else:
    pass                      # AI says no — no action
```

Notice what this code deliberately avoids: it never lets `ai_reply` alone trigger `trigger_action()`. The motion sensor's independent, deterministic reading has to agree before the system treats the situation as confirmed. When the two disagree, the safer choice is to log the case for a person to review rather than to guess which source is right — a small, concrete example of the human-in-the-loop principle from Part 4.

**Design question.** Suppose you wanted this system to send an unattended notification only when it was fairly confident, but to always ask for human confirmation when the AI's answer and the sensor disagreed. Where in the code above would that split happen, and what would you need to check to decide which branch to take?

---

## Bringing the Module Together

Across this module you have followed one continuous thread, widening at each step:

```text
IoT  →  AIoT  →  Automation  →  GenAI  →  Embedded Vision  →  Vision AI  →  Reliable AI  →  Integrated AIoT System
```

You began with the familiar Sense → Compute → Actuate loop, then let an LLM help generate decisions and alerts from structured sensor data. This reading extended "sense" to include a camera, extended "compute" to include a vision-capable AI model interpreting unstructured images, and — most importantly — insisted that "actuate" should never happen directly off an AI's raw answer. The system you now know how to design captures a picture, encodes it efficiently, sends it for interpretation, treats that interpretation as a probabilistic guess rather than a measurement, checks it against other evidence, and only then acts.

That last habit — validating before acting — is not a limitation specific to cameras or to this module. It is the general shape of any system that lets AI influence the physical world, and it is the idea this reading most wants you to carry forward.

---

### References

1. Adafruit / CircuitPython documentation. *espcamera – ESP32 and ESP32-S3 camera support* (`Camera`, `PixelFormat`, `FrameSize`, `take`). https://docs.circuitpython.org/en/latest/shared-bindings/espcamera/
2. CircuitPython documentation. *binascii – Binary/ASCII conversions* (`b2a_base64`, for encoding image bytes as text). https://docs.circuitpython.org/en/latest/shared-bindings/binascii/
3. ISO/IEC 10918 (JPEG). *Digital compression and coding of continuous-tone still images* — the standard defining lossy JPEG compression.
4. n8n. *Official documentation* (workflow nodes, HTTP requests, conditional logic, notification integrations). https://docs.n8n.io/
5. General multimodal LLM API pattern, consistent with major vendor documentation on image input as base64/data URIs in HTTP request bodies. Exact request/response format depends on the specific vision AI provider used in your course setup — always confirm against that provider's own API documentation.
6. General principles of AI reliability and human-in-the-loop system design, consistent with widely documented limitations of generative AI models (probabilistic output, hallucination, absence of a fixed error bound).

> **Note.** Camera sensor models, supported resolutions, pin names and available image formats depend entirely on your specific board and are not stated here as fixed facts — confirm them against your board's own documentation before writing camera-configuration code. Similarly, the exact request format, size limits and any confidence-related fields for your vision AI service depend on the provider you use, and must be checked against that provider's documentation rather than assumed from this reading.