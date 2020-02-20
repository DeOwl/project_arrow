import os
import serial.tools.list_ports


ser = None
def connect_eco_sensor():
    global ser
    port_name = None
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Prolif" in str(p):
            port_name = str(p)[:5]
            # определение порта
    if port_name:
        ser = serial.Serial(port_name)
        ser.baudrate = 115200
    return True if ser else False

def get_data():
    global ser
    if ser:
        line = str(ser.readline())[4:-3].split()
        number_of_data_string = line[0][2:]
        res = []
        res.append(str('Температура, \u00b0С: \t\t' + line[1][2:]))
        res.append(str('Атм. давление, мм рт.ст.: \t' + line[2][2:]))
        res.append(str('Отн. влажность, %: \t\t' + line[3][2:]))
        res.append(str('Индекс качества воздуха: \t' + line[4][5:]))
        res.append(str('Индекс уровня CO2: \t\t' + line[5][4:]))
        res.append(str('Уровень освещенности: \t\t' + line[6][6:]))
        return res
    return None