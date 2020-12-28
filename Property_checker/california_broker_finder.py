import requests
from bs4 import BeautifulSoup
import csv

#https://thebrokerlist.com/directory/california-commercial-real-estate-brokers

URL = 'https://thebrokerlist.com/directory/california-commercial-real-estate-brokers'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

page = requests.get(URL, headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')

def find_brokers(soup):
    title = soup.find_all("div", class_="listing")
    records = []
    for listing in title:
        #Name of person
        name = listing.h4.a.text.strip()
        print(name)
        profile_link = listing.h4.find('a', href=True)['href']
        #URL of profile page
        profile_URL = f'https://thebrokerlist.com{profile_link}'
        profile_page = requests.get(profile_URL, headers = headers)
        profile_soup = BeautifulSoup(profile_page.content, 'html.parser')

        profile_header = profile_soup.find("div", class_="indent")

        # retrieve phone numbers
        digits = []
        phone_numbers = profile_soup.find("div", class_="values phone_numbers_wrapper")
        if len(phone_numbers) > 1:
            for number in phone_numbers.span:
                digits.append(phone_numbers.text.strip())
            
        employer = ''
        if profile_header.a is not None:
            employer = profile_header.a.text.strip()
        else:
            employer = "Employer not available"
        
        #Email of person
        email = ''
        if profile_soup.find("div", class_="email") is not None:
            email = profile_soup.find("div", class_="email").text.strip()[7:]
        else:
            email = "Email is not available"
        #Location of person
        location = ''
        if profile_soup.find("div", class_="location") is not None:
            location = profile_soup.find("div", class_="location").text.strip()[10:]
        else:
            location = "Location not available"
        
        record = (name, employer, email, ''.join(digits).strip().replace('\n', ' '), location, profile_URL)
        records.append(record)
    write_to_file(records)

def write_to_file(records):
    with open('brokers.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Employer', 'Email', 'Number(s)', 'Location', 'Profile URL'])
        writer.writerows(records)
    
find_brokers(soup)