from tello_modules import connect_module
import tello_modules.common as con
from functools import wraps


def connection_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = connect_module(2)
        if connection:
            return func(*args, **kwargs)

    return wrapper


@connection_dec
def Lamp1(color=None):
    if con.connection_type == 2 and con.ser:
        con.ser.write(bytes('L1=0', 'utf-8'))
        con.ser.write(bytes('L2=0', 'utf-8'))
        if color:
            if color == "r":
                con.ser.write(bytes('L1=1', 'utf-8'))
            elif color == "g":
                con.ser.write(bytes('L2=1', 'utf-8'))
            elif color == "y":
                con.ser.write(bytes('L1=1', 'utf-8'))
                con.ser.write(bytes('L2=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if con.ser:
            print("wrong module connected")
        else:
            print("no module connected")


@connection_dec
def Lamp2(color=None):
    if con.connection_type == 2 and con.ser:
        con.ser.write(bytes('L3=0', 'utf-8'))
        con.ser.write(bytes('L4=0', 'utf-8'))
        if color:
            if color == "r":
                con.ser.write(bytes('L4=1', 'utf-8'))
            elif color == "g":
                con.ser.write(bytes('L3=1', 'utf-8'))
            elif color == "y":
                con.ser.write(bytes('L3=1', 'utf-8'))
                con.ser.write(bytes('L4=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if con.ser:
            print("wrong module connected")
        else:
            print("no module connected")


@connection_dec
def Lamp3(color=None):
    if con.connection_type == 2 and con.ser:
        con.ser.write(bytes('L5=0', 'utf-8'))
        con.ser.write(bytes('L6=0', 'utf-8'))
        if color:
            if color == "r":
                con.ser.write(bytes('L6=1', 'utf-8'))
            elif color == "g":
                con.ser.write(bytes('L5=1', 'utf-8'))
            elif color == "y":
                con.ser.write(bytes('L6=1', 'utf-8'))
                con.ser.write(bytes('L5=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if con.ser:
            print("wrong module connected")
        else:
            print("no module connected")


@connection_dec
def Lamp4(color=None):
    if con.connection_type == 2 and con.ser:
        con.ser.write(bytes('L7=0', 'utf-8'))
        con.ser.write(bytes('L8=0', 'utf-8'))
        if color:
            if color == "r":
                con.ser.write(bytes('L7=1', 'utf-8'))
            elif color == "g":
                con.ser.write(bytes('L8=1', 'utf-8'))
            elif color == "y":
                con.ser.write(bytes('L7=1', 'utf-8'))
                con.ser.write(bytes('L8=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if con.ser:
            print("wrong module connected")
        else:
            print("no module connected")


@connection_dec
def Lamp5(color=None):
    if con.connection_type == 2 and con.ser:
        con.ser.write(bytes('L9=0', 'utf-8'))
        con.ser.write(bytes('L0=0', 'utf-8'))
        if color:
            if color == "r":
                con.ser.write(bytes('L9=1', 'utf-8'))
            elif color == "g":
                con.ser.write(bytes('L0=1', 'utf-8'))
            elif color == "y":
                con.ser.write(bytes('L9=1', 'utf-8'))
                con.ser.write(bytes('L80=1', 'utf-8'))
            else:
                print("wrong color")
    else:
        if con.ser:
            print("wrong module connected")
        else:
            print("no module connected")


@connection_dec
def laser_on():
    '''Turns the laser pointer on'''
    con.ser.write(bytes('LL=1', 'utf-8'))


@connection_dec
def laser_off():
    '''Turns the laser pointer off'''
    con.ser.write(bytes('LL=0', 'utf-8'))


@connection_dec
def beep_on():
    '''Turns the beeper on'''
    con.ser.write(bytes('BP=1', 'utf-8'))


@connection_dec
def beep_off():
    '''Turns the laser pointer off'''
    con.ser.write(bytes('BP=0', 'utf-8'))


@connection_dec
def reset_all():
    '''Turns all the feedback off'''
    Lamp1()
    Lamp2()
    Lamp3()
    Lamp4()
    Lamp5()

    laser_off()
    beep_off()
