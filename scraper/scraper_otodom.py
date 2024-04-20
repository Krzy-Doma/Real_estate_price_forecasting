from bs4 import BeautifulSoup

import time
import requests
import random

from tabulate import tabulate

TEST = 1

def estate_info(link):  
    time.sleep(SLEEP_TIME) # To avoid being blocked by the server
    
    page = requests.get(link, headers=headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')

    record = []

    # title of offer
    try:
        title = soup1.select_one('h1[data-cy="adPageAdTitle"]').text.strip()
    except AttributeError:
        title = None

    # address of estate
    try:
        address = soup1.select_one('a[href="#map"]').text.strip()
    except AttributeError:
        address = None

    # price for estate
    try:
        price = soup1.select_one('strong[data-cy="adPageHeaderPrice"]').text.strip()
        if price != 'Zapytaj o cenę':
            price_digits = ''.join(filter(str.isdigit, price))
            price = int(price_digits)
        else:
            return None  # Skip the record if price is 'Zapytaj o cenę'
    except (AttributeError, ValueError):
        price = None

    # area of estate
    try:
        area = float(soup1.select_one('div[data-testid="table-value-area"]').text.strip().split(' ')[0].replace(',', '.'))
    except AttributeError:
        area = None

    # numbers of rooms in estate
    try:
        rooms = soup1.select_one('a[data-cy="ad-information-link"]').text.strip()
    except AttributeError:
        rooms = None

    # number of floors in estate
    try:
        floor = soup1.select_one('div[data-testid="table-value-floor"]').text.strip().split('/')[0]
    except AttributeError:
        floor = None
    
    record.extend((title, address, price, area, rooms, floor))
    
    return record


SLEEP_TIME = random.uniform(1, 2)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
}

BASE_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/wiele-lokalizacji?limit=36&ownerTypeSingleSelect=ALL&locations=%5Bpomorskie%2Fgdansk%2Fgdansk%2Fgdansk%2Cpomorskie%2Fsopot%2Fsopot%2Fsopot%2Cpomorskie%2Fgdynia%2Fgdynia%2Fgdynia%5D&by=BEST_MATCH&direction=DESC&viewType=listing&page=1"

response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# number of pages
total_pages = int(soup.select_one('ul.css-1vdlgt7 li.css-1tospdx:nth-last-of-type(2)').text.strip())

data = []

for page in range(total_pages):
    
    URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/wiele-lokalizacji?limit=36&ownerTypeSingleSelect=ALL&locations=%5Bpomorskie%2Fgdansk%2Fgdansk%2Fgdansk%2Cpomorskie%2Fsopot%2Fsopot%2Fsopot%2Cpomorskie%2Fgdynia%2Fgdynia%2Fgdynia%5D&by=BEST_MATCH&direction=DESC&viewType=listing&page={page}"

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # list of URLs on page
    links = soup.select('a.css-16vl3c1.e1x0p3r10')
    links_list = ['https://www.otodom.pl' + link.get('href') for link in links]
    
    print(f'page {page + 1} of {total_pages}')
    
    # iterate over  the list of URLs on page
    for index, link in enumerate(links_list):
        print(f'|----link {index + 1} of {len(links_list)}')
        
        record = []
        record = estate_info(link)
        
        if record != None:
            data.append(record)
            
        #! TEST    
        if index == 1 & TEST == 1:
            break
    
    #! TEST      
    if page == 1 & TEST == 1:
        break


print(f'Total pages: {total_pages}')
    
print(f'Total number of records: {len(data)}')
print(tabulate(data, headers=["title", "address", "price[PLN]", "area[m^2]", "rooms", "floor"], tablefmt='outline'))
print(1/2)

