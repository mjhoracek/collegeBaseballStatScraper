import requests
import csv
from bs4 import BeautifulSoup
from csv import writer

url = 'https://thesundevils.com/sports/baseball/stats/2021'

response = requests.get(url)

soup = BeautifulSoup( response.text, 'html.parser' )


hitters = soup.find_all('thead')

print(hitters)


with open('dartmouthStats.csv', 'wt+', newline="") as f:
    writer = csv.writer(f)
    for row in rowsHitter:
        csv_row = []
        for cell in row.find_all(['td', 'th']):
            cellText = cell.get_text()
            cleanCell = cellText.replace('&nbsp', '')
            cell.replace_with(cleanCell)
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)

    writer.writerow('')

    for row in rowsPitcher:
        csv_row = []
        for cell in row.find_all(['td', 'th']):
            cellText = cell.get_text()
            cleanCell = cellText.replace('&nbsp', '')
            cell.replace_with(cleanCell)
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)

print("mission success")