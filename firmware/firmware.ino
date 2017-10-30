#include <RFControl.h>



//SHORT_UP, SHORT_DOWN, LONG_UP, SHORT_DOWN, LONG_UP, SHORT_DOWN, LONG_UP, LONG_DOWN, SHORT_UP, SHORT_DOWN, LONG_UP, LONG_DOWN, SHORT_UP, LONG_DOWN,
//SHORT_UP, SHORT_DOWN, LONG_UP, SHORT_DOWN, LONG_UP, SHORT_DOWN, LONG_UP, LONG_DOWN, SHORT_UP, LONG_DOWN, SHORT_UP, LONG_DOWN, SHORT_UP
// 388 264 764 252 764 272 748 564 388 264 748 576 356 588 360 280 744 284 744 276 740 592 352 580 364 5656


// Microsecond durations for different signals
const unsigned int LONG_UP = 730;
const unsigned int LONG_DOWN = 550;

// Fault tolerance in ms, for signal durations
const unsigned char TOLERANCE = 50;

// Signal pattern to match
const unsigned char PATTERN_LENGTH = 11;
const unsigned char PATTERN[PATTERN_LENGTH] = {1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0};

const unsigned char OUTPUT_PIN = 3;
const unsigned char LED_PIN = A5;

void setup() {
  pinMode(OUTPUT_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  
  digitalWrite(OUTPUT_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  RFControl::startReceiving(0);

  
}


bool between(unsigned int input, unsigned int min, unsigned int max) {
  return input >= min && input <= max;
}

bool is_one(unsigned long time) {
  return between(time, LONG_UP - TOLERANCE, LONG_UP + TOLERANCE);
}

bool is_zero(unsigned long time) {
  return between(time, LONG_DOWN - TOLERANCE, LONG_DOWN + TOLERANCE);
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