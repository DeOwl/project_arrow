import os
import serial.tools.list_ports


ser = None
connection_type = None
def connect_eco_sensor():
    try:
        global ser, connection_type
        port_name = None
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Prolif" in str(p):
                port_name = str(p)[:5]
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
    try:
        if ser:

            line = str(ser.readline())[4:-3].split()
            if connection_type == 1:
                res = {}
                res['Температура, \u00b0С:'] = line[1][2:]
                res['Атм. давление, мм рт.ст.:'] = line[2][2:]
                res['Отн. влажность, %: \t\t'] = line[3][2:]
                res['Индекс качества воздуха: \t'] = line[4][5:]
                res['Индекс уровня CO2: \t\t'] = line[5][4:]
                res['Уровень освещенности: \t\t'] = line[6][6:]
                return res
    except:
        ser = None
        return False
    return None