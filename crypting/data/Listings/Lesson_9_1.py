from tello import *

# Отображение экрана UI
def show_ui(): # Определить функцию show_ui
    print(" [ ТУР С РОБОГИДОМ ]")
    print(" ")
    print(" [w] – лететь вперед")
    print(" [a] – повернуть налево")
    print(" [d] – повернуть направо")
    print(" [z] – лететь вниз")
    print(" [x] – лететь вверх")
    print(" ")
    print("Введите команду")

# Действия по команде
def do_command(cmd):
    if cmd == "w":
        forward(20)
    if cmd == "a":
        anticlockwise(30)
    if cmd == "d":
        clockwise(30)
    if cmd == "z":
        down(20)
    if cmd == "x":
        up(20)

start() # Начать отправку команд квадрокоптеру
takeoff() # Взлет
# получение входных данных от пользователя
while True:
    show_ui()
    command = input("> ")
    if command == "":
        break # Выход из цикла
    else: # В противном случае выполните команду
        do_command(command)
print("[ До свидания! ]")
land() #Посадка
