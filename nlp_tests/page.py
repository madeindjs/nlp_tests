from bs4 import BeautifulSoup
import re
import requests

from spacy_lefff import LefffLemmatizer, POSTagger

import sys
from termcolor import colored, cprint

import spacy
import pprint

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag


####### CONSTANTE ##############
# nltk.download('punkt')
# nlp = spacy.load('fr')
# french_lemmatizer = LefffLemmatizer()
# nlp.add_pipe(french_lemmatizer, name='lefff')


class Page(object):
    """dans page: url, page_parent, nom de domaine, urls internes, url externes, mot_clef,"""

    def __init__(self, url, root_url, site_url):
        self.url = url
        self.site_url = site_url
        self.root_url = root_url
        self.soup, self.code = self.get_soup()

        if self.code == 200:
            cprint(self.url, 'green')
        else:
            cprint(self.url, 'red')

    def get_soup(self):
        try:
            r = requests.get(self.url)
            s = BeautifulSoup(r.text, 'lxml')
            # print("code de la requête", r.status_code, " page: ", s.title)
            return s, r.status_code
        except:
            cprint("something went wrong. HTTP Code: {}".format(r.status_code), 'red')

    def get_links(self):
        '''get all links of the page (if mode internal=> only internal links)'''
        if self.code == 200:
            links = [l.get("href") for l in self.soup.find_all(
                "a") if l.get("href") != "#"]  # --->

            intab_links = [self.site_url +
                           l for l in links if l.startswith("/")]
            intre_links = [
                self.url + "/" + l for l in links if re.match(r"^(?!(http|/|#\w|mailto))", l)]
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

    def get_text(self):
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

    def get_lemmes(self):
        tokens = word_tokenize(self.text)
        tokens = [w.lower() for w in tokens]
        #p_tag = pos_tag(tokens)

        # print(lemmes)
        doc = nlp(self.text)

        for d in doc:
            print(d.text, d.pos_, d.tag_, d.lemma_)

        for entity in doc.ents:
            print(entity.text, entity.label_)
