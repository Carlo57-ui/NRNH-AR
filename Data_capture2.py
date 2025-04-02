import cv2
import time
import numpy as np

# Define the path to the output directory
output_dir = "./Data CNN2/010"

# Initialize the camera
camera = cv2.VideoCapture(1)

# Initialize the image counter
image_count = 0
num = 0

# Initialize a list to store the captured images
images = []

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
        cv2.imwrite(f"{image_count}.jpg", frame)
        print(f"Image {image_count} captured.")

        # Add the captured image to the list
        images.append(frame)

        # Increment the image counter
        image_count += 1

        # If 3 images have been captured, concatenate them and save the result
        if image_count == 3:
            # Concatenate the images horizontally
            concatenated_image = np.concatenate(images, axis=1)

            # Save the concatenated image
            cv2.imwrite(f"{output_dir}/{num}.jpg", concatenated_image)
            print(f"Concatenated image {num}saved.")
            num += 1
            
            # Reset the image counter and the image list
            image_count = 0
            images = []

    # If the user presses 'q', quit the program
    if key == ord("q"):
        break

# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()