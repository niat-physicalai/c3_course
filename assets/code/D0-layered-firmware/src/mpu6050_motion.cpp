#include <Arduino.h>   // PlatformIO compiles .cpp files as plain C++
#include "mpu6050_motion.h"

namespace {
constexpr uint8_t REG_ACCEL_XOUT_H = 0x3B;
constexpr uint8_t REG_PWR_MGMT_1   = 0x6B;   // resets to 0x40: asleep
constexpr uint8_t REG_WHO_AM_I     = 0x75;   // 0x68 on a genuine part
constexpr float   LSB_PER_G        = 16384.0f;  // +/-2 g range (default)
constexpr float   G                = 9.80665f;
}

bool Mpu6050Motion::writeReg(uint8_t reg, uint8_t value) {
  bus_.beginTransmission(addr_);
  bus_.write(reg);
  bus_.write(value);
  return bus_.endTransmission() == 0;
}

bool Mpu6050Motion::begin() {
  bus_.beginTransmission(addr_);
  bus_.write(REG_WHO_AM_I);
  if (bus_.endTransmission(false) != 0) return false;
  if (bus_.requestFrom(addr_, (uint8_t)1) != 1) return false;
  uint8_t id = bus_.read();
  // A genuine MPU-6050 answers 0x68. Clone chips answer other values
  // (esp_watch's reads 0x70) and still work, so accept both, and report it.
  if (id != 0x68 && id != 0x70) return false;
  if (id != 0x68) Serial.printf("MPU-6050 WHO_AM_I = 0x%02X (clone)\n", id);
  return writeReg(REG_PWR_MGMT_1, 0x00);   // clear SLEEP: start measuring
}

bool Mpu6050Motion::read(Accel &out) {
  bus_.beginTransmission(addr_);
  bus_.write(REG_ACCEL_XOUT_H);
  if (bus_.endTransmission(false) != 0) return false;
  if (bus_.requestFrom(addr_, (uint8_t)6) != 6) return false;
  int16_t raw[3];
  for (int i = 0; i < 3; i++) {
    uint8_t hi = bus_.read();
    uint8_t lo = bus_.read();
    raw[i] = (int16_t)((hi << 8) | lo);
  }
  out.x = raw[0] / LSB_PER_G * G;
  out.y = raw[1] / LSB_PER_G * G;
  out.z = raw[2] / LSB_PER_G * G;
  return true;
}
