import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
from bt import *
import time
import sys
import cv2


LABELS = [
    'Front/Top',
    'Left',
    'Bottom',
    'Right',
    'NoWhere'
]

video_port = 0

try:
    connection = configure_bluetooth_device()
    # Creating Connection with the devices choosen

    connection['socket'], error, msg = create_connection(connection)
    if(error):
        print(msg)
        # sys.exit(0)
except:
    print("")

try:
    video_capture = cv2.VideoCapture(video_port)
except:
    print("Try changing the camera to 0")

size = (224, 224)

prev_pred = ''
curr_pred = ''

np.set_printoptions(suppress = True)
model = tensorflow.keras.models.load_model('models/keras_model.h5')

data = np.ndarray(shape = (1, 224, 224, 3), dtype = np.float32)
while True:
    ret, frame = video_capture.read()
    cv2.imshow('Video Feed', frame)
    
    image = Image.fromarray(frame, 'RGB')
    image = image.resize(size)

    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array


    curr_pred = np.argmax(model.predict(data))
    curr_label = LABELS[curr_pred]
    print("PRED: ", curr_label)

    if(curr_pred != prev_pred):
        try:
            error, msg = send_message(connection['socket'], curr_label)
            if error:
                print("Error: sending data to the client!!")
        except:
            print("")
        

    prev_pred = curr_pred
    time.sleep(0.1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
try:
    close_connection(connection)
except:
    print("")
