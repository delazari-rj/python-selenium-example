from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class ChartFunctions(unittest.TestCase):

	def setUp(self):
		self.browse = webdriver.Chrome()

	def test_serach(self):
		browse = self.browse
		try:
			browse.get('https://www.binance.com')
		except Exception as e:
			print(e)
		else:	
			browse.maximize_window()
			assert 'Bitcoin Exchange | Cryptocurrency Exchange | Binance' in browse.page_source
			browse.find_element_by_xpath('//*[@id="ba-tableMarkets"]').click()
			browse.find_element_by_xpath('//*[@id="__APP"]/div[1]/main/div/div[2]/div/div/div[2]/div[1]/div[1]/div/button[4]').click()
			
	def tearDown(self):
		time.sleep(15)
		self.browse.quit;

if __name__ == "__main__":
	unittest.main()



