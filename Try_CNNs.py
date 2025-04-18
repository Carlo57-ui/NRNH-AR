from CNN1_inf import CNN1_inf as CNN1
from CNN2_inf import CNN2_inf as CNN2

'''With data pictures'''

case = CNN1('./Data CNN1/No target/10.jpg')
case = case.predicted_class

case2 = CNN2('./Data CNN2/010/10.jpg')
case2 = case2.predicted_class

print("CASE CNN1", case)
print("CASE CNN2", case2)


'''With robot'''
import cv2
cam = cv2.VideoCapture(0)
ret,frame = cam.read()
cv2.imwrite("TryCNN.jpg",frame) 
cam.release()

case = CNN1('TryCNN.jpg')
case = case.predicted_class

print("CASE CNN1", case)