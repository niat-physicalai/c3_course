// D1 — The esp_watch state diagram, transcribed into code.
// Events are typed into the Serial Monitor so it runs on any ESP32 or in Wokwi:
//   b = button press, h = request heart rate, r = heart-rate result
// Every case below matches one box in the diagram; every "enter(...)" call
// matches one arrow.

enum class State { Boot, Awake, Measuring, Asleep };

const unsigned long SCREEN_TIMEOUT_MS = 30000;   // 30 s with no input

State state = State::Boot;
unsigned long lastInput = 0;

const char *name(State s) {
  switch (s) {
    case State::Boot:      return "BOOT";
    case State::Awake:     return "AWAKE";
    case State::Measuring: return "MEASURING";
    case State::Asleep:    return "ASLEEP";
  }
  return "?";
}

void enter(State next) {
  // Exit actions
  if (state == State::Measuring) Serial.println("  exit: heart-rate LEDs off");
  if (state == State::Asleep)    Serial.println("  exit: display on");

  Serial.printf("%s -> %s\n", name(state), name(next));
  state = next;
  lastInput = millis();

  // Entry actions
  if (state == State::Measuring) Serial.println("  entry: heart-rate LEDs on");
  if (state == State::Asleep)    Serial.println("  entry: display off");
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("BOOT: connect WiFi once, fetch time and weather, WiFi off");
  enter(State::Awake);   // event: done
}

void loop() {
  int c = Serial.available() ? Serial.read() : -1;

  switch (state) {
    case State::Boot:
      break;  // left in setup()
    case State::Awake:
      if (c == 'h') enter(State::Measuring);
      else if (c == 'b') lastInput = millis();          // stays AWAKE, timer restarts
      else if (millis() - lastInput >= SCREEN_TIMEOUT_MS) enter(State::Asleep);
      break;
    case State::Measuring:
      if (c == 'r') enter(State::Awake);                // result / abort
      break;
    case State::Asleep:
      if (c == 'b') enter(State::Awake);                // button
      break;
  }
}
