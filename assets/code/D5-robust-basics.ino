// D5 — Robustness basics: reset reason, log levels, watchdog, and a bus read
// that can fail without hanging. Runs on any ESP32-C3 (MPU-6050 optional).

#include <Wire.h>
#include <esp_system.h>
#include <esp_task_wdt.h>

// ---- Log levels: change LOG_LEVEL to see more or less ----
#define LVL_ERROR 1
#define LVL_WARN  2
#define LVL_INFO  3
#define LVL_DEBUG 4
#define LOG_LEVEL LVL_INFO
#define LOG(lvl, tag, fmt, ...) \
  do { if ((lvl) <= LOG_LEVEL) Serial.printf("# [%s] %s: " fmt "\n", tag, __func__, ##__VA_ARGS__); } while (0)
#define LOGE(fmt, ...) LOG(LVL_ERROR, "E", fmt, ##__VA_ARGS__)
#define LOGW(fmt, ...) LOG(LVL_WARN,  "W", fmt, ##__VA_ARGS__)
#define LOGI(fmt, ...) LOG(LVL_INFO,  "I", fmt, ##__VA_ARGS__)
#define LOGD(fmt, ...) LOG(LVL_DEBUG, "D", fmt, ##__VA_ARGS__)

const uint8_t ADDR_IMU = 0x68;
const uint32_t WDT_TIMEOUT_S = 5;

const char *resetReasonName(esp_reset_reason_t r) {
  switch (r) {
    case ESP_RST_POWERON:  return "power on";
    case ESP_RST_SW:       return "software restart";
    case ESP_RST_PANIC:    return "crash (panic)";
    case ESP_RST_INT_WDT:  return "interrupt watchdog";
    case ESP_RST_TASK_WDT: return "task watchdog";
    case ESP_RST_WDT:      return "other watchdog";
    case ESP_RST_BROWNOUT: return "brownout";
    case ESP_RST_DEEPSLEEP:return "wake from deep sleep";
    default:               return "other";
  }
}

// Read one register, with a bounded number of retries. Never hangs:
// Wire has its own timeout, and we give up after RETRIES attempts.
bool readRegister(uint8_t addr, uint8_t reg, uint8_t &value) {
  const int RETRIES = 3;
  for (int attempt = 1; attempt <= RETRIES; attempt++) {
    Wire.beginTransmission(addr);
    Wire.write(reg);
    if (Wire.endTransmission(false) == 0 && Wire.requestFrom(addr, (uint8_t)1) == 1) {
      value = Wire.read();
      return true;
    }
    LOGD("attempt %d failed", attempt);
  }
  return false;
}

void setup() {
  Serial.begin(115200);
  delay(500);
  esp_reset_reason_t why = esp_reset_reason();
  LOGI("boot, reset reason: %s", resetReasonName(why));
  if (why == ESP_RST_BROWNOUT) LOGW("last reset was a brownout: check battery and current peaks");

  Wire.begin(6, 7);
  Wire.setClock(400000);
  Wire.setTimeOut(20);                         // ms; bound every bus transaction

  // Watchdog: if loop() stops coming back for WDT_TIMEOUT_S, the chip resets.
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  esp_task_wdt_config_t cfg = {WDT_TIMEOUT_S * 1000, 0, true};
  esp_task_wdt_reconfigure(&cfg);
#else
  esp_task_wdt_init(WDT_TIMEOUT_S, true);
#endif
  esp_task_wdt_add(NULL);                      // watch this task (loop)
}

unsigned long lastRead = 0, failures = 0;

void loop() {
  esp_task_wdt_reset();                        // "I'm still alive"

  unsigned long now = millis();
  if (now - lastRead >= 1000) {
    lastRead = now;
    uint8_t id;
    if (readRegister(ADDR_IMU, 0x75, id)) {
      LOGD("WHO_AM_I = 0x%02X", id);
    } else {
      failures++;
      LOGW("motion sensor not answering (%lu failures)", failures);
    }
  }

  // Type 'h' in the Serial Monitor to simulate a hang and watch the watchdog act.
  if (Serial.available() && Serial.read() == 'h') {
    LOGE("simulating a hang");
    while (true) { }
  }
}
