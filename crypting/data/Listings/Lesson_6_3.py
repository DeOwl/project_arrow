from tello import *
import time
 
upperBodyCascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
lowerBodyCascade = cv2.CascadeClassifier('Haarcascade_lowerbody.xml')
# Убедитесь, что файлы XML находятся в одной папке с файлом Python
start()
start_video()
takeoff()
up(50)
while True:
    if get_video_frame() is not None:
        frame = get_video_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        upperBodies = upperBodyCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30,30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        lowerBodies = lowerBodyCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(upperBodies) >= 1:
            down(20)
            print ('распознана верхняя часть тела, лечу вниз')
        elif len(lowerBodies) >= 1:
            up(20)
            print ('распознана нижняя часть тела, лечу вверх')
        time.sleep(0.3)
