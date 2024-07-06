import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import islice
import deepl
import os
from dotenv import load_dotenv

# init variables
load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

language_codes = {
    "albanian": "sq",
    "indonesian": "id",
    "arabic": "ar",
    "italian": "it",
    "bulgarian": "bg",
    "latvian": "lv",
    "chinese": "zh",
    "macedonian": "mk",
    "croatian": "hr",
    "malay": "ms",
    "czech": "cs",
    "norwegian": "no",
    "danish": "da",
    "polish": "pl",
    "dutch": "nl",
    "portuguese": "pt",
    "estonian": "et",
    "romanian": "ro",
    "finnish": "fi",
    "russian": "ru",
    "french": "fr",
    "serbian": "sr",
    "german": "de",
    "slovak": "sk",
    "greek": "el",
    "slovenian": "sl",
    "hebrew": "he",
    "spanish": "es",
    "hungarian": "hu",
    "swedish": "sv",
    "icelandic": "is",
    "turkish": "tr"
}


language = 'german'

# scraping the page 101languages.net page
url = f'https://www.101languages.net/{language}/most-common-{language}-words/'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'} # required to be able to access 101languages.net
page = requests.get(url, headers=headers).text

doc = BeautifulSoup(page, 'html.parser')

links = doc.find_all('a')

# get url of google sheet present on 101languages.net
raw_excel_url = next((link.get('href') for link in links if '2,000' in link.text), '')
print(raw_excel_url)

# converting the google sheet to csv so that pandas can read it
csv_url = raw_excel_url.rsplit('edit')[0] + 'export?format=csv'

df = pd.read_csv(csv_url)
list_of_words = df[language.capitalize()].tolist()

# init deepl translator
translator = deepl.Translator(DEEPL_API_KEY)

# compose anki deck txt file
num_of_words = 3 # number of most common words wanted

with open('mostCommonWords.txt', 'w', encoding='utf-8') as file:
    file.write('#separator:tab\n#html:true\n') # boilerplate Anki text
    for word in islice(list_of_words, num_of_words):
        translation_res = translator.translate_text(word, source_lang=language_codes[language.lower()], target_lang='EN-US')
        file.write(f'"{word}"\t"{translation_res.text}"\n')
