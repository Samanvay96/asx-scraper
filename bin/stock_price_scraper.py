import urllib.request
from datetime import datetime
import string
from argparse import ArgumentParser

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from sortedcontainers import SortedDict


class StockPriceScraper:

    def __init__(self, base_url, stock_codes, google_sheet, client_secret, test):
        self.stock_codes = stock_codes
        self.base_url = base_url
        if not test:
            self.sheet = client(client_secret).open(google_sheet)

    def insert_prices(self):
        worksheet = self.sheet.add_worksheet(title=f'{datetime.today().strftime("%Y-%m-%d")}', rows='2', cols=f'{len(self.stock_codes)}')
        for i, (stock_code, stock_price) in enumerate(self.stock_prices().items()):
            self.update_sheet(worksheet, i, [stock_code, stock_price])

    def stock_prices(self):
        stock_prices = {}
        for stock_code in self.stock_codes:
            stock_prices[stock_code] = price(url(self.base_url, stock_code))
        return SortedDict(stock_prices)

    def update_sheet(self, worksheet, i, contents):
        for j, content in enumerate(contents):
            update_cell(worksheet, cell(string.ascii_uppercase[i], j+1), content)

def cell(letter, number):
    return f'{letter}{number}'

def update_cell(worksheet, cell, info):
    worksheet.update_acell(cell, info)

def client(client_secret):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)
    return gspread.authorize(creds)

def price(url):
    soup = make_soup(url)
    return scrape_price(soup)

def make_soup(url):
    page = urllib.request.urlopen(url)
    return BeautifulSoup(page, 'html.parser')

def scrape_price(soup):
    return soup.find('div', attrs={'class':'page-content entry-content'}).find('h2').text.strip()

def url(base_url, stock_code):
    return f'{base_url}{stock_code.upper()}'

if __name__ == '__main__':
    parser = ArgumentParser(description='Takes stock codes, scrapes prices from website and inserts into a given google sheet')
    parser.add_argument('-c', '--client-secret',   action='store',      help='the client',                                 type=str, dest='base_url',               required=True)
    parser.add_argument('-c', '--client-secret',   action='store',      help='the client',                                 type=str, dest='client_secret',               required=True)
    parser.add_argument('-g', '--google-sheet',    action='store',      help='the google sheet to insert prices into',     type=str, dest='google_sheet',                required=True)
    parser.add_argument('-s', '--stock-codes',     action='store',      help='the stock codes to get price for',           type=str, dest='stock_codes',      nargs='+', required=True)
    parser.add_argument('-t', '--test',            action='store_true', help='Perform test',                                         dest='test'                                      )
    args = parser.parse_args().__dict__
    StockPriceScraper(**args).insert_prices()