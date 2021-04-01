# turns values into float type
def floatSwitch(stat, data, index):
    if stat in data[index]:
        try:
            data[index][stat] = float(data[index][stat])
        except:
            data[index][stat] = 9999999