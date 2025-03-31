import cv2
import time

# Define the path to the output directory
output_dir = "./Data CNN1/Target"

# Initialize the camera
camera = cv2.VideoCapture(0)

# Capture 200 images with a 1-second delay between each
for i in range(200):
    # Capture a frame from the camera
    ret, frame = camera.read()

    # Save the frame as an image
    cv2.imwrite(f"{output_dir}/{i}.jpg", frame)

    # Wait for 1 second
    time.sleep(1)

# Release the camera
camera.release()