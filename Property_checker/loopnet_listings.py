import requests
from bs4 import BeautifulSoup
import csv

#https://www.loopnet.com/search/industrial-properties/los-angeles-ca/for-sale/?sk=386b4cc60cf2318989aad7d8be7d5d4c&bb=k-w4sqn-qNjs2-613D

URL = 'https://www.loopnet.com/Listing/10920-Hawthorne-Blvd-Inglewood-CA/20984496/'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

page = requests.get(URL, headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')

# features = soup.find_all('table')[0].find_all('tr')

features=soup.find_all('table')[0]
rows = features.find_all('tr')
for row in rows:
    cols=row.find_all('td')
    cols=[x.text.strip() for x in cols]
    print(cols)
