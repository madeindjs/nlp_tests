from spacy_lefff import LefffLemmatizer, POSTagger

import spacy
import pprint

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag


nltk.download('punkt')
nlp = spacy.load('fr')
french_lemmatizer = LefffLemmatizer()
nlp.add_pipe(french_lemmatizer, name='lefff',before='ner')


def main():
    with open('assets/zola-assommoir.txt', 'r') as content_file:
        content = content_file.read()
        # tokens = word_tokenize(content)
        # tokens = [w.lower() for w in tokens]
        #p_tag = pos_tag(tokens)

        chapters = content.split('\n\n')

        persons = []
        organisations = []
        locations = []

        for chapter in chapters:

            chapter = chapter.replace('\n', ' ')

            # print(lemmes)
            doc = nlp(u'%s'%chapter)

            for entity in doc.ents:
                # Get only persons
                if entity.label_ == 'PER':
                    persons.append(entity.text)

                # Get only locations
                if entity.label_ == 'LOC':
                    locations.append(entity.text)

                # Get only organisation
                if entity.label_ == 'ORG':
                    organisations.append(entity.text)
                # print(entity.text, entity.label_)

        uniq_organisations = list(sorted(set(organisations)))
        uniq_locations = list(sorted(set(locations)))
        uniq_persons = list(sorted(set(persons)))
        print(uniq_organisations)

if __name__ == '__main__':
    main()
