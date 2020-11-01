import requests
from bs4 import BeautifulSoup
import csv

# https://www.youtube.com/watch?v=_AeudsbKYG8&ab_channel=IzzyAnalytics

URL = 'https://www.amazon.com/s?k=raspberry+pi+camera&ref=nb_sb_noss_2'
response = requests.get(URL)


headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}


def check_listings():
    try:
        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        titles = soup.findAll(
            'div', {'data-component-type': 's-search-result'})

        records = []

        resultNumber = 1
        for title in titles:
            atag = title.h2.a
            description = atag.text.strip()
            productURL = 'https://www.amazon.com' + atag.get('href')
            price_parent = title.find('span', 'a-price')
            price = price_parent.find('span', 'a-offscreen').text
            rating = title.i.text
            print(
                f"Result number {resultNumber}: {description}\n Here is the URL: {productURL}\nHere is the price: {price}\n This products rating is {rating}\n\n")
            resultNumber = resultNumber + 1
            record = (description, price, rating, productURL)
            records.append(record)
        write_to_file(records)

    except AttributeError:
        pass


def write_to_file(records):
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'URL'])
        writer.writerows(records)


check_listings()
