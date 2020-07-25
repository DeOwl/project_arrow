from tello_binom import *

def start_flight(): # занятие стартовой позиции у первого участка
    takeoff()
    forward(80) # подлет к лесу
    anticlockwise(45) # поворот против часовой стрелки

def patrol_section(): # облет одного квадратного участка
    for i in range(4):
        forward(40)
        clockwise(90)

def next_section(): # подлет к следующему участку 
    forward(80)
    clockwise(90)

start() 
start_flight() 
for i in range(4): 
    patrol_section() 
    next_section() 
land()
