import time
import random
import torch
import torch.nn as nn
import torch.optim as optim
from AC_models import Actor, Critica
import torch.nn.functional as F
#from agent import Entorno       #Real environment
from agent_s import Entorno      #Simulation environment
from CNN1_inf import CNN1_inf as CNN1
from CNN2_inf import CNN2_inf as CNN2
from Buffer import ReplayBuffer

# Parameters
num_episodes = 5
max_number_of_steps = 30
gamma = 0.9                   # Discount factor
learning_rate = 0.001         # Learning rate
tau = 0.1                     # Smoothing factor
policy_delay = 2              # Delay in policy update
batch_size = 1
buffer_size = 10000
llA = 0.9961                       # Learning Level A


input_size = 1
output_size = 2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Networks
Predi_actor = Actor(input_size, output_size).to(device)
Predi_critic1 = Critica(input_size, output_size).to(device)


Real_actor = Actor(input_size, output_size).to(device)          
Real_actor.load_state_dict(Predi_actor.state_dict()) 
Real_critic1 = Critica(input_size, output_size).to(device)
Real_critic1.load_state_dict(Predi_critic1.state_dict())



# Optimizers
opt_actor = optim.Adam(Predi_actor.parameters(), lr=learning_rate)
opt_critico1 = optim.Adam(Predi_critic1.parameters(), lr=learning_rate)


# Load the model if it exists
try:
  Predi_actor.load_state_dict(torch.load('weights.pth', weights_only=True))
  print("Model loaded successfully.")
except FileNotFoundError:   
  print("Model not found.")
  
# Load the buffer if it exists
try:
  Buff = ReplayBuffer(buffer_size).loads()
  print("Buffer successfully.")
except FileNotFoundError:   
  Buff = ReplayBuffer(buffer_size)
  print("Buffer not found.")


# Create an object of the Environment class
env = Entorno()
inicio = time.time()

# Training loop
for episode in range(num_episodes):
    state = env.reset()                             # Ultrasonic sensor signal (0,1)
    
    while state == 0:
        action = random.randint(1,4)                # random action (1:go, 2:turn left, 3:turn right, 4:stop)
        state, reward, next_state, terminated = env.step(action)
        #print("State: ", state)
        #print("Action: ", action)
        if terminated:
           break
        state = next_state

    for step in range(max_number_of_steps):
        Cc_t = torch.Tensor([state]).unsqueeze(1)     # Add a new dimension at position 1

        Cc, ar, next_stat = Buff.sample(batch_size, device)            # From buffer
        next_stat_t = torch.Tensor([n.item() for n in next_stat]).unsqueeze(1)

        ap = Predi_actor.forward(Cc_t)             # Predicted action
        ar = Real_actor.forward(next_stat_t)       # Real action with next_stat_t (C ̃_c)
        ap_t = torch.argmax(ap).item()
        ar_t = torch.argmax(ar).item()

        qr = Real_critic1.forward(next_stat_t, ar_t)      # Real Q with next_stat_t (C ̃_c)
        qp = Predi_critic1.forward(Cc_t, ap_t)            # Predicted Q
            
        ar_t2 = ar_t + 1
        Cc, reward, next_state, terminated = env.step(ar_t2)             # Do the action (0-3 for that reason +1)
        #print("AR: ", ar_t2)
        Buff.append((Cc,ar_t2,next_state))
        Buff.save()

        if terminated:
           break
        state = next_state

        if Buff.size() >= batch_size:
            Cc, ar, next_stat = Buff.sample(batch_size, device)
            Cc_t = torch.Tensor([c.item() for c in Cc]).unsqueeze(1)  # Convert each element of Cc to scalar
            ar_t = torch.Tensor([a.item() for a in ar]).unsqueeze(1)  # Convert each element of ar to scalar

            ap = Predi_actor.forward(Cc_t)                 # Predicted action
            ap_t = torch.argmax(ap).item()
 
            val_qp = Predi_critic1.forward(Cc_t, ap_t).detach().max(1)[0]
            val_qr = Real_critic1.forward(next_stat_t, ar_t).detach().max(1)[0]
            val_qp.requires_grad_(True)  # Enables gradient calculation for val_qp
            val_qr.requires_grad_(True)

            loss = F.mse_loss(val_qr.float(), gamma * val_qp.float())

            llA = 1 - loss
            llA = llA.item()

            opt_critico1.zero_grad()
            loss.backward()
            opt_critico1.step()

            for param, param_pred in zip(Real_critic1.parameters(), Predi_critic1.parameters()):
                param.data.copy_(tau * param_pred.data + (1 - tau) * param.data)
            for param, param_pred in zip(Real_actor.parameters(), Predi_actor.parameters()):
                param.data.copy_(tau * param_pred.data + (1 - tau) * param.data)

        print('Step: ', step)

    print('Episode:', episode, 'Learning Level A: ', llA)
    # Save the weights after each episode
    torch.save(Predi_actor.state_dict(), 'weights.pth')
    if terminated:
        fin = time.time()
        tiempo_total = fin - inicio
        print(f"Execution time: {tiempo_total:.4f} seconds")
        break
env.fin()