import requests
import re
from bs4 import BeautifulSoup
import logging


class Website():

    def __init__(self, root_url):
        self.root_url = root_url
        self.pages_to_crawl = []
        self.url_crawled = []
        self.pages_to_crawl.append( Page(self.root_url) )

    def crawl(self):
        """Get the root page and start to walk between them"""
        while self.pages_to_crawl:
            page = self.pages_to_crawl.pop()
            # print(page.links)
            for link in page.links:
                if link not in self.url_crawled:
                    p = Page(self.root_url + link)
                    self.pages_to_crawl.append(p)
                    self.url_crawled.append(link)


class Page():

    @staticmethod
    def get_soup(url):
        """Build a Beautifull soup object from request result"""
        r = requests.get(url)
        return BeautifulSoup(r.text, 'html.parser')

    def __init__(self, url):
        """Initialize page and make a GET query"""
        # logger = logging.getLogger("nom_programme")
        # logger.info('Start crawling %s', url)
        print('Start crawling ' + url)
        self.url = url
        self.soup = Page.get_soup(self.url)
        self.links = self._get_links()
        # self.links = [l for l in self.get_links()]

    def _get_links(self, mode = 'all'):
        """Parse content and get all links"""
        for link in self.soup.findAll('a', attrs={'href': re.compile("^/")}):
            yield link.get('href')



def main():
    w = Website('http://rousseau-alexandre.fr')
    w.crawl()

if __name__ == '__main__':
    main()
