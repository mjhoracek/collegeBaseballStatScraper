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
from jucoScraper import jucoScraper
from jucoMetaRanges import jucoMetaRanges



today = date.today()
date = today.strftime("%m/%d/%Y")


teamPaths = [
    #juco d1 hitters/pitchers
    'https://www.njcaa.org/sports/bsb/2020-21/div1/players?sort=ab&view=&pos=h&r=0&maxCount=500',
    'https://www.njcaa.org/sports/bsb/2020-21/div1/players?sort=ip&view=&pos=p&r=0&maxCount=500',
    #juco d2 hitters/pitchers
    'https://www.njcaa.org/sports/bsb/2020-21/div2/players?sort=ab&view=&pos=h&r=0&maxCount=500',
    'https://www.njcaa.org/sports/bsb/2020-21/div2/players?sort=ip&view=&pos=p&r=0&maxCount=500',
    #juco d3 hitters/pitchers
    'https://www.njcaa.org/sports/bsb/2020-21/div3/players?sort=ab&view=&pos=h&r=0&maxCount=500',
    'https://www.njcaa.org/sports/bsb/2020-21/div3/players?sort=ip&view=&pos=p&r=0&maxCount=500',
]

playerArray = []
index = 0

for each in teamPaths:
    teamPlayers = jucoScraper(each)
    print(index)
    index += 1
    if teamPlayers is None:
        continue
    playerArray = playerArray + teamPlayers


ranges = jucoMetaRanges(playerArray)


fullData = {
'meta': {
    'lastUpdated': date,
    'ranges' : ranges
},
'data': playerArray
}


with open('JUCOoutputfile', 'w') as fout:
    json.dump(fullData, fout, indent=4)
