import requests
import json
from bs4 import BeautifulSoup
from d1Fields import *
from intSwitch import intSwitch
from floatSwitch import floatSwitch

urlList = ['https://d1baseball.com/team/albany/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/', 'https://d1baseball.com/team/sunybing/2021/stats/']

url = urlList[1]


def d1Scraper(url): 

    response = requests.get(url)
    soup = BeautifulSoup( response.text, 'html.parser' )

    # Isolate title, pitcher table, hitter table
    # title = soup.find('h1').get_text()
    pitchers = soup.find_all('table', {'id': 'pitching-stats'})[0]
    hitters = soup.find_all('table', {'class': 'batting-sortable-stats'})[0]

    # Init table headers for pitchers/hitters, init table_data where all the JSON objects will live
    pitcherFields= []
    hitterFields = []
    table_data = []

    # Build Hitter objects
    for tr in hitters.find_all('tr', recursive=True):
        for th in tr.find_all('th', recursive=True):
            hitterFields.append(th.get_text())
    for tr in hitters.find_all('tr', recursive=True):
        datum = {}
        for i, td in enumerate(tr.find_all(['td'], recursive=True)):
            datum[hitterFields[i]] = td.get_text()
        if datum:
            table_data.append(datum)

    # Build Pitcher objects
    for tr in pitchers.find_all('tr', recursive=True):
        for th in tr.find_all('th', recursive=True):
            pitcherFields.append(th.get_text())
    for tr in pitchers.find_all('tr', recursive=True):
        datum = {}
        for i, td in enumerate(tr.find_all(['td'], recursive=True)):
            datum[pitcherFields[i]] = td.get_text()
        if datum:
            table_data.append(datum)

    ###### Data Cleaning Block ######
    index = 0
    while index < len(table_data):

    # Split name into two k/v pairs
        name = table_data[index]['Player'].split(' ')
        table_data[index].update({'firstName' : name[0]})
        table_data[index].update({'lastName' : name[1]})
        table_data[index].pop('Player')

        #Convert stats into integers from strings
        for each in intFields:
            intSwitch(each, table_data, index)
        
        for each in floatFields:
            floatSwitch(each, table_data, index)

    # Dont forget to increment yo shit
        index += 1


        return table_data