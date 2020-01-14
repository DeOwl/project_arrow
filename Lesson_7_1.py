from tello import *
import time
import cv2

artworks = ["einstein.template.png", "monalisa.template.png", "dali.template.png"]

def check_next_template(file_name):
    template = cv2.imread(file_name, 0)
    time.sleep(1)
    for i in range(20):
        time.sleep(0.5)
        if get_video_frame() is not None:
            frame = get_video_frame()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            for list_of_values in result:
                for value in list_of_values:
                    if value >= threshold:
                        return True
    # Если  программа дошла сюда, соответствие не найдено после 20 попыток
    return False

start()
start_video()
takeoff()
up(100)
for art in artworks:
    result = check_next_template(art)
    print(art + " все еще находится в галерее? " + str(result)) 
    if not result:
        print(art + " украдено!")
        break
    right(100)
land()
stop_video()
