import RPi.GPIO as GPIO
import time
import random
import cv2
import serial

'''
ser = serial.Serial(
    port = "/dev/ttyACM0",              #Modificar este puerto JETSON -- "/dev/ttyACM0"  Computadora "COM3"
    baudrate = 115200,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 2,
    xonxoff = False,
    rtscts = False,
    dsrdtr = False,
    write_timeout = 2)
'''

class Entorno:
    def __init__(self):
  
        GPIO.setmode(GPIO.BOARD)
        camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(0)+' ! video/x-raw, width='+str(640)+', height='+str(480)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        #cam = cv2.VideoCapture(camSet)
        self.cam = cv2.VideoCapture(0)

    def reset(self): # Ultrasonic sensor signal
        state = random.randint(0,1)
        return state

    def concat(self):
        I_I = cv2.imread("2.jpg",0)
        I_F = cv2.imread("3.jpg",0)
        I_D = cv2.imread("1.jpg",0)
        
        img_concatena = cv2.hconcat([I_I,I_F,I_D])
        cv2.imwrite("cat.jpg",img_concatena) 


        return 

    def take_picture(self):
        for i in [1,2,3]:
            if i == 1:
                a = 0
#               ser.write("a".encode())
            elif i == 2:
                a = 0
#               ser.write("b".encode())
            elif i == 3:
                a = 0
#               ser.write("c".encode())

            ret,frame = self.cam.read()

            cv2.imwrite("%d.jpg"%i,frame) 
            print("Se toma foto ", i)
        #self.cam.release()

    def step(self,action):
        #que realice la acción
        next_state = random.randint(0,1)  #Cc~ con el sensor o bien las fotos concatenadas
        return next_state        