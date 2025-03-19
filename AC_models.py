
import torch
import torch.nn as nn
import torch.nn.functional as F

class Actor(nn.Module):
  def __init__(self, input_size, output_size):
    super(Actor, self).__init__()
    self.fc1 = nn.Linear(input_size, 250)
    self.fc2 = nn.Linear(250, 200)
    self.fc4 = nn.Linear(200, output_size)    
    self.relu = nn.ReLU()
    self.softmax = nn.Softmax(dim=1)

  def forward(self, x):
    x = self.relu(self.fc1(x))
    x = self.relu(self.fc2(x))
    x = self.fc4(x)
    x = self.softmax(x)
    return x

class Critica(nn.Module):
  def __init__(self, input_size, output_size):
    super(Critica, self).__init__()
    self.fc1 = nn.Linear(input_size + output_size, 250)
    self.fc2 = nn.Linear(250, 200)
    self.fc3 = nn.Linear(200, 1)
    self.relu = nn.ReLU()


  def forward(self, x, y):
      concatena = torch.cat([x, torch.tensor(y).repeat(1, 2)], dim=1)   
      Q = self.relu(self.fc1(concatena))
      Q = self.relu(self.fc2(Q))
      Q = F.sigmoid(self.fc3(Q))
      
      return Q
