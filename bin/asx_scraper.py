import urllib.request
from bs4 import BeautifulSoup

class AsxScraper:

    BASE_URL = 'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes='

    def __init__(self, stock_codes):
        self.stock_codes = stock_codes

    def insert_price(self):
        for stock_code in self.stock_codes:
            print(price(url(self.BASE_URL, stock_code)))

def price(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find('td', attrs={'class':'last'}).text.strip()

def url(base_url, stock_code):
    return f'{base_url}{stock_code.upper()}'