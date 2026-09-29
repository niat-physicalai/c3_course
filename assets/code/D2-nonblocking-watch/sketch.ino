// D2 — Non-blocking watch firmware (Wokwi, XIAO ESP32-C3; same wiring as B5)
// Three peripherals at three rates, a state machine, and no delay() anywhere:
//   - motion sensor read every 20 ms (50 per second), always
//   - heart-rate sensor read every 40 ms, but only during a measurement burst
//   - display redrawn only when something shown on it has changed
// Buttons: "next" changes screen; "previous" starts a heart-rate measurement.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// ---- Configuration ----
const int PIN_SDA = 6, PIN_SCL = 7;
const int PIN_BTN_NEXT = 10, PIN_BTN_PREV = 3;
const unsigned long MOTION_PERIOD_MS  = 20;
const unsigned long HEART_PERIOD_MS   = 40;
const unsigned long MEASURE_TIME_MS   = 10000;  // shortened from 30 s for testing
const unsigned long SCREEN_TIMEOUT_MS = 30000;
const unsigned long DEBOUNCE_MS       = 30;

Adafruit_SSD1306 display(128, 64, &Wire, -1);
Adafruit_MPU6050 imu;

// ---- A periodic task: "has my interval passed?" without waiting ----
struct Every {
  unsigned long period, last;
  bool due(unsigned long now) {
    if (now - last >= period) {   // safe across millis() rollover
      last = now;
      return true;
    }
    return false;
  }
};
Every motionTask{MOTION_PERIOD_MS, 0};
Every heartTask{HEART_PERIOD_MS, 0};

// ---- A debounced button, checked every pass, never waits ----
struct Button {
  int pin;
  bool stable, lastRaw;
  unsigned long changedAt;
  bool pressed(unsigned long now) {           // true once per press
    bool raw = digitalRead(pin);
    if (raw != lastRaw) { lastRaw = raw; changedAt = now; }
    if (now - changedAt >= DEBOUNCE_MS && raw != stable) {
      stable = raw;
      return stable == LOW;
    }
    return false;
  }
};
Button btnNext{PIN_BTN_NEXT, HIGH, HIGH, 0};
Button btnPrev{PIN_BTN_PREV, HIGH, HIGH, 0};

// ---- Mock heart-rate sensor (Wokwi has no MAX30102) ----
int mockBpm(unsigned long now) { return 72 + (int)(6.0f * sinf(now / 10000.0f)); }

// ---- State ----
enum class State { Awake, Measuring, Asleep };
State state = State::Awake;
unsigned long lastInput = 0, measureStart = 0;
int screen = 0;
long steps = 0;
bool stepHigh = false;
int bpm = 0, samples = 0;
bool dirty = true;                 // something on screen has changed
unsigned long worstLoopUs = 0;

void enter(State next, unsigned long now) {
  state = next;
  lastInput = now;
  if (next == State::Measuring) { measureStart = now; samples = 0; }
  if (next == State::Asleep) display.ssd1306_command(SSD1306_DISPLAYOFF);
  else display.ssd1306_command(SSD1306_DISPLAYON);
  dirty = true;
}

void readMotion() {
  sensors_event_t a, g, t;
  imu.getEvent(&a, &g, &t);
  float m = sqrtf(a.acceleration.x * a.acceleration.x +
                  a.acceleration.y * a.acceleration.y +
                  a.acceleration.z * a.acceleration.z);
  if (!stepHigh && m > 11.5f) { stepHigh = true; steps++; if (screen == 0) dirty = true; }
  else if (stepHigh && m < 9.0f) stepHigh = false;
}

void redraw() {
  display.clearDisplay();
  display.setTextWrap(false);
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  if (state == State::Measuring) {
    display.println("MEASURING...");
    display.printf("%d samples", samples);
  } else if (screen == 0) {
    display.println("STEPS");
    display.setTextSize(3);
    display.printf("%ld", steps);
  } else {
    display.println("HEART RATE");
    display.setTextSize(3);
    if (bpm > 0) display.printf("%d", bpm); else display.print("--");
  }
  display.display();
  dirty = false;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_BTN_NEXT, INPUT_PULLUP);
  pinMode(PIN_BTN_PREV, INPUT_PULLUP);
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(400000);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) Serial.println("Display not found");
  if (!imu.begin(0x68, &Wire)) Serial.println("Motion sensor not found");
  enter(State::Awake, millis());
}

void loop() {
  unsigned long start = micros();
  unsigned long now = millis();

  // 1. Always: sensors that must never be missed
  if (motionTask.due(now)) readMotion();

  // 2. Inputs
  bool next = btnNext.pressed(now);
  bool prev = btnPrev.pressed(now);

  // 3. State machine (from D1)
  switch (state) {
    case State::Awake:
      if (next) { screen = (screen + 1) % 2; lastInput = now; dirty = true; }
      if (prev) enter(State::Measuring, now);
      else if (now - lastInput >= SCREEN_TIMEOUT_MS) enter(State::Asleep, now);
      break;
    case State::Measuring:
      if (heartTask.due(now)) { samples++; if (samples % 25 == 0) dirty = true; }
      if (now - measureStart >= MEASURE_TIME_MS) {
        bpm = mockBpm(now);
        screen = 1;
        enter(State::Awake, now);
      }
      break;
    case State::Asleep:
      if (next || prev) enter(State::Awake, now);  // shake-to-wake would go here too
      break;
  }

  // 4. Display: only when something changed, and never while asleep
  if (dirty && state != State::Asleep) redraw();

  // 5. Keep an eye on the longest pass through loop()
  unsigned long took = micros() - start;
  if (took > worstLoopUs) {
    worstLoopUs = took;
    Serial.printf("new worst loop time: %lu us\n", worstLoopUs);
  }
}
