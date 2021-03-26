import requests
import csv
import json
from bs4 import BeautifulSoup
from csv import writer

# Enter URL of XML Baseball Stat sheet
# url = 'https://dartmouthsports.com/sports/baseball/stats/2013'
# url = 'https://uclabruins.com/sports/baseball/stats'
url = 'https://fightingillini.com/sports/baseball/stats'


# Collect HTML w/Beautiful Soup
response = requests.get(url)
soup = BeautifulSoup( response.text, 'html.parser' )

# Find team name via title tag
title = soup.find('title').get_text()
title = title.replace(' ', '_').replace('\r', '').replace("\n", '').replace('\t', '')
csvTitle = str(title)
csvTitle = '%s.csv' % csvTitle

# Isolate Tables for hitters and pitchers data
hitters = soup.find_all('table')[0]

# Remove tfoot from table, which contains unwanted totals/opponents data
for tfoot in hitters.find_all('tfoot', recursive=True):
    tfoot.decompose()

pitchers = soup.find_all('table')[1]
for tfoot in pitchers.find_all('tfoot', recursive=True):
    tfoot.decompose()

#Initialize fields array, which is the header column for Hitter data
hitterFields = []
#Initialize table_data, where all of the data is going to live. This is an array of dictionaries
table_data = []

# Build Hitters data
for tr in hitters.find_all('tr', recursive=True):
    for th in tr.find_all('th', recursive=True):
        hitterFields.append(th.get_text())
for tr in hitters.find_all('tr', recursive=True):
    datum = {}
    for i, td in enumerate(tr.find_all(['td', {'a': 'data-player-id'}], recursive=True)):
        datum[hitterFields[i]] = td.get_text()
    if datum:
        table_data.append(datum)

# Build Pitchers Data
pitcherFields = []
for tr in pitchers.find_all('tr', recursive=True):
    for th in tr.find_all('th', recursive=True):
        pitcherFields.append(th.get_text())
for tr in pitchers.find_all('tr', recursive=True):
    pitcherData = {}
    for i, td in enumerate(tr.find_all(['td', 'a'], recursive=True)):
        pitcherData[pitcherFields[i]] =td.get_text()
    if pitcherData:
        table_data.append(pitcherData)

###### Data Cleaning Block ######
index = 0
while index < len(table_data):

    # Remove unwanted k/v junk at the end of each dict
    table_data[index].popitem()
    table_data[index].popitem()

    # Add team info k/v
    table_data[index].update({'dataSet' : title})

    # Split "Player" key into first/last names, remove "Player" 
    name = table_data[index]['Player'].split(', ')
    table_data[index].update({'firstName' : name[0]})
    table_data[index].update({'lastName' : name[1]})
    table_data[index].pop('Player')

    # Separate double values in hitter/pitcher data
    gpgs = 'GP-GS'
    if gpgs in table_data[index]:
        games = table_data[index]['GP-GS'].split('-')
        table_data[index].update({'gamesPlayed' : games[0]})
        table_data[index].update({'gamesStarted' : games[1]})
        table_data[index].pop('GP-GS')

    sbatt = 'SB-ATT'
    if sbatt in table_data[index]:
        sb = table_data[index]['SB-ATT'].split('-')
        table_data[index].update({'stolenBases' : sb[0]})
        table_data[index].update({'attempts' : sb[1]})
        table_data[index].pop('SB-ATT')
         
    winloss = 'W-L'
    if winloss in table_data[index]:
        win = table_data[index]['W-L'].split('-')
        table_data[index].update({'wins' : win[0]})
        table_data[index].update({'losses' : win[1]})
        table_data[index].pop('W-L')

    appgs = 'APP-GS'
    if appgs in table_data[index]:
        win = table_data[index]['APP-GS'].split('-')
        table_data[index].update({'appearances' : win[0]})
        table_data[index].update({'gamesStarted' : win[1]})
        table_data[index].pop('APP-GS')

    sho = 'SHO'
    if sho in table_data[index]:
        shutouts = table_data[index]['SHO'].split('-')
        table_data[index].update({'shutouts' : shutouts[0]})
        table_data[index].update({'completeGames' : shutouts[1]})
        table_data[index].pop('SHO')

    index += 1

##### End Data Cleaning Block #####



# print(table_data[5]['GP-GS'].split('-'))

tableLength = len(table_data)

print(f'***{tableLength} players found for {title}***')
print(json.dumps(table_data[0], indent=4))
print(json.dumps(table_data[tableLength-8], indent=4))


# print("mission success")