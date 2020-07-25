import tello_modules.common as com


def get_data():
    if com.ser:
        line = str(com.ser.readline())[4:-3].split()
        if com.connection_type == 1:
            res = {}
            res['Температура, \u00b0С'] = line[1][2:]
            res['Атм. давление, мм рт.ст.'] = line[2][2:]
            res['Отн. влажность, %'] = line[3][2:]
            res['Индекс качества воздуха'] = line[4][5:]
            res['Индекс уровня CO2'] = line[5][4:]
            res['Уровень освещенности'] = line[6][6:]
            return res
    return None
