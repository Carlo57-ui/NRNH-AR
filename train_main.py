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
from Buffer import ReplayBuffer

# Parameters
num_episodes = 500
max_number_of_steps = 30
gamma = 0.999                 # Discount factor
learning_rate = 0.001         # Learning rate
tau = 0.05                    # Smoothing factor
policy_delay = 2              # Delay in policy update
batch_size = 32
buffer_size = 10000


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
  Predi_actor.load_state_dict(torch.load('weights.pth', weights_only=True))
  print("Model loaded successfully.")
except FileNotFoundError:   
  print("Model not found.")
  
# Load the buffer if it exists
try:
  Buff = ReplayBuffer.load()
  print("Buffer successfully.")
except FileNotFoundError:   
  Buff = ReplayBuffer(buffer_size)
  print("Buffer not found.")




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
        #observation = CNN1(img) 
        observation = CNN1('./Data CNN1/No target/10.jpg') 
        observation = observation.predicted_class      #It can be 1 or 0                  

        if observation == 1:
            terminated = True                           # It has found the object
            break
        else:
            #Cc = CNN2(img)
            Cc = CNN2('./Data CNN2/010/10.jpg')
            Cc = Cc.predicted_class                     # It can be 1-4

            ap = Real_actor.forward(Cc)                 # Predicted action
            ar = random.randint(2,3)                    # Real action, random  (2:turn left, 3:turn right)

            qr = Real_critic1.forward(Cc, ar)           # Real Q
            qp = Predi_critic1.forward(Cc, ap)          # Predicted Q
           
            next_state = env.step(action)               # Do the action
            if next_state == 0:
                next_state = 0
            else:
                img = take_pictures()
                next_state = CNN1('./Data CNN1/No target/10.jpg') 
                next_state = next_state.predicted_class      #It can be 1 or 0                  

                if next_state == 1:
                    terminated = True                           # It has found the object
                    break
                else:
                    #next_state = CNN2(img)
                    next_state = CNN2('./Data CNN2/010/10.jpg')
                    next_state = next_state.predicted_class                     # It can be 1-4

            Buff.append((Cc,ar,next_state))
            Buff.save()

            if Buff.size() >= batch_size:
                Cc,ar,next_stat = Buff.sample(batch_size, device)

            # Optimize the model
            with torch.no_grad():
                val_qp = qp(Cc, ap).detach().max(1)[0]
                val_qr = qp(Cc, ar).detach().max(1)[0]
                loss = F.mse_loss(val_t.float(), val_qp.float())

                opt_critico1.zero_grad()
                opt_critico2.zero_grad()
                loss.backward()
                opt_critico1.step()
                opt_critico2.step()
            

    print('Episodio:', episode, 'Recompensa:', episode_reward)
    # Save the weights after each episode
    torch.save(Predi_actor.state_dict(), 'weights.pth')