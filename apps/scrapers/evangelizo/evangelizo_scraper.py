import requests
import json
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


versions = [
    {
        "base_url": "https://levangileauquotidien.org",
        "language": "FR",
    },
    {
        "base_url": "https://dailygospel.org",
        "language": "AM",
    },
    {
        "base_url": "https://evangeliodeldia.org",
        "language": "SP",
    },
    {
        "base_url": "https://evangeliumtagfuertag.org",
        "language": "DE",
    },
    {
        "base_url": "https://vangelodelgiorno.org",
        "language": "IT",
    },
    {
        "base_url": "https://alingilalyawmi.org",
        "language": "AR",
    },
    {
        "base_url": "https://alingilalyawmi.org",
        "language": "BYA",
    },
    {
        "base_url": "https://alingilalyawmi.org",
        "language": "COA",
    },
    {
        "base_url": "https://alingilalyawmi.org",
        "language": "SYA",
    },
    {
        "base_url": "https://alingilalyawmi.org",
        "language": "MAA",
    },
    {
        "base_url": "https://aroriaavedarane.org",
        "language": "ARM",
    },
]


class EvangelizoScraper:
    def __init__(self, index):
        self.base_url = versions[index]["base_url"]
        self.language = versions[index]["language"]

    def get_saint_list(self, date):
        params = {
            "language": self.language,
            "module": "allsaints",
            "type": "s",
            "localmonth": date.strftime("%m"),
            "localday": date.strftime("%d"),
            "localyear": date.strftime("%Y"),
        }
        res = requests.get(url="{}/main.php".format(self.base_url), params=params)
        soup = BeautifulSoup(res.content, 'html.parser')
        # If there is no saint
        if not soup.h4:
            return []
        saint_links = soup.h4.find_all_next('a')
        saint_url_list = [{
            "url": saint_link["href"],
            "name": saint_link.string,
            "id": int(saint_link["href"].split("&")[-2][3:])
        } for saint_link in saint_links]
        return saint_url_list

    def get_saint(self, url):
        res = requests.get(url="{}{}".format(self.base_url, url))
        soup = BeautifulSoup(res.content, 'html.parser')
        saint_name = soup.h3.string
        hagio = soup.find_all('table')[2].find_all('table')[1]
        image = hagio.find('img', {'height': ""})
        image_url = image["src"] if image else ""

        return {
            "name": saint_name,
            "hagio": str(hagio),
            "image_url": image_url,
        }


def save_saints_calendar(index, year):
    language = versions[index]["language"]
    start_date = datetime(year, 01, 01)
    end_date = datetime(year, 12, 31)
    day_count = (end_date - start_date).days + 1

    try:
        with open("data/data/{}_{}_saints_calendar.json".format(language, year), "rb") as f:
            saints_calendar = json.load(f)
    except:
        saints_calendar = {}

    for single_date in (start_date + timedelta(n) for n in range(day_count)):
        day_saints = EvangelizoScraper(index=index).get_saint_list(single_date)
        saints_calendar[single_date.strftime("%m-%d")] = day_saints

        with open("data/data/{}_{}_saints_calendar.json".format(language, year), "w") as f:
            json.dump(saints_calendar, f)


def save_saints_life(index, year):
    language = versions[index]["language"]
    with open("data/data/{}_{}_saints_calendar.json".format(language, year), "r") as f:
        saints_calendar = json.load(f)

    try:
        with open("data/data/{}_saints_life.json".format(language), "rb") as f:
            saints_life = json.load(f)
    except:
        saints_life = {}

    for day, saints_list in saints_calendar.iteritems():
        for saint in saints_list:
            # If saint is already here
            if saints_life.get(saint["id"], None):
                continue
            saint_life = EvangelizoScraper(index=index).get_saint(saint["url"])
            saint_life["feast_date"] = day
            saint_life["name_bis"] = saint["name"]
            saint_life["url"] = saint["url"]
            saints_life[saint["id"]] = saint_life
        with open("data/data/{}_saints_life.json".format(language), "w") as f:
            json.dump(saints_life, f)


if __name__ == '__main__':
    for index in [6, 7, 8, 9, 10]:
        for year in [2018, 2017]:
            save_saints_calendar(index=index, year=year)
            save_saints_life(index=index, year=year)
