from bs4 import BeautifulSoup

import time
import requests
import random

from tabulate import tabulate
import pandas as pd

#! possible options: True - test with smaller output, False - normal output
TEST = False

SLEEP_TIME = random.uniform(1, 2)

def estate_info(link):  
    #time.sleep(SLEEP_TIME) # To avoid being blocked by the server
    
    page = requests.get(link, headers=headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')

    record = []

    # price for estate
    try:
        price = soup1.select_one('strong[data-cy="adPageHeaderPrice"]').text.strip()
        if price != 'Zapytaj o cenę':
            price_digits = ''.join(filter(str.isdigit, price))
            price = int(price_digits)
        else:
            #print('|----DELETED----|')
            return None  # Skip the record if price is 'Zapytaj o cenę'
    except (AttributeError, ValueError, Exception):
        price = None
    
    # title of offer
    try:
        title = soup1.select_one('h1[data-cy="adPageAdTitle"]').text.strip()
    except (AttributeError, Exception):
        title = None

    # address of estate
    try:
        address = soup1.select_one('a[href="#map"]').text.strip()
    except (AttributeError, Exception):
        address = None
    #! FIX ERROR
    # area of estate
    try:
        area = float(soup1.select_one('div[data-testid="table-value-area"]').text.strip().split(' ')[0].replace(',', '.'))
    except (AttributeError, Exception):
        area = None

    # numbers of rooms in estate
    try:
        rooms = soup1.select_one('div[aria-label="Liczba pokoi"] > div:nth-of-type(2)').text.strip()
    except (AttributeError, Exception):
        rooms = None

    # number of floors in estate
    try:
        floor = soup1.select_one('div[data-testid="table-value-floor"]').text.strip().split('/')[0]
    except (AttributeError, Exception):
        floor = None
        
    # market either primary of aftermarket
    try:
        market = soup1.select_one('div.css-1yvps34.e10umaf20 div.css-1qzszy5.enb64yk2:nth-child(2)').text.strip()
    except (AttributeError, Exception):
        market = None        
    
    # balcony, garde, terrace
    try:
        addition = soup1.select_one('div[data-testid="table-value-outdoor"]').text.strip()
    except (AttributeError, Exception):
        addition = None
        
    # parking
    try:
        parking = soup1.select_one('div[data-testid="table-value-car"]').text.strip()
    except (AttributeError, Exception):
        parking = None
    
    # elevator
    try:
        elevator = soup1.select_one('div[aria-label="Winda"] > div:nth-of-type(2)').text.strip()
    except (AttributeError, Exception):
        elevator = None
        
    #! rent FIX
    try:
        rent = None
    except (AttributeError, Exception):
        rent = None
        
    # build year
    try:
        build_year = soup1.select_one('div[aria-label="Rok budowy"] > div:nth-of-type(2)').text.strip()
        if build_year == 'brak informacji':
            build_year = None
    except (AttributeError, Exception):
        build_year = None
        
    # internet
    try:
        media = soup1.select_one('div[aria-label="Media"] > div:nth-of-type(2)').text.strip()
        if 'internet' in media:
            internet = 1
        else:
            internet = 0
    except (AttributeError, Exception):
        internet = None
        
    # type of development
    try:
        building_type = soup1.select_one('div[aria-label="Rodzaj zabudowy"] > div:nth-of-type(2)').text.strip()
        if building_type == 'brak informacji':
            building_type = None
    except (AttributeError, Exception):
        building_type = None
            
    # basement
    try:
        basement = soup1.select_one('div[aria-label="Informacje dodatkowe"] > div:nth-of-type(2)').text.strip()
        if 'piwnica' in basement:
            basement = 1
        else:
            basement = 0
    except (AttributeError, Exception):
        basement = None
    
    record.extend((title, address, price, area, rooms, floor, market, addition, parking, elevator, build_year, internet, building_type, basement))
    
    return record


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
}

BASE_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/wiele-lokalizacji?limit=36&ownerTypeSingleSelect=ALL&locations=%5Bpomorskie%2Fgdansk%2Fgdansk%2Fgdansk%2Cpomorskie%2Fsopot%2Fsopot%2Fsopot%2Cpomorskie%2Fgdynia%2Fgdynia%2Fgdynia%5D&by=BEST_MATCH&direction=DESC&viewType=listing&page=1"

response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# number of pages
total_pages = int(soup.select_one('ul.css-1vdlgt7 li.css-1tospdx:nth-last-of-type(2)').text.strip())

data = []
# header of the data
header=["title", "address", "price[PLN]", "area[m^2]", "rooms", "floor", "market", "addition", "parking", "elevator", "build year", "internet", "buiiding_type", 'basement']

for page in range(1, total_pages):
    
    URL = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/wiele-lokalizacji?limit=36&ownerTypeSingleSelect=ALL&locations=%5Bpomorskie%2Fgdansk%2Fgdansk%2Fgdansk%2Cpomorskie%2Fsopot%2Fsopot%2Fsopot%2Cpomorskie%2Fgdynia%2Fgdynia%2Fgdynia%5D&by=BEST_MATCH&direction=DESC&viewType=listing&page={page}"

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # list of URLs on page
    links = soup.select('a.css-16vl3c1.e1x0p3r10')
    links_list = ['https://www.otodom.pl' + link.get('href') for link in links]
    
    print(f'page {page} of {total_pages}')
    
    # iterate over  the list of URLs on page
    for index, link in enumerate(links_list):
        print(f'|----link {index + 1} of {len(links_list)}')
        
        record = []
        record = estate_info(link)
        
        if record != None:
            data.append(record)
            
        #! TEST    
        if index == 1 and TEST is True:
            break
    
    #! TEST      
    if page >= 2 and TEST is True:
        print(tabulate(data, headers=header, tablefmt='outline'))
        break


print(f'\nTotal pages: {total_pages}')  
print(f'\nTotal number of records: {len(data)}')

data_df = pd.DataFrame(data)
data_df.to_csv('otodom_data.csv', sep = '|', header = header, index = False)
