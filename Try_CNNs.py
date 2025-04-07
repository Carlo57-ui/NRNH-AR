from CNN1_inf import CNN1_inf as CNN1
from CNN2_inf import CNN2_inf as CNN2

case = CNN1('./Data CNN1/No target/10.jpg')
case = case.predicted_class

case2 = CNN2('./Data CNN2/111/10.jpg')
case2 = case2.predicted_class

print("CASE CNN1", case)
print("CASE CNN2", case2)
