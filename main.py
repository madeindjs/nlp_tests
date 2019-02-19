import requests
from bs4 import BeautifulSoup

def main():
    r = requests.get('http://rousseau-alexandre.fr')
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.prettify())

if __name__ == '__main__':
    main()
