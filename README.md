This project was from grade 10 that is a prototype for a real AI waste analyzer. Instead of using real objects for it, it makes use of cards first to test the efficiency of an AI machine learning model Keras.
It makes use of the coding language python and the openCV library. The training of the model was set in Teachable Machine, A website where you can train your models on image, sound and pose recognition and uploaded in the
python project. 
The webcam will detect what waste it is and I have made use of a servomotor to make a hardware bin that open its lid to the correct bin.



Example:
>If detected index is 1.png (plastic straws) Show plastic straw and what bin it should be placed and rotate the lid of the non biodegredable bin to open it.
-----

The cards are labeled accordingly
> 1-15 > Non biodegredable

> 16-30 > Biodegredable
-----
This is because we had limited time of coding this project and therefore having fixed numbers for this, makes it easier for me to draw the algorithm. Take note that this research focuses on the efficiency of the model especially pin pointing on its classification rate
TAKE NOTE: Python always starts with zero, but this project starts with Index 1 therefore please do not erase the : detected_index == -1



Servomotor - Please download firmata in your Arduino IDE to connect it to python


Dummy explanation (your angle may depend on what placement your servomotor is)
------------
>if detected index 0 - show no image
-------------
 >if 1<= detected index <=15 - slide the servomotor to the non biodegredable
 ------
 >if 15<= detected index <=30 - - slide the servomotor to the biodegredable
 -------------
