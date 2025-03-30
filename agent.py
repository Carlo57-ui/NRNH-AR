import time
import random
import cv2
import serial



#ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 115200)     #Modificar este puerto JETSON -- "/dev/ttyUSB0"  Computadora "COM10"
ser = serial.Serial(port = "COM11", baudrate = 115200)
time.sleep(1.7)  #Es necesario colocar el time para que pueda leer y enviar mensajes

class Entorno:
    def __init__(self):
        camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(0)+' ! video/x-raw, width='+str(640)+', height='+str(480)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        #cam = cv2.VideoCapture(camSet)
        
        self.state = 0

    def reset(self): # Ultrasonic sensor signal
        ser.write("M".encode())                   #Python wait a message
        time.sleep(0.05)
        in_sensor = ser.read()
        if in_sensor == b'0':                     #Always put b 
            #print("No obstacle")
            self.state = 0
        
        elif in_sensor == b'1':  
            #print("Obstacle")
            self.state = 1
    
        return self.state

    def concat(self):
        I_I = cv2.imread("2.jpg",0)
        I_F = cv2.imread("3.jpg",0)
        I_D = cv2.imread("1.jpg",0)
        
        img_concatena = cv2.hconcat([I_I,I_F,I_D])
        cv2.imwrite("cat.jpg",img_concatena) 


        return 

    def take_picture(self):
        cam = cv2.VideoCapture(0)
        ret,frame = cam.read()
        for i in [1,2,3]:
            if i == 1:
                ser.write("a".encode())     # Servo motor 0°
            elif i == 2:
                ser.write("b".encode())     # Servo motor 90°
            elif i == 3:
                ser.write("c".encode())     # Servo motor 180°     
            ent = ser.read()
            #print(ent)
            if ent == b'F':
                cv2.imwrite("%d.jpg"%i,frame) 
                print("Se toma foto ", i)
                cam.release()

    def step(self,action):
        #que realice la acción
        if action == 1:                  # Go  (1:go, 2:turn left, 3:turn right, 4:stop)
            ser.write("d".encode())
            print("go")
        elif action == 2:                # Turn left
            ser.write("e".encode())
            print("TL")
        elif action == 3:                # Turn right
            ser.write("f".encode())
            print("TR")
        elif action == 4:                # Stop   
            ser.write("g".encode())
            print("Stop")
        next_state = self.reset()        # Cc~ con el sensor o bien las fotos concatenadas
        return next_state   

    def fin(self):
        ser.close()
