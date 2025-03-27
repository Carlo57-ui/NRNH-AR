#include <Servo.h>

int mensaje; 

//motores
int IN1 = 10;
int IN2 = 9;
int IN3 = 8;
int IN4 = 7;

//servos
Servo s1;
int servo1 = 11;

//VARIABLES DEL SENSOR DE PROXIMIDAD//
int ECO = 12;       
int TRIG = 13;      
int DURACION;
int DISTANCIA;

//int coli = 0;

void setup() {
  
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  s1.attach(servo1);

  //SENSOR DE PROXIMIDAD//
  pinMode(TRIG, OUTPUT);  
  pinMode(ECO, INPUT);

  Serial.begin(115200);
}

void go()
{
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
}

void turn_left() {
  for (int i = 0; i < 5; i++) {
    // Move left forward
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    delay(100); // Adjust delay as needed

    // Move right backward
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    delay(100); // Adjust delay as needed
  }
}

void turn_right() {
  for (int i = 0; i < 5; i++) {
    // Move left forward
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    delay(100); // Adjust delay as needed

    // Move right backward
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    delay(100); // Adjust delay as needed
  }
}

void Stop()
{
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
}

void sensor(){
  digitalWrite(TRIG, HIGH);     // generacion del pulso a enviar
  delay(1);                     // al pin conectado al trigger
  digitalWrite(TRIG, LOW);      // del sensor
  
  DURACION = pulseIn(ECO, HIGH);  // con funcion pulseIn se espera un pulso
                                  // alto en Echo
  DISTANCIA = DURACION / 58.2;    // distancia medida en centimetros
  delay(1);                       // demora entre datos
  
  
  if(DISTANCIA < 25) //Si la distancia es mayor a 25cm no colisiona
  {
    Serial.write('1');
  }

  else{
    Serial.write('0');
  }
   

}


void loop() {
  mensaje = Serial.read();  //lee el mensaje

  if(mensaje == 'a'){
    s1.write(0);
    Serial.write('F');  //Enviar F para tomar foto
  }

  if(mensaje == 'b'){
    s1.write(90);
    Serial.write('F');  //Enviar F para tomar foto
  }

  if(mensaje == 'c'){
    s1.write(180);
    Serial.write('F');  //Enviar F para tomar foto
  }


  if(mensaje == 'd'){
    go();
  }

  if(mensaje == 'e'){
    turn_left();
  }
  
  if(mensaje == 'f'){
    turn_right();
  }
  
  if(mensaje == 'g'){
    Stop();
  }

  if(mensaje == 'M'){
    sensor();
  }


                  
}