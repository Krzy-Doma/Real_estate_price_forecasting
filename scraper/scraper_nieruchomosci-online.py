from bs4 import BeautifulSoup

import requests

from tabulate import tabulate
import pandas as pd

#! possible options: True - test with smaller output, False - normal output
TEST: bool = True

data: list = []

def estate_info(soup) -> list:
    """Takes a soup object and returns a list with the information about the estate.

    Args:
        soup (_type_): soup object

    Returns:
        list: list with the information about the estate
    """
    record: list = []
    
    # title
    try:
        title: str = soup.select_one('div#boxOffTop > h1').text.strip()
    except AttributeError:
        title = None
        
    # address
    try:        
        address: str = soup.select_one('div#boxOffTop > div > h2').text.strip()
    except AttributeError:
        address = None
        
    # price
    try:
        price: str = soup.select_one('span.info-primary-price').text.strip()
    except AttributeError:
        price = None
        
    # area
    try:        
        area: str = soup.select_one('span.info-area').text.strip()
    except AttributeError:
        area = None
        
    # rooms
    try:        
        rooms: str = soup.find('span', string='Liczba pokoi:').find_next_sibling('span').text.strip()
    except AttributeError:
        rooms = None
        
    # floor
    try:        
        floor: str = soup.find('span', string='Piętro:').find_next_sibling('span').text.strip() 
    except AttributeError:
        floor = None
        
    # build year
    try:
        build_year: str = soup.find('span', string='Rok budowy:').find_next_sibling('span').text.strip() 
    except AttributeError:
        build_year = None
        
    # parking
    try:
        parking: str = soup.find('span', string='Miejsce parkingowe:').find_next_sibling('span').text.strip() 
    except AttributeError:
        parking = None
        
    # market
    try:
        market: str = soup.find('strong', string='Rynek:').find_next_sibling('span').text.strip()
    except AttributeError:
        market = None
    
    # building type
    try:
        building_type: str = soup.find('strong', string='Budynek:').find_next_sibling('span').text.strip()
    except AttributeError:
        building_type = None

    record.extend((title, address, price, area, rooms, floor, market, build_year, parking, building_type))
    
    return record

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

BASE_URL = 'https://www.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Gda%C5%84sk'

response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

total_pages: int = int(soup.select_one('ul.pagination-mob-sub li:nth-last-of-type(2)').text.strip())

for page in range(1, total_pages):
    URL = f'https://www.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Gda%C5%84sk&p={page}'
    
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')   
    
    links = soup.select('a.tabCtrl')
    links_list: list = [link.get('href') for link in links]

    print(f'page {page} of {total_pages}')

    for index, link in enumerate(links_list):
        print(f'link {index + 1} of {len(links_list)}')
        
        request = requests.get(link, headers=headers)
        soup = BeautifulSoup(request.content, 'html.parser')

        record = estate_info(soup)
        data.append(record)
        
        if TEST is True and index == 1:
            break

    if TEST is True and page == 2:
        break
    
print(tabulate(data))
