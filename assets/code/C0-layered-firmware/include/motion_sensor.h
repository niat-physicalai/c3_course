// motion_sensor.h — what the rest of the firmware knows about a motion sensor.
// Nothing here names a chip. Any driver that fills in these two functions
// can replace any other.
#pragma once

struct Accel {
  float x, y, z;   // metres per second squared
};

class MotionSensor {
public:
  virtual ~MotionSensor() {}
  virtual bool begin() = 0;
  virtual bool read(Accel &out) = 0;   // false if the read failed
};
