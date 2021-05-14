import requests
import json
import csv
from bs4 import BeautifulSoup
import numpy as np
from intSwitch import intSwitch
from floatSwitch import floatSwitch
from d1Scraper import d1Scraper
from getTeamPaths import getTeamPaths
from datetime import date
from metaRanges import metaRanges



today = date.today()
date = today.strftime("%m/%d/%Y")


pathUrl = 'https://d1baseball.com/teams/'

teamPaths = getTeamPaths(pathUrl)

playerArray = []
index = 0

for each in teamPaths:
    teamPlayers = d1Scraper(each)
    print(index)
    index += 1
    if teamPlayers is None:
        continue
    playerArray = playerArray + teamPlayers


ranges = metaRanges(playerArray)


fullData = {
'meta': {
    'lastUpdated': date,
    'ranges' : ranges
},
'data': playerArray
}


# print(json.dumps(fullData, indent=4))

with open('outputfile', 'w') as fout:
    json.dump(fullData, fout, indent=4)
