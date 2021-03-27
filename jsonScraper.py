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

    #Convert stats into integers from strings
    Num = '#'
    if Num in table_data[index]:
        table_data[index][Num] = int(table_data[index][Num])
    
    ERA = 'ERA'
    if ERA in table_data[index]:
        try:
            table_data[index][ERA] = float(table_data[index][ERA])
        except:
            table_data[index][ERA]

    WHIP = 'WHIP'
    if WHIP in table_data[index]:
        try:
            table_data[index][WHIP] = float(table_data[index][WHIP])
        except:
            table_data[index][WHIP]

    CG = 'CG'
    if CG in table_data[index]:
        table_data[index][CG] = int(table_data[index][CG])

    HBP = 'HBP'
    if HBP in table_data[index]:
        table_data[index][HBP] = int(table_data[index][HBP])

    SV = 'SV'
    if SV in table_data[index]:
        table_data[index][SV] = int(table_data[index][SV])
    
    IP = 'IP'
    if IP in table_data[index]:
        table_data[index][IP] = float(table_data[index][IP])
    
    H = 'H'
    if H in table_data[index]:
        table_data[index][H] = int(table_data[index][H])
    
    R = 'R'
    if R in table_data[index]:
        table_data[index][R] = int(table_data[index][R])

    ER = 'ER'
    if ER in table_data[index]:
        table_data[index][ER] = int(table_data[index][ER])
    
    BB = 'BB'
    if BB in table_data[index]:
        table_data[index][BB] = int(table_data[index][BB])

    SO = 'SO'
    if SO in table_data[index]:
        table_data[index][SO] = int(table_data[index][SO])

    Double = '2B'
    if Double in table_data[index]:
        table_data[index][Double] = int(table_data[index][Double])

    Triple = '3B'
    if Triple in table_data[index]:
        table_data[index][Triple] = int(table_data[index][Triple])

    HR = 'HR'
    if HR in table_data[index]:
        table_data[index][HR] = int(table_data[index][HR])

    AB = 'AB'
    if AB in table_data[index]:
        table_data[index][AB] = int(table_data[index][AB])

    BAVG = 'B/AVG'
    if BAVG in table_data[index]:
        table_data[index][BAVG] = float(table_data[index][BAVG])

    WP = 'WP'
    if WP in table_data[index]:
        table_data[index][WP] = int(table_data[index][WP])
    
    BK = 'BK'
    if BK in table_data[index]:
        table_data[index][BK] = int(table_data[index][BK])

    SFA = 'SFA'
    if SFA in table_data[index]:
        table_data[index][SFA] = int(table_data[index][SFA])

    SHA = 'SHA'
    if SHA in table_data[index]:
        table_data[index][SHA] = int(table_data[index][SHA])

    AVG = 'AVG'
    if AVG in table_data[index]:
        table_data[index][AVG] = float(table_data[index][AVG])

    OPS = 'OPS'
    if OPS in table_data[index]:
        table_data[index][OPS] = float(table_data[index][OPS])

    RBI = 'RBI'
    if RBI in table_data[index]:
        table_data[index][RBI] = int(table_data[index][RBI])

    TB = 'TB'
    if TB in table_data[index]:
        table_data[index][TB] = int(table_data[index][TB])

    SLG = 'SLG%'
    if SLG in table_data[index]:
        table_data[index][SLG] = float(table_data[index][SLG])
    
    GDP = 'GDP'
    if GDP in table_data[index]:
        table_data[index][GDP] = int(table_data[index][GDP])

    OB = 'OB%'
    if OB in table_data[index]:
        table_data[index][OB] = float(table_data[index][OB])

    SF = 'SF'
    if SF in table_data[index]:
        table_data[index][SF] = int(table_data[index][SF])

    SH = 'SH'
    if SH in table_data[index]:
        table_data[index][SH] = int(table_data[index][SH])

    
    # Separate double values in hitter/pitcher data
    gpgs = 'GP-GS'
    if gpgs in table_data[index]:
        games = table_data[index]['GP-GS'].split('-')
        table_data[index].update({'gamesPlayed' : int(games[0])})
        table_data[index].update({'gamesStarted' : int(games[1])})
        table_data[index].pop('GP-GS')

    sbatt = 'SB-ATT'
    if sbatt in table_data[index]:
        sb = table_data[index]['SB-ATT'].split('-')
        table_data[index].update({'stolenBases' : int(sb[0])})
        table_data[index].update({'attempts' : int(sb[1])})
        table_data[index].pop('SB-ATT')
         
    winloss = 'W-L'
    if winloss in table_data[index]:
        win = table_data[index]['W-L'].split('-')
        table_data[index].update({'wins' :int( win[0])})
        table_data[index].update({'losses' : int(win[1])})
        table_data[index].pop('W-L')

    appgs = 'APP-GS'
    if appgs in table_data[index]:
        win = table_data[index]['APP-GS'].split('-')
        table_data[index].update({'appearances' : int(win[0])})
        table_data[index].update({'gamesStarted' : int(win[1])})
        table_data[index].pop('APP-GS')

    sho = 'SHO'
    if sho in table_data[index]:
        shutouts = table_data[index]['SHO'].split('-')
        table_data[index].update({'completeGames' : int(shutouts[0])})
        table_data[index].update({'shutouts' : int(shutouts[1])})
        table_data[index].pop('SHO')

    index += 1

##### End Data Cleaning Block #####

# print(table_data[5]['GP-GS'].split('-'))

tableLength = len(table_data)

print(f'***{tableLength} players found for {title}***')
print(json.dumps(table_data[0], indent=4))
print(json.dumps(table_data[tableLength-8], indent=4))


# print("mission success")