import torch
import torchvision.transforms as transforms
import os
from PIL import Image
from CNN_model import CNN  # Import the model from CNN1_model.py

# Defines the device to use (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
categories = 2

# Defines data transformations
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # Convert to grayscale
    transforms.Resize((150, 150)),                # Redimensiona a 150x150
    transforms.ToTensor(),                        # Convert to tensor
    transforms.Normalize((0.5,), (0.5,))          # Normaliza para escala de grises
])

# Load the model and trained weights
model = CNN(categories).to(device)
model.load_state_dict(torch.load("cnn1.pth"))
model.eval()  # Put the model in evaluation mode

model_s = CNN(categories).to(device)
model_s.load_state_dict(torch.load("cnn1_s.pth"))
model_s.eval()  # Put the model in evaluation mode

class CNN1_inf:
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
            class_names = [0, 1]  #0: No target 1: Target
            # Gets the name of the class
            self.predicted_class = class_names[predicted_class.item()]
            # Print the predicted class
            #print(f'Predicted class: {self.predicted_class}')

class CNN1_inf_s:
    def __init__(self, path):
        # Make predictions about new images
        with torch.no_grad():
            image_path = os.path.abspath(path)
            image = Image.open(image_path)
            
            # Apply the transformations to the image
            image = transform(image)
            # Converts the image to a tensor and moves it to the device
            image = image.unsqueeze(0).to(device)
            # Realiza la predicción
            output = model_s(image)
            # Gets the predicted class
            _, predicted_class = torch.max(output.data, 1)
            # Defines the names of the classes
            class_names = [0, 1]  #0: No target 1: Target
            # Gets the name of the class
            self.predicted_class = class_names[predicted_class.item()]
            # Print the predicted class
            #print(f'Predicted class: {self.predicted_class}')