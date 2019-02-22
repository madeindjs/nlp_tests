# Some NLP tests

## Usage

### `parse_website.py`

~~~
$ python3 parse_website.py --help
usage: parse_website.py [-h] [--limit LIMIT_PAGES] website_url

Crawl website and extract usefull data.

positional arguments:
  website_url          an integer for the accumulator

optional arguments:
  -h, --help           show this help message and exit
  --limit LIMIT_PAGES  Max number of page to scrape
~~~

### `parse_book.py`

Parse a TXT book from <http://www.gutenberg.org>

## Instalation

~~~
$ pip3 install -r REQUIRMENTS.txt
$ python3 -m spacy download fr
~~~
