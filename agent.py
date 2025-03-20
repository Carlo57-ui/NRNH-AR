import time
import random
import cv2
import serial


ser = serial.Serial(
    port = "/dev/ttyACM0",              #Modificar este puerto JETSON -- "/dev/ttyACM0"  Computadora "COM3"
    baudrate = 115200)


class Entorno:
    def __init__(self):
        camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(0)+' ! video/x-raw, width='+str(640)+', height='+str(480)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        #cam = cv2.VideoCapture(camSet)
        self.cam = cv2.VideoCapture(0)

    def reset(self): # Ultrasonic sensor signal
        ser.write("M".encode())                   #Python wait a message
        in_sensor = ser.read()

        if in_sensor == b'0':                     #Always put b 
            #print("No obstacle")
            state = 0
        
        elif in_sensor == b'1':  
            #print("Obstacle")
            state = 1
    
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
                ser.write("a".encode())     # Servo motor 0°
            elif i == 2:
                a = 0
                ser.write("b".encode())     # Servo motor 90°
            elif i == 3:
                a = 0
                ser.write("c".encode())     # Servo motor 180°
 
            ret,frame = self.cam.read()

            ent = ser.read()                # input message, indicate that servo is already moved
            if ent == b'F':
                cv2.imwrite("%d.jpg"%i,frame) 
                print("Se toma foto ", i)
        #self.cam.release()

    def step(self,action):
        #que realice la acción
        if action == 1:                  # Go  (1:go, 2:turn left, 3:turn right, 4:stop)
            ser.write("d".encode())
        elif action == 2:                # Turn left
            ser.write("e".encode())
        elif action == 3:                # Turn right
            ser.write("f".encode())
        elif action == 4:                # Stop   
            ser.write("g".encode())
        next_state = self.reset()        # Cc~ con el sensor o bien las fotos concatenadas
        return next_state        