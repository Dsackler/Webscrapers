from bs4 import BeautifulSoup
import csv
from datetime import datetime
import requests

# https://www.youtube.com/watch?v=eN_3d4JrL_w&t=599s&ab_channel=IzzyAnalytics


def get_url(position, location, job_type):
    "Generate a URL"
    template = 'https://www.indeed.com/jobs?q={}&l={}&jt={}&vjk=73fed0c0413ab839'
    url = template.format(position, location, job_type)
    return url


url = get_url("computer science", "Los Angeles, CA", "fulltime")

response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')

jobs = soup.findAll('div', 'jobsearch-SerpJobCard')

job = jobs[0]

atag = job.h2.a

atag.get('title')

print(atag.get('title'))
