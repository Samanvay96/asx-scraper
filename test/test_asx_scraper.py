import unittest
import bin.asx_scraper as asx_scraper
import gspread
import ujson
from oauth2client.service_account import ServiceAccountCredentials

class AsxScrapperTest(unittest.TestCase):

    def test_cell(self):
        expected = 'A1'
        result = asx_scraper.cell('A', '1')
        self.assertEqual(expected, result)

    def test_price(self):
        stock_code = 'VAS'
        url = f'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes={stock_code}'
        self.assertTrue(isinstance(float(asx_scraper.price(url)), float))

    def test_url(self):
        expected = 'helloworld.com/VAS'
        result = asx_scraper.url('helloworld.com/', 'vas')
        self.assertEqual(expected, result)

    def test_stock_prices(self):
        result = asx_scraper.AsxScraper(stock_codes=['VAS', 'VTS'], google_sheet='', client_secret='', test=True).stock_prices()
        for code, price in result.items():
            self.assertTrue(isinstance(float(price), float))

    def test_cell_update(self):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials/asx-scraper-credentials.json', scope)
        gc = gspread.authorize(credentials)
        sh = gc.create('test_spreadsheet')
        worksheet = sh.get_worksheet(0)
        asx_scraper.update_cell(worksheet, 'A1', 'Hello')
        self.assertEqual('Hello', worksheet.acell('B1').value)