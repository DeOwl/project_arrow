from tello_binom import *
import time

start()
takeoff() # Взлет квадрокоптера
current_pad = get_mission_pad() # Запомнить номер первой карточки                 
while True: # Бесконечный цикл
    forward(30) # Вперед на 30 см
    if get_mission_pad() != current_pad: # Если обнаружена новая
        print("Обнаружена новая карточка!")
        forward(30) # Вперед на 30 см
        land() # Посадка квадрокоптера
        time.sleep(1)
        takeoff() # Взлет квадрокоптера
        current_pad = get_mission_pad() # Запомнить номер текущей 
        print("Взлет с карточки №" + str(current_pad))
        clockwise(90) # Повернуть на 90° направо
