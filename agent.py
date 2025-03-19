#import RPi.GPIO as GPIO
import time
import random

class Entorno:
    def __init__(self):
        self.led_1 = 37
        self.led_2 = 35
        self.led_3 = 33
        self.led_4 = 31
        self.led_5 = 29
        self.led_6 = 11 #cambio 27 a 11
        self.led_7 = 23
        self.led_8 = 21
        self.led_9 = 19
        self.led_azul = 15

        self.boton_0 = 18 #cambio 28 a 18
        self.boton_1 = 22
        self.boton_2 = 24
        self.boton_c8 = 26
        

        #GPIO.setmode(GPIO.BOARD)



    def reset(self): # Ultrasonic sensor signal
        state = random.randint(0,1)
        return state

    def step(self,action):
        #que realice la acción
        next_state = random.randint(0,1)  #Cc~ con el sensor o bien las fotos concatenadas
        return next_state        

 