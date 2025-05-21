import cv2
import time
import numpy as np
import os
from agent_s import Entorno

# Create an object of the Environment class
env = Entorno()
output_dir = "./Data CNN2_s/010"

# Initialize the image counter
num = 0

# Capture images until the user presses 'c'
while True:
    # Save the frame as an image
    env.take_picture()

    #3 images concatenated
    env.concat() 
    
    # Save the concatenated image
    filename = f"{output_dir}/{num}.jpg"
    os.rename("cat.jpg", filename)
    time.sleep(1)
    print(f"Concatenated image {num}saved.")

    num += 1

    if num == 100:
        break

env.fin()

