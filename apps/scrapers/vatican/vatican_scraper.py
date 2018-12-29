import requests
import json
from utils.scraping.beautiful_soup import BeautifulSoup, get_text_from_bs
from datetime import timedelta, datetime
import re


class VaticanScraper:
    AVAILABLE_LANGUAGES = ["fr", "en", "de", "it", "es", "pt", "ar"]

    def __init__(self, ):
        self.host = "http://w2.vatican.va"
        self.content_url = "{}/content".format(self.host)

    def get_popes(self, language="fr"):
        url = "{}/vatican/{}.html".format(self.content_url, language)
        res = requests.get(url)
        bs = BeautifulSoup(res.content, 'html.parser')
        pope_bs_list = bs.find(id='pope-scrollbar').find_all('a')
        pope_urls = map(lambda e: self.host + e['href'], pope_bs_list)
        pope_list = list()
        for pope_url in pope_urls:
            res = requests.get(pope_url)
            bs = BeautifulSoup(res.content, 'html.parser')
            pope_page = bs.find(class_='holy-father-page')
            name = pope_page.h1.get_text().strip()
            subtitle = pope_page.find(class_='subtitle').get_text().strip()
            link = bs.find('table', class_='sinottico').find('a')
            if 'holy-father' in pope_url:
                code = pope_url.split("/")[-1][:-5]
            # Particular case when pope link redirect directly to mixed page with pope index
            else:
                code = pope_url.split("/")[-2]
            if link:
                code = link['href'].split('/')[-2]
            pope_list.append({
                "name": name,
                "subtitle": subtitle,
                "code": code,
                "has_content": link != None,
            })
        return pope_list

    def get_index_menu(self, pope="francesco", language="fr"):
        url = "{}/{}/{}.html".format(self.content_url, pope, language)
        res = requests.get(url)
        bs = BeautifulSoup(res.content, 'html.parser')
        menu = bs.find(id="accordionmenu")
        link_elements = list()
        for li in menu.ul.findChildren("li", recursive=False):
            has_sub = li.has_attr('class') and 'has-sub' in li['class']
            if not has_sub:
                link_elements.append(li)
            else:
                li.a.extract()
                for sub_li in li.find_all('li'):
                    has_sub = sub_li.has_attr('class') and 'has-sub' in sub_li['class']
                    if not has_sub:
                        link_elements.append(sub_li)
                    else:
                        link_elements += sub_li.find_all('li')
        urls = list(map(lambda e: self.host + e.find('a')['href'], link_elements))
        return urls

    def get_index_content(self, index_url):
        params = index_url.replace(self.content_url, '').split('/')
        params.pop(0)  # We remove first element which is ''
        pope = params.pop(0)
        language = params.pop(0)
        content_type = params.pop(0).replace('.index.html', '')
        optional_params = params
        whole_index = list()
        complete = False
        page = 1
        while not complete:
            url = "{}.index.{}.html"\
                .format(index_url.replace('.index.html', ''), page)
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
                        if self.host not in link or not link:
                            continue
                        new_index = {
                            "url": link,
                            "label": index_h1.a.get_text().strip(),
                            "content_type": content_type,
                            "pope": pope,
                            "language": language,
                            "optional_params": optional_params,
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
    def get_content(index_dict):
        """
        :param index: {"url": "...", "label": "..."}
        :return: {"url": "...", "label": "...", "title": "...", "date": "...", }
        """
        url = index_dict.get("url")
        try:
            # Sometimes, there is no date in url (most of the time for the pope travels,
            # we don't handle this type of content)
            date_string = re.findall(r'\D(\d{8})\D', url)[0]
            index_dict["date"] = datetime\
                .strptime(date_string, "%Y%m%d")
        except:
            return None
        index_dict["code"] = url.split("/")[-1]\
            .replace('.html', '')  # We remove .html and extract content id from url
        res = requests.get(url)
        bs = BeautifulSoup(res.content, 'html.parser')
        content = bs.find(class_="testo")
        if not content:
            return None
        headers = content.find_all(align="center")
        index_dict["headers"] = str(headers)
        for order, header in enumerate(headers):
            # We separate headers from rest of text
            head = header.extract()
            if order == 0:
                index_dict["label2"] = get_text_from_bs(head)
            if order == 2:
                index_dict["label3"] = get_text_from_bs(head)
            if order == 3:
                # We try to collect youtube video url in iframe element
                try:
                    multimedia_link = head.a['href']
                    multimedia_res = requests.get(multimedia_link)
                    multimedia_bs = BeautifulSoup(multimedia_res.content, 'html.parser')
                    i_frame = multimedia_bs.find('iframe')
                    if i_frame:
                        index_dict["multimedia"] = i_frame['src']
                except:
                    print("Problem with multimedia link for url : {}".format(url))

        index_dict["content"] = str(content)
        return index_dict


if __name__ == '__main__':
    language = "en"
    vs = VaticanScraper()

    print("[*] Scraping index...")
    index_content = vs.get_index_content()
    print("[*] Index successfully scraped...")

    print("[*] Collecting content...")
    whole_content = list()
    for index_dict in index_content:
        whole_content.append(vs.get_content(index_dict))

    print("[*] Saving content...")
    import json
    with open('./apps/scrapers/vatican/pope_homilies_{}.json'.format(language), 'w') as f:
        json.dump(whole_content, f)
    print("[*] Done! =)")
