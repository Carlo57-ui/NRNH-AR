#from CNN1_inf import CNN1_inf as CNN1
#from CNN2_inf import CNN2_inf as CNN2

from CNN1_inf import CNN1_inf_s as CNN1_s
#from CNN2_inf import CNN2_inf_s as CNN2

#from agent import Entorno

#env = Entorno()

'''With data pictures'''

case = CNN1_s('./Data CNN1_s/No target/10.jpg')
case = case.predicted_class

#case2 = CNN2('./Data CNN2/010/10.jpg')
#case2 = case2.predicted_class

print("CASE CNN1", case)
#print("CASE CNN2", case2)


'''With robot'''
#img = env.take_picture()

#o1 = CNN1("1.jpg")
#o2 = CNN1("2.jpg")
#o3 = CNN1("3.jpg")
        
#o1 = o1.predicted_class      #It can be 1 or 0 (target or no target)
#o2 = o2.predicted_class      #It can be 1 or 0                  
#o3 = o3.predicted_class      #It can be 1 or 0  

#print("o1", o1)
#print("o2", o2)
#print("o3", o3)

#img_Cc = env.concat()                   #3 images concatenated
            
#Cc = CNN2("cat.jpg")                       # concatenated image in CNN2
#Cc = Cc.predicted_class  

#print("Cat: ", Cc)