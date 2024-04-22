from bs4 import BeautifulSoup

import time
import requests
import random

from tabulate import tabulate

#! possible options: True - test with smaller output, False - normal output
TEST = True

SLEEP_TIME = random.uniform(1, 2)

def estate_info(link):  
    time.sleep(SLEEP_TIME) # To avoid being blocked by the server
    
    page = requests.get(link, headers=headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    
    record = []
    
    # title of the offer
    try:
        title = soup1.select_one('div.t47vy80 > h1:not(p)').text.strip()
    except AttributeError:
        title = None
        
    # address of the estate
    try:
        address = soup1.select_one('h2.t129p2ny').text.strip()
    except AttributeError:
        address = None
    
    # price of the estate
    try:
        price = soup1.select_one('.gh-1johxon.e1kihjfm0').text.strip()
        price_digits = ''.join(filter(str.isdigit, price))
        price = int(price_digits)
    except AttributeError:
        price = None
    
    # area of the estate
    try:
        area = float(soup1.select_one('.gh-15dfr6w.e1kihjfm6:nth-of-type(3) p').text.strip().split(' ')[0].replace(',', '.'))
    except AttributeError:
        area = None
        
    # number of rooms
    try:
        rooms = soup1.select_one('.gh-15dfr6w.e1kihjfm6:nth-of-type(2) p').text.strip()
    except AttributeError:
        rooms = None
      
    # floor number
    try:
        floor = soup1.select_one('div.gh-z6h6j9.e1kihjfm5:nth-of-type(2) p').text.strip()
    except AttributeError:
        floor = None  
    
    record.extend((title, address, price, area, rooms, floor))
    
    return record

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
}

BASE_URL = "https://gethome.pl/nieruchomosci/gdansk/?price__gte=50000"

response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# number of pages
total_pages = int(soup.select_one('ul.gh-1wjowh8.e134q4pk1 li:nth-last-of-type(1)').text.strip())

data = []


for page in range(1, total_pages):
    
    URL = f'https://gethome.pl/nieruchomosci/gdansk/?page={page}&price__gte=50000'
    
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # list of URLs on page
    links = soup.select('a.o13k6g1y')
    links_list = ['https://gethome.pl' + link.get('href') for link in links]

    print(f'page {page} of {total_pages}')
    
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
        break
    
print(tabulate(data, headers=["title", "address", "price[PLN]", "area[m^2]", "rooms", "floor"], tablefmt='outline'))

print(f'\nTotal pages: {total_pages}')
print(f'\nTotal number of records: {len(data)}')