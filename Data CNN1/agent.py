import RPi.GPIO as GPIO
import time

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
        

        GPIO.setmode(GPIO.BOARD)

        self.configurar_leds()
        self.configurar_botones()

    def reset(self): # Ultrasonic sensor signal
        state = random.randit(0,1)
        return state

    def configurar_botones(self):
        GPIO.setup(self.boton_0, GPIO.IN)
        GPIO.setup(self.boton_1, GPIO.IN)
        GPIO.setup(self.boton_2, GPIO.IN)
        GPIO.setup(self.boton_c8, GPIO.IN)
        

    def encender_led(self, accion):
        leds = [self.led_1, self.led_2, self.led_3, self.led_4, self.led_5, self.led_6, self.led_7, self.led_8, self.led_9]
        for led in leds:  #Apaga todos los leds
            GPIO.output(led, False)
        accion = accion - 1
        if 1 <= accion <= 9: #prende la del caso
            GPIO.output(leds[accion], True)