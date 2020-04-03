import os
import serial.tools.list_ports


ser = None
connection_type = None
def connect_eco_sensor():
    global ser, connection_type
    try:
        if ser:
            ser.close()
        port_name = None
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Prolif" in p.manufacturer:
                port_name = p.device
                break
                # определение порта
        if port_name:
            ser = serial.Serial(port_name)
            ser.baudrate = 115200
            connection_type = 1
    except Exception:
        return False
    return True if ser else False

def get_data():
    global ser, connection_type
    if ser:

        line = str(ser.readline())[4:-3].split()
        if connection_type == 1:
            res = {}
            res['Температура, \u00b0С'] = line[1][2:]
            res['Атм. давление, мм рт.ст.'] = line[2][2:]
            res['Отн. влажность, %'] = line[3][2:]
            res['Индекс качества воздуха'] = line[4][5:]
            res['Индекс уровня CO2'] = line[5][4:]
            res['Уровень освещенности'] = line[6][6:]
            return res
    return None


def Lamp1(color="", state=False):
    if connection_type == 2 and ser:
        ser.write(bytes('L1=0', 'utf-8'))
        ser.write(bytes('L2=0', 'utf-8'))
        if state:
            if color == "red":
                ser.write(bytes('L1=1', 'utf-8'))
            elif color == "green":
                ser.write(bytes('L2=1', 'utf-8'))
            elif color == "yellow":
                ser.write(bytes('L1=1', 'utf-8'))
                ser.write(bytes('L2=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if ser:
            print("wrong module connected")
        else:
            print("no module connected")


def Lamp2(color="", state=False):
    if connection_type == 2 and ser:
        ser.write(bytes('L3=0', 'utf-8'))
        ser.write(bytes('L4=0', 'utf-8'))
        if state:
            if color == "red":
                ser.write(bytes('L4=1', 'utf-8'))
            elif color == "green":
                ser.write(bytes('L3=1', 'utf-8'))
            elif color == "yellow":
                ser.write(bytes('L3=1', 'utf-8'))
                ser.write(bytes('L4=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if ser:
            print("wrong module connected")
        else:
            print("no module connected")

def Lamp3(color="", state=False):
    if connection_type == 2 and ser:
        ser.write(bytes('L5=0', 'utf-8'))
        ser.write(bytes('L6=0', 'utf-8'))
        if state:
            if color == "red":
                ser.write(bytes('L6=1', 'utf-8'))
            elif color == "green":
                ser.write(bytes('L5=1', 'utf-8'))
            elif color == "yellow":
                ser.write(bytes('L6=1', 'utf-8'))
                ser.write(bytes('L5=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if ser:
            print("wrong module connected")
        else:
            print("no module connected")


def Lamp4(color="", state=False):
    if connection_type == 2 and ser:
        ser.write(bytes('L7=0', 'utf-8'))
        ser.write(bytes('L8=0', 'utf-8'))
        if state:
            if color == "red":
                ser.write(bytes('L7=1', 'utf-8'))
            elif color == "green":
                ser.write(bytes('L8=1', 'utf-8'))
            elif color == "yellow":
                ser.write(bytes('L7=1', 'utf-8'))
                ser.write(bytes('L8=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if ser:
            print("wrong module connected")
        else:
            print("no module connected")


def Lamp5(color="", state=False):
    if connection_type == 2 and ser:
        ser.write(bytes('L9=0', 'utf-8'))
        ser.write(bytes('L0=0', 'utf-8'))
        if state:
            if color == "red":
                ser.write(bytes('L9=1', 'utf-8'))
            elif color == "green":
                ser.write(bytes('L0=1', 'utf-8'))
            elif color == "yellow":
                ser.write(bytes('L9=1', 'utf-8'))
                ser.write(bytes('L80=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if ser:
            print("wrong module connected")
        else:
            print("no module connected")


def laser_on():
    '''Turns the laser pointer on'''
    ser.write(bytes('LL=1', 'utf-8'))


def laser_off():
    '''Turns the laser pointer off'''
    ser.write(bytes('LL=0', 'utf-8'))


def beep_on():
    '''Turns the beeper on'''
    ser.write(bytes('BP=1', 'utf-8'))


def beep_off():
    '''Turns the laser pointer off'''
    ser.write(bytes('BP=0', 'utf-8'))


def reset_all():
    '''Turns all the feedback off'''
    Lamp1("", False)
    Lamp2("", False)
    Lamp3("", False)
    Lamp4("", False)
    Lamp5("", False)

    laser_off()
    beep_off()