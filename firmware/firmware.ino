// This is the Arduino firmware
// for snarky-doorbell RF receiver module
// The whole purpose of this is to turn
// a pin HIGH when the doorbell button has been
// pressed, so that Raspberry could react

#include <RFControl.h>

const unsigned int TRUE_MARK = 500;

// Signal pattern to match
const unsigned char PATTERN_LENGTH = 4;
const unsigned char PATTERN[PATTERN_LENGTH] = {0, 0, 1, 1};

const unsigned char OUTPUT_PIN = 3;
const unsigned char LED_PIN = A5;

void setup() {
  
  pinMode(OUTPUT_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  
  digitalWrite(OUTPUT_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  RFControl::startReceiving(0);
}

bool is_one(unsigned long time) {
  return time > TRUE_MARK;
}

bool is_zero(unsigned long time) {
  return time <= TRUE_MARK;
}

void activate() {
  digitalWrite(OUTPUT_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);
  delay(2000);
  digitalWrite(OUTPUT_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  RFControl::continueReceiving();
}

void loop() {

  if (!RFControl::hasData()) {
    delay(50);
    return;
  }

  digitalWrite(LED_PIN, HIGH);
  
  unsigned int *timings;
  unsigned int timings_size;
  unsigned int pulse_length_divider = RFControl::getPulseLengthDivider();

  unsigned char index = 0;

  RFControl::getRaw(&timings, &timings_size);
  
  for (int i = 0; i < timings_size; i++) {

    unsigned long timing = timings[i] * pulse_length_divider;
    
    if (index + 1 == PATTERN_LENGTH) {
      activate();
      return;
    }
    
    if (is_one(timing)) {
      if (PATTERN[index] != 1) {
        break;
      }
      
      index += 1;
    }

    if (is_zero(timing)) {
      if (PATTERN[index] != 0) {
        break;
      }
     
      index += 1;
    }
  }
  
  digitalWrite(LED_PIN, LOW);
  RFControl::continueReceiving();
}
