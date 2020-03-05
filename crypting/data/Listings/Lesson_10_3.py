from tello_binom import *
import time
import math

def takePhoto(): 
    time.sleep(1)
    photo = get_video_frame() 
    cv2.imwrite('photo%d.jpg' % time.time(), photo) 
    print("Фото сделано!")
    time.sleep(1)

def scan_circle(layer_radius, stops):
    for i in range(stops):
        side = (2 * layer_radius) * math.sin(math.pi / stops) 
        left(side)
        takePhoto() 
        clockwise(360 / stops) 
        takePhoto()

def next_layer(): # Переход к следующему слою
    up(30) 
    forward(20)

def layer(layer_id, layer_radius, stops): #Сканирование слоя
    scan_circle(layer_radius, stops)
    print("Сканирован слой " + str(layer_id)) 
    next_layer()

start() 
takeoff()
start_video()
layer(1, 160, 20) #Слой 1: 20-угольник 3.2 м в ширину, 40 снимков 
layer(2, 140, 16) #Слой 2: 16-угольник 2.8 м в ширину, 32 снимка 
layer(3, 120, 12) #Слой 3: 12-угольник 2,4 м в ширину, 24 снимка 
print("Сканирование окончено!")
land()
stop_video()
