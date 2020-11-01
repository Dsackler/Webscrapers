import requests
from bs4 import BeautifulSoup
import smtplib

# This program looks at a raspberry pi camera and
# emails me if the price has fallen below a certain amount
# https://www.youtube.com/watch?v=Bg9r_yLk7VY&t=330s&ab_channel=DevEd

URL = 'https://www.amazon.com/Raspberry-Camera-Vision-IR-Cut-Longruner/dp/B07R4JH2ZV/ref=sr_1_6?dchild=1&keywords=raspberry+pi+camera&qid=1603577903&sr=8-6'
response = requests.get(URL)


headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}


def check_price():
    try:
        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id='productTitle').get_text()
        price = soup.find(id='priceblock_ourprice').get_text()
        # converts to float and only shows first 5 characters. It starts at the 1 index because the dollar sign cannot be converted to a float
        string_price_to_float = float(price[1:5])
        print(title.strip())
        print(price.strip())
        print(f"Here is the price in float form: {string_price_to_float}")

        if string_price_to_float < 23:
            send_mail()
        else:
            print("price has not dropped")

    except AttributeError:
        pass


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('avyskier@gmail.com', 'vnjqtzgmqrzuqgua')
    subject = 'Price fell down!'
    body = 'Check the link! \n https://www.amazon.com/Raspberry-Camera-Vision-IR-Cut-Longruner/dp/B07R4JH2ZV/ref=sr_1_6?dchild=1&keywords=raspberry+pi+camera&qid=1603577903&sr=8-6'
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'avyskier@gmail.com',
        'davidesackler@gmail.com',
        msg

    )

    print('Email has been sent!')

    server.quit()


check_price()

# while(True): if I want it to continually run and check once a day, I can uncomment this out and get rid of the check_price() call on line 57
#     check_price()
#     time.sleep(86400)
