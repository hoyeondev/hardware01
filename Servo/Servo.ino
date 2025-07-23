#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
const int buttonPin = 2; // 버튼
int buttonState = 0;

const int trigPin = 9;
const int echoPin = 10;

float duration, distance;

void setup() {
  myservo.attach(6);  // attaches the servo on pin 9 to the servo object
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState);  // 상태 확인용 출력

  if (buttonState == HIGH) {
    for (int i = 0; i < 2; i++) {
      // 0도 → 180도
      for (pos = 0; pos <= 180; pos++) {
        myservo.write(pos);
        delay(5);
      }
      // 180도 → 0도
      for (pos = 180; pos >= 0; pos--) {
        myservo.write(pos);
        delay(5);
      }
    }

    Serial.println("go");
    
    // 버튼을 뗄 때까지 대기 (중복 입력 방지용)
    while (digitalRead(buttonPin) == HIGH) {
      delay(10);
    }
  }
}