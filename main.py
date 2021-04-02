import requests
import json
import csv
from bs4 import BeautifulSoup
import numpy as np
from intSwitch import intSwitch
from floatSwitch import floatSwitch
from d1Scraper import d1Scraper
from getTeamPaths import getTeamPaths

# urlList = ['https://d1baseball.com/team/albany/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/']

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


print(json.dumps(playerArray, indent=4))

with open('outputfile', 'w') as fout:
    json.dump(playerArray, fout, indent=4)
