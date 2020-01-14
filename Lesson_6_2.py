from tello import *
import time

eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
# Убедитесь, что файл XML находится в одной папке с файлом Python
start()
start_video()
takeoff()
up(100)
while True:
    if get_video_frame() is not None:
        frame = get_video_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eyeCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30,30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        print('найдены глаза: ' + str(len(eyes)))
        if len(eyes) >= 2:
            flip_forward()
        time.sleep(0.3)
