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

today = date.today()
date = today.strftime("%m/%d/%Y")

urlList = ['https://d1baseball.com/team/albany/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/']

pathUrl = 'https://d1baseball.com/teams/'

teamPaths = urlList

playerArray = []
index = 0

for each in teamPaths:
    teamPlayers = d1Scraper(each)
    print(index)
    index += 1
    if teamPlayers is None:
        continue
    playerArray = playerArray + teamPlayers


fullData = {
'meta': {
    'lastUpdated': date,
},
'data': playerArray
}


print(json.dumps(fullData, indent=4))

with open('testfile', 'w') as fout:
    json.dump(fullData, fout, indent=4)
