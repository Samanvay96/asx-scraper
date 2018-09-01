import urllib.request
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

class AsxScraper:

    BASE_URL = 'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes='

    def __init__(self, stock_codes, google_sheet, client_secret):
        self.stock_codes = stock_codes
        self.sheet = client(client_secret).open(google_sheet)

    def insert_prices(self):
        worksheet = self.sheet.add_worksheet(title=f'{datetime.today().strftime("%Y-%m-%d")}', rows='2', cols=f'{len(self.stock_codes)}')
        for stock_code, stock_price in stock_prices(self.stock_codes).items():
            update_sheet(worksheet, stock_code, stock_price)

    def stock_prices(self, stock_codes):
        stock_prices = {}
        for stock_code in self.stock_codes:
            stock_prices[stock_code] = price(url(self.BASE_URL, stock_code))
        return stock_prices

    def update_sheet(self, worksheet, stock_code, stock_price):
        worksheet.update_acell('A1', f'{stock_code}')
        worksheet.update_acell('A2', f'{stock_price}')

def client(client_secret):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)
    return gspread.authorize(creds)

def price(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find('td', attrs={'class':'last'}).text.strip()

def url(base_url, stock_code):
    return f'{base_url}{stock_code.upper()}'