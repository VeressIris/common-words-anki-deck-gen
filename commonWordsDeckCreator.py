import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import islice

language = 'german'

# scraping the page 101languages.net page
url = f'https://www.101languages.net/{language}/most-common-{language}-words/'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
page = requests.get(url, headers=headers).text

doc = BeautifulSoup(page, 'html.parser')

links = doc.find_all('a')

# url of google sheet present on 101languages.net
raw_excel_url = next((link.get('href') for link in links if '2,000' in link.text), '')
print(raw_excel_url)

# converting the google sheet to csv so that pandas can read it
csv_url = raw_excel_url.rsplit('edit')[0] + 'export?format=csv'

df = pd.read_csv(csv_url)
list_of_words = df[language.capitalize()].tolist()

num_of_words = 5 # number of most common words wanted
with open('mostCommonWords.txt', 'w', encoding='utf-8') as file:
    file.write('#separator:tab\n#html:true\n') # boilerplate Anki text
    for word in islice(list_of_words, num_of_words):
        file.write(f'"{word}"' + '\n')
