import sim
import sympy as sp
import numpy as np
import time
import random as ra
from timeit import default_timer
import cv2                      
import matplotlib.pyplot as plt 

#Agregar en coppelia simRemoteApi.start(19999)
def connect(port):
    sim.simxFinish(-1) 
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5)
    if clientID == 0: print("Conectado a", port)
    else: print("No se pudo conectar")
    return clientID

clientID = connect(19999)

class Entorno():
    def __init__(self):
        self.retCode, self.sensor=sim.simxGetObjectHandle(clientID,'Sensor',sim.simx_opmode_blocking)
        self.state = 0
        self.retCode, self.frame1 = sim.simxGetObjectHandle(clientID,'visionSensor1',sim.simx_opmode_blocking)
        self.retCode2, self.frame2 = sim.simxGetObjectHandle(clientID,'visionSensor2',sim.simx_opmode_blocking)
        self.retCode3, self.frame3 = sim.simxGetObjectHandle(clientID,'visionSensor3',sim.simx_opmode_blocking)
        self.retCode4, self.m1=sim.simxGetObjectHandle(clientID,'motor_joint',sim.simx_opmode_blocking)
        self.retCode, self.m2=sim.simxGetObjectHandle(clientID,'steer_joint',sim.simx_opmode_blocking)
        self.v = 3 #Velocidad de motores

    
    def reset(self):
        
        self.retCode,self.estado, self.coordenadas, self.objeto, self.vector=sim.simxReadProximitySensor(clientID,self.sensor,sim.simx_opmode_streaming)
        if self.estado == False:                     #Always put b 
            #print("No obstacle")
            self.state = 0
        
        elif self.estado == True:  
            #print("Obstacle")
            self.state = 1
        return self.state

    def concat(self):
        I_I = cv2.imread("1.jpg",0)
        I_F = cv2.imread("2.jpg",0)
        I_D = cv2.imread("3.jpg",0)
        
        img_concatena = cv2.hconcat([I_I,I_F,I_D])
        cv2.imwrite("cat.jpg",img_concatena) 
        return

    def take_picture(self): #Toma foto de lo que observa
        
        retCode, resolution1, imag1=sim.simxGetVisionSensorImage(clientID,self.frame1,1,sim.simx_opmode_oneshot_wait)
        img1 = np.array(imag1, dtype = np.uint8)
        img1.resize([resolution1[1], resolution1[0],1])

        retCode2, resolution2, imag2=sim.simxGetVisionSensorImage(clientID,self.frame2,1,sim.simx_opmode_oneshot_wait)
        img2 = np.array(imag2, dtype = np.uint8)
        img2.resize([resolution2[1], resolution2[0],1])
        
        retCode3, resolution3, imag3=sim.simxGetVisionSensorImage(clientID,self.frame3,1,sim.simx_opmode_oneshot_wait)
        img3 = np.array(imag3, dtype = np.uint8)
        img3.resize([resolution3[1], resolution3[0],1])


        img_vert1 = cv2.flip(img1,0)  #Voltea la imagen en vertical
        imagen1 = img_vert1
        x = 1
        img_guardada_ent1 = cv2.imwrite('E:/Doctorado/Investigacion/Jetson/RedesNeuronales/NRNH-AR/%d.jpg'%x, imagen1)

        img_vert2 = cv2.flip(img2,0)  #Voltea la imagen en vertical
        imagen2 = img_vert2
        y = 2
        img_guardada_ent1 = cv2.imwrite('E:/Doctorado/Investigacion/Jetson/RedesNeuronales/NRNH-AR/%d.jpg'%y, imagen2)

        img_vert3 = cv2.flip(img3,0)  #Voltea la imagen en vertical
        imagen3 = img_vert3
        z = 3
        img_guardada_ent1 = cv2.imwrite('E:/Doctorado/Investigacion/Jetson/RedesNeuronales/NRNH-AR/%d.jpg'%3, imagen3)


    def step(self,action):
        #que realice la acción
        if action == 1:                  # Go  (1:go, 2:turn left, 3:turn right, 4:stop)
            retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, self.v, sim.simx_opmode_oneshot)
            retCode = sim.simxSetJointTargetPosition(clientID, self.m2, 0, sim.simx_opmode_oneshot)
            print("go")
            
        elif action == 2:                # Turn left
            for i in range(3):
                retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, -self.v, sim.simx_opmode_oneshot)
                retCode = sim.simxSetJointTargetPosition(clientID, self.m2, -0.3, sim.simx_opmode_oneshot)
                time.sleep(1)
                retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, self.v, sim.simx_opmode_oneshot)
                retCode = sim.simxSetJointTargetPosition(clientID, self.m2, 0.3, sim.simx_opmode_oneshot)
                time.sleep(1)
            retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, 0, sim.simx_opmode_oneshot)
            retCode = sim.simxSetJointTargetPosition(clientID, self.m2, 0, sim.simx_opmode_oneshot)
            print("TL")
            
        elif action == 3:                # Turn right
            for i in range(3):
                retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, -self.v, sim.simx_opmode_oneshot)
                retCode = sim.simxSetJointTargetPosition(clientID, self.m2, 0.3, sim.simx_opmode_oneshot)
                time.sleep(1)
                retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, self.v, sim.simx_opmode_oneshot)
                retCode = sim.simxSetJointTargetPosition(clientID, self.m2, -0.3, sim.simx_opmode_oneshot)
                time.sleep(1)
            retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, 0, sim.simx_opmode_oneshot)
            retCode = sim.simxSetJointTargetPosition(clientID, self.m2, 0, sim.simx_opmode_oneshot)
            print("TR")
            
        elif action == 4:                # Stop   
            retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, 0, sim.simx_opmode_oneshot)
            retCode = sim.simxSetJointTargetPosition(clientID, self.m2, 0, sim.simx_opmode_oneshot)
            print("Stop")
            
        elif action == 5:                # Back  
            retCode = sim.simxSetJointTargetVelocity(clientID, self.m1, -self.v, sim.simx_opmode_oneshot)
            retCode = sim.simxSetJointTargetPosition(clientID, self.m2, 0, sim.simx_opmode_oneshot)
            print("Back")
        next_state = self.reset()        # Cc~ con el sensor o bien las fotos concatenadas
        
        return next_state

    def fin(self):
        # Reinicia el entorno
        sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot_wait)
        sim.simxStopSimulation(clientID,sim.simx_opmode_oneshot_wait)
        
env = Entorno()
env.take_picture()        