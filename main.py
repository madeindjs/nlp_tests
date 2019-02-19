import requests
import re
from bs4 import BeautifulSoup


class Website():
    """Represent a Website
    """

    def __init__(self, root_url):
        self.root_url = root_url
        self.page = []

    def crawl(self):
        first_page = Page(self.root_url, self.root_url)
        print([l for l in first_page.get_links()])



class Page():

    def __init__(self, url, root_url):
        self.url = url
        self.root_url = root_url
        self._initialise_soup()

    def get_links(self, mode = 'all'):
        for link in self.soup.findAll('a', attrs={'href': re.compile("^/")}):
            yield self.root_url + link.get('href')

    def _initialise_soup(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')




def main():
    w = Website('http://rousseau-alexandre.fr')
    w.crawl()

if __name__ == '__main__':
    main()
