'''
Test module for bin/stock_price_scraper
'''

import unittest
from datetime import datetime

import bin.stock_price_scraper as stock_price_scraper

class StockPriceScraperTest(unittest.TestCase):
    'Class to test scraper module'
    def test_cell(self):
        'Unit test for cell method'
        expected = 'A1'
        result = stock_price_scraper.cell('A', '1')
        self.assertEqual(expected, result)

    def test_price(self):
        'Unit test for price method'
        stock_code = 'VAS'
        url = f'http://samanvaykarambhe.com/{stock_code}'
        self.assertTrue(isinstance(float(stock_price_scraper.price(url)), float))

    def test_url(self):
        'Unit test for url method'
        expected = 'http://samanvaykarambhe.com/VAS'
        result = stock_price_scraper.url('http://samanvaykarambhe.com/', 'VAS')
        self.assertEqual(expected, result)

    def test_stock_prices(self):
        'Unit test for stock price scrapping'
        result = stock_price_scraper.StockPriceScraper(
            base_url='http://samanvaykarambhe.com/',
            stock_codes=['VAS', 'VTS'],
            google_sheet='',
            client_secret='',
            test=True
        ).stock_prices()
        for code, price in result.items():
            self.assertTrue(isinstance(float(price), float))

    def test_cell_update(self):
        'Unit test for cell update method online'
        google_client = stock_price_scraper.client('credentials/asx-scraper-credentials.json')
        sh = google_client.open('test')
        worksheet = sh.get_worksheet(0)
        stock_price_scraper.update_cell(worksheet, 'A1', '')
        stock_price_scraper.update_cell(worksheet, 'A1', 'Hello')
        self.assertEqual('Hello', worksheet.acell('A1').value)

    def test_stock_price_update(self):
        'Integration test for stock price scrapping and update'
        stock_price_scraper.StockPriceScraper(
            base_url='http://samanvaykarambhe.com/',
            stock_codes=['VAS', 'VTS'],
            google_sheet='test',
            client_secret='credentials/asx-scraper-credentials.json',
            test=False
        ).insert_prices()
        google_client = stock_price_scraper.client('credentials/asx-scraper-credentials.json')
        sh = google_client.open('test')
        worksheet = sh.worksheet(f'{datetime.today().strftime("%Y-%m-%d")}')
        self.assertEqual(
            ['VAS', '80.45', 'VTS', '102.1'],
            [worksheet.acell('A1').value, worksheet.acell('A2').value, worksheet.acell('B1').value, worksheet.acell('B2').value]
        )
