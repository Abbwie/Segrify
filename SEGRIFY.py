#SEGRIFY

import os
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from pyfirmata2 import Arduino, SERVO
from time import sleep


model = load_model('C:/Users/Abbwie/SEGRIFY/MODEL/keras_model.h5')


port = "COM4"
pin = 8
pin2 = 9
board = Arduino(port)
board.digital[pin].mode = SERVO
board.digital[pin2].mode = SERVO


def rotate_servo(pin, angle):
    board.digital[pin].write(angle)


def rotate_servo2(pin2, angle):
    board.digital[pin2].write(angle)



waste_folder = 'C:/Users/Abbwie/SEGRIFY/MATERIALS'
waste_images = []
waste_names = []

file_list = sorted(os.listdir(waste_folder), key=lambda x: int(os.path.splitext(x)[0]))
for file in file_list:
    file_path = os.path.join(waste_folder, file)
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    if img is not None:
        if img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        waste_images.append(img)
        waste_names.append(file)


non_bio_bin_path = 'C:/Users/Abbwie/SEGRIFY/BINS/NONBIO.png'
bio_bin_path = 'C:/Users/Abbwie/SEGRIFY/BINS/BIO.png'
non_bio_bin = cv2.imread(non_bio_bin_path, cv2.IMREAD_UNCHANGED)
bio_bin = cv2.imread(bio_bin_path, cv2.IMREAD_UNCHANGED)


bg_path = 'C:/Users/Abbwie/SEGRIFY/BACKGROUND/BG.png'
background = cv2.imread(bg_path)


cap = cv2.VideoCapture(0)


def overlay_transparent(background, overlay, x, y):
    overlay_h, overlay_w = overlay.shape[:2]
    background_h, background_w = background.shape[:2]

    if x >= background_w or y >= background_h:
        return background

    h, w = min(overlay_h, background_h - y), min(overlay_w, background_w - x)
    overlay_crop = overlay[:h, :w]
    background_crop = background[y:y + h, x:x + w]

    if overlay.shape[-1] == 4:
        alpha = overlay_crop[:, :, 3] / 255.0
        for c in range(3):
            background_crop[:, :, c] = (
                    alpha * overlay_crop[:, :, c] +
                    (1 - alpha) * background_crop[:, :, c]
            )
    return background


def Servo_motor(detected_index):
    detected_index -= 1
    if detected_index == 0:
        rotate_servo(pin, 0)
    elif 1 <= detected_index <= 14:
        rotate_servo(pin, 160)
    elif 15 <= detected_index <= 30:
        rotate_servo(pin, 60)





def main():
    global detected_index

    while True:
        ret, frame = cap.read()


        resized_frame = cv2.resize(frame, (650, 550))
        display_background = background.copy()
        display_background[220:220 + 550, 170:170 + 650] = resized_frame

        # Preprocess the frame for the AI model
        input_img = cv2.resize(frame, (224, 224))
        img_tensor = image.img_to_array(input_img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.0


        prediction = model.predict(img_tensor)
        if prediction.size > 0:
            detected_index = np.argmax(prediction[0])
            confidence = prediction[0][detected_index]

            detected_index -= 1



            if 0 <= detected_index < len(waste_images):
                waste_img = cv2.resize(waste_images[detected_index], (300, 300))
                if detected_index <= 14:  # Non-biodegradable
                    bin_img = cv2.resize(non_bio_bin, (300, 300))
                    detected_class = "Non-biodegradable"
                else:  # Biodegradable
                    bin_img = cv2.resize(bio_bin, (300, 300))
                    detected_class = "Biodegradable"

                # Overlay images
                display_background[180:480, 1000:1300] = waste_img
                display_background = overlay_transparent(display_background, bin_img, 1000, 500)

                Detection = f"SEGRIFY HAS DETECTED: {waste_names[detected_index]} ({detected_class}) - {confidence * 100:.2f}%"
                cv2.putText(display_background, Detection, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            Servo_motor(detected_index)

        # Display the updated frame
        cv2.imshow("Waste Segregation System", display_background)


        if cv2.waitKey(1) & 0xFF == ord('x'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


