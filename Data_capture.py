import cv2
import time

# Define the path to the output directory
output_dir = "./Data CNN1_s/Target"

'''
#---------REAL ROBOT----------#
# Initialize the camera
camera = cv2.VideoCapture(0)

# Initialize the image counter
image_count = 0

# Capture images until the user presses 'c'
while True:
    # Capture a frame from the camera
    ret, frame = camera.read()

    # Display the frame
    cv2.imshow("Press 'c' to capture", frame)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # If the user presses 'c', capture an image
    if key == ord("c"):
        # Save the frame as an image
        cv2.imwrite(f"{output_dir}/{image_count}.jpg", frame)
        print(f"Image {image_count} captured.")
        image_count += 1

    # If the user presses 'q', quit the program
    if key == ord("q"):
        break

# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()'''

#-------------------------------------------------------------------------------------------#

#---------SIMULATION ROBOT-----------#
import sim
import numpy as np

x = 0
def connect(port):
    sim.simxFinish(-1) 
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5)
    if clientID == 0: print("Conected with", port)
    else: print("Error conection")
    return clientID

clientID = connect(19999)



while True:
    retCode, frame1 = sim.simxGetObjectHandle(clientID,'visionSensor1',sim.simx_opmode_blocking)
    retCode2, frame2 = sim.simxGetObjectHandle(clientID,'visionSensor2',sim.simx_opmode_blocking)
    retCode3, frame3 = sim.simxGetObjectHandle(clientID,'visionSensor3',sim.simx_opmode_blocking)
    # Display the frame
    cv2.imshow("Press 'c' to capture", frame2)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # If the user presses 'c', capture an image
    if key == ord("c"):

        retCode, resolution1, imag1=sim.simxGetVisionSensorImage(clientID,frame1,1,sim.simx_opmode_oneshot_wait)
        img1 = np.array(imag1, dtype = np.uint8)
        img1.resize([resolution1[1], resolution1[0],1])

        retCode2, resolution2, imag2=sim.simxGetVisionSensorImage(clientID,frame2,1,sim.simx_opmode_oneshot_wait)
        img2 = np.array(imag2, dtype = np.uint8)
        img2.resize([resolution2[1], resolution2[0],1])
            
        retCode3, resolution3, imag3=sim.simxGetVisionSensorImage(clientID,frame3,1,sim.simx_opmode_oneshot_wait)
        img3 = np.array(imag3, dtype = np.uint8)
        img3.resize([resolution3[1], resolution3[0],1])


        img_vert1 = cv2.flip(img1,0)  
        imagen1 = img_vert1
        x += 1
        img_guardada_ent1 = cv2.imwrite(f"{output_dir}/{x}.jpg", imagen1)

        img_vert2 = cv2.flip(img2,0)  
        imagen2 = img_vert2
        x += 1
        img_guardada_ent1 = cv2.imwrite(f"{output_dir}/{x}.jpg", imagen2)

        img_vert3 = cv2.flip(img3,0)  
        imagen3 = img_vert3
        x += 1
        img_guardada_ent1 = cv2.imwrite(f"{output_dir}/{x}.jpg", imagen3)

    # If the user presses 'q', quit the program
    if key == ord("q"):
        break