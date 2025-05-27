import time
import random
import torch
import torch.nn as nn
import torch.optim as optim
from AC_models import Actor, Critica
import torch.nn.functional as F
#from agent import Entorno       #Real environment
from agent_s import Entorno      #Simulation environment
from Buffer import ReplayBuffer

# Parameters
num_episodes = 100
max_number_of_steps = 30
gamma = 0.9                   # Discount factor
learning_rate = 0.001         # Learning rate
tau = 0.1                     # Smoothing factor
policy_delay = 2              # Delay in policy update
batch_size = 1
buffer_size = 10000
llA = 0.999                    # Learning Level A
dis_t = 0.1                    # Discount time of reward
reward = 0
ep_rew = 0
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
  Predi_actor.load_state_dict(torch.load('weights_s.pth', weights_only=True))
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
terminated = False
inicio = time.time()

# Bucle de entrenamiento
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
        Cc_b, ar_b, next_state_b = Buff.sample(batch_size, device)            # From buffer
        next_stat_t = torch.Tensor([n.item() for n in next_state_b]).unsqueeze(1)
        Cc_b_t = torch.Tensor([c.item() for c in Cc_b]).unsqueeze(1)

        ap = Predi_actor.forward(Cc_b_t)             # Predicted action
        ar = Real_actor.forward(next_stat_t)       # Real action with next_stat_t (C ̃_c)
        ap_t = torch.argmax(ap).item()
        ar_t = torch.argmax(ar).item()

        qr = Real_critic1.forward(next_stat_t, ar_t)      # Real Q with next_stat_t (C ̃_c)
        qp = Predi_critic1.forward(Cc_b_t, ap_t)            # Predicted Q
        ar_t2 = ar_t + 1
        #print("Real a", ar_t2)
        state, reward, next_state, terminated = env.step(ar_t2)              # Do the action          
        
        Cc = Cc_b_t.item()
        Buff.append((Cc,ar_t2,next_state))
        Buff.save()
        if terminated:
           break

        if Buff.size() >= batch_size:
            Cc, ar, next_stat = Buff.sample(batch_size, device)
            Cc_t = torch.Tensor([c.item() for c in Cc]).unsqueeze(1)  # Convierte cada elemento de Cc a escalar
            ar_t = torch.Tensor([a.item() for a in ar]).unsqueeze(1)  # Convierte cada elemento de ar a escalar

            ap = Predi_actor.forward(Cc_t)                 # Predicted action
            ap_t = torch.argmax(ap).item()
 
            val_qp = Predi_critic1.forward(Cc_t, ap_t).detach().max(1)[0]
            val_qr = Real_critic1.forward(next_stat_t, ar_t).detach().max(1)[0]
            val_qp.requires_grad_(True)  # Habilita el cálculo de gradiente para val_qp
            val_qr.requires_grad_(True)
            
            loss = F.mse_loss(val_qp.float(), (reward + gamma * val_qr.float()))
            llA = loss
            llA = llA.item()

            if llA > 1:
                llA = 1
            elif llA < 0:
                llA = 0

            opt_critico1.zero_grad()
            loss.backward()
            opt_critico1.step()

            for param, param_pred in zip(Real_critic1.parameters(), Predi_critic1.parameters()):
                param.data.copy_(tau * param_pred.data + (1 - tau) * param.data)
            for param, param_pred in zip(Real_actor.parameters(), Predi_actor.parameters()):
                param.data.copy_(tau * param_pred.data + (1 - tau) * param.data)

        print('Step: ', step,"Reward: ", reward)  
        ep_rew = ep_rew + reward
    print('Episodio:', episode, 'Learning Level A: ', llA, 'Reward: ', ep_rew)
    # Save the weights after each episode
    torch.save(Predi_actor.state_dict(), 'weights_s.pth')
    
    if terminated:
        fin = time.time()
        tiempo_total = fin - inicio
        print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
        break

env.fin()    #Activate when use Real environment