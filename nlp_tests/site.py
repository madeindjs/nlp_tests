from urllib.parse import urlparse

from .page import Page

class Site(object):
    """dans site: mot clef, urls interne, url externe, nom de domaine, document_matrix"""

    def __init__(self, url, limit = 300):
        self.root_url = urlparse(url).netloc
        self.entry_point = url
        self.limit = int(limit)
        self.site_url = urlparse(url).scheme + "://" + self.root_url
        self.home_page = self.factory_page(url)

    # une factory method
    def factory_page(self, page_url):
        return Page(page_url, self.root_url, self.site_url)

    def scrap_site(self):
        self.home_page.get_links()
        pile = self.home_page.internal_links.copy()
        parsed = self.home_page.internal_links.copy()

        count = 0



        while pile != [] and count != self.limit:
            # Loop during pages exists or limit reached
            count += 1
            a = self.factory_page(pile[0])
            a.get_links()

            if a.code == 200:
                new_links = set(a.internal_links) - set(parsed)
                pile.extend(new_links)
                parsed.extend(new_links)

            pile.pop(0)
