import pandas as pd

# url of google sheet present on 101languages.net
raw_url = "https://docs.google.com/spreadsheets/d/1VXTLrhgZ-HOOy65m7H76cPnm3z1jobbjp54CBs8nK2A/edit?gid=449211973#gid=449211973"

# converting the google sheet to csv so that pandas can read it
csv_url = raw_url.rsplit('edit')[0] + 'export?format=csv'

df = pd.read_csv(csv_url)
target_language = df.columns[1]
list_of_words = df[target_language].tolist()

with open('mostCommonWords.txt', 'w', encoding='utf-8') as file:
    for word in list_of_words:
        file.write(word + '\n')
