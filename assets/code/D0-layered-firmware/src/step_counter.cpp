#include "step_counter.h"
#include <math.h>

namespace {
// Teaching model: a step is counted each time the size of the acceleration
// rises through an upper threshold, after first falling below a lower one.
constexpr float HIGH_THRESHOLD = 11.5f;   // m/s^2, example value
constexpr float LOW_THRESHOLD  = 9.0f;    // m/s^2, example value
}

void StepCounter::update(const Accel &a) {
  float magnitude = sqrtf(a.x * a.x + a.y * a.y + a.z * a.z);
  if (!above_ && magnitude > HIGH_THRESHOLD) {
    above_ = true;
    steps_++;
  } else if (above_ && magnitude < LOW_THRESHOLD) {
    above_ = false;
  }
}
