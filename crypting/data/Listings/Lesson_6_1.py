from tello import *
import time

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Убедитесь, что файл XML находится в одной папке с файлом Python
# Инициализация переменные
faceCount = 0 # Текущее количество найденных лиц
maxFaces = 0 # Максимальное количество посчитанных лиц
start()
start_video()
takeoff()
up(120)
# Подсчитываем лица, пока они распознаются
while True:
    if get_video_frame() is not None: # Проверяем, получен ли кадр
        frame = get_video_frame() # Получить видеокадр
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Перевести кадр в режим оттенков серого
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30,30),
            flags = cv2.CASCADE_SCALE_IMAGE
            ) # Поиск лиц в кадре с использованием данных XML каскада лиц
        faceCount = len(faces) # Текущее количество найденных лиц
        if maxFaces == faceCount and faceCount != 0: # Количество лиц не изменилось
            print('окончательный счет: ' + str(maxFaces))
            land() 
            stop_video()
            break
        if maxFaces < faceCount: # Распознано большее количество лиц
            print(str(faceCount - maxFaces) + ' найдено больше лиц!')
            maxFaces = faceCount # Новое макс. количество найденных лиц
            backward(80) # Перемещение назад для поиска новых лиц
            time.sleep(4)
