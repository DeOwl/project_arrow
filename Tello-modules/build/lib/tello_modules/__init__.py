import serial.tools.list_ports
import tello_modules.common as com


def connect_module(number):
    try:
        if com.ser and com.connection_type == number:
            return True
        if com.ser:
            com.ser.close()
        port_name = None
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if number == 1:
                if "Prolif" in p.manufacturer:
                    port_name = p.device
                    com.connection_type = 1
                    break
                    # определение порта
            elif number == 2:
                if "SBRICKS" in p.manufacturer:
                    port_name = p.device
                    com.connection_type = 2
                    break
        if port_name:
            com.ser = serial.Serial(port_name)
            com.ser.baudrate = 115200
    except Exception as err:
        com.connection_type = None
        return False
    if com.ser:
        return True
    else:
        com.connection_type = None
        return False
