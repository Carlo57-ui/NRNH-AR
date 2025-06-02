#CNN1 train


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from CNN_model import CNN                        # Import the model from CNN_model.py

categories = 2
# Defines the device to use (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Defines data transformations
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # Convert to grayscale
    transforms.Resize((150, 150)),                # Resize to 150x150
    transforms.ToTensor(),                        # Convert to tensor
    transforms.Normalize((0.5,), (0.5,))          # Normalizes to grayscale
])

# Load training data
train_dataset = ImageFolder("./Data CNN1_s", transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Creates the model instance and moves it to the device
model = CNN(categories).to(device)

# Define the loss function and the optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Model training
epochs = 30
for epoch in range(epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        
        # Calculate the output of the model
        outputs = model(images)

        # Calculate the loss
        loss = criterion(outputs, labels)

        # Updates the model weights
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Print training progress
        if (i + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Step [{i + 1}/{len(train_loader)}], Loss: {loss.item():.4f}')

# Saves the model weights
torch.save(model.state_dict(), "cnn1_s.pth")