from tello import *

start()
takeoff() # Взлет
up(60) # Дополнительно: вверх до высоты канатов
i = 0 # Обнулить счетчик
while True: # Бесконечный цикл
    up(40) # Вверх
    if i % 2 == 0: # Если номер петли четный
        right(100) # Вправо
        down(80) # Вниз
        right(100) # Вправо
    else: # Если номер петли нечетный
        left(100) # Влево
        down(80) # Вниз
        left(100) # Влево
    up(40) # Вверх
    forward(40) # Вперед к следующему витку
    i += 1 # Увеличить значение счетчика
    answer = input("Продолжать? ") # Получить ответ от пользователя
    if answer == "нет": # Если ответ "нет"
        break # Выйти из цикла 
land() # Посадка
