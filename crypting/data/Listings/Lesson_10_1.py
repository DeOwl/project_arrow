from tello_binom import *

def scan(layer_radius): # Скан объектов в квадрате со стороной 3 м
    right(layer_radius)
    for i in range(3): 
        anticlockwise(90) 
        right(layer_radius * 2)
    anticlockwise(90) 
    right(layer_radius)

def next_layer(): # Переход к следующему слою
    up(20) 
    forward(25)

def layer(layer_id, layer_radius): #Сканирование слоя
    scan(layer_radius)
    print("Сканирован слой " + str(layer_id)) 
    next_layer()

start() 
takeoff()
start_video()
layer(1, 150) #Слой 1
layer(2, 125) #Слой 2
layer(3, 100) #Слой 3
print("Сканирование окончено!")
land()
stop_video()
