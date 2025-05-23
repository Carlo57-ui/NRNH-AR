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

# Bucle de entrenamiento
for episode in range(num_episodes):
    state = env.reset()                             # Ultrasonic sensor signal (0,1)
    
    while state == 0:
        action = random.randint(1,4)                # random action (1:go, 2:turn left, 3:turn right, 4:stop)
        env.step(action)
        state = env.reset()
        print("State: ", state)
        print("Action: ", action)
        time.sleep(1)

    env.step(4)                                 # stop
    env.step(5)                                 # back

    for step in range(max_number_of_steps):
        
        img = env.take_picture()

        o1 = CNN1("1.jpg")
        o2 = CNN1("2.jpg")
        o3 = CNN1("3.jpg")
        
        o1 = o1.predicted_class      #It can be 1 or 0 (target or no target)
        o2 = o2.predicted_class      #It can be 1 or 0                  
        o3 = o3.predicted_class      #It can be 1 or 0                  
           

        if o1 == 1 or o2 == 1 or o3 == 1:                                
            terminated = True                           # It has found the object
            print("The objetive has been find")
            r = 10                                       # reward if find the target

            break
        else:
            img_Cc = env.concat()                   #3 images concatenated
            
            Cc = CNN2("cat.jpg")                       # concatenated image in CNN2
            Cc = Cc.predicted_class                    # It can be 1-4
            Cc_t = torch.Tensor([Cc]).unsqueeze(1)     # Agrega una nueva dimensión en la posición 1

            Cc_b, ar_b, next_state_b = Buff.sample(batch_size, device)            # From buffer
            next_stat_t = torch.Tensor([n.item() for n in next_state_b]).unsqueeze(1)

            ap = Predi_actor.forward(Cc_t)             # Predicted action
            ar = Real_actor.forward(next_stat_t)       # Real action with next_stat_t (C ̃_c)
            ap_t = torch.argmax(ap).item()
            ar_t = torch.argmax(ar).item()

            qr = Real_critic1.forward(next_stat_t, ar_t)      # Real Q with next_stat_t (C ̃_c)
            qp = Predi_critic1.forward(Cc_t, ap_t)            # Predicted Q

            ar_t2 = ar_t + 1
            r1 = -1                      # state reward
            env.step(ar_t2)              # Do the action
            next_state = env.reset()     # Ultrasonic sensor signal (0,1)

            #print("Real action: ", ar_t2)
            time.sleep(1)  #Time to do the action

            if next_state == 0:
                next_state = 0
                r2 = 5                   # next_state reward
                r= r1 + r2
                break
            else:
                env.step(4)
                env.step(5) 

                img = env.take_picture()
                o1 = CNN1("1.jpg")
                o2 = CNN1("2.jpg")
                o3 = CNN1("3.jpg")
                
                o1 = o1.predicted_class      #It can be 1 or 0 (target or no target)
                o2 = o2.predicted_class      #It can be 1 or 0                  
                o3 = o3.predicted_class      #It can be 1 or 0                  
                                

                if o1 == 1 or o2 == 1 or o3 == 1:
                    next_state = 0           #It can be 1 or 0 (target or no target)
                    terminated = True                           # It has found the object
                    print("The objective has been find")
                    r2 = 3                   # next_state reward
                    r = r1 + r2 - step * dis_t
                    break
                else:
                    img_Cc = env.concat()                   #3 images concatenated
                    next_state = CNN2("cat.jpg")                       # concatenated image in CNN2
                    next_state = next_state.predicted_class                     # It can be 1-4
                    print("Next_state: ",next_state)
                    r2 = -1                 # next_state reward
        
        Buff.append((Cc,ar_t2,next_state))
        Buff.save()

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

            r = r1 + r2 - dis_t * step
            
            loss = F.mse_loss(val_qp.float(), (r1 + gamma * val_qr.float()))
            print("loss: ", loss)
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
        reward = reward + r

    reward = reward + r
    print('Episodio:', episode, 'Learning Level A: ', llA, 'Reward: ', reward)
    # Save the weights after each episode
    torch.save(Predi_actor.state_dict(), 'weights_s.pth')
    reward = 0
    if terminated:
        break

env.fin()    #Activate when use Real environment