// D3 — Stream sensor data off the device in a documented CSV format.
// Runs on any ESP32 or in Wokwi. The PPG signal is synthetic (Wokwi has no
// MAX30102): a large, slowly drifting level with a small pulse on top, like
// a real optical heart-rate signal, plus noise.

const unsigned long SAMPLE_PERIOD_MS = 20;   // 50 samples per second
unsigned long lastSample = 0;

long syntheticPpg(unsigned long t_ms) {
  float t = t_ms / 1000.0f;
  float drift = 2000.0f * sinf(2.0f * PI * 0.05f * t);      // slow drift
  float pulse = 150.0f * sinf(2.0f * PI * 1.2f * t);        // 72 bpm
  float noise = random(-40, 41);
  return 50000L + (long)(drift + pulse + noise);
}

void setup() {
  Serial.begin(115200);
  delay(500);                                  // give the monitor time to open
  // Header: format name and version, then the column names with units.
  Serial.println("# esp_watch_stream v1");
  Serial.println("t_ms,ppg_counts,steps");
}

void loop() {
  unsigned long now = millis();
  if (now - lastSample >= SAMPLE_PERIOD_MS) {
    lastSample = now;
    long ppg = syntheticPpg(now);
    long steps = now / 600;                    // stand-in: a step every 0.6 s
    Serial.print(now);
    Serial.print(',');
    Serial.print(ppg);
    Serial.print(',');
    Serial.println(steps);
  }
}
