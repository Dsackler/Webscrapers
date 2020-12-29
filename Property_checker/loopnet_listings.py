import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://www.loopnet.com/search/industrial-properties/los-angeles-ca/for-sale/?sk=386b4cc60cf2318989aad7d8be7d5d4c&bb=k-w4sqn-qNjs2-613D'


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

page = requests.get(URL, headers = headers)
soup = BeautifulSoup(page.content, 'html.parser')


def loop_through_properties(soup):
    number = 2
    
    records = property_looper(soup)
    while number <= 20:
        URL = f'https://www.loopnet.com/search/industrial-properties/los-angeles-ca/for-sale/{number}/?sk=c26e49d5f6ad8b42edef8ed8b597bb50&bb=k-w4sqn-qNjs2-613D'
        page = requests.get(URL, headers = headers)
        pagesoup = BeautifulSoup(page.content, 'html.parser')
        for record in property_looper(pagesoup):
            records.append(record)
        number = number + 1

    write_to_file(records)
        

def write_to_file(records):
    with open('loopnet_properties.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Address','Price', 'Lot Size', 'Price Per SF', 'Rentable Building Area', 'Sale Type', 
                        'No. Stories', 'Cap Rate', 'Year Built/Renovated', 'Sale Conditions', 'Parking Ratio', 
                        'Property Type', 'Clear Ceiling Height', 'No. Drive In / Grade-Level Doors', 'Building Class', 'URL'])
        writer.writerows(records)

def property_looper(soup):
    records = []
    properties = soup.find_all(class_ = 'header-col')
    for prop in properties:
        propert = prop.text
        price = 'N/A'
        lot_size = 'N/A'
        price_per_sf = 'N/A'
        rentable_building_area = 'N/A'
        sale_type = 'N/A'
        number_stories = 'N/A'
        cap_rate = 'N/A'
        year_br = 'N/A'
        sale_conditions = 'N/A'
        parking_ratio = 'N/A' 
        property_type = 'N/A'
        clear_ceiling_height = 'N/A' 
        drive_in_doors = 'N/A'
        building_class = 'N/A'
        URL = ''
        prop_link = prop.h4.find('a', href=True)['href']
        URL = prop_link
        properties_page = requests.get(prop_link, headers = headers)
        property_page = BeautifulSoup(properties_page.content, 'html.parser')

        features = property_page.find_all('table')[0]
        rows = features.find_all('tr')
        property_info = []
        for row in rows:
            cols=row.find_all('td')
            for label in cols:
                property_info.append(label.text.strip())
            for i in range(0,len(property_info)):
                if property_info[i] == 'Price':
                    price = property_info[i + 1]
                if property_info[i] == 'Lot Size':
                    lot_size = property_info[i + 1]
                if property_info[i] == 'Price Per SF':
                    price_per_sf = property_info[i + 1]
                if property_info[i] == 'Rentable Building Area':
                    rentable_building_area = property_info[i + 1]
                if property_info[i] == 'Sale Type':
                    sale_type = property_info[i + 1]
                if property_info[i] == 'No. Stories':
                    number_stories = property_info[i + 1]
                if property_info[i] == 'Cap Rate':
                    cap_rate = property_info[i + 1]
                if property_info[i] == 'Year Built/Renovated':
                    year_br = property_info[i + 1]
                if property_info[i] == 'Sale Conditions':
                    sale_conditions = property_info[i + 1]
                if property_info[i] == 'Parking Ratio':
                    parking_ratio = property_info[i + 1]
                if property_info[i] == 'Property Type':
                    property_type = property_info[i + 1]
                if property_info[i] == 'Clear Ceiling Height':
                    clear_ceiling_height = property_info[i + 1]
                if property_info[i] == 'No. Drive In / Grade-Level Doors':
                    drive_in_doors = property_info[i + 1]
                if property_info[i] == 'Building Class':
                    building_class = property_info[i + 1]
        #print(f'''Property: {propert}\n Price: {price}\n Lot Size: {lot_size}\n Price per SF: {price_per_sf}\n Rentable Building Area {rentable_building_area}\n Sale Type: {sale_type}\n No. Stories: {number_stories}\n Cap Rate: {cap_rate}\n Year Built/Renovated: {year_br}\n Sale Conditions: {sale_conditions}\n Parking Ratio: {parking_ratio}\n Property Type: {property_type}\n Clear Ceiling Height: {clear_ceiling_height}\n No. Drive In / Grade-Level Doors: {drive_in_doors}\n Building Class: {building_class}\n''')
        
        
        record = (propert, price, lot_size, price_per_sf, rentable_building_area, sale_type, number_stories, cap_rate, year_br, sale_conditions, parking_ratio, property_type, clear_ceiling_height, drive_in_doors, building_class, URL)
        print(propert)
        records.append(record)
    return records
            


loop_through_properties(soup)
