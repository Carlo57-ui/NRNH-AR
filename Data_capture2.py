import cv2
import time
import numpy as np
import os
from agent import Entorno

# Create an object of the Environment class
env = Entorno()
output_dir = "./Data CNN2/111"

# Initialize the image counter
num = 0

# Capture images until the user presses 'c'
while True:
    # Save the frame as an image
    img = env.take_picture()

    #3 images concatenated
    img_Cc = env.concat() 
    
    # Save the concatenated image
    filename = f"{output_dir}/{num}.jpg"
    os.rename("cat.jpg", filename)
    time.sleep(1)
    print(f"Concatenated image {num}saved.")

    num += 1

    if num == 100:
        break

env.fin()
