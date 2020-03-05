from tello_binom import *
template = cv2.imread("einstein.template.png") # любой шаблон
threshold = 0.7 # можно менять это значение
h, w, c = template.shape
start()
start_video()
while True:
    frame = get_video_frame()
    if frame is not None:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(grey, template, cv2.TM_CCOEFF_NORMED) 
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv2.imshow('Пороговое значение: ' + str(threshold), frame)
        cv2.waitKey(1)
