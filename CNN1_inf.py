import torch
import torchvision.transforms as transforms
import os
from PIL import Image
from CNN_model import CNN  # Importa el modelo desde CNN1_model.py

# Define el dispositivo a utilizar (CPU o GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
categories = 2

# Define las transformaciones de datos
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # Convierte a escala de grises
    transforms.Resize((150, 150)),                # Redimensiona a 150x150
    transforms.ToTensor(),                        # Convierte a tensor
    transforms.Normalize((0.5,), (0.5,))          # Normaliza para escala de grises
])

# Carga el modelo y los pesos entrenados
model = CNN(categories).to(device)
model.load_state_dict(torch.load("cnn1.pth"))
model.eval()  # Pon el modelo en modo de evaluación

model_s = CNN(categories).to(device)
model_s.load_state_dict(torch.load("cnn1_s.pth"))
model_s.eval()  # Pon el modelo en modo de evaluación

class CNN1_inf:
    def __init__(self, path):
        # Realiza predicciones sobre nuevas imágenes
        with torch.no_grad():
            image_path = os.path.abspath(path)
            image = Image.open(image_path)
            
            # Aplica las transformaciones a la imagen
            image = transform(image)
            # Convierte la imagen a un tensor y mueve al dispositivo
            image = image.unsqueeze(0).to(device)
            # Realiza la predicción
            output = model(image)
            # Obtiene la clase predicha
            _, predicted_class = torch.max(output.data, 1)
            # Define los nombres de las clases
            class_names = [0, 1]  #0: No target 1: Target
            # Obtiene el nombre de la clase
            self.predicted_class = class_names[predicted_class.item()]
            # Imprime la clase predicha
            #print(f'Predicted class: {self.predicted_class}')

class CNN1_inf_s:
    def __init__(self, path):
        # Realiza predicciones sobre nuevas imágenes
        with torch.no_grad():
            image_path = os.path.abspath(path)
            image = Image.open(image_path)
            
            # Aplica las transformaciones a la imagen
            image = transform(image)
            # Convierte la imagen a un tensor y mueve al dispositivo
            image = image.unsqueeze(0).to(device)
            # Realiza la predicción
            output = model_s(image)
            # Obtiene la clase predicha
            _, predicted_class = torch.max(output.data, 1)
            # Define los nombres de las clases
            class_names = [0, 1]  #0: No target 1: Target
            # Obtiene el nombre de la clase
            self.predicted_class = class_names[predicted_class.item()]
            # Imprime la clase predicha
            #print(f'Predicted class: {self.predicted_class}')