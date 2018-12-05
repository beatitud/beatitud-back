import scriptures
import json
from utils.scraping.beautiful_soup import BeautifulSoup, get_text_from_bs

with open('./apps/scrapers/vatican/pope_homilies_en.json', 'r') as f:
    homilies = json.load(f)

for index, homily in enumerate(homilies):
    if index > 3:
        continue
    homily_bs = BeautifulSoup(homily.get("content"), 'html.parser')
    homily_text = get_text_from_bs(homily_bs)
    bible_refs = scriptures.extract(homily_text)
    print(homily_text)
    print('*'*50)
    print(bible_refs)
