import torch
import torchvision.transforms as transforms
import os
from PIL import Image
from CNN_model import CNN  # Import the model from CNN_model.py

# Defines the device to use (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
categories = 4

# Defines data transformations
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # Convert to grayscale
    transforms.Resize((150, 150)),                # Resize to 150x150
    transforms.ToTensor(),                        # Convert to tensor
    transforms.Normalize((0.5,), (0.5,))          # Normalizes to grayscale
])

# Load the model and trained weights
model = CNN(categories).to(device)
model.load_state_dict(torch.load("cnn2.pth"))
model.eval()  # Put the model in evaluation mode

model_s = CNN(2).to(device)
model_s.load_state_dict(torch.load("cnn2_s.pth"))
model_s.eval()  # Put the model in evaluation mode

class CNN2_inf:
    def __init__(self, path):
        # Make predictions about new images
        with torch.no_grad():
            image_path = os.path.abspath(path)
            image = Image.open(image_path)
            
            # Apply the transformations to the image
            image = transform(image)
            # Converts the image to a tensor and moves it to the device
            image = image.unsqueeze(0).to(device)
            # Make the prediction
            output = model(image)
            # Gets the predicted class
            _, predicted_class = torch.max(output.data, 1)
            # Defines the names of the classes
            class_names = [1, 2, 3, 4]  #1:010 2:011 3:110 4:111
            # Gets the name of the class
            self.predicted_class = class_names[predicted_class.item()]
            # Print the predicted class
            #print(f'Predicted class: {self.predicted_class}')

class CNN2_inf_s:
    def __init__(self, path):
        # Make predictions about new images
        with torch.no_grad():
            image_path = os.path.abspath(path)
            image = Image.open(image_path)
            
            # Apply the transformations to the image
            image = transform(image)
            # Converts the image to a tensor and moves it to the device
            image = image.unsqueeze(0).to(device)
            # Make the prediction
            output = model_s(image)
            # Gets the predicted class
            _, predicted_class = torch.max(output.data, 1)
            # Defines the names of the classes
            class_names = [1, 2]  #1:010 2:011 3:110 4:111
            # Gets the name of the class
            self.predicted_class = class_names[predicted_class.item()]
            # Print the predicted class
            #print(f'Predicted class: {self.predicted_class}')
