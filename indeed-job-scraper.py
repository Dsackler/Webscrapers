from bs4 import BeautifulSoup
import csv

# https://www.youtube.com/watch?v=eN_3d4JrL_w&t=599s&ab_channel=IzzyAnalytics

URL = 'https://www.indeed.com/jobs?q=computer%20science%20%2487%2C000&l=Los%20Angeles%2C%20CA&rbl=Los%20Angeles%2C%20CA&jlid=d05a4fe50c5af0a8&jt=fulltime&explvl=entry_level&taxo2=FregbhAzTjWUem4LngOP1g&vjk=6e3537b75e30494e'
response = requests.get(URL)
