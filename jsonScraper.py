import requests
import csv
import json
from bs4 import BeautifulSoup
from csv import writer

# Enter URL of XML Baseball Stat sheet
url = 'https://dartmouthsports.com/sports/baseball/stats/2013'

# Collect HTML w/Beautiful Soup
response = requests.get(url)
soup = BeautifulSoup( response.text, 'html.parser' )

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

#Build Hitters data
for tr in hitters.find_all('tr', recursive=True):
    for th in tr.find_all('th', recursive=True):
        hitterFields.append(th.get_text())
for tr in hitters.find_all('tr', recursive=True):
    datum = {}
    for i, td in enumerate(tr.find_all(['td', {'a': 'data-player-id'}], recursive=True)):
        datum[hitterFields[i]] = td.get_text()
    if datum:
        table_data.append(datum)


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

# Removes unwanted key/value pairs at the end of each dictionary
index = 0
while index < len(table_data):
    table_data[index].popitem()
    table_data[index].popitem()
    index +=1


print(json.dumps(table_data, indent=4))
# print(table_data[1]['AVG'])

# keller = table_data[0]
# print(json.dumps(keller, indent=4))

# print("mission success")
