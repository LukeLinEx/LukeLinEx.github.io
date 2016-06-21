import pandas as pd
import re
import numpy as np
#import datetime as dt
#import unicodedata
import requests
from bs4 import BeautifulSoup
import sqlite3
#import time


def scrape_list(site):
    #hdr = {'User-Agent': 'Mozilla/5.0'}
    #req = urllib2.Request(site, headers=hdr)
    page = requests.get(site).text
    soup = BeautifulSoup(page)

    table = soup.find('table', {'class': 'wikitable sortable'})
    sector_tickers = dict()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            sector = str(col[3].string.strip()).lower().replace(' ', '_')
            ticker = str(col[0].string.strip())
            if sector not in sector_tickers:
                sector_tickers[sector] = list()
            sector_tickers[sector].append(ticker)
    sector_tickers = reduce(lambda x,y: x+y, sector_tickers.values())
    return sector_tickers


def random_sample(size=6):
	con = sqlite3.connect('stock_database/stock_db')
	cursor = con.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	lst = cursor.fetchall()
	lst = map(lambda x: str(x[0]), lst)
 	lst = np.random.choice(lst, size = size, replace=False)
 	tobesave =  '\n'.join(lst)
 	con.close()
 	
 	f = open('sample.txt', 'w')
 	f.write(tobesave)
 	f.close()
	


if __name__ ==  '__main__':
	random_sample()
	
	
	
	
	
	
	
	
	
	
	
	
	