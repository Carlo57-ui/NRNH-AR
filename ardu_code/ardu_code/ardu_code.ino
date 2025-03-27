#include <ESP32Servo.h>

int mensaje; 

//motores
int IN1 = 27;
int IN2 = 14;
int IN3 = 12;
int IN4 = 13;

//servos
Servo s1;
Servo s3;
Servo s4;
Servo s6;

int servo1 = 19;
int servo3 = 5;
int servo4 = 4;
int servo6 = 15;


void setup() {
  
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  s1.attach(servo1);
  s3.attach(servo3);
  s4.attach(servo4);
  s6.attach(servo6);

  Serial.begin(115200);
}

int limitToMaxValue(int value, int maxValue) {
  if (value > maxValue) {
    return maxValue;
  } else {
    return value;
  }
}

void loop() {
  int speedLeft = 0; 
  int speedRight = 0; 
  mensaje = Serial.read();

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n'); 
    
    if (data.startsWith("l")) {
      speedLeft = data.substring(1, data.indexOf("r")).toInt();
      speedRight = data.substring(data.indexOf("r") + 1).toInt();

      // Set rigth motor direction and speed
      if (speedRight > 0) {
        digitalWrite(IN2, LOW);
        analogWrite(IN1, abs(limitToMaxValue(speedRight, 250)));
      } else {
        digitalWrite(IN1, LOW);
        analogWrite(IN2, abs(limitToMaxValue(speedRight, 250)));
      }

      if (speedRight == 0) {
        digitalWrite(IN2, LOW);
        analogWrite(IN1, LOW);
      }

      // Set left motor direction and speed
      if (speedLeft > 0) {
        digitalWrite(IN4, LOW);
        analogWrite(IN3, abs(limitToMaxValue(speedLeft, 250)));
      } else {
        digitalWrite(IN3, LOW);
        analogWrite(IN4, abs(limitToMaxValue(speedLeft, 250)));
      }

      if (speedLeft == 0) {
        digitalWrite(IN4, LOW);
        analogWrite(IN3, LOW);
      }
      
    }
    //Recto
  if(mensaje == 'a'){
    s1.write(90);
    s3.write(90);
    s4.write(90);
    s6.write(90);
  }
    //Arco abierto a la izquierda
  if(mensaje == 'b'){
    s1.write(0);
    s3.write(0);
    s4.write(180);
    s6.write(180);
  }

    //Arco abierto a la derecha
  if(mensaje == 'c'){
    s1.write(180);
    s3.write(180);
    s4.write(0);
    s6.write(0);
  }

  }                  
}