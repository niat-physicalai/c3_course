// mpu6050_motion.h — driver layer: the only file that knows MPU-6050 registers.
#pragma once
#include <Wire.h>
#include "motion_sensor.h"

class Mpu6050Motion : public MotionSensor {
public:
  Mpu6050Motion(TwoWire &bus, uint8_t address) : bus_(bus), addr_(address) {}
  bool begin() override;
  bool read(Accel &out) override;

private:
  bool writeReg(uint8_t reg, uint8_t value);
  TwoWire &bus_;
  uint8_t addr_;
};
