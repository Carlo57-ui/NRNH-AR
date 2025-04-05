import cv2
import time

# Define the path to the output directory
output_dir = "./Data CNN1/No target"

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
cv2.destroyAllWindows()