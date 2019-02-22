import argparse

from nlp_tests.site import Site


def parse_args():
    parser = argparse.ArgumentParser(
        description='Crawl website and extract usefull data.')
    parser.add_argument('website_url', type=str,
                        help='an integer for the accumulator')
    parser.add_argument('--limit', dest='limit_pages', default=300,
                        help='Max number of page to scrape')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    site = Site(args.website_url)
    page = site.factory_page(args.website_url)
    page.get_text()
    page.get_lemmes()
