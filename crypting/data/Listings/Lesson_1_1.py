﻿from tello import *

start()
takeoff() # Взлет квадрокоптера
forward(400) # Вперед на 400 см
clockwise(90) # Поворот по часовой стрелке на 90 градусов
forward(350) # Вперед на 350 см
land() # Посадка квадрокоптера
