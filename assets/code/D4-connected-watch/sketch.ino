// D4 — Robust connectivity: WiFi and MQTT that never block the loop for long,
// reconnect with backoff, buffer readings while offline, and keep settings in NVS.
// Runs in Wokwi (SSID "Wokwi-GUEST") or on a real ESP32-C3.
// Serial commands:  wifi <ssid> <password>   save new WiFi details
//                   reset                    factory reset (clears NVS)
// Holding the "next" button (GPIO10) for 5 s also performs a factory reset.

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Preferences.h>

// ---- Configuration ----
const char *MQTT_HOST = "test.mosquitto.org";   // public test broker: never send private data
const int   MQTT_PORT = 1883;
const int   PIN_BTN_NEXT = 10;
const unsigned long READING_PERIOD_MS = 5000;
const unsigned long WIFI_TIMEOUT_MS   = 15000;
const unsigned long BACKOFF_MIN_MS    = 1000;
const unsigned long BACKOFF_MAX_MS    = 60000;
const unsigned long RESET_HOLD_MS     = 5000;

Preferences prefs;
WiFiClient net;
PubSubClient mqtt(net);
String ssid, pass, deviceId, topicData, topicStatus;

// ---- Readings and the offline buffer (a ring buffer in RAM) ----
struct Reading { unsigned long t_ms; long steps; int hr_bpm; float batt_v; };
const int BUF_SIZE = 64;
Reading buf[BUF_SIZE];
int bufHead = 0, bufCount = 0;          // head = oldest item
unsigned long dropped = 0;

void pushReading(const Reading &r) {
  if (bufCount == BUF_SIZE) {           // full: drop the oldest (a design choice)
    bufHead = (bufHead + 1) % BUF_SIZE;
    bufCount--;
    dropped++;
  }
  buf[(bufHead + bufCount) % BUF_SIZE] = r;
  bufCount++;
}

// ---- Network state machine with exponential backoff ----
enum class Net { Idle, WifiConnecting, WifiUp, Online };
Net netState = Net::Idle;
unsigned long netSince = 0, retryAt = 0, backoff = BACKOFF_MIN_MS;

void scheduleRetry(unsigned long now, const char *why) {
  unsigned long jitter = random(0, backoff / 5 + 1);
  retryAt = now + backoff + jitter;
  Serial.printf("# %s; retry in %lu ms\n", why, backoff + jitter);
  backoff = min(backoff * 2, BACKOFF_MAX_MS);
  netState = Net::Idle;
}

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
    case Net::Online:
      if (WiFi.status() != WL_CONNECTED || !mqtt.connected()) {
        scheduleRetry(now, "link lost");
        break;
      }
      mqtt.loop();
      // Flush a few buffered readings per pass, oldest first.
      for (int i = 0; i < 5 && bufCount > 0; i++) {
        const Reading &r = buf[bufHead];
        JsonDocument doc;
        doc["v"] = 1;
        doc["device"] = deviceId;
        doc["t_ms"] = r.t_ms;
        doc["steps"] = r.steps;
        doc["hr_bpm"] = r.hr_bpm;
        doc["batt_v"] = r.batt_v;
        doc["buffered"] = bufCount - 1;
        char payload[192];
        serializeJson(doc, payload, sizeof(payload));
        if (!mqtt.publish(topicData.c_str(), payload)) break;  // keep it for next time
        bufHead = (bufHead + 1) % BUF_SIZE;
        bufCount--;
      }
      break;
  }
}

// ---- Settings in NVS (Preferences) ----
void loadSettings() {
  prefs.begin("watch", true);                  // read-only
  ssid = prefs.getString("ssid", "Wokwi-GUEST");
  pass = prefs.getString("pass", "");
  prefs.end();
}

void saveWifi(const String &s, const String &p) {
  prefs.begin("watch", false);
  prefs.putString("ssid", s);
  prefs.putString("pass", p);
  prefs.end();
  Serial.println("# saved WiFi details; restarting");
  ESP.restart();
}

void factoryReset() {
  prefs.begin("watch", false);
  prefs.clear();
  prefs.end();
  Serial.println("# factory reset; restarting");
  ESP.restart();
}

void handleSerial() {
  if (!Serial.available()) return;
  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line == "reset") factoryReset();
  if (line.startsWith("wifi ")) {
    int sp = line.indexOf(' ', 5);
    String s = sp > 0 ? line.substring(5, sp) : line.substring(5);
    String p = sp > 0 ? line.substring(sp + 1) : "";
    saveWifi(s, p);
  }
}

// ---- Setup and loop ----
unsigned long lastReading = 0, pressedSince = 0;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(20);
  pinMode(PIN_BTN_NEXT, INPUT_PULLUP);
  loadSettings();
  WiFi.mode(WIFI_STA);
  uint8_t mac[6];
  WiFi.macAddress(mac);
  char id[20];
  snprintf(id, sizeof(id), "watch-%02x%02x%02x", mac[3], mac[4], mac[5]);
  deviceId = id;
  topicData = "c3course/" + deviceId + "/data";
  topicStatus = "c3course/" + deviceId + "/status";
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  Serial.printf("# device %s, publishing to %s\n", id, topicData.c_str());
}

void loop() {
  unsigned long now = millis();

  if (now - lastReading >= READING_PERIOD_MS) {   // mock readings every 5 s
    lastReading = now;
    pushReading({now, (long)(now / 600), 70 + (int)random(0, 8), 3.9f});
  }

  serviceNetwork(now);
  handleSerial();

  // Hold "next" for 5 s to factory reset, checked without waiting.
  if (digitalRead(PIN_BTN_NEXT) == LOW) {
    if (pressedSince == 0) pressedSince = now;
    else if (now - pressedSince >= RESET_HOLD_MS) factoryReset();
  } else {
    pressedSince = 0;
  }
}
