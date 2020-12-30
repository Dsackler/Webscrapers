import requests
from bs4 import BeautifulSoup
import csv
import sys
import os

#template for URL
URL = f'https://www.showcase.com/ca/{sys.argv[1]}/warehouses/for-sale/'

#BeautifulSoup boiler plate
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
page = requests.get(URL, headers = headers)
soup = BeautifulSoup(page.content, 'html.parser')

#Function that returns address, price, price/sf, land/acre, land/sf, and URL of listing
def listings(soup):
    records = [] #To be written to file
    listings = soup.find_all("div", class_ = 'wrapper')
    links_to_properties = URL_finder(listings)
    for link in links_to_properties:
        property_page = requests.get(link, headers = headers)
        pagesoup = BeautifulSoup(property_page.content, 'html.parser')
        ADDRESS = pagesoup.find('div', class_ = 'street-address').text
        print(ADDRESS) #So user knows which address is being viewed
        details = pagesoup.find_all('div', class_ = 'details-header-data-wrapper')
        PRICE = 'Not available'
        PRICE_SF = 'Not available'
        LAND_ACRES = 'Not available'
        LAND_SF = 'Not available'
        URL = link
        #Retrieve information
        section_details = []
        for label in details:
            for section in label:
                section_details.append(section.text)
        for i in range(0,len(section_details)):
            if section_details[i] == 'PRICE':
                PRICE = section_details[i + 1]
            if section_details[i] == 'PRICE/SF':
                PRICE_SF = section_details[i + 1]
            if section_details[i] == 'LAND ACRES':
                LAND_ACRES = section_details[i + 1]
            if section_details[i] == 'LAND SF':
                LAND_SF = section_details[i + 1]
        record = (ADDRESS, PRICE, PRICE_SF, LAND_ACRES, LAND_SF, URL)
        records.append(record)
    write_to_file(records)

#Function to create URL for specific property listing
def URL_finder(listings):
    property_links = []
    for prop in listings:
        for href in prop.find_all('a', href=True):
            URL = href['href']
            prop_link = f'https://www.showcase.com{URL}' #Format of URL
            property_links.append(prop_link)
    return property_links

#Function to write information to csv file
def write_to_file(records):
    with open(f'Properties_in_area/{sys.argv[1]}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Address','Price', 'Price/SF', 'Land/acres', 'Land/SF', 'URL'])
        writer.writerows(records)


listings(soup)