import requests
import json
import csv
from bs4 import BeautifulSoup
from getTeamPaths import getTeamPaths


urlList = ['https://d1baseball.com/team/albany/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/']

url = urlList[1]

response = requests.get(url)
soup = BeautifulSoup( response.text, 'html.parser' )

# Isolate title, pitcher table, hitter table
# title = soup.find('h1').get_text()
title = soup.find('h1').get_text()
csvTitle = str(title)
csvTitle = '%s.csv' % csvTitle

hitters = soup.find_all('table', {'class': 'batting-sortable-stats'})[0]
pitchers = soup.find_all('table', {'id': 'pitching-stats'})[0]

rowsHitter = hitters.find_all('tr')
rowsPitcher = pitchers.find_all('tr')

# Init table headers for pitchers/hitters, init table_data where all the JSON objects will live
pitcherFields= []
hitterFields = []
table_data = []


# Build fields lists
for tr in hitters.find_all('tr', recursive=True):
    for th in tr.find_all('th', recursive=True):
        hitterFields.append(th.get_text())

for tr in pitchers.find_all('tr', recursive=True):
    for th in tr.find_all('th', recursive=True):
        pitcherFields.append(th.get_text())


# Build csv file
with open(csvTitle, 'wt+', newline="") as f:
    writer = csv.writer(f)
    writer.writerow([csvTitle,''])
    writer.writerow(hitterFields)
    for row in rowsHitter:
        csv_row = []
        for cell in row.find_all(['td']):
            cellText = cell.get_text()
            cleanCell = cellText.replace('&nbsp', '')
            cell.replace_with(cleanCell)
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)

    writer.writerow('')

    writer.writerow(pitcherFields)
    for row in rowsPitcher:
        csv_row = []
        for cell in row.find_all(['td']):
            cellText = cell.get_text()
            cleanCell = cellText.replace('&nbsp', '')
            cell.replace_with(cleanCell)
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)


# print(pitcherFields, hitterFields)