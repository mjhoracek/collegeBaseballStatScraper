def intSwitch(stat, data, index):
    if stat in data[index]:
        data[index][stat] = int(data[index][stat])
