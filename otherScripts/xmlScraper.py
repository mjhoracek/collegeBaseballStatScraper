import requests
import csv
import json
from bs4 import BeautifulSoup
from csv import writer

# Enter URL of XML Baseball Stat sheet
url = 'https://uclabruins.com/sports/baseball/stats'


# Collect HTML w/Beautiful Soup
response = requests.get(url)
soup = BeautifulSoup( response.text, 'html.parser' )

title = soup.find('title').get_text()
title = title.replace(' ', '_').replace('\r', '').replace("\n", '').replace('\t', '')
csvTitle = str(title)
csvTitle = '%s.csv' % csvTitle

# Isolate Tables for hitters and pitchers data
hitters = soup.find_all('table')[0]
pitchers = soup.find_all('table')[1]

rowsHitter = hitters.find_all('tr')
rowsPitcher = pitchers.find_all('tr')

# Pull Headers for each table type
hitterHeader = []
pitcherHeader= []

header1 = hitters.find_all('thead')
for data in header1[0].find_all('th'):
    hitterHeader.append(data.get_text())


header2 = pitchers.find_all('thead')
for data in header2[0].find_all('th'):
    pitcherHeader.append(data.get_text())

# Create and write data to csv file
with open(csvTitle, 'wt+', newline="") as f:
    writer = csv.writer(f)
    writer.writerow([csvTitle,''])
    writer.writerow(hitterHeader)
    for row in rowsHitter:
        csv_row = []
        for cell in row.find_all(['td', 'a']):
            cellText = cell.get_text()
            cleanCell = cellText.replace('&nbsp', '')
            cell.replace_with(cleanCell)
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)

    writer.writerow('')

    writer.writerow(pitcherHeader)
    for row in rowsPitcher:
        csv_row = []
        for cell in row.find_all(['td', 'a']):
            cellText = cell.get_text()
            cleanCell = cellText.replace('&nbsp', '')
            cell.replace_with(cleanCell)
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)


print("mission success")
