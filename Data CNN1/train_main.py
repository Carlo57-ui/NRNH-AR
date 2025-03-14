import time
import random
import torch
import torch.nn as nn
import torch.optim as optim
from AC_models import Actor, Critica
import torch.nn.functional as F
from agent import Entorno
from CNN1_inf import CNN1_inf as CNN1
from CNN2_inf import CNN2_inf as CNN2
# Parameters
num_episodes = 500
max_number_of_steps = 30
gamma = 0.999                 # Discount factor
learning_rate = 0.001         # Learning rate
tau = 0.05                    # Smoothing factor
policy_delay = 2              # Delay in policy update
batch_size = 32
replay_memory_size = 10000

input_size = 1
output_size = 2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Networks
Real_actor = Actor(input_size, output_size).to(device)
Real_critic1 = Critica(input_size, output_size.to(device))
Real_critic2 = Critica(input_size, output_size).to(device)


Predi_actor = Actor(input_size, output_size).to(device)
Predi_actor.load_state_dict(Real_actor.state_dict())      # Copy weights from the original

Predi_critic1 = Critica(input_size, output_size).to(device)
Predi_critic1.load_state_dict(Real_actor.state_dict())

Predi_critic2 = Critica(input_size, output_size).to(device)
Predi_critic2.load_state_dict(Real_critic2.state_dict())

# Optimizers
opt_actor = optim.Adam(Real_actor.parameters(), lr=learning_rate)
opt_critico1 = optim.Adam(Real_critic1.parameters(), lr=learning_rate)
opt_critico2 = optim.Adam(Real_critic2.parameters(), lr=learning_rate)

# Initialize the global reward
recompensa_global = 0

# Load the model if it exists
try:
  Real_actor.load_state_dict(torch.load('weights.pth', weights_only=True))
  print("Model loaded successfully.")
except FileNotFoundError:   
  print("Model not found.")
  



def take_pictures():
    img = './Data CNN1/No target/10.jpg' #código para tomar 3 fotos y concatenarlas

    return img


def get_action(state, episode):
    
    if state == 0:
        return random.randint(1,4)     # random action (1:go, 2:turn left, 3:turn right, 4:stop)
    else:
        return 4                       # action 4
        

# Create an object of the Environment class
env = Entorno()


# Bucle de entrenamiento
for episode in range(num_episodes):
    state = env.reset()                                 # Ultrasonic sensor signal
    episode_reward = 0

    while state == 0:
        action = get_action(state, episode)
        state = env.reset()

    for step in range(max_number_of_steps):
        action = get_action(state, episode)
        img = take_pictures()
        observation = CNN1(img)                        

        if observation == 1:
            terminated = True                           # It has found the object
        else:
            Cc = CNN2(img)

        next_state, reward, terminated, truncated = env.step(action)
        episode_reward = episode_reward + reward
        update_Q(state, action, reward, next_state, done)
        state = next_state
        
        if done:
            break

    print('Episodio:', episode, 'Recompensa:', episode_reward)
    # Save the weights after each episode
    torch.save(policy_net.state_dict(), 'pesosQ.pth')