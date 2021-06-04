# turns values into integer type
def intSwitch(stat, data, index):
    if stat in data[index]:
        try:
            data[index][stat] = int(data[index][stat])
        except:
            data[index][stat] = 0
