# Digital Signals: Reading Inputs and Controlling Outputs

---

## From Running Programs to Building Interactions

In the previous lesson, you set up your ESP32-S3 environment in **Wokwi** and ran your first programs in **Arduino C/C++**. You did that by following a recipe: set a pin as an output, then switch it HIGH and LOW to make an LED blink. This lesson turns that recipe into understanding.

We will look closely at what a **digital signal** actually is, and how a program uses one to *control* something in the physical world. Then we reverse the direction, and let the physical world *talk to* the program, using a button. Finally, we connect the two, so that pressing a button changes what an LED does:

```text
Digital states → GPIO output → Control an LED → GPIO input → Read a button → Make a decision → Control an output
```

That final connection is a complete, tiny IoT system: it senses something, decides something and does something. It is the same **Sense → Compute → Actuate** loop you learned at the beginning of the course, now built with your own hands and your own code.

### What You Will Be Able to Do After This Lesson

- Explain what a digital signal represents, and distinguish between the HIGH and LOW states — and between a digital and an analog signal.
- Explain the difference between a digital input and a digital output, from the microcontroller's point of view.
- Configure a GPIO pin as a digital output, and use it to control an LED, or several, as in a simple traffic light.
- Explain why a digital input needs a pull-up or pull-down resistor, and configure a GPIO pin as a digital input using the ESP32-S3's built-in pull resistors.
- Use the state of a button input to make a decision that controls an output.
- Describe the complete flow from a physical input to a software decision to a physical output.

> **How to read the labels in this material.** As before:
> - **Teaching model** — a simplification that is useful for thinking but not the full truth.
> - **Example values** — numbers chosen to make a calculation clear. Real parts vary, and the documentation of your actual board always wins.
> - **Assumption** — something this lesson assumes because it depends on your specific hardware or setup.

> **Assumptions for this lesson.**
> - **Pins and tool.** This lesson's experiments run in the **Wokwi** simulator, on an **ESP32-S3** board, programmed in **Arduino C/C++**. The example code uses concrete pin numbers — GPIO 4 for an LED and GPIO 7 for a button — to keep the wiring and the code consistent throughout. If you wire your own circuit on different pins, use your own numbers instead.
> - **Parts.** The experiments use an LED with a series resistor and a push button, added as parts in Wokwi, which you have already used in earlier lessons. A slide switch or toggle switch behaves the same way as a button.
> - **Values.** Voltage figures in this lesson for the chip's pins come from Espressif's ESP32-S3 datasheet for a 3.3 V supply. Your board's documentation is the final authority for real hardware.
> - **Scope.** Analog signals, varying brightness, communication with sensors, and techniques for making button inputs fully reliable — such as debouncing — are covered in later lessons. Here we keep to simple, level-based on/off signals.

---

# The Digital World

## Physical States and Their Digital Representation

Look around you and notice how many things have two states. A light is on or off. A door is open or closed. A switch is up or down. A button is pressed or not pressed. A tank is full or not full.

These are **physical states**: real conditions in the physical world. A microcontroller cannot look at a door. It can only work with **electrical signals**. To use a physical state in a program, we need a way to *represent* it, as an electrical signal that a chip can measure and a program can use.

That representation is what makes a signal **digital**. In its simplest form:

- The physical world has some condition of interest with two possibilities (open or closed).
- A circuit turns those two possibilities into two different **voltages**.
- The microcontroller measures the voltage and reports one of **two values** to the program.
- The program treats them as `true` or `false`, or as 1 or 0.

```text
Physical state  ──►  Voltage on a wire  ──►  Digital value  ──►  Value in the program
(door closed)         (about 0 V)             LOW                   false
(door open)           (about 3.3 V)           HIGH                  true
```

The physical state and its digital representation are *not the same thing*. The door is a door. The voltage is a voltage. The `true` in your program is a number stored in memory. The circuit designer decides how one stands for the other, and that choice can be made in more than one way. (A door sensor could be wired so that "open" is LOW instead of HIGH, and you will see why that matters shortly.)

### Binary Thinking

Many decisions in IoT systems are yes-or-no questions:

- Is the door open?
- Was motion detected?
- Is the water tank full?
- Has the button been pressed?
- Should the pump be on?

A system of this kind, with two possible states, is called **binary**. Getting used to *binary thinking* means learning to look at a physical situation and ask, "Which yes-or-no questions do I need answered, and what will each state make the system do?"

Notice that some quantities do not fit this pattern naturally. The temperature of a room is not "hot or cold". It can be any value in a range. Later lessons deal with such continuous quantities. But even then, a decision often ends up being binary. "Is it too hot?" is a yes-or-no question about a continuous quantity, and the answer decides whether a fan turns on or off. Digital thinking is everywhere.

## HIGH and LOW: Two Voltage Levels

A **digital signal** carries information using just **two voltage levels**:

- **HIGH**: a voltage close to the chip's supply voltage. On the ESP32-S3 running at 3.3 V, that means roughly 3.3 V.
- **LOW**: a voltage close to 0 V, the ground level.

You met these terms in the earlier lesson on GPIO. Now let us be more precise about what they mean, because a real voltage is never exactly 3.3 V or exactly 0 V. Batteries sag, wires have resistance, and electrical noise adds small fluctuations. So a digital input does not require exactly 3.3 V to call something HIGH. It has a **range** for each level, with a gap in between.

Espressif's datasheet specifies these ranges for the ESP32-S3 with a 3.3 V supply. With VDD as the supply voltage (3.3 V here):

| | Range | With VDD = 3.3 V |
|---|---|---|
| **Input read as HIGH** | at least 0.75 × VDD | above about 2.5 V |
| **Input read as LOW** | at most 0.25 × VDD | below about 0.8 V |
| **Output guaranteed HIGH** | at least 0.8 × VDD | above about 2.64 V |
| **Output guaranteed LOW** | at most 0.1 × VDD | below about 0.33 V |

```text
 3.3 V ┤ ███████  the pin can output a HIGH here (≥ about 2.64 V)
 2.5 V ┤ ███████  an input reads HIGH above about 2.5 V
       │ ░░░░░░░  the undefined zone: the input may read either way
 0.8 V ┤ ███████  an input reads LOW below about 0.8 V
 0.33 V┤ ███████  the pin can output a LOW here (≤ about 0.33 V)
   0 V ┤
```

Look at how the numbers fit together. When the chip outputs a HIGH, it produces at least about 2.64 V, which is comfortably above the 2.5 V that an input needs to read HIGH. When it outputs a LOW, it produces at most about 0.33 V, comfortably below the 0.8 V where an input reads LOW. That margin is deliberate. It means small amounts of noise do not flip a signal from one state to the other.

The zone in between is **undefined**. A voltage of 1.6 V, for example, could be read as either HIGH or LOW, and may change unpredictably. Good digital circuits avoid living there.

> **Teaching model.** For most of this course, "HIGH is about 3.3 V and LOW is about 0 V" is all you need. The ranges above explain *why* it works, and they become important when a signal looks wrong or behaves inconsistently.

### HIGH Does Not Mean "On"

A very common beginner misunderstanding is to think that HIGH means "on" and LOW means "off". This is *often* true, but it is not a rule of nature. **HIGH and LOW describe voltage levels. What they mean is decided by how the circuit is wired.**

- An LED wired between the pin and ground lights when the pin is HIGH.
- An LED wired between the 3.3 V supply and the pin lights when the pin is LOW, because current now flows *into* the pin.
- A button wired to ground with a pull-up reads LOW when pressed.

You already met that last case, called **active-low** behaviour: the "active" (pressed) state is LOW. The physical state, the voltage and the program's value are three different things, connected by the circuit. Keeping that in mind will save you from many confusing moments.

## Digital Signals in IoT Systems

Digital signals appear throughout IoT hardware. Here are a few places you will meet them:

| Signal | Physical state | Direction (from the microcontroller) |
|---|---|---|
| Push button | Pressed / not pressed | Into the microcontroller (input) |
| Door or window sensor | Open / closed | Input |
| Many motion-detector modules | Motion detected / not detected | Input (check the module's documentation) |
| Indicator LED | Lit / dark | Out of the microcontroller (output) |
| A transistor or relay control line | Load on / off | Output |

There is one more use worth previewing. Chips also talk to each other by sending rapid sequences of HIGH and LOW levels, which is how many sensors, displays and networks communicate. That uses exactly the same idea, a wire switching between two voltage levels, but at high speed and with agreed patterns. Later modules build on this. For now, notice how much can be done with a single wire and two states.

> **Try it: Observe and identify digital states.** Look around the room, and choose five devices or situations. For each one:
> 1. Describe the physical state and its two possibilities (for example, "lift door: open or closed").
> 2. Say what kind of electrical signal might represent it.
> 3. Decide whether it is an input to a control system (something the system needs to *know*) or an output (something the system *does*).
> 4. Find at least one example where the *underlying* quantity is not really two-valued, such as the brightness of a room, but where a yes-or-no question about it might still be useful. What is that question?

### Digital vs Analog: Two Ways to Represent a Signal

Everything so far has used a signal with exactly **two** possible values, HIGH or LOW. That is a **digital signal**. Not every physical quantity fits neatly into two states, though. The brightness of a room, the temperature of a cup of tea, the distance to a wall — these can take any value in a continuous range, not just two. A signal that can take any value in a range, not just two fixed ones, is called an **analog signal**.

```text
Digital signal:   ▔▔▔▔╱‾╲______╱‾‾‾‾╲___       only ever HIGH or LOW
Analog signal:    ╱╲__╱‾╲___╱‾╲╱‾╲___╱╲       any value in between
```

A digital input pin only ever reports one of two states, HIGH or LOW, however you wired the circuit. To read a genuinely continuous voltage — for example, from a sensor whose output varies smoothly with light or temperature — a microcontroller needs a different kind of circuitry, one that can measure a varying voltage and turn it into a number. That circuitry, and the sensors that produce analog signals, are the subject of a later lesson. For now, the important idea is simpler: **a digital signal is a deliberate simplification.** The circuit is designed so that only two voltages are ever meaningful, which is exactly what makes digital signals so easy to reason about, wire and debug.

## A Digital Signal Experiment in Wokwi

The clearest way to understand HIGH and LOW is to produce them yourself and watch what happens. As in the previous lesson, this course's simulation practicals use **Wokwi**, with an **ESP32-S3** board, programmed in **Arduino C/C++**.

Wire a single LED with its series resistor to one GPIO pin (this lesson uses **GPIO 4**), exactly as you did in the previous lesson:

```text
    GPIO 4 ──[ Resistor ]──►|── GND
                            LED
```

Then run this short program:

```cpp
void setup() {
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);   // about 3.3 V: the LED lights
}

void loop() {
}
```

Start the simulation and observe the LED: it lights, and stays lit, because the pin is left HIGH. Now change `HIGH` to `LOW`, restart the simulation, and observe that the LED stays dark. You have just produced, and observed, the two voltage levels this whole lesson is about. Nothing else in this program matters yet — `loop()` is left empty on purpose, so the pin's state does not change after `setup()` runs once.

> **Try it: Predict, then test.** Before running the program: what voltage do you expect on GPIO 4 when it is HIGH? When it is LOW? Watch the LED in Wokwi, then explain in one sentence what "HIGH" and "LOW" mean in terms of the wire's voltage, not just "on" and "off".

---

# Digital Output: Code Controls the Physical World

## The Output Direction

Recall that every GPIO pin has a **direction**, which your program chooses. When the pin is an **output**, the program is in charge, and the signal flows from the microcontroller to the component:

```text
Microcontroller  ──── signal ────►  Component (LED, transistor, relay…)
   (program decides)
```

Remember that "input" and "output" are always defined from the **microcontroller's point of view**. An LED is an *output device* because the microcontroller sends a signal *out* to it.

When your program sets the value of an output pin, the chip does something simple and physical inside:

- **Setting the pin HIGH** connects it, inside the chip, to the supply voltage. The pin now sits at about 3.3 V, and can push a small current out.
- **Setting the pin LOW** connects it, inside the chip, to ground. The pin now sits at about 0 V, and can let a small current flow in.

So an output pin is like a tiny switch, controlled by your program, that connects a wire either to the supply or to ground. That is the whole trick. All the "intelligence" is in the *program* deciding when to flip it.

### What a Pin Can and Cannot Do

An output pin is a signal source, not a power supply. Everything you learned about power and current applies. An indicator LED with a series resistor draws a few milliamperes, a light load for a pin. A motor, a pump or a strip of many LEDs draws far more, and must be switched through a transistor or a driver module, as you saw earlier.

> **Assumption.** Espressif's datasheet lists current figures for the chip's pins, but they apply under specific test conditions and settings, and are not targets to aim for. In this course, keep loads on GPIO pins small, use indicator-level currents for LEDs and always use a series resistor. If you are unsure whether a component can be connected directly to a pin, check its datasheet first.

## Controlling an LED from Code

You already wired an LED to GPIO 4 in the digital signal experiment, and watched it light up when the pin went HIGH. Now let us look closely at the code pattern behind that, because you will reuse it constantly.

Every GPIO program in Arduino C/C++ follows the same short pattern:

```text
1. Choose the pin                    #define LED_PIN 4
2. Set its direction                 pinMode(LED_PIN, OUTPUT);
3. Use it                            digitalWrite(LED_PIN, HIGH);   or   digitalWrite(LED_PIN, LOW);
```

We can call this the **basic GPIO workflow**: *choose, configure, use*. You will follow it for every digital input and output you write.

Here is how each line of the program you already ran connects to the physical world:

- `#define LED_PIN 4` gives a name to the pin number, so the rest of the program reads clearly and the pin is easy to change from one place.
- `pinMode(LED_PIN, OUTPUT)` tells the chip: *this pin will send signals out.*
- `digitalWrite(LED_PIN, HIGH)` sets the pin HIGH. About 3.3 V appears on the pin, current flows through the resistor and LED, and the LED lights.
- `setup()` runs once, when the program starts; `loop()` runs afterwards, over and over, forever — here it was left empty, since the LED simply stayed lit.

## Program-Controlled Physical Action

When a program controls an output, it can do far more than switch it on. It decides **when** and **for how long**. That is what makes the action *program-controlled*. Here are two small programs. Read each before running it, and predict what the LED will do.

**A pattern that repeats forever:**

```cpp
#define LED_PIN 4

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(250);
}
```

**The same blink, written using the "opposite" idea:**

```cpp
#define LED_PIN 4

bool ledState = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  ledState = !ledState;
  digitalWrite(LED_PIN, ledState);
  delay(500);
}
```

Both programs blink the LED forever, but the second one tracks the LED's state in a variable and flips it (`!ledState`) instead of writing `HIGH` and `LOW` explicitly. The result looks the same; the technique is different, and you will find the toggle pattern useful once a program has more than one thing to keep track of.

> **Try it: Modify and predict.** Change one thing at a time, predict the result, then test.
> - Change the pattern in the first program to on for 0.1 seconds and off for 2 seconds. How does it look?
> - In the second program, change `delay(500)` to `delay(50)`. What do you expect to see?
> - Use two different `delay()` values in the loop to create a "heartbeat" pattern (two short pulses, then a pause).

### One Program, Different Actuators

Here is something worth noticing. The program does not know what is connected to the pin. It sets a voltage. What the voltage *does* depends on what you connect:

- an LED with a resistor lights up,
- a second LED, wired the same way on a different pin, lights up independently,
- the control input of a transistor or relay circuit can switch a motor or pump on and off.

The code is essentially identical: `digitalWrite(pin, HIGH)` or `digitalWrite(pin, LOW)`. That is the beauty of digital output. A single yes-or-no signal is enough to turn many kinds of actuators on and off, as long as the circuit between the pin and the actuator is right.

## Extending the Idea: A Simple Traffic Light

Nothing about digital output is limited to one LED. A **traffic light** is simply three LED circuits, each on its own GPIO pin, switched HIGH and LOW in a sequence your program decides:

```text
    GPIO 19 ──[ Resistor ]──►|── GND     (red)
    GPIO 21 ──[ Resistor ]──►|── GND     (yellow)
    GPIO 45 ──[ Resistor ]──►|── GND     (green)
```

![Three LEDs wired as a traffic light on the ESP32-S3: red on GPIO 19, yellow on GPIO 21, green on GPIO 45, each through its own resistor to GND](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-12-traffic-light-circuit.png)

> **Assumption.** GPIO 19 and GPIO 20 carry the ESP32-S3's native-USB data lines on real hardware, and GPIO 45 is a strapping pin read at boot — exactly the pins the earlier assumption box told you to avoid "for your first experiments." Wokwi's simulated ESP32-S3 does not use native USB for its own connection to your browser and does not model strapping behaviour, so all three are free to use here. If you rebuild this circuit on physical hardware, check your board's documentation before reusing GPIO 19, 20 or 45 for anything other than this traffic light.

```cpp
#define RED_PIN    19
#define YELLOW_PIN 21
#define GREEN_PIN  45

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  digitalWrite(RED_PIN, HIGH);
  delay(2000);
  digitalWrite(RED_PIN, LOW);

  digitalWrite(GREEN_PIN, HIGH);
  delay(2000);
  digitalWrite(GREEN_PIN, LOW);

  digitalWrite(YELLOW_PIN, HIGH);
  delay(500);
  digitalWrite(YELLOW_PIN, LOW);
}
```

Every idea you have already met is here, just repeated three times: each pin is configured the same way, each `digitalWrite()` call sets a voltage the same way, and each LED lights for exactly the reason the first one did. The only genuinely new idea is **sequencing**: the order and the timing are a decision your program makes, not something the hardware does by itself. Trace it through: HIGH on a pin means about 3.3 V, which drives current through that LED's resistor and lights it; LOW means about 0 V, and that LED goes dark. The traffic light **looks** more complex than a single blinking LED, but every voltage, every current and every light is governed by the same rule you learned with one LED.

> **Try it: Predict, then test.** Before running the program, sketch the sequence you expect to see (which light, for how long). Then run it in Wokwi and check. What would you change to make the red light stay on twice as long as the green light?

### When an Output Does Not Behave

If an output does not do what you expect, use the same order of reasoning you learned in the previous lesson. You are looking for the first point at which reality departs from your prediction:

```text
Is the program running?  ─►  Does the pin change state?  ─►  Is the wiring right?  ─►  Is the component OK?
```

1. Is the program running and reaching the line that changes the pin? (Add a `Serial.println()` and check Wokwi's Serial Monitor.)
2. Does the pin's voltage actually change? Try a minimal sketch that only sets that one pin, to isolate the question.
3. Is the wiring correct, with the resistor in series, the LED the right way round and a shared ground?
4. Is the component healthy? Try a different simulated LED or resistor value.

Isolating the software side from the hardware side this way tells you which one to keep investigating.

---

# Digital Input: The Physical World Talks to Code

## The Input Direction

So far, the signal has flowed *out* of the microcontroller. Now we reverse it. When a pin is configured as an **input**, the physical world is in charge. The signal flows *into* the microcontroller, and the program **reads** it:

```text
Component (button, switch, digital sensor…)  ──── signal ────►  Microcontroller
                                                                 (program reads it)
```

An input pin does not drive anything. It **measures** the voltage on the wire connected to it and reports whether that voltage counts as HIGH or LOW, using the ranges you saw earlier. In effect, it is a very sensitive digital voltmeter. Espressif's datasheet gives the input current of a pin as at most 50 nanoamperes, which is almost nothing. This has two consequences:

- An input pin **cannot power a component**. Connecting an LED to an input pin does nothing, because the pin supplies no current. Inputs *listen*, and outputs *drive*.
- An input pin is easily influenced by whatever is connected to it, or by whatever *is nearby* if nothing is connected. This second point is the key to reading a button correctly.

## Reading a Button

Recall from the earlier lesson on components that a button does not produce a voltage by itself. It only opens or closes a path. If you connect one side of a button to ground and the other to an input pin, the pin reads LOW when the button is pressed, but when the button is released, **the pin is connected to nothing**. It is **floating**, with no defined voltage, and it may read HIGH or LOW at random.

The solution is a **pull-up resistor**: a resistor from the pin to the supply voltage, so that the pin has a default HIGH when nothing else is driving it. A **pull-down resistor** does the opposite, pulling the pin to LOW by default.

### Using the Chip's Built-In Pull Resistors

You do not need to add a separate resistor. GPIO pins on the ESP32-S3 have **internal weak pull-up and pull-down resistors** that the program can switch on. Espressif's datasheet gives their typical value as about 45 kΩ. In Arduino C/C++, this is chosen through the pin's mode:

```cpp
pinMode(BUTTON_PIN, INPUT_PULLUP);
```

This makes the button circuit very simple. Connect one side of the button to the input pin and the other to a **GND** pin, and configure the internal pull-up:

```text
    3.3 V
      │
   [ ~45 kΩ ]        ← inside the chip; enabled by INPUT_PULLUP
      │
      ├────────► GPIO 4 (button pin)
      │
   [ Button ]        ← the only part you wire
      │
     GND
```

Now the behaviour is predictable:

| Button | Pin voltage | Digital state | `digitalRead(BUTTON_PIN)` |
|---|---|---|---|
| Released | About 3.3 V (pulled up) | HIGH | `HIGH` |
| Pressed | About 0 V (connected to GND) | LOW | `LOW` |

This is the **active-low** behaviour: pressing the button makes the pin go LOW. Notice what looks backwards: a pressed button gives `LOW`, not `HIGH`.

Let us use Ohm's Law to check that this is sensible. When the button is pressed, the ~45 kΩ pull-up sits between 3.3 V and ground, so the current is about 3.3 V ÷ 45,000 Ω ≈ 73 µA (microamperes), which is tiny. The pull-up is called "weak" for a reason. It is strong enough to hold the pin HIGH when nothing else is connected, but it wastes almost no energy when the button pulls the pin to ground.

### The Other Way: Pull-Down

You can also wire a button the other way round. Connect one side of the button to **3.3 V** and the other to the input pin, and choose the pull-**down** mode:

```cpp
pinMode(BUTTON_PIN, INPUT_PULLDOWN);
```

Now the released button gives LOW and the pressed button gives HIGH, which feels more natural. Both work. Which one you choose depends on the circuit, and on what the board and other parts already do. The important thing is to know which one *you* have built, because it decides how you interpret the value.

> **Assumption.** This lesson uses a button wired to ground with the internal pull-up, the simplest and most common arrangement. Some pins on some boards may already be connected to on-board resistors or buttons, so check that your chosen pin has no special role. On the ESP32-S3, for instance, Espressif identifies certain pins (GPIO0, GPIO3, GPIO45 and GPIO46) as **strapping pins** that are read at start-up to configure the chip, and the native USB uses GPIO19 and GPIO20. Avoid these for your first experiments, and choose a plain general-purpose pin.

> **Try it: Predict the pin state.** Before wiring, fill in this table on paper for the pull-up arrangement. Then build it in Wokwi, add a `Serial.println(digitalRead(BUTTON_PIN))` inside `loop()`, and check the Serial Monitor.
>
> | State | Predicted pin voltage | Predicted `digitalRead(BUTTON_PIN)` |
> |---|---|---|
> | Button released | | |
> | Button pressed | | |
>
> Then repeat for the pull-down arrangement. Were you surprised by anything?

## Reading the State in Code

Now we write the program. Here is the input version of the GPIO workflow: *choose, configure, use*. There is one extra detail, which is the pull mode.

Wire a push button to **GPIO 4**: one leg to the pin, the other leg to **GND**. No resistor is needed, since the internal pull-up already does that job.

![Push button wired to GPIO 4 on the ESP32-S3, the other leg to GND, ready to read with INPUT_PULLUP](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-10-button-read-circuit.png)

```cpp
#define BUTTON_PIN 4

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  Serial.println(digitalRead(BUTTON_PIN));
  delay(100);
}
```

Here is how it works:

- `pinMode(BUTTON_PIN, INPUT_PULLUP)` configures the pin to *listen*, with the internal pull-up resistor switched on.
- `digitalRead(BUTTON_PIN)` **reads** the pin at that moment. It returns `HIGH` if the pin is HIGH and `LOW` if it is LOW.
- `Serial.println(...)` shows the value in Wokwi's Serial Monitor, since the board has no screen. `delay(100)` makes the program check ten times per second.

Run the program and open the Serial Monitor. You should see a stream of `1` (HIGH) while the button is released, and `0` (LOW) while you hold it down.

A program that keeps checking an input over and over is said to be **polling** it. Polling is the simplest way to watch an input: ask, wait a moment, ask again.

> **Try it: Observe and explain.** With the program running and the Serial Monitor open:
> 1. What do you see when the button is released? Pressed? Does it match your prediction?
> 2. Press and hold the button for about one second. Roughly how many `0` values do you expect to see printed? Why that number?
> 3. What happens if you change `delay(100)` to `delay(2000)` and tap the button quickly? What does that tell you about how often the program looks at the input?

### Translating Electrical States into Meaning

The value `LOW` for a *pressed* button is confusing to read. A common habit is to give the value a name that says what it *means*:

```cpp
bool pressed = (digitalRead(BUTTON_PIN) == LOW);
```

Now `pressed` is `true` when the button is pressed and `false` when it is not. The code carries the same information but reads like a sentence. This is the "digital representation of a physical state" idea from the start of this lesson, turned into code. The pin has a voltage, the voltage becomes the result of `digitalRead()`, and your program turns that into `pressed`, a name for something that matters in the physical world.

## Making a Decision: The Button Controls the LED

We now have all the pieces. We can read an input, and we can control an output. Connecting them means the program makes a **decision**: *if the button is pressed, then the LED is on.*

### Building the Circuit

The LED needs a pin of its own, so move the button from **GPIO 4**, where you just read it, to **GPIO 7**, freeing GPIO 4 for the LED. You now have two separate circuits connected to two separate pins, sharing the board's ground:

```text
     Button circuit                       LED circuit

   GPIO 7 ──┬── [ Button ] ── GND      GPIO 4 ──[ Resistor ]──►|── GND
            │                                                  LED
     (internal pull-up
      switched on in code)
```

![Button on GPIO 7 (INPUT_PULLUP) and LED on GPIO 4 (OUTPUT), both returning to GND](https://s3.ap-south-1.amazonaws.com/new-assets.ccbp.in/frontend/loading-data/niat_java/niat_coding_questions/rm1-11-button-led-circuit.png)

Build it in this order, in Wokwi:

1. **Add the LED and resistor**, and wire them: output pin → resistor → LED anode, LED cathode → GND.
2. **Move the button** from GPIO 4 to GPIO 7, and wire it: one side to the input pin, the other side to GND.
3. **Check** each connection against the diagram. Are the two pins different? Is the LED the right way round?
4. **Start the simulation.**

### The Program

```cpp
#define LED_PIN    4
#define BUTTON_PIN 7

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  bool pressed = (digitalRead(BUTTON_PIN) == LOW);   // true while the button is held down

  if (pressed) {
    digitalWrite(LED_PIN, HIGH);   // button held: LED on
  } else {
    digitalWrite(LED_PIN, LOW);    // button released: LED off
  }

  delay(10);
}
```

Read it as a story. Each time round the loop, the program **senses** the button (`digitalRead(BUTTON_PIN)`), **decides** (`if (pressed)`) and **acts** (`digitalWrite(LED_PIN, ...)`). Then it waits ten milliseconds and repeats, hundreds of times a second.

That short pause gives the processor a breather, and that is all it does here. It is **not** a solution to every reliability problem a mechanical button can cause — later lessons look at those in more depth. For the simple task of following the button's current state, this is enough.

There is a shorter way to write the same logic, since the LED should simply copy the state of the button:

```cpp
digitalWrite(LED_PIN, pressed);
```

The longer `if`/`else` form is easier to *read* and, more importantly, easier to *change*. When you want the LED to do something more interesting than copy the button, the `if` is where you add it.

### Following One Press from Start to Finish

Let us follow a single button press all the way through the system, one step at a time:

```text
1. You press the button.                           PHYSICAL INPUT
2. The button closes; the pin is connected to GND.
3. The pin voltage falls to about 0 V (LOW).        DIGITAL SIGNAL
4. The chip reads the pin: digitalRead returns LOW. MICROCONTROLLER
5. The program sets pressed = true.                 PROGRAM LOGIC
6. The if-branch runs: digitalWrite(LED_PIN, HIGH).
7. The output pin is driven HIGH (about 3.3 V).     DIGITAL OUTPUT
8. Current flows through the resistor and LED.
9. The LED lights.                                  PHYSICAL ACTION
```

This is the full chain of the system, and it is worth reading twice:

```text
Physical Input → Digital Signal → Microcontroller → Program Logic → Digital Output → Physical Action
```

Every IoT system you build in this course, however complex it becomes, follows this same shape.

> **Try it: Predict, then test.** Before pressing anything:
> 1. **Predict.** What do you expect `digitalRead(BUTTON_PIN)` to return when the button is released? When it is pressed? What do you expect the LED to do in each case?
> 2. **Test.** Add a `Serial.println()` of both the button reading and `pressed` inside the loop, and check the Serial Monitor for both button states.
> 3. **Explain.** If anything differs from your prediction, what does the difference tell you?

### Changing the Logic

Because the behaviour lives in the program, you can change it without touching the wiring. This is one of the great advantages of a microcontroller. Try these, one at a time, and predict the result each time:

- **Invert it.** Make the LED light when the button is *released*, and go dark when it is pressed. What one word changes?
- **Add a message.** Print `"Pressed"` or `"Released"` while the LED changes.
- **Add a second behaviour.** Make the LED stay off when the button is pressed but blink when it is released.
- **Predict before testing.** What happens if you change `INPUT_PULLUP` to plain `INPUT`, with nothing else connected to the pin? Predict what the LED does, then check.

---

# Putting It All Together

## The Complete Flow

You now understand every link in the chain that connects the physical world to a program and back:

| Stage | What happens | Where it lives |
|---|---|---|
| **Physical input** | A finger presses a button | The physical world |
| **Digital signal** | The pin goes LOW (about 0 V) | The wire, and the pin's voltage |
| **Microcontroller** | The pin is read as `LOW` | The GPIO input |
| **Program logic** | `bool pressed = (digitalRead(BUTTON_PIN) == LOW);`, then `if (pressed)` | Your code |
| **Digital output** | `digitalWrite(LED_PIN, HIGH)` drives the pin HIGH | The GPIO output |
| **Physical action** | Current flows and the LED lights | The physical world |

Read it as the loop you learned at the start of the course:

```text
Sense (button) → Compute (your program) → Actuate (LED)
```

## Applying What You Have Learned

The activities below move from observing to reproducing, modifying, debugging and designing. Predict before every test.

### Predict Before You Test

For each of these two set-ups, predict what the LED does when the button is released and when it is pressed. Write your predictions down first. Then build or simulate each and check. Where a prediction was wrong, explain why.

| | Button wiring | Pull setting | LED wiring | Program line |
|---|---|---|---|---|
| **A** | Between pin and GND | `INPUT_PULLUP` | Pin → resistor → LED → GND | `digitalWrite(LED_PIN, !digitalRead(BUTTON_PIN));` |
| **B** | Between pin and 3.3 V | `INPUT_PULLDOWN` | Pin → resistor → LED → GND | `digitalWrite(LED_PIN, digitalRead(BUTTON_PIN));` |

### Debug

This program is meant to light an LED while a button is pressed. It contains errors. Find every one by reading, then check your list by running it.

```cpp
#define LED_PIN 4
#define BUTTON_PIN 7

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == HIGH) {
    digitalWrite(LED_PIN, HIGH)
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
```

Then reason about these situations, saying what you would check, and in what order:

- The program runs without errors, but the LED is *always* on, whatever the button does.
- The LED lights when you press the button, but the effect is the opposite of what you intended.
- The button seems to work, but sometimes the LED lights when nobody is touching it.
- The LED never lights, but the Serial Monitor shows `LOW` when you press the button.

### Design

Design and build one of these using only digital inputs and outputs. Write down your predictions before testing, and describe the logic in plain words before writing code.

- **Push-to-light:** The LED lights when the button is pressed and *stays on for two seconds after release*.
- **Traffic light with a pedestrian button:** Combine the traffic-light program with a button. While the button is held down, force the light to red; release it, and the normal sequence resumes.

For whichever you build, draw the signal path from physical input to physical action, and mark which parts are sensing, computing and actuating.

## What You Can Now Do, and What Comes Next

You began this lesson with the LED recipe from your first programs. You can now explain it, and extend it.

- You understand that a **digital signal** represents a two-state physical condition as one of two voltage levels, **HIGH** or **LOW** — and how that differs from an **analog** signal, which can take any value in a range.
- You can configure a GPIO pin as a **digital output** to control an LED, or several, as in a traffic light, and as a **digital input** to read a button, using the pattern *choose, configure, use*.
- You can use a **pull-up** or **pull-down** resistor to give a button input a reliable default, and you can translate an electrical state into a meaningful name in code.
- You can use an input to make a **decision** that controls an output.
- You can explain the whole flow: **Physical Input → Digital Signal → Microcontroller → Program Logic → Digital Output → Physical Action.**

The mental model to carry forward is this: **a digital I/O system reads yes-or-no conditions from the physical world, applies logic that you wrote and produces yes-or-no actions in return.**

The next steps build on exactly this foundation. You will look at what happens when a button *changes* state, rather than just its current state — including why mechanical buttons need special handling and how to detect a press reliably. After that, digital sensors that go beyond a simple button, and then quantities that vary smoothly, such as light and temperature, and outputs that can be varied rather than merely switched on and off.

---

## References

1. Espressif Systems. *ESP32-S3 Series Datasheet* (electrical characteristics: input and output voltage levels, input current, internal pull-up and pull-down resistors, strapping pins, USB pins). https://documentation.espressif.com/esp32-s3_datasheet_en.html
2. Espressif Systems. *ESP32-S3-WROOM-1 & ESP32-S3-WROOM-1U Datasheet* (DC characteristics, strapping pins). https://media.digikey.com/pdf/Data%20Sheets/Espressif%20PDFs/ESP32-S3-WROOM-1_1U_v0.5.1_Preliminary.pdf
3. Arduino. *Language Reference* (`pinMode`, `digitalWrite`, `digitalRead`, `delay`, `Serial`). https://www.arduino.cc/reference/en/
4. Arduino. *Digital Pins* (`INPUT`, `OUTPUT`, `INPUT_PULLUP` explained). https://docs.arduino.cc/learn/microcontrollers/digital-pins/
5. Espressif Systems. *Arduino-ESP32: GPIO* (`INPUT_PULLUP` and `INPUT_PULLDOWN` support on the ESP32 family). https://docs.espressif.com/projects/arduino-esp32/en/latest/api/gpio.html
6. Wokwi. *Wokwi for ESP32* (browser-based ESP32/ESP32-S3 simulator, wiring parts, running a simulation). https://wokwi.com/esp32

> **Note.** Voltage thresholds and pull-resistor values are taken from Espressif's ESP32-S3 datasheet for a 3.3 V supply and are typical figures. LED and resistor values are example values. Always confirm details against the documentation of your own board and components, and against Wokwi's own part specifications when simulating.
