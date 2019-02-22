from bs4 import BeautifulSoup
import re
import requests

from spacy_lefff import LefffLemmatizer, POSTagger

import sys
from termcolor import colored, cprint

from .entity import Entity

import spacy
import pprint

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

####### CONSTANTE ##############
nltk.download('punkt')


class Page(object):
    """dans page: url, page_parent, nom de domaine, urls internes, url externes, mot_clef,"""

    EXTENSION_BLACKLIST = ('.png', '.jpg', '.gif', '.pdf', '.js', '.css')
    VALID_ENTITY_TYPES = ('ORG', 'PERSON')

    def __init__(self, url, root_url, site_url):
        self.url = url
        self.site_url = site_url
        self.root_url = root_url
        self.soup, self.code = self._get_soup()
        self._get_links()
        self._get_text()
        self._get_lang()

        if self.code == 200:
            cprint(self.url, 'green')
        else:
            cprint(self.url, 'red')

    def _get_soup(self):
        try:
            r = requests.get(self.url)
            s = BeautifulSoup(r.text, 'lxml')
            # print("code de la requête", r.status_code, " page: ", s.title)
            return s, r.status_code
        except:
            cprint("something went wrong. HTTP Code: {}".format(
                r.status_code), 'red')

    def _get_links(self):
        """get all links of the page (if mode internal=> only internal links)"""
        if self.code == 200:
            links = []

            for link in self.soup.find_all("a", href=True):
                href = link.get("href")

                if href != "#" and not href.endswith(self.EXTENSION_BLACKLIST):
                    links.append(href)

            intab_links = [self.site_url
                           + l for l in links if l.startswith("/")]

            intre_links = [
                self.url + l for l in links if re.match(r"^(?!(http|/|#\w|mailto))", l)]
            # print(intre_links)
            intex_links = [l for l in links if re.match(
                r"https?://{%s}.*" % self.root_url, l)]
            ext_links = [l for l in links if re.match(
                r"^https?(?!.*{%s}).*$" % self.root_url, l)]

            self.internal_links = list(
                set(intab_links + intex_links + intre_links))
            self.external_links = list(set(ext_links))

        else:
            self.internal_links = []

    def _get_text(self):
        """récupère le contenu de la page"""
        div_tags = ["h{}".format(i) for i in range(1, 6)]

        p_text = [x.text.replace("\n", " ") for x in self.soup.find_all(
            "p") if re.match(r"\w+", x.text)]
        div_text = {}

        for d in div_tags:
            div_text[d] = [x.text.replace("\n", " ")
                           for x in self.soup.find_all(d)]
        div_text["strong"] = [x.text.replace(
            "\n", " ") for x in self.soup.find_all("strong")]

        self.text = " ".join(p_text)
        self.remarkable = div_text

    def _get_lang(self):
        """get Lang of the page according to `<html lang='en' >` attribute"""
        self.lang = self.soup.find('html')['lang'][:2]

        self.nlp = spacy.load(self.lang)

        if self.lang == 'fr':
            french_lemmatizer = LefffLemmatizer()
            self.nlp.add_pipe(french_lemmatizer, name='lefff')

    def get_lemmes(self):
        tokens = word_tokenize(self.text)
        tokens = [w.lower() for w in tokens]
        #p_tag = pos_tag(tokens)

        # print(lemmes)
        doc = self.nlp(self.text)

        # for d in doc:
        #     print(d.text, d.pos_, d.tag_, d.lemma_)

        for entity in doc.ents:
            if entity.label_ in self.VALID_ENTITY_TYPES:
                print(Entity(entity))
