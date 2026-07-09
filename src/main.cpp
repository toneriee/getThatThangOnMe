#include <ESP32Servo.h>      // Library for controlling servo motors with ESP32
#include <Arduino.h>
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;
// ----- Pin Definitions -----
#define IN1 27               // Motor A input pin 1
#define IN2 26               // Motor A input pin 2
#define IN3 25               // Motor B input pin 1
#define IN4 33               // Motor B input pin 2

#define ENA 14               // PWM control pin for Motor A
#define ENB 32               // PWM control pin for Motor B

#define pump 23            // Pin connected to relay controlling the water pump
#define ServoPin 15         // Servo motor signal pin

#define FlameLeft 34         // Analog input pin for left flame sensor
#define FlameMiddle 39       // Analog input pin for middle flame sensor
#define FlameRight 35        // Analog input pin for right flame sensor

#define inbuilt_led 2        // On-board LED pin for ESP32

// Time constants (in milliseconds)
#define move_forward 300     // Forward movement time
#define turning_time 300     // Turning duration
#define move_backward 150    // Backward movement time
#define stop_delay 100       // Delay after stopping

int fireThreshold = 500;     // Analog value threshold to detect fire
int motorSpeed = 200;        // Speed of motors (PWM value from 0-255)

// ----- Objects -----
Servo myServo;              // Create servo motor object

// ----- Global Variables -----
bool fireDetected = false;  // Flag for fire detection
void stopMoving();
void moveForward();
void moveBackward();
void turnLeft();
void turnRight();
void slightLeft();
void slightRight();
void stopMoving();
void firefightMode(int left, int middle, int right);
void reset();
void bluetoothControl();
enum RobotMode
{
    BLUETOOTH_MODE,
    FIRE_MODE
};
void setup() {
  Serial.begin(9600);     // Start serial communication
  SerialBT.begin("FireRobot");
  Serial.println("Bluetooth Started");
  // Set motor control pins as output
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Set other component pins
  pinMode(pump, OUTPUT);
  pinMode(inbuilt_led, OUTPUT);
  pinMode(FlameLeft, INPUT);
  pinMode(FlameMiddle, INPUT);
  pinMode(FlameRight, INPUT);

  // Attach servo motor to pin
  myServo.attach(ServoPin);
  myServo.write(90);  // Center servo

  // Ensure pump and LED are off initially
  digitalWrite(pump, HIGH);
  digitalWrite(inbuilt_led, LOW);

}
RobotMode mode = BLUETOOTH_MODE;
void loop() {
  // Read analog values from flame sensors
  int leftSensor = analogRead(FlameLeft);
  int middleSensor = analogRead(FlameMiddle);
  int rightSensor = analogRead(FlameRight);
  Serial.print(leftSensor);
  Serial.print(" ");
  Serial.print(middleSensor);
  Serial.print(" ");
  Serial.println(rightSensor);
  // Check if any sensor detects fire (value below threshold)
  if (leftSensor < fireThreshold || middleSensor < fireThreshold || rightSensor < fireThreshold) {
    fireDetected = true;
  } else {
    fireDetected = false;
  }

  // Chọn chế độ hoạt động
if (fireDetected)
{
    mode = FIRE_MODE;
}
else
{
    mode = BLUETOOTH_MODE;
}

// Thực hiện theo chế độ
switch(mode)
{
    case BLUETOOTH_MODE:
        digitalWrite(pump, LOW);
        digitalWrite(inbuilt_led, LOW);
        myServo.write(90);

        bluetoothControl();
        break;

    case FIRE_MODE:

        firefightMode(leftSensor, middleSensor, rightSensor);
        break;
}
}

void firefightMode(int left, int middle, int right) {
  digitalWrite(inbuilt_led, HIGH);  // Turn on LED as alarm indicator
  Serial.println("FIRE DETECTED");

  // ******************** Robot Movement Logic ********************

  // Fire detected on right and middle sensors
  if (middle < fireThreshold && right < fireThreshold) {
    moveBackward();
    delay(move_backward);
    stopMoving();
    delay(stop_delay);
    slightRight();             // Slight right turn
    delay(turning_time);
    stopMoving();
    delay(stop_delay);
  }
  // Fire detected on left and middle sensors
  else if (middle < fireThreshold && left < fireThreshold) {
    moveBackward();
    delay(move_backward);
    stopMoving();
    delay(stop_delay);
    slightLeft();              // Slight left turn
    delay(turning_time);
    stopMoving();
    delay(stop_delay);
  }
  // Fire detected in the middle only
  else if (middle < fireThreshold) {
    moveForward();             // Move straight
    delay(move_forward);
    stopMoving();
    delay(stop_delay);
  }
  // Fire detected on left only
  else if (left < fireThreshold) {
    moveBackward();
    delay(move_backward);
    stopMoving();
    delay(stop_delay);
    turnLeft();                // Full left turn
    delay(turning_time);
    stopMoving();
  }
  // Fire detected on right only
  else if (right < fireThreshold) {
    moveBackward();
    delay(move_backward);
    stopMoving();
    delay(stop_delay);
    turnRight();               // Full right turn
    delay(turning_time);
    stopMoving();
  }
  else {
    stopMoving();              // No fire detected - stay still
  }

  digitalWrite(pump, HIGH);    // Activate pump to spray water

  // Sweep servo left to right to spray water
  for (int angle = 45; angle <= 135; angle += 5) {
    myServo.write(angle);
    delay(150);
  }
  for (int angle = 135; angle >= 45; angle -= 5) {
    myServo.write(angle);
    delay(150);
  }
  for (int angle = 45; angle <= 90; angle += 5) {
    myServo.write(angle);
    delay(150);
  }

  reset();  // Reset robot after spraying
}
 
void reset() {
  moveBackward();              // Move back a bit
  delay(move_backward);
  stopMoving();                // Stop
  digitalWrite(pump, LOW);     // Turn off pump
  digitalWrite(inbuilt_led, LOW);  // Turn off LED
}

// ---- Motor Control Functions ----
void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, motorSpeed);  // Set motor speed
  analogWrite(ENB, motorSpeed);
}

void moveBackward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);
}

void turnLeft() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);
}

void turnRight() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);
}

void slightLeft() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed * 0.6);  // Reduce speed of right motor
}

void slightRight() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, motorSpeed * 0.6);  // Reduce speed of left motor
  analogWrite(ENB, motorSpeed);
}

void stopMoving() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);         // Stop both motors
  analogWrite(ENB, 0);
}
void bluetoothControl()
{
    if(!SerialBT.available())
        return;

    char cmd = SerialBT.read();

    switch(cmd)
    {
        case 'F':
            moveForward();
            break;

        case 'B':
            moveBackward();
            break;

        case 'L':
            turnLeft();
            break;

        case 'R':
            turnRight();
            break;

        case 'S':
            stopMoving();
            break;
    }
}
// test123