import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer as strainer
import json

import pprint
import ssl
import certifi

class PageToJson():

    def __init__(self):
        pass

    def get_title(self, html):
        title = None
        if html.title.string:
            title = html.title.string
        elif html.find("meta", property="og:title"):
            description = html.find("meta", property="og:title").get('content')
        elif html.find("meta", property="twitter:title"):
            description = html.find("meta", property="twitter:title").get('content')
        elif html.find("h1"):
            title = html.find("h1").string
        elif html.find_all("h1"):
            title = html.find_all("h1")[0].string
        if title:
            title = title.split('|')[0]
        return title


    def get_description(self, html):
        description = None
        if html.find("meta", property="description"):
            description = html.find("meta", property="description").get('content')
        elif html.find("meta", property="og:description"):
            description = html.find("meta", property="og:description").get('content')
        elif html.find("meta", property="twitter:description"):
            description = html.find("meta", property="twitter:description").get('content')
        elif html.find("p"):
            description = html.find("p").contents
        return description


    def get_image(self, html):
        image = None
        if html.find("meta", property="image"):
            image = html.find("meta", property="image").get('content')
        elif html.find("meta", property="og:image"):
            image = html.find("meta", property="og:image").get('content')
        elif html.find("meta", property="twitter:image"):
            image = html.find("meta", property="twitter:image").get('content')
        elif html.find_all("img", src=True):
            image = html.find_all("img")
            if image:
                image = html.find_all("img")[0].get('src')
        return image


    def get_site_name(self, html, url):
        if html.find("meta", property="og:site_name"):
            sitename = html.find("meta", property="og:site_name").get('content')
        elif html.find("meta", property='twitter:title'):
            sitename = html.find("meta", property="twitter:title").get('content')
        else:
            sitename = url.split('//')[1]
            return sitename.split('/')[0].rsplit('.')[1].capitalize()
        return sitename


    def get_favicon(self, html, url):
        if html.find("link", attrs={"rel": "icon"}):
            favicon = html.find("link", attrs={"rel": "icon"}).get('href')
        elif html.find("link", attrs={"rel": "shortcut icon"}):
            favicon = html.find("link", attrs={"rel": "shortcut icon"}).get('href')
        else:
            favicon = f'{url.rstrip("/")}/favicon.ico'
        return favicon


    def get_theme_color(self, html):
        if html.find("meta", property="theme-color"):
            color = html.find("meta", property="theme-color").get('content')
            return color
        return None

    def get_all_links_and_print_meta_data(self, url):
      
        final_json = {}
        main_meta = self.scrape_page_metadata('https://cnn.com')
        final_json['MAIN_PAGE'] = main_meta
        r = requests.get(url)
        html = BeautifulSoup(r.content, 'html.parser')
        all_links = set()
        for tag in html.find_all('a'):
            href = str(tag['href'])

            if href.startswith('http'):
                all_links.add(href)
            elif href.startswith('/'):
                all_links.add('https://cnn.com/' + href.lstrip("/"))

        for alink in all_links:
            meta_data = self.scrape_page_metadata(alink)
            final_json[alink] = meta_data

        print(json.dumps(final_json, indent=4))


    def scrape_page_metadata(self, url):
        """Scrape target URL for metadata."""
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        pp = pprint.PrettyPrinter(indent=4)
        r = requests.get(url, headers=headers)
        html = BeautifulSoup(r.content, 'html.parser')

        try:
            metadata = {
            'title': self.get_title(html),
            'description': self.get_description(html),
            'image': self.get_image(html),
            'favicon': self.get_favicon(html, url),
            'sitename': self.get_site_name(html, url),
            'color': self.get_theme_color(html),
            'url': url
            }
        except:
           return None
        #pp.pprint(metadata)
       
        return metadata


if __name__ == '__main__':

    p = PageToJson();
    p.get_all_links_and_print_meta_data('https://cnn.com')
