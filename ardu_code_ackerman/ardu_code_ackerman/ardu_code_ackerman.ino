#include <Servo.h>

int mensaje; 

//motors
int IN1 = 10;
int IN2 = 9;
int IN3 = 8;
int IN4 = 7;

//servos
Servo s1;
int servo1 = 11;

//Proximity sensor variables
int ECO = 12;       
int TRIG = 13;      
int DURACION;
int DISTANCIA;

void setup() {
  
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  s1.attach(servo1);

  //PROXIMITY SENSOR
  pinMode(TRIG, OUTPUT);  
  pinMode(ECO, INPUT);

  Serial.begin(115200);
}

//ACTIONS
void go()
{
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
}


void turn_left() {
  for (int i = 0; i < 5; i++) {
    // Move left forward
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    delay(300); // Adjust delay as needed

    // Move right backward
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    delay(300); // Adjust delay as needed
  }
}

void turn_right() {
  for (int i = 0; i < 5; i++) {
    // Move left forward
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    delay(300); // Adjust delay as needed

    // Move right backward
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    delay(300); // Adjust delay as needed
  }
}

void Stop()
{
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
}

void sensor(){
  digitalWrite(TRIG, HIGH);     // generation of the pulse to be sent
  delay(1);                     
  digitalWrite(TRIG, LOW);      
  
  DURACION = pulseIn(ECO, HIGH);  // with pulseIn function a pulse is expected
                                
  DISTANCIA = DURACION / 58.2;    // distance measured in centimeters
  delay(1);                       // delay between data
  
  
  if(DISTANCIA < 25) //if DISTANCIA is lower than 25cm this colides
  {
    Serial.write('1');
  }

  else{
    Serial.write('0');
  }
   

}


void loop() {
  

  if (Serial.available()) {
    mensaje = Serial.read();  //Read the message

    if(mensaje == 'a'){     //Right
      s1.write(40);
      delay(1000);
      Serial.write('F');  //Send 'F' to take picture
    }

    else if(mensaje == 'b'){ //Front
      s1.write(85);
      delay(1000);
      Serial.write('F');  //Send 'F' to take picture
    }

    else if(mensaje == 'c'){ //Left
      s1.write(135);
      delay(1000);
      Serial.write('F');  //Send 'F' to take picture
    }


    else if(mensaje == 'd'){
      go();
    }

    else if(mensaje == 'e'){
      turn_left();
    }
    
    else if(mensaje == 'f'){
      turn_right();
    }
    
    else if(mensaje == 'g'){
      Stop();
    }

    else if(mensaje == 'M'){
      sensor();
    }

  }
                  
}
