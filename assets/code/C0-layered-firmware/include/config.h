// config.h — every board-specific number lives here, and only here.
#pragma once
#include <stdint.h>

// Pin map (from B1)
constexpr int PIN_SDA = 6;   // D4
constexpr int PIN_SCL = 7;   // D5

// I2C
constexpr uint32_t I2C_CLOCK_HZ = 400000;
constexpr uint8_t  ADDR_IMU     = 0x68;   // MPU-6050, AD0 tied to GND

// Timing
constexpr uint32_t MOTION_PERIOD_MS = 20;    // 50 samples per second
constexpr uint32_t REPORT_PERIOD_MS = 1000;

// Set to true to run without hardware (for example in a simulator).
constexpr bool USE_MOCK_MOTION = false;
