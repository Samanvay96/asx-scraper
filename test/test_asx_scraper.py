import unittest
import bin.asx_scraper as asx_scraper

class AsxScrapperTest(unittest.TestCase):

    def test_price(self):
        stock_code = 'VAS'
        url = f'https://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes={stock_code}'
        self.assertTrue(isinstance(float(asx_scraper.price(url)), float))

    def test_url(self):
        expected = 'helloworld.com/VAS'
        result = asx_scraper.url('helloworld.com/', 'vas')
        self.assertEqual(expected, result)

