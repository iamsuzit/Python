"""1. Learning Web Sraping from tutorial using BeautifulSoup
   2. Import CSV file into SQL Server or do data cleaning using Pandas
   3. Visualize
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=business%20intelligence&l=United%20States&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    jobcards = soup.find_all('div', class_='slider_container')
    for item in jobcards:
        title = item.find('h2').text.strip().replace("new", "")
        company = item.find('span', class_='companyName').text.strip()
        location = item.find('div', class_='companyLocation').text.strip()
        try:
            salary = item.find('span', class_='salary-snippet').text.strip()
        except:
            salary = ''
        date_updated = item.find('span', class_='date').text.strip().replace('\n', '')

        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'date_updated': date_updated
        }
        joblist.append(job)
    return

joblist = []

for i in range(0, 9000, 10):
    print(f'Getting page {i}')
    c = extract(i)
    transform(c)


df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('BIjobs.csv')
