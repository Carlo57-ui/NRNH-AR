INSTRUCTIONS FOR USING THE NRNH-AR ALGORITHM

1. Make the connections shown in the image "conexion.jpg"

2. Upload the "ardu_code_ackerman" script to the Arduino Uno. You can modify this code with your agent's code.

3. Upload photos of your environment to "Data CNN1" where your target is and where your target is not. The categories may vary depending on your application.

4. Upload the four cases to "Data CNN2". The categories may vary depending on your application.

5. Run "CNN1_train.py" and "CNN2_train.py" to train the CNNs.

6. Run "CNN1_inf.py" and "CNN2_inf.py" to perform inference.

7. Run the first stage "SSL_main.py" until you achieve a learning level of 1 for 10 consecutive episodes. Then, train "CNN2_train.py" again, then "CNN2_inf.py".

8. Run the second stage "USL_main.py" until you achieve a learning level A of 1 for 10 consecutive episodes. Then, train "CNN2_train.py" again, then "CNN2_inf.py".

9. Run the final stage "DRL_main.py" until you want to train, ideally until a learning level A of 1 for 10 consecutive episodes.
