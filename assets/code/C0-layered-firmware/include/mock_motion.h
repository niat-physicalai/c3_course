// mock_motion.h — a stand-in with the same interface, for testing without hardware.
// It pretends the wearer is walking at about two steps per second.
#pragma once
#include <Arduino.h>
#include "motion_sensor.h"

class MockMotion : public MotionSensor {
public:
  bool begin() override { return true; }
  bool read(Accel &out) override {
    float t = millis() / 1000.0f;
    out.x = 0.5f * sinf(t);
    out.y = 0.3f;
    out.z = 9.81f + 3.0f * sinf(2.0f * PI * 2.0f * t);
    return true;
  }
};
