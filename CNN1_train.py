#CNN1 train


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from CNN_model import CNN                        # Importa el modelo desde CNN_model.py

categories = 2
# Define el dispositivo a utilizar (CPU o GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define las transformaciones de los datos
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # Convierte a escala de grises
    transforms.Resize((150, 150)),                # Redimensiona a 150x150
    transforms.ToTensor(),                        # Convierte a tensor
    transforms.Normalize((0.5,), (0.5,))          # Normaliza para escala de grises
])

# Carga los datos de entrenamiento
train_dataset = ImageFolder("./Data CNN1", transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Crea la instancia del modelo y la mueve al dispositivo
model = CNN(categories).to(device)

# Define la función de pérdida y el optimizador
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Entrenamiento del modelo
epochs = 10
for epoch in range(epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        
        # Calcula la salida del modelo
        outputs = model(images)

        # Calcula la pérdida
        loss = criterion(outputs, labels)

        # Actualiza los pesos del modelo
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Imprime el progreso del entrenamiento
        if (i + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Step [{i + 1}/{len(train_loader)}], Loss: {loss.item():.4f}')

# Guarda los pesos del modelo
torch.save(model.state_dict(), "cnn1.pth")