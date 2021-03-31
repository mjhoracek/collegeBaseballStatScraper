import requests
import json
from bs4 import BeautifulSoup
import re

# Web page with list of D1 Baseball teams w/links
url = 'https://d1baseball.com/teams/'

# Define function to get a list of links
def getTeamPaths(url):
    
    response = requests.get(url)
    soup = BeautifulSoup( response.text, 'html.parser' )

    teams = soup.find_all('td', {'class': 'team'})

    index = 0
    tags = []
    links = []

    while index < len(teams):
        tags.append(teams[index].find('a', recursive=True))
        index += 1

    for link in tags:
        links.append('https://d1baseball.com' + str(link['href']) + '/2021/stats/')

    # Array of links
    return links

