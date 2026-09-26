// main.cpp — application layer: decides what happens and when.
// It talks to a MotionSensor and a StepCounter, never to registers.
#include <Arduino.h>
#include <Wire.h>
#include "config.h"
#include "mpu6050_motion.h"
#include "mock_motion.h"
#include "step_counter.h"

Mpu6050Motion realMotion(Wire, ADDR_IMU);
MockMotion    mockMotion;
MotionSensor &motion = USE_MOCK_MOTION ? static_cast<MotionSensor &>(mockMotion)
                                       : static_cast<MotionSensor &>(realMotion);
StepCounter stepCounter;

unsigned long lastMotion = 0;
unsigned long lastReport = 0;
unsigned long failedReads = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(I2C_CLOCK_HZ);
  if (!motion.begin()) {
    Serial.println("Motion sensor did not start");
  }
}

void loop() {
  unsigned long now = millis();

  if (now - lastMotion >= MOTION_PERIOD_MS) {
    lastMotion = now;
    Accel a;
    if (motion.read(a)) {
      stepCounter.update(a);
    } else {
      failedReads++;
    }
  }

  if (now - lastReport >= REPORT_PERIOD_MS) {
    lastReport = now;
    Serial.printf("steps=%lu failed_reads=%lu\n", stepCounter.steps(), failedReads);
  }
}
