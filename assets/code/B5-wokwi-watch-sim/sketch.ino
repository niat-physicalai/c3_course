// B5 — Virtual prototype of a module-based watch (Wokwi, XIAO ESP32-C3)
// Display + motion sensor on one I2C bus, a mock heart-rate sensor and
// two buttons, wired like esp_watch. Pin map follows B3.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// ---- Pin map (XIAO label -> GPIO) ----
const int PIN_SDA      = 6;   // D4
const int PIN_SCL      = 7;   // D5
const int PIN_BTN_NEXT = 10;  // D10, button to GND, internal pull-up
const int PIN_BTN_PREV = 3;   // D1,  button to GND, internal pull-up

// ---- I2C addresses ----
const uint8_t ADDR_OLED = 0x3C;
const uint8_t ADDR_IMU  = 0x68;   // AD0 tied to GND

const uint32_t I2C_CLOCK_HZ = 400000;

// Pass the bus speed to the display library too: by default it switches the
// bus to 400 kHz while sending a frame and back to 100 kHz afterwards.
Adafruit_SSD1306 display(128, 64, &Wire, -1, I2C_CLOCK_HZ, I2C_CLOCK_HZ);
Adafruit_MPU6050 imu;

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

int screen = 0;               // 0 = motion, 1 = heart rate
const int SCREEN_COUNT = 2;

bool lastNext = HIGH;
bool lastPrev = HIGH;
unsigned long lastRedraw = 0;

void scanBus() {
  Serial.println("I2C scan:");
  for (uint8_t addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.printf("  found device at 0x%02X\n", addr);
    }
  }
}

void drawScreen() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextWrap(false);          // see esp_watch known issue 4
  display.setTextSize(1);
  display.setCursor(0, 0);

  if (screen == 0) {
    sensors_event_t a, g, temp;
    imu.getEvent(&a, &g, &temp);
    display.println("MOTION (m/s^2)");
    display.printf("x %6.2f\n", a.acceleration.x);
    display.printf("y %6.2f\n", a.acceleration.y);
    display.printf("z %6.2f\n", a.acceleration.z);
  } else {
    display.println("HEART RATE (mock)");
    display.setTextSize(3);
    display.setCursor(0, 20);
    display.printf("%d", heart.readBpm());
  }

  // Time how long it takes to send one full frame over I2C.
  unsigned long t0 = micros();
  display.display();
  unsigned long dt = micros() - t0;
  Serial.printf("screen %d sent in %lu us\n", screen, dt);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_BTN_NEXT, INPUT_PULLUP);
  pinMode(PIN_BTN_PREV, INPUT_PULLUP);

  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(I2C_CLOCK_HZ);
  scanBus();

  if (!display.begin(SSD1306_SWITCHCAPVCC, ADDR_OLED)) {
    Serial.println("Display not found");
  }
  if (!imu.begin(ADDR_IMU, &Wire)) {
    Serial.println("Motion sensor not found");
  }
  heart.begin();
  drawScreen();
}

void loop() {
  bool next = digitalRead(PIN_BTN_NEXT);
  bool prev = digitalRead(PIN_BTN_PREV);

  // A press is a change from HIGH (released) to LOW (pressed).
  if (lastNext == HIGH && next == LOW) {
    screen = (screen + 1) % SCREEN_COUNT;
    drawScreen();
  }
  if (lastPrev == HIGH && prev == LOW) {
    screen = (screen + SCREEN_COUNT - 1) % SCREEN_COUNT;
    drawScreen();
  }
  lastNext = next;
  lastPrev = prev;

  // Refresh the current screen once a second, not on every loop.
  if (millis() - lastRedraw >= 1000) {
    lastRedraw = millis();
    drawScreen();
  }
  delay(20);  // simple debounce; D2 replaces this with non-blocking timing
}
