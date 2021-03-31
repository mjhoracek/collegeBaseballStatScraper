def splitter(stat, data, index, firstField, secondField):
    if stat in data[index]:
        splitList = data[index][stat].split('-')
        data[index].update({firstField : int(splitList[0])})
        data[index].update({secondField : int(splitList[1])})
        data[index].pop(stat)