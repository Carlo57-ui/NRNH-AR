#include <ESP32Servo.h>

int mensaje; 

//motores
int IN1 = 27;
int IN2 = 14;
int IN3 = 12;
int IN4 = 13;

//servos
Servo s1;
int servo1 = 19;

//VARIABLES DEL SENSOR DE PROXIMIDAD//
int ECO = 11;       
int TRIG = 10;      
int DURACION;
int DISTANCIA;


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

void sensor()
{
  digitalWrite(TRIG, HIGH);     // generacion del pulso a enviar
  delay(1);                     // al pin conectado al trigger
  digitalWrite(TRIG, LOW);      // del sensor
  
  DURACION = pulseIn(ECO, HIGH);  // con funcion pulseIn se espera un pulso
                                  // alto en Echo
  DISTANCIA = DURACION / 58.2;    // distancia medida en centimetros
  Serial.println(DISTANCIA);      // envio de valor de distancia por monitor serial
  delay(2);                       // demora entre datos
  
  if(DISTANCIA < 20) //Si la distancia es mayor a 20cm no colisiona
  {
    coli = 1
    delay(500);
  }

  else{
    coli = 0
  }

  return coli

}

void loop() {
  mensaje = Serial.read();  //lee el mensaje

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
    signal = sensor();
    return signal
  }

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

                  
}