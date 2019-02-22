import argparse
import logging

from nlp_tests.site import Site

# disable log messages from the Requests library
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Crawl website and extract usefull data.')
    parser.add_argument('website_url', type=str,
                        help='an integer for the accumulator')
    parser.add_argument('--limit', dest='limit', default=300,
                        help='Max number of page to scrape')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    site = Site(args.website_url, limit=args.limit)
    site.scrap_site()
    # page = site.factory_page(args.website_url)
    # page.get_text()
    # page.get_lemmes()
