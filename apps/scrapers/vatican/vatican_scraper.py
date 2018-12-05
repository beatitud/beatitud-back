import requests
import json
from utils.scraping.beautiful_soup import BeautifulSoup, get_text_from_bs
from datetime import timedelta, datetime


class VaticanScraper:
    def __init__(self, language="fr"):
        self.host = "http://w2.vatican.va"
        self.content_path = "/content/francesco"
        self.language = language

    def get_content_index(self, content_type="homilies"):
        whole_index = list()
        for year in [2013, 2014, 2015, 2016, 2017, 2018]:
            complete = False
            page = 1
            while not complete:
                url = "{}{}/{}/{}/{}.index.{}.html"\
                    .format(self.host, self.content_path, self.language, content_type, year, page)
                res = requests.get(url)
                bs = BeautifulSoup(res.content, 'html.parser')
                index = bs.find("div", class_="vaticanindex")
                index_items = index.find_all("li")
                if not index_items:
                    complete = True
                else:
                    for index_item in index_items:
                        index_h1 = index_item.find('h1')
                        index_a = index_h1.a
                        # Most of the time, there is a link
                        if index_a:
                            link = index_a['href']
                            # Sometimes we just have a path
                            if 'http' not in link and link:
                                link = self.host + link
                            # Sometimes, link goes outside of the site, if it is the case,
                            # we don't index it
                            if self.host not in link:
                                continue
                            new_index = {
                                "url": link,
                                "label": index_h1.a.string,
                            }
                        # # But sometimes, content is not available for the specific
                        # # language, so there is no link, only a text
                        # else:
                        #     new_index = {
                        #         "url": '',
                        #         "label": index_h1.string,
                        #     }
                            whole_index.append(new_index)
                    page += 1
        return whole_index

    @staticmethod
    def get_content(index):
        """
        :param index: [{"url": "...", "label": "..."}, ...]
        :return: [{"url": "...", "label": "...", "title": "...", "date": "...", }, ...]
        """
        whole_content = list()
        for el in index:
            url = el.get("url")
            try:
                el["date"] = datetime\
                    .strptime(url.split("_")[1], "%Y%m%d")\
                    .strftime("%Y-%m-%d")  # We extract date from url
                el["id"] = url.split("_")[2][:-5]  # We remove .html and extract content id from url
            except:
                print("[*] Problem while parsing url: {}".format(url))
            res = requests.get(url)
            bs = BeautifulSoup(res.content, 'html.parser')
            content = bs.find(class_="testo")
            headers = content.find_all(align="center")
            el["headers"] = str(headers)
            for order, header in enumerate(headers):
                # We separate headers from rest of text
                head = header.extract()
                if order == 0:
                    el["date_title"] = get_text_from_bs(head)
                if order == 2:
                    el["context"] = get_text_from_bs(head)
                if order == 3:
                    # We try to collect youtube video url in iframe element
                    try:
                        multimedia_link = head.a['href']
                        multimedia_res = requests.get(multimedia_link)
                        multimedia_bs = BeautifulSoup(multimedia_res.content, 'html.parser')
                        i_frame = multimedia_bs.find('iframe')
                        if i_frame:
                            el["multimedia"] = i_frame['src']
                    except:
                        print("Problem with multimedia link for url : {}".format(url))

            el["content"] = str(content)
            whole_content.append(el)
        return whole_content


if __name__ == '__main__':
    vs = VaticanScraper()

    print("[*] Scraping index...")
    content_index = vs.get_content_index(content_type="homilies")
    print("[*] Index successfully scraped...")

    print("[*] Collecting content...")
    whole_content = vs.get_content(content_index)

    print("[*] Saving content...")
    import json
    with open('./apps/scrapers/vatican/pope_homilies.json', 'w') as f:
        json.dump(whole_content, f)
    print("[*] Done! =)")
