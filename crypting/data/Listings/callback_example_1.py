from tello_binom import *
from tello_modules.laser import *
from time import sleep

start()
start_video()
laser_on()

clockwise(90)
Lamp1('r')
beep_on()
sleep(1)
beep_off()

clockwise(90)
Lamp2('r')
beep_on()
sleep(1)
beep_off()

clockwise(90)
Lamp3('r')
beep_on()
sleep(1)
beep_off()

clockwise(90)
Lamp4('r')
beep_on()
sleep(1)
beep_off()

land()
stop_video()
reset_all()
