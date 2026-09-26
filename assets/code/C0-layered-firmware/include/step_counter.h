// step_counter.h — service layer: turns acceleration into steps.
// It knows nothing about which chip produced the numbers.
#pragma once
#include "motion_sensor.h"

class StepCounter {
public:
  void update(const Accel &a);
  unsigned long steps() const { return steps_; }

private:
  unsigned long steps_ = 0;
  bool above_ = false;
};
