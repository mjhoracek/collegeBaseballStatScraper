import requests
import json
from bs4 import BeautifulSoup
from requests.api import options
from d1Fields import *
from intSwitch import intSwitch
from floatSwitch import floatSwitch
from metaRanges import metaRanges

urlList = ['https://www.njcaa.org/sports/bsb/2020-21/div1/players?sort=ip&view=&pos=p&r=0']

url = urlList[0]

header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

def jucoScraper(url): 

    response = requests.get(url, headers=header)
    soup = BeautifulSoup( response.text, 'html.parser' )

    # Isolate title, pitcher table, hitter table
    # title = soup.find('h1').get_text()
    table = soup.find('table')

    # Init table headers for pitchers/hitters, init table_data where all the JSON objects will live
    headers = []
    table_data = []

    # Build Hitter objects
    for tr in table.find_all('tr', recursive=True):
        for th in tr.find_all('th', recursive=True):
            head = th.get_text().replace(' ','').replace('\n','').replace('\xa0', 'School')
            headers.append(head)
    for tr in table.find_all('tr', recursive=True):
        datum = {}
        for i, td in enumerate(tr.find_all(['td'], recursive=True)):
            datum[headers[i]] = td.get_text().replace('\n','').replace('\r','')
        if datum:
            table_data.append(datum)


    ###### Data Cleaning Block ######
    index = 0
    while index < len(table_data):

        table_data[index].pop('Rk')
        table_data[index]['School'] = table_data[index]['School'].strip()

        # Split name into two k/v pairs
        table_data[index]['Name'] = table_data[index]['Name'].lstrip(' ')
        name = table_data[index]['Name'].split('  ')
        table_data[index].update({'firstName' : name[0]})
        table_data[index].update({'lastName' : name[1]})
        table_data[index].pop('Name')

        # Convert stats into integers from strings
        for each in jucoIntFields:
            intSwitch(each, table_data, index)
        
        for each in jucoFloatFields:
            floatSwitch(each, table_data, index)

        runs = table_data[index]['r']
        table_data[index].update({'R' : runs})
        table_data[index].pop('r')

        hits = table_data[index]['h']
        table_data[index].update({'H' : hits})
        table_data[index].pop('h')

        strikeouts = table_data[index]['k']
        table_data[index].update({'SO' : strikeouts})
        table_data[index].pop('k')

        walks = table_data[index]['bb']
        table_data[index].update({'BB' : walks})
        table_data[index].pop('bb')  

        homers = table_data[index]['hr']
        table_data[index].update({'HR' : homers})
        table_data[index].pop('hr')  


        if 'slg' in table_data[index]:
            #clean up and standardize the keys in the dict to the d1 stats
            table_data[index].update({'position' : 'H'})

            ops = round(table_data[index]['obp'] + table_data[index]['slg'], 3)
            table_data[index].update({'OPS' : ops})

            average = table_data[index]['avg']
            table_data[index].update({'AVG' : average})
            table_data[index].pop('avg')

            onBase = table_data[index]['obp']
            table_data[index].update({'OBP' : onBase})
            table_data[index].pop('obp')

            slug = table_data[index]['slg']
            table_data[index].update({'SLG' : slug})
            table_data[index].pop('slg')

            games = table_data[index]['g']
            table_data[index].update({'GP' : games})
            table_data[index].pop('g')

            atbats = table_data[index]['ab']
            table_data[index].update({'AB' : atbats})
            table_data[index].pop('ab')

            doubles = table_data[index]['2b']
            table_data[index].update({'2B' : doubles})
            table_data[index].pop('2b')       

            triples = table_data[index]['3b']
            table_data[index].update({'3B' : triples})
            table_data[index].pop('3b')

            rbi = table_data[index]['rbi']
            table_data[index].update({'RBI' : rbi})
            table_data[index].pop('rbi')

            sb = table_data[index]['sb']
            table_data[index].update({'SB' : sb})
            table_data[index].pop('sb')

            cs = table_data[index]['cs']
            table_data[index].update({'CS' : cs})
            table_data[index].pop('cs')

            table_data[index].update({'HP' : None}) 

        else:
            table_data[index].update({'position' : 'P'})

            wins = table_data[index]['w']
            table_data[index].update({'W' : wins})
            table_data[index].pop('w')

            losses = table_data[index]['l']
            table_data[index].update({'L' : losses})
            table_data[index].pop('l')

            era = table_data[index]['era']
            table_data[index].update({'ERA' : era})
            table_data[index].pop('era')

            app = table_data[index]['app']
            table_data[index].update({'APP' : app})
            table_data[index].pop('app')

            gs = table_data[index]['gs']
            table_data[index].update({'GS' : gs})
            table_data[index].pop('gs')

            cg = table_data[index]['cg']
            table_data[index].update({'CG' : cg})
            table_data[index].pop('cg')

            sv = table_data[index]['sv']
            table_data[index].update({'SV' : sv})
            table_data[index].pop('sv')

            ip = table_data[index]['ip']
            table_data[index].update({'IP' : ip})
            table_data[index].pop('ip')

            er = table_data[index]['er']
            table_data[index].update({'ER' : er})
            table_data[index].pop('er')

            kRate = table_data[index]['k/9']
            table_data[index].update({'kRate' : kRate})
            table_data[index].pop('k/9')

            table_data[index].update({'SHO' : None})
            table_data[index].update({'WP' : None})
            table_data[index].update({'HP' : None})
            table_data[index].update({'OBA' : None})

                        # Prevents division by zero if IP = 0
            if table_data[index]['IP'] > 0:
                hRate = round((table_data[index]['H'] / table_data[index]['IP']*9), 2)
                table_data[index].update({'hRate': hRate})
                bbRate = round((table_data[index]['BB'] / table_data[index]['IP']*9), 2)
                table_data[index].update({'bbRate': bbRate})

            if table_data[index]['BB'] > 0:
                soTObb = round((table_data[index]['SO'] / table_data[index]['BB']), 2)
                table_data[index].update({'soTObb': soTObb})
            
            if table_data[index]['IP'] <= 0:
                hRate = 0
                bbRate = 0
                table_data[index].update({'kRate': kRate})
                table_data[index].update({'bbRate': bbRate})
                table_data[index].update({'hRate': bbRate})
            
            if table_data[index]['BB'] <= 0:
                soTObb = 0
                table_data[index].update({'soTObb': soTObb})


        # Dont forget to increment yo shit
        index += 1


    # print(json.dumps(table_data, indent=4))

    return table_data
    

jucoScraper(url)