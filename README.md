INSTRUCTIONS FOR USING THE NRNH-AR ALGORITHM
[![Captura-de-pantalla-2025-05-20-192920.jpg](https://i.postimg.cc/tRscHkTN/Captura-de-pantalla-2025-05-20-192920.jpg)](https://postimg.cc/G91KFkv4)

[![Imagen-de-Whats-App-2025-05-20-a-las-19-33-39-de24b800.jpg](https://i.postimg.cc/W1YrjGt0/Imagen-de-Whats-App-2025-05-20-a-las-19-33-39-de24b800.jpg)](https://postimg.cc/w1J3QsXB)

1. Make the connections shown in the image "conexion.jpg"

2. Upload the "ardu_code_ackerman" script to the Arduino Uno. You can modify this code with your agent's code.

3. Upload photos of your environment to "Data CNN1" (Real environment) or "Data CNN1_s" (Simulation environment) with "Data_capture.py" where your target is and where your target is not. The categories may vary depending on your application.

4. Upload the four cases to "Data CNN2" (Real environment) or "Data CNN2_s" (Simulation environment) with "Data_capture2.py". The categories may vary depending on your application.

5. Run "CNN1_train.py" and "CNN2_train.py" to train the CNNs.

6. Run "CNN1_inf.py" and "CNN2_inf.py" to perform inference.

7. You can test the prediction effectiveness of your CNN's training with "Try_CNNs.py"

NOTE: If you want to use it in the Real environment please use "from agent import Entorno" or if you want to use the simulation environment please use "from agen_s import Entorno".

8. Run the first stage "SSL_main.py" until you achieve a learning level of 1 for 10 consecutive episodes. Then, train "CNN2_train.py" again.

9. Run the second stage "USL_main.py" until you achieve a learning level A of 1 for 10 consecutive episodes. Then, train "CNN2_train.py" again.

10. Run the final stage "DRL_main.py" until you want to train, ideally until a learning level A of 1 for 10 consecutive episodes.
