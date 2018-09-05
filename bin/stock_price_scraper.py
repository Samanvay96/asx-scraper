'''
This module when provided with an array of stock codes and scrape their stock prices
from a specified url and insert the prices into a google sheet.
'''
import urllib.request
from datetime import datetime
import string
from argparse import ArgumentParser

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

class StockPriceScraper:
    'Class to scrape stock prices and inserting them into a google sheet'

    def __init__(self, base_url, stock_codes, google_sheet, client_secret, test):
        self.stock_codes = stock_codes
        self.base_url = base_url
        if not test:
            self.sheet = client(client_secret).open(google_sheet)

    def insert_prices(self):
        'Add worksheet to spreadsheet and insert the stock prices into it'
        worksheet = self.sheet.add_worksheet(title=datestring(), rows='2', cols=col_num(self.stock_codes))
        for i, (stock_code, stock_price) in enumerate(self.stock_prices().items()):
            self.update_sheet(worksheet, i, [stock_code, stock_price])

    def stock_prices(self):
        'Get stock prices and build a dict with them'
        stock_prices = {}
        for stock_code in self.stock_codes:
            stock_prices[stock_code] = price(url(self.base_url, stock_code))
        return dict(sorted(stock_prices.items()))

    def update_sheet(self, worksheet, i, contents):
        'Update a worksheet from a dict, keys being the header'
        for j, content in enumerate(contents):
            update_cell(worksheet, cell(string.ascii_uppercase[i], j+1), content)

def cell(letter, number):
    'Construct a cell using a letter and number, eg. cell("A", "1") = "A1"'
    return f'{letter}{number}'

def update_cell(worksheet, cell, info):
    'Update a specified cell in worksheet with info'
    worksheet.update_acell(cell, info)

def client(client_secret):
    'Initialise a google client to access spreadsheets'
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)
    return gspread.authorize(creds)

def price(url):
    'Scrape price from given url'
    soup = make_soup(url)
    return scrape_price(soup)

def make_soup(url):
    'Make a soup object from url'
    page = urllib.request.urlopen(url)
    return BeautifulSoup(page, 'html.parser')

def scrape_price(soup):
    'Scrape price from a provided soup object'
    return soup.find('div', attrs={'class':'page-content entry-content'}).find('h2').text.strip()

def url(base_url, stock_code):
    'Construct url given a base_url and stock_code'
    return f'{base_url}{stock_code.upper()}'

def datestring():
    'Date string of today"s date'
    return f'{datetime.today().strftime("%Y-%m-%d")}'

def col_num(content):
    'String of content array length'
    return f'{len(content)}'

if __name__ == '__main__':
    parser = ArgumentParser(description='Takes stock codes, scrapes prices from website and inserts into a given google sheet')
    parser.add_argument('-c', '--client-secret',   action='store',      help='the client',                                 type=str, dest='base_url',               required=True)
    parser.add_argument('-c', '--client-secret',   action='store',      help='the client',                                 type=str, dest='client_secret',               required=True)
    parser.add_argument('-g', '--google-sheet',    action='store',      help='the google sheet to insert prices into',     type=str, dest='google_sheet',                required=True)
    parser.add_argument('-s', '--stock-codes',     action='store',      help='the stock codes to get price for',           type=str, dest='stock_codes',      nargs='+', required=True)
    parser.add_argument('-t', '--test',            action='store_true', help='Perform test',                                         dest='test'                                      )
    args = parser.parse_args().__dict__
    StockPriceScraper(**args).insert_prices()
